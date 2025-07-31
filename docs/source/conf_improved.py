"""Optimized Sphinx configuration for Haive documentation.

This configuration utilizes all available documentation dependencies
for a professional, feature-rich documentation experience with enhanced
theme support and comprehensive extension usage.
"""

from datetime import datetime
import logging
from pathlib import Path
import sys
import warnings


# Set up logging for debugging
log_file = Path(__file__).parent / "sphinx_debug.log"
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler(str(log_file)), logging.StreamHandler()],
)
logger = logging.getLogger(__name__)

# Suppress specific warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", message=".*Matplotlib.*")
warnings.filterwarnings("ignore", category=UserWarning, module="sphinx")

# ==============================================================================
# Path Setup for Namespaced Monorepo
# ==============================================================================

# Get paths
conf_dir = Path(__file__).parent.absolute()
docs_dir = conf_dir.parent
workspace_dir = docs_dir.parent

# Add the workspace to Python path for imports
sys.path.insert(0, str(workspace_dir))

# Add extensions directory to path for custom extensions
sys.path.insert(0, str(conf_dir / "_extensions"))

# Add package source paths - namespaced imports require parent directory
packages_dir = workspace_dir / "packages"

# Note: haive-prebuilt is excluded from docs as it contains generated/binary content
package_names = [
    "haive-core",
    "haive-agents",
    "haive-tools",
    "haive-games",
    "haive-dataflow",
    "haive-mcp",
    # "haive-prebuilt",
]

# Configure nitpicky mode
nitpicky = False  # Set to False to prevent build failures on missing references
nitpick_ignore = [
    # Add ignored references here if needed
    ("py:class", "typing.Optional"),
    ("py:class", "typing.Union"),
    ("py:class", "typing.List"),
    ("py:class", "typing.Dict"),
]

# For namespaced packages, we need to add the src directory
logger.info(f"Found packages directory: {packages_dir}")
for package in package_names:
    src_path = packages_dir / package / "src"
    if src_path.exists():
        logger.info(f"Adding to sys.path: {src_path}")
        sys.path.insert(0, str(src_path))

        # Try to import the package
        package_module = f"haive.{package.split('-')[1]}"
        try:
            __import__(package_module)
            logger.info(f"Successfully imported {package_module}")
        except Exception as e:
            logger.warning(f"Failed to import {package_module}: {e}")

# Add custom extensions
extensions_path = conf_dir / "_extensions"
if extensions_path.exists():
    sys.path.insert(0, str(extensions_path))

# ==============================================================================
# Project Information
# ==============================================================================

project = "Haive"
author = "William R. Astley"
current_year = datetime.now().year
copyright = f"2025-{current_year}, {author}"  # noqa: A001
version = "1.0"
release = "1.0.0"

# ==============================================================================
# Extensions Configuration - COMPREHENSIVE EXTENSION USAGE
# ==============================================================================

