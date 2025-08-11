"""Minimal AutoAPI test configuration."""

project = "Haive Test"
copyright = "2024, Haive Team"
author = "Haive Team"
version = "1.0"
release = "1.0.0"

# Minimal extensions - only AutoAPI
extensions = [
    "autoapi.extension",
]

# AutoAPI configuration - just core package
autoapi_type = "python"
autoapi_dirs = ["../../packages/haive-core/src"]  # Corrected path
autoapi_root = "api"
autoapi_add_toctree_entry = True
autoapi_generate_api_docs = True
autoapi_keep_files = True

# Minimal ignore patterns
autoapi_ignore = [
    "**/test*.py",
    "**/tests/**/*.py",
    "**/examples/**/*.py",
]

# No mock imports to test
autodoc_mock_imports = []

# Basic settings
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]
html_theme = "alabaster"
templates_path = ["_templates"]
html_static_path = ["_static"]

print("✅ Minimal AutoAPI test configuration loaded!")
print(f"📦 AutoAPI dirs: {autoapi_dirs}")
print(f"🎯 AutoAPI root: {autoapi_root}")