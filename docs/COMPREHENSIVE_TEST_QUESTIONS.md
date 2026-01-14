# 50-Question Comprehensive Test Suite

## Overview

**50 questions** organized by increasing complexity (Level 1-4) covering all 17 mapped topics.

## Complexity Levels

### Level 1: Basic (13 questions)
- Simple, direct, single-fact queries
- Expected: Immediate answer with minimal processing
- Topics: Inflation, Population, Employment, GDP, Wages, Retail

**Examples:**
- "What is the current inflation rate?"
- "What is the population of Sydney?"
- "What is the unemployment rate?"

### Level 2: Intermediate (19 questions)
- Queries with filters, regional specifics, or time-based constraints
- Expected: Answer with one filter dimension
- Topics: All cities, historical data, regional variations

**Examples:**
- "What was the inflation rate last year?"
- "What is the CPI for Sydney?"
- "What is the population of Brisbane?"

### Level 3: Advanced (10 questions)
- Comparisons, trends, multi-part questions
- Expected: Analysis across time or regions
- Topics: Trends, comparisons, time-series

**Examples:**
- "How has inflation changed over the last 12 months?"
- "Compare inflation rates between Sydney and Melbourne"
- "What are the population trends in major Australian cities?"

### Level 4: Complex (8 questions)
- Deep analysis, multiple dimensions, comprehensive queries
- Expected: Multi-dataset usage, complex reasoning
- Topics: Economic indicators, multi-topic analysis, relationships

**Examples:**
- "What are the main economic indicators for Australia right now?"
- "Analyze the economic performance of Australia in the past year"
- "What's happening with cost of living in Australian capital cities?"

## Topic Coverage

| Topic | Level 1 | Level 2 | Level 3 | Level 4 | Total |
|-------|---------|---------|---------|---------|-------|
| Inflation/CPI | 3 | 4 | 3 | 2 | 12 |
| Population | 3 | 5 | 3 | 2 | 13 |
| Employment | 2 | 3 | 3 | 1 | 9 |
| GDP | 2 | 2 | 0 | 2 | 6 |
| Wages | 2 | 2 | 1 | 0 | 5 |
| Retail | 1 | 2 | 0 | 0 | 3 |
| Multi-Topic | 0 | 0 | 2 | 1 | 3 |

## Usage

### Test by Level
```bash
# Basic questions only
python tests/test_randomized.py --tag level-1

# Intermediate
python tests/test_randomized.py --tag level-2

# Advanced
python tests/test_randomized.py --tag level-3

# Complex
python tests/test_randomized.py --tag level-4
```

### Progressive Testing
```bash
# 3 questions from each level (12 total)
python -c "
from tests.comprehensive_questions import get_progressive_sample, print_stats
print_stats()
questions = get_progressive_sample(n_per_level=3)
for q in questions:
    print(f'L{q[\"level\"]}: {q[\"query\"]}')
"
```

### Test by Topic
```bash
# All inflation questions
python tests/test_randomized.py --tag inflation

# All population questions
python tests/test_randomized.py --tag population
```

## Validation Criteria

Each question includes:
- **Expected Dataset**: Which dataset should be used
- **Expected Search Calls**: 0-1 (efficiency check)
- **Validation Rules**:
  - Keywords that must appear
  - Numeric values required
  - Min/max value ranges
  - Regional names

## Example Test Run

```python
from tests.comprehensive_questions import COMPREHENSIVE_QUESTION_BANK, get_questions_by_level

# Test Level 1 (Basic)
level_1 = get_questions_by_level(1)
print(f"Testing {len(level_1)} basic questions...")

for q in level_1:
    print(f"Q{q['id']}: {q['query']}")
    # Expected: Quick, accurate answer with 0 searches
```

## Success Criteria

| Level | Target Pass Rate | Avg Response Time | Max Searches |
|-------|-----------------|-------------------|--------------|
| 1 | ≥95% | <3s | 0 |
| 2 | ≥90% | <4s | 0-1 |
| 3 | ≥85% | <5s | 0-1 |
| 4 | ≥75% | <7s | 1-2 |

## Quick Reference Table

| ID | Level | Query | Topic |
|----|-------|-------|-------|
| 1 | 1 | What is the current inflation rate? | Inflation |
| 4 | 1 | What is the population of Sydney? | Population |
| 7 | 1 | What is the unemployment rate? | Employment |
| 14 | 2 | What was the inflation rate last year? | Inflation (Historical) |
| 18 | 2 | What is the population of Brisbane? | Population (Regional) |
| 32 | 3 | How has inflation changed over the last 12 months? | Inflation (Trend) |
| 35 | 3 | What are the population trends in major Australian cities? | Population (Analysis) |
| 43 | 4 | What are the main economic indicators for Australia right now? | Economy (Comprehensive) |
| 48 | 4 | What's happening with cost of living in Australian capital cities? | Multi-topic (Analysis) |

---

**Total**: 50 questions across 4 complexity levels  
**Coverage**: All 17 mapped topics  
**Ready for comprehensive validation testing!**