extensions = [
    # === CORE API DOCUMENTATION ===
    "autoapi.extension",  # ✅ RE-ENABLED: Best-in-class API documentation
    "sphinx.ext.autodoc",  # Autodoc support
    "sphinx.ext.napoleon",  # Google/NumPy docstring support
    "sphinx.ext.viewcode",  # [source] links
    "sphinx.ext.linkcode",  # GitHub source links
    "sphinx.ext.intersphinx",  # Cross-project references
    "sphinx.ext.autosummary",  # Summary tables
    # === PYDANTIC INTEGRATION ===
    "sphinxcontrib.autodoc_pydantic",  # ✅ NEW: Essential for Pydantic v2 models
    # === TYPE HINTS & DOCUMENTATION ===
    "sphinx_autodoc_typehints",  # 🎯 Beautiful type hints
    # === ENHANCED CONTENT & INTERACTIVITY ===
    "sphinx_design",  # 🎨 Cards, grids, badges, dropdowns
    "sphinx_tabs",  # 📑 Tabbed content sections
    # REMOVED: sphinx_inline_tabs - conflicts with sphinx_tabs
    "sphinx_togglebutton",  # 🔽 Collapsible sections
    "sphinx_copybutton",  # 📋 Copy code buttons
    "sphinx_exec_directive",  # ⚡ Execute Python code in docs
    # === MARKDOWN & CONTENT ===
    "myst_parser",  # 📝 Markdown support (MyST)
    "myst_nb",  # 📓 Jupyter notebook support
    # === DIAGRAMS & MEDIA ===
    "sphinxcontrib.mermaid",  # 📊 Mermaid diagrams
    "sphinxcontrib.youtube",  # 🎬 YouTube video embedding
    # === SEARCH & NAVIGATION ===
    "readthedocs_sphinx_search",  # ✅ NEW: Enhanced search functionality
    "sphinx_sitemap",  # 📍 SEO sitemap generation
    # === API DOCUMENTATION ===
    "sphinxcontrib.openapi",  # 📚 OpenAPI/Swagger docs
    "sphinxcontrib.httpdomain",  # 🌐 HTTP API documentation
    # === SOCIAL & SEO ===
    "sphinxext.opengraph",  # 📱 Open Graph metadata
    # === EXAMPLES & GALLERIES ===
    "sphinx_gallery",  # 🖼️ Example gallery generation
    # === REQUIREMENTS & DATA ===
    "sphinx_needs",  # 📋 Requirements management
    # === CODE QUALITY & REFERENCES ===
    "sphinx_codeautolink",  # 🔗 Auto-link code references
    "sphinx_prompt",  # 💻 Terminal prompt styling
    # === TEMPLATE PROCESSING ===
    "sphinx_jinja2",  # 🎨 Jinja2 template processing for agent demos
    # === ADVANCED FEATURES ===
    "sphinx_external_toc",  # 📚 External table of contents
    "sphinx_thebe",  # 🚀 Interactive code execution
    "sphinx_tippy",  # 💡 Enhanced tooltips
    "sphinx_hoverxref",  # 🎯 Hover cross-references
    # === DOCUMENTATION QUALITY ===
    "sphinx_lint",  # 📝 Sphinx-specific linting
    "sphinx_last_updated_by_git",  # 🕐 Git-based timestamps
    "sphinx_contributors",  # 👥 Show contributors
    "sphinx_version_warning",  # ⚠️ Version warnings
    # === SPECIALIZED DOCUMENTATION ===
    "sphinx_argparse",  # 🎛️ Argparse CLI documentation
    "sphinx_click",  # 🖱️ Click CLI documentation
    "sphinx_jsonschema",  # 📋 JSON schema documentation
    "sphinxcontrib.fulltoc",  # 📑 Full TOC in sidebar
    # === ACCESSIBILITY & UX ===
    "sphinx_notfound_page",  # 🚫 Custom 404 pages
    "sphinx_favicon",  # 🌟 Favicon support
    "sphinx_paramlinks",  # 🔗 Linkable parameters
    "sphinxemoji",  # 😊 Emoji support
    # === DIAGRAMS & VISUALIZATION ===
    "sphinxcontrib.plantuml",  # 📊 PlantUML diagrams
    "sphinxcontrib.drawio",  # 🎨 Draw.io diagrams
    "sphinxcontrib.images",  # 🖼️ Advanced image handling
    "sphinxcontrib.seqdiag",  # 📈 Sequence diagrams
    "sphinxcontrib.blockdiag",  # 📦 Block diagrams
    # === SPECIALIZED EXTENSIONS ===
    "sphinx_autosummary_accessors",  # 🔍 Document accessor methods
    "autodocsumm",  # 📑 Auto-generate summary tables
    "sphinx_jinja",  # 🎭 Jinja2 templates
    "sphinx_examples",  # 📚 Example management
    "sphinx_removed_in",  # 🚮 Deprecation warnings
    "sphinx_selective_exclude",  # 🚫 Selective exclusion
    "sphinx_substitution_extensions",  # 🔄 Variable substitution
    "sphinx_pyproject",  # 📦 pyproject.toml integration
    # === INTERNATIONALIZATION ===
    "sphinx_intl",  # 🌍 Internationalization support
    # === PRESENTATIONS ===
    "sphinx_revealjs",  # 🎪 RevealJS presentations
    # === EDUCATIONAL ===
    "sphinx_exercise",  # 📝 Exercise directives
    "sphinx_proof",  # 🔍 Proof directives
    # === PDF & EXPORT (Optional - enable when needed) ===
    # "sphinx_simplepdf",  # 📄 PDF generation
    # === VERSIONING (Optional - enable when needed) ===
    # "sphinx_multiversion",  # 📚 Multi-version docs
]

