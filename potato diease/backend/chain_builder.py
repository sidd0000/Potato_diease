# backend/chainbuilder.py

import os
from dotenv import load_dotenv
from langchain.schema import HumanMessage
from langchain.chat_models import ChatGoogleGenerativeAI

load_dotenv()

def get_chain():
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        google_api_key=os.getenv("GEMINI_API_KEY")
    )
    return llm

def run_chain(image_description: str) -> str:
    llm = get_chain()
    messages = [HumanMessage(content=f"Analyze this leaf description: {image_description}")]
    response = llm(messages)
    return response.content
