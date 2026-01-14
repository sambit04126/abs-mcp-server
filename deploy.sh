#!/bin/bash

# Build the image
echo "🔨 Building Docker image..."
docker build -t abs-mcp-chat .

# Check if .env exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found!"
    echo "Please create a .env file with your GOOGLE_API_KEY before running."
    exit 1
fi

# Run the container
echo "🚀 Running container on port 8501..."
docker run -p 8501:8501 --env-file .env abs-mcp-chat
