# routes of api using langserve and Fastapi

from fastapi import FastAPI
from langserve import add_routes
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate 
import uvicorn

app = FastAPI(
    title="My LangChain Chat App",
    version="1.0",
    description="Simple Langchain chatbot demo"
)

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "you are a helpful assistant"),
        ("user", "Question: {topic}")
    ]
)
llm = OllamaLLM(model="phi3:mini")

add_routes(
    app,
    prompt|llm,
    path="/chat"
)

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)

