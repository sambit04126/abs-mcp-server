"""ABS Dataset MCP Server implementation."""

import logging
from typing import List, Dict, Any, Optional
from mcp.server.fastmcp import FastMCP
from .sdmx_service import SDMXService

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastMCP server
mcp = FastMCP("abs-data")

@mcp.tool()
def search_datasets(keyword: str = "", limit: int = 10) -> List[Dict[str, Any]]:
    """
    Step 1: Search for ABS datasets by keyword.
    Use this to find the `dataset_id` (e.g. "CPI").
    """
    return SDMXService.search_datasets(keyword, limit)

@mcp.tool()
def get_dataset_structure(dataset_id: str) -> Dict[str, Any]:
    """
    Step 2: Get the "Grammar" (Dimensions and Codes) for a dataset.
    CRITICAL: You MUST call this before `get_dataset_data`.
    It returns the valid `filters` keys and allowed values (codes).
    
    Example:
    If it returns `{"dimensions": [{"id": "REGION", "values": {"1": "NSW"}}]}`
    Then you know you can filter by `{"REGION": "1"}`.
    """
    try:
        logger.info(f"Getting structure for dataset: {dataset_id}")
        
        structure = SDMXService.get_structure(dataset_id)
        dimensions = SDMXService.parse_dimensions(structure)
        
        # Flatten values for display
        simple_dims = []
        for d in dimensions:
            simple_dims.append({
                "id": d["id"],
                "name": d["name"],
                "values": {v["id"]: v["name"] for v in d["values"]}
            })

        return {
            "dataset_id": dataset_id,
            "dimensions": simple_dims,
            "description": structure.get("description", "No description")
        }

    except Exception as e:
        logger.error(f"Error getting structure: {e}")
        return {"error": str(e)}

@mcp.tool()
def get_dataset_data(
    dataset_id: str,
    start_period: Optional[str] = None,
    end_period: Optional[str] = None,
    filters: Optional[Dict[str, str]] = None
) -> Dict[str, Any]:
    """
    Step 3: Fetch data using the specific codes from `get_dataset_structure`.
    
    CRITICAL Rules:
    1. `filters` keys MUST match dimension IDs (e.g. "MEASURE", "REGION").
    2. `filters` values MUST match the Codes (e.g. "1", "M13"), NOT names.
    3. You usually need to provide a filter for EVERY dimension, or result might be too large.
    4. Time Period (YYYY-MM) is handled by `start_period`/`end_period`, NOT `filters`.
    
    Example:
    `filters={"MEASURE": "3", "REGION": "50", "INDEX": "10001", "FREQ": "M"}`
    """
    try:
        logger.info(f"Getting data for dataset: {dataset_id} with filters: {filters}")

        # Step 1: Get structure
        structure_obj = SDMXService.get_structure(dataset_id)
        dimensions = SDMXService.parse_dimensions(structure_obj)
        
        # Construct SDMX Key
        path_key = "all"
        if filters:
             key_parts = []
             for dim in dimensions:
                 dim_id = dim.get("id")
                 if dim_id in filters:
                     key_parts.append(filters[dim_id])
                 else:
                     key_parts.append("") # Empty means "all"
             
             if any(part for part in key_parts):
                 path_key = ".".join(key_parts)
                 # Strip trailing empty parts (dots) which can cause API errors
                 if path_key.endswith("."):
                     path_key = path_key.rstrip(".")

        # Step 2: Fetch data
        data = SDMXService.get_data(dataset_id, path_key, start_period, end_period)
        
        if not data:
             return {"error": f"No data found for dataset {dataset_id} with path {path_key}. Check filters."}
        
        # Re-parse structure from THIS response data
        response_structure = SDMXService._parse_structure(data)
        response_dims = SDMXService.parse_dimensions(response_structure)
        
        observations = SDMXService.parse_observations(data, response_dims)

        MAX_OBS = 200  # Increased to allow for longer trend analysis (e.g. ~16 years of monthly data)
        total_obs = len(observations)
        truncated = False
        if total_obs > MAX_OBS:
            # Return the LATEST observations (end of list) as they are most relevant
            observations = observations[-MAX_OBS:]
            truncated = True

        result = {
            "dataset_id": dataset_id,
            "title": response_structure.get("name", "Unknown Dataset"),
            "truncated": truncated,
            "total_observations_found": total_obs,
            "data_sample": observations,
            "note": "Data contains a subset of observations (showing latest)." if truncated else ""
        }
        
        return result

    except Exception as e:
        logger.error(f"Error fetching data: {e}")
        return {"error": str(e)}

def main() -> None:
    """Run the MCP server."""
    logger.info("Starting ABS Dataset MCP Server")
    mcp.run(transport="stdio")

if __name__ == "__main__":
    main()
