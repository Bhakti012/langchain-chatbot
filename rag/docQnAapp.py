#project: build a fastAPI QnA app using streamlit for frontend which takes a pdf doc from user and user asks question from that pdf
# give output

# questions:
#   explain this line loader = PyPDFLoader("sample.pdf"), if loader.load() gives the docs then what does this do?
#   what does documents = text_splitter.split_text(docs) line does? I mean I understand that text_splitter= RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
#    is just a config of how to split text but this line, what is does?  
#   is embeddings = OllamaEmbeddings(model="nomic-embed-text") also just setting config for embedding?
#  explain very simply what exactly is retriever = db.as_retriever() doing? is it internally using a certain similarity serach algorithm
#   to retrive relevant details? if so where is the the value for which it is seraching? or it a configuration? how does retriver take input?
#  what typically comes in langchain_community and  langchain_core? what kind of packages, I keep getting confused
# whats BaseModel why does schema class need to inherit from it always?

from fastapi import FastAPI, UploadFile, File, HTTPException
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OllamaEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import OllamaLLM
from langchain_core.runnables import RunnablePassthrough
# from langserve import add_routes
import uvicorn
import shutil
from schema import QuestionRequest
import os

app = FastAPI(title="RAG: Document based question and answer", version="1.0.0")

db = None

#uploadfile path
@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):

    global db
    upload_path = os.path.join(os.getcwd(), "doc.pdf")

    with open(upload_path, "wb") as f:
        shutil.copyfileobj(file.file, f)
    
    await file.close() # this is closing the uploaded temp file, f is closed automatically
    
    # preprocessing: loading, chunking
    loader = PyPDFLoader(upload_path)
    docs = loader.load()
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    documents = text_splitter.split_documents(docs)

    # vector embeddings and store in db
    embeddings = OllamaEmbeddings(model="nomic-embed-text")

    db = FAISS.from_documents(documents, embeddings)

    return {
    "filename": file.filename,
    "status": "uploaded"
    }  

    
@app.post("/ask")
async def ask_question(request: QuestionRequest):
    global db

    # prepare prompt and take input
    prompt = ChatPromptTemplate.from_template(
        """ Based only on the given context
        give appropriate answer to the following question
        
        <context>
            {context}
        </context>
            
        Question: {question}"""
    )

    llm = OllamaLLM(model="phi3:mini")

    if db is None:
        raise HTTPException(status_code=400, detail="Error: Upload file first")

    # retrive on basis of input
    retriever = db.as_retriever()

    rag_chain = (
        {
        "context": retriever,
        "question": RunnablePassthrough() 
        }
        |prompt
        |llm
    )

    return rag_chain.invoke(request.question)


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)


# # prepare prompt and take input
# prompt = ChatPromptTemplate.from_template(
#     """ Based only on the given context
#        give appropriate answer to the following question
       
#        <context>
#         {context}
#        </context>
        
#        Question: {question}"""
# )

# llm = OllamaLLM(model="phi3:mini")

# # retrive on basis of input
# retriever = db.as_retriever()

# rag_chain = (
#     {
#        "context": retriever,
#        "question": RunnablePassthrough() 
#     }
#     |prompt
#     |llm
# )

# add_routes(
#     app=app,
#     runnable=rag_chain,
#     path="/rag_bot"
# )


   
 






