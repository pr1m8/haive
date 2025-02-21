# conf.py
import os
import sys

# Add the src directory to the path so sphinx can find your modules
sys.path.insert(0, os.path.abspath('../../src'))

# Project information
project = 'Haive'
copyright = '2025, William R. Astley'
author = 'William R. Astley'
release = '1.0.0'  # Update with your current version

# Extensions
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
    'sphinx.ext.intersphinx',
    'myst_parser',
]

# Theme configuration
html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

# autodoc configuration
autodoc_typehints = 'description'
autodoc_member_order = 'bysource'
autodoc_default_options = {
    'members': True,
    'show-inheritance': True,
    'undoc-members': True,
}

# intersphinx configuration
intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
}