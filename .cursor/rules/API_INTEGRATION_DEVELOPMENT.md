# 🔌 API Integration Development Rules

## Cursor Role: API Integration Developer

You are a specialized API integration developer focused on creating robust, test-driven API integrations for the Streamlit Hello App. Follow these rules for all API-related development.

## 🎯 Core Principles

### 1. Test-Driven Development (TDD)
- **ALWAYS write tests first** before implementing any API functionality
- **Mock external API calls** to avoid dependencies and rate limits
- **Test all error scenarios** including network failures, timeouts, and API errors
- **Achieve >90% test coverage** for all API-related code

### 2. Error Handling First
- **Handle all possible error states** before implementing success paths
- **Provide user-friendly error messages** for all failure scenarios
- **Implement retry logic** for transient failures
- **Log detailed errors** for debugging while showing clean messages to users

### 3. Security by Design
- **Never log sensitive data** (API keys, tokens, personal information)
- **Validate all inputs** before making API calls
- **Use secure storage** for credentials and sensitive data
- **Implement rate limiting** to respect API quotas

## 🏗️ API Integration Patterns

### 1. Service Layer Pattern
```python
class ApiService:
    """Base class for API services."""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        self.base_url = "https://api.example.com"
        self._session = requests.Session()
        self._session.headers.update({
            'User-Agent': 'Streamlit-Hello-App/1.0',
            'Accept': 'application/json'
        })
    
    def _make_request(self, endpoint: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """Make API request with comprehensive error handling."""
        try:
            response = self._session.get(
                f"{self.base_url}{endpoint}",
                params=params,
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.Timeout:
            raise ApiTimeoutError("Request timed out")
        except requests.exceptions.ConnectionError:
            raise ApiConnectionError("Connection failed")
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 401:
                raise ApiAuthenticationError("Invalid API key")
            elif e.response.status_code == 429:
                raise ApiRateLimitError("Rate limit exceeded")
            else:
                raise ApiError(f"HTTP error: {e.response.status_code}")
        except requests.exceptions.RequestException as e:
            raise ApiError(f"Request failed: {str(e)}")
```

### 2. API Key Management Pattern
```python
def get_api_key(service_name: str) -> Optional[str]:
    """Get API key with environment variable and user input fallback."""
    # 1. Check environment variable
    env_var = f"{service_name.upper()}_API_KEY"
    api_key = os.getenv(env_var)
    if api_key:
        return api_key
    
    # 2. Prompt user for input
    try:
        import streamlit as st
        api_key = st.text_input(
            f"Enter your {service_name} API key:",
            type="password",
            help=f"Get your API key from {service_name} settings"
        )
        return api_key if api_key else None
    except ImportError:
        return None

def validate_api_key(api_key: Optional[str], validation_endpoint: str) -> str:
    """Validate API key with health check."""
    if not api_key:
        return "error"
    
    try:
        response = requests.get(
            validation_endpoint,
            params={"api_key": api_key},
            timeout=10
        )
        
        if response.status_code == 200:
            return "valid"
        elif response.status_code == 401:
            return "invalid"
        else:
            return "error"
    except Exception:
        return "error"
```

### 3. Data Formatting Pattern
```python
def format_api_response(raw_data: Dict[str, Any]) -> Dict[str, Any]:
    """Format API response for consistent display."""
    return {
        'id': raw_data.get('id'),
        'title': raw_data.get('title', 'Unknown Title'),
        'description': _format_description(raw_data.get('description', '')),
        'image_url': _get_image_url(raw_data.get('image_path')),
        'metadata': _extract_metadata(raw_data),
        'formatted_date': _format_date(raw_data.get('date')),
        'rating': _format_rating(raw_data.get('rating', 0))
    }

def _format_description(description: str) -> str:
    """Format description with length limits."""
    if not description:
        return 'No description available'
    elif len(description) > 200:
        return description[:197] + '...'
    return description

def _get_image_url(image_path: Optional[str]) -> Optional[str]:
    """Get full image URL from path."""
    if not image_path:
        return None
    return f"https://image.example.com/w500{image_path}"
```

## 🧪 Testing Patterns for API Integrations

