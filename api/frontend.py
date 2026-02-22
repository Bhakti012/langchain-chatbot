#  frontend using streamlit

import requests
import streamlit as st

def get_llm_response(input_text):
    response = requests.post(
        url="http://localhost:8000/poem/invoke",
        json={"input": {"topic": input_text}}
    )

    return response.json()["output"]

st.title("My LangChain Chat App")
input_text = st.text_input("Poem on what topic...")

st.write(get_llm_response(input_text))