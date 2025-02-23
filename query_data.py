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
CHROMA_PATH = "/data/chromadb"

PROMPT_TEMPLATE = """
You are an AI assistant representing the City of Kingston, Ontario. Your role is to provide accurate, well-structured, and legally compliant answers regarding local bylaws, rules, and regulations. 

**Guidelines for Answering:**
1️**Use Only Provided Context**: Only answer using the information retrieved from the Kingston regulations dataset. If the answer is not available in the data, respond with:  
   *"I'm sorry, but I couldn't find this information in my records. You may check [Kingston's official website](https://www.cityofkingston.ca/) for more details."*  
   
2️**Include Document Sources**: If the response is based on a document, always mention its name. Example:  
   - *"According to the 'Noise Regulation Act 2023', you cannot play loud music past 11 PM."*  

3️**Be Concise & Professional**: Avoid unnecessary details. Keep responses brief yet informative.  

4️**Suggest Related Topics**: If relevant, suggest other topics the user may find useful.  

---
** You will need to give links to the documents when necessory. **

🔍 **Context (Extracted Laws & Regulations):**  
{context}

❓ **User Question:**       
{question}

💡 **Answer in a Clear & Concise Manner:**
"""

class EnhancedQueryProcessor:
    def __init__(self):
        if not os.getenv("OPENAI_API_KEY"):
            raise ValueError("OPENAI_API_KEY environment variable is not set. Please set it to use OpenAI services.")

        self.embedding_function = OpenAIEmbeddings()
        self.db = Chroma(persist_directory=CHROMA_PATH, embedding_function=self.embedding_function)
        self.llm = ChatOpenAI(model_name="gpt-4-turbo", temperature=0.7)
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
