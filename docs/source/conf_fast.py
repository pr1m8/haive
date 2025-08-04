"""Fast Sphinx configuration focusing on core content."""
# Basic project info
from __future__ import annotations

project = 'Haive AI Agent Framework'
copyright = '2024, Haive Team'
author = 'Haive Team'

# Minimal extensions for fast build
extensions = [
    'sphinx.ext.autodoc',
    'myst_parser',
]

# Skip AutoAPI for faster build
# Just build the RST documentation files

# File patterns to exclude
exclude_patterns = [
    '_build',
    'Thumbs.db',
    '.DS_Store',
    'api/*',  # Skip API for now
    'auto_examples/*',  # Skip examples
    'reference/*',  # Skip reference
    'logs/*',
    'archive/*',
]

# HTML theme and output
html_theme = 'alabaster'
html_static_path = ['_static']
templates_path = ['_templates']

# Mock imports
autodoc_mock_imports = [
    'google_search_results',
    'serpapi',
    'agents',
]

print('✅ Fast Sphinx configuration for content pages!')
