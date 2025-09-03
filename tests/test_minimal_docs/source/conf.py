"""Minimal Sphinx configuration to test AutoAPI issue."""

# Minimal configuration
project = "Test"
extensions = ["autoapi.extension"]

# AutoAPI settings - just one small test module
autoapi_dirs = ["../test_module"]
autoapi_type = "python"
autoapi_keep_files = True  # Keep intermediate files for debugging

# Minimal theme
html_theme = "alabaster"

# No mocking - let's see what breaks
autodoc_mock_imports = []
