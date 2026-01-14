# ABS MCP Server

> Production-ready MCP server for Australian Bureau of Statistics data access with AI-powered natural language queries.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 🚀 Quick Start (< 5 minutes)

```bash
# Clone and install
git clone https://github.com/sambit04126/abs-mcp-server.git
cd abs-mcp-server
pip install -e .

# Configure API key
cp .env.template .env
# Edit .env and add your GOOGLE_API_KEY
# (Note: For Claude Desktop, API keys are handled differently, see below)

# Run Streamlit UI
streamlit run src/client/app.py
```

## 🔌 Connecting to Claude Desktop (Standard MCP)

This server adheres to the Model Context Protocol (MCP) and can be used directly with Claude Desktop.

1.  **Install the package** (as above).
2.  **Edit your config**: `~/Library/Application Support/Claude/claude_desktop_config.json`
3.  **Add the server**:

```json
{
  "mcpServers": {
    "abs-data": {
      "command": "uv",
      "args": [
        "--directory",
        "/ABSOLUTE/PATH/TO/abs-mcp-server",
        "run",
        "abs-mcp-server"
      ],
      "env": {
        "GOOGLE_API_KEY": "your-key-here"
      }
    }
  }
}
```

## ✨ Features

- 🤖 **AI-Powered Queries**: Natural language interface via Gemini AI
- 📊 **Complete ABS Access**: All SDMX-compliant ABS datasets
- 🔍 **Optimized Performance**: Minimal API calls with intelligent caching
- 📝 **Full Query Logging**: Trace all requests for debugging
- 🎯 **Zero-Search Topics**: Pre-mapped common queries (inflation, employment, population)

## 💬 Example Queries

Try these in the UI:

- "What is the current inflation rate?"
- "What is the population of Perth?"
- "What is the unemployment rate?"
- "What was the inflation rate last year?"
- "What is the population of Sydney?"

## 🏗️ Architecture

This project consists of:

1. **MCP Server** (`src/abs_mcp_server/`) - FastMCP server providing 3 tools:
   - `search_datasets` - Search ABS datasets by keyword
   - `get_dataset_structure` - Get dimensions and codes
   - `get_dataset_data` - Fetch observations with filters

2. **AI Agent** (`src/client/mcp_agent.py`) - Gemini-powered agent that:
   - Translates natural language to dataset queries
   - Uses topic mappings to skip search for known topics
   - Handles SDMX complexity automatically

3. **Streamlit UI** (`src/client/app.py`) - User-friendly web interface with:
   - Autocomplete suggestions
   - Real-time query logs
   - Chat-style interaction

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for detailed architecture.

## 📖 Documentation

- [Architecture Overview](docs/ARCHITECTURE.md)
- [API Reference](docs/API_REFERENCE.md)
- [Deployment Guide](docs/DEPLOYMENT.md)
- [Contributing Guidelines](docs/CONTRIBUTING.md)

## 🐳 Docker Deployment

You can deploy using the provided script:

```bash
# 1. Create .env file
cp .env.template .env
# Edit .env with your key

# 2. Run deploy script
./deploy.sh
```

Or manually:

```bash
```bash
docker build -t abs-mcp-chat .
docker run -p 8501:8501 --env-file .env abs-mcp-chat
```

## ☁️ Cloud Deployment (Google Cloud Run)

Deploying to production is automated with the included script.

### Prerequisites
1. [Google Cloud SDK](https://cloud.google.com/sdk/docs/install) installed (`gcloud` command).
2. A Google Cloud Project with billing enabled.

### Deploy
Run the automated deployment script:

```bash
# Make executable (first time only)
chmod +x deploy_gcp.sh

# Deploy
./deploy_gcp.sh
```

The script will:
1. Ask for your GCP Project ID (if not set).
2. Build the Docker image using Cloud Build.
3. Deploy the service to Cloud Run (Region: `australia-southeast1`).
4. Output your live public URL.

## 🧪 Examples

Check out the `examples/` directory:

- `search_datasets.py` - Basic dataset search
- `explore_dataset.py` - Inspect dataset structure
- `explore_perth_data.py` - Population data example

## 🤝 Contributing

Contributions welcome! Please see [CONTRIBUTING.md](docs/CONTRIBUTING.md).

## 📝 License

MIT License - see [LICENSE](LICENSE) file.

## 🙏 Acknowledgments

- Built on the [Model Context Protocol](https://modelcontextprotocol.io)
- Data from [Australian Bureau of Statistics](https://www.abs.gov.au)
- Powered by [Google Gemini AI](https://ai.google.dev)
