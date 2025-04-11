"""
Configuration file for pytest to properly handle imports.
Save as tests/conftest.py
"""
import os
import sys

# Add the project root to the Python path
def pytest_configure(config):
    """Add the project root to sys.path to enable correct imports."""
    # Get the directory where conftest.py is located (tests dir)
    tests_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Navigate up to project root
    project_root = os.path.dirname(tests_dir)
    
    # Add project root to sys.path if not already there
    if project_root not in sys.path:
        sys.path.insert(0, project_root)
        print(f"Added {project_root} to sys.path")