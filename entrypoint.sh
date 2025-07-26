#!/bin/bash
set -e

# Step 1: Build vector store
python AI-engine/vectorstore.py

# Step 2: Run RAG pipeline
python AI-engine/ragpipeline.py

# Step 3: Start the Streamlit app
streamlit run AI-engine/llama.py --server.port 7860 --server.address 0.0.0.0
