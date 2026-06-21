import streamlit as st
from langchain_groq import ChatGroq

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=st.secrets["GROQ_API_KEY"]
)

def ask_groq(prompt):
    response = llm.invoke(prompt)
    return response.content