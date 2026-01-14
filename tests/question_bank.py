"""
Comprehensive question bank for ABS MCP Agent testing.
Each entry includes: query, expected dataset, validation criteria, and tags.
"""

QUESTION_BANK = [
    # === INFLATION QUERIES ===
    {
        "query": "What is the current inflation rate?",
        "expected_dataset": "CPI_M",
        "expected_search_calls": 0,  # Should use mapping directly
        "validation": {"contains": ["inflation", "%"], "numeric": True},
        "tags": ["inflation", "cpi", "basic"]
    },
    {
        "query": "What was the inflation rate last year?",
        "expected_dataset": "CPI_M",
        "expected_search_calls": 0,
        "validation": {"contains": ["%"], "numeric": True},
        "tags": ["inflation", "historical"]
    },
    {
        "query": "How has inflation changed over the last 12 months?",
        "expected_dataset": "CPI_M",
        "expected_search_calls": 0,
        "validation": {"contains": ["%"], "numeric": True},
        "tags": ["inflation", "trend"]
    },
    {
        "query": "What is the CPI for Sydney?",
        "expected_dataset": "CPI_M",
        "expected_search_calls": 0,
        "validation": {"contains": ["Sydney"], "numeric": True},
        "tags": ["inflation", "regional"]
    },
    
    # === POPULATION QUERIES ===
    {
        "query": "What is the population of Perth?",
        "expected_dataset": "ABS_ANNUAL_ERP_ASGS2021",
        "expected_search_calls": 0,
        "validation": {"contains": ["Perth"], "numeric": True, "min_value": 2000000},
        "tags": ["population", "basic", "regional"]
    },
    {
        "query": "What is the population of Sydney?",
        "expected_dataset": "ABS_ANNUAL_ERP_ASGS2021",
        "expected_search_calls": 0,
        "validation": {"contains": ["Sydney"], "numeric": True, "min_value": 5000000},
        "tags": ["population", "basic", "regional"]
    },
    {
        "query": "What is the population of Melbourne?",
        "expected_dataset": "ABS_ANNUAL_ERP_ASGS2021",
        "expected_search_calls": 0,
        "validation": {"contains": ["Melbourne"], "numeric": True, "min_value": 4500000},
        "tags": ["population", "basic", "regional"]
    },
    {
        "query": "What is the population of Brisbane?",
        "expected_dataset": "ABS_ANNUAL_ERP_ASGS2021",
        "expected_search_calls": 0,
        "validation": {"contains": ["Brisbane"], "numeric": True, "min_value": 2000000},
        "tags": ["population", "basic", "regional"]
    },
    {
        "query": "What is the population of Adelaide?",
        "expected_dataset": "ABS_ANNUAL_ERP_ASGS2021",
        "expected_search_calls": 0,
        "validation": {"contains": ["Adelaide"], "numeric": True, "min_value": 1000000},
        "tags": ["population", "basic", "regional"]
    },
    
    # === EMPLOYMENT QUERIES ===
    {
        "query": "What is the current unemployment rate?",
        "expected_dataset": "LF",
        "expected_search_calls": 0,
        "validation": {"contains": ["unemployment", "%"], "numeric": True},
        "tags": ["employment", "unemployment", "basic"]
    },
    {
        "query": "What is the employment rate in Australia?",
        "expected_dataset": "LF",
        "expected_search_calls": 0,
        "validation": {"contains": ["%"], "numeric": True},
        "tags": ["employment", "basic"]
    },
    {
        "query": "How many people are employed in Australia?",
        "expected_dataset": "LF",
        "expected_search_calls": 0,
        "validation": {"numeric": True, "min_value": 10000000},
        "tags": ["employment", "count"]
    },
    {
        "query": "What is the labor force participation rate?",
        "expected_dataset": "LF",
        "expected_search_calls": 0,
        "validation": {"contains": ["%"], "numeric": True},
        "tags": ["employment", "participation"]
    },
    
    # === GDP QUERIES ===
    {
        "query": "What is Australia's GDP?",
        "expected_dataset": "ANA_EXP",
        "expected_search_calls": 0,
        "validation": {"contains": ["GDP"], "numeric": True},
        "tags": ["gdp", "economy", "basic"]
    },
    {
        "query": "What is the GDP growth rate?",
        "expected_dataset": "ANA_EXP",
        "expected_search_calls": 0,
        "validation": {"contains": ["%"], "numeric": True},
        "tags": ["gdp", "growth"]
    },
    
    # === WAGES QUERIES ===
    {
        "query": "What is the average weekly earnings?",
        "expected_dataset": "AWE",
        "expected_search_calls": 0,
        "validation": {"contains": ["earnings"], "numeric": True},
        "tags": ["wages", "earnings", "basic"]
    },
    {
        "query": "How much do Australians earn on average?",
        "expected_dataset": "AWE",
        "expected_search_calls": 0,
        "validation": {"numeric": True},
        "tags": ["wages", "average"]
    },
    
    # === RETAIL QUERIES ===
    {
        "query": "What is the retail trade turnover?",
        "expected_dataset": "RT",
        "expected_search_calls": 0,
        "validation": {"contains": ["retail"], "numeric": True},
        "tags": ["retail", "trade", "basic"]
    },
    {
        "query": "How is the retail sector performing?",
        "expected_dataset": "RT",
        "expected_search_calls": 0,
        "validation": {"contains": ["retail"]},
        "tags": ["retail", "trend"]
    },
    
    # === COMPLEX QUERIES ===
    {
        "query": "Compare inflation rates between Sydney and Melbourne",
        "expected_dataset": "CPI_M",
        "expected_search_calls": 0,
        "validation": {"contains": ["Sydney", "Melbourne"], "numeric": True},
        "tags": ["inflation", "comparison", "advanced"]
    },
    {
        "query": "What are the population trends in major Australian cities?",
        "expected_dataset": "ABS_ANNUAL_ERP_ASGS2021",
        "expected_search_calls": 0,
        "validation": {"contains": ["population"]},
        "tags": ["population", "trend", "advanced"]
    },
    {
        "query": "Show me unemployment numbers for the past quarter",
        "expected_dataset": "LF",
        "expected_search_calls": 0,
        "validation": {"contains": ["unemployment"], "numeric": True},
        "tags": ["employment", "time-series", "advanced"]
    },
    
    # === EDGE CASES ===
    {
        "query": "What's the latest CPI data?",
        "expected_dataset": "CPI_M",
        "expected_search_calls": 0,
        "validation": {"contains": ["CPI"], "numeric": True},
        "tags": ["inflation", "edge-case"]
    },
    {
        "query": "Population statistics for Perth metro area",
        "expected_dataset": "ABS_ANNUAL_ERP_ASGS2021",
        "expected_search_calls": 0,
        "validation": {"contains": ["Perth"], "numeric": True},
        "tags": ["population", "edge-case"]
    },
]

def get_questions_by_tag(tag: str):
    """Get all questions with a specific tag."""
    return [q for q in QUESTION_BANK if tag in q.get("tags", [])]

def get_random_questions(count: int = 10):
    """Get random sample of questions."""
    import random
    return random.sample(QUESTION_BANK, min(count, len(QUESTION_BANK)))

def get_basic_questions():
    """Get basic/fundamental questions."""
    return get_questions_by_tag("basic")

def get_advanced_questions():
    """Get complex/advanced questions."""
    return get_questions_by_tag("advanced")
