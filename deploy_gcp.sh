#!/bin/bash

# Cloud Run Deployment Script for ABS MCP Server

# Exit on error
set -e

# Default values
SERVICE_NAME="abs-mcp-chat"
REGION="australia-southeast1" # Default to Sydney for ABS data proximity

# Check for gcloud
if ! command -v gcloud &> /dev/null; then
    echo "❌ Error: 'gcloud' command not found."
    echo "Please install the Google Cloud SDK: https://cloud.google.com/sdk/docs/install"
    exit 1
fi

# Get Project ID
if [ -z "$PROJECT_ID" ]; then
    # Try to get from gcloud config
    PROJECT_ID=$(gcloud config get-value project 2>/dev/null)
fi

if [ -z "$PROJECT_ID" ] || [ "$PROJECT_ID" = "(unset)" ]; then
    echo "⚠️  No default Google Cloud Project found."
    read -p "Please enter your GCP Project ID: " PROJECT_ID
fi

if [ -z "$PROJECT_ID" ]; then
    echo "❌ Error: Project ID is required."
    exit 1
fi

echo "🚀 Deploying to Google Cloud Project: $PROJECT_ID"
echo "📍 Region: $REGION"
echo "📦 Service: $SERVICE_NAME"

# Enable required services
echo "🔌 Enabling required APIs..."
gcloud services enable run.googleapis.com containerregistry.googleapis.com --project "$PROJECT_ID"

# Build and Submit to Cloud Build (easiest way to get image in registry)
# Alternatively, we could build locally and push, but Cloud Build does it all in cloud.
echo "🔨 Building and pushing container image (using Cloud Build)..."
gcloud builds submit --tag "gcr.io/$PROJECT_ID/$SERVICE_NAME" --project "$PROJECT_ID" .

# Deploy to Cloud Run
echo "🚀 Deploying to Cloud Run..."

# Check env file
# Check env file
ENV_FLAGS=""
SECRETS_FILE=".env"

if [ -f "$SECRETS_FILE" ]; then
    echo "📄 Found secrets file: $SECRETS_FILE"
    # Extract API Key robustly (handling potential comments or empty lines)
    API_KEY=$(grep "^GOOGLE_API_KEY=" "$SECRETS_FILE" | cut -d '=' -f2-)
    
    if [ -n "$API_KEY" ]; then
        echo "✅ Loaded GOOGLE_API_KEY from $SECRETS_FILE"
        ENV_FLAGS="--set-env-vars GOOGLE_API_KEY=$API_KEY"
    else
        echo "⚠️  GOOGLE_API_KEY not found in $SECRETS_FILE"
        echo "Please add: GOOGLE_API_KEY=your-actual-key-here"
        exit 1
    fi
else
    echo "❌ Error: $SECRETS_FILE not found."
    echo "Please create a '$SECRETS_FILE' file with your GOOGLE_API_KEY="
    exit 1
fi

gcloud run deploy "$SERVICE_NAME" \
  --image "gcr.io/$PROJECT_ID/$SERVICE_NAME" \
  --platform managed \
  --region "$REGION" \
  --allow-unauthenticated \
  --port 8501 \
  --memory 2Gi \
  --cpu 2 \
  $ENV_FLAGS \
  --project "$PROJECT_ID"

echo "✅ Deployment Complete!"
echo "🌍 Your app should be live at the URL above."
