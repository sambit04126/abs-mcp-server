# API Reference

## MCP Tools

The ABS MCP Server exposes 3 tools via the Model Context Protocol.

### 1. `search_datasets`

Search for ABS datasets by keyword.

**Parameters**:
- `keyword` (string, optional): Search term (matches name/description)
- `limit` (integer, default=10): Max results to return

**Returns**:
```python
[
    {
        "id": "CPI_M",
        "name": "Consumer Price Index - Monthly",
        "description": "CPI measures quarterly...",
        "version": "1.0.0",
        "agency_id": "ABS"
    },
    ...
]
```

**Example**:
```python
results = search_datasets(keyword="CPI", limit=5)
```

---

### 2. `get_dataset_structure`

Get dimensions and valid codes for a dataset.

**Parameters**:
- `dataset_id` (string, required): Dataset identifier (e.g., "CPI_M")

**Returns**:
```python
{
    "dataset_id": "CPI_M",
    "dimensions": [
        {
            "id": "MEASURE",
            "name": "Measure",
            "values": {
                "3": "Percentage Change from Previous Year",
                "10": "Index Numbers"
            }
        },
        {
            "id": "REGION",
            "name": "Region",
            "values": {
                "50": "Weighted average of eight capital cities",
                "1": "Sydney",
                ...
            }
        },
        ...
    ]
}
```

**Example**:
```python
structure = get_dataset_structure(dataset_id="CPI_M")
# Use structure["dimensions"] to build filters
```

---

### 3. `get_dataset_data`

Fetch observations from a dataset with filters.

**Parameters**:
- `dataset_id` (string, required): Dataset identifier
- `filters` (dict, required): Dimension code filters (e.g., `{"MEASURE": "3", "REGION": "50"}`)
- `start_period` (string, optional): Start date (format: "YYYY-MM" or "YYYY-QX")
- `end_period` (string, optional): End date

**Returns**:
```python
{
    "dataset_id": "CPI_M",
    "title": "Consumer Price Index",
    "total_observations_found": 50,
    "truncated": false,
    "data_sample": [
        {
            "value": 3.5,
            "Measure": "Percentage Change",
            "Region": "Weighted average",
            "Time Period": "2025-09"
        },
        ...
    ]
}
```

**Example**:
```python
data = get_dataset_data(
    dataset_id="CPI_M",
    filters={
        "MEASURE": "3",
        "INDEX": "10001",
        "FREQ": "M",
        "REGION": "50",
        "TSEST": "10"
    }
)
```

---

## Python SDK (Agent)

### MCPAgent

**Constructor**:
```python
from mcp_agent import MCPAgent

agent = MCPAgent(api_key="your_google_api_key")
```

**Method**: `process_query(query: str)`

Async generator yielding events:

```python
async for event_type, content in agent.process_query("What is the inflation rate?"):
    if event_type == "log":
        print(f"LOG: {content}")
    elif event_type == "thought":
        print(f"THOUGHT: {content}")
    elif event_type == "answer":
        print(f"ANSWER: {content}")
```

**Event Types**:
- `"log"`: Tool invocations, arguments, outputs
- `"thought"`: Model's reasoning (extracted from responses)
- `"answer"`: Final formatted answer

---

## SDMX Data Key Format

ABS API uses SDMX keys to filter data:

### Format

```
/data/{DATASET}/{DIM1}.{DIM2}.{DIM3}...
```

### Example

```
/data/CPI_M/3.10001.10.50.M
            │ │     │  │  └─ FREQ=M (Monthly)
            │ │     │  └──── REGION=50 (Weighted avg)
            │ │     └─────── TSEST=10 (Original)
            │ └───────────── INDEX=10001 (All groups CPI)
            └─────────────── MEASURE=3 (% change)
```

### Important Notes

1. **Order matters**: Dimension order must match dataset structure
2. **All dimensions required**: Except `TIME_PERIOD`
3. **Wildcards not supported**: Must specify exact codes

---

## Dataset IDs (Common)

| Topic | Dataset ID | Description |
|-------|-----------|---|
| Inflation (Monthly) | `CPI_M` | Consumer Price Index - Monthly |
| Employment | `LF` | Labour Force Survey |
| Population (Regional) | `ABS_ANNUAL_ERP_ASGS2021` | Estimated Resident Population |
| GDP | `5206` | National Accounts |
| Wages | `AWE` | Average Weekly Earnings |

Full list: https://api.data.abs.gov.au/dataflow

### Refreshing Dataset Catalog

The complete catalog of all ABS datasets can be fetched from:

```
GET https://data.api.abs.gov.au/rest/dataflow/all?detail=allstubs
```

This endpoint returns SDMX XML with all available dataflows (datasets), their IDs, versions, and names. Use this to:
- Discover new datasets
- Update `topic_mapping.py` with new dataset IDs
- Verify dataset availability

**Example**: Parse the catalog with `examples/parse_abs_catalog.py`

---

## Error Codes

| Code | Meaning | Solution |
|------|---------|----------|
| 200 | Success | - |
| 404 | Dataset/key not found | Verify dataset ID via `search_datasets` |
| 422 | Invalid filter | Ensure all dimensions included |
| 500 | Server error | Retry with exponential backoff |

---

## Rate Limits

- **ABS API**: No explicit rate limit (public data)
- **Best Practice**: Add 100ms delay between requests

---

## Code Examples

### Example 1: Search and Explore

```python
# Search for inflation datasets
results = search_datasets(keyword="CPI", limit=3)
dataset_id = results[0]["id"]

# Get structure
structure = get_dataset_structure(dataset_id)

# Extract dimension codes
measure_codes = structure["dimensions"][0]["values"]
print(measure_codes)  # {"3": "% change", ...}
```

### Example 2: Fetch Latest Data

```python
# Get latest CPI (no time filter)
data = get_dataset_data(
    dataset_id="CPI_M",
    filters={
        "MEASURE": "3",
        "INDEX": "10001",
        "FREQ": "M",
        "REGION": "50",
        "TSEST": "10"
    }
)

latest = data["data_sample"][0]
print(f"Latest inflation: {latest['value']}%")
```

### Example 3: Historical Data

```python
# Get 2024 monthly CPI
data = get_dataset_data(
    dataset_id="CPI_M",
    filters={"MEASURE": "3", ...},
    start_period="2024-01",
    end_period="2024-12"
)
```

---

## Topic Mapping

Pre-defined mappings in `src/client/topic_mapping.py`:

```python
TOPIC_TO_DATASET = {
    "inflation": {
        "dataset_id": "CPI_M",
        "common_dimensions": {"MEASURE": "3", ...}
    },
    ...
}
```

Use `get_dataset_for_topic(query)` to get mapping for a query string.
