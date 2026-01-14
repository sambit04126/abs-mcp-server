# Architecture

## Overview

The ABS MCP Server is a three-tier architecture that bridges natural language queries to the ABS SDMX API.

```
┌─────────────┐      ┌──────────────┐      ┌────────────┐
│  Streamlit  │ ←──→ │   AI Agent   │ ←──→ │ MCP Server │ ←──→ ABS API
│     UI      │      │   (Gemini)   │      │  (FastMCP) │
└─────────────┘      └──────────────┘      └────────────┘
```

## Components

###1. **Streamlit UI** (`src/client/app.py`)

**Purpose**: User-facing web interface

**Features**:
- Text input with autocomplete suggestions
- Real-time query logging (tool calls, model thoughts)
- Session state management for conversation history

**Key Functions**:
- `get_suggestions()` - Filters example queries based on user input
- Chat message rendering with status updates

### 2. **AI Agent** (`src/client/mcp_agent.py`)

**Purpose**: Translates natural language to ABS API calls

**Core Logic**:
1. **Topic Matching**: Checks `TOPIC_TO_DATASET` for known topics (inflation, population, etc.)
2. **Smart Search**: If unknown, uses `search_datasets` with ABS technical terms
3. **Structure Discovery**: Calls `get_dataset_structure` to find dimension codes
4. **Data Fetching**: Builds complete filter dict and calls `get_dataset_data`

**System Prompt Strategy**:
- Provides known dataset mappings with dimension defaults
- Enforces SD MX rules (all dimensions required, data key format)
- Includes examples of correct workflows

**Key Methods**:
- `process_query()` - Main async generator yielding events ("log", "thought", "answer")
- `_run_mcp_session()` - Handles MCP client lifecycle

### 3. **MCP Server** (`src/abs_mcp_server/server.py`)

**Purpose**: Exposes ABS data as MCP tools

**Tools**:

| Tool | Input | Output |
|------|-------|--------|
| `search_datasets` | `keyword`, `limit` | List of matching datasets |
| `get_dataset_structure` | `dataset_id` | Dimensions with codes |
| `get_dataset_data` | `dataset_id`, `filters`, `start_period`, `end_period` | Observations |

**Implementation**: Built with FastMCP, delegates to `SDMXService`

### 4. **SDMX Service** (`src/abs_mcp_server/sdmx_service.py`)

**Purpose**: Low-level ABS API client

**Key Methods**:
- `get_structure()` - Fetches metadata from `/data/{dataset}?detail=full`
- `get_data()` - Fetches observations from `/data/{dataset}/{key}`
-` parse_dimensions()` - Normalizes SDMX dimension structure
- `parse_observations()` - Converts SDMX series/observations to flat list

**SDMX Handling**:
- Supports both flat observations and time-series (series) format
- Maps dimension indices to human-readable names

## Data Flow

### Example: "What is the current inflation rate?"

```
1. User types query
   ↓
2. UI sends to Agent
   ↓
3. Agent sees "inflation" → matches TOPIC_TO_DATASET → dataset_id="CPI_M"
   ↓
4. Agent calls get_dataset_structure(CPI_M)
   ↓
5. MCP Server calls SDMXService.get_structure()
   ↓
6. ABS API returns dimensions: [MEASURE, INDEX, FREQ, REGION, TSEST, TIME_PERIOD]
   ↓
7. Agent builds filters using defaults from topic_mapping.py:
   {MEASURE: "3", INDEX: "10001", FREQ: "M", REGION: "50", TSEST: "10"}
   ↓
8. Agent calls get_dataset_data(CPI_M, filters)
   ↓
9. MCP Server builds SDMX key: "3.10001.10.50.M"
   ↓
10. ABS API returns observations
   ↓
11. Server parses to [{value: 3.5, time: "2025-09", ...}]
   ↓
12. Agent formats: "The latest inflation rate is 3.5%"
   ↓
13. UI displays answer
```

## SDMX API Details

### Dataflow Structure

ABS uses **SDMX 2.1** format:

- **Dataflow** = Dataset (e.g., `CPI_M`)
- **Dimensions** = Categories for filtering (e.g., `MEASURE`,  `REGION`)
- **Data Key** = Combination of dimension codes (`3.10001.10.50.M`)
- **Observations** = Actual values with metadata

### Critical Rules

1. **All dimensions must be specified** (except `TIME_PERIOD`)
2. **Data key order matters** - must match dimension order in structure
3. **Missing dimensions cause 422 errors**

### Example API Call

```
GET https://api.data.abs.gov.au/data/CPI_M/3.10001.10.50.M
Accept: application/vnd.sdmx.data+json
```

Returns:
```json
{
  "data": {
    "dataSets": [{
      "series": {
        "0:0:0:0:0": {
          "observations": {
            "0": [3.5],  // Latest value
            "1": [3.2],  // Previous
            ...
          }
        }
      }
    }],
    "structure": {...}
  }
}
```

## Topic Mapping Optimization

**Problem**: Agent was searching 5 times for "population of Perth"

**Solution**: Pre-map common topics to datasets with dimension defaults

**Implementation** (`src/client/topic_mapping.py`):

```python
TOPIC_TO_DATASET = {
    "inflation": {
        "dataset_id": "CPI_M",
        "common_dimensions": {
            "MEASURE": "3",    # % change
            "INDEX": "10001",  # All groups
            ...
        }
    }
}
```

**Impact**: Search calls reduced from 1-5 to 0 for known topics

## Configuration

All config centralized in `.env`:

```env
GOOGLE_API_KEY=...        # Required for agent
ABS_API_BASE=...          # Optional override
LOG_LEVEL=INFO            # DEBUG/INFO/WARNING/ERROR
```

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| 422 Unprocessable Entity | Missing dimension | Add all dimensions from structure |
| 404 Not Found | Invalid dataset/key | Verify dataset exists via search |
| KeyError in observations | Unexpected structure | Check SDMX format version |

## Performance

- **Caching**: Session persists MCP client across queries
- **Lazy Loading**: Dimensions loaded only when needed
- **Streaming**: Agent yields events progressively (logs, thoughts, answer)

## Security

- API keys stored in `.env` (gitignored)
- No authentication required for ABS API (public data)
- HTTPS enforced for all external calls

## Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for:
- Docker containerization
- Cloud Run / Lambda deployment
- Environment configuration
