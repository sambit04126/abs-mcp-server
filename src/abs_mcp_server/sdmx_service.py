import requests
import logging
from typing import Dict, Any, List, Optional
from functools import lru_cache
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

try:
    from .config import Config
except ImportError:
    # Fallback if config not available
    class Config:
        ABS_API_BASE = "https://api.data.abs.gov.au"
        API_TIMEOUT = 30
        ENABLE_CACHING = True
        CACHE_SIZE = 100

logger = logging.getLogger(__name__)

ABS_API_BASE = Config.ABS_API_BASE
API_TIMEOUT = Config.API_TIMEOUT

def _get_session() -> requests.Session:
    """Create a requests session with retry logic."""
    session = requests.Session()
    retry_strategy = Retry(
        total=3,
        backoff_factor=0.5,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["HEAD", "GET", "OPTIONS"]
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    return session

class SDMXService:
    @staticmethod
    @lru_cache(maxsize=Config.CACHE_SIZE if Config.ENABLE_CACHING else 0)
    def get_structure(dataset_id: str) -> Dict[str, Any]:
        """Fetch and parse structure for a dataset.
        
        Args:
            dataset_id: The ABS dataset identifier
            
        Returns:
            dict: Parsed structure with dimensions and metadata
            
        Raises:
            requests.exceptions.RequestException: If API request fails
        """
        url = f"{ABS_API_BASE}/data/{dataset_id}?detail=full&dimensionAtObservation=AllDimensions"
        headers = {"Accept": "application/vnd.sdmx.data+json"}
        logger.info(f"Fetching structure from: {url}")
        
        try:
            session = _get_session()
            response = session.get(url, headers=headers, timeout=API_TIMEOUT)
            response.raise_for_status()
            data = response.json()
            return SDMXService._parse_structure(data)
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to get structure for {dataset_id}: {e}")
            raise e

    @staticmethod
    def get_data(dataset_id: str, key: str = "all", start_period: Optional[str] = None, end_period: Optional[str] = None) -> Dict[str, Any]:
        """Fetch data with specific key and time params."""
        url = f"{ABS_API_BASE}/data/{dataset_id}"
        if key != "all":
            url = f"{url}/{key}"
            
        params = {"detail": "full"}
        if start_period:
            params["startPeriod"] = start_period
        if end_period:
            params["endPeriod"] = end_period
            
        try:
            response = requests.get(
                url,
                params=params, 
                headers={"Accept": "application/vnd.sdmx.data+json"},
                timeout=30
            )
            
            if response.status_code == 404:
                logger.warning(f"ABS API 404 for {url}")
                return {} # Return empty dict for no data
                
            response.raise_for_status()
            data = response.json()
            # Debug: Check if dataSets is empty
            ds = data.get("data", {}).get("dataSets", [])
            # Note: structure of response is root -> data -> dataSets (sometimes) or root -> dataSets
            # Standard SDMX-JSON 2.0: root -> data -> dataSets
            # But earlier we saw root -> dataSets ? verifying..
            if "data" in data and "dataSets" in data["data"]:
                 ds = data["data"]["dataSets"]
                 logger.info(f"DataSets found in data.dataSets: {len(ds)}")
            elif "dataSets" in data:
                 ds = data["dataSets"]
                 logger.info(f"DataSets found in root.dataSets: {len(ds)}")
            else:
                 logger.warning("No dataSets found in response keys: " + str(data.keys()))
                 
            return data
        except requests.RequestException as e:
            logger.error(f"ABS API Request failed: {e}")
            raise e

    @staticmethod
    def _parse_structure(data: Dict[str, Any]) -> Dict[str, Any]:
        """Normalize extracting structure from SDMX-JSON response."""
        # 1. Try root `structure`
        structure = data.get("structure", {})
        
        # 2. Try `data.structures` (list or dict)
        if not structure and "data" in data and "structures" in data["data"]:
            structures = data["data"]["structures"]
            if isinstance(structures, list) and len(structures) > 0:
                structure = structures[0]
            elif isinstance(structures, dict):
                structure = structures
        
        # 3. Fallback or specific paths for older/newer SDMX versions
        return structure

    @staticmethod
    def search_datasets(keyword: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Search available ABS datasets."""
        try:
             # We need to implement search here. Reusing logic from old server.py
             ABS_DATAFLOWS_URL = f"{ABS_API_BASE}/dataflow"
             response = requests.get(
                ABS_DATAFLOWS_URL, 
                headers={"Accept": "application/vnd.sdmx.structure+json"},
                timeout=30
            )
             response.raise_for_status()
             
             data = response.json()
             dataflows_container = data.get("data", {})
             if isinstance(dataflows_container, dict):
                 datasets = dataflows_container.get("dataflows", [])
             else:
                 datasets = []

             if keyword:
                keyword_lower = keyword.lower()
                datasets = [
                    ds for ds in datasets
                    if keyword_lower in ds.get("name", "").lower()
                    or keyword_lower in ds.get("description", "").lower()
                ]
            
             datasets = datasets[:limit]
             
             result = []
             for ds in datasets:
                result.append({
                    "id": ds.get("id"),
                    "name": ds.get("name"),
                    "description": ds.get("description"),
                    "version": ds.get("version"),
                    "agency_id": ds.get("agencyID"),
                })
             return result

        except Exception as e:
            logger.error(f"Search failed: {e}")
            return []

    @staticmethod
    def parse_dimensions(structure: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract user-friendly dimension list from structure object."""
        # Dimensions can be at series or observation level
        dimensions_container = structure.get("dimensions", {})
        series_dims = dimensions_container.get("series", [])
        obs_dims = dimensions_container.get("observation", [])
        
        # Combine (usually Series dims come first, then Obs dims in the key)
        # But order matters for the key construction!
        # SDMX-JSON usually orders them safely if we just concat? 
        # Actually we should trust the order in the key.
        # But for now, let's just get them all.
        
        all_dims = series_dims + obs_dims
        
        formatted_dims = []
        for dim in all_dims:
            # We keep values as a list for index mapping, but also want ID lookup?
            # For parsing observations we need index -> value.
            # For filtering we need ID -> value.
            values_list = dim.get("values", [])
            formatted_dims.append({
                "id": dim.get("id"),
                "name": dim.get("name"),
                "values": values_list # Keep raw list of {id:..., name:...}
            })
        return formatted_dims

    @staticmethod
    def parse_observations(data: Dict[str, Any], dimensions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Parse observations into a flat list of dicts with dimension names."""
        # Handle standard SDMX-JSON 2.0 (root -> data -> dataSets)
        # and other variants (root -> dataSets)
        data_sets = []
        if "data" in data and isinstance(data["data"], dict) and "dataSets" in data["data"]:
            data_sets = data["data"]["dataSets"]
        else:
            data_sets = data.get("dataSets", [])
            
        observations = []
        
        if not data_sets:
            return observations

        ds = data_sets[0]
        
        # Case 1: Series (Time Series usually)
        if "series" in ds:
            series = ds["series"]
            for series_key, series_data in series.items():
                series_indices = [int(i) for i in series_key.split(":")]
                
                obs_map = series_data.get("observations", {})
                for obs_key, obs_val in obs_map.items():
                    # obs_key usually matches the Observation Dimension
                    obs_dict = {"value": obs_val[0]}
                    
                    # Iterate dimensions to map series indices and obs indices
                    current_dim_idx = 0
                    
                    # Map Series Dimensions
                    for s_idx in series_indices:
                        if current_dim_idx < len(dimensions):
                            dim = dimensions[current_dim_idx]
                            if s_idx < len(dim["values"]):
                                obs_dict[dim["name"]] = dim["values"][s_idx]["name"]
                            current_dim_idx += 1
                            
                    # Map Observation Dimensions (usually just Time)
                    obs_indices = [int(i) for i in obs_key.split(":")]
                    for o_idx in obs_indices:
                         if current_dim_idx < len(dimensions):
                            dim = dimensions[current_dim_idx]
                            if o_idx < len(dim["values"]):
                                obs_dict[dim["name"]] = dim["values"][o_idx]["name"]
                            current_dim_idx += 1
                            
                    observations.append(obs_dict)
                    
        # Case 2: Flat Observations
        elif "observations" in ds:
            raw_obs = ds["observations"]
            for key, value in raw_obs.items():
                indices = [int(i) for i in key.split(":")]
                obs_dict = {"value": value[0]} 
                
                for i, idx in enumerate(indices):
                    if i < len(dimensions):
                         dim = dimensions[i]
                         if idx < len(dim["values"]):
                             val_obj = dim["values"][idx]
                             obs_dict[dim["name"]] = val_obj["name"]
                         else:
                             obs_dict[dim["name"]] = "Unknown"
                
                observations.append(obs_dict)

        return observations
