"""
Predefined example queries that work well with the ABS MCP Server.
Used for autocomplete suggestions in the UI.
"""

EXAMPLE_QUERIES = [
    # Inflation / CPI
    "What is the current inflation rate?",
    "What is the inflation rate in Sydney?",
    "What was the inflation rate last year?",
    "How have prices changed?",
    
    # Employment
    "What is the current unemployment rate?",
    "What is the unemployment rate in Australia?",
    "What is the participation rate?",
    "How many people are employed?",
    
    # Population
    "What is the population of Perth?",
    "What is the population of Sydney?",
    "What is the population of Melbourne?",
    "What is the population of Australia?",
    "What is the population of New South Wales?",
    
    # GDP / Economy
    "What is the current GDP?",
    "What is Australia's economic growth rate?",
    
    # Wages
    "What are average weekly earnings?",
    "What is the average wage in Australia?",
]

def get_suggestions(partial_query: str, max_suggestions: int = 5):
    """
    Returns matching example queries based on partial input.
    
    Args:
        partial_query: The text user has typed so far
        max_suggestions: Maximum number of suggestions to return
        
    Returns:
        List of matching example queries
    """
    if not partial_query or len(partial_query) < 2:
        # Show all examples if query is too short
        return EXAMPLE_QUERIES[:max_suggestions]
    
    partial_lower = partial_query.lower()
    
    # Find matches (case-insensitive substring search)
    matches = [
        query for query in EXAMPLE_QUERIES
        if partial_lower in query.lower()
    ]
    
    return matches[:max_suggestions]
