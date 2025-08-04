"""Simple Sphinx configuration for debugging."""
# Basic project info
from __future__ import annotations

project = 'Haive AI Agent Framework'
copyright = '2024, Haive Team'
author = 'Haive Team'
version = '1.0'
release = '1.0.0'

# Minimal extensions for testing
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'autoapi.extension',
]

# Simple AutoAPI configuration
autoapi_type = 'python'
autoapi_dirs = ['../../packages/haive-core/src']  # Just core package
autoapi_root = 'api'
autoapi_add_toctree_entry = False
autoapi_generate_api_docs = True

# Skip problematic files
autoapi_ignore = [
    '**/test*.py',
    '**/tests/**/*.py',
    '**/examples/**/*.py',
    '**/example*.py',
    '**/demo*.py',
    '**/app.py',
]

# Basic mock imports for missing dependencies
autodoc_mock_imports = [
    'google_search_results',
    'serpapi',
    'agents',
    'langgraph_supervisor',
]

# Templates and excludes
templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# HTML theme
html_theme = 'alabaster'
html_static_path = ['_static']

# Disable problematic features
autosummary_generate = False
suppress_warnings = ['ref.python', 'autosummary', 'autoapi']

print('✅ Simple Sphinx configuration loaded!')
