"""Simplified Sphinx configuration for Haive documentation.

This is a clean, minimal configuration that focuses on essentials. To
use this, copy it to docs/source/conf.py.
"""

from __future__ import annotations

import sys
from datetime import datetime
from pathlib import Path

# ==============================================================================
# Path Setup
# ==============================================================================

# Get paths
docs_dir = Path(__file__).parent.parent
workspace_dir = docs_dir.parent
packages_dir = workspace_dir / "packages"

# Add package source paths for imports
for package in [
    "haive-core",
    "haive-agents",
    "haive-tools",
    "haive-games",
    "haive-mcp",
    "haive-dataflow",
]:
    src_path = packages_dir / package / "src"
    if src_path.exists():
        sys.path.insert(0, str(src_path))

# ==============================================================================
# Project Information
# ==============================================================================

project = "Haive"
author = "William R. Astley"
copyright = f"{datetime.now().year}, {author}"
version = "1.0"
release = "1.0.0"

# ==============================================================================
# General Configuration
# ==============================================================================

extensions = [
    # Core Sphinx
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
    "sphinx.ext.todo",
    # Enhanced features
    "sphinx_copybutton",
    "sphinx_design",
    "myst_parser",
    # API documentation
    "sphinx_autodoc_typehints",
]

# File types
source_suffix = {
    ".rst": "restructuredtext",
    ".md": "markdown",
}

# Exclude patterns
exclude_patterns = [
    "_build",
    "Thumbs.db",
    ".DS_Store",
    "**/.git",
    "**/__pycache__",
    "**/test_*.py",
    "**/tests/**",
]

# ==============================================================================
# HTML Output
# ==============================================================================

html_theme = "furo"
html_title = "Haive Documentation"
html_static_path = ["_static"]
html_css_files = ["custom.css"]

# Furo theme options
html_theme_options = {
    "sidebar_hide_name": False,
    "navigation_with_keys": True,
    "light_css_variables": {
        "color-brand-primary": "#0066cc",
        "color-brand-content": "#0066cc",
        "font-stack": "system-ui, -apple-system, sans-serif",
        "font-stack--monospace": "'JetBrains Mono', Consolas, monospace",
    },
}

# ==============================================================================
# Extension Configuration
# ==============================================================================

# Napoleon - Google docstrings
napoleon_google_docstring = True
napoleon_numpy_docstring = False
napoleon_include_init_with_doc = True

# Autodoc
autodoc_member_order = "bysource"
autodoc_typehints = "description"
autodoc_default_options = {
    "members": True,
    "show-inheritance": True,
}

# Type hints
typehints_document_rtype = True
always_document_param_types = True

# MyST Parser
myst_enable_extensions = [
    "deflist",
    "tasklist",
    "colon_fence",
]

# Intersphinx
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "langchain": ("https://python.langchain.com/", None),
    "pydantic": ("https://docs.pydantic.dev/", None),
}

# Todo extension
todo_include_todos = True

# ==============================================================================
# Custom Setup
# ==============================================================================


def setup(app):
    """Add custom configuration."""
    app.add_css_file("custom.css", priority=500)

    return {
        "version": "1.0",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
