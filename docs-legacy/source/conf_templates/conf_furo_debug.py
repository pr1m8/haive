"""Minimal Furo debug configuration"""

project = "Furo Debug Test"
copyright = "2024, Test"
author = "Test"

# Minimal extensions
extensions = [
    "autoapi.extension",
]

# Furo theme
html_theme = "furo"

# Minimal AutoAPI
autoapi_type = "python"
autoapi_dirs = ["../../packages/haive-core/src"]
autoapi_root = "api"
autoapi_add_toctree_entry = True
autoapi_generate_api_docs = True
autoapi_keep_files = False

# Minimal ignore patterns
autoapi_ignore = [
    "**/test*.py",
    "**/tests/**/*.py",
]

# Essential mock imports only
autodoc_mock_imports = [
    "langchain_core",
    "langchain_community",
    "pydantic",
]

# Basic settings
exclude_patterns = ["_build"]
templates_path = ["_templates"]
html_static_path = ["_static"]

print("🔧 Minimal Furo debug configuration loaded")