"""Tests for TMDB service functions."""

import pytest
from unittest.mock import patch, MagicMock
from requests.exceptions import RequestException, ConnectionError, Timeout

from streamlit_hello_app.modules.tmdb_service import (
    TmdbService,
    TMDB_BASE_URL,
    TMDB_SEARCH_ENDPOINT,
    TMDB_CONFIG_ENDPOINT
)


class TestTmdbService:
    """Test cases for TmdbService class."""
    
    def test_init_with_api_key(self):
        """Test TmdbService initialization with API key."""
        service = TmdbService('test_api_key_123')
        assert service.api_key == 'test_api_key_123'
        assert service.base_url == TMDB_BASE_URL
    
    def test_init_without_api_key(self):
        """Test TmdbService initialization without API key."""
        service = TmdbService()
        assert service.api_key is None
        assert service.base_url == TMDB_BASE_URL
    
    @patch('streamlit_hello_app.modules.tmdb_service.requests.get')
    def test_search_movies_success(self, mock_get):
        """Test successful movie search."""
        # Mock successful search response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "page": 1,
            "results": [
                {
                    "id": 12345,
                    "title": "Test Movie",
                    "overview": "A test movie description",
                    "poster_path": "/test_poster.jpg",
                    "release_date": "2024-01-01",
                    "vote_average": 8.5,
                    "vote_count": 1000
                }
            ],
            "total_pages": 1,
            "total_results": 1
        }
        mock_get.return_value = mock_response
        
        service = TmdbService('test_api_key')
        results = service.search_movies('Test Movie')
        
        assert results['success'] is True
        assert len(results['movies']) == 1
        assert results['movies'][0]['title'] == 'Test Movie'
        assert results['total_pages'] == 1
        assert results['total_results'] == 1
        
        # Verify API calls were made correctly (search + config)
        assert mock_get.call_count == 2  # Search call + config call
        
        # Check search call
        search_call = mock_get.call_args_list[0]
        expected_url = f"{TMDB_BASE_URL}{TMDB_SEARCH_ENDPOINT}"
        assert expected_url in search_call[0][0]
        assert search_call[1]['params']['api_key'] == 'test_api_key'
        assert search_call[1]['params']['query'] == 'Test Movie'
    
    @patch('streamlit_hello_app.modules.tmdb_service.requests.get')
    def test_search_movies_with_pagination(self, mock_get):
        """Test movie search with pagination."""
        # Mock response with multiple pages
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "page": 2,
            "results": [
                {
                    "id": 12346,
                    "title": "Test Movie 2",
                    "overview": "Another test movie",
                    "poster_path": "/test_poster2.jpg",
                    "release_date": "2024-02-01",
                    "vote_average": 7.5,
                    "vote_count": 500
                }
            ],
            "total_pages": 3,
            "total_results": 50
        }
        mock_get.return_value = mock_response
        
        service = TmdbService('test_api_key')
        results = service.search_movies('Test Movie', page=2)
        
        assert results['success'] is True
        assert results['current_page'] == 2
        assert results['total_pages'] == 3
        assert results['total_results'] == 50
        assert len(results['movies']) == 1
        
        # Verify page parameter was passed in search call
        search_call = mock_get.call_args_list[0]
        assert search_call[1]['params']['page'] == 2
    
    @patch('streamlit_hello_app.modules.tmdb_service.requests.get')
    def test_search_movies_no_results(self, mock_get):
        """Test movie search with no results."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "page": 1,
            "results": [],
            "total_pages": 0,
            "total_results": 0
        }
        mock_get.return_value = mock_response
        
        service = TmdbService('test_api_key')
        results = service.search_movies('Nonexistent Movie')
        
        assert results['success'] is True
        assert len(results['movies']) == 0
        assert results['total_results'] == 0
    
    @patch('streamlit_hello_app.modules.tmdb_service.requests.get')
    def test_search_movies_api_error(self, mock_get):
        """Test movie search with API error."""
        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_response.json.return_value = {
            "success": False,
            "status_code": 7,
            "status_message": "Invalid API key"
        }
        mock_get.return_value = mock_response
        
        service = TmdbService('invalid_key')
        results = service.search_movies('Test Movie')
        
        assert results['success'] is False
        assert 'error' in results
        assert 'Invalid API key' in results['error']
    
    @patch('streamlit_hello_app.modules.tmdb_service.requests.get')
    def test_search_movies_connection_error(self, mock_get):
        """Test movie search with connection error."""
        mock_get.side_effect = ConnectionError("Connection failed")
        
        service = TmdbService('test_api_key')
        results = service.search_movies('Test Movie')
        
        assert results['success'] is False
        assert 'error' in results
        assert 'Connection failed' in results['error']
    
    @patch('streamlit_hello_app.modules.tmdb_service.requests.get')
    def test_search_movies_timeout(self, mock_get):
        """Test movie search with timeout."""
        mock_get.side_effect = Timeout("Request timed out")
        
        service = TmdbService('test_api_key')
        results = service.search_movies('Test Movie')
        
        assert results['success'] is False
        assert 'error' in results
        assert 'Request timed out' in results['error']
    
    @patch('streamlit_hello_app.modules.tmdb_service.requests.get')
    def test_search_movies_request_exception(self, mock_get):
        """Test movie search with general request exception."""
        mock_get.side_effect = RequestException("Request failed")
        
        service = TmdbService('test_api_key')
        results = service.search_movies('Test Movie')
        
        assert results['success'] is False
        assert 'error' in results
        assert 'Request failed' in results['error']
    
    def test_search_movies_no_api_key(self):
        """Test movie search without API key."""
        service = TmdbService()
        results = service.search_movies('Test Movie')
        
        assert results['success'] is False
        assert 'error' in results
        assert 'API key is required' in results['error']
    
    def test_search_movies_empty_query(self):
        """Test movie search with empty query."""
        service = TmdbService('test_api_key')
        results = service.search_movies('')
        
        assert results['success'] is False
        assert 'error' in results
        assert 'Query cannot be empty' in results['error']
    
    def test_search_movies_none_query(self):
        """Test movie search with None query."""
        service = TmdbService('test_api_key')
        results = service.search_movies(None)
        
        assert results['success'] is False
        assert 'error' in results
        assert 'Query cannot be empty' in results['error']
    
    @patch('streamlit_hello_app.modules.tmdb_service.requests.get')
    def test_get_movie_poster_url(self, mock_get):
        """Test getting movie poster URL."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "images": {
                "base_url": "https://image.tmdb.org/t/p/",
                "poster_sizes": ["w92", "w154", "w185", "w342", "w500", "w780", "original"]
            }
        }
        mock_get.return_value = mock_response
        
        service = TmdbService('test_api_key')
        poster_url = service.get_movie_poster_url('/test_poster.jpg', size='w500')
        
        assert poster_url == 'https://image.tmdb.org/t/p/w500/test_poster.jpg'
    
    @patch('streamlit_hello_app.modules.tmdb_service.requests.get')
    def test_get_movie_poster_url_no_poster_path(self, mock_get):
        """Test getting poster URL with no poster path."""
        service = TmdbService('test_api_key')
        poster_url = service.get_movie_poster_url(None)
        
        assert poster_url is None
    
    @patch('streamlit_hello_app.modules.tmdb_service.requests.get')
    def test_get_movie_poster_url_config_error(self, mock_get):
        """Test getting poster URL with config API error."""
        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_response.json.return_value = {"success": False}
        mock_get.return_value = mock_response
        
        service = TmdbService('test_api_key')
        poster_url = service.get_movie_poster_url('/test_poster.jpg')
        
        assert poster_url is None


