"""Fixed Sphinx configuration for Haive documentation."""

import logging
import sys
import warnings
from datetime import datetime
from pathlib import Path

# Set up logging
logger = logging.getLogger(__name__)

# Suppress warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", message=".*Matplotlib.*")
warnings.filterwarnings("ignore", category=UserWarning, module="sphinx")

# ==============================================================================
# Path Setup
# ==============================================================================

conf_dir = Path(__file__).parent.absolute()
docs_dir = conf_dir.parent
workspace_dir = docs_dir.parent

# Add package paths to sys.path WITHOUT importing them
packages_dir = workspace_dir / "packages"
package_names = [
    "haive-core",
    "haive-agents", 
    "haive-tools",
    "haive-games",
    "haive-dataflow",
    "haive-mcp",
]

# Add src directories to path but DON'T import
for package in package_names:
    src_path = packages_dir / package / "src"
    if src_path.exists():
        sys.path.insert(0, str(src_path))

# ==============================================================================
# Project Information
# ==============================================================================

project = "Haive"
author = "William R. Astley"
copyright = f"2025, {author}"
version = "1.0"
release = "1.0.0"

# ==============================================================================
# Extensions
# ==============================================================================

extensions = [
    # Core documentation
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
    "sphinx.ext.autodoc",
    
    # Enhanced content
    "sphinx_design",
    "sphinx_copybutton",
    "myst_parser",
    
    # AutoAPI - with FIXED configuration
    "autoapi.extension",
]

# ==============================================================================
# AutoAPI Configuration - FIXED for namespaced monorepo
# ==============================================================================

autoapi_type = "python"

# Point to src directories, NOT the namespace directories
autoapi_dirs = [
    str(packages_dir / "haive-core" / "src"),
    str(packages_dir / "haive-agents" / "src"),
    str(packages_dir / "haive-tools" / "src"),
    str(packages_dir / "haive-games" / "src"),
    str(packages_dir / "haive-dataflow" / "src"),
    str(packages_dir / "haive-mcp" / "src"),
]

autoapi_root = "api"
autoapi_ignore = [
    "**/test_*",
    "**/tests/*",
    "**/*_test.py",
    "**/examples/*",
    "**/scripts/*",
]

autoapi_options = [
    "members",
    "show-inheritance",
    "show-module-summary",
]

# This is KEY - tells AutoAPI to handle namespace packages correctly
autoapi_python_use_implicit_namespaces = True

# ==============================================================================
# Theme Configuration
# ==============================================================================

html_theme = "furo"
html_title = "🤖 Haive AI Agent Framework"
html_static_path = ["_static"]

# CSS files
html_css_files = [
    "haive-minimal.css",
    "haive-css-fixes.css",
]

# Theme options - SIMPLIFIED without duplicates
html_theme_options = {
    "sidebar_hide_name": False,
    "navigation_with_keys": True,
    "light_css_variables": {
        "sidebar-width": "18rem",  # Fixed width
        "content-width": "50rem",
        "color-brand-primary": "#0066cc",
    },
}

# ==============================================================================
# Other Settings
# ==============================================================================

source_suffix = {
    ".rst": "restructuredtext",
    ".md": "markdown",
}

exclude_patterns = [
    "_build",
    "**/__pycache__",
    "**/test_*.py",
    "**/tests/**",
]

# Disable nitpicky mode during development
nitpicky = False

# ==============================================================================
# Setup Function - FIXED
# ==============================================================================

def setup(app):
    """Setup function - only connect valid events."""
    # Only connect to autoapi events if autoapi is loaded
    if "autoapi.extension" in app.config.extensions:
        app.connect("autoapi-skip-member", autoapi_skip_member)
    
    return {
        "version": "1.0",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }

def autoapi_skip_member(app, what, name, obj, skip, options):
    """Skip test files and problematic modules."""
    if "test_" in name or "_test" in name:
        return True
    if any(pattern in name.lower() for pattern in ["demo", "example", "debug"]):
        return True
    return skip