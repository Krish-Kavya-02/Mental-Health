FROM python:3.9-slim
# Set the working directory
WORKDIR /app
# Copy the requirements file into the container
COPY . /app/
# Change the working directory to the AI-engine folder
WORKDIR /app/AI-engine
# Create a virtual environment
RUN python -m venv .venv
# Activate the virtual environment and install dependencies
RUN .venv/bin/pip install --upgrade pip && \
    .venv/bin/pip install -r requirements.txt
# Expose the port for Streamlit
EXPOSE 8501
# Activate the virtual environment
# Run the application
CMD [".venv/bin/python", "-m", "streamlit", "run", "llama.py"]