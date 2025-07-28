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
    # Essential Sphinx
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    # Documentation enhancement
    "myst_parser",
    # Examples and galleries
    "sphinx_gallery.gen_gallery",
]

# ==============================================================================
# AutoAPI Configuration - Optimized for Namespace Packages
# ==============================================================================

autoapi_type = "python"

# Point directly to haive namespace directories (skip problematic packages for now)
# Start with just games package to test sphinx_gallery
autoapi_dirs = [
    str(packages_dir / "haive-games" / "src" / "haive"),
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
    "**/startup/**",  # Syntax errors in pitchdeck agent
    "**/scientific_paper_agent/**",  # Syntax errors in nodes
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


# AutoAPI skip function removed - causing event name errors


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
# Sphinx Gallery Configuration
# ==============================================================================

sphinx_gallery_conf = {
    # Specify path to Python files
    'examples_dirs': [
        str(packages_dir / 'haive-games' / 'src' / 'haive' / 'games' / 'chess'),
        str(packages_dir / 'haive-games' / 'src' / 'haive' / 'games' / 'tic_tac_toe'),
    ],
    # Gallery directories in documentation
    'gallery_dirs': ['examples/chess', 'examples/tic_tac_toe'],
    
    # Pattern for files to include in the gallery
    'filename_pattern': r'/example.*\.py$',
    
    # Directory where images should be saved
    'download_all_examples': False,
    
    # Remove config comments from examples
    'remove_config_comments': True,
    
    # Matplotlib settings
    'matplotlib_animations': True,
    'image_scrapers': ('matplotlib',),
    
    # Gallery styling
    'within_subsection_order': 'FileNameSortKey',
    'line_numbers': False,
    'nested_sections': True,
    
    # First cell text
    'first_notebook_cell': (
        "# This example was auto-generated from a Python file\n"
        "# To run: python {0}"
    ),
}

# ==============================================================================
# Setup
# ==============================================================================


def setup(app):
    """Setup Sphinx application."""
    pass

# ==============================================================================
# Sphinx Gallery Configuration - CHESS EXAMPLE
# ==============================================================================

sphinx_gallery_conf = {
    'examples_dirs': [
        str(packages_dir / "haive-games" / "src" / "haive" / "games" / "chess"),
    ],
    'gallery_dirs': ['auto_examples'],
    'filename_pattern': '/example\\.py$',  # Only match example.py
    'plot_gallery': False,  # No plotting for chess
    'download_all_examples': True,
    'show_memory': True,
    'expected_failing_examples': [],
    'min_reported_time': 0,
    'abort_on_example_error': False,
    'reset_modules': ('matplotlib', 'seaborn'),
}
