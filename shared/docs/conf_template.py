# Haive Documentation Template Configuration
# This template is shared across all packages and customized per package
# Generated from PyAutoDoc's proven 43-extension system

import os
import sys
from pathlib import Path

from sphinx.application import Sphinx

# Path setup - TEMPLATE VARIABLES (replaced by sync script)
# PACKAGE_NAME will be replaced with actual package name (e.g., "haive-core")
# PROJECT_TITLE will be replaced with display name (e.g., "Haive Core")
project_root = Path(__file__).parent.parent.parent
package_src = project_root / "packages" / "PACKAGE_NAME" / "src"

# Add package src to path
sys.path.insert(0, str(package_src))

# Project information - TEMPLATE VARIABLES
project = "PROJECT_TITLE"
author = "Haive Team"
copyright = "2025, Haive Team"
release = "1.0.0"

# Extensions - HYPER-ORGANIZED with proper loading order (compatibility filtered)
extensions = [
    # Core (Priority 1-10) - AutoAPI FIRST as requested
    "sphinx.ext.autodoc",
    "autoapi.extension",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
    "seed_intersphinx_mapping",  # Auto-populate intersphinx from pyproject.toml
    # Enhanced API (Priority 11-20) - REMOVED enum_tools due to compatibility
    "sphinxcontrib.autodoc_pydantic",
    "sphinx_autodoc_typehints",
    # Content & Design (Priority 21-30) - INTENSE FURO FOCUS
    "myst_parser",
    "sphinx_design",  # KEY for intense theming
    "sphinx_togglebutton",
    "sphinx_copybutton",
    "sphinx_tabs.tabs",
    # Execution (Priority 31-40) - TESTING FOCUS
    "sphinxcontrib.programoutput",
    # Diagrams (Priority 41-50) - MERMAID FOCUS
    "sphinx.ext.graphviz",
    "sphinxcontrib.mermaid",
    "sphinxcontrib.plantuml",
    # Utilities (Priority 51-60)
    "sphinx_sitemap",
    "sphinx_codeautolink",
    # TOC Enhancements (Priority 61-70)
    "sphinx_treeview",  # Dynamic collapsible tree view sidebar
    # Enhanced Features (Priority 71-80)
    "sphinx_toggleprompt",  # Toggle Python prompts in code blocks
    "sphinx_prompt",  # Better CLI prompt documentation
    "sphinx_last_updated_by_git",  # Last modification from git
    "sphinx_inlinecode",  # Enhanced inline code styling
    "sphinx_library",  # Better library documentation
    "sphinx_icontract",  # Document contracts
    "sphinx_tippy",  # Rich hover tooltips
    # Documentation Tools (Priority 81-90)
    "sphinx_comments",  # Add comments and annotations
    "sphinx_contributors",  # Contributors extension
    "sphinx_issues",  # Link to GitHub issues
    "sphinx_needs",  # Requirements tracking and traceability
    "sphinxarg.ext",  # Automatic CLI documentation
    "notfound.extension",  # Custom 404 page
    "sphinx_reredirects",  # Redirect management for moved pages
    "sphinxext.rediraffe",  # Broken link detection and redirect generation
    "sphinx_git",  # Git changelog integration
    "sphinx_debuginfo",  # Development debug information
    "sphinxext.opengraph",  # OpenGraph metadata for social sharing
    "sphinx_tags",  # Content tagging system
    "sphinx_favicon",  # Favicon management
    "sphinxcontrib.collections",  # Document collections
    "sphinx_combine",  # Combine multiple documents
]

# General configuration
templates_path = ["_templates", "_autoapi_templates"]
html_static_path = ["_static"]
exclude_patterns = [
    "_build",
    "Thumbs.db",
    ".DS_Store",
    "**/CVS",
    "**/.git",
    "_collections/*/_collections",
    "**/symlink_loops",
]
add_module_names = False
toc_object_entries_show_parents = "hide"

# TOC Configuration - Enhanced nesting and presentation
html_sidebars = {
    "**": [
        "sidebar/brand.html",
        "sidebar/search.html",
        "sidebar/scroll-start.html",
        "sidebar/navigation.html",
        "sidebar/ethical-ads.html",
        "sidebar/scroll-end.html",
    ]
}

# Furo-specific TOC options
navigation_with_keys = True
top_of_page_button = "edit"

# Sphinx TOC settings
toctree_maxdepth = 4
toctree_collapse = False
toctree_titles_only = False
toctree_includehidden = True

# Jinja2 options
jinja_env_options = {"extensions": ["jinja2.ext.do"]}

# AutoAPI configuration - PRIORITY FIRST
autoapi_type = "python"
autoapi_dirs = ["../src"]  # Points to package's src directory
autoapi_template_dir = "_autoapi_templates"
autoapi_add_toctree_entry = True
autoapi_generate_api_docs = True
autoapi_keep_files = True
autoapi_options = [
    "members",
    "undoc-members",
    "show-inheritance",
    "show-module-summary",
    "private-members",
    "special-members",
    "imported-members",
]
autoapi_python_class_content = "both"
autoapi_add_class_diagram = True
autoapi_class_diagram_depth = 2

