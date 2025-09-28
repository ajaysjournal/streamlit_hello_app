"""Tests for TMDB utility functions."""

import pytest
import os
from unittest.mock import patch, MagicMock
from requests.exceptions import RequestException, ConnectionError, Timeout

from streamlit_hello_app.utils import (
    get_tmdb_api_key,
    validate_tmdb_api_key,
    TMDB_API_KEY_ERROR,
    TMDB_API_KEY_INVALID,
    TMDB_API_KEY_VALID
)


class TestGetTmdbApiKey:
    """Test cases for get_tmdb_api_key function."""
    
    @patch.dict(os.environ, {'TMDB_API_KEY': 'test_api_key_123'})
    def test_get_api_key_from_environment(self):
        """Test getting API key from environment variable."""
        api_key = get_tmdb_api_key()
        assert api_key == 'test_api_key_123'
    
    @patch.dict(os.environ, {}, clear=True)
    def test_get_api_key_no_environment_no_streamlit(self):
        """Test getting API key when not in environment and streamlit not available."""
        # This should return None when streamlit is not available
        api_key = get_tmdb_api_key()
        assert api_key is None


class TestValidateTmdbApiKey:
    """Test cases for validate_tmdb_api_key function."""
    
    @patch('streamlit_hello_app.utils.requests.get')
    def test_validate_api_key_success(self, mock_get):
        """Test successful API key validation."""
        # Mock successful response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "success": True,
            "status_code": 1,
            "status_message": "Success."
        }
        mock_get.return_value = mock_response
        
        result = validate_tmdb_api_key('valid_api_key')
        
        assert result == TMDB_API_KEY_VALID
        mock_get.assert_called_once()
    
    @patch('streamlit_hello_app.utils.requests.get')
    def test_validate_api_key_invalid_key(self, mock_get):
        """Test validation with invalid API key."""
        # Mock unauthorized response
        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_response.json.return_value = {
            "success": False,
            "status_code": 7,
            "status_message": "Invalid API key: You must be granted a valid key."
        }
        mock_get.return_value = mock_response
        
        result = validate_tmdb_api_key('invalid_api_key')
        
        assert result == TMDB_API_KEY_INVALID
        mock_get.assert_called_once()
    
    @patch('streamlit_hello_app.utils.requests.get')
    def test_validate_api_key_connection_error(self, mock_get):
        """Test validation with connection error."""
        mock_get.side_effect = ConnectionError("Connection failed")
        
        result = validate_tmdb_api_key('test_key')
        
        assert result == TMDB_API_KEY_ERROR
        mock_get.assert_called_once()
    
    @patch('streamlit_hello_app.utils.requests.get')
    def test_validate_api_key_timeout(self, mock_get):
        """Test validation with timeout error."""
        mock_get.side_effect = Timeout("Request timed out")
        
        result = validate_tmdb_api_key('test_key')
        
        assert result == TMDB_API_KEY_ERROR
        mock_get.assert_called_once()
    
    @patch('streamlit_hello_app.utils.requests.get')
    def test_validate_api_key_request_exception(self, mock_get):
        """Test validation with general request exception."""
        mock_get.side_effect = RequestException("Request failed")
        
        result = validate_tmdb_api_key('test_key')
        
        assert result == TMDB_API_KEY_ERROR
        mock_get.assert_called_once()
    
    @patch('streamlit_hello_app.utils.requests.get')
    def test_validate_api_key_http_error(self, mock_get):
        """Test validation with HTTP error status."""
        # Mock server error response
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.json.return_value = {
            "success": False,
            "status_code": 25,
            "status_message": "Your request count (40) is over the allowed limit of 40."
        }
        mock_get.return_value = mock_response
        
        result = validate_tmdb_api_key('test_key')
        
        assert result == TMDB_API_KEY_ERROR
        mock_get.assert_called_once()
    
    def test_validate_api_key_none_input(self):
        """Test validation with None API key."""
        result = validate_tmdb_api_key(None)
        assert result == TMDB_API_KEY_ERROR
    
    def test_validate_api_key_empty_input(self):
        """Test validation with empty API key."""
        result = validate_tmdb_api_key('')
        assert result == TMDB_API_KEY_ERROR
    
    @patch('streamlit_hello_app.utils.requests.get')
    def test_validate_api_key_json_decode_error(self, mock_get):
        """Test validation with JSON decode error."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.side_effect = ValueError("Invalid JSON")
        mock_get.return_value = mock_response
        
        result = validate_tmdb_api_key('test_key')
        
        assert result == TMDB_API_KEY_ERROR
        mock_get.assert_called_once()


class TestTmdbApiKeyIntegration:
    """Integration tests for TMDB API key management."""
    
    @patch.dict(os.environ, {'TMDB_API_KEY': 'test_api_key_123'})
    @patch('streamlit_hello_app.utils.requests.get')
    def test_get_and_validate_api_key_success(self, mock_get):
        """Test getting API key from environment and validating it."""
        # Mock successful validation
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"success": True}
        mock_get.return_value = mock_response
        
        api_key = get_tmdb_api_key()
        validation_result = validate_tmdb_api_key(api_key)
        
        assert api_key == 'test_api_key_123'
        assert validation_result == TMDB_API_KEY_VALID
    
    @patch.dict(os.environ, {'TMDB_API_KEY': 'test_api_key_123'})
    @patch('streamlit_hello_app.utils.requests.get')
    def test_get_and_validate_api_key_environment_success(self, mock_get):
        """Test getting API key from environment and validating it."""
        # Mock successful validation
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"success": True}
        mock_get.return_value = mock_response
        
        api_key = get_tmdb_api_key()
        validation_result = validate_tmdb_api_key(api_key)
        
        assert api_key == 'test_api_key_123'
        assert validation_result == TMDB_API_KEY_VALID
