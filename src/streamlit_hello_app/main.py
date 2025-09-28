"""Main Streamlit application entry point."""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from typing import Dict, Any

from streamlit_hello_app.config import AppConfig, load_config
from streamlit_hello_app.utils import setup_logging, load_environment, get_project_root
from streamlit_hello_app.components import (
    render_header,
    render_sidebar,
    render_dashboard,
    render_data_explorer,
    render_about,
)


def configure_page() -> None:
    """Configure Streamlit page settings."""
    st.set_page_config(
        page_title="Streamlit Hello App",
        page_icon="🚀",
        layout="wide",
        initial_sidebar_state="expanded",
    )


def main() -> None:
    """
    Main application function.
    
    This function sets up the Streamlit application, loads configuration,
    and renders the main interface.
    """
    # Load environment variables
    load_environment()
    
    # Setup logging
    setup_logging()
    
    # Configure page
    configure_page()
    
    # Load configuration
    config = load_config()
    
    # Initialize session state
    if "page" not in st.session_state:
        st.session_state.page = "Dashboard"
    
    # Render header
    render_header(config)
    
    # Render sidebar
    page = render_sidebar()
    
    # Render main content based on selected page
    if page == "Dashboard":
        render_dashboard()
    elif page == "Data Explorer":
        render_data_explorer()
    elif page == "About":
        render_about(config)


def cli_main():
    """CLI entry point for the streamlit-app command."""
    import subprocess
    import sys
    import os
    
    # Get the directory of this file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Run streamlit with this file
    cmd = [sys.executable, "-m", "streamlit", "run", os.path.join(current_dir, "main.py")]
    subprocess.run(cmd)


if __name__ == "__main__":
    main()
