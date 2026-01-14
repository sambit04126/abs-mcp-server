# Deployment Guide

## Local Development

```bash
# Clone and install
git clone https://github.com/yourusername/abs-mcp-server
cd abs-mcp-server
pip install -e .

# Configure
cp .env.template .env
# Edit .env and add GOOGLE_API_KEY

# Run Streamlit UI
streamlit run src/client/app.py
```

App available at: http://localhost:8501

---

## Docker Deployment

### Build Image

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml .
RUN pip install --no-cache-dir .

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "src/client/app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### Build and Run

```bash
# Build
docker build -t abs-mcp-server .

# Run
docker run -p 8501:8501 \
  -e GOOGLE_API_KEY="your_key" \
  abs-mcp-server
```

---

## Google Cloud Run

### Prerequisites

- Google Cloud account
- `gcloud` CLI installed
- Billing enabled

### Deploy

```bash
# Authenticate
gcloud auth login
gcloud config set project YOUR_PROJECT_ID

# Build and push to Artifact Registry
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/abs-mcp-server

# Deploy to Cloud Run
gcloud run deploy abs-mcp-server \
  --image gcr.io/YOUR_PROJECT_ID/abs-mcp-server \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars GOOGLE_API_KEY="your_key"
```

### Custom Domain

```bash
gcloud run domain-mappings create \
  --service abs-mcp-server \
  --domain abs.yourdomain.com
```

---

## AWS Lambda (Serverless)

**Note**: Streamlit requires persistent connection, so Lambda isn't ideal. Consider AWS App Runner instead.

### AWS App Runner

```bash
# Create apprunner.yaml
version: 1.0
runtime: python311
build:
  commands:
    build:
      - pip install .
run:
  command: streamlit run src/client/app.py --server.port=8080
  network:
    port: 8080
    env: APP_PORT
  env:
    - name: GOOGLE_API_KEY
      value: "your_key"
```

Deploy via AWS Console or CLI.

---

## Azure Container Instances

```bash
# Create resource group
az group create --name abs-mcp-rg --location eastus

# Build and push image
az acr create --resource-group abs-mcp-rg --name absmcpregistry --sku Basic
az acr build --registry absmcpregistry --image abs-mcp-server .

# Deploy container
az container create \
  --resource-group abs-mcp-rg \
  --name abs-mcp-server \
  --image absmcpregistry.azurecr.io/abs-mcp-server \
  --dns-name-label abs-mcp \
  --ports 8501 \
  --environment-variables GOOGLE_API_KEY="your_key"
```

Access: http://abs-mcp.eastus.azurecontainer.io:8501

---

## Configuration

### Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `GOOGLE_API_KEY` | Yes | - | Gemini API key |
| `ABS_API_BASE` | No | `https://api.data.abs.gov.au` | ABS API URL |
| `LOG_LEVEL` | No | `INFO` | Logging level |
| `LLM_MODEL` | No | `gemini-2.0-flash-exp` | Gemini model |

### Streamlit Config

Create `.streamlit/config.toml`:

```toml
[server]
port = 8501
headless = true
enableCORS = false

[browser]
gatherUsageStats = false
```

---

## Monitoring

### Logging

Logs written to:
- Console (stdout/stderr)
- `query_trace.jsonl` (query traces)

### Metrics

Monitor:
- Request latency
- Error rates
- API call counts

Use platform-specific tools:
- Cloud Run: Stackdriver
- AWS: CloudWatch
- Azure: Application Insights

---

## Security

### API Keys

- **Never commit** `.env` to version control
- Use **secrets management**:
  - Cloud Run: Secret Manager
  - AWS: Secrets Manager
  - Azure: Key Vault

### Network

- Enable HTTPS (automatic on Cloud Run)
- Restrict access with IAM/firewall rules
- Use VPC if accessing private data

---

## Scaling

### Streamlit Limitations

- Not designed for high concurrency
- Consider these alternatives for scale:
  - **FastAPI** + background workers
  - **Load balancer** with multiple instances
  - **Queueing** (Redis/RabbitMQ)

### Cost Optimization

**Cloud Run**:
- **Min instances**: 0 (scale to zero)
- **Max instances**: 10
- **CPU**: 1
- **Memory**: 512MB

Estimated cost: $5-10/month for low traffic

---

## Troubleshooting

### Common Issues

**1. `ModuleNotFoundError`**
```bash
# Ensure installed in editable mode
pip install -e .
```

**2**. **Port already in use**
```bash
# Kill existing process
lsof -ti:8501 | xargs kill
# Or use different port
streamlit run src/client/app.py --server.port=8502
```

**3. API key not loading**
```bash
# Verify .env is in root directory
cat .env | grep GOOGLE_API_KEY

# Check it's loaded
python -c "import os; print(os.getenv('GOOGLE_API_KEY'))"
```

---

## Backup & Recovery

### Data

- **No persistent data** stored by default
- `query_trace.jsonl` logs can be backed up

### Disaster Recovery

- Keep `.env.template` updated
- Document any custom configurations
- Use IaC (Terraform/Pulumi) for reproducible deployments

---

## Performance Tuning

### Cache MCP Client

Current: Client persists across queries in session

Improvement: Add Redis cache for dataset structures

### Batch Requests

For multiple queries, batch API calls:

```python
async def batch_queries(queries):
    async with MCPClient() as client:
        results = await asyncio.gather(*[
            process_query(q, client) for q in queries
        ])
    return results
```

---

## Next Steps

- Set up CI/CD pipeline
- Add health check endpoint
- Implement rate limiting
- Enable CORS for API access
