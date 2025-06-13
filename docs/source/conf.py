# Configuration file for the Sphinx documentation builder.
import os
import sys
from pathlib import Path

# Get the workspace root (where all packages are)
workspace_root = Path(__file__).resolve().parents[2]

# Add the main src directory
sys.path.insert(0, os.path.abspath("../../src"))

# IMPORTANT: Add all package src directories to sys.path
packages = ['haive-core', 'haive-agents', 'haive-tools', 'haive-games', 'haive-dataflow', 'haive-prebuilt']
for package in packages:
    package_src = workspace_root / 'packages' / package / 'src'
    if package_src.exists():
        sys.path.insert(0, str(package_src))

# Also add the workspace root itself
sys.path.insert(0, str(workspace_root))

project = "haive"
copyright = "2025, William R. Astley"
author = "William R. Astley"
release = "1.0.0"

# -- General configuration ---------------------------------------------------
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
    "sphinx.ext.mathjax",
    "sphinx.ext.todo",
    "sphinx.ext.coverage",
    "sphinx.ext.githubpages",
    "myst_parser",
    "sphinx_copybutton",
    "sphinx_tabs.tabs",
    "sphinx_design",
]

# Autodoc configuration
autodoc_default_options = {
    "members": True,
    "undoc-members": True,
    "show-inheritance": True,
    "member-order": "bysource",
    "private-members": False,  # Don't document private members
    "special-members": "__init__",  # Only document __init__
}

# Mock imports for modules that might not be available during doc build
autodoc_mock_imports = [
    "langchain",
    "langchain_core",
    "langchain_community",
    "langgraph",
    "pydantic",
    "numpy",
    "pandas",
    "torch",
    "tensorflow",
    # Add any other external dependencies that might cause import errors
]

# Autosummary configuration
autosummary_generate = True
autosummary_imported_members = False  # Don't document imported members
autosummary_ignore_module_all = False  # Respect __all__ in modules

# Add this to handle import errors gracefully
autosummary_mock_imports = autodoc_mock_imports

# Napoleon configuration
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = True
napoleon_include_private_with_doc = False
napoleon_use_admonition_for_examples = True
napoleon_use_admonition_for_notes = True
napoleon_use_admonition_for_references = True

# HTML theme configuration
html_theme = "furo"

# HTML static path and custom stylesheet
html_static_path = ["_static"]
html_css_files = ["custom.css"]

# Additional templates path
templates_path = ["_templates"]

# Intersphinx mapping
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "numpy": ("https://numpy.org/doc/stable/", None),
    "pandas": ("https://pandas.pydata.org/docs/", None),
    "pydantic": ("https://docs.pydantic.dev/latest/", None),
    "langchain": ("https://python.langchain.com/docs/", None),
}

# Suppress specific warnings
suppress_warnings = ["autosummary", "autosummary.import_cycle"]

# Add custom error handling
def setup(app):
    """Custom setup to handle import errors gracefully."""
    import logging
    
    # Set up custom logging to capture import errors
    logger = logging.getLogger('sphinx.ext.autosummary')
    logger.setLevel(logging.WARNING)