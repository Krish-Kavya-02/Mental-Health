import streamlit as st
import time
from ragpipeline import create_rag_pipeline

st.set_page_config(
    page_title="🧠 MindMate Chatbot",
    layout="wide"
)
st.title("🧠 MindMate - Your Mental Health Chatbot")
st.markdown("Ask anything related to mental health. Your data stays private. 🤖")

# Load your chain once and cache it
@st.cache_resource(show_spinner="Loading Gemma & Chroma Vector Store...")
def get_chain():
    return create_rag_pipeline()

rag_chain = get_chain()

# ---------------------- Custom CSS ----------------------
st.markdown("""
    <style>
    .chat-container {
        background-color: #1E1E1E;
        padding: 1.5rem;
        border-radius: 1rem;
        max-height: 70vh;
        overflow-y: auto;
    }
    .user-bubble {
        background-color: #4CAF50;
        color: white;
        padding: 1rem;
        margin: 0.5rem 0 0.5rem auto;
        border-radius: 1rem;
        max-width: 75%;
        text-align: right;
    }
    .bot-bubble {
        background-color: #2E2E2E;
        color: #f0f0f0;
        padding: 1rem;
        margin: 0.5rem auto 0.5rem 0;
        border-radius: 1rem;
        max-width: 75%;
        text-align: left;
    }
    .bubble-text {
        font-size: 1rem;
        line-height: 1.4;
    }
    input[type="text"] {
        color: white !important;
    }
    </style>
""", unsafe_allow_html=True)

# Session state for chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Input container
with st.container():
    user_input = st.chat_input("How can I help you today?")

ask_with_followups = get_chain()  # Use the cached chain/function

# Handle user input
if user_input:
    start_time = time.time()
    with st.spinner("Gemma is thinking..."):
        history = [msg for role, msg in st.session_state.chat_history if role in ("user", "bot")]
        response = ask_with_followups(user_input, history)
        answer = response.get("answer", response.get("result", ""))
    end_time = time.time()

    elapsed_time = round(end_time - start_time, 2)
    print(f"🕒 Model response time: {elapsed_time} sec")  #Backend log

    # Save messages to history
    st.session_state.chat_history.append(("user", user_input))
    st.session_state.chat_history.append(("bot", answer))

# Display chat history
st.markdown('<div class="chat-container">', unsafe_allow_html=True)
for role, message in st.session_state.chat_history:
    if role == "user":
        st.markdown(f'<div class="user-bubble"><div class="bubble-text">{message}</div></div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="bot-bubble"><div class="bubble-text">{message}</div></div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
 