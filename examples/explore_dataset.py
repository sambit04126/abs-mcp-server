
import requests
import json
from src.abs_mcp_server.sdmx_service import SDMXService

def check_cpi():
    dataset_id = "CPI"
    print(f"Checking structure for {dataset_id}...")
    
    # 1. Structure
    structure = SDMXService.get_structure(dataset_id)
    dimensions = SDMXService.parse_dimensions(structure)
    print("Dimensions:")
    for d in dimensions:
        print(f"  {d['id']}: {[v['id'] for v in d['values'][:5]]}...")

    # 2. Test Fetch - specific for Sydney
    # Path: MEASURE.INDEX.TSEST.REGION.FREQ
    # We suspect FREQ is required or implicitly Q.
    
    # Filters based on previous failure
    # REGION: 1 (Sydney)
    # MEASURE: 3 (Percentage Change)
    # INDEX: 10001 (All groups CPI)
    # TSEST: 10 (Original)
    
    # Let's verify the ID for Region Sydney.
    region_dim = next((d for d in dimensions if d['id'] == "REGION"), None)
    if region_dim:
        syd = next((v for v in region_dim['values'] if "Sydney" in v['name']), None)
        print(f"Sydney Code: {syd}")
    
    # Construct key manually for test
    # Order matters!
    # Usually: MEASURE.INDEX.TSEST.REGION.FREQ
    
    # Try 1: With M frequency (Should fail for CPI quarterly, but maybe exist?)
    key_m = "3.10001.10.1.M"
    print(f"\nFetching Key (Monthly): {key_m}")
    data_m = SDMXService.get_data(dataset_id, key_m)
    if data_m:
        print("Result M: Found (Structure present)")
        obs = SDMXService.parse_observations(data_m, dimensions)
        print(f"Observations Count: {len(obs)}")
        if obs:
            print(f"Sample Dates: {[o['Time Period'] for o in obs[:5]]}")
    else:
        print("Result M: None (404)")
    
    # Try 2: With Q frequency
    key_q = "3.10001.10.1.Q"
    print(f"\nFetching Key (Quarterly): {key_q}")
    data_q = SDMXService.get_data(dataset_id, key_q)
    print(f"Result Q: {'Found' if data_q else 'None'}")
    
    # Try 3: Missing Frequency (The 422 case) - Try with wildcard manually by adding dot?
    key_wildcard = "3.10001.10.1."
    print(f"\nFetching Key (Wildcard Freq): {key_wildcard}")
    data_wild = SDMXService.get_data(dataset_id, key_wildcard)
    print(f"Result Wildcard: {'Found' if data_wild else '404/Error'}")
    
    # Check CPI_M (Monthly Indicator) for Sydney
    dataset_m = "CPI_M"
    print(f"\nChecking {dataset_m} for Sydney...")
    structure_m = SDMXService.get_structure(dataset_m)
    dims_m = SDMXService.parse_dimensions(structure_m)
    
    # Check if Sydney (1) is in REGION for CPI_M
    reg_m = next((d for d in dims_m if d['id'] == "REGION"), None)
    if reg_m:
        syd_m = next((v for v in reg_m['values'] if "Sydney" in v['name']), None)
        print(f"Sydney in CPI_M: {syd_m}")
    else:
        print("REGION dimension not found in CPI_M")
        
    # Fetch sample CPI_M for Sydney?
    # Key: MEASURE.INDEX.TSEST.REGION.FREQ (Assume same order?)
    # Let's trust structure order.
    # We will try to fetch if Sydney code exists.
    if reg_m and syd_m:
         # Construct key
         # MEASURE=3 (Change), INDEX=10001 (All groups), TSEST=10, REGION=1, FREQ=M
         # Check dims_m to be sure of order.
         pass

if __name__ == "__main__":
    check_cpi()
