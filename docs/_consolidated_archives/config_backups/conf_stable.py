"""Stable Sphinx configuration with working extensions and all packages."""

from __future__ import annotations

import sys
from pathlib import Path

# Add conf_modules to Python path for imports
conf_modules_dir = Path(__file__).parent / "conf_modules"
sys.path.insert(0, str(conf_modules_dir))

# =============================================================================
# PROJECT INFORMATION
# =============================================================================

project = "Haive AI Agent Framework"
copyright = "2024, Haive Team"
author = "Haive Team"
version = "1.0"
release = "1.0.0"

# =============================================================================
# GENERAL CONFIGURATION
# =============================================================================

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store", "**/*.md"]
pygments_style = "sphinx"

# =============================================================================
# STABLE EXTENSIONS - Tested and working
# =============================================================================

extensions = [
    # Core Sphinx extensions
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.doctest",
    "sphinx.ext.intersphinx",
    "sphinx.ext.todo",
    "sphinx.ext.coverage",
    "sphinx.ext.mathjax",
    "sphinx.ext.ifconfig",
    "sphinx.ext.viewcode",
    "sphinx.ext.githubpages",
    "sphinx.ext.napoleon",
    "sphinx.ext.inheritance_diagram",
    "sphinx.ext.graphviz",
    # AutoAPI for automatic documentation
    "autoapi.extension",
    # Markdown support
    "myst_parser",
    # Theme
    "furo",
    # Enhanced features
    "sphinx_copybutton",
    "sphinx_design",
    "sphinxcontrib.mermaid",
    "sphinx_togglebutton",
    "sphinx_tabs.tabs",
]

# =============================================================================
# AUTOAPI CONFIGURATION - ALL PACKAGES
# =============================================================================

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

autoapi_root = "api"
autoapi_add_toctree_entry = True
autoapi_generate_api_docs = True
autoapi_python_class_content = "both"
autoapi_member_order = "bysource"
autoapi_options = [
    "members",
    "undoc-members",
    "show-inheritance",
    "show-module-summary",
    "special-members",
    "imported-members",
]

# Skip patterns to avoid problematic files
autoapi_ignore = [
    "**/examples/**/*.py",
    "**/example*.py",
    "**/*example*.py",
    "**/demos/**/*.py",
    "**/demo*.py",
    "**/test*.py",
    "**/tests/**/*.py",
    "**/app.py",
    "**/app/**/*.py",
]

# Mock imports for missing dependencies
autodoc_mock_imports = [
    "google_search_results",
    "google-search-results",
    "serpapi",
    "agents",
    "langgraph_supervisor",
    "compiled_state_graph",
    "agent_types",
    "complex_rag",
    "usage_examples",
    "normalize_contents",
    "map_branch",
    "llm_compiler",
    "plan_and_execute",
    "web_nav",
    "SolvabilityStatus",
    "SimpleAgentConfig",
    "tool",
    "task_analysis",
    "react_agent2",
    "from_llms",
    "models",
    "base",
    "WebSource",
    "LocalSource",
    "TypeConverter",
    "Config",
]

# =============================================================================
# HTML THEME CONFIGURATION
# =============================================================================

html_theme = "furo"
html_title = f"{project} Documentation"
html_short_title = "Haive Docs"

html_theme_options = {
    "source_repository": "https://github.com/yourusername/haive/",
    "source_branch": "main",
    "source_directory": "docs/source/",
    "sidebar_hide_name": True,
    "light_css_variables": {
        "color-brand-primary": "#2563eb",
        "color-brand-content": "#2563eb",
    },
    "dark_css_variables": {
        "color-brand-primary": "#3b82f6",
        "color-brand-content": "#3b82f6",
    },
}

html_static_path = ["_static"]
html_css_files = [
    "custom.css",
    "enhanced-docs.css",
]
html_js_files = ["custom.js"]

# =============================================================================
# MYST CONFIGURATION
# =============================================================================

myst_enable_extensions = [
    "amsmath",
    "colon_fence",
    "deflist",
    "dollarmath",
    "fieldlist",
    "html_admonition",
    "html_image",
    "linkify",
    "replacements",
    "smartquotes",
    "strikethrough",
    "substitution",
    "tasklist",
]

myst_heading_anchors = 3
myst_footnote_transition = True
myst_dmath_double_inline = True

# =============================================================================
# AUTODOC CONFIGURATION
# =============================================================================

autodoc_default_options = {
    "members": True,
    "member-order": "bysource",
    "special-members": "__init__",
    "undoc-members": True,
    "exclude-members": "__weakref__",
}

autodoc_typehints = "description"
autodoc_typehints_description_target = "documented"
autosummary_generate = False

# Type hint configuration
typehints_fully_qualified = False
autodoc_typehints_format = "short"

# Enable better type hint resolution
python_use_unqualified_type_names = True

# Suppress warnings
suppress_warnings = ["ref.python", "autosummary", "autoapi"]

# =============================================================================
# INTERSPHINX MAPPING
# =============================================================================

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "numpy": ("https://numpy.org/doc/stable/", None),
    "pandas": ("https://pandas.pydata.org/docs/", None),
    "pydantic": ("https://docs.pydantic.dev/latest/", None),
    "langchain": ("https://python.langchain.com/docs/", None),
}

# =============================================================================
# ENHANCED FEATURES
# =============================================================================

# Napoleon settings for Google/NumPy style docstrings
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = False
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True

# Enhanced copybutton configuration
copybutton_prompt_text = r">>> |\.\.\. |\$ |In \[\d*\]: | {2,5}\.\.\.: | {5,8}: "
copybutton_prompt_is_regexp = True

# Enhanced diagrams
if "sphinxcontrib.mermaid" in extensions:
    mermaid_output_format = "svg"

# Todo extension settings
todo_include_todos = True
todo_emit_warnings = False

# =============================================================================
# CONFIGURATION SUMMARY
# =============================================================================

print("✅ STABLE Sphinx configuration loaded successfully!")
print(f"📦 Extensions: {len(extensions)}")
print(f"🎨 Theme: {html_theme}")
print("🔧 AutoAPI configured for all 7 Haive packages")
print("🚀 Building documentation with stable, tested extensions!")
