import sys
import os
import json

# Add src to path
sys.path.append(os.path.abspath("src"))

from abs_mcp_server.sdmx_service import SDMXService

def map_census():
    print("--- Searching for Census 2021 ---")
    
    # "Census 2021" might yield hundreds. We want General Community Profiles (GCP) or similar.
    # Usually "ABS_CENSUS2021_G01" etc.
    results = SDMXService.search_datasets("Census 2021", limit=10)
    
    print(f"Found {len(results)} matches.")
    targets = []
    
    # Look for "Country of Birth" or "Language"
    for r in results:
        print(f"  {r['id']}: {r['name']}")
        if "GCP" in r['id'] or "G01" in r['id'] or "Country of Birth" in r['name']:
            targets.append(r['id'])
            
    # If no specific GCP found, let's try searching "Country of Birth"
    if not targets:
        print("Searching specific topics...")
        cob_res = SDMXService.search_datasets("Country of Birth", limit=5)
        for r in cob_res:
             print(f"  {r['id']}: {r['name']}")
             targets.append(r['id'])
             
    # Pick one target to map dimensions
    if targets:
        t_id = targets[0]
        print(f"\nScanning: {t_id}")
        try:
            struct = SDMXService.get_structure(t_id)
            dims = SDMXService.parse_dimensions(struct)
            
            print(f"Dataset: {t_id}")
            for d in dims:
                print(f"  Dim: {d['id']} ({d['name']})")
                # Check for "Mandarin" or "England"
                matches = []
                for v in d['values']:
                    if "Mandarin" in v['name'] or "England" in v['name']:
                        matches.append(f"{v['id']}={v['name']}")
                if matches:
                    print(f"    Keywords found: {matches}")
                    
        except Exception as e:
            print(f"Error scanning {t_id}: {e}")

if __name__ == "__main__":
    map_census()
