"""Organized Sphinx configuration with proper package structure."""

from __future__ import annotations

project = "Haive AI Agent Framework"
copyright = "2024, Haive Team"
author = "Haive Team"
version = "1.0"
release = "1.0.0"

# General configuration
templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store", "**/*.md"]
pygments_style = "sphinx"

# Working extensions only
extensions = [
    # Core Sphinx extensions
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.doctest",
    "sphinx.ext.intersphinx",
    "sphinx.ext.todo",
    "sphinx.ext.coverage",
    "sphinx.ext.mathjax",
    "sphinx.ext.viewcode",
    "sphinx.ext.napoleon",
    "sphinx.ext.graphviz",
    # AutoAPI for automatic documentation
    "autoapi.extension",
    # Markdown support
    "myst_parser",
    # Enhanced features (tested)
    "sphinx_copybutton",
    "sphinx_design",
    "sphinxcontrib.mermaid",
]

# AutoAPI Configuration - Process packages separately for better organization
autoapi_type = "python"
autoapi_dirs = [
    "../../packages/haive-core/src",
    "../../packages/haive-agents/src",
    "../../packages/haive-tools/src",
    "../../packages/haive-games/src",
    "../../packages/haive-dataflow/src",
    "../../packages/haive-mcp/src",
    "../../packages/haive-prebuilt/src",
]

# AutoAPI settings for better organization
autoapi_root = "api"
autoapi_add_toctree_entry = False  # We'll manage TOC manually
autoapi_keep_files = True
autoapi_generate_api_docs = True
autoapi_python_class_content = "both"
autoapi_member_order = "bysource"
autoapi_template_dir = "_templates/autoapi"  # Custom templates for better structure

# Tell AutoAPI to use proper module names
autoapi_options = [
    "members",
    "undoc-members",
    "show-inheritance",
    "show-module-summary",
    "imported-members",
]

# Skip problematic files
autoapi_ignore = [
    "**/examples/**/*.py",
    "**/test*.py",
    "**/tests/**/*.py",
    "**/app.py",
]

# Mock imports
autodoc_mock_imports = [
    "google_search_results",
    "serpapi",
    "agents",
    "langgraph_supervisor",
]

# HTML theme configuration
html_theme = "furo"
html_title = f"{project} Documentation"
html_short_title = "Haive Docs"

html_theme_options = {
    "source_repository": "https://github.com/yourusername/haive/",
    "source_branch": "main",
    "navigation_depth": 4,  # Show deeper navigation
    "collapse_navigation": False,  # Don't collapse by default
}

html_static_path = ["_static"]

# MyST configuration
myst_enable_extensions = [
    "colon_fence",
    "deflist",
    "html_admonition",
    "html_image",
    "linkify",
    "replacements",
    "smartquotes",
    "substitution",
]

# Autodoc configuration
autodoc_default_options = {
    "members": True,
    "member-order": "bysource",
    "special-members": "__init__",
    "undoc-members": True,
    "exclude-members": "__weakref__",
}

autodoc_typehints = "description"
autosummary_generate = False

# Intersphinx mapping
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "pydantic": ("https://docs.pydantic.dev/latest/", None),
}

# Napoleon settings
napoleon_google_docstring = True
napoleon_numpy_docstring = True

# Suppress warnings
suppress_warnings = ["ref.python", "autosummary", "autoapi"]


# Custom AutoAPI processing
def autoapi_prepare_jinja_env(jinja_env):
    """Customize AutoAPI template environment."""
    # Add custom filters or functions if needed


def setup(app):
    """Setup Sphinx application."""
    app.connect("autoapi-prepare-jinja-env", autoapi_prepare_jinja_env)


print("✅ Organized Sphinx configuration loaded!")
print("🔧 AutoAPI configured with better package organization")
