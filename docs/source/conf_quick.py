"""Quick Sphinx configuration to show HTML writing."""
# Basic project info
from __future__ import annotations

project = "Haive AI Agent Framework"
copyright = "2024, Haive Team"
author = "Haive Team"

# Just autodoc - no AutoAPI to speed up
extensions = [
    "sphinx.ext.autodoc",
]

# Basic settings
templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]
html_theme = "alabaster"
html_static_path = ["_static"]

# Mock imports for missing deps
autodoc_mock_imports = [
    "google_search_results",
    "serpapi",
    "langgraph_supervisor",
]

print("✅ Quick Sphinx configuration loaded - should show writing phase!")
