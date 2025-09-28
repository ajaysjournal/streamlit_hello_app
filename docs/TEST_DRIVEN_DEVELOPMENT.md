# 🧪 Test-Driven Development (TDD) Guidelines

## Overview

This document outlines the test-driven development approach used in the Streamlit Hello App, with specific focus on API integrations like TMDB movie search.

## 🎯 TDD Principles

### 1. Red-Green-Refactor Cycle

#### Red Phase
- Write a failing test first
- Test should fail for the right reason
- Don't write any implementation code yet

#### Green Phase
- Write minimal code to make the test pass
- Don't worry about code quality yet
- Focus on making the test pass

#### Refactor Phase
- Improve code quality while keeping tests green
- Remove duplication
- Improve readability and performance

### 2. Test-First Development

```python
# 1. Write test first (RED)
def test_search_movies_success():
    """Test successful movie search."""
    service = TmdbService('test_api_key')
    results = service.search_movies('Inception')
    
    assert results['success'] is True
    assert len(results['movies']) > 0
    assert results['movies'][0]['title'] == 'Inception'

# 2. Run test (should fail)
# 3. Write minimal implementation (GREEN)
def search_movies(self, query: str):
    return {
        'success': True,
        'movies': [{'title': 'Inception'}]
    }

# 4. Refactor while keeping tests green
```

## 🏗️ Test Architecture

### Test Categories

#### 1. Unit Tests
- Test individual functions/methods
- Mock external dependencies
- Fast execution
- High coverage

#### 2. Integration Tests
- Test component interactions
- Test API integrations
- Mock external APIs
- Test data flow

#### 3. UI Tests
- Test Streamlit components
- Mock user interactions
- Test error states
- Test user experience

### Test File Structure

```
tests/
├── test_tmdb_utils.py          # API key management
├── test_tmdb_service.py        # TMDB service layer
├── test_movie_search.py        # UI components
├── test_config.py              # Configuration
└── test_utils.py               # Utility functions
```

## 🧪 Testing Patterns

### 1. API Testing Pattern

```python
class TestTmdbService:
    """Test cases for TMDB service."""
    
    @patch('streamlit_hello_app.modules.tmdb_service.requests.get')
    def test_search_movies_success(self, mock_get):
        """Test successful movie search."""
        # Arrange
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "page": 1,
            "results": [{"id": 123, "title": "Test Movie"}],
            "total_pages": 1,
            "total_results": 1
        }
        mock_get.return_value = mock_response
        
        # Act
        service = TmdbService('test_api_key')
        results = service.search_movies('Test Movie')
        
        # Assert
        assert results['success'] is True
        assert len(results['movies']) == 1
        assert results['movies'][0]['title'] == 'Test Movie'
        mock_get.assert_called_once()
    
    @patch('streamlit_hello_app.modules.tmdb_service.requests.get')
    def test_search_movies_api_error(self, mock_get):
        """Test API error handling."""
        # Arrange
        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_response.json.return_value = {
            "success": False,
            "status_code": 7,
            "status_message": "Invalid API key"
        }
        mock_get.return_value = mock_response
        
        # Act
        service = TmdbService('invalid_key')
        results = service.search_movies('Test Movie')
        
        # Assert
        assert results['success'] is False
        assert 'Invalid API key' in results['error']
```

### 2. UI Testing Pattern

```python
class TestMovieSearchPage:
    """Test cases for movie search page."""
    
    @patch('streamlit_hello_app.modules.movie_search.get_tmdb_api_key')
    @patch('streamlit_hello_app.modules.movie_search.validate_tmdb_api_key')
    def test_render_movie_search_with_valid_api_key(self, mock_validate, mock_get_key):
        """Test page rendering with valid API key."""
        # Arrange
        mock_get_key.return_value = 'valid_api_key'
        mock_validate.return_value = 'valid'
        
        # Act
        render_movie_search()
        
        # Assert
        mock_get_key.assert_called_once()
        mock_validate.assert_called_once_with('valid_api_key')
```

### 3. Error Handling Testing Pattern

```python
class TestErrorHandling:
    """Test error handling scenarios."""
    
    def test_validate_api_key_connection_error(self):
        """Test validation with connection error."""
        # Arrange
        with patch('streamlit_hello_app.utils.requests.get') as mock_get:
            mock_get.side_effect = ConnectionError("Connection failed")
            
            # Act
            result = validate_tmdb_api_key('test_key')
            
            # Assert
            assert result == TMDB_API_KEY_ERROR
    
    def test_search_movies_timeout(self):
        """Test search with timeout error."""
        # Arrange
        with patch('streamlit_hello_app.modules.tmdb_service.requests.get') as mock_get:
            mock_get.side_effect = Timeout("Request timed out")
            
            # Act
            service = TmdbService('test_api_key')
            results = service.search_movies('Test Movie')
            
            # Assert
            assert results['success'] is False
            assert 'Request timed out' in results['error']
```

