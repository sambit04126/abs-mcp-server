# Randomized Test Suite

## Overview

The randomized test suite validates the ABS MCP Agent's consistency and reliability by running random subsets of queries from a comprehensive question bank.

## Question Bank

Located in `tests/question_bank.py`:
- **25 test queries** covering all major topics
- Categories: inflation, population, employment, GDP, wages, retail
- Each query includes:
  - Expected dataset
  - Validation criteria (text, numeric, ranges)
  - Tags for filtering
  - Expected search efficiency

## Running Tests

### Random Sample (Default)
```bash
python tests/test_randomized.py
```
Runs 10 random tests from the bank.

### Custom Count
```bash
python tests/test_randomized.py --count 20
```

### Filter by Tag
```bash
python tests/test_randomized.py --tag basic    # Basic queries only
python tests/test_randomized.py --tag advanced # Complex queries
```

### Reproducible Tests
```bash
python tests/test_randomized.py --seed 42
```
Uses fixed random seed for reproducible results.

## Validation Criteria

Each test validates:
1. ✅ **Response Quality**: Contains expected keywords
2. ✅ **Numeric Accuracy**: Valid numbers within expected ranges
3. ✅ **Search Efficiency**: <= expected search calls (target: 0-1)
4. ✅ **Dataset Correctness**: Uses the right dataset
5. ✅ **Response Time**: Completes within reasonable time

## Example Output

```
================================================================================
RUNNING 10 RANDOMIZED TESTS
================================================================================

[1/10] Testing: What is the current inflation rate?
    ✅ PASS - 3.2s - 0 searches

[2/10] Testing: What is the population of Sydney?
    ✅ PASS - 4.1s - 0 searches

[3/10] Testing: What is the retail trade turnover?
    ❌ FAIL (1 errors) - 5.3s - 2 searches

================================================================================
TEST SUMMARY
================================================================================

Total Tests: 10
✅ Passed: 9 (90.0%)
❌ Failed: 1
⏱️  Avg Duration: 3.8s
🔍 Avg Searches: 0.2
```

## CI/CD Integration

Add to GitHub Actions:

```yaml
- name: Run Randomized Tests
  run: |
    python tests/test_randomized.py --count 10 --seed ${{ github.run_number }}
```

## Adding New Questions

Edit `tests/question_bank.py`:

```python
{
    "query": "Your new query here",
    "expected_dataset": "DATASET_ID",
    "expected_search_calls": 0,
    "validation": {
        "contains": ["keyword1", "keyword2"],
        "numeric": True,
        "min_value": 1000
    },
    "tags": ["category", "difficulty"]
}
```

## Tags

- `basic`: Simple, single-fact queries
- `advanced`: Complex or multi-part queries
- `inflation`, `population`, `employment`, `gdp`, `wages`, `retail`: Topic tags
- `regional`: City-specific queries
- `historical`: Time-based queries
- `trend`: Trend analysis queries
- `edge-case`: Unusual phrasing or edge cases
