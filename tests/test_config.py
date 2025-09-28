"""Tests for configuration management."""

import pytest
from pathlib import Path
from tempfile import NamedTemporaryFile
import tomllib
from pydantic import ValidationError
from pydantic_core import ValidationError as CoreValidationError

from streamlit_hello_app.config import AppConfig, load_config


class TestAppConfig:
    """Test cases for AppConfig class."""
    
    def test_default_config(self):
        """Test default configuration values."""
        config = AppConfig()
        
        assert config.app_name == "Streamlit Hello App"
        assert config.app_version == "0.1.0"
        assert config.debug is False
        assert "primary_color" in config.theme
        assert config.theme["primary_color"] == "#FF6B6B"
    
    def test_custom_config(self):
        """Test custom configuration values."""
        config_data = {
            "app_name": "Custom App",
            "app_version": "1.0.0",
            "debug": True,
            "theme": {
                "primary_color": "#00FF00",
                "background_color": "#000000"
            }
        }
        
        config = AppConfig(**config_data)
        
        assert config.app_name == "Custom App"
        assert config.app_version == "1.0.0"
        assert config.debug is True
        assert config.theme["primary_color"] == "#00FF00"
        assert config.theme["background_color"] == "#000000"
    
    def test_config_validation(self):
        """Test configuration validation."""
        with pytest.raises((ValidationError, CoreValidationError)):
            AppConfig(app_name=123)  # Should be string
        
        with pytest.raises((ValidationError, CoreValidationError)):
            AppConfig(debug=[1, 2, 3])  # Should be boolean, not list


class TestLoadConfig:
    """Test cases for load_config function."""
    
    def test_load_default_config(self):
        """Test loading default configuration."""
        config = load_config()
        
        assert isinstance(config, AppConfig)
        assert config.app_name == "Streamlit Hello App"
    
    def test_load_config_from_file(self):
        """Test loading configuration from TOML file."""
        # Create temporary TOML file
        toml_content = """
app_name = "Test App"
app_version = "2.0.0"
debug = true

[theme]
primary_color = "#FF0000"
background_color = "#FFFFFF"
"""
        
        with NamedTemporaryFile(mode='w', suffix='.toml', delete=False) as f:
            f.write(toml_content)
            temp_path = Path(f.name)
        
        try:
            config = load_config(temp_path)
            
            assert config.app_name == "Test App"
            assert config.app_version == "2.0.0"
            assert config.debug is True
            assert config.theme["primary_color"] == "#FF0000"
        finally:
            temp_path.unlink()  # Clean up
    
    def test_load_config_nonexistent_file(self):
        """Test loading configuration from nonexistent file."""
        nonexistent_path = Path("nonexistent_config.toml")
        config = load_config(nonexistent_path)
        
        # Should return default config
        assert config.app_name == "Streamlit Hello App"
    
    def test_config_environment_prefix(self):
        """Test that AppConfig uses correct environment prefix."""
        config = AppConfig()
        
        # The model_config should have env_prefix = "STREAMLIT_"
        assert hasattr(config, 'model_config')
        assert config.model_config.get('env_prefix') == "STREAMLIT_"
