LangChain + FastAPI Chatbot

This is a simple AI chatbot built using:
FastAPI
LangChain
OpenAI
Streamlit

It takes user input and returns an AI-generated response.

Setup Instructions:
1️.Clone Repository
   git clone <repo-url>
   
2️.Create Virtual Environment
   python -m venv myenv
   Activate (Windows):
    myenv\Scripts\activate

3️.Install Dependencies
   pip install -r requirements.txt
   If streaming error occurs:
    pip install sse_starlette

4️.Run Backend
   uvicorn api.app:app --reload

5️.Run Frontend
   streamlit run chatbot/app.py