## 🔧 Mocking Strategies

### 1. API Mocking

```python
# Mock HTTP requests
@patch('streamlit_hello_app.modules.tmdb_service.requests.get')
def test_api_call(self, mock_get):
    """Test API call with mocked response."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"success": True}
    mock_get.return_value = mock_response
    
    # Test implementation
```

### 2. Streamlit Mocking

```python
# Mock Streamlit components
@patch('streamlit_hello_app.modules.movie_search.st.text_input')
@patch('streamlit_hello_app.modules.movie_search.st.button')
def test_user_input(self, mock_button, mock_text_input):
    """Test user input handling."""
    mock_text_input.return_value = 'user_input'
    mock_button.return_value = True
    
    # Test implementation
```

### 3. Environment Mocking

```python
# Mock environment variables
@patch.dict(os.environ, {'TMDB_API_KEY': 'test_key'})
def test_environment_variable(self):
    """Test environment variable handling."""
    api_key = get_tmdb_api_key()
    assert api_key == 'test_key'
```

## 📊 Test Coverage

### Coverage Targets

- **Unit Tests**: >95% coverage
- **Integration Tests**: >90% coverage
- **UI Tests**: >80% coverage
- **Overall**: >90% coverage

### Coverage Measurement

```bash
# Run coverage analysis
pytest --cov=src/streamlit_hello_app --cov-report=html --cov-report=term

# Run specific module coverage
pytest --cov=src/streamlit_hello_app/modules/tmdb_service.py --cov-report=html
```

### Coverage Reports

```bash
# Generate HTML coverage report
pytest --cov=src/streamlit_hello_app --cov-report=html
open htmlcov/index.html
```

## 🚀 TDD Workflow

### 1. Feature Development

```bash
# 1. Write failing test
def test_new_feature():
    assert new_feature() == expected_result

# 2. Run test (should fail)
pytest tests/test_new_feature.py::test_new_feature -v

# 3. Write minimal implementation
def new_feature():
    return expected_result

# 4. Run test (should pass)
pytest tests/test_new_feature.py::test_new_feature -v

# 5. Refactor while keeping tests green
# 6. Add more test cases
# 7. Repeat cycle
```

### 2. Bug Fixing

```bash
# 1. Write test that reproduces bug
def test_bug_reproduction():
    result = buggy_function()
    assert result == expected_result  # This will fail

# 2. Fix the bug
def buggy_function():
    return expected_result  # Fixed

# 3. Run test (should pass)
pytest tests/test_bug_fix.py::test_bug_reproduction -v
```

### 3. Refactoring

```bash
# 1. Ensure all tests pass
pytest tests/ -v

# 2. Refactor code
# 3. Run tests again
pytest tests/ -v

# 4. If tests fail, fix implementation
# 5. Repeat until all tests pass
```

## 🎯 Test Quality Guidelines

### 1. Test Naming

```python
# Good test names
def test_search_movies_success():
    """Test successful movie search with valid API key."""

def test_search_movies_invalid_api_key():
    """Test movie search with invalid API key."""

def test_search_movies_connection_error():
    """Test movie search with connection error."""

# Bad test names
def test1():
def test_search():
def test_movies():
```

### 2. Test Structure

```python
def test_feature_scenario():
    """Test description of what is being tested."""
    # Arrange - Set up test data and mocks
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"success": True}
    
    # Act - Execute the code under test
    result = function_under_test()
    
    # Assert - Verify the results
    assert result['success'] is True
    assert result['data'] == expected_data
```

### 3. Test Documentation

```python
def test_search_movies_success(self):
    """
    Test successful movie search with valid API key.
    
    This test verifies that:
    - API call is made with correct parameters
    - Response is parsed correctly
    - Movie data is formatted properly
    - Success status is returned
    """
    # Test implementation
```

## 🔍 Test Debugging

### 1. Verbose Output

```bash
# Run tests with verbose output
pytest tests/test_tmdb_service.py -v -s

# Run specific test with debug output
pytest tests/test_tmdb_service.py::TestTmdbService::test_search_movies_success -v -s
```

### 2. Test Isolation

