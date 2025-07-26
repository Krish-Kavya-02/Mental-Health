from datasets import load_dataset
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import CharacterTextSplitter
from langchain.schema import Document
from chromadb.config import Settings  # ✅ For local embedded mode
from dotenv import load_dotenv
import os

# Load environment variables from .env if any
load_dotenv()

def create_vector_store():
    # Load the MentalChat16K dataset
    ds = load_dataset("ShenLab/MentalChat16K")
    print("Dataset loaded.")

    print("Converting to LangChain documents...")
    docs = []

    for row in ds["train"]:
        user_input = row['input']
        bot_reply = row['output']
        docs.append(Document(
            page_content=f"Q: {user_input}\nA: {bot_reply}",
            metadata={"source": "MentalChat16K"}
        ))

    print(f"Loaded {len(docs)} documents.")

    # Split documents into chunks
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=300,
        chunk_overlap=50,
        length_function=len,
    )
    chunked_docs = text_splitter.split_documents(docs)
    print(f"Split into {len(chunked_docs)} chunks.")

    # Initialize HuggingFace embeddings
    huggingface_embeddings = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2",
        model_kwargs={'device': 'cpu'},
        encode_kwargs={'normalize_embeddings': True}
    )

    # Create and persist Chroma vector store (in local/embedded mode)
    db = Chroma(
        collection_name="example_collection",
        embedding_function=huggingface_embeddings,
        persist_directory="./chroma_db",  # Ensure this exists or will be created
        client_settings=Settings(
            chroma_db_impl="duckdb+parquet",
            persist_directory="./chroma_db",
            anonymized_telemetry=False,
        )
    )

    db.add_documents(chunked_docs)
    db.persist()
    print("✅ Vector store created and persisted successfully.")

    return db
