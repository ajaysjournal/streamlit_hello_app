"""Tests for utility functions."""

import pytest
import logging
from pathlib import Path
from tempfile import NamedTemporaryFile
from unittest.mock import patch, mock_open, MagicMock

from streamlit_hello_app.utils import (
    setup_logging,
    load_environment,
    get_project_root,
    ensure_directory,
)


class TestSetupLogging:
    """Test cases for setup_logging function."""
    
    def test_setup_logging_default_level(self):
        """Test setup_logging with default level."""
        # Reset logging to default state
        logging.getLogger().handlers.clear()
        logging.getLogger().setLevel(logging.WARNING)
        
        setup_logging()
        
        # Check that logging is configured with INFO level
        root_logger = logging.getLogger()
        assert root_logger.level == logging.INFO
    
    def test_setup_logging_custom_level(self):
        """Test setup_logging with custom level."""
        # Reset logging to default state
        logging.getLogger().handlers.clear()
        logging.getLogger().setLevel(logging.WARNING)
        
        setup_logging("DEBUG")
        
        root_logger = logging.getLogger()
        assert root_logger.level == logging.DEBUG
    
    def test_setup_logging_invalid_level(self):
        """Test setup_logging with invalid level."""
        with pytest.raises(AttributeError):
            setup_logging("INVALID_LEVEL")


class TestLoadEnvironment:
    """Test cases for load_environment function."""
    
    @patch('streamlit_hello_app.utils.load_dotenv')
    @patch('streamlit_hello_app.utils.Path')
    def test_load_environment_with_file(self, mock_path_class, mock_load_dotenv):
        """Test load_environment with specific file that doesn't exist."""
        # Create a mock Path that behaves correctly
        mock_path_instance = MagicMock()
        mock_path_instance.exists.return_value = False  # The specific file doesn't exist
        mock_path_class.return_value = mock_path_instance
        
        # Mock the default paths to exist
        def path_side_effect(path_str):
            mock_path = MagicMock()
            if path_str in [".env", ".env.local", ".env.development"]:
                mock_path.exists.return_value = True
            else:
                mock_path.exists.return_value = False
            return mock_path
        
        mock_path_class.side_effect = path_side_effect
        
        env_file = Path("test.env")
        load_environment(env_file)
        
        # Should call load_dotenv with the first default file that exists
        mock_load_dotenv.assert_called_once()
    
    @patch('streamlit_hello_app.utils.load_dotenv')
    def test_load_environment_with_existing_file(self, mock_load_dotenv):
        """Test load_environment with existing file."""
        with NamedTemporaryFile(mode='w', suffix='.env', delete=False) as f:
            f.write("TEST_VAR=test_value\n")
            temp_path = Path(f.name)
        
        try:
            load_environment(temp_path)
            mock_load_dotenv.assert_called_once_with(temp_path)
        finally:
            temp_path.unlink()
    
    @patch('streamlit_hello_app.utils.load_dotenv')
    @patch('streamlit_hello_app.utils.Path.exists')
    def test_load_environment_default_files(self, mock_exists, mock_load_dotenv):
        """Test load_environment with default file search."""
        mock_exists.return_value = True
        
        load_environment()
        
        # Should call load_dotenv for the first existing file
        mock_load_dotenv.assert_called_once()


class TestGetProjectRoot:
    """Test cases for get_project_root function."""
    
    def test_get_project_root(self):
        """Test get_project_root returns correct path."""
        root = get_project_root()
        
        assert isinstance(root, Path)
        # Should be the project root (3 levels up from utils.py)
        assert root.name == "streamlit_hello_app"


class TestEnsureDirectory:
    """Test cases for ensure_directory function."""
    
    def test_ensure_directory_creates_new(self, tmp_path):
        """Test ensure_directory creates new directory."""
        new_dir = tmp_path / "new_directory"
        
        ensure_directory(new_dir)
        
        assert new_dir.exists()
        assert new_dir.is_dir()
    
    def test_ensure_directory_existing(self, tmp_path):
        """Test ensure_directory with existing directory."""
        existing_dir = tmp_path / "existing_directory"
        existing_dir.mkdir()
        
        ensure_directory(existing_dir)
        
        assert existing_dir.exists()
        assert existing_dir.is_dir()
    
    def test_ensure_directory_nested(self, tmp_path):
        """Test ensure_directory creates nested directories."""
        nested_dir = tmp_path / "level1" / "level2" / "level3"
        
        ensure_directory(nested_dir)
        
        assert nested_dir.exists()
        assert nested_dir.is_dir()
        assert (tmp_path / "level1").exists()
        assert (tmp_path / "level1" / "level2").exists()
