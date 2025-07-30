# 🧠 MindMate – AI-Powered Mental Health Chatbot

**MindMate** is an AI-driven mental health chatbot built with LangChain, ChromaDB, and a local LLM (via Ollama). It uses Retrieval-Augmented Generation (RAG) to provide context-aware, supportive responses to users dealing with mental health concerns. All responses are powered by a custom-trained mental health dataset, ensuring empathy and relevance in every interaction.

---

## 🌟 Features

- 💬 **Conversational Mental Health Support**
- 🔍 **RAG Pipeline** using LangChain + Chroma for smart context-aware responses
- 🧠 **Local LLM** integration using `phi3:3.8b` via Ollama
- 🧾 **Custom Dataset**: Based on `ShenLab/MentalChat16K` for high-quality Q&A
- 📦 **Modular Codebase**: Organized structure for easy updates and scaling
- 🐳 **Docker-ready** for local development and deployment
- 🧪 **Streamlit Interface** for user-friendly interaction

---

## 🛠️ Tech Stack

| Layer      | Tools Used                                |
|------------|--------------------------------------------|
| Backend    | Python, LangChain, Ollama (phi3)           |
| Embeddings | HuggingFace Sentence Transformers          |
| Vector DB  | Chroma                                     |
| UI         | Streamlit                                  |
| Deployment | Docker                                     |
| Dataset    | ShenLab/MentalChat16K                      |

---

## 📁 Project Structure

```bash
mindmate/
├── llama.py             # Connects to local LLM using Ollama
├── vectorstore.py       # Loads, chunks & vectorizes documents
├── ragpipeline.py       # Combines retriever with LLM using LangChain
├── data.ipynb           # Dataset inspection and experimentation
├── requirements.txt     # Python dependencies
├── .venv/               # Virtual environment
└── README.md            # Project overview
```

---

## ⚙️ How It Works

1. **Load Dataset**
   - Imports Q&A pairs from `ShenLab/MentalChat16K`
   - Preprocesses and chunks text into ~500-character sections

2. **Embed & Store**
   - Uses HuggingFace Transformers to embed text chunks
   - Stores vectors in ChromaDB for efficient similarity-based retrieval

3. **Retrieve + Generate**
   - Accepts user questions via the Streamlit UI
   - Retrieves top relevant chunks from ChromaDB
   - Combines context with the user's query and sends it to the local `phi3` LLM (via Ollama) using LangChain

---

## 🚀 Getting Started

### 🧱 Prerequisites

- Python 3.9+
- [Ollama](https://ollama.com/) installed and running with `phi3:3.8b` model
- Docker (optional, for containerized deployment)

---

### 🔧 Installation & Running the Project

#### ✅ Step 1: Clone the Repository

```bash
git clone https://github.com/krish-kavya-02/mental-health-chatbot.git
cd mental-health-chatbot
```

#### ✅ Step 2: Set Up Python Virtual Environment

```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On Windows
.venv\Scripts\activate

# On macOS/Linux
source .venv/bin/activate
```

#### ✅ Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### 🧪 Run the Chatbot Locally

Make sure the phi3:3.8b model is downloaded and running using Ollama:

```bash
ollama run phi3:3.8b
```

Then in another terminal, run:

```bash
python vectorstore.py
```

```bash
python ragpipeline.py
```

```bash
streamlit run llama.py
```

Visit http://localhost:8501 in your browser to start chatting with MindMate 🧠.

---


## 👨‍💻 Author

**Krish Kavya Upadhyay**

- 🌐 [GitHub](https://github.com/krish-kavya-02)
- 💼 [LinkedIn](https://www.linkedin.com/in/krish-kavya-upadhyay-8b3322355/)
