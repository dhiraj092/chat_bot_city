import argparse
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_community.vectorstores import Chroma
from dotenv import load_dotenv
import os
import logging
from typing import Dict  


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()
CHROMA_PATH = "chroma"

PROMPT_TEMPLATE = """
You are a highly knowledgeable and reliable Regulatory Compliance Chatbot designed to provide accurate, up-to-date, and well-structured answers to users' questions about rules, laws, and regulations. Your goal is to assist users in understanding compliance requirements, legal frameworks, and policy guidelines while maintaining clarity and accessibility.

Use the following context to answer the user's question. If the context is not relevant, use your general knowledge to provide a helpful response.

Also tell them where they can find more information. 

Context:
{context}

Question:
{question}

Answer the question directly and concisely:
"""

class EnhancedQueryProcessor:
    def __init__(self):
        if not os.getenv("OPENAI_API_KEY"):
            raise ValueError("OPENAI_API_KEY environment variable is not set. Please set it to use OpenAI services.")

        self.embedding_function = OpenAIEmbeddings()
        self.db = Chroma(persist_directory=CHROMA_PATH, embedding_function=self.embedding_function)
        self.llm = ChatOpenAI(temperature=0.7)
        self.chat_prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)

    def process_query(self, query_text: str) -> Dict:
        """Process user query."""
        try:
            results = self.db.similarity_search(query_text, k=3)
            local_context = "\n".join([doc.page_content for doc in results]) if results else ""

            response = self.llm.invoke(
                self.chat_prompt.format(
                    context=local_context,
                    question=query_text
                )
            ).content

            return {"response": response}

        except Exception as e:
            logger.error(f"Error processing query: {e}")
            return {"error": str(e)}


if __name__ == "__main__":
    processor = EnhancedQueryProcessor()

    print("Welcome to the Regulatory Compliance Chatbot! Type 'exit' to quit.")
    while True:
        query = input("You: ").strip()

        # Exit condition
        if query.lower() == "exit":
            print("Goodbye! 👋")
            break

        # Process the query
        result = processor.process_query(query)

        # Print the result
        if "response" in result:
            print(f"Bot: {result['response']}")
        else:
            print(f"Bot: Sorry, I encountered an error: {result['error']}")