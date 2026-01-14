"""
Comprehensive 50-Question Test Suite for ABS MCP Agent
Organized by complexity level (1-4) covering all mapped topics.

Usage:
    python tests/run_comprehensive_test.py --level 1  # Basic only
    python tests/run_comprehensive_test.py --all      # All 50 questions
"""

COMPREHENSIVE_QUESTION_BANK = [
    
    # ============================================================================
    # LEVEL 1: BASIC QUERIES (Simple, single-fact, direct)
    # ============================================================================
    
    # Inflation/CPI (Basic)
    {
        "id": 1,
        "level": 1,
        "query": "What is the current inflation rate?",
        "expected_dataset": "CPI_M",
        "expected_search_calls": 0,
        "validation": {"contains": ["inflation", "%"], "numeric": True},
        "tags": ["inflation", "cpi", "basic", "level-1"]
    },
    {
        "id": 2,
        "level": 1,
        "query": "What is the CPI?",
        "expected_dataset": "CPI_M",
        "expected_search_calls": 0,
        "validation": {"contains": ["CPI"], "numeric": True},
        "tags": ["inflation", "cpi", "basic", "level-1"]
    },
    {
        "id": 3,
        "level": 1,
        "query": "Show me the latest inflation data",
        "expected_dataset": "CPI_M",
        "expected_search_calls": 0,
        "validation": {"contains": ["inflation"], "numeric": True},
        "tags": ["inflation", "basic", "level-1"]
    },
    
    # Population (Basic)
    {
        "id": 4,
        "level": 1,
        "query": "What is the population of Sydney?",
        "expected_dataset": "ABS_ANNUAL_ERP_ASGS2021",
        "expected_search_calls": 0,
        "validation": {"contains": ["Sydney"], "numeric": True, "min_value": 5000000},
        "tags": ["population", "regional", "basic", "level-1"]
    },
    {
        "id": 5,
        "level": 1,
        "query": "What is the population of Melbourne?",
        "expected_dataset": "ABS_ANNUAL_ERP_ASGS2021",
        "expected_search_calls": 0,
        "validation": {"contains": ["Melbourne"], "numeric": True, "min_value": 4500000},
        "tags": ["population", "regional", "basic", "level-1"]
    },
    {
        "id": 6,
        "level": 1,
        "query": "What is the population of Perth?",
        "expected_dataset": "ABS_ANNUAL_ERP_ASGS2021",
        "expected_search_calls": 0,
        "validation": {"contains": ["Perth"], "numeric": True, "min_value": 2000000},
        "tags": ["population", "regional", "basic", "level-1"]
    },
    
    # Employment (Basic)
    {
        "id": 7,
        "level": 1,
        "query": "What is the unemployment rate?",
        "expected_dataset": "LF",
        "expected_search_calls": 0,
        "validation": {"contains": ["unemployment", "%"], "numeric": True},
        "tags": ["employment", "unemployment", "basic", "level-1"]
    },
    {
        "id": 8,
        "level": 1,
        "query": "What is the current employment rate?",
        "expected_dataset": "LF",
        "expected_search_calls": 0,
        "validation": {"contains": ["%"], "numeric": True},
        "tags": ["employment", "basic", "level-1"]
    },
    
    # GDP (Basic)
    {
        "id": 9,
        "level": 1,
        "query": "What is Australia's GDP?",
        "expected_dataset": "ANA_EXP",
        "expected_search_calls": 0,
        "validation": {"contains": ["GDP"], "numeric": True},
        "tags": ["gdp", "economy", "basic", "level-1"]
    },
    {
        "id": 10,
        "level": 1,
        "query": "Show me the GDP data",
        "expected_dataset": "ANA_EXP",
        "expected_search_calls": 0,
        "validation": {"contains": ["GDP"]},
        "tags": ["gdp", "basic", "level-1"]
    },
    
    # Wages (Basic)
    {
        "id": 11,
        "level": 1,
        "query": "What is the average weekly earnings?",
        "expected_dataset": "AWE",
        "expected_search_calls": 0,
        "validation": {"contains": ["earnings"], "numeric": True},
        "tags": ["wages", "earnings", "basic", "level-1"]
    },
    {
        "id": 12,
        "level": 1,
        "query": "What are the average wages?",
        "expected_dataset": "AWE",
        "expected_search_calls": 0,
        "validation": {"numeric": True},
        "tags": ["wages", "basic", "level-1"]
    },
    
    # Retail (Basic)
    {
        "id": 13,
        "level": 1,
        "query": "What is the retail trade turnover?",
        "expected_dataset": "RT",
        "expected_search_calls": 0,
        "validation": {"contains": ["retail"], "numeric": True},
        "tags": ["retail", "trade", "basic", "level-1"]
    },
    
    # ============================================================================
    # LEVEL 2: INTERMEDIATE QUERIES (Filters, regional, time-based)
    # ============================================================================
    
    # Inflation (Intermediate)
    {
        "id": 14,
        "level": 2,
        "query": "What was the inflation rate last year?",
        "expected_dataset": "CPI_M",
        "expected_search_calls": 0,
        "validation": {"contains": ["%"], "numeric": True},
        "tags": ["inflation", "historical", "level-2"]
    },
    {
        "id": 15,
        "level": 2,
        "query": "What is the CPI for Sydney?",
        "expected_dataset": "CPI_M",
        "expected_search_calls": 0,
        "validation": {"contains": ["Sydney"], "numeric": True},
        "tags": ["inflation", "regional", "level-2"]
    },
    {
        "id": 16,
        "level": 2,
        "query": "Show me CPI for Melbourne",
        "expected_dataset": "CPI_M",
        "expected_search_calls": 0,
        "validation": {"contains": ["Melbourne"], "numeric": True},
        "tags": ["inflation", "regional", "level-2"]
    },
    {
        "id": 17,
        "level": 2,
        "query": "What was inflation in the last quarter?",
        "expected_dataset": "CPI_M",
        "expected_search_calls": 0,
        "validation": {"contains": ["%"], "numeric": True},
        "tags": ["inflation", "quarterly", "level-2"]
    },
    
    # Population (Intermediate)
    {
        "id": 18,
        "level": 2,
        "query": "What is the population of Brisbane?",
        "expected_dataset": "ABS_ANNUAL_ERP_ASGS2021",
        "expected_search_calls": 0,
        "validation": {"contains": ["Brisbane"], "numeric": True, "min_value": 2000000},
        "tags": ["population", "regional", "level-2"]
    },
    {
        "id": 19,
        "level": 2,
        "query": "What is the population of Adelaide?",
        "expected_dataset": "ABS_ANNUAL_ERP_ASGS2021",
        "expected_search_calls": 0,
        "validation": {"contains": ["Adelaide"], "numeric": True, "min_value": 1000000},
        "tags": ["population", "regional", "level-2"]
    },
    {
        "id": 20,
        "level": 2,
        "query": "What is the population of Canberra?",
        "expected_dataset": "ABS_ANNUAL_ERP_ASGS2021",
        "expected_search_calls": 0,
        "validation": {"contains": ["Canberra"], "numeric": True},
        "tags": ["population", "regional", "level-2"]
    },
    {
        "id": 21,
        "level": 2,
        "query": "What is the population of Hobart?",
        "expected_dataset": "ABS_ANNUAL_ERP_ASGS2021",
        "expected_search_calls": 0,
        "validation": {"contains": ["Hobart"], "numeric": True},
        "tags": ["population", "regional", "level-2"]
    },
    {
        "id": 22,
        "level": 2,
        "query": "What is the population of Darwin?",
        "expected_dataset": "ABS_ANNUAL_ERP_ASGS2021",
        "expected_search_calls": 0,
        "validation": {"contains": ["Darwin"], "numeric": True},
        "tags": ["population", "regional", "level-2"]
    },
    
    # Employment (Intermediate)
    {
        "id": 23,
        "level": 2,
        "query": "How many people are employed in Australia?",
        "expected_dataset": "LF",
        "expected_search_calls": 0,
        "validation": {"numeric": True, "min_value": 10000000},
        "tags": ["employment", "count", "level-2"]
    },
    {
        "id": 24,
        "level": 2,
        "query": "What is the labor force participation rate?",
        "expected_dataset": "LF",
        "expected_search_calls": 0,
        "validation": {"contains": ["%"], "numeric": True},
        "tags": ["employment", "participation", "level-2"]
    },
    {
        "id": 25,
        "level": 2,
        "query": "What was the unemployment rate last month?",
        "expected_dataset": "LF",
        "expected_search_calls": 0,
        "validation": {"contains": ["%"], "numeric": True},
        "tags": ["employment", "historical", "level-2"]
    },
    
    # GDP (Intermediate)
    {
        "id": 26,
        "level": 2,
        "query": "What is the GDP growth rate?",
        "expected_dataset": "ANA_EXP",
        "expected_search_calls": 0,
        "validation": {"contains": ["%"], "numeric": True},
        "tags": ["gdp", "growth", "level-2"]
    },
    {
        "id": 27,
        "level": 2,
        "query": "What was GDP last quarter?",
        "expected_dataset": "ANA_EXP",
        "expected_search_calls": 0,
        "validation": {"contains": ["GDP"], "numeric": True},
        "tags": ["gdp", "quarterly", "level-2"]
    },
    
    # Wages (Intermediate)
    {
        "id": 28,
        "level": 2,
        "query": "How much do Australians earn on average per week?",
        "expected_dataset": "AWE",
        "expected_search_calls": 0,
        "validation": {"numeric": True},
        "tags": ["wages", "average", "level-2"]
    },
    {
        "id": 29,
        "level": 2,
        "query": "What is the average salary in Australia?",
        "expected_dataset": "AWE",
        "expected_search_calls": 0,
        "validation": {"numeric": True},
        "tags": ["wages", "salary", "level-2"]
    },
    
    # Retail (Intermediate)
    {
        "id": 30,
        "level": 2,
        "query": "How is the retail sector performing?",
        "expected_dataset": "RT",
        "expected_search_calls": 0,
        "validation": {"contains": ["retail"]},
        "tags": ["retail", "trend", "level-2"]
    },
    {
        "id": 31,
        "level": 2,
        "query": "What was retail turnover last month?",
        "expected_dataset": "RT",
        "expected_search_calls": 0,
        "validation": {"contains": ["retail"], "numeric": True},
        "tags": ["retail", "historical", "level-2"]
    },
    
    # ============================================================================
    # LEVEL 3: ADVANCED QUERIES (Comparisons, trends, multi-part)
    # ============================================================================
    
    # Inflation (Advanced)
    {
        "id": 32,
        "level": 3,
        "query": "How has inflation changed over the last 12 months?",
        "expected_dataset": "CPI_M",
        "expected_search_calls": 0,
        "validation": {"contains": ["%"], "numeric": True},
        "tags": ["inflation", "trend", "time-series", "level-3"]
    },
    {
        "id": 33,
        "level": 3,
        "query": "Compare inflation rates between Sydney and Melbourne",
        "expected_dataset": "CPI_M",
        "expected_search_calls": 0,
        "validation": {"contains": ["Sydney", "Melbourne"], "numeric": True},
        "tags": ["inflation", "comparison", "advanced", "level-3"]
    },
    {
        "id": 34,
        "level": 3,
        "query": "What is the inflation trend this year?",
        "expected_dataset": "CPI_M",
        "expected_search_calls": 0,
        "validation": {"contains": ["inflation"], "numeric": True},
        "tags": ["inflation", "trend", "level-3"]
    },
    
    # Population (Advanced)
    {
        "id": 35,
        "level": 3,
        "query": "What are the population trends in major Australian cities?",
        "expected_dataset": "ABS_ANNUAL_ERP_ASGS2021",
        "expected_search_calls": 0,
        "validation": {"contains": ["population"]},
        "tags": ["population", "trend", "advanced", "level-3"]
    },
    {
        "id": 36,
        "level": 3,
        "query": "Compare population of Sydney and Melbourne",
        "expected_dataset": "ABS_ANNUAL_ERP_ASGS2021",
        "expected_search_calls": 0,
        "validation": {"contains": ["Sydney", "Melbourne"], "numeric": True},
        "tags": ["population", "comparison", "level-3"]
    },
    {
        "id": 37,
        "level": 3,
        "query": "Which city has the highest population growth?",
        "expected_dataset": "ABS_ANNUAL_ERP_ASGS2021",
        "expected_search_calls": 0,
        "validation": {"contains": ["population"]},
        "tags": ["population", "analysis", "level-3"]
    },
    
    # Employment (Advanced)
    {
        "id": 38,
        "level": 3,
        "query": "Show me unemployment numbers for the past quarter",
        "expected_dataset": "LF",
        "expected_search_calls": 0,
        "validation": {"contains": ["unemployment"], "numeric": True},
        "tags": ["employment", "time-series", "advanced", "level-3"]
    },
    {
        "id": 39,
        "level": 3,
        "query": "How has employment changed this year?",
        "expected_dataset": "LF",
        "expected_search_calls": 0,
        "validation": {"contains": ["employment"]},
        "tags": ["employment", "trend", "level-3"]
    },
    {
        "id": 40,
        "level": 3,
        "query": "What is the employment trend in the last 6 months?",
        "expected_dataset": "LF",
        "expected_search_calls": 0,
        "validation": {"contains": ["employment"]},
        "tags": ["employment", "trend", "level-3"]
    },
    
    # Multi-Topic (Advanced)
    {
        "id": 41,
        "level": 3,
        "query": "How does unemployment relate to GDP?",
        "expected_dataset": "LF",  # Will use both LF and ANA_EXP
        "expected_search_calls": 0,
        "validation": {"contains": ["unemployment", "GDP"]},
        "tags": ["employment", "gdp", "analysis", "multi-topic", "level-3"]
    },
    {
        "id": 42,
        "level": 3,
        "query": "Show me wage growth compared to inflation",
        "expected_dataset": "AWE",  # Will use both AWE and CPI_M
        "expected_search_calls": 0,
        "validation": {"contains": ["wage", "inflation"]},
        "tags": ["wages", "inflation", "comparison", "multi-topic", "level-3"]
    },
    
    # ============================================================================
    # LEVEL 4: COMPLEX QUERIES (Deep analysis, multiple dimensions)
    # ============================================================================
    
    # Complex Analysis
    {
        "id": 43,
        "level": 4,
        "query": "What are the main economic indicators for Australia right now?",
        "expected_dataset": "CPI_M",  # Will use multiple datasets
        "expected_search_calls": 0,
        "validation": {"contains": ["economic"]},
        "tags": ["economy", "multi-topic", "comprehensive", "level-4"]
    },
    {
        "id": 44,
        "level": 4,
        "query": "How have prices changed across different cities this year?",
        "expected_dataset": "CPI_M",
        "expected_search_calls": 0,
        "validation": {"contains": ["price"], "numeric": True},
        "tags": ["inflation", "regional", "trend", "advanced", "level-4"]
    },
    {
        "id": 45,
        "level": 4,
        "query": "What is the relationship between population growth and employment?",
        "expected_dataset": "ABS_ANNUAL_ERP_ASGS2021",
        "expected_search_calls": 0,
        "validation": {"contains": ["population", "employment"]},
        "tags": ["population", "employment", "analysis", "multi-topic", "level-4"]
    },
    {
        "id": 46,
        "level": 4,
        "query": "Analyze the economic performance of Australia in the past year",
        "expected_dataset": "ANA_EXP",
        "expected_search_calls": 0,
        "validation": {"contains": ["economic"]},
        "tags": ["economy", "analysis", "comprehensive", "level-4"]
    },
    {
        "id": 47,
        "level": 4,
        "query": "Compare economic indicators between 2023 and 2024",
        "expected_dataset": "CPI_M",
        "expected_search_calls": 0,
        "validation": {"contains": ["2023", "2024"]},
        "tags": ["economy", "comparison", "historical", "level-4"]
    },
    {
        "id": 48,
        "level": 4,
        "query": "What's happening with cost of living in Australian capital cities?",
        "expected_dataset": "CPI_M",
        "expected_search_calls": 0,
        "validation": {"contains": ["cost"]},
        "tags": ["inflation", "regional", "analysis", "level-4"]
    },
    {
        "id": 49,
        "level": 4,
        "query": "Show me quarterly economic trends for 2024",
        "expected_dataset": "ANA_EXP",
        "expected_search_calls": 0,
        "validation": {"contains": ["2024", "quarter"]},
        "tags": ["economy", "trend", "quarterly", "level-4"]
    },
    {
        "id": 50,
        "level": 4,
        "query": "What are the key demographic and economic changes in Australia?",
        "expected_dataset": "ABS_ANNUAL_ERP_ASGS2021",
        "expected_search_calls": 0,
        "validation": {"contains": ["demographic", "economic"]},
        "tags": ["population", "economy", "comprehensive", "multi-topic", "level-4"]
    },
]

