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

# Set environment variables for Hugging Face and transformers cache
ENV HF_HOME=/app/hf_cache
ENV TRANSFORMERS_CACHE=/app/hf_cache
ENV SENTENCE_TRANSFORMERS_HOME=/app/hf_cache

# Copy requirements and install Python packages
COPY AI-engine/requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy your application files
COPY . .

# 👇 Add this after copying files
RUN chmod +x /app/entrypoint.sh

# Ensure cache folder exists and is writable
RUN mkdir -p /app/hf_cache && chmod -R 777 /app/hf_cache

# Expose Streamlit port
EXPOSE 8501

# Entrypoint
ENTRYPOINT ["/app/entrypoint.sh"]
