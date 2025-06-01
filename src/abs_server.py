import requests
from typing import List, Dict
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("abs-data")

@mcp.tool()
def search_datasets(keyword: str = "") -> List[Dict]:
    """Search available ABS datasets"""
    # We'll implement this next
    pass

@mcp.tool() 
def get_dataset_data(dataset_id: str) -> Dict:
    """Get data from specific ABS dataset"""
    # We'll implement this next
    pass

if __name__ == "__main__":
    mcp.run(transport='stdio')