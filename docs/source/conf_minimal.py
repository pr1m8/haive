"""Minimal Sphinx configuration for debugging HTML generation."""
# Basic project info
from __future__ import annotations

project = "Haive AI Agent Framework"
copyright = "2024, Haive Team"
author = "Haive Team"

# Minimal extensions - just the basics
extensions = [
    "sphinx.ext.autodoc",
]

# No AutoAPI for now - just basic HTML generation
templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# Simple HTML theme
html_theme = "alabaster"
html_static_path = ["_static"]

print("✅ Minimal Sphinx configuration loaded!")