# ==============================================================================
# Source File Configuration
# ==============================================================================

# MyST handles source suffixes automatically
source_suffix = {
    ".rst": "restructuredtext",
    ".md": "markdown",
}

exclude_patterns = [
    "_build",
    "Thumbs.db",
    ".DS_Store",
    "**/.git",
    "**/node_modules",
    "discovered_readmes/**",
    "**/.venv/**",
    "**/site-packages/**",
    "**/__pycache__",
    "**/test_*.py",
    "**/tests/**",
    "**/*_test.py",
    "**/*_v2.py",  # ✅ NEW: Skip .v2 files as requested
    "**/*.v2.py",  # ✅ NEW: Alternative pattern for .v2 files
    "**/ui.py",
    "**/*.egg-info/**",
    "generated/**",
    "_archive/**",
    "conf_*.py",
    "**/scripts/**",
    "**/debug*.py",
    "**/demo*.py",
    "**/example*.py",
]

# ==============================================================================
# HTML Theme Configuration - FURO THEME WITH ENHANCED STYLING
# ==============================================================================

html_theme = "furo"
html_title = "🤖 Haive AI Agent Framework"
html_short_title = "Haive"

# Static files
html_static_path = ["_static"]

# Enhanced CSS and JS files
html_css_files = [
    "haive-minimal.css",  # 🎨 ENHANCED: Main theme customizations
    "haive-enhanced.css",  # ✅ NEW: Additional enhancements
]

html_js_files = [
    "haive-graph-visualizations.js",  # 🎨 Graph visualization classes
    "agent-visualization.js",
    "enhanced-search.js",  # Enhanced search functionality
    "showcase-interactions.js",  # Interactive showcase elements
    "enhanced-interface.js",  # Unified interface enhancements
    "agent-demo-utils.js",  # Agent demo visualization utilities
]

