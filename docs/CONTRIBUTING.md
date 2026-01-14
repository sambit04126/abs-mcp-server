# Contributing to ABS MCP Server

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## 🚀 Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR_USERNAME/abs-mcp-server`
3. Create a branch: `git checkout -b feature/your-feature`
4. Install dependencies: `pip install -e .[dev]`

## 📋 Development Setup

```bash
# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install in editable mode with dev dependencies
pip install -e .[dev]

#Configure environment
cp .env.template .env
# Add your GOOGLE_API_KEY

# Run tests
pytest
```

## 🎯 What to Contribute

We welcome contributions in these areas:

### 1. New Dataset Mappings

Add more topics to `src/client/topic_mapping.py`:

```python
"retail_trade": {
    "dataset_id": "RT",
    "description": "Retail Turnover",
    "common_dimensions": {
        "MEASURE": "...",
        ...
    }
}
```

### 2. Example Queries

Add to `src/client/example_queries.py`:

```python
EXAMPLE_QUERIES = [
    ...
    "What is the retail trade turnover?",
]
```

### 3. Bug Fixes

- Check [Issues](https://github.com/yourusername/abs-mcp-server/issues)
- Create tests to reproduce the bug
- Fix and ensure tests pass

### 4. Documentation

- Improve README clarity
- Add code examples
- Document edge cases

## ✅ Code Quality

### Style Guidelines

- Follow PEP 8
- Use type hints
- Write docstrings for public functions

### Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src

# Run specific test
pytest tests/test_consistency.py::test_inflation_query
```

### Linting

```bash
# Format code
black src/ tests/

# Check types
mypy src/

# Lint
flake8 src/ tests/
```

## 📝 Commit Messages

Use conventional commits:

```
feat: add support for housing price index
fix: correct FREQ dimension handling for quarterly data
docs: update API reference with new examples
test: add unit tests for SDMXService
```

## 🔀 Pull Request Process

1. **Create PR** with descriptive title
2. **Link issue** if applicable (#123)
3. **Describe changes**:
   - What problem does this solve?
   - How did you test it?
4. **Update docs** if adding features
5. **Add tests** for new functionality
6. **Wait for review**

### PR Checklist

- [ ] Tests pass (`pytest`)
- [ ] Code formatted (`black .`)
- [ ] Types checked (`mypy src/`)
- [ ] Documentation updated
- [ ] Commit messages follow convention

## 🐛 Reporting Bugs

Create an issue with:

1. **Title**: Brief description
2. **Environment**: OS, Python version, package version
3. **Steps to Reproduce**:
   ```
   1. Run X
   2. Call Y
   3. See error
   ```
4. **Expected vs Actual**: What should happen vs what happens
5. **Logs**: Include relevant error messages/stack traces

## 💡 Suggesting Features

Create an issue with:

1. **Use Case**: What problem does this solve?
2. **Proposal**: How should it work?
3. **Examples**: Show example usage
4. **Alternatives**: Other approaches considered

## ❓ Questions

- **General questions**: [Discussions](https://github.com/yourusername/abs-mcp-server/discussions)
- **Bugs**: [Issues](https://github.com/yourusername/abs-mcp-server/issues)
- **PRs**: Comment on the PR

## 📜 Code of Conduct

- Be respectful and constructive
- Welcome newcomers
- Focus on what's best for the community

## 🏅 Recognition

Contributors will be:
- Listed in README (if significant contribution)
- Mentioned in release notes
- Appreciated! 🎉

Thank you for contributing!
