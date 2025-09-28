#!/usr/bin/env python3
"""
TMDB Movie Search Test Runner

This script runs all TMDB-related tests with comprehensive reporting.
"""

import subprocess
import sys
import os
from pathlib import Path


def run_command(command: str, description: str) -> bool:
    """Run a command and return success status."""
    print(f"\n{'='*60}")
    print(f"🧪 {description}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Command failed with exit code {e.returncode}")
        print("STDOUT:", e.stdout)
        print("STDERR:", e.stderr)
        return False


def main():
    """Run all TMDB tests with comprehensive reporting."""
    print("🎬 TMDB Movie Search Test Runner")
    print("=" * 60)
    
    # Change to project root
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)
    
    # Test commands
    test_commands = [
        {
            "command": "python -m pytest tests/test_tmdb_utils.py -v",
            "description": "API Key Management Tests"
        },
        {
            "command": "python -m pytest tests/test_tmdb_service.py -v",
            "description": "TMDB Service Layer Tests"
        },
        {
            "command": "python -m pytest tests/test_movie_search.py -v",
            "description": "Movie Search UI Tests"
        },
        {
            "command": "python -m pytest tests/test_tmdb_*.py tests/test_movie_search.py -v",
            "description": "All TMDB Tests Combined"
        },
        {
            "command": "python -m pytest tests/test_tmdb_*.py tests/test_movie_search.py --cov=src/streamlit_hello_app/modules/tmdb_service.py --cov=src/streamlit_hello_app/modules/movie_search.py --cov=src/streamlit_hello_app/utils.py --cov-report=term --cov-report=html",
            "description": "TMDB Tests with Coverage Report"
        }
    ]
    
    # Run tests
    success_count = 0
    total_tests = len(test_commands)
    
    for test_cmd in test_commands:
        if run_command(test_cmd["command"], test_cmd["description"]):
            success_count += 1
            print(f"✅ {test_cmd['description']} - PASSED")
        else:
            print(f"❌ {test_cmd['description']} - FAILED")
    
    # Summary
    print(f"\n{'='*60}")
    print(f"📊 Test Summary")
    print(f"{'='*60}")
    print(f"Total test suites: {total_tests}")
    print(f"Passed: {success_count}")
    print(f"Failed: {total_tests - success_count}")
    print(f"Success rate: {(success_count/total_tests)*100:.1f}%")
    
    if success_count == total_tests:
        print("\n🎉 All TMDB tests passed successfully!")
        print("✅ TMDB Movie Search implementation is ready for production!")
        return 0
    else:
        print(f"\n⚠️  {total_tests - success_count} test suite(s) failed.")
        print("Please check the output above for details.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
