# Minimal Sphinx configuration for basic HTML generation
import os
import sys

# Add source path
sys.path.insert(0, os.path.abspath("."))

# Project information
project = "Haive"
copyright = "2025, Haive Team"
author = "Haive Team"
version = "1.0.0"
release = "1.0.0"

# Basic extensions
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "myst_parser",
]

# HTML theme
html_theme = "furo"
html_title = "Haive Documentation"

# Source files
source_suffix = {
    ".rst": None,
    ".md": "myst_parser",
}

# Basic HTML options
html_static_path = ["_static"]
templates_path = ["_templates"]

# Exclude problematic patterns
exclude_patterns = [
    "_build",
    "Thumbs.db",
    ".DS_Store",
    "**/conversation/*.rst",  # Has broken literalinclude
    "enhanced_features_demo.rst",
    "agents/demos/index.rst",  # Has unknown grid directives
]

# MyST configuration
myst_enable_extensions = [
    "colon_fence",
    "deflist",
]

# Suppress warnings for now
suppress_warnings = ["image.nonlocal_uri"]
