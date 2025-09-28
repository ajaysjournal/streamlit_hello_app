"""Tests for OpenAI service functions."""

import pytest
from unittest.mock import patch, MagicMock
from requests.exceptions import RequestException, ConnectionError, Timeout

from streamlit_hello_app.modules.openai_service import (
    OpenAIService,
    OPENAI_BASE_URL,
    OPENAI_CHAT_ENDPOINT,
    OPENAI_MODELS_ENDPOINT
)


class TestOpenAIService:
    """Test cases for OpenAIService class."""
    
    def test_init_with_api_key(self):
        """Test OpenAIService initialization with API key."""
        service = OpenAIService('test_api_key_123')
        assert service.api_key == 'test_api_key_123'
        assert service.base_url == OPENAI_BASE_URL
    
    def test_init_without_api_key(self):
        """Test OpenAIService initialization without API key."""
        service = OpenAIService()
        assert service.api_key is None
        assert service.base_url == OPENAI_BASE_URL
    
    @patch('streamlit_hello_app.modules.openai_service.requests.post')
    def test_chat_completion_success(self, mock_post):
        """Test successful chat completion."""
        # Mock successful chat response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "id": "chatcmpl-123",
            "object": "chat.completion",
            "created": 1677652288,
            "model": "gpt-3.5-turbo",
            "choices": [
                {
                    "index": 0,
                    "message": {
                        "role": "assistant",
                        "content": "Hello! How can I help you today?"
                    },
                    "finish_reason": "stop"
                }
            ],
            "usage": {
                "prompt_tokens": 9,
                "completion_tokens": 12,
                "total_tokens": 21
            }
        }
        mock_post.return_value = mock_response
        
        service = OpenAIService('test_api_key')
        result = service.chat_completion('Hello, how are you?')
        
        assert result['success'] is True
        assert result['response'] == 'Hello! How can I help you today?'
        assert result['model'] == 'gpt-3.5-turbo'
        assert result['usage']['total_tokens'] == 21
        
        # Verify API call was made correctly
        mock_post.assert_called_once()
        call_args = mock_post.call_args
        assert call_args[0][0] == f"{OPENAI_BASE_URL}{OPENAI_CHAT_ENDPOINT}"
        assert call_args[1]['headers']['Authorization'] == 'Bearer test_api_key'
    
    @patch('streamlit_hello_app.modules.openai_service.requests.post')
    def test_chat_completion_with_system_message(self, mock_post):
        """Test chat completion with system message."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [
                {
                    "message": {
                        "role": "assistant",
                        "content": "I'm a helpful assistant."
                    }
                }
            ],
            "usage": {"total_tokens": 15}
        }
        mock_post.return_value = mock_response
        
        service = OpenAIService('test_api_key')
        result = service.chat_completion(
            'Hello',
            system_message='You are a helpful assistant.',
            model='gpt-4'
        )
        
        assert result['success'] is True
        assert result['response'] == "I'm a helpful assistant."
        
        # Verify request payload
        call_args = mock_post.call_args
        request_data = call_args[1]['json']
        assert request_data['model'] == 'gpt-4'
        assert len(request_data['messages']) == 2
        assert request_data['messages'][0]['role'] == 'system'
        assert request_data['messages'][0]['content'] == 'You are a helpful assistant.'
        assert request_data['messages'][1]['role'] == 'user'
        assert request_data['messages'][1]['content'] == 'Hello'
    
    @patch('streamlit_hello_app.modules.openai_service.requests.post')
    def test_chat_completion_with_conversation_history(self, mock_post):
        """Test chat completion with conversation history."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [
                {
                    "message": {
                        "role": "assistant",
                        "content": "I understand you're asking about Python."
                    }
                }
            ],
            "usage": {"total_tokens": 20}
        }
        mock_post.return_value = mock_response
        
        service = OpenAIService('test_api_key')
        conversation = [
            {"role": "user", "content": "What is Python?"},
            {"role": "assistant", "content": "Python is a programming language."},
            {"role": "user", "content": "Tell me more about it."}
        ]
        
        result = service.chat_completion_with_history(conversation)
        
        assert result['success'] is True
        assert result['response'] == "I understand you're asking about Python."
        
        # Verify request payload includes conversation history
        call_args = mock_post.call_args
        request_data = call_args[1]['json']
        assert len(request_data['messages']) == 3
        assert request_data['messages'] == conversation
    
    @patch('streamlit_hello_app.modules.openai_service.requests.post')
    def test_chat_completion_api_error(self, mock_post):
        """Test chat completion with API error."""
        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_response.json.return_value = {
            "error": {
                "message": "Invalid API key",
                "type": "invalid_request_error"
            }
        }
        mock_post.return_value = mock_response
        
        service = OpenAIService('invalid_key')
        result = service.chat_completion('Hello')
        
        assert result['success'] is False
        assert 'error' in result
        assert 'Invalid API key' in result['error']
    
    @patch('streamlit_hello_app.modules.openai_service.requests.post')
    def test_chat_completion_connection_error(self, mock_post):
        """Test chat completion with connection error."""
        mock_post.side_effect = ConnectionError("Connection failed")
        
        service = OpenAIService('test_api_key')
        result = service.chat_completion('Hello')
        
        assert result['success'] is False
        assert 'error' in result
        assert 'Connection failed' in result['error']
    
    @patch('streamlit_hello_app.modules.openai_service.requests.post')
    def test_chat_completion_timeout(self, mock_post):
        """Test chat completion with timeout."""
        mock_post.side_effect = Timeout("Request timed out")
        
        service = OpenAIService('test_api_key')
        result = service.chat_completion('Hello')
        
        assert result['success'] is False
        assert 'error' in result
        assert 'Request timed out' in result['error']
    
    def test_chat_completion_no_api_key(self):
        """Test chat completion without API key."""
        service = OpenAIService()
        result = service.chat_completion('Hello')
        
        assert result['success'] is False
        assert 'error' in result
        assert 'API key is required' in result['error']
    
    def test_chat_completion_empty_message(self):
        """Test chat completion with empty message."""
        service = OpenAIService('test_api_key')
        result = service.chat_completion('')
        
        assert result['success'] is False
        assert 'error' in result
        assert 'Message cannot be empty' in result['error']
    
    def test_chat_completion_none_message(self):
        """Test chat completion with None message."""
        service = OpenAIService('test_api_key')
        result = service.chat_completion(None)
        
        assert result['success'] is False
        assert 'error' in result
        assert 'Message cannot be empty' in result['error']
    
    @patch('streamlit_hello_app.modules.openai_service.requests.get')
    def test_get_available_models(self, mock_get):
        """Test getting available models."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": [
                {
                    "id": "gpt-3.5-turbo",
                    "object": "model",
                    "created": 1677610602,
                    "owned_by": "openai"
                },
                {
                    "id": "gpt-4",
                    "object": "model",
                    "created": 1687882411,
                    "owned_by": "openai"
                }
            ]
        }
        mock_get.return_value = mock_response
        
        service = OpenAIService('test_api_key')
        models = service.get_available_models()
        
        assert models['success'] is True
        assert len(models['models']) == 2
        assert models['models'][0]['id'] == 'gpt-3.5-turbo'
        assert models['models'][1]['id'] == 'gpt-4'
    
    @patch('streamlit_hello_app.modules.openai_service.requests.get')
    def test_get_available_models_error(self, mock_get):
        """Test getting available models with error."""
        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_response.json.return_value = {
            "error": {
                "message": "Invalid API key",
                "type": "invalid_request_error"
            }
        }
        mock_get.return_value = mock_response
        
        service = OpenAIService('invalid_key')
        models = service.get_available_models()
        
        assert models['success'] is False
        assert 'error' in models
        assert 'Invalid API key' in models['error']
    
    def test_get_available_models_no_api_key(self):
        """Test getting available models without API key."""
        service = OpenAIService()
        models = service.get_available_models()
        
        assert models['success'] is False
        assert 'error' in models
        assert 'API key is required' in models['error']


class TestOpenAIServiceIntegration:
    """Integration tests for OpenAIService."""
    
    @patch('streamlit_hello_app.modules.openai_service.requests.post')
    def test_full_chat_workflow(self, mock_post):
        """Test complete chat workflow."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [
                {
                    "message": {
                        "role": "assistant",
                        "content": "I can help you with that!"
                    }
                }
            ],
            "usage": {"total_tokens": 25}
        }
        mock_post.return_value = mock_response
        
        service = OpenAIService('test_api_key')
        result = service.chat_completion(
            'Can you help me with Python?',
            system_message='You are a Python expert.',
            model='gpt-4'
        )
        
        assert result['success'] is True
        assert result['response'] == "I can help you with that!"
        assert result['model'] == 'gpt-4'
        assert result['usage']['total_tokens'] == 25
