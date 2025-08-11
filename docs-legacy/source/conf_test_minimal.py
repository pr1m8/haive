"""Minimal test configuration to verify AutoAPI paths."""

from pathlib import Path
import os

# Path setup
project_root = Path(__file__).parent.parent.parent
packages_dir = project_root / "packages"

# Project info
project = "Haive Test"
copyright = "2024, Haive Team"
author = "Haive Team"

# Extensions
extensions = [
    "autoapi.extension",
]

# AutoAPI configuration
autoapi_type = "python"
autoapi_dirs = [str(packages_dir / "haive-agents/src")]
autoapi_root = "api"
autoapi_add_toctree_entry = True
autoapi_generate_api_docs = True
autoapi_keep_files = True
autoapi_python_use_implicit_namespaces = False

# Minimal theme
html_theme = "alabaster"

# Exclude patterns
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]