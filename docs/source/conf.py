# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
import os
import sys

sys.path.insert(0, os.path.abspath("../../src"))


project = "haive"
copyright = "2025, William R. Astley"
author = "William R. Astley"
release = "1.0.0"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration
# Extensions configuration
extensions = [
    "sphinx.ext.autodoc",  # Core docstring documentation
    "sphinx.ext.autosummary",  # Generate summary tables
    "sphinx.ext.napoleon",  # Support for Google/NumPy docstring format
    "sphinx.ext.viewcode",  # Add links to source code
    "sphinx.ext.intersphinx",  # Link to other projects' documentation
    "sphinx.ext.mathjax",  # Math support
    "sphinx.ext.todo",  # Support for TODO items
    "sphinx.ext.coverage",  # Check documentation coverage
    "sphinx.ext.githubpages",  # GitHub Pages support
    "myst_parser",  # Markdown support
    "sphinx_copybutton",  # Add copy button to code blocks
    "sphinx_tabs.tabs",  # Add tabbed content
    "sphinx_press_theme",  # Press theme
    "sphinx_design",  # Grid layout, cards, dropdowns, and more
]

# Autodoc configuration
autodoc_default_options = {
    "members": True,
    "undoc-members": True,
    "show-inheritance": True,
    "member-order": "bysource",
}

# Autosummary configuration
autosummary_generate = True
autosummary_imported_members = True

# Napoleon configuration (Google-style docstrings)
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = True
napoleon_include_private_with_doc = False
napoleon_use_admonition_for_examples = True
napoleon_use_admonition_for_notes = True
napoleon_use_admonition_for_references = True

# HTML theme configuration
html_theme = "sphinx_press_theme"  # Modern VuePress-like theme
# Alternative modern themes: 'furo', 'pydata_sphinx_theme', 'sphinx_rtd_theme'

# HTML theme options
html_theme_options = {
    # Press theme options
}

# HTML static path and custom stylesheet
html_static_path = ["_static"]
html_css_files = ["custom.css"]

# Additional templates path
templates_path = ["_templates"]

# Intersphinx mapping for linking to other projects
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "numpy": ("https://numpy.org/doc/stable/", None),
    "pandas": ("https://pandas.pydata.org/docs/", None),
}
