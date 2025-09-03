"""Furo configuration for haive-core ONLY - avoiding agent documentation issues."""

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

project = "Haive Core Documentation"
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
    "packages/*",  # Exclude ALL package docs
    "api_backup/*",  # Exclude backup directory
    "api_backup/**/*",  # Exclude everything in backup
    "api/haive/agents/*",  # Exclude agent API docs specifically
    "api/agent*",  # Exclude ANY agent references
    "api/agents/*",  # Exclude agents directory
    "api/**/agent*",  # Exclude agent references at any level
    "api/**/*agent*",  # Exclude anything with agent in name
    "**/autosummary/*",  # Exclude any autosummary directories
    "index.rst",   # Exclude main index
]

# Use simplified index
master_doc = "index_furo_clean"

# =============================================================================
# MINIMAL EXTENSIONS - CORE FUNCTIONALITY ONLY
# =============================================================================

extensions = [
    # CRITICAL: AutoAPI MUST BE FIRST
    "autoapi.extension",
    
    # Core Sphinx extensions only
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode", 
    "sphinx.ext.intersphinx",
    
    # Basic enhancements
    "sphinx_copybutton",
    "myst_parser",
]

# =============================================================================
# AUTOAPI CONFIGURATION - HAIVE-CORE ONLY
# =============================================================================

# Force haive-core only
autoapi_dirs = [str(packages_dir / "haive-core/src")]

# Add to Python path for imports
sys.path.insert(0, str(packages_dir / "haive-core/src"))

print(f"📁 AutoAPI directory: {autoapi_dirs[0]}")
print(f"🎯 Building ONLY haive-core documentation")

# AutoAPI settings
autoapi_root = "api"
autoapi_add_toctree_entry = False
autoapi_generate_api_docs = True
autoapi_python_class_content = "both"
autoapi_member_order = "bysource"
autoapi_keep_files = True

# Use simple templates without autosummary
autoapi_template_dir = "_templates/autoapi_simple"

# Minimal options
autoapi_options = [
    "members",
    "undoc-members", 
    "show-inheritance",
]

# Ignore patterns - EXCLUDE agent references
autoapi_ignore = [
    "*/test_*.py",
    "*/tests/*",
    "*_test.py",
    "*/conftest.py",
    "*/examples/*",
    "*/example_*.py",
    "*_example.py",
    "*_demo.py",
    "*/__pycache__/*",
    "*.pyc",
    # Specifically ignore any agent-related imports in core
    "*/agent*",
    "*agent*.py",
]

# Suppress warnings
suppress_warnings = [
    "autoapi.python_import_resolution",
    "autosummary",
]

# Explicitly disable autosummary
autosummary_generate = False
autosummary_imported_members = False

# =============================================================================
# THEME CONFIGURATION - FURO
# =============================================================================

html_theme = "furo"

html_theme_options = {
    "light_css_variables": {
        "color-brand-primary": "#2563eb",
        "color-brand-content": "#2563eb",
        "color-admonition-background": "#f8fafc",
    },
    "dark_css_variables": {
        "color-brand-primary": "#60a5fa",
        "color-brand-content": "#60a5fa",
    },
    "sidebar_hide_name": False,
    "navigation_with_keys": True,
    "top_of_page_buttons": ["view", "edit"],
    "source_repository": "https://github.com/will-astley/haive",
    "source_branch": "main",
    "source_directory": "docs/source/",
    "navigation_depth": 4,
    "collapse_navigation": False,
}

html_static_path = ["_static"]
html_title = "🤖 Haive Core Documentation"

# =============================================================================
# MYST PARSER
# =============================================================================

myst_enable_extensions = [
    "deflist",
    "tasklist",
    "html_image",
    "colon_fence",
    "smartquotes",
    "substitution",
]

# =============================================================================
# INTERSPHINX
# =============================================================================

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "pydantic": ("https://docs.pydantic.dev", None),
}

# =============================================================================
# NAPOLEON (Google-style docstrings)
# =============================================================================

napoleon_google_docstring = True
napoleon_numpy_docstring = False
napoleon_include_init_with_doc = True
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = True
napoleon_use_admonition_for_notes = True
napoleon_use_admonition_for_references = False
napoleon_use_ivar = False
napoleon_use_param = True
napoleon_use_rtype = True
napoleon_preprocess_types = True

# HTML output options
html_show_sourcelink = True
html_copy_source = True