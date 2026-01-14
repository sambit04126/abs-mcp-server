import sys
import os
import json
import logging

# Add src to path
sys.path.append(os.path.abspath("src"))

from abs_mcp_server.sdmx_service import SDMXService

# Configure logging to show info
logging.basicConfig(level=logging.INFO)

def establish_ground_truth():
    queries = [
        {
            "id": "q1_inflation",
            "question": "What is the current inflation rate?",
            "dataset": "CPI",
            "filters": {
                "MEASURE": "3",  # Percentage Change from Corresponding Quarter of Previous Year
                "INDEX": "10001", # All groups CPI
                "REGION": "50",   # Weighted Average of Eight Capital Cities
                "TSEST": "10",    # Original
                "FREQ": "M"       # Using Monthly as per verification sample
            },
            "expect_latest": True
        },
        {
            "id": "q2_unemployment",
            "question": "What is the current Australia unemployment rate?",
            "dataset": "LF",
            "filters": {
                "MEASURE": "M13", # Unemployment rate (Confirmed)
                "TSEST": "30",    # Seasonally Adjusted
                "REGION": "AUS",
                "SEX": "3",       # Persons
                "AGE": "1599",    # 15+
                "FREQ": "M"       # Monthly
            },
            "expect_latest": True
        },
        {
            "id": "q3_population",
            "question": "What is the population of Australia?",
            "dataset": "ABS_ANNUAL_ERP_ASGS",
            "filters": {
                "MEASURE": "ERP", # Estimated Resident Population
                "REGION_TYPE": "AUS",
                "ASGS_2011": "0", # Australia
                "FREQUENCY": "A"  # Annual
            },
        },
        # Level 2: Dimensional Filtering
        {
            "id": "q4_cpi_sydney",
            "question": "What is the inflation rate in Sydney?",
            "dataset": "CPI",
            "filters": {
                "MEASURE": "3",  # Percentage Change
                "INDEX": "10001", # All groups
                "REGION": "1",    # Sydney (Verified code)
                "TSEST": "10",
                "FREQ": "M"
            },
            "expect_latest": True
        },
        {
            "id": "q5_fuel_price",
            "question": "What is the price index for Automotive Fuel?",
            "dataset": "CPI",
            "filters": {
                "MEASURE": "1",    # Index Number (Price level)
                "INDEX": "40081",  # Automotive fuel (Verified code)
                "REGION": "50",    # Avg 8 Capabilities
                "TSEST": "10",
                "FREQ": "M"
            },
            "expect_latest": True
        },
        # Level 3: Comparisons / Other Datasets
        {
            "id": "q6_retail_vic",
            "question": "What is the turnover for Department Stores in Victoria?",
            "dataset": "RT",
            "filters": {
                "INDUSTRY": "44", # Department Stores (Verified)
                "REGION": "2",    # Victoria
                "MEASURE": "20",  # Turnover at current prices
                "TSEST": "20",    # Seasonally Adjusted
                "FREQ": "M"
            },
            "expect_latest": True
        }
    ]
    
    results = {}
    
    print("--- Establishing Ground Truth ---")
    
    for q in queries:
        print(f"Running: {q['question']}")
        try:
            # 1. Fetch Structure (Simulate agent workflow)
            struct = SDMXService.get_structure(q['dataset'])
            dims = SDMXService.parse_dimensions(struct)
            
            print(f"  Dims found: {[d['id'] for d in dims]}")
            
            # 2. Construct Key from Filters
            key_parts = []
            for dim in dims:
                dim_id = dim.get("id")
                # Time period is not part of the path key in SDMX usually
                if dim_id == "TIME_PERIOD":
                    continue
                    
                if dim_id in q['filters']:
                    key_parts.append(q['filters'][dim_id])
                else:
                    key_parts.append("")
            
            # Strip trailing empty parts for cleaner key
            # But technically SDMX allows "A.B..D" if C is empty.
            # However "A.B." at the end is usually "A.B"
            
            path_key = ".".join(key_parts)
            if path_key.endswith("."):
                path_key = path_key.rstrip(".")
            
            path_key = path_key if path_key else "all"
            print(f"  Generated Key: {path_key}")
            
            # 3. Fetch Data
            data = SDMXService.get_data(q['dataset'], path_key)
            
            # 4. Parse Observations
            resp_struct = SDMXService._parse_structure(data)
            resp_dims = SDMXService.parse_dimensions(resp_struct)
            observations = SDMXService.parse_observations(data, resp_dims)
            
            # Sort by time/value if possible? 
            # The API returns time series usually. The last one is the latest.
            # SDMX JSON observations keys usually imply time if TimePeriod is a dimension.
            # But our parse_observations flattens them. 
            # We should assume the list order roughly follows input, but let's check.
            
            if q['expect_latest'] and observations:
                # Find the one with the "latest" time period? 
                # For now, just take the last observation in the list as "latest"
                # assuming the API returns chronological order (standard SDMX behavior).
                latest_obs = observations[-1]
                val = latest_obs.get("value")
                
                # Try to find date info
                time_val = "Unknown"
                for k, v in latest_obs.items():
                    if "TIME" in k.upper() or "Quarter" in k or "Month" in k or "Year" in k:
                         # Heuristic for time label
                         time_val = v
                
                print(f"  Result: {val} ({time_val})")
                results[q['id']] = {
                    "question": q['question'],
                    "dataset": q['dataset'],
                    "key": path_key,
                    "latest_value": val,
                    "latest_period": time_val,
                    "full_obs": latest_obs
                }
            else:
                print("  No observations found.")
                results[q['id']] = {"error": "No data"}
                
        except Exception as e:
            print(f"  Error: {e}")
            results[q['id']] = {"error": str(e)}
            
    # Save to file
    with open("ground_truth.json", "w") as f:
        json.dump(results, f, indent=2)
    print("\nSaved to ground_truth.json")

if __name__ == "__main__":
    establish_ground_truth()
