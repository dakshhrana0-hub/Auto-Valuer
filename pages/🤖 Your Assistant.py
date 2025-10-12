import streamlit as st
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

# ------------------------------
# Setup
# ------------------------------
load_dotenv()
API_KEY = os.getenv(".GROQ_API_KEY")

st.set_page_config(page_title="Chat with Groq", layout="centered")
st.title("💬 Chat with Assistant")

# ------------------------------
# Sidebar Info
# ------------------------------
with st.sidebar:
    st.markdown("### ℹ️ About This Chat")
    st.write("This assistant uses Groq's LLaMA 4 model for fast, intelligent responses.")
    st.write("You can ask questions, get summaries, or explore ideas.")
    st.write("Chat history is preserved during the session for smarter replies.")

# ------------------------------
# Initialize Chat Model
# ------------------------------
llm = ChatGroq(
    model="meta-llama/llama-4-scout-17b-16e-instruct",
    temperature=0.7,
    max_retries=2,
    groq_api_key=API_KEY
)

# ------------------------------
# Session State for Chat History
# ------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = [{
        "role": "assistant",
        "content": "👋 Hi there! I'm your assistant powered by Groq. Ask me anything!",
    }]

# ------------------------------
# Display Chat History
# ------------------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ------------------------------
# Chat Input
# ------------------------------
user_input = st.chat_input("Type your message...")

if user_input:
    st.chat_message("user").markdown(user_input)
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    # Build full context for Groq
    full_prompt = ""
    for msg in st.session_state.messages:
        full_prompt += f"{msg['role'].capitalize()}: {msg['content']}\n"

    # Query Groq model
    try:
        response = llm.invoke(full_prompt)
        bot_reply = response.content.strip()
    except Exception:
        bot_reply = "⚠️ Sorry, something went wrong while connecting to Groq."

    # Show bot reply
    st.chat_message("assistant").markdown(bot_reply)
    st.session_state.messages.append({
        "role": "assistant",
        "content": bot_reply
    })