### 1. API Service Testing
```python
class TestApiService:
    """Test cases for API service."""
    
    @patch('requests.Session.get')
    def test_successful_api_call(self, mock_get):
        """Test successful API call."""
        # Arrange
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "success": True,
            "data": [{"id": 1, "title": "Test Item"}]
        }
        mock_get.return_value = mock_response
        
        # Act
        service = ApiService('test_key')
        result = service.get_data()
        
        # Assert
        assert result['success'] is True
        assert len(result['data']) == 1
        assert result['data'][0]['title'] == 'Test Item'
        mock_get.assert_called_once()
    
    @patch('requests.Session.get')
    def test_api_authentication_error(self, mock_get):
        """Test API authentication error."""
        # Arrange
        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_response.raise_for_status.side_effect = HTTPError("401 Client Error")
        mock_get.return_value = mock_response
        
        # Act & Assert
        service = ApiService('invalid_key')
        with pytest.raises(ApiAuthenticationError):
            service.get_data()
    
    @patch('requests.Session.get')
    def test_api_rate_limit_error(self, mock_get):
        """Test API rate limit error."""
        # Arrange
        mock_response = MagicMock()
        mock_response.status_code = 429
        mock_response.raise_for_status.side_effect = HTTPError("429 Too Many Requests")
        mock_get.return_value = mock_response
        
        # Act & Assert
        service = ApiService('test_key')
        with pytest.raises(ApiRateLimitError):
            service.get_data()
    
    @patch('requests.Session.get')
    def test_api_connection_error(self, mock_get):
        """Test API connection error."""
        # Arrange
        mock_get.side_effect = ConnectionError("Connection failed")
        
        # Act & Assert
        service = ApiService('test_key')
        with pytest.raises(ApiConnectionError):
            service.get_data()
    
    @patch('requests.Session.get')
    def test_api_timeout_error(self, mock_get):
        """Test API timeout error."""
        # Arrange
        mock_get.side_effect = Timeout("Request timed out")
        
        # Act & Assert
        service = ApiService('test_key')
        with pytest.raises(ApiTimeoutError):
            service.get_data()
```

### 2. API Key Management Testing
```python
class TestApiKeyManagement:
    """Test cases for API key management."""
    
    @patch.dict(os.environ, {'TEST_API_KEY': 'test_key_123'})
    def test_get_api_key_from_environment(self):
        """Test getting API key from environment variable."""
        api_key = get_api_key('test')
        assert api_key == 'test_key_123'
    
    @patch.dict(os.environ, {}, clear=True)
    def test_get_api_key_no_environment(self):
        """Test getting API key when not in environment."""
        api_key = get_api_key('test')
        assert api_key is None
    
    @patch('requests.get')
    def test_validate_api_key_success(self, mock_get):
        """Test successful API key validation."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        
        result = validate_api_key('valid_key', 'https://api.test.com/validate')
        assert result == 'valid'
    
    @patch('requests.get')
    def test_validate_api_key_invalid(self, mock_get):
        """Test invalid API key validation."""
        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_get.return_value = mock_response
        
        result = validate_api_key('invalid_key', 'https://api.test.com/validate')
        assert result == 'invalid'
```

### 3. UI Integration Testing
```python
class TestApiIntegrationUI:
    """Test cases for API integration UI."""
    
    @patch('streamlit_hello_app.modules.api_page.get_api_key')
    @patch('streamlit_hello_app.modules.api_page.validate_api_key')
    def test_render_page_with_valid_api_key(self, mock_validate, mock_get_key):
        """Test page rendering with valid API key."""
        # Arrange
        mock_get_key.return_value = 'valid_key'
        mock_validate.return_value = 'valid'
        
        # Act
        render_api_page()
        
        # Assert
        mock_get_key.assert_called_once()
        mock_validate.assert_called_once_with('valid_key')
    
    @patch('streamlit_hello_app.modules.api_page.get_api_key')
    @patch('streamlit_hello_app.modules.api_page.validate_api_key')
    def test_render_page_with_invalid_api_key(self, mock_validate, mock_get_key):
        """Test page rendering with invalid API key."""
        # Arrange
        mock_get_key.return_value = 'invalid_key'
        mock_validate.return_value = 'invalid'
        
        # Act
        render_api_page()
        
        # Assert
        mock_validate.assert_called_once_with('invalid_key')
```

## 🔧 Implementation Guidelines

### 1. Error Handling Implementation
```python
class ApiError(Exception):
    """Base exception for API errors."""
    pass

class ApiAuthenticationError(ApiError):
    """API authentication error."""
    pass

class ApiRateLimitError(ApiError):
    """API rate limit error."""
    pass

class ApiConnectionError(ApiError):
    """API connection error."""
    pass

class ApiTimeoutError(ApiError):
    """API timeout error."""
    pass

def handle_api_error(error: Exception) -> str:
    """Convert API errors to user-friendly messages."""
    if isinstance(error, ApiAuthenticationError):
        return "❌ Invalid API key. Please check your credentials."
    elif isinstance(error, ApiRateLimitError):
        return "❌ Rate limit exceeded. Please try again later."
    elif isinstance(error, ApiConnectionError):
        return "❌ Connection failed. Please check your internet connection."
    elif isinstance(error, ApiTimeoutError):
        return "❌ Request timed out. Please try again."
    else:
        return "❌ An unexpected error occurred. Please try again."
```

