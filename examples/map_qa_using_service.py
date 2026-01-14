import sys
import os
import json

# Add src to path
sys.path.append(os.path.abspath("src"))

from abs_mcp_server.sdmx_service import SDMXService

def map_datasets():
    # QA Level 2 & 3 targets
    targets = [
        # Level 2
        {"name": "CPI", "id": "CPI"}, # For commodities / cities
        {"name": "Labour Force", "id": "LF"}, # For State/Industry
        
        # Level 3
        # Building Approvals
        {"name": "Building Approvals", "id": "ABS_BA_SA2_ASGS2016"}, # Guessing, will search
        # Retail Trade
        {"name": "Retail Trade", "id": "RT"}, # Guessing
    ]
    
    mapping = {}
    
    for t in targets:
        print(f"\n--- Mapping {t['name']} ---")
        dataset_id = t["id"]
        
        # 1. Validate ID or Search
        try:
            struct = SDMXService.get_structure(dataset_id)
        except:
            print(f"Direct fetch for {dataset_id} failed. Searching...")
            search_res = SDMXService.search_datasets(t["name"], limit=5)
            if search_res:
                # Pick best match?
                # For Retail Trade, look for RT
                dataset_id = search_res[0]["id"]
                print(f"Found alternative ID: {dataset_id}")
                struct = SDMXService.get_structure(dataset_id)
            else:
                print("No dataset found.")
                continue
                
        dims = SDMXService.parse_dimensions(struct)
        print(f"Dataset: {dataset_id}")
        map_entry = {"id": dataset_id, "dimensions": {}}
        
        for d in dims:
            dom_id = d["id"]
            d_name = d["name"]
            print(f"  Dim: {dom_id} ({d_name})")
            
            # Intelligent filtering for QA mapping
            # We want to find codes for: Sydney, Melbourne, Automotive Fuel, Food, Construction, Mining
            keywords = ["Sydney", "Melbourne", "Automotive", "Food", "Construction", "Mining", "Males", "Females"]
            
            matches = []
            for v in d["values"]:
                v_name = v["name"]
                if any(k.lower() in v_name.lower() for k in keywords):
                    matches.append(f"{v['id']}={v_name}")
            
            if matches:
                print(f"    Keywords found: {matches[:10]}")
                map_entry["dimensions"][dom_id] = matches
            else:
                # Save sample if no keywords matched, just in case
                codes = list(d["values"])[:3]
                map_entry["dimensions"][dom_id] = [c["id"] + "=" + c["name"] for c in codes]
            
        mapping[t["name"]] = map_entry
        
    # Validation helper
    print("\n\n=== MAPPING RESULT ===")
    print(json.dumps(mapping, indent=2))

if __name__ == "__main__":
    map_datasets()
