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
    apply_theme,
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
    
    if "theme" not in st.session_state:
        st.session_state.theme = "Dark"
    
    # Apply initial theme
    apply_theme(st.session_state.theme)
    
    # Render sidebar first to get theme selection
    page = render_sidebar()
    
    # Apply theme again after sidebar is rendered (in case theme changed)
    apply_theme(st.session_state.theme)
    
    # Add JavaScript to force dropdown dark mode
    st.markdown("""
    <script>
    function forceThemeMode() {
        // Check if we're in dark mode by looking at the app background
        const app = document.querySelector('.stApp');
        const isDarkMode = app && window.getComputedStyle(app).backgroundColor.includes('14, 17, 23'); // #0E1117
        
        if (isDarkMode) {
            // Dark mode styling
            const selectboxes = document.querySelectorAll('.stSelectbox');
            selectboxes.forEach(selectbox => {
                const allElements = selectbox.querySelectorAll('*');
                allElements.forEach(element => {
                    element.style.backgroundColor = '#262730';
                    element.style.color = '#FF6B6B'; // Orange color for dropdown text
                });
            });
            
            // Force sidebar dark mode
            const sidebar = document.querySelector('.stSidebar');
            if (sidebar) {
                sidebar.style.backgroundColor = '#262730';
                sidebar.style.color = '#FAFAFA';
                
                const sidebarElements = sidebar.querySelectorAll('*');
                sidebarElements.forEach(element => {
                    element.style.backgroundColor = '#262730';
                    element.style.color = '#FAFAFA';
                });
            }
            
            // Force main content area to dark mode
            const mainContent = document.querySelector('.main .block-container');
            if (mainContent) {
                mainContent.style.backgroundColor = '#0E1117';
                mainContent.style.color = '#FAFAFA';
                
                const mainElements = mainContent.querySelectorAll('*');
                mainElements.forEach(element => {
                    element.style.backgroundColor = '#0E1117';
                    element.style.color = '#FAFAFA';
                });
            }
            
            // Force all text elements to light color
            const textElements = document.querySelectorAll('h1, h2, h3, h4, h5, h6, p, div, span, label');
            textElements.forEach(element => {
                element.style.color = '#FAFAFA';
            });
        } else {
            // Light mode styling
            const selectboxes = document.querySelectorAll('.stSelectbox');
            selectboxes.forEach(selectbox => {
                const allElements = selectbox.querySelectorAll('*');
                allElements.forEach(element => {
                    element.style.backgroundColor = '#FFFFFF';
                    element.style.color = '#FF6B6B'; // Orange color for dropdown text
                });
            });
            
            // Force sidebar light mode
            const sidebar = document.querySelector('.stSidebar');
            if (sidebar) {
                sidebar.style.backgroundColor = '#F0F2F6';
                sidebar.style.color = '#262730';
                
                const sidebarElements = sidebar.querySelectorAll('*');
                sidebarElements.forEach(element => {
                    element.style.backgroundColor = '#F0F2F6';
                    element.style.color = '#262730';
                });
            }
            
            // Force main content area to light mode
            const mainContent = document.querySelector('.main .block-container');
            if (mainContent) {
                mainContent.style.backgroundColor = '#FFFFFF';
                mainContent.style.color = '#262730';
                
                const mainElements = mainContent.querySelectorAll('*');
                mainElements.forEach(element => {
                    element.style.backgroundColor = '#FFFFFF';
                    element.style.color = '#262730';
                });
            }
            
            // Force all text elements to dark color
            const textElements = document.querySelectorAll('h1, h2, h3, h4, h5, h6, p, div, span, label');
            textElements.forEach(element => {
                element.style.color = '#262730';
            });
        }
    }
    
    // Apply when page loads
    document.addEventListener('DOMContentLoaded', forceThemeMode);
    
    // Apply when Streamlit reruns
    if (window.parent !== window) {
        window.parent.addEventListener('load', forceThemeMode);
    }
    
    // Run continuously to catch dynamically created elements
    setInterval(forceThemeMode, 500);
    
    // Also run on any DOM changes
    const observer = new MutationObserver(forceThemeMode);
    observer.observe(document.body, { childList: true, subtree: true });
    </script>
    """, unsafe_allow_html=True)
    
    # Render header
    render_header(config)
    
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