### 2. Retry Logic Implementation
```python
import time
from functools import wraps

def retry_on_failure(max_retries: int = 3, delay: float = 1.0):
    """Decorator for retrying API calls on failure."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except (ApiConnectionError, ApiTimeoutError) as e:
                    last_exception = e
                    if attempt < max_retries - 1:
                        time.sleep(delay * (2 ** attempt))  # Exponential backoff
                        continue
                    break
                except Exception as e:
                    # Don't retry on authentication or rate limit errors
                    raise e
            
            raise last_exception
        return wrapper
    return decorator

@retry_on_failure(max_retries=3, delay=1.0)
def make_api_call(self, endpoint: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
    """Make API call with retry logic."""
    return self._make_request(endpoint, params)
```

### 3. Caching Implementation
```python
from functools import lru_cache
import time

class CachedApiService:
    """API service with caching."""
    
    def __init__(self, api_key: str, cache_ttl: int = 300):
        self.api_key = api_key
        self.cache_ttl = cache_ttl
        self._cache = {}
    
    def _get_cached_data(self, key: str) -> Optional[Dict[str, Any]]:
        """Get cached data if not expired."""
        if key in self._cache:
            data, timestamp = self._cache[key]
            if time.time() - timestamp < self.cache_ttl:
                return data
            else:
                del self._cache[key]
        return None
    
    def _set_cached_data(self, key: str, data: Dict[str, Any]) -> None:
        """Set cached data with timestamp."""
        self._cache[key] = (data, time.time())
    
    def get_data(self, query: str) -> Dict[str, Any]:
        """Get data with caching."""
        cache_key = f"data_{query}"
        cached_data = self._get_cached_data(cache_key)
        
        if cached_data:
            return cached_data
        
        # Make API call
        data = self._make_api_call(query)
        self._set_cached_data(cache_key, data)
        return data
```

## 🎨 UI/UX Guidelines for API Integrations

### 1. Loading States
```python
def render_api_page():
    """Render API page with loading states."""
    # Show loading spinner during API calls
    with st.spinner("Loading data..."):
        try:
            data = api_service.get_data()
            display_results(data)
        except ApiError as e:
            st.error(handle_api_error(e))
```

### 2. Error Messages
```python
def display_api_error(error: Exception):
    """Display user-friendly error messages."""
    if isinstance(error, ApiAuthenticationError):
        st.error("❌ Invalid API key. Please check your credentials.")
        st.info("Get your API key from [API Settings](https://api.example.com/settings)")
    elif isinstance(error, ApiRateLimitError):
        st.error("❌ Rate limit exceeded. Please try again later.")
        st.info("You can make up to 100 requests per hour.")
    elif isinstance(error, ApiConnectionError):
        st.error("❌ Connection failed. Please check your internet connection.")
    else:
        st.error("❌ An unexpected error occurred. Please try again.")
```

### 3. User Guidance
```python
def render_api_key_input():
    """Render API key input with guidance."""
    st.markdown("### API Key Setup")
    
    api_key = st.text_input(
        "Enter your API key:",
        type="password",
        help="Get your API key from the API provider's settings page"
    )
    
    if st.button("Validate API Key"):
        with st.spinner("Validating API key..."):
            validation_result = validate_api_key(api_key)
            
            if validation_result == "valid":
                st.success("✅ API key is valid!")
            elif validation_result == "invalid":
                st.error("❌ Invalid API key. Please check your credentials.")
            else:
                st.error("❌ Error validating API key. Please try again.")
```

## 📊 Performance Guidelines

### 1. Request Optimization
```python
class OptimizedApiService:
    """API service with request optimization."""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self._session = requests.Session()
        self._session.headers.update({
            'Authorization': f'Bearer {api_key}',
            'Accept': 'application/json',
            'User-Agent': 'Streamlit-Hello-App/1.0'
        })
    
    def batch_requests(self, requests: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Batch multiple requests for efficiency."""
        # Implement request batching if API supports it
        pass
    
    def paginate_results(self, endpoint: str, params: Dict[str, Any]) -> Iterator[Dict[str, Any]]:
        """Paginate through large result sets."""
        page = 1
        while True:
            params['page'] = page
            response = self._make_request(endpoint, params)
            
            if not response.get('results'):
                break
            
            for item in response['results']:
                yield item
            
            if page >= response.get('total_pages', 1):
                break
            
            page += 1
```

