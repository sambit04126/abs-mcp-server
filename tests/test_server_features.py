import sys
import os
import json

# Add src to path
sys.path.append(os.path.abspath("src"))

from abs_mcp_server.server import get_dataset_structure, get_dataset_data, search_datasets

def test_server_logic():
    print("1. Searching for datasets...")
    results = search_datasets(keyword="CPI", limit=1)
    if not results:
        print("No datasets found.")
        return
    
    dataset_id = results[0]["id"]
    print(f"Targeting: {dataset_id}")
    
    print("\n2. Getting Structure...")
    struct = get_dataset_structure(dataset_id)
    if "error" in struct:
        print("Error getting structure:", struct["error"])
        return
        
    dims = struct.get("dimensions", [])
    print(f"Dimensions found: {len(struct['dimensions'])}")
    
    # 3. Getting Data with strict filters (Grammar-based)
    # The grammar tells us we need: MEASURE, INDEX, TSEST, REGION, FREQ (from previous findings)
    # Let's verify we can construct a valid query using the structure we just got?
    # For this test, we'll hardcode the known valid semantic filters to prove the loop works.
    
    filters = {
        "MEASURE": "3",      # Inflation
        "INDEX": "10001",    # All groups
        "REGION": "50",      # weighted avg
        "TSEST": "10",       # Original
        "FREQ": "M"          # Monthly
    }
    print(f"Filtering by {filters}...")
    
    # 4. Fetch Data
    # Note: The tool expects 'dataset_id' and 'filters'
    data = get_dataset_data(dataset_id=dataset_id, filters=filters)
    
    if "error" in data:
        print("Error getting data:", data["error"])
    else:
        print(f"Data Retrieved! Total observations: {data.get('total_observations_found')}")
        sample = data.get("data_sample", [])
        if sample:
            print("First observation:", sample[0])
            # Verify filter worked?
            # The key should verify it match, but simpler to just see if we got data.
        else:
            print("No observations returned (might be valid sparse data).")

if __name__ == "__main__":
    test_server_logic()
