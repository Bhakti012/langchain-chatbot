import streamlit as st
import requests

def upload_doc(file):
    response = requests.post(
        url = "http://localhost:8000/upload",
        files={"file": file}
    )

    if response.json()["status"] == "uploaded":
        return "pdf uploaded successfully"
     
def get_llm_response(input_text):
    response = requests.post(
        url="http://localhost:8000/ask",
        json= {"question": input_text}
    )     

    return response.json()

st.title("RAG: Document based Question and Answer")

uploaded_file = st.file_uploader("Upload a PDF", type="pdf")
if uploaded_file and st.button("Upload"):
    # message = upload_doc(uploaded_file)
    # st.success(message)
    try:
        message = upload_doc(uploaded_file)
        st.success(message)
    except Exception as e:
        st.error(str(e))


text_input = st.text_input("ask any question related to uploaded document")
if text_input:
    st.write(get_llm_response(text_input))

