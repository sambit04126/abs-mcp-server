"""
Test script to verify all example queries work consistently.
Run this to validate the agent's performance across different query types.
"""

import asyncio
import sys
import os

# Add src/client to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src', 'client'))

from mcp_agent import MCPAgent
from dotenv import load_dotenv

load_dotenv()

# Test queries covering all major topics
TEST_QUERIES = [
    # Inflation/CPI
    ("What is the current inflation rate?", "CPI_M"),
    
    # Employment
    ("What is the current unemployment rate?", "LF"),
    
    # Population
    ("What is the population of Perth?", "ABS_ANNUAL_ERP_ASGS2021"),
    ("What is the population of Sydney?", "ABS_ANNUAL_ERP_ASGS2021"),
]

async def test_query(agent, query, expected_dataset):
    """Test a single query and track tool calls."""
    print(f"\n{'='*80}")
    print(f"Testing: {query}")
    print(f"Expected Dataset: {expected_dataset}")
    print(f"{'='*80}\n")
    
    search_count = 0
    datasets_used = []
    
    async for event_type, content in agent.process_query(query):
        if event_type == "log":
            if "search_datasets" in content:
                search_count += 1
            if "get_dataset_structure" in content and "dataset_id" in content:
                # Extract dataset ID from the log
                import json
                try:
                    if "Arguments:" in content:
                        args_start = content.find("{")
                        if args_start != -1:
                            args_json = content[args_start:content.find("}", args_start)+1]
                            args = json.loads(args_json)
                            if "dataset_id" in args:
                                datasets_used.append(args["dataset_id"])
                except:
                    pass
        elif event_type == "answer":
            print(f"\n✅ Answer: {content}\n")
            
    print(f"📊 Metrics:")
    print(f"   Search calls: {search_count}")
    print(f"   Datasets used: {datasets_used}")
    print(f"   Expected: {expected_dataset}")
    
    if search_count == 0:
        print(f"   ✅ OPTIMAL - No search needed!")
    elif search_count == 1:
        print(f"   ⚠️  OK - 1 search (acceptable)")
    else:
        print(f"   ❌ INEFFICIENT - {search_count} searches")
    
    if expected_dataset in datasets_used:
        print(f"   ✅ Correct dataset used")
    else:
        print(f"   ❌ Wrong dataset: {datasets_used}")
    
    return search_count, datasets_used

async def main():
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("ERROR: GOOGLE_API_KEY not found in environment")
        return
    
    agent = MCPAgent(api_key=api_key)
    
    print("\n" + "="*80)
    print("ABS MCP AGENT - CONSISTENCY TEST")
    print("="*80)
    
    total_searches = 0
    for query, expected_ds in TEST_QUERIES:
        searches, _ = await test_query(agent, query, expected_ds)
        total_searches += searches
        await asyncio.sleep(2)  # Rate limiting
    
    print(f"\n" + "="*80)
    print(f"SUMMARY")
    print(f"="*80)
    print(f"Total queries: {len(TEST_QUERIES)}")
    print(f"Total searches: {total_searches}")
    print(f"Average searches per query: {total_searches / len(TEST_QUERIES):.1f}")
    print(f"\nTarget: 0-1 searches per query")

if __name__ == "__main__":
    asyncio.run(main())
