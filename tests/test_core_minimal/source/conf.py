"""Minimal config for testing haive-core only."""

project = "Haive Core Test"

# Minimal extensions
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "autoapi.extension",
]

# Just haive-core
autoapi_dirs = ["../../packages/haive-core/src"]
autoapi_type = "python"
autoapi_keep_files = True
autoapi_options = ["members", "show-inheritance"]

# Minimal mocking
autodoc_mock_imports = [
    "langchain",
    "langchain_core",
    "langgraph",
    "pydantic",
]

# Basic theme
html_theme = "alabaster"

# Suppress warnings
suppress_warnings = ["autoapi"]
