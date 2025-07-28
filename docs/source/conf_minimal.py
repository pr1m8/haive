"""Minimal Sphinx configuration for testing CSS fixes."""

# Project information
project = "Haive"
author = "William R. Astley"
copyright = "2025, William R. Astley"

# Extensions
extensions = [
    "sphinx_design",
    "myst_parser",
]

# Theme
html_theme = "furo"
html_title = "🤖 Haive AI Agent Framework"

# Static files
html_static_path = ["_static"]

# CSS files
html_css_files = [
    "haive-minimal.css",
    "haive-css-fixes.css",
]

# Source suffix
source_suffix = {
    ".rst": "restructuredtext",
    ".md": "markdown",
}

# Master doc
master_doc = "index"