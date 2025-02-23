import os
import sys
from datetime import datetime

# -- Path setup --------------------------------------------------------------
sys.path.insert(0, os.path.abspath('../src'))  # Ensure Haive is in the Python path

# Project information
project = 'Haive'
copyright = f'{datetime.now().year}, Your Name'
author = 'Your Name'
release = '0.1.0'

# -- General configuration ---------------------------------------------------
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
    'sphinx.ext.intersphinx',
    'sphinx.ext.autosectionlabel',
    'sphinx.ext.todo',
    'sphinx.ext.mathjax',
    'sphinx_copybutton',
    'sphinx_design',  # Ensure this is here
]


# Ensure Sphinx detects modules correctly
# Enable automatic module documentation generation
autosummary_generate = True
autodoc_default_options = {
    'members': True,
    'undoc-members': True,
    'special-members': '__init__, __call__',
    'inherited-members': True,
    'show-inheritance': True,
}

# Enable correct package detection
autodoc_mock_imports = [
    'langchain', 'langchain_community', 'pydantic', 'BaseModel'
]

# -- HTML output settings ---------------------------------------------------
html_theme = 'furo'
html_title = "Haive Documentation"
html_short_title = "Haive"
html_static_path = ['_static']
html_css_files = ['custom.css']
html_favicon = '_static/favicon.ico'
html_logo = '_static/logo.png'

# Furo theme options
html_theme_options = {
    "sidebar_hide_name": False,
    "light_css_variables": {
        "color-brand-primary": "#3776ab",  # Python blue
        "color-brand-content": "#3776ab",
        "color-admonition-background": "#f8f9fb",
        "font-stack": "system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue', sans-serif",
        "font-stack--monospace": "SFMono-Regular, Menlo, Monaco, Consolas, 'Liberation Mono', 'Courier New', monospace",
    },
    "dark_css_variables": {
        "color-brand-primary": "#5994ce",  # Lighter blue for dark mode
        "color-brand-content": "#5994ce",
    },
}

# -- Intersphinx mapping --------------------------------------------------
intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
}

# -- Additional settings ---------------------------------------------------
todo_include_todos = True  # Include TODOs in documentation
pygments_style = "sphinx"  # Syntax highlighting style

# Mock imports to prevent import errors
autodoc_mock_imports = [
    'src',
    'langchain', 
    'langchain_community',
    'pydantic',
    'BaseModel'
]
