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
# Check env for API Key (Order: Shell Env -> .env file)
API_KEY="$GOOGLE_API_KEY"
ENV_FLAGS=""

if [ -n "$API_KEY" ]; then
    echo "✅ Found GOOGLE_API_KEY in current shell environment."
elif [ -f ".env" ]; then
    echo "📄 Found .env file, reading key..."
    API_KEY=$(grep "^GOOGLE_API_KEY=" .env | cut -d '=' -f2-)
fi

# Validation
if [ -n "$API_KEY" ]; then
    ENV_FLAGS="--set-env-vars GOOGLE_API_KEY=$API_KEY"
else
    echo "❌ Error: GOOGLE_API_KEY is missing."
    echo "You must either:"
    echo "  1. Export it in your shell: export GOOGLE_API_KEY=..."
    echo "  2. Or add it to a '.env' file: GOOGLE_API_KEY=..."
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
