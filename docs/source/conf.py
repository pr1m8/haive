"""Sphinx configuration with fixed AutoAPI for namespace packages."""

import sys
import warnings
from datetime import datetime
from pathlib import Path

# Suppress warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", message=".*Matplotlib.*")

# ==============================================================================
# Project Information
# ==============================================================================

project = "Haive"
author = "William R. Astley"
current_year = datetime.now().year
copyright = f"2025-{current_year}, {author}"
version = "1.0"
release = "1.0.0"

# ==============================================================================
# Path Setup for Namespace Packages - FIXED
# ==============================================================================

# Get paths
conf_dir = Path(__file__).parent.absolute()
docs_dir = conf_dir.parent
workspace_dir = docs_dir.parent
packages_dir = workspace_dir / "packages"

# CRITICAL FIX: Add package roots, not src directories
package_names = [
    "haive-core",
    "haive-agents",
    "haive-tools",
    "haive-games",
    "haive-dataflow",
    "haive-prebuilt",
    "haive-mcp",
]

# Fix sys.path for namespace packages
for package in package_names:
    package_path = packages_dir / package
    if package_path.exists():
        # Add package root so imports work without 'src.'
        sys.path.insert(0, str(package_path))

# ==============================================================================
# Extensions - Focused Configuration
# ==============================================================================

extensions = [
    # Core AutoAPI
    "autoapi.extension",
    
    # Essential Sphinx
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
    
    # Documentation enhancement
    "sphinx_copybutton",
    "sphinx_design",
    "myst_parser",
    "sphinxcontrib.mermaid",
    
    # Examples and galleries
    "sphinx_gallery",
    "sphinx_exec_directive",
]

# ==============================================================================
# AutoAPI Configuration - Optimized for Namespace Packages
# ==============================================================================

autoapi_type = "python"

# Point to src directories
autoapi_dirs = [
    str(packages_dir / package / "src")
    for package in package_names
    if (packages_dir / package / "src").exists()
]

autoapi_root = "api"
autoapi_keep_files = True
autoapi_add_toctree_entry = True

# CRITICAL: Enable namespace package support
autoapi_python_use_implicit_namespaces = True

# Options for better output
autoapi_options = [
    "members",
    "undoc-members",
    "show-inheritance",
    "show-module-summary",
    "special-members",
    "imported-members",
]

# Member ordering
autoapi_member_order = "groupwise"
autoapi_python_class_content = "both"

# Aggressive ignore patterns to reduce errors
autoapi_ignore = [
    # Test files
    "**/test*/**",
    "**/*_test.py",
    "**/test_*.py",
    "**/tests/**",
    "**/testing/**",
    "**/fixtures/**",
    "**/conftest.py",
    
    # Build artifacts
    "**/__pycache__/**",
    "**/build/**",
    "**/dist/**",
    "**/*.egg-info/**",
    "**/.git/**",
    
    # Examples and demos
    "**/examples/**",
    "**/example_*.py",
    "**/demo_*.py",
    "**/demo/**",
    
    # Debug and development files
    "**/debug_*.py",
    "**/debug/**",
    "**/*_debug.py",
    
    # CLI and UI files
    "**/ui.py",
    "**/cli.py",
    "**/main.py",
    "**/app.py",
    "**/run.py",
    
    # Deprecated and experimental
    "**/deprecated/**",
    "**/legacy/**",
    "**/experimental/**",
    "**/archive/**",
    
    # Private modules
    "**/_*.py",
    
    # Specific problematic files
    "**/supervisor/**",
    "**/sequential_planner.py",
    "**/prompt_planning.py",
    "**/graph_checkpointer.py",
    "**/planning_langgraph_entrypoint.py",
    "**/haive_agent_mcp_integration.py",
    "**/compiled_agent.py",
]

# ==============================================================================
# AutoAPI Customization
# ==============================================================================

def fix_module_name(name):
    """Remove src. prefix from module names."""
    if name.startswith("src."):
        return name[4:]
    return name

def prepare_jinja_env(jinja_env):
    """Add custom filters to Jinja environment."""
    jinja_env.filters["fix_module_name"] = fix_module_name
    return jinja_env

autoapi_prepare_jinja_env = prepare_jinja_env

# Skip problematic members
def autoapi_skip_member(app, what, name, obj, skip, options):
    """Skip certain members from documentation."""
    # Skip test-related
    if any(pattern in name.lower() for pattern in ["test_", "_test", "mock", "fixture"]):
        return True
    
    # Skip private members unless explicitly documented
    if name.startswith("_") and not name.startswith("__"):
        if not (hasattr(obj, "docstring") and obj.docstring):
            return True
    
    return skip

# ==============================================================================
# Theme Configuration
# ==============================================================================

html_theme = "furo"
html_title = "Haive Documentation"
html_theme_options = {
    "light_css_variables": {
        "color-brand-primary": "#7C4DFF",
        "color-brand-content": "#6200EA",
        "sidebar-width": "19rem",  # Fixed from 30.5rem
    },
    "dark_css_variables": {
        "color-brand-primary": "#9C27B0",
        "color-brand-content": "#BA68C8",
    },
}

# ==============================================================================
# Other Settings
# ==============================================================================

# Source file handling
source_suffix = {
    ".rst": "restructuredtext",
    ".md": "markdown",
}

# Exclude patterns
exclude_patterns = [
    "_build",
    "Thumbs.db",
    ".DS_Store",
]

# Napoleon settings
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = True

# MyST settings
myst_enable_extensions = [
    "deflist",
    "tasklist",
    "dollarmath",
    "amsmath",
]

# Intersphinx
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "langchain": ("https://python.langchain.com/docs", None),
    "pydantic": ("https://docs.pydantic.dev", None),
}

# ==============================================================================
# Setup
# ==============================================================================

def setup(app):
    """Setup Sphinx application."""
    app.connect("autoapi-skip-member", autoapi_skip_member)