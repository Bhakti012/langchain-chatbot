# Using ollama to integrate open source llms

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_ollama import OllamaLLM
from dotenv import load_dotenv
import os
import streamlit as st

load_dotenv()

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "you are a helpful assistant"),
        ("user", "Question: {question}")
    ]
)

st.title("phi3:mini: Hi, ask me any thing!")
input_text = st.text_input("Search your queries here!")

llm = OllamaLLM(model="phi3:mini")

output_parser = StrOutputParser()

chain = prompt|llm|output_parser

if input_text:
    st.write(chain.invoke({"question": input_text}))