# FIXED: Furo theme options with consolidated light_css_variables
html_theme_options = {
    # === SIDEBAR ===
    "sidebar_hide_name": False,
    "navigation_with_keys": True,
    "top_of_page_buttons": ["edit", "view"],
    "show_prev_next": True,
    # === NAVIGATION ENHANCEMENTS ===
    "navigation_depth": 4,
    "collapse_navigation": False,
    "titles_only": False,
    # === TABLE OF CONTENTS (RIGHT SIDEBAR) ===
    "show_toc_level": 3,
    "toc_title": "On this page",
    # === CONSOLIDATED CSS VARIABLES (FIXED: No duplicates) ===
    "light_css_variables": {
        # === LAYOUT ===
        "sidebar-width": "15rem",  # Reduced for better balance
        "content-width": "50rem",  # Increased content width
        "content-padding": "2rem",  # Optimized padding
        "sidebar-item-spacing-vertical": "0.5rem",
        "sidebar-item-spacing-horizontal": "1rem",
        "sidebar-item-font-size": "0.9rem",
        "sidebar-search-space-above": "1rem",
        "toc-spacing-vertical": "0.5rem",
        "toc-spacing-horizontal": "1rem",
        "toc-font-size": "0.85rem",
        # === TYPOGRAPHY ===
        "font-stack": "system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif",
        "font-stack--monospace": "'JetBrains Mono', 'Consolas', 'Monaco', 'Courier New', monospace",
        "font-stack--headings": "'Inter', system-ui, -apple-system, sans-serif",
        "font-size--small": "0.875rem",
        "font-size--normal": "1rem",
        "font-size--medium": "1.125rem",
        "font-size--small--2": "0.75rem",
        "font-size--small--3": "0.6875rem",
        "line-height--normal": "1.7",
        "line-height--small": "1.5",
        # === COLORS - BRAND ===
        "color-brand-primary": "#0066cc",
        "color-brand-content": "#0066cc",
        # === COLORS - GENERAL ===
        "color-foreground-primary": "#1a1a1a",
        "color-foreground-secondary": "#666666",
        "color-foreground-muted": "#6b7280",
        "color-background-primary": "#ffffff",
        "color-background-secondary": "#f8f9fa",
        "color-background-hover": "#f0f0f0",
        "color-background-hover--transparent": "#f3f4f6",
        "color-background-item": "#e5e7eb",
        # === COLORS - SIDEBAR ===
        "color-sidebar-background": "#fafafa",
        "color-sidebar-background-border": "#e1e4e8",
        # === COLORS - CODE & API ===
        "color-inline-code-background": "#f1f5f9",
        "color-inline-code-foreground": "#334155",
        "color-api-background": "#f8fafc",
        "color-api-background-hover": "#f1f5f9",
        "color-api-overall": "#64748b",
        "color-api-name": "#0f172a",
        "color-api-pre-name": "#475569",
        "color-api-paren": "#94a3b8",
        "color-api-keyword": "#7c3aed",
        # === COLORS - UI ELEMENTS ===
        "color-problematic": "#dc2626",
        "color-card-border": "#e2e8f0",
        "color-card-marginals-background": "#f8fafc",
        "color-admonition-background": "#f8f9fa",
        "color-announcement-background": "#007acc",
        "color-announcement-text": "#ffffff",
        # === COLORS - SEARCH ===
        "color-search-background": "#ffffff",
        "color-search-foreground": "#1f2937",
        "color-search-border": "#d1d5db",
        "color-search-border--focus": "#3b82f6",
        # === CODE STYLING ===
        "color-code-tab-size": "4",
        "color-code-max-lines": "none",
        "font-size--code": "0.875rem",
        "font-size--code--small": "0.8125rem",
        "code-font-size": "0.85rem",
        "api-font-size": "0.9rem",
        "admonition-font-size": "0.9rem",
        "admonition-title-font-size": "0.95rem",
    },
    # === DARK MODE VARIABLES ===
    "dark_css_variables": {
        "color-brand-primary": "#4da6ff",
        "color-brand-content": "#4da6ff",
        "color-foreground-primary": "#e2e8f0",
        "color-foreground-secondary": "#a0aec0",
        "color-foreground-muted": "#9ca3af",
        "color-background-primary": "#1a202c",
        "color-background-secondary": "#2d3748",
        "color-background-hover": "#4a5568",
        "color-background-hover--transparent": "#374151",
        "color-sidebar-background": "#1e2835",
        "color-sidebar-background-border": "#2d3748",
        "color-inline-code-background": "#1e293b",
        "color-inline-code-foreground": "#cbd5e1",
        "color-api-background": "#0f172a",
        "color-api-background-hover": "#1e293b",
        "color-card-border": "#334155",
        "color-card-marginals-background": "#1e293b",
        "color-admonition-background": "#2d3748",
        "color-announcement-background": "#007acc",
        "color-announcement-text": "#ffffff",
        "color-search-background": "#1f2937",
        "color-search-foreground": "#f9fafb",
        "color-search-border": "#4b5563",
        "color-search-border--focus": "#60a5fa",
    },
    # === PYGMENTS STYLES ===
    "pygments_light_style": "default",
    "pygments_dark_style": "github-dark",
    # === FOOTER ===
    "footer_icons": [
        {
            "name": "GitHub",
            "url": "https://github.com/will-astley/haive",
            "html": """
                <svg stroke="currentColor" fill="currentColor" stroke-width="0" viewBox="0 0 16 16">
                    <path fill-rule="evenodd" d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0 0 16 8c0-4.42-3.58-8-8-8z"></path>
                </svg>
            """,
            "class": "",
        },
        {
            "name": "PyPI",
            "url": "https://pypi.org/project/haive/",
            "html": """
                <svg stroke="currentColor" fill="currentColor" stroke-width="0" viewBox="0 0 24 24">
                    <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"></path>
                </svg>
            """,
            "class": "",
        },
    ],
    # === SOURCE REPOSITORY ===
    "source_repository": "https://github.com/will-astley/haive",
    "source_branch": "main",
    "source_directory": "docs/source/",
}