### 2. Rate Limiting
```python
import time
from collections import deque

class RateLimitedApiService:
    """API service with rate limiting."""
    
    def __init__(self, api_key: str, requests_per_minute: int = 60):
        self.api_key = api_key
        self.requests_per_minute = requests_per_minute
        self.request_times = deque()
    
    def _wait_for_rate_limit(self):
        """Wait if rate limit would be exceeded."""
        now = time.time()
        
        # Remove requests older than 1 minute
        while self.request_times and self.request_times[0] <= now - 60:
            self.request_times.popleft()
        
        # Wait if we're at the rate limit
        if len(self.request_times) >= self.requests_per_minute:
            sleep_time = 60 - (now - self.request_times[0])
            if sleep_time > 0:
                time.sleep(sleep_time)
        
        self.request_times.append(now)
    
    def make_request(self, endpoint: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """Make request with rate limiting."""
        self._wait_for_rate_limit()
        return self._make_request(endpoint, params)
```

## 🔒 Security Guidelines

### 1. Credential Management
```python
def secure_api_key_storage():
    """Secure API key storage and retrieval."""
    # Never log API keys
    # Use environment variables for production
    # Use secure input types in UI
    # Implement key rotation if needed
    pass

def sanitize_user_input(user_input: str) -> str:
    """Sanitize user input before API calls."""
    # Remove potentially harmful characters
    # Validate input format
    # Escape special characters
    return user_input.strip()
```

### 2. Data Protection
```python
def protect_sensitive_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """Remove sensitive data from responses."""
    sensitive_keys = ['password', 'token', 'secret', 'key']
    
    for key in sensitive_keys:
        if key in data:
            data[key] = '***REDACTED***'
    
    return data
```

## 🚀 Deployment Guidelines

### 1. Environment Configuration
```bash
# Required environment variables
API_KEY=your_api_key_here
API_BASE_URL=https://api.example.com
API_TIMEOUT=10
API_RETRY_COUNT=3
```

### 2. Configuration Management
```python
class ApiConfig:
    """API configuration management."""
    
    def __init__(self):
        self.api_key = os.getenv('API_KEY')
        self.base_url = os.getenv('API_BASE_URL', 'https://api.example.com')
        self.timeout = int(os.getenv('API_TIMEOUT', '10'))
        self.retry_count = int(os.getenv('API_RETRY_COUNT', '3'))
    
    def validate(self) -> bool:
        """Validate configuration."""
        if not self.api_key:
            raise ValueError("API_KEY environment variable is required")
        return True
```

## 📝 Documentation Standards

### 1. API Documentation
```python
def get_data(self, query: str, page: int = 1) -> Dict[str, Any]:
    """
    Get data from API with pagination.
    
    Args:
        query: Search query string
        page: Page number for pagination (default: 1)
        
    Returns:
        Dictionary containing API response data
        
    Raises:
        ApiAuthenticationError: If API key is invalid
        ApiRateLimitError: If rate limit is exceeded
        ApiConnectionError: If connection fails
        ApiTimeoutError: If request times out
        
    Example:
        >>> service = ApiService('your_api_key')
        >>> results = service.get_data('search query')
        >>> print(results['data'])
    """
```

### 2. Test Documentation
```python
def test_api_authentication_error(self):
    """
    Test API authentication error handling.
    
    This test verifies that:
    - Invalid API keys are properly detected
    - Appropriate error is raised
    - Error message is user-friendly
    """
```

## 🎯 Success Metrics

### 1. Test Coverage
- **Target**: >90% coverage for API-related code
- **Measurement**: `pytest --cov=src/streamlit_hello_app/modules/api_*`

### 2. Error Handling
- **Target**: Handle all possible error states
- **Measurement**: Test coverage of error scenarios

### 3. Performance
- **Target**: <2s response time for API calls
- **Measurement**: Response time monitoring

### 4. User Experience
- **Target**: Clear error messages and loading states
- **Measurement**: User feedback and testing

## 🚨 Common Pitfalls to Avoid

### 1. Testing
- ❌ Don't make real API calls in tests
- ❌ Don't skip error case testing
- ❌ Don't test implementation details

### 2. Error Handling
- ❌ Don't expose sensitive error information
- ❌ Don't skip network error handling
- ❌ Don't assume API responses are valid

### 3. Security
- ❌ Don't log API keys or sensitive data
- ❌ Don't hardcode credentials
- ❌ Don't skip input validation

### 4. Performance
- ❌ Don't ignore rate limits
- ❌ Don't skip caching opportunities
- ❌ Don't make unnecessary API calls

---

**Remember**: API integrations are critical for user experience. Always test thoroughly, handle errors gracefully, and prioritize security and performance.
