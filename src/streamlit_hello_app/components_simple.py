"""Simplified Streamlit UI components for the Hello App - Dark Mode Only."""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from typing import Dict, Any

from streamlit_hello_app.config import AppConfig


def get_plotly_dark_theme() -> dict:
    """Get Plotly dark theme configuration."""
    return {
        "layout": {
            "paper_bgcolor": "#0E1117",
            "plot_bgcolor": "#0E1117",
            "font": {"color": "#FAFAFA"},
            "xaxis": {
                "gridcolor": "#404040",
                "color": "#FAFAFA"
            },
            "yaxis": {
                "gridcolor": "#404040", 
                "color": "#FAFAFA"
            }
        }
    }


def apply_dark_theme() -> None:
    """Apply dark theme to the Streamlit app."""
    st.markdown("""
    <style>
    .stApp {
        background-color: #0E1117 !important;
        color: #FAFAFA !important;
    }
    .stSidebar {
        background-color: #404040 !important;
    }
    .stSidebar * {
        background-color: #404040 !important;
        color: #FAFAFA !important;
    }
    .stButton > button {
        background-color: #FF6B6B !important;
        color: white !important;
        border: 1px solid #FF6B6B !important;
    }
    .stButton > button:hover {
        background-color: #FF5252 !important;
    }
    .stSelectbox > div > div {
        background-color: #404040 !important;
        color: #FAFAFA !important;
    }
    .stCheckbox > div > div {
        background-color: #404040 !important;
    }
    .stMetric {
        background-color: #404040 !important;
        color: #FAFAFA !important;
    }
    .stDataFrame {
        background-color: #404040 !important;
        color: #FAFAFA !important;
    }
    h1, h2, h3, h4, h5, h6, p, div, span, label {
        color: #FAFAFA !important;
    }
    </style>
    """, unsafe_allow_html=True)


def render_header(config: AppConfig) -> None:
    """Render the application header."""
    st.title("🚀 Streamlit Hello App")
    st.markdown(f"**Version:** {config.app_version}")


def render_sidebar() -> str:
    """Render the sidebar navigation."""
    # Add custom CSS for better sidebar styling
    st.sidebar.markdown("""
    <style>
    .sidebar .stButton > button {
        width: 100%;
        border-radius: 8px;
        border: 1px solid transparent;
        padding: 0.5rem 1rem;
        margin: 0.25rem 0;
        font-size: 0.9rem;
        font-weight: 500;
        text-align: left;
        transition: all 0.2s;
    }
    
    .sidebar .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .sidebar .stButton > button[kind="primary"] {
        background-color: #FF6B6B;
        color: white;
        border-color: #FF6B6B;
    }
    
    .sidebar .stButton > button[kind="primary"]:hover {
        background-color: #FF5252;
        border-color: #FF5252;
    }
    
    .sidebar .stButton > button[kind="secondary"] {
        background-color: transparent;
        color: inherit;
        border-color: rgba(255,255,255,0.2);
    }
    
    .sidebar .stButton > button[kind="secondary"]:hover {
        background-color: rgba(255,255,255,0.1);
        border-color: rgba(255,255,255,0.3);
    }
    
    .sidebar .stCaption {
        font-size: 0.8rem;
        color: #888;
        margin-top: -0.5rem;
        margin-bottom: 0.5rem;
    }
    
    .sidebar h3 {
        color: #FF6B6B;
        margin-top: 1.5rem;
        margin-bottom: 0.5rem;
    }
    
    .sidebar .stInfo {
        background-color: rgba(255,107,107,0.1);
        border: 1px solid rgba(255,107,107,0.2);
        border-radius: 6px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Create a clean, organized sidebar
    st.sidebar.markdown("## 🚀 Streamlit Hello App")
    st.sidebar.markdown("---")
    
    # Navigation section
    st.sidebar.markdown("### 📋 Navigation")
    
    # Define pages with icons and descriptions
    pages = {
        "Dashboard": {"icon": "📊", "desc": "Overview & Analytics"},
        "Data Explorer": {"icon": "🔍", "desc": "Upload & Analyze Data"},
        "Compound Interest Calculator": {"icon": "💰", "desc": "Financial Planning Tool"},
        "About": {"icon": "ℹ️", "desc": "App Information"}
    }
    
    current_page = st.session_state.get("page", "Dashboard")
    
    # Create navigation buttons
    for page_name, page_info in pages.items():
        if st.sidebar.button(
            f"{page_info['icon']} {page_name}",
            key=f"nav_{page_name}",
            use_container_width=True,
            type="primary" if page_name == current_page else "secondary"
        ):
            st.session_state.page = page_name
            st.rerun()
        
        # Add description
        st.sidebar.caption(page_info['desc'])
    
    # App info
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📱 App Info")
    st.sidebar.info("**Version:** 1.0.0\n\n**Theme:** Dark Mode\n\n**Status:** ✅ Running")
    
    return st.session_state.get("page", "Dashboard")
