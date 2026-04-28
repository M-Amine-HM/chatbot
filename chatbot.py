import requests
import streamlit as st
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- Constants and Configuration ---
API_URL = os.getenv("API_URL", "http://localhost:1234/v1/chat/completions")
MODEL = os.getenv("MODEL", "mistral-7b-instruct-v0.3")
DEFAULT_SYSTEM_PROMPT = os.getenv(
    "DEFAULT_SYSTEM_PROMPT", "You are a helpful AI assistant.")

st.set_page_config(page_title="AI Chatbot", page_icon="")
st.title("AI Chatbot")
st.caption(f'Powered by **{MODEL}** via LM Studio')

# Initialize history (NO system role anymore)
if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar
with st.sidebar:
    temperature = st.slider("Temperature", 0.0, 2.0, 0.7)
    max_tokens = st.slider("Max tokens", 50, 2048, 512)
    new_system = st.text_area("System prompt", value=SYSTEM_PROMPT)

    if st.button("Apply"):
        SYSTEM_PROMPT = new_system

    if st.button("🗑️ Clear conversation"):
        st.session_state.messages = []
        st.rerun()

# User input
if user_input := st.chat_input("Type your message..."):

    # Show user message
    with st.chat_message("user"):
        st.write(user_input)

    # 🔥 Inject system prompt into user message
    full_prompt = f"{SYSTEM_PROMPT}\n\nUser: {user_input}"

    # Add to history (as user only)
    st.session_state.messages.append({
        "role": "user",
        "content": full_prompt
    })

    # Call LM Studio
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = requests.post(API_URL, json={
                    "model": MODEL,
                    "temperature": temperature,
                    "max_tokens": max_tokens,
                    "messages": st.session_state.messages
                }, timeout=60)

                answer = response.json()["choices"][0]["message"]["content"]

                st.write(answer)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer
                })

            except requests.exceptions.ConnectionError:
                st.error("❌ LM Studio not running on port 1234")