# === SIDEBAR CONFIGURATION FOR FURO ===
html_sidebars = {
    "**": [
        "sidebar/brand.html",
        "sidebar/search.html",
        "sidebar/scroll-start.html",
        "sidebar/navigation.html",
        "sidebar/scroll-end.html",
    ],
}

# ==============================================================================
# Extension Configurations - COMPREHENSIVE SETUP
# ==============================================================================

# === AUTOAPI - ENHANCED API DOCUMENTATION ===
autoapi_type = "python"
autoapi_dirs = [
    "../../packages/haive-core/src",
    "../../packages/haive-agents/src",
    "../../packages/haive-tools/src",
    "../../packages/haive-dataflow/src",
    "../../packages/haive-games/src",
    "../../packages/haive-mcp/src",
]
autoapi_root = "api"
autoapi_options = [
    "members",
    "show-inheritance",
    "show-module-summary",
    "special-members",  # Show __init__, __call__, etc.
    "private-members",  # Show documented private methods
]
autoapi_keep_files = True
autoapi_add_toctree_entry = True
autoapi_member_order = "groupwise"
autoapi_python_class_content = "both"
autoapi_python_use_implicit_namespaces = True
autoapi_generate_api_docs = True
autoapi_template_dir = "_templates/autoapi"

# Enhanced AutoAPI ignore patterns (including .v2 files)
autoapi_ignore = [
    "**/__pycache__/**",
    "**/*.pyc",
    "**/*.pyo",
    "**/test_*.py",
    "**/tests/**",
    "**/*_test.py",
    "**/*_v2.py",  # ✅ NEW: Skip .v2 files
    "**/*.v2.py",  # ✅ NEW: Alternative .v2 pattern
    "**/demo*.py",
    "**/debug*.py",
    "**/example*.py",
    "**/app.py",
    "**/main.py",
    "**/cli.py",
    "**/.ipynb_checkpoints/**",
    "**/examples/**",
    "**/scripts/**",
]

# === AUTODOC-PYDANTIC - PYDANTIC MODEL DOCUMENTATION ===
autodoc_pydantic_model_show_json = False
autodoc_pydantic_model_show_config_summary = False
autodoc_pydantic_field_show_constraints = True  # ✅ Show Field() constraints
autodoc_pydantic_field_show_required = True  # ✅ Show required fields
autodoc_pydantic_model_show_field_summary = True  # ✅ Show field summaries
autodoc_pydantic_field_list_validators = True  # ✅ Show field validators
autodoc_pydantic_model_show_validator_summary = True  # ✅ Show validator info
autodoc_pydantic_model_signature_prefix = "class"
autodoc_pydantic_model_member_order = "bysource"

# === NAPOLEON - GOOGLE DOCSTRINGS ===
napoleon_google_docstring = True
napoleon_numpy_docstring = False
napoleon_include_init_with_doc = True
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = True
napoleon_use_admonition_for_notes = True
napoleon_use_admonition_for_references = True
napoleon_use_ivar = True
napoleon_use_param = True
napoleon_use_rtype = True
napoleon_use_keyword = True
napoleon_preprocess_types = True
napoleon_attr_annotations = True

# === AUTODOC & TYPE HINTS (ENHANCED) ===
autodoc_typehints = "both"  # Show in signature AND description
typehints_document_rtype = True
typehints_use_signature = True
typehints_use_signature_return = True
typehints_format = "short"  # Better readability
always_document_param_types = True
autodoc_preserve_defaults = True
autodoc_member_order = "groupwise"
autodoc_type_aliases = {
    "Agent": "haive.agents.base.Agent",
    "StateSchema": "haive.core.schema.StateSchema",
    "Engine": "haive.core.engine.Engine",
    "Tool": "haive.core.tools.Tool",
    "Graph": "haive.core.graph.BaseGraph",
    "MessagesState": "haive.core.schema.prebuilt.MessagesState",
    "MetaStateSchema": "haive.core.schema.prebuilt.MetaStateSchema",
}

