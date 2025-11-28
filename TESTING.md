# Testing Guide for AI Story Point Estimator

## Overview
This project uses **pytest** for automated testing with coverage reporting. Tests are automatically run on every push and pull request via GitHub Actions.

## Test Structure

```
story_point_estimator/
├── tests/
│   ├── __init__.py
│   ├── test_estimator.py       # Unit tests for core logic
│   └── test_app_integration.py # Integration tests for Streamlit app
├── pyproject.toml              # Pytest configuration
└── .github/workflows/tests.yml # CI/CD automation
```

## Running Tests Locally

### 1. Install Test Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run All Tests
```bash
pytest
```

### 3. Run with Coverage Report
```bash
pytest --cov=. --cov-report=html --cov-report=term-missing
```

This generates:
- Terminal output showing coverage percentages
- HTML report in `htmlcov/index.html` (open in browser)

### 4. Run Specific Test Files
```bash
pytest tests/test_estimator.py
pytest tests/test_app_integration.py
```

### 5. Run Specific Test Classes or Functions
```bash
pytest tests/test_estimator.py::TestValidateAndCleanDF
pytest tests/test_estimator.py::TestSanitizeText::test_prompt_injection_removal
```

## Coverage Requirements

- **Minimum Coverage**: 70% (enforced in CI/CD)
- **Target Coverage**: 80%+
- Coverage reports exclude:
  - Test files themselves
  - Virtual environments
  - `__pycache__` directories

## Test Categories

### Unit Tests (`test_estimator.py`)
Tests individual functions in isolation:
- ✅ Data validation and cleaning
- ✅ Text sanitization and security
- ✅ CSV file loading
- ✅ Prompt construction
- ✅ Fibonacci mapping

### Integration Tests (`test_app_integration.py`)
Tests complete workflows:
- ✅ End-to-end estimation flow
- ✅ CSV data processing
- ✅ API integration (mocked)
- ✅ Error handling

## Continuous Integration (GitHub Actions)

Tests run automatically on:
- Push to `main` or `develop` branches
- Pull requests to `main` or `develop`

### CI Pipeline:
1. **Matrix Testing**: Tests run on Python 3.9, 3.10, and 3.11
2. **Coverage Calculation**: Generates coverage reports
3. **Codecov Upload**: Uploads coverage to Codecov.io (optional)
4. **Threshold Check**: Fails if coverage < 70%
5. **Artifact Storage**: Saves HTML coverage reports

## Viewing CI Results

1. Go to your GitHub repository
2. Click **Actions** tab
3. Select a workflow run to see:
   - Test results for each Python version
   - Coverage percentages
   - Downloadable coverage reports

## Adding New Tests

### For New Functions:
1. Add test class to `tests/test_estimator.py`
2. Follow naming convention: `TestFunctionName`
3. Write test methods: `test_specific_behavior`

Example:
```python
class TestNewFunction:
    def test_normal_case(self):
        result = new_function("input")
        assert result == "expected"
    
    def test_edge_case(self):
        result = new_function("")
        assert result is None
```

### For Integration Tests:
1. Add to `tests/test_app_integration.py`
2. Use mocking for external dependencies (API calls, file I/O)
3. Test complete user workflows

## Best Practices

1. **Test Naming**: Use descriptive names that explain what's being tested
2. **Arrange-Act-Assert**: Structure tests clearly
3. **Mock External Calls**: Don't make real API calls in tests
4. **Test Edge Cases**: Empty inputs, invalid data, boundary conditions
5. **Keep Tests Fast**: Unit tests should run in milliseconds
6. **Independent Tests**: Each test should be able to run alone

## Coverage Badges

Add to your README.md:
```markdown
[![codecov](https://codecov.io/gh/USERNAME/REPO/branch/main/graph/badge.svg)](https://codecov.io/gh/USERNAME/REPO)
```

## Troubleshooting

### Tests Not Found
```bash
# Make sure you're in the project root
cd /path/to/story_point_estimator
pytest
```

### Import Errors
```bash
# Install in development mode
pip install -e .
```

### Coverage Not Updating
```bash
# Clear cache and rerun
pytest --cache-clear --cov=. --cov-report=html
```

## Next Steps

- [ ] Add tests for edge cases discovered in production
- [ ] Increase coverage to 80%+
- [ ] Add performance benchmarks
- [ ] Set up mutation testing (optional)
