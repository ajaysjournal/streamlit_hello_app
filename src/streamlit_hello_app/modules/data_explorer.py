"""Data explorer page component for Streamlit Hello App."""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from streamlit_hello_app.components import get_plotly_dark_theme


def render_data_explorer() -> None:
    """Render the data explorer page."""
    st.header("🔍 Data Explorer")
    
    # File uploader
    uploaded_file = st.file_uploader(
        "Choose a CSV file",
        type="csv",
        help="Upload a CSV file to explore its data"
    )
    
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            
            st.subheader("📋 Data Preview")
            st.dataframe(df.head(10))
            
            st.subheader("📊 Data Summary")
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Dataset Info:**")
                st.write(f"- Rows: {len(df)}")
                st.write(f"- Columns: {len(df.columns)}")
                st.write(f"- Memory usage: {df.memory_usage(deep=True).sum() / 1024:.2f} KB")
            
            with col2:
                st.write("**Column Types:**")
                # Convert dtypes to string to avoid Arrow serialization issues
                dtype_df = df.dtypes.to_frame('Type')
                dtype_df['Type'] = dtype_df['Type'].astype(str)
                st.dataframe(dtype_df)
            
            # Column selector for visualization
            numeric_columns = df.select_dtypes(include=[np.number]).columns.tolist()
            
            if numeric_columns:
                st.subheader("📈 Data Visualization")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    x_col = st.selectbox("X-axis:", numeric_columns)
                    y_col = st.selectbox("Y-axis:", numeric_columns)
                    
                    if x_col and y_col and x_col != y_col:
                        # Get current theme for chart styling
                        theme_config = get_plotly_dark_theme()
                        
                        fig = px.scatter(df, x=x_col, y=y_col, title=f"{x_col} vs {y_col}")
                        fig.update_layout(**theme_config["layout"])
                        st.plotly_chart(fig, config={'displayModeBar': False})
                
                with col2:
                    hist_col = st.selectbox("Histogram column:", numeric_columns)
                    if hist_col:
                        # Get current theme for chart styling
                        theme_config = get_plotly_dark_theme()
                        
                        fig = px.histogram(df, x=hist_col, title=f"Distribution of {hist_col}")
                        fig.update_layout(**theme_config["layout"])
                        st.plotly_chart(fig, config={'displayModeBar': False})
            
        except Exception as e:
            st.error(f"Error reading file: {str(e)}")
    else:
        st.info("👆 Please upload a CSV file to explore data")
        
        # Show sample data
        st.subheader("🎯 Sample Data")
        sample_data = {
            'Name': ['Alice', 'Bob', 'Charlie', 'Diana', 'Eve'],
            'Age': [25, 30, 35, 28, 32],
            'City': ['New York', 'London', 'Tokyo', 'Paris', 'Sydney'],
            'Salary': [50000, 60000, 70000, 55000, 65000]
        }
        sample_df = pd.DataFrame(sample_data)
        
        st.dataframe(sample_df)
        
        # Interactive visualization of sample data
        st.subheader("📊 Sample Visualization")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Get dark theme for chart styling
            theme_config = get_plotly_dark_theme()
            
            fig = px.bar(sample_df, x='Name', y='Salary', title='Salary by Name')
            fig.update_layout(**theme_config["layout"])
            st.plotly_chart(fig, config={'displayModeBar': False})
        
        with col2:
            # Get dark theme for chart styling
            theme_config = get_plotly_dark_theme()
            
            fig = px.scatter(sample_df, x='Age', y='Salary', hover_data=['City'], 
                           title='Age vs Salary')
            fig.update_layout(**theme_config["layout"])
            st.plotly_chart(fig, config={'displayModeBar': False})