# AutoAPI TOC configuration
autoapi_member_order = "groupwise"
autoapi_root = "autoapi"
autoapi_toctree_depth = 3

# Napoleon configuration
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = False
napoleon_include_private_with_doc = False

# Intersphinx configuration
pkg_requirements_source = "pyproject"
repository_root = "../.."  # Path to repo root from package/docs

# Manual intersphinx mappings
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "pydantic": ("https://docs.pydantic.dev/latest", None),
    "sphinx": ("https://www.sphinx-doc.org/en/master", None),
}

# Pydantic configuration
autodoc_pydantic_model_show_json = True
autodoc_pydantic_model_show_config_summary = True
autodoc_pydantic_model_show_validator_summary = True
autodoc_pydantic_model_show_field_summary = True
autodoc_pydantic_model_show_validator_members = True
autodoc_pydantic_field_list_validators = True
autodoc_pydantic_field_show_constraints = True
autodoc_pydantic_model_erdantic_figure = False
autodoc_pydantic_model_erdantic_figure_collapsed = False

# Type hints configuration
typehints_fully_qualified = False
typehints_use_signature = True

# MyST Parser configuration
myst_enable_extensions = [
    "deflist",
    "tasklist",
    "html_image",
    "colon_fence",
    "smartquotes",
    "replacements",
    "linkify",
    "strikethrough",
    "attrs_inline",
    "attrs_block",
]
myst_heading_anchors = 3
myst_fence_as_directive = ["mermaid", "note", "warning"]

# INTENSE FURO THEME CONFIGURATION
html_theme = "furo"

html_theme_options = {
    "sidebar_hide_name": False,
    # Enhanced TOC configuration
    "navigation_depth": 4,
    "collapse_navigation": False,
    "sticky_navigation": True,
    "includehidden": True,
    "titles_only": False,
    # Intense branding colors
    "light_css_variables": {
        "color-brand-primary": "#2563eb",  # Blue-600
        "color-brand-content": "#1d4ed8",  # Blue-700
        "color-background-primary": "#ffffff",
        "color-background-secondary": "#f8fafc",  # Slate-50
        "color-background-hover": "#e2e8f0",  # Slate-200
        "color-background-border": "#cbd5e1",  # Slate-300
        "color-code-background": "#1e293b",  # Slate-800
        "color-code-foreground": "#e2e8f0",  # Slate-200
        "color-sidebar-background": "#0f172a",  # Slate-900
        "color-sidebar-foreground": "#cbd5e1",  # Slate-300
        "color-api-background": "#f1f5f9",  # Slate-100
        "color-api-background-hover": "#e2e8f0",  # Slate-200
        "color-admonition-background": "#dbeafe",  # Blue-100
    },
    "dark_css_variables": {
        "color-brand-primary": "#60a5fa",  # Blue-400
        "color-brand-content": "#3b82f6",  # Blue-500
        "color-background-primary": "#0f172a",  # Slate-900
        "color-background-secondary": "#1e293b",  # Slate-800
        "color-background-hover": "#334155",  # Slate-700
        "color-background-border": "#475569",  # Slate-600
        "color-code-background": "#0f172a",  # Slate-900
        "color-code-foreground": "#cbd5e1",  # Slate-300
        "color-sidebar-background": "#020617",  # Slate-950
        "color-sidebar-foreground": "#94a3b8",  # Slate-400
    },
    # Repository integration - TEMPLATE VARIABLES
    "source_repository": "https://github.com/prim8/haive/",
    "source_branch": "main",
    "source_directory": "packages/PACKAGE_NAME/docs/",
    # Package-specific announcement
    "announcement": "🚀 <strong>PROJECT_TITLE</strong> - Part of the Haive AI Agent Framework!",
    # Footer icons
    "footer_icons": [
        {
            "name": "GitHub",
            "url": "https://github.com/prim8/haive/",
            "html": """<svg stroke="currentColor" fill="currentColor" stroke-width="0" viewBox="0 0 16 16">
                <path fill-rule="evenodd" d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"></path>
            </svg>""",
        },
    ],
}

# Custom CSS and JS files for intense theming
html_css_files = [
    "furo-intense.css",
    "api-docs.css",
    "mermaid-custom.css",
    "toc-enhancements.css",
    "tippy-enhancements.css",
]

html_js_files = [
    "furo-enhancements.js",
    "mermaid-config.js",
    "toc-navigator.js",
    "js/api-enhancements.js",
]


# Event Hooks
def autoapi_skip_member(app, what, name, obj, skip, options):
    if name.startswith("__pydantic"):
        return True
    return None


def setup(app: Sphinx):
    app.connect("autoapi-skip-member", autoapi_skip_member)

    # Add custom CSS classes for TOC
    app.add_css_file("toc-enhancements.css")
    app.add_js_file("toc-navigator.js")

    print(f"✨ {project} documentation loaded!")
    print("🎨 Furo theme with PyAutoDoc extensions active!")
