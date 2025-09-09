import streamlit as st
from sidebar import model_selection
from chat_interface import display_chat_interface

st.title("Langchain RAG Chatbot")

# Initialize session state variables
if "messages" not in st.session_state:
    st.session_state.messages = []

if "session_id" not in st.session_state:
    st.session_state.session_id = None

## Show the model section in sidebar
model_selection()

# Display the chat interface
display_chat_interface()