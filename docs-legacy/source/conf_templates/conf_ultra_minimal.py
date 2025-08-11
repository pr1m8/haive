"""Ultra-minimal configuration to isolate autosummary issue."""

from __future__ import annotations

import os
import sys
from pathlib import Path

# Path setup
project_root = Path(__file__).parent.parent.parent
packages_dir = project_root / "packages"

# =============================================================================
# PROJECT INFORMATION
# =============================================================================

project = "Haive Core Test"
copyright = "2024, Haive Team"
author = "Haive Team"
version = "1.0"
release = "1.0.0"

# =============================================================================
# GENERAL CONFIGURATION
# =============================================================================

templates_path = ["_templates"]
exclude_patterns = [
    "_build", 
    "Thumbs.db", 
    ".DS_Store",
    "packages/*",
    "api_backup/*",
    "**/autosummary/*",
]

# Use simplified index
master_doc = "index_core_only"

# =============================================================================
# MINIMAL EXTENSIONS - NO AUTOAPI
# =============================================================================

extensions = [
    # Core Sphinx only
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    
    # Basic enhancements
    "myst_parser",
]

# Explicitly disable autosummary
autosummary_generate = False

# =============================================================================
# THEME CONFIGURATION - FURO
# =============================================================================

html_theme = "furo"

html_theme_options = {
    "light_css_variables": {
        "color-brand-primary": "#2563eb",
    },
    "dark_css_variables": {
        "color-brand-primary": "#60a5fa",
    },
}

html_static_path = ["_static"]
html_title = "🤖 Haive Test Build"

# =============================================================================
# MYST PARSER
# =============================================================================

myst_enable_extensions = [
    "deflist",
    "tasklist",
]

# =============================================================================
# NAPOLEON (Google-style docstrings)
# =============================================================================

napoleon_google_docstring = True
napoleon_numpy_docstring = False