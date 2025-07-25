import streamlit as st
import time
from ragpipeline import create_rag_pipeline
import os
from dotenv import load_dotenv

load_dotenv()

# Page config
st.set_page_config(
    page_title="🧠 MindMate Chatbot",
    layout="centered"
)

st.title("🧠 MindMate - Your Mental Health Chatbot")
st.markdown("Ask anything related to mental health. Your data stays private. 🤖")

# Session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Load RAG pipeline
@st.cache_resource(show_spinner="Loading MindMate & Chroma Vector Store...")
def get_chain():
    return create_rag_pipeline()

ask_with_followups = get_chain()

# ---------------------- ✅ Custom Dark Mode + Scroll CSS ----------------------
st.markdown("""
    <style>
    body {
        background-color: #121212;
        color: #FFFFFF;
    }
    .main {
        background-color: #121212;
        color: white;
    }
    .chat-container {
        max-width: 750px;
        margin: 20px auto;
        background-color: #1E1E1E;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0px 0px 10px rgba(255,255,255,0.05);
        max-height: 60vh;
        overflow-y: auto;
        scroll-behavior: smooth;
    }
    .message {
        padding: 10px 15px;
        border-radius: 10px;
        max-width: 75%;
        margin-bottom: 10px;
        font-size: 15px;
        line-height: 1.5;
        word-wrap: break-word;
    }
    .user-msg {
        background-color: #1976d2;
        color: white;
        margin-left: auto;
        text-align: right;
    }
    .bot-msg {
        background-color: #2C2C2C;
        color: #e0e0e0;
        margin-right: auto;
        text-align: left;
    }
    .avatar {
        display: inline-block;
        width: 30px;
        height: 30px;
        margin-right: 10px;
        vertical-align: middle;
    }
    .avatar-right {
        margin-left: 10px;
        margin-right: 0;
    }
    .msg-container {
        display: flex;
        align-items: flex-start;
        margin-bottom: 10px;
    }
    .stTextInput>div>div>input {
        border: 1.5px solid #BB86FC;
        border-radius: 8px;
        padding: 10px;
        background-color: #1e1e1e;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# ✅ Chat message display
# st.markdown('<div class="chat-container">', unsafe_allow_html=True)

for role, message in st.session_state.chat_history:
    if role == "user":
        st.markdown(f"""
            <div class="msg-container" style="justify-content: flex-end;">
                <div class="message user-msg">{message}</div>
                <img src="https://img.icons8.com/emoji/48/000000/person.png" class="avatar avatar-right"/>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
            <div class="msg-container">
                <img src="https://img.icons8.com/emoji/48/000000/robot-emoji.png" class="avatar"/>
                <div class="message bot-msg">{message}</div>
            </div>
        """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ✅ Input box
user_input = st.chat_input("How can I help you today?", key="main_input")

# ✅ Handle new input
if user_input:
    st.session_state.chat_history.append(("user", user_input))
    history = [(r, m) for r, m in st.session_state.chat_history if r in ("user", "assistant")]

    with st.spinner("MindMate is thinking..."):
        start_time = time.time()
        response = ask_with_followups(user_input, history)
        end_time = time.time()

    # ✅ Log response time
    elapsed_time = round(end_time - start_time, 2)
    print(f"🕒 Model response time: {elapsed_time} sec")  # Backend log

    answer = response.get("reply", "Sorry, something went wrong.")
    st.session_state.chat_history.append(("assistant", answer))

    st.rerun()
