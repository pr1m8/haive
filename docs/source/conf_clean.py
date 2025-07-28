"""Clean Sphinx configuration for Haive - Working WITH Furo theme."""

import sys
import warnings
from pathlib import Path

# Suppress warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

# ==============================================================================
# Path Setup for Namespaced Monorepo
# ==============================================================================

conf_dir = Path(__file__).parent.absolute()
docs_dir = conf_dir.parent
workspace_dir = docs_dir.parent
packages_dir = workspace_dir / "packages"

# Add src directories to Python path for correct imports
package_names = [
    "haive-core",
    "haive-agents",
    "haive-tools",
    "haive-games",
    "haive-dataflow",
    "haive-mcp",
]

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
    
    # AutoAPI for automatic documentation
    "autoapi.extension",
]

# ==============================================================================
# AutoAPI Configuration - Optimized for Namespace Packages
# ==============================================================================

autoapi_type = "python"

# Point to haive namespace directories (not src)
autoapi_dirs = [
    str(packages_dir / "haive-core" / "src" / "haive"),
    str(packages_dir / "haive-agents" / "src" / "haive"),
    str(packages_dir / "haive-tools" / "src" / "haive"),
    str(packages_dir / "haive-games" / "src" / "haive"),
]

# Enable PEP 420 namespace package support
autoapi_python_use_implicit_namespaces = True

# Output location
autoapi_root = "api"
autoapi_add_toctree_entry = True

# Aggressive ignore patterns to reduce processing
autoapi_ignore = [
    # Test files
    "**/test_*",
    "**/tests/**",
    "**/*_test.py",
    "**/testing/**",
    
    # Examples and demos
    "**/examples/**",
    "**/example_*.py",
    "**/demo*.py",
    "**/*_demo.py",
    "**/*_example.py",
    
    # Development files
    "**/scripts/**",
    "**/.ipynb_checkpoints/**",
    "**/archive/**",
    "**/old/**",
    "**/deprecated/**",
    "**/debug*.py",
    "**/cli.py",
    
    # Specific problematic directories
    "**/supervisor/**",  # Too many experimental files
    "**/conversation/examples/**",
    "**/planning/examples/**",
]

# AutoAPI options
autoapi_options = [
    "members",
    "show-inheritance",
    "show-module-summary",
]

# Keep generated files for debugging
autoapi_keep_files = True

# ==============================================================================
# Furo Theme Configuration - Working WITH the Theme
# ==============================================================================

html_theme = "furo"
html_title = "🤖 Haive AI Agent Framework"

# Static files
html_static_path = ["_static"]

# Minimal CSS - just one clean override file
html_css_files = [
    "furo-custom.css",  # Our minimal customizations
]

# Furo theme options - using documented configuration
html_theme_options = {
    # Sidebar configuration
    "sidebar_hide_name": False,
    "navigation_with_keys": True,
    
    # Top navigation
    "top_of_page_buttons": ["edit"],
    
    # CSS Variables - Working with Furo's system
    "light_css_variables": {
        # Brand colors
        "color-brand-primary": "#007acc",
        "color-brand-content": "#0066cc",
        
        # Sidebar colors
        "color-sidebar-background": "#f8f9fb",
        "color-sidebar-background-border": "#eeebee",
        "color-sidebar-link-text": "#333333",
        "color-sidebar-link-text--top-level": "#0066cc",
        "color-sidebar-search-background": "#ffffff",
        
        # Content colors
        "color-content-foreground": "#333333",
        "color-background-primary": "#ffffff",
        "color-background-secondary": "#f8f9fb",
        
        # Code colors
        "color-code-background": "#f8f8f8",
        "color-code-foreground": "#333333",
        
        # Admonition colors
        "color-admonition-background": "#f0f7ff",
    },
    
    # Dark mode support
    "dark_css_variables": {
        "color-brand-primary": "#4db8ff",
        "color-brand-content": "#66ccff",
        "color-sidebar-background": "#131416",
        "color-code-background": "#1e1e1e",
    },
}

# ==============================================================================
# Other Sphinx Configuration
# ==============================================================================

# Source file parsing
source_suffix = {
    ".rst": "restructuredtext",
    ".md": "markdown",
}

# Master document
master_doc = "index"

# Patterns to exclude
exclude_patterns = [
    "_build",
    "**/__pycache__",
    "**/test_*.py",
    "**/tests/**",
    "Thumbs.db",
    ".DS_Store",
]

# MyST configuration for Markdown
myst_enable_extensions = [
    "colon_fence",
    "deflist",
    "html_image",
]

# Intersphinx for cross-references
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "sphinx": ("https://www.sphinx-doc.org/en/master/", None),
}

# Napoleon settings for Google-style docstrings
napoleon_google_docstring = True
napoleon_numpy_docstring = False
napoleon_include_init_with_doc = True
napoleon_include_private_with_doc = False

# ==============================================================================
# Setup Function
# ==============================================================================

def setup(app):
    """Application setup hook."""
    # Only connect AutoAPI events if extension is loaded
    if "autoapi.extension" in app.config.extensions:
        app.connect("autoapi-skip-member", skip_member_handler)
    
    return {
        "version": "1.0",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }

def skip_member_handler(app, what, name, obj, skip, options):
    """Skip certain members from documentation."""
    # Skip test-related items
    if any(pattern in name for pattern in ["test_", "_test", "Test"]):
        return True
    
    # Skip private members unless explicitly included
    if name.startswith("_") and not name.startswith("__"):
        return True
    
    return skip