
import sys
import os
import json
sys.path.append(os.path.abspath("src"))

from abs_mcp_server.server import search_datasets, get_dataset_structure

def explore():
    print("--- Step 1: Search ---")
    results = search_datasets("Regional Population")
    # If empty, try "ERP"
    if not results:
        print("Retrying with 'ERP'...")
        results = search_datasets("ERP")

    print(f"Found {len(results)} datasets.")
    for r in results[:10]:
        print(f"ID: {r['id']}, Name: {r['name']}")
    
    # Try to find one with "ERP" in ID which usually means Estimated Resident Population
    target_id = None
    for r in results:
        if "ERP" in r['id'] and "REGIONAL" in r['id']:
            target_id = r['id']
            break
            
    if not target_id and results:
         target_id = results[0]['id']

    print(f"\n--- Step 2: Structure for {target_id} ---")
    if target_id:
        struct = get_dataset_structure(target_id)
        
        if "error" in struct:
            print(f"Error: {struct['error']}")
            return

        print(f"Description: {struct.get('description')}")
        print("Dimensions:")
        found_perth_code = None
        for dim in struct.get("dimensions", []):
            print(f"  [{dim['id']}] {dim['name']}")
            # Print first few values
            values = dim.get("values", {})
            for k, v in values.items():
                if "Perth" in v:
                    print(f"    🌟 FOUND PERTH: {k} -> {v}")
                    found_perth_code = k
        
        if found_perth_code:
            print("\n--- Step 3: Fetch Data for Perth ---")
            # We need to construct filters. The Agent would do this by mapping dims.
            # I will try to fetch with just the region filter and let the others default (or guess).
            # Usually we need MEASURE, FREQ etc.
            # Let's see what keys are in dimensions.
            filters = {}
            for dim in struct.get("dimensions", []):
                if dim['id'] == "REGION" or dim['id'] == "ASGS_2011" or dim['id'] == "GCCSA" or "REGION" in dim['id']:
                     if found_perth_code in dim['values']: # Use the code we found for this specific dim
                         filters[dim['id']] = found_perth_code
            
            # Default for Measure usually "1" or "Estimated Resident Population"
            # I'll try to find a "Persons" measure or similar
            
            print(f"Attempting fetch with filters: {filters}")
            data = get_dataset_data(target_id, filters=filters)
            
            if "error" in data:
                 print(f"Fetch Error: {data['error']}")
                 # Try adding default measure?
            else:
                 sample = data.get("data_sample", [])
                 if sample:
                     print(f"Latest Data: {sample[-1]}")
                 else:
                     print("No observations returned.")
    
if __name__ == "__main__":
    explore()
