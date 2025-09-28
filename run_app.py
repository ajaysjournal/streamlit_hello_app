#!/usr/bin/env python3
"""
Simple launcher script for the Streamlit Hello App.

This script can be used to run the application directly without worrying about
import path issues.
"""

import sys
from pathlib import Path

# Add the src directory to Python path
src_dir = Path(__file__).parent / "src"
sys.path.insert(0, str(src_dir))

if __name__ == "__main__":
    from streamlit_hello_app.main import main
    main()