# === COPY BUTTON ===
copybutton_prompt_text = (
    r">>> |\\.\\.\\. |\\$ |In \\[\\d*\\]: | {2,5}\\.\\.\\.: | {5,8}: "
)
copybutton_prompt_is_regexp = True
copybutton_exclude = ".linenos, .gp"

# === MYST PARSER - ENHANCED MARKDOWN SUPPORT ===
myst_enable_extensions = [
    "deflist",  # Definition lists
    "tasklist",  # Task lists with checkboxes
    "colon_fence",  # ::: code blocks
    "smartquotes",  # Smart quotes
    "linkify",  # Auto-link URLs
    "strikethrough",  # ~~strikethrough~~
    "dollarmath",  # $math$ syntax
    "substitution",  # Variable substitution
    "attrs_inline",  # Inline attributes
    "attrs_block",  # Block attributes
    "amsmath",  # AMS math support
    "html_image",  # HTML image support
]

# === MYST-NB - JUPYTER NOTEBOOK SUPPORT ===
nb_execution_mode = "cache"
nb_execution_timeout = 600  # 10 minutes
nb_execution_show_tb = "short"
nb_execution_in_temp = False

# === MERMAID DIAGRAMS ===
mermaid_version = "10.6.1"
mermaid_init_js = """
mermaid.initialize({
    startOnLoad: true,
    theme: 'default',
    themeVariables: {
        primaryColor: '#0066cc',
        primaryTextColor: '#ffffff',
        primaryBorderColor: '#0066cc',
        lineColor: '#666666',
        secondaryColor: '#f0f0f0',
        tertiaryColor: '#ffffff'
    },
    flowchart: {
        useMaxWidth: true,
        htmlLabels: true,
        curve: 'basis'
    }
});
"""

# === SPHINX GALLERY - ENHANCED EXAMPLES ===
sphinx_gallery_conf = {
    "examples_dirs": [
        "../../packages/haive-agents/examples",
        "../../packages/haive-games/examples",
        "../../packages/haive-mcp/examples",
    ],
    "gallery_dirs": [
        "auto_examples/agents",
        "auto_examples/games",
        "auto_examples/mcp",
    ],
    "filename_pattern": "/.*tutorial|.*guide|.*example",
    "ignore_pattern": "__init__.py|debug_*|test_*|*_v2.py|*.v2.py",  # ✅ NEW: Ignore .v2 files
    "download_all_examples": True,
    "show_memory": True,
    "remove_config_comments": True,
    "expected_failing_examples": [],
    "thumbnail_size": (300, 200),
    "subsection_order": "ExplicitOrder",
    "within_subsection_order": "FileNameSortKey",
    "show_signature": True,
    "plot_gallery": False,
    "promote_jupyter_magic": True,
    "binder_conf": {
        "org": "haive",
        "repo": "haive",
        "branch": "main",
        "binderhub_url": "https://mybinder.org",
        "dependencies": ["../../pyproject.toml"],
    },
}

# === SPHINX-EXEC-DIRECTIVE - INLINE CODE EXECUTION ===
exec_code_working_dir = "../.."
exec_code_example_dir = "examples/executed"
exec_code_source_folders = ["packages"]
exec_code_add_conf_path = True

# === SPHINX NEEDS - REQUIREMENTS MANAGEMENT ===
needs_types = [
    {
        "directive": "req",
        "title": "Requirement",
        "prefix": "R_",
        "color": "#BFD8D2",
        "style": "node",
    },
    {
        "directive": "spec",
        "title": "Specification",
        "prefix": "S_",
        "color": "#FEDCD2",
        "style": "node",
    },
    {
        "directive": "agent",
        "title": "Agent",
        "prefix": "A_",
        "color": "#667eea",
        "style": "node",
    },
    {
        "directive": "tool",
        "title": "Tool",
        "prefix": "T_",
        "color": "#764ba2",
        "style": "node",
    },
]

# === OPEN GRAPH - SOCIAL SHARING ===
ogp_site_url = "https://haive.readthedocs.io"
ogp_description_length = 200
ogp_image = "_static/haive-logo.png"
ogp_social_cards = {
    "enable": True,
    "image": "_static/haive-logo.png",
}

