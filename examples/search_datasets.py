import requests
import json

ABS_API_BASE = "https://api.data.abs.gov.au"

def discover_ids(keyword):
    print(f"\n--- Searching for: {keyword} ---")
    r = requests.get(f"{ABS_API_BASE}/dataflow", headers={"Accept": "application/vnd.sdmx.structure+json"})
    r.raise_for_status()
    flows = r.json().get("data", {}).get("dataflows", [])
    
    matches = []
    for f in flows:
        if keyword.lower() in f.get("name", "").lower():
            matches.append(f)
            
    print(f"Found {len(matches)} matches.")
    for m in matches[:10]: # List top 10
        print(f"  ID: {m['id']}  Name: {m['name']}")
        
    return matches

def check_structure(dataset_id):
    print(f"   Checking structure of {dataset_id}...")
    try:
        r = requests.get(f"{ABS_API_BASE}/data/{dataset_id}", 
                         headers={"Accept": "application/vnd.sdmx.data+json"},
                         params={"detail": "full", "startPeriod": "2023"})
        
        if r.status_code == 200:
             data = r.json()
             dims = data.get("structure", {}).get("dimensions", {}).get("observation", [])
             print(f"   -> Dimensions: {len(dims)}")
             if dims:
                 print(f"   -> First Dim: {dims[0]['id']}")
        else:
             print(f"   -> Status: {r.status_code}")
    except Exception as e:
        print(f"   -> Error: {e}")

def main():
    # CPI
    cpi = discover_ids("Consumer Price Index")
    # Try checking structure of 'CPI' and 'CPI_M'
    check_structure("CPI")
    check_structure("CPI_M")
    
    # Labour Force
    lf = discover_ids("Labour Force")
    # Check simple IDs if any
    for x in ["LF", "LABOUR_FORCE", "ABS_LF"]:
        check_structure(x)

    # ERP
    erp = discover_ids("Estimated Resident Population")
    # Check top match
    if erp:
        check_structure(erp[0]['id'])

if __name__ == "__main__":
    main()