class TestTmdbServiceIntegration:
    """Integration tests for TmdbService."""
    
    @patch('streamlit_hello_app.modules.tmdb_service.requests.get')
    def test_full_search_workflow(self, mock_get):
        """Test complete search workflow with poster URLs."""
        # Mock search response
        search_response = MagicMock()
        search_response.status_code = 200
        search_response.json.return_value = {
            "page": 1,
            "results": [
                {
                    "id": 12345,
                    "title": "Test Movie",
                    "overview": "A test movie",
                    "poster_path": "/test_poster.jpg",
                    "release_date": "2024-01-01",
                    "vote_average": 8.5,
                    "vote_count": 1000
                }
            ],
            "total_pages": 1,
            "total_results": 1
        }
        
        # Mock config response
        config_response = MagicMock()
        config_response.status_code = 200
        config_response.json.return_value = {
            "images": {
                "base_url": "https://image.tmdb.org/t/p/",
                "poster_sizes": ["w92", "w154", "w185", "w342", "w500", "w780", "original"]
            }
        }
        
        # Configure mock to return different responses for different calls
        mock_get.side_effect = [search_response, config_response]
        
        service = TmdbService('test_api_key')
        results = service.search_movies('Test Movie')
        
        assert results['success'] is True
        assert len(results['movies']) == 1
        
        movie = results['movies'][0]
        assert movie['title'] == 'Test Movie'
        assert movie['poster_url'] == 'https://image.tmdb.org/t/p/w500/test_poster.jpg'
        assert movie['vote_average'] == 8.5
        assert movie['release_year'] == '2024'
