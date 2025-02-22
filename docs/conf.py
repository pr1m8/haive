# Configuration file for the Sphinx documentation builder
import os
import sys
from datetime import datetime

# -- Path setup --------------------------------------------------------------
# Add mockups directory to the path so Sphinx can find the modules
sys.path.insert(0, os.path.abspath('./mockups'))

# Project information
project = 'Haive'
copyright = f'{datetime.now().year}, Your Name'
author = 'Your Name'
release = '0.1.0'

# -- General configuration ---------------------------------------------------
extensions = [
    # Core Sphinx extensions
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
    'sphinx.ext.intersphinx',
    'sphinx.ext.autosectionlabel',
    'sphinx.ext.todo',
    'sphinx.ext.mathjax',
    
    # Third-party extensions
    'myst_parser',
    'sphinx_copybutton',
    'sphinx_design',
]

# -- Autodoc settings ----------------------------------------------
autodoc_typehints = 'both'
autodoc_typehints_format = 'short'
autodoc_member_order = 'groupwise'  # Group by type (methods, attributes, etc.)
autodoc_default_options = {
    'members': True,
    'undoc-members': True,
    'special-members': '__init__, __call__',
    'inherited-members': True,
    'show-inheritance': True,
    'member-order': 'groupwise',
}

# -- Napoleon settings (for Google and NumPy style docstrings) -----------
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = True
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = True
napoleon_use_admonition_for_notes = True
napoleon_use_admonition_for_references = True
napoleon_use_ivar = True
napoleon_use_param = True
napoleon_use_rtype = True
napoleon_preprocess_types = True
napoleon_attr_annotations = True

# -- MyST Parser settings (for Markdown support) ---------------------------
myst_enable_extensions = [
    "colon_fence",
    "deflist",
    "dollarmath",
    "amsmath",
    "html_image",
    "html_admonition",
    "replacements",
    "smartquotes",
    "tasklist",
]
myst_heading_anchors = 3

# -- HTML output settings ---------------------------------------------------
html_theme = 'furo'  # Modern, clean theme
html_title = f"{project} Documentation"
html_short_title = project
html_static_path = ['_static']
html_css_files = ['custom.css']
html_js_files = ['custom.js']
html_favicon = '_static/favicon.ico'
html_logo = '_static/logo.png'
html_show_sourcelink = False
html_copy_source = False

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
