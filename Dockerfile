FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python packages
COPY AI-engine/requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy your application files
COPY . .

# Expose a port (change if you're using FastAPI, Streamlit, etc.)
EXPOSE 8501

# Default command — update based on your entrypoint
CMD ["streamlit", "run", "AI-engine/llama.py"]