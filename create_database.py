from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from dotenv import load_dotenv
import os
import logging
import shutil

# Load environment variables
load_dotenv()

# Logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define constants
CHROMA_PATH = "chroma"  # Persistent path
DATA_PATH = "data"  # Folder with PDFs

# Set OpenAI API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def main():
    generate_data_store()

def generate_data_store():
    documents = load_documents()
    if not documents:
        logger.error("No documents were loaded! Check your data folder.")
        return

    chunks = split_text(documents)
    save_to_chroma(chunks)

def load_documents():
    """Loads PDF documents from the specified directory."""
    documents = []
    for pdf_file in os.listdir(DATA_PATH):
        if pdf_file.endswith(".pdf"):
            logger.info(f"Loading PDF: {pdf_file}")
            loader = PyPDFLoader(os.path.join(DATA_PATH, pdf_file))
            documents.extend(loader.load())

    logger.info(f"Total documents loaded: {len(documents)}")
    return documents

def split_text(documents):
    """Splits documents into smaller chunks."""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=300,
        chunk_overlap=100,
        length_function=len,
        add_start_index=True,
    )
    chunks = text_splitter.split_documents(documents)
    logger.info(f"Total chunks created: {len(chunks)}")
    return chunks

def save_to_chroma(chunks):
    """Saves text chunks into a ChromaDB vector store."""
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)

    db = Chroma.from_documents(
        chunks, OpenAIEmbeddings(), persist_directory=CHROMA_PATH
    )
    db.persist()
    logger.info(f"Saved {len(chunks)} chunks to ChromaDB at {CHROMA_PATH}.")

if __name__ == "__main__":
    main()
