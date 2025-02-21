from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from dotenv import load_dotenv
import openai
import os
import shutil
import logging
from langchain_community.document_loaders import PyPDFLoader

load_dotenv()

logging.basicConfig(level=logging.INFO)

CHROMA_PATH = "chroma"
DATA_PATH = "data"

openai.api_key = os.environ['OPENAI_API_KEY']

def main():
    generate_data_store()

def generate_data_store():
    documents = load_documents()
    chunks = split_text(documents)
    save_to_chroma(chunks)

def load_documents():
    """Loads PDF documents from the specified directory."""
    documents = []
    for pdf_file in os.listdir(DATA_PATH):
        if pdf_file.endswith(".pdf"):
            loader = PyPDFLoader(os.path.join(DATA_PATH, pdf_file))
            documents.extend(loader.load())
    logging.info(f"Loaded {len(documents)} documents.")
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
    logging.info(f"Split {len(documents)} documents into {len(chunks)} chunks.")
    return chunks

def save_to_chroma(chunks):
    """Saves text chunks into a ChromaDB vector store."""
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)

    db = Chroma.from_documents(
        chunks, OpenAIEmbeddings(), persist_directory=CHROMA_PATH
    )
    db.persist()
    logging.info(f"Saved {len(chunks)} chunks to {CHROMA_PATH}.")

if __name__ == "__main__":
    main()
