FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY src/ src/
COPY .env.template .env.template
# Note: We do NOT copy .env for security. It should be mounted or passed as env vars.

# Set python path
ENV PYTHONPATH="${PYTHONPATH}:/app/src"
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0

# Expose Streamlit port
EXPOSE 8501

# Run the application
CMD ["streamlit", "run", "src/client/app.py"]