# === SITEMAP ===
sitemap_url_scheme = "{link}"
html_baseurl = "https://haive.readthedocs.io/"

# === CODE AUTOLINK - AUTO-LINK CODE REFERENCES ===
codeautolink_global_preface = """
import haive
from haive.agents.simple import SimpleAgent
from haive.agents.react import ReactAgent
from haive.core.engine import Engine
from haive.core.schema import StateSchema
"""

codeautolink_custom_blocks = {
    "haive.agents.simple.SimpleAgent": ":class:`~haive.agents.simple.SimpleAgent`",
    "haive.agents.react.ReactAgent": ":class:`~haive.agents.react.ReactAgent`",
    "haive.core.engine.Engine": ":class:`~haive.core.engine.Engine`",
    "SimpleAgent": ":class:`~haive.agents.simple.SimpleAgent`",
    "ReactAgent": ":class:`~haive.agents.react.ReactAgent`",
}

codeautolink_concat_default = True
codeautolink_warn_on_missing_inventory = False

# === SPHINX THEBE - INTERACTIVE CODE ===
thebe_config = {
    "repository_url": "https://github.com/will-astley/haive",
    "repository_branch": "main",
}

# === SPHINX TIPPY - ENHANCED TOOLTIPS ===
tippy_enable_mathjax = True
tippy_enable_docrefs = True

# === SPHINX HOVERXREF - HOVER CROSS-REFERENCES ===
hoverxref_auto_ref = True
hoverxref_domains = ["py"]
hoverxref_roles = ["class", "func", "meth", "attr", "exc", "data"]

# === READTHEDOCS SEARCH (NEW) - ENHANCED SEARCH ===
# Configuration is handled automatically by the extension

# === SPHINX PARAMLINKS - LINKABLE PARAMETERS ===
paramlinks_hyperlink_param = "name"

# === SPHINX CONTRIBUTORS ===
contributors_file = "CONTRIBUTORS.md"

# === SPHINX VERSION WARNING ===
version_warning_messages = {
    "latest": "You are reading the latest (unstable) version of this documentation.",
    "stable": "You are reading the stable version of this documentation.",
}

# === SPHINX NOTFOUND PAGE ===
notfound_urls_prefix = "/en/latest/"
notfound_template = "404.html"
notfound_pagename = "404"

# === SPHINX FAVICON ===
favicons = [
    {"rel": "icon", "href": "favicon.ico"},
    {"rel": "apple-touch-icon", "href": "apple-touch-icon.png"},
]

# === SPHINX EXERCISE & PROOF ===
exercise_include_exercises = True
exercise_numbered_exercises = True

# === SPHINX SELECTIVE EXCLUDE ===
selective_exclude_list = {
    "draft": ["*draft*", "*wip*"],
    "internal": ["*internal*", "*private*"],
}

# === PLANTUML CONFIGURATION ===
plantuml = "java -jar /usr/local/bin/plantuml.jar"
plantuml_output_format = "svg"
plantuml_latex_output_format = "pdf"

# === DRAWIO CONFIGURATION ===
drawio_binary_path = "/usr/local/bin/drawio"
drawio_output_format = "svg"

# === SEQDIAG & BLOCKDIAG ===
seqdiag_fontpath = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
blockdiag_fontpath = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"

# === SPHINX JINJA ===
jinja_contexts = {
    "default": {
        "project": project,
        "version": version,
        "release": release,
        "author": author,
    }
}

# === SPHINX PYPROJECT ===
pyproject_config = True

# === INTERSPHINX ===
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "langchain": ("https://python.langchain.com/", None),
    "pydantic": ("https://docs.pydantic.dev/", None),
    "numpy": ("https://numpy.org/doc/stable/", None),
    "pandas": ("https://pandas.pydata.org/docs/", None),
    "fastapi": ("https://fastapi.tiangolo.com/", None),
    "sqlalchemy": ("https://docs.sqlalchemy.org/", None),
}

# === MOCK IMPORTS ===
autodoc_mock_imports = [
    "torch",
    "tensorflow",
    # Minimal mocking - let real imports work
]

