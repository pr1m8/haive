"""Fixed Sphinx configuration with all packages and working extensions."""

import os
import sys

project = "Haive AI Agent Framework"
copyright = "2024, Haive Team"
author = "Haive Team"
version = "1.0"
release = "1.0.0"

# General configuration
templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store", "**/*.md"]
pygments_style = "friendly"

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

# AutoAPI Configuration - ALL PACKAGES
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

# Add the package roots to Python path so imports work

for package in [
        "haive-core",
        "haive-agents",
        "haive-tools",
        "haive-games",
        "haive-dataflow",
        "haive-mcp",
        "haive-prebuilt",
]:
    sys.path.insert(0, os.path.abspath(f"../../packages/{package}/src"))

autoapi_root = "api"
autoapi_add_toctree_entry = False  # We'll manage the TOC ourselves
autoapi_keep_files = True  # Keep generated files for custom organization
autoapi_generate_api_docs = True
autoapi_python_class_content = "both"
autoapi_member_order = "bysource"
autoapi_python_use_implicit_namespaces = True  # Preserve full module paths
autoapi_options = [
    "members",
    "undoc-members",
    "show-inheritance",
    "show-module-summary",
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
    "compiled_state_graph",
    "agent_types",
    "complex_rag",
    "usage_examples",
    "normalize_contents",
    "map_branch",
    "llm_compiler",
    "plan_and_execute",
    "web_nav",
]

# HTML theme configuration
html_theme = "furo"
html_title = f"{project} Documentation"
html_short_title = "Haive Docs"

html_theme_options = {
    "source_repository": "https://github.com/yourusername/haive/",
    "source_branch": "main",
    "source_directory": "docs/source/",
    "pygments_light_style": "friendly",
    "pygments_dark_style": "monokai",
    "light_css_variables": {
        "color-code-background": "#f8f8f8",
        "color-code-foreground": "#333333",
    },
    "dark_css_variables": {
        "color-code-background": "#2b2b2b",
        "color-code-foreground": "#f8f8f2",
    },
}

html_static_path = ["_static"]

# Add adaptive TOC functionality
html_js_files = [
    "adaptive-toc.js",
]

html_css_files = [
    "enhanced-docs.css",
    "adaptive-toc.css",
]

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

print("✅ Fixed Sphinx configuration loaded!")
print("🔧 AutoAPI configured for all 7 Haive packages")
print("✨ Using stable, tested extensions only")


# Configure AutoAPI Jinja environment
def prepare_autoapi_jinja_env(jinja_env):
    """Prepare the Jinja environment for autoapi."""

    def fix_module_name(name):
        # Remove src. prefix if present
        if name and name.startswith("src."):
            return name[4:]
        return name

    def fix_path(path):
        # Fix paths in toctree references
        if path and "/src/haive/" in path:
            return path.replace("/src/haive/", "/haive/")
        if path and "src/haive/" in path:
            return path.replace("src/haive/", "haive/")
        return path

    def fix_include_path(path):
        # Fix include paths for toctree entries
        if path and "/src/" in path:
            return path.replace("/src/", "/")
        return path

    jinja_env.filters["fix_module_name"] = fix_module_name
    jinja_env.filters["fix_path"] = fix_path
    jinja_env.filters["fix_include_path"] = fix_include_path
    return jinja_env


# Connect to AutoAPI
autoapi_prepare_jinja_env = prepare_autoapi_jinja_env
