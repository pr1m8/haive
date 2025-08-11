"""Working Sphinx configuration that generates HTML."""

# Basic project info
from __future__ import annotations

project = "Haive AI Agent Framework"
copyright = "2024, Haive Team"
author = "Haive Team"
version = "1.0"
release = "1.0.0"

# Working extensions
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "autoapi.extension",
    "myst_parser",  # For markdown support
]

# AutoAPI configuration - just core package
autoapi_type = "python"
autoapi_dirs = ["../../packages/haive-core/src"]
autoapi_root = "api"
autoapi_add_toctree_entry = True
autoapi_generate_api_docs = True
autoapi_keep_files = True

# Skip problematic files
autoapi_ignore = [
    "**/test*.py",
    "**/tests/**/*.py",
    "**/examples/**/*.py",
    "**/example*.py",
    "**/demo*.py",
    "**/app.py",
    "**/*_test.py",
    "**/*_demo.py",
]

# Mock imports for missing dependencies
autodoc_mock_imports = [
    "google_search_results",
    "serpapi",
    "agents",
    "langgraph_supervisor",
    "compiled_state_graph",
    "agent_types",
    "complex_rag",
]

# File patterns to exclude from source
exclude_patterns = [
    "_build",
    "Thumbs.db",
    ".DS_Store",
    "**/*.md",  # Exclude markdown files from autosummary
    "logs/*",
    "archive/*",
]

# HTML theme and output
html_theme = "alabaster"
html_static_path = ["_static"]
templates_path = ["_templates"]

# Disable autosummary for now to avoid errors
autosummary_generate = False

# MyST for markdown support
myst_enable_extensions = [
    "colon_fence",
    "deflist",
    "dollarmath",
]

print("✅ Working Sphinx configuration loaded!")
