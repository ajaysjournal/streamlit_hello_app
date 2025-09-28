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
        background-color: #404040 !important;
        color: #FAFAFA !important;
        border: 1px solid #606060 !important;
    }
    .stButton > button:hover {
        background-color: #505050 !important;
        color: #FAFAFA !important;
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
    # Minimal CSS - ensure all buttons have same color
    st.sidebar.markdown("""
    <style>
    /* Ensure sidebar is visible and styled */
    .stSidebar {
        visibility: visible !important;
        display: block !important;
        background-color: #404040 !important;
    }
    
    /* Make all buttons the same color regardless of type */
    .stSidebar .stButton > button,
    .stSidebar .stButton > button[kind="primary"],
    .stSidebar .stButton > button[kind="secondary"] {
        background-color: #404040 !important;
        color: #FAFAFA !important;
        border: 1px solid #606060 !important;
    }
    
    .stSidebar .stButton > button:hover,
    .stSidebar .stButton > button[kind="primary"]:hover,
    .stSidebar .stButton > button[kind="secondary"]:hover {
        background-color: #505050 !important;
        color: #FAFAFA !important;
        border-color: #606060 !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Create a simple sidebar for testing
    st.sidebar.title("🚀 Streamlit Hello App")
    st.sidebar.markdown("---")
    
    # Simple navigation
    st.sidebar.markdown("### Navigation")
    
    if st.sidebar.button("📊 Dashboard", key="nav_dashboard", type="secondary"):
        st.session_state.page = "Dashboard"
        st.rerun()
    
    if st.sidebar.button("🔍 Data Explorer", key="nav_data_explorer", type="secondary"):
        st.session_state.page = "Data Explorer"
        st.rerun()
    
    if st.sidebar.button("💰 Compound Interest Calculator", key="nav_compound_interest", type="secondary"):
        st.session_state.page = "Compound Interest Calculator"
        st.rerun()
    
    if st.sidebar.button("🎬 Movie Search", key="nav_movie_search", type="secondary"):
        st.session_state.page = "Movie Search"
        st.rerun()
    
    if st.sidebar.button("🤖 AI Chat", key="nav_chat", type="secondary"):
        st.session_state.page = "AI Chat"
        st.rerun()
    
    if st.sidebar.button("ℹ️ About", key="nav_about", type="secondary"):
        st.session_state.page = "About"
        st.rerun()
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("**Version:** 1.0.0")
    
    return st.session_state.get("page", "Dashboard")
