@mcp.tool()
def get_dataset_structure(dataset_id: str) -> Dict[str, Any]:
    """
    Get the structure (dimensions and codes) of a dataset.
    Call this BEFORE `get_dataset_data` to understand how to filter.

    Args:
        dataset_id: The dataset identifier.

    Returns:
        Dictionary containing dimension names and their allowed values (codes).
    """
    try:
        logger.info(f"Getting structure for dataset: {dataset_id}")
        
        structure = SDMXService.get_structure(dataset_id)
        dimensions = SDMXService.parse_dimensions(structure)
        
        # Format for LLM consumption (simplifying the list of dicts back to simple key-val for display if needed)
        # But keeping it structured is fine too.
        # Let's flatten the values for the output to make it readable
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
    Get data from a specific ABS dataset using its ID. 
    Can be filtered by dimensions.
    
    Args:
        dataset_id: The ABS dataset identifier.
        start_period: Start period (YYYY-MM).
        end_period: End period (YYYY-MM).
        filters: Dictionary of dimension ID (e.g. "REGION") to Value ID (e.g. "AUS"). 
                 Use `get_dataset_structure` to find valid IDs.

    Returns:
        Dataset observations.
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
        
        # Step 2: Fetch data
        data = SDMXService.get_data(dataset_id, path_key, start_period, end_period)
        
        if not data:
             return {"error": f"No data found for dataset {dataset_id} with path {path_key}. Check filters."}
        
        # Re-parse structure from THIS response data in case it changed (it shouldn't for dimensions)
        response_structure = SDMXService._parse_structure(data)
        response_dims = SDMXService.parse_dimensions(response_structure)
        
        observations = SDMXService.parse_observations(data, response_dims)

        MAX_OBS = 20
        truncated = False
        if len(observations) > MAX_OBS:
            observations = observations[:MAX_OBS]
            truncated = True

        result = {
            "dataset_id": dataset_id,
            "title": response_structure.get("name", "Unknown Dataset"),
            "truncated": truncated,
            "total_observations_found": len(observations) + (MAX_OBS if truncated else 0), # approx
            "data_sample": observations,
            "note": "Data contains a subset of observations."
        }
        
        return result

    except Exception as e:
        logger.error(f"Error fetching data: {e}")
        return {"error": str(e)}
