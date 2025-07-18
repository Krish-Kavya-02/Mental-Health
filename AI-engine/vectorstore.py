from datasets import load_dataset
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import CharacterTextSplitter
from langchain.schema import Document

def create_vector_store():
    # Load the dataset
    ds = load_dataset("ShenLab/MentalChat16K")
    print(ds)
    
    print("Converting to LangChain documents...")
    docs = []

    if 'ds' in globals():
        for row in ds["train"]:
            user_input = row['input']
            bot_reply = row['output']
        
            docs.append(Document(
                page_content=f"Q: {user_input}\nA: {bot_reply}",
                metadata={"source": "MentalChat16K"}
        ))
    else:
        print("Please run the cell that loads the dataset into 'ds' first.")
    
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=300,       
        chunk_overlap=50,     
       length_function=len,
    )

    chunked_docs = text_splitter.split_documents(docs)
    
    # Create embeddings using HuggingFaceBgeEmbeddings
    huggingface_embeddings = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2",      
        model_kwargs={'device': 'cpu'},
        encode_kwargs={'normalize_embeddings': True}
    )

    # Create a Chroma vector store

    db = Chroma(
        collection_name="example_collection",
        embedding_function=huggingface_embeddings,
        collection_metadata={"in_memory": True},
        persist_directory="./chroma_db",  # Where to save data locally, remove if not necessary
    )
    db.persist()

    print("Vector store created and persisted successfully.")
    
    return db