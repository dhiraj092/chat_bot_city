import streamlit as st
from openai import OpenAI
from langchain_openai import OpenAIEmbeddings
from langchain.prompts import ChatPromptTemplate
from langchain_community.vectorstores import Chroma
from dotenv import load_dotenv
import os
import logging
from typing import Dict, List

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()
CHROMA_PATH = "chroma"

PROMPT_TEMPLATE = """
You are an AI assistant representing the City of Kingston, Ontario. Your role is to provide accurate, well-structured, and legally compliant answers regarding local bylaws, rules, and regulations. 

**Guidelines for Answering:**
1️⃣ **Use Only Provided Context**: Only answer using the information retrieved from the Kingston regulations dataset. If the answer is not available in the data, respond with:  
   *"I'm sorry, but I couldn't find this information in my records. You may check [Kingston's official website](https://www.cityofkingston.ca/) for more details."*  
   
2️⃣ **Include Document Sources**: If the response is based on a document, always mention its name. Example:  
   - *"According to the 'Noise Regulation Act 2023', you cannot play loud music past 11 PM."*  

3️⃣ **Be Concise & Professional**: Avoid unnecessary details. Keep responses brief yet informative.

4️⃣ **Suggest Related Topics**: If relevant, suggest other topics the user may find useful.

Previous conversation context:
{chat_history}

🔍 **Context (Extracted Laws & Regulations):**  
{context}

❓ **User Question:**       
{question}

💡 **Answer in a Clear & Concise Manner:**
"""

class EnhancedQueryProcessor:
    def __init__(self):
        """Initialize the chatbot, embeddings, and database."""
        if not os.getenv("OPENAI_API_KEY"):
            raise ValueError("OPENAI_API_KEY environment variable is not set. Please set it to use OpenAI services.")
        
        self.client = OpenAI()
        self.embedding_function = OpenAIEmbeddings()
        self.db = Chroma(persist_directory=CHROMA_PATH, embedding_function=self.embedding_function)
        self.chat_prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)

    def process_query(self, query_text: str, chat_history: List[Dict]) -> Dict:
        """Process user query and return AI-generated response."""
        try:
            # Get relevant documents
            results = self.db.similarity_search(query_text, k=3)
            local_context = "\n".join([doc.page_content for doc in results]) if results else ""

            # Format chat history
            formatted_history = "\n".join([
                f"User: {exchange['user']}\nAssistant: {exchange['assistant']}"
                for exchange in chat_history
            ])

            # Create messages for the chat
            messages = [
                {"role": "system", "content": self.chat_prompt.format(
                    context=local_context,
                    chat_history=formatted_history,
                    question=query_text
                )},
            ]

            # Add chat history
            for exchange in chat_history:
                messages.append({"role": "user", "content": exchange["user"]})
                messages.append({"role": "assistant", "content": exchange["assistant"]})
            
            # Add current query
            messages.append({"role": "user", "content": query_text})

            # Get response from OpenAI
            response = self.client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=messages,
                temperature=0.7,
            )

            return {"response": response.choices[0].message.content}
        except Exception as e:
            logger.error(f"Error processing query: {e}")
            return {"error": str(e)}

# Initialize session state for chat history
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Initialize the chatbot processor
if 'processor' not in st.session_state:
    st.session_state.processor = EnhancedQueryProcessor()

# Streamlit UI
st.set_page_config(page_title="City of Kingston Chatbot", page_icon="🏛️", layout="wide")
st.title("🏛️ City of Kingston Chatbot")
st.write("Ask any question about Kingston's local bylaws and regulations!")

# Chat interface
query = st.text_input("Enter your question:")

if query:
    with st.spinner("Processing..."):
        result = st.session_state.processor.process_query(
            query, 
            st.session_state.chat_history
        )
    
    if "response" in result:
        # Add to chat history
        st.session_state.chat_history.append({
            "user": query,
            "assistant": result["response"]
        })
    else:
        st.error(f"Error: {result['error']}")

# Display chat history
st.write("### 💬 Chat History:")
for exchange in st.session_state.chat_history:
    st.write("**You:** " + exchange["user"])
    st.write("**Assistant:** " + exchange["assistant"])
    st.markdown("---")

# Clear chat button
if st.button("Clear Chat History"):
    st.session_state.chat_history = []
    st.experimental_rerun()

st.markdown("---")
st.write("🔗 Visit the [City of Kingston Official Website](https://www.cityofkingston.ca/) for more details.")