# ==============================================================================
# AutoAPI Event Handlers
# ==============================================================================


def autoapi_skip_member(app, what, name, obj, skip, options):
    """Skip certain members during autoapi generation."""
    # Skip test files
    if "test_" in name or "_test" in name:
        return True

    # Skip .v2 files
    if "_v2" in name or ".v2" in name:
        return True

    # Skip files that were causing import issues
    for pattern in ["debug", "demo", "example", "ui.py", "main.py", "app.py", "cli.py"]:
        if pattern in name.lower():
            return True

    return skip


def prepare_autoapi_jinja_env(jinja_env):
    """Prepare the Jinja environment for autoapi."""

    def fix_module_name(name):
        if name and name.startswith("src."):
            return name[4:]
        return name

    def fix_path(path):
        if path and "/src/haive/" in path:
            return path.replace("/src/haive/", "/haive/")
        if path and "src/haive/" in path:
            return path.replace("src/haive/", "haive/")
        return path

    jinja_env.filters["fix_module_name"] = fix_module_name
    jinja_env.filters["fix_path"] = fix_path
    return jinja_env


# Connect to AutoAPI
autoapi_prepare_jinja_env = prepare_autoapi_jinja_env

# ==============================================================================
# Build Configuration
# ==============================================================================

templates_path = ["_templates"]
language = "en"
master_doc = "index"

# Performance optimizations
html_copy_source = False
html_show_sourcelink = True
html_show_sphinx = False
html_show_copyright = True

# Search
html_search_language = "en"

# Suppress warnings
suppress_warnings = [
    "autosummary.import_cycle",
    "autodoc.import_object",
    "ref.citation",
    "misc.highlighting_failure",
]

# Enhanced error handling
keep_warnings = True
autodoc_warningiserror = False

# ==============================================================================
# Pygments Configuration
# ==============================================================================

pygments_style = "default"
pygments_dark_style = "github-dark"

# ==============================================================================
# GitHub Source Links
# ==============================================================================


def linkcode_resolve(domain, info):
    """Resolve function to link to GitHub source code."""
    if domain != "py":
        return None
    if not info["module"]:
        return None

    module_parts = info["module"].split(".")
    if len(module_parts) < 2 or module_parts[0] != "haive":
        return None

    package_name = module_parts[1]
    package_dir = f"haive-{package_name}"

    submodule_path = "/".join(module_parts[2:]) if len(module_parts) > 2 else ""
    if submodule_path:
        filename = (
            f"packages/{package_dir}/src/haive/{package_name}/{submodule_path}.py"
        )
    else:
        filename = f"packages/{package_dir}/src/haive/{package_name}/__init__.py"

    return f"https://github.com/will-astley/haive/blob/main/{filename}"


# ==============================================================================
# Setup Function
# ==============================================================================


def setup(app):
    """Setup function for custom modifications."""
    logger.info("Running enhanced Sphinx setup function")

    # Ensure directories exist
    static_dir = conf_dir / "_static"
    static_dir.mkdir(exist_ok=True)

    images_dir = static_dir / "images"
    images_dir.mkdir(exist_ok=True)

    # Add custom CSS for enhanced styling
    app.add_css_file("haive-enhanced.css")

    # Connect autoapi hooks
    app.connect("autoapi-skip-member", autoapi_skip_member)

    return {
        "version": "1.0",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }


# ==============================================================================
# Sphinx-Jinja2 Configuration (if enabled)
# ==============================================================================

# Import agent demo data if available
try:
    from agent_cache_loader import get_agent_demo_context, get_available_agent_types
    from agent_demo_data import AVAILABLE_AGENTS, get_agent_context

    # Configure Jinja2 contexts for sphinx-jinja2
    jinja2_contexts = {
        "agent_demo": {
            "get_agent_context": get_agent_context,
            "available_agents": AVAILABLE_AGENTS,
            "get_agent_demo_context": get_agent_demo_context,
            "get_available_agent_types": get_available_agent_types,
        }
    }

    jinja2_debug = False
except ImportError:
    logger.warning("Agent demo data not available - sphinx-jinja2 contexts disabled")