```python
# Use fixtures for test isolation
@pytest.fixture
def mock_tmdb_service():
    """Create mock TMDB service for testing."""
    with patch('streamlit_hello_app.modules.tmdb_service.requests.get') as mock_get:
        yield mock_get

def test_with_fixture(mock_tmdb_service):
    """Test using fixture."""
    mock_tmdb_service.return_value.status_code = 200
    # Test implementation
```

### 3. Test Data

```python
# Use test data fixtures
@pytest.fixture
def sample_movie_data():
    """Sample movie data for testing."""
    return {
        "id": 12345,
        "title": "Test Movie",
        "overview": "A test movie",
        "poster_path": "/test_poster.jpg",
        "release_date": "2024-01-01",
        "vote_average": 8.5,
        "vote_count": 1000
    }

def test_with_sample_data(sample_movie_data):
    """Test using sample data."""
    result = format_movie_data(sample_movie_data)
    assert result['title'] == 'Test Movie'
```

## 📈 Continuous Integration

### 1. Automated Testing

```yaml
# .github/workflows/test.yml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.11
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run tests
        run: pytest tests/ -v --cov=src/streamlit_hello_app
```

### 2. Test Automation

```bash
# Run all tests
pytest tests/ -v

# Run specific test categories
pytest tests/test_tmdb_*.py -v
pytest tests/test_movie_search.py -v

# Run with coverage
pytest tests/ --cov=src/streamlit_hello_app --cov-report=html
```

### 3. Quality Gates

```bash
# Ensure all tests pass
pytest tests/ -v

# Ensure coverage threshold
pytest tests/ --cov=src/streamlit_hello_app --cov-fail-under=90

# Ensure no linting errors
flake8 src/streamlit_hello_app/
black --check src/streamlit_hello_app/
```

## 🎯 Best Practices

### 1. Test Independence

- Each test should be independent
- Tests should not depend on each other
- Use setup/teardown for test isolation

### 2. Test Clarity

- Tests should be easy to understand
- Use descriptive test names
- Include helpful assertions

### 3. Test Maintenance

- Keep tests up to date with code changes
- Refactor tests when refactoring code
- Remove obsolete tests

### 4. Test Performance

- Keep tests fast
- Use mocks for external dependencies
- Avoid slow operations in tests

## 🚨 Common Pitfalls

### 1. Testing Implementation Details

```python
# Bad - testing implementation details
def test_internal_method():
    service = TmdbService('key')
    assert service._get_configuration() is not None

# Good - testing behavior
def test_search_movies():
    service = TmdbService('key')
    results = service.search_movies('Inception')
    assert results['success'] is True
```

### 2. Over-Mocking

```python
# Bad - over-mocking
@patch('streamlit_hello_app.modules.tmdb_service.requests.get')
@patch('streamlit_hello_app.modules.tmdb_service.TmdbService._get_configuration')
@patch('streamlit_hello_app.modules.tmdb_service.TmdbService._format_movie_data')
def test_search_movies(self, mock_format, mock_config, mock_get):
    # Too many mocks

# Good - minimal mocking
@patch('streamlit_hello_app.modules.tmdb_service.requests.get')
def test_search_movies(self, mock_get):
    # Only mock external dependencies
```

### 3. Ignoring Edge Cases

```python
# Bad - only testing happy path
def test_search_movies_success():
    # Only test success case

# Good - testing edge cases
def test_search_movies_success():
    # Test success case

def test_search_movies_empty_query():
    # Test empty query

def test_search_movies_network_error():
    # Test network error

def test_search_movies_invalid_api_key():
    # Test invalid API key
```

## 📚 Resources

### Testing Libraries

- [pytest](https://docs.pytest.org/) - Testing framework
- [unittest.mock](https://docs.python.org/3/library/unittest.mock.html) - Mocking library
- [coverage.py](https://coverage.readthedocs.io/) - Coverage measurement

### TDD Resources

- [Test-Driven Development by Example](https://www.amazon.com/Test-Driven-Development-Kent-Beck/dp/0321146530)
- [Growing Object-Oriented Software, Guided by Tests](https://www.amazon.com/Growing-Object-Oriented-Software-Guided-Tests/dp/0321503627)
- [Clean Code](https://www.amazon.com/Clean-Code-Handbook-Software-Craftsmanship/dp/0132350882)

### Streamlit Testing

- [Streamlit Testing Guide](https://docs.streamlit.io/library/advanced-features/testing)
- [Streamlit Testing Examples](https://github.com/streamlit/streamlit/tree/develop/tests)

---

**Remember**: Tests are not just for catching bugs - they're for documenting behavior, enabling refactoring, and building confidence in your code. Write tests first, keep them simple, and maintain them well.