def get_questions_by_level(level: int):
    """Get all questions at a specific complexity level."""
    return [q for q in COMPREHENSIVE_QUESTION_BANK if q["level"] == level]

def get_questions_by_tag(tag: str):
    """Get all questions with a specific tag."""
    return [q for q in COMPREHENSIVE_QUESTION_BANK if tag in q.get("tags", [])]

def get_random_questions(count: int = 10):
    """Get random sample of questions."""
    import random
    return random.sample(COMPREHENSIVE_QUESTION_BANK, min(count, len(COMPREHENSIVE_QUESTION_BANK)))

def get_progressive_sample(n_per_level: int = 3):
    """Get progressive sample across all levels."""
    import random
    sample = []
    for level in [1, 2, 3, 4]:
        questions = get_questions_by_level(level)
        sample.extend(random.sample(questions, min(n_per_level, len(questions))))
    return sample

# Summary statistics
def print_stats():
    """Print question bank statistics."""
    total = len(COMPREHENSIVE_QUESTION_BANK)
    by_level = {i: len(get_questions_by_level(i)) for i in [1, 2, 3, 4]}
    
    print(f"Total Questions: {total}")
    print(f"Level 1 (Basic): {by_level[1]}")
    print(f"Level 2 (Intermediate): {by_level[2]}")
    print(f"Level 3 (Advanced): {by_level[3]}")
    print(f"Level 4 (Complex): {by_level[4]}")
