import requests
import json

ABS_API_BASE = "https://api.data.abs.gov.au"

def get_structure_deep(dataset_id, name_hint=""):
    print(f"\n=== INSPECTING: {dataset_id} ({name_hint}) ===")
    
    # Method 1: Data endpoint with no filtering (defaults to structure usually, or default slice)
    # We want to see DIMENSIONS and their VALUES (Codes)
    url = f"{ABS_API_BASE}/data/{dataset_id}"
    params = {"detail": "full"} 
    
    try:
        r = requests.get(url, params=params, headers={"Accept": "application/vnd.sdmx.data+json"}, timeout=20)
        if r.status_code != 200:
             print(f"  [Warn] Default Fetch failed: {r.status_code}. Trying with startPeriod=2022")
             r = requests.get(url, params={**params, "startPeriod": "2022"}, headers={"Accept": "application/vnd.sdmx.data+json"}, timeout=20)
        
        if r.status_code != 200:
            print(f"  [Error] Failed to get structure for {dataset_id}")
            return

        data = r.json()
        structure = data.get("structure", {})
        dimensions = structure.get("dimensions", {}).get("observation", [])
        
        print(f"  Dimensions Found: {len(dimensions)}")
        for dim in dimensions:
            d_id = dim['id']
            d_name = dim['name']
            
            # Print Codes
            values = dim.get("values", [])
            print(f"    Dim: {d_id} ({d_name}) - {len(values)} codes")
            
            # Smart sampling: look for keywords user cares about
            keywords = ["Percentage", "Change", "Index", "Sydney", "Australia", "Person", "Unemployment", "Seasonally"]
            
            matching_codes = []
            for v in values:
                v_name = v.get("name", "")
                if any(k.lower() in v_name.lower() for k in keywords):
                    matching_codes.append(f"{v['id']}='{v_name}'")
            
            # Print top 5 matches or first 5
            if matching_codes:
                print(f"      Matched Codes: {matching_codes[:5]} ...")
            else:
                print(f"      Sample Codes: {[v['id'] + '=' + v['name'] for v in values[:3]]}")

    except Exception as e:
        print(f"Error: {e}")

def main():
    # Level 1 Targets
    # CPI is usually 'CPI'
    get_structure_deep("CPI", "Consumer Price Index")
    
    # Labour Force
    # Try LF
    get_structure_deep("LF", "Labour Force")
    
    # ERP
    # Try ABS_ERP_ASGS2021 (from previous search) 
    # Or 'ERP_QUARTERLY' if it exists.
    # Searching identified: ABS_ANNUAL_ERP_ASGS2021
    get_structure_deep("ABS_ANNUAL_ERP_ASGS2021", "Est. Resident Pop")
    
    # GDP (National Accounts)
    # Try finding the code 'ANA' or '5206' (ABS Cat number)
    # Previous search showed stuff like ABS_SU_TABLE.
    # Let's search specifically for "National Accounts" ID again if needed.
    
if __name__ == "__main__":
    main()
