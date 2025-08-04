import os
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")

llm = ChatGroq(
    temperature=0,
    max_tokens=None,
    groq_api_key=groq_api_key,
    model_name="llama3-70b-8192"
)

llm2 = ChatGroq(
    temperature=0,
    max_tokens=None,
    groq_api_key=groq_api_key,
    model_name="llama3-70b-8192"
)
