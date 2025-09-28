"""OpenAI API service for chat functionality."""

import logging
from typing import Dict, List, Optional, Any
import requests
from requests.exceptions import RequestException, ConnectionError, Timeout

# OpenAI API Configuration
OPENAI_BASE_URL = "https://api.openai.com/v1"
OPENAI_CHAT_ENDPOINT = "/chat/completions"
OPENAI_MODELS_ENDPOINT = "/models"

# Error messages
API_KEY_REQUIRED_ERROR = "API key is required"
INVALID_API_KEY_ERROR = "Invalid API key"
APPLICATION_JSON = "application/json"


class OpenAIService:
    """Service class for interacting with OpenAI API."""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize OpenAI service.
        
        Args:
            api_key: OpenAI API key
        """
        self.api_key = api_key
        self.base_url = OPENAI_BASE_URL
    
    def chat_completion(
        self, 
        message: str, 
        system_message: Optional[str] = None,
        model: str = "gpt-3.5-turbo",
        temperature: float = 0.7,
        max_tokens: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Send a chat completion request to OpenAI API.
        
        Args:
            message: User message to send
            system_message: Optional system message to set context
            model: Model to use for completion
            temperature: Sampling temperature (0.0 to 2.0)
            max_tokens: Maximum tokens in response
            
        Returns:
            Dictionary containing response and metadata
        """
        if not self.api_key:
            return {
                'success': False,
                'error': API_KEY_REQUIRED_ERROR
            }
        
        if not message or not message.strip():
            return {
                'success': False,
                'error': 'Message cannot be empty'
            }
        
        try:
            url = f"{self.base_url}{OPENAI_CHAT_ENDPOINT}"
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": APPLICATION_JSON
            }
            
            # Build messages array
            messages = []
            if system_message:
                messages.append({
                    "role": "system",
                    "content": system_message
                })
            messages.append({
                "role": "user",
                "content": message.strip()
            })
            
            payload = {
                "model": model,
                "messages": messages,
                "temperature": temperature
            }
            
            if max_tokens:
                payload["max_tokens"] = max_tokens
            
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                
                # Extract response content
                if data.get('choices') and len(data['choices']) > 0:
                    response_content = data['choices'][0]['message']['content']
                else:
                    response_content = "No response generated"
                
                return {
                    'success': True,
                    'response': response_content,
                    'model': data.get('model', model),
                    'usage': data.get('usage', {}),
                    'finish_reason': data.get('choices', [{}])[0].get('finish_reason', 'unknown')
                }
            
            elif response.status_code == 401:
                return {
                    'success': False,
                    'error': INVALID_API_KEY_ERROR
                }
            
            elif response.status_code == 429:
                return {
                    'success': False,
                    'error': 'Rate limit exceeded. Please try again later.'
                }
            
            else:
                try:
                    error_data = response.json()
                    error_message = error_data.get('error', {}).get('message', f'HTTP {response.status_code}')
                except ValueError:
                    error_message = f'HTTP {response.status_code}'
                
                return {
                    'success': False,
                    'error': f'API error: {error_message}'
                }
                
        except (ConnectionError, Timeout) as e:
            logging.error(f"OpenAI API connection error: {e}")
            return {
                'success': False,
                'error': f'Connection error: {str(e)}'
            }
        except RequestException as e:
            logging.error(f"OpenAI API request error: {e}")
            return {
                'success': False,
                'error': f'Request error: {str(e)}'
            }
        except Exception as e:
            logging.error(f"Unexpected error in OpenAI chat completion: {e}")
            return {
                'success': False,
                'error': f'Unexpected error: {str(e)}'
            }
    
    def chat_completion_with_history(
        self, 
        conversation_history: List[Dict[str, str]], 
        model: str = "gpt-3.5-turbo",
        temperature: float = 0.7,
        max_tokens: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Send a chat completion request with conversation history.
        
        Args:
            conversation_history: List of message dictionaries with 'role' and 'content'
            model: Model to use for completion
            temperature: Sampling temperature (0.0 to 2.0)
            max_tokens: Maximum tokens in response
            
        Returns:
            Dictionary containing response and metadata
        """
        if not self.api_key:
            return {
                'success': False,
                'error': API_KEY_REQUIRED_ERROR
            }
        
        if not conversation_history or len(conversation_history) == 0:
            return {
                'success': False,
                'error': 'Conversation history cannot be empty'
            }
        
        try:
            url = f"{self.base_url}{OPENAI_CHAT_ENDPOINT}"
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": APPLICATION_JSON
            }
            
            payload = {
                "model": model,
                "messages": conversation_history,
                "temperature": temperature
            }
            
            if max_tokens:
                payload["max_tokens"] = max_tokens
            
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                
                # Extract response content
                if data.get('choices') and len(data['choices']) > 0:
                    response_content = data['choices'][0]['message']['content']
                else:
                    response_content = "No response generated"
                
                return {
                    'success': True,
                    'response': response_content,
                    'model': data.get('model', model),
                    'usage': data.get('usage', {}),
                    'finish_reason': data.get('choices', [{}])[0].get('finish_reason', 'unknown')
                }
            
            elif response.status_code == 401:
                return {
                    'success': False,
                    'error': INVALID_API_KEY_ERROR
                }
            
            elif response.status_code == 429:
                return {
                    'success': False,
                    'error': 'Rate limit exceeded. Please try again later.'
                }
            
            else:
                try:
                    error_data = response.json()
                    error_message = error_data.get('error', {}).get('message', f'HTTP {response.status_code}')
                except ValueError:
                    error_message = f'HTTP {response.status_code}'
                
                return {
                    'success': False,
                    'error': f'API error: {error_message}'
                }
                
        except (ConnectionError, Timeout) as e:
            logging.error(f"OpenAI API connection error: {e}")
            return {
                'success': False,
                'error': f'Connection error: {str(e)}'
            }
        except RequestException as e:
            logging.error(f"OpenAI API request error: {e}")
            return {
                'success': False,
                'error': f'Request error: {str(e)}'
            }
        except Exception as e:
            logging.error(f"Unexpected error in OpenAI chat completion: {e}")
            return {
                'success': False,
                'error': f'Unexpected error: {str(e)}'
            }
    
    def get_available_models(self) -> Dict[str, Any]:
        """
        Get list of available OpenAI models.
        
        Returns:
            Dictionary containing available models or error
        """
        if not self.api_key:
            return {
                'success': False,
                'error': API_KEY_REQUIRED_ERROR
            }
        
        try:
            url = f"{self.base_url}{OPENAI_MODELS_ENDPOINT}"
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": APPLICATION_JSON
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                models = data.get('data', [])
                
                # Filter for chat models only
                chat_models = [
                    model for model in models 
                    if model.get('id', '').startswith(('gpt-', 'claude-'))
                ]
                
                return {
                    'success': True,
                    'models': chat_models
                }
            
            elif response.status_code == 401:
                return {
                    'success': False,
                    'error': INVALID_API_KEY_ERROR
                }
            
            else:
                try:
                    error_data = response.json()
                    error_message = error_data.get('error', {}).get('message', f'HTTP {response.status_code}')
                except ValueError:
                    error_message = f'HTTP {response.status_code}'
                
                return {
                    'success': False,
                    'error': f'API error: {error_message}'
                }
                
        except (ConnectionError, Timeout) as e:
            logging.error(f"OpenAI API connection error: {e}")
            return {
                'success': False,
                'error': f'Connection error: {str(e)}'
            }
        except RequestException as e:
            logging.error(f"OpenAI API request error: {e}")
            return {
                'success': False,
                'error': f'Request error: {str(e)}'
            }
        except Exception as e:
            logging.error(f"Unexpected error getting OpenAI models: {e}")
            return {
                'success': False,
                'error': f'Unexpected error: {str(e)}'
            }
