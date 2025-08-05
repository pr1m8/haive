"""Minimal Sphinx configuration for basic HTML generation."""

import os
import sys
from pathlib import Path

# Basic project information
project = "Haive"
copyright = "2025, Haive Team"
author = "Haive Team"
version = "1.0.0"
release = "1.0.0"

# Basic extensions only
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.viewcode",
    "sphinx.ext.napoleon",
    "sphinx.ext.intersphinx",
    "sphinx.ext.todo",
]

# HTML output
html_theme = "furo"
html_title = f"{project} Documentation"

# Basic paths
templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# Master document
master_doc = "index"

# Source suffix
source_suffix = {
    ".rst": None,
    ".md": "markdown",
}

# Language
language = "en"

# HTML theme options
html_theme_options = {
    "sidebar_hide_name": False,
    "navigation_with_keys": True,
}

# Static files
html_static_path = ["_static"]

# Output file base name for HTML help builder
htmlhelp_basename = "Haivedoc"

# Intersphinx mapping
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
}
