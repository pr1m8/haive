"""Sphinx configuration for haive documentation."""

import os
import sys

from sphinx.application import Sphinx

# Path setup
sys.path.insert(0, os.path.abspath("../../src"))

# -- Project information -----------------------------------------------------
project = "haive"
copyright = "2025, Haive Team"
author = "Haive Team"
release = "0.1.0"

# -- General configuration ---------------------------------------------------
extensions = [
    # "autoapi.extension",  # Disabled - causing build issues
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
    "sphinx_copybutton",
    "sphinx_design",
    "sphinxcontrib.mermaid",
    "sphinx.ext.graphviz",
]

# AutoAPI Configuration - Disabled for now
# autoapi_dirs = ["../../src"]
# autoapi_type = "python"
# autoapi_add_toctree_entry = True
# autoapi_keep_files = True
# autoapi_root = "autoapi"
# autoapi_include_inheritance_diagram = False
# autoapi_options = [
#     "members",
#     "undoc-members",
#     "show-inheritance",
#     "show-module-summary",
#     "imported-members",
#     "special-members",
# ]
#
# # CRITICAL: Use module-level pages for hierarchical organization
# autoapi_own_page_level = "module"
# autoapi_member_order = "groupwise"

# -- Options for HTML output -------------------------------------------------
html_theme = "furo"
html_static_path = ["_static"]

# Furo theme configuration - Enhanced purple theme
html_theme_options = {
    "navigation_with_keys": True,
    "show_nav_level": 3,
    "collapse_navigation": False,
    "sidebar_hide_name": False,
    "navigation_depth": 4,
    "show_toc_level": 3,
    "light_css_variables": {
        "color-brand-primary": "#8b5cf6",
        "color-brand-content": "#7c3aed",
        "color-sidebar-background": "#faf5ff",
        "color-sidebar-background-border": "#e9d5ff",
    },
    "dark_css_variables": {
        "color-brand-primary": "#a78bfa",
        "color-brand-content": "#c084fc",
        "color-background-primary": "#0f0019",  # Very dark purple
        "color-background-secondary": "#1a0033",  # Dark purple
        "color-background-hover": "#2d0059",  # Purple hover
        "color-background-border": "#4c1d95",  # Purple border
        "color-sidebar-background": "#14001f",  # Darker purple sidebar
        "color-sidebar-background-border": "#4c1d95",
        "color-sidebar-link-text": "#e9d5ff",
        "color-sidebar-link-text--top-level": "#f3e8ff",
        "color-sidebar-item-background--hover": "#2d0059",
        "color-sidebar-item-expander-background--hover": "#4c1d95",
        "color-content-foreground": "#ffffff",
        "color-code-background": "#1e0936",  # Dark purple code bg
    },
}

# Napoleon settings
napoleon_google_docstring = True
napoleon_numpy_docstring = True

# Intersphinx
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "sphinx": ("https://www.sphinx-doc.org/en/master", None),
}

# -- Purple Theme Configuration ----------------------------------------------
# Syntax highlighting - use purple-friendly themes
pygments_style = "default"  # Better for light mode with our custom CSS
pygments_dark_style = "monokai"  # Good for dark mode

# AutoAPI configuration for prominent API Reference - Disabled
# autoapi_add_toctree_entry = True
# autoapi_toctree_caption = "🔍 API Reference"
# autoapi_toctree_first = True  # Put at top!

# Graphviz configuration for beautiful diagrams
graphviz_output_format = "svg"
graphviz_dot_args = [
    "-Kdot",
    "-Tsvg",
    "-Gfontname=Inter",
    "-Nfontname=Inter",
    "-Efontname=Inter",
    "-Gbgcolor=transparent",
    "-Gpad=0.5",
    "-Grankdir=TB",
    "-Gnodesep=0.7",
    "-Granksep=0.8",
    "-Gsplines=true",
]

# Simplified - using Furo's built-in theme + tippy for tooltips
html_css_files = [
    "tippy-enhancements.css",  # Keep tooltip enhancements only
]
