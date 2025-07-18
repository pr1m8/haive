"""Optimized Sphinx configuration for Haive documentation.

This configuration utilizes all available documentation dependencies
for a professional, feature-rich documentation experience.
"""

import logging
import sys
import warnings
from datetime import datetime
from pathlib import Path

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
nitpicky = True
nitpick_ignore = [
    # Add ignored references here if needed
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
# Extensions Configuration - UTILIZING ALL AVAILABLE EXTENSIONS
# ==============================================================================

extensions = [
    # === CORE API DOCUMENTATION ===
    "autoapi.extension",  # 🚀 RE-ENABLED for P0 fix testing
    "sphinx.ext.napoleon",  # Google/NumPy docstring support
    "sphinx.ext.viewcode",  # [source] links
    "sphinx.ext.linkcode",  # GitHub source links
    "sphinx.ext.intersphinx",  # Cross-project references
    "sphinx.ext.autosummary",  # Summary tables
    "sphinx.ext.autodoc",  # Autodoc support
    # === ENHANCED CONTENT & INTERACTIVITY ===
    "sphinx_design",  # 🎨 Cards, grids, badges, dropdowns
    "sphinx_tabs",  # 📑 Tabbed content sections
    "sphinx_inline_tabs",  # Inline tabbed content
    "sphinx_togglebutton",  # 🔽 Collapsible sections
    "sphinx_copybutton",  # 📋 Copy code buttons
    "sphinx_exec_directive",  # ⚡ Execute Python code in docs
    # === MARKDOWN & CONTENT ===
    "myst_parser",  # 📝 Markdown support (MyST)
    # Note: sphinx_mdinclude disabled to avoid conflicts with myst_parser
    # === DIAGRAMS & MEDIA ===
    "sphinxcontrib.mermaid",  # 📊 Mermaid diagrams
    "sphinxcontrib.youtube",  # 🎬 YouTube video embedding
    # === SEARCH & NAVIGATION ===
    "sphinx_sitemap",  # 📍 SEO sitemap generation
    # === API DOCUMENTATION ===
    "sphinxcontrib.openapi",  # 📚 OpenAPI/Swagger docs
    "sphinxcontrib.httpdomain",  # 🌐 HTTP API documentation
    # === SOCIAL & SEO ===
    "sphinxext.opengraph",  # 📱 Open Graph metadata
    # === EXAMPLES & GALLERIES ===
    # "sphinx_gallery",  # 🖼️ Example gallery generation (temp disabled)
    # === TYPE HINTS & DOCUMENTATION ===
    "sphinx_autodoc_typehints",  # 🎯 Beautiful type hints
    # === REQUIREMENTS & DATA ===
    "sphinx_needs",  # 📋 Requirements management - ENABLED for tracking
    # === CODE QUALITY & REFERENCES ===
    # "sphinx_codeautolink",  # 🔗 Auto-link code references (causing get_logger error)
    "sphinx_prompt",  # 💻 Terminal prompt styling
    # === TEMPLATE PROCESSING ===
    "sphinx_jinja2",  # 🎨 Jinja2 template processing for agent demos
    # === PDF & EXPORT ===
    # "sphinx_simplepdf",  # 📄 PDF generation (enable when needed)
    # === VERSIONING ===
    # "sphinx_multiversion",  # 📚 Multi-version docs (enable when needed)
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
    # Examples are handled by sphinx-gallery
    "**/ui.py",
    "**/*.egg-info/**",
    "generated/**",
    "_archive/**",
    "conf_*.py",
    "**/scripts/**",
    "**/debug*.py",
]

# ==============================================================================
# HTML Theme Configuration - Furo Theme with Showcase Styling
# ==============================================================================

html_theme = "furo"
html_title = "🤖 Haive AI Agent Framework"
html_short_title = "Haive"

# Static files
html_static_path = ["_static"]

# Enhanced CSS and JS for Furo with showcase styling
html_css_files = [
    "haive-design-system.css",  # 🎨 NEW: Professional design system foundation
    "custom.css",
    "haive-enhanced.css",  # Enhanced styling with gradients and animations
    "furo-showcase.css",  # Showcase styling for agents and games
    "showcase.css",  # Main showcase styling
    "api-showcase.css",  # API documentation showcase
    "agent-demo-visualizations.css",  # Agent demo visualization styles
]

html_js_files = [
    "agent-visualization.js",
    "enhanced-search.js",  # Enhanced search functionality
    "showcase-interactions.js",  # Interactive showcase elements
    "enhanced-interface.js",  # Unified interface enhancements
    "agent-demo-utils.js",  # Agent demo visualization utilities
]

# Furo theme options - SHOWCASE OPTIMIZED
html_theme_options = {
    # === SIDEBAR ===
    "sidebar_hide_name": False,
    "navigation_with_keys": True,
    "top_of_page_buttons": ["edit", "view"],
    # === PYGMENTS STYLES ===
    "pygments_light_style": "default",
    "pygments_dark_style": "github-dark",
    # === COLORS & STYLING ===
    "light_css_variables": {
        "color-brand-primary": "#0066cc",
        "color-brand-content": "#0066cc",
        "color-admonition-background": "#f8f9fa",
        "color-foreground-primary": "#1a1a1a",
        "color-foreground-secondary": "#666666",
        "color-background-primary": "#ffffff",
        "color-background-secondary": "#f8f9fa",
        "color-background-hover": "#f0f0f0",
        "color-sidebar-background": "#fafafa",
        "color-sidebar-background-border": "#e1e4e8",
        "color-announcement-background": "#007acc",
        "color-announcement-text": "#ffffff",
        "font-stack": "system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Noto Sans', 'Ubuntu', 'Cantarell', 'Helvetica Neue', sans-serif",
        "font-stack--monospace": "'JetBrains Mono', 'Consolas', 'Monaco', 'Courier New', monospace",
        "font-size--small": "0.875rem",
        "font-size--normal": "1rem",
        "font-size--medium": "1.125rem",
        "sidebar-width": "20rem",
        "sidebar-item-spacing-vertical": "0.5rem",
        "sidebar-item-spacing-horizontal": "1rem",
        "sidebar-item-font-size": "0.9rem",
        "sidebar-search-space-above": "1rem",
        "toc-spacing-vertical": "0.5rem",
        "toc-spacing-horizontal": "1rem",
        "toc-font-size": "0.85rem",
        "admonition-font-size": "0.9rem",
        "admonition-title-font-size": "0.95rem",
        "code-font-size": "0.85rem",
        "api-font-size": "0.9rem",
    },
    "dark_css_variables": {
        "color-brand-primary": "#4da6ff",
        "color-brand-content": "#4da6ff",
        "color-admonition-background": "#2d3748",
        "color-foreground-primary": "#e2e8f0",
        "color-foreground-secondary": "#a0aec0",
        "color-background-primary": "#1a202c",
        "color-background-secondary": "#2d3748",
        "color-background-hover": "#4a5568",
        "color-sidebar-background": "#1e2835",
        "color-sidebar-background-border": "#2d3748",
        "color-announcement-background": "#007acc",
        "color-announcement-text": "#ffffff",
    },
    # === ANNOUNCEMENT ===
    # "announcement": "🤖 <strong>Haive AI Agent Framework</strong> - Build intelligent agents with ease! 🚀",  # 🚨 REMOVED: Ugly blue banner
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

# ==============================================================================
# Extension Configurations - OPTIMIZED FOR ALL EXTENSIONS
# ==============================================================================

# === AUTOAPI - BEST-IN-CLASS API DOCUMENTATION ===
autoapi_type = "python"
autoapi_dirs = [
    # Point to src directories (will generate haive.* namespace)
    "../../packages/haive-core/src",
    "../../packages/haive-agents/src",
    # "../../packages/haive-tools/src",
    # "../../packages/haive-games/src",
    # "../../packages/haive-mcp/src",
    # "../../packages/haive-dataflow/src",
]
autoapi_root = "api"
autoapi_options = [
    "members",
    "show-inheritance",
    "show-module-summary",
    # "undoc-members",  # Skip undocumented members to reduce noise
    # "imported-members",  # Skip imported members to avoid duplicates
]
autoapi_keep_files = True
autoapi_add_toctree_entry = True
autoapi_member_order = "bysource"
autoapi_python_class_content = "class"  # Only show class docstring, not init
autoapi_python_use_implicit_namespaces = True  # Handle namespace packages


# Clean up module names to remove src. prefix
def autoapi_skip_member(app, what, name, obj, skip, options):
    """Skip certain members during autoapi generation."""
    return skip


def autoapi_prepare_jinja_env(jinja_env):
    """Prepare the Jinja environment for autoapi."""

    def fix_module_name(name):
        # Remove src. prefix if present
        if name.startswith("src."):
            name = name[4:]
        return name

    jinja_env.filters["fix_module_name"] = fix_module_name
    return jinja_env


# Custom hook to modify autoapi objects
def autoapi_process_docstring(app, what, name, obj, options, lines):
    """Process docstrings to clean up module names."""
    if what == "module" and name.startswith("src."):
        # Update the module name in the object
        obj.name = name[4:]  # Remove "src." prefix


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

# === AUTODOC & TYPE HINTS ===
autodoc_typehints = "description"
typehints_document_rtype = True
typehints_use_signature = True
typehints_use_signature_return = True
always_document_param_types = True
autodoc_type_aliases = {
    "Agent": "haive.agents.base.Agent",
    "StateSchema": "haive.core.schema.StateSchema",
    "Engine": "haive.core.engine.Engine",
    "Tool": "haive.core.tools.Tool",
    "Graph": "haive.core.graph.BaseGraph",
}

# === SPHINX DESIGN - ENHANCED CONTENT ===
# No additional configuration needed - works out of the box

# === SPHINX TABS - TABBED CONTENT ===
# No additional configuration needed - works out of the box

# === COPY BUTTON ===
copybutton_prompt_text = (
    r">>> |\\.\\.\\. |\\$ |In \\[\\d*\\]: | {2,5}\\.\\.\\.: | {5,8}: "
)
copybutton_prompt_is_regexp = True
copybutton_exclude = ".linenos, .gp"

# === MYST PARSER - MARKDOWN SUPPORT ===
myst_enable_extensions = [
    "deflist",
    "tasklist",
    "colon_fence",
    "smartquotes",
    "linkify",
    "strikethrough",
    "dollarmath",
    "substitution",
    "attrs_inline",
    "attrs_block",
]

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
    }
});
"""

# === SPHINX GALLERY - EXAMPLE GALLERIES ===
sphinx_gallery_conf = {
    "examples_dirs": [
        # Only use directories that actually exist
        "../../packages/haive-agents/examples",
        "../../packages/haive-tools/examples",
        "../../packages/haive-games/examples",
    ],
    "gallery_dirs": [
        # Corresponding output directories
        "auto_examples/agents",
        "auto_examples/tools",
        "auto_examples/games",
    ],
    "filename_pattern": "/.*tutorial|.*guide|.*example",
    "ignore_pattern": "__init__.py|debug_*|test_*",
    "download_all_examples": True,
    "show_memory": True,
    "remove_config_comments": True,
    "expected_failing_examples": [],
    "thumbnail_size": (300, 200),
    "subsection_order": "ExplicitOrder",
    "within_subsection_order": "FileNameSortKey",
    "show_signature": True,
    "plot_gallery": False,  # We don't need matplotlib plots
    "first_notebook_cell": "%matplotlib inline",
    "last_notebook_cell": "# End of example",
    # Enhanced gallery features
    "promote_jupyter_magic": True,
    "binder_conf": {
        "org": "haive",
        "repo": "haive",
        "branch": "main",
        "binderhub_url": "https://mybinder.org",
        "dependencies": ["../../pyproject.toml"],
    },
    "gallery_dirs_config": {
        "gallery_beginner": {
            "expected_failing_examples": [],
            "description": "🌱 Beginner-friendly tutorials for your first Haive agents",
        },
        "gallery_intermediate": {
            "expected_failing_examples": [],
            "description": "🌿 Intermediate patterns for multi-agent coordination",
        },
        "gallery_advanced": {
            "expected_failing_examples": [],
            "description": "🌲 Advanced workflows and custom patterns",
        },
        "gallery_games": {
            "expected_failing_examples": [],
            "description": "🎮 AI agents playing games and strategic thinking",
        },
    },
}

# === JUPYTER CACHE - NOTEBOOK INTEGRATION ===
jupyter_cache = "../../.jupyter_cache"
jupyter_execute_notebooks = "cache"
execution_timeout = 600  # 10 minutes for complex examples
execution_show_tb = "short"  # Show short tracebacks on errors
execution_in_temp = False  # Execute in project directory

# === SPHINX-EXEC-DIRECTIVE - INLINE CODE EXECUTION ===
exec_code_working_dir = "../.."  # Project root
exec_code_example_dir = "examples/executed"
exec_code_source_folders = ["packages"]  # Where to look for imports
exec_code_add_conf_path = True  # Add conf.py path to sys.path

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
html_baseurl = "https://haive.readthedocs.io/"  # Required for sitemap generation

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

codeautolink_concat_default = True  # Link to default Python docs
codeautolink_warn_on_missing_inventory = False  # Don't warn on missing

# === READTHEDOCS SEARCH ===
# Configuration handled automatically

# === INTERSPHINX ===
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "langchain": ("https://python.langchain.com/", None),
    "pydantic": ("https://docs.pydantic.dev/", None),
    "numpy": ("https://numpy.org/doc/stable/", None),
    "pandas": ("https://pandas.pydata.org/docs/", None),
}

# === MOCK IMPORTS ===
autodoc_mock_imports = [
    "torch",
    "tensorflow",
    # Remove tool mocking to enable proper documentation
]

# ==============================================================================
# Pygments Configuration for Better Code Contrast
# ==============================================================================

# Enhanced pygments styling for better code readability
pygments_style = "default"  # Light mode - good contrast
pygments_dark_style = "github-dark"  # Dark mode - accessible colors

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
nitpicky = False  # Don't fail on missing references
keep_warnings = True  # Keep warnings in output
autodoc_warningiserror = False  # Don't treat autodoc warnings as errors
autoapi_keep_files = True  # Keep generated API files for debugging

# AutoAPI error handling
autoapi_ignore = [
    "**/test_*.py",
    "**/tests/**",
    "**/*_test.py",
    "**/demo*.py",
    "**/debug*.py",
    "**/bin/**",
    "**/cli.py",
    "**/litellm_cli.py",
    "**/aug_llms.py",
    "**/example*.py",
    "**/logger.py",  # Ignore logger modules
    "**/*logger*",  # Ignore anything with logger in name
    "**/examples/**",  # Ignore examples
    "**/scripts/**",  # Ignore scripts
    "**/*_example.py",  # Ignore example files
    "**/blackjack/**",  # Ignore game examples
    "**/app.py",  # Ignore app files
    "**/main.py",  # Ignore main files
    "**/background_process_manager/**",
    "**/automatic_test_case_generator/**",
    "**/code_smell_detector/**",
    "**/complexity_analyzer/**",
    "**/universal_loader_demo/**",  # Add this specific problem directory
    "**/*demo*/**",  # Ignore all demo directories
    "**/create_agentic_router_declarative*",  # Ignore this specific problem file
    "**/chain/examples/**",  # Ignore chain examples
    "**/conversation/social_media/example.py",  # Syntax error: unmatched '}'
    "**/document_modifiers/kg/kg_base/example.py",  # Syntax error: unterminated string
    "**/rag/db_rag/graph_db/example.py",  # Syntax error: indentation
    "**/reasoning_and_critique/lats/example.py",  # Syntax error: indentation
    "**/reasoning_and_critique/self_discover/example.py",  # Syntax error: indentation
    "**/reasoning_and_critique/tot/modular/example.py",  # Syntax error: indentation
    "**/react_class/react_agent2/example.py",  # Syntax error: indentation
    "**/conversation/collaberative/example.py",  # Syntax error: indentation
]

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
    logger.info("Running optimized Sphinx setup function")

    # Ensure directories exist
    static_dir = conf_dir / "_static"
    static_dir.mkdir(exist_ok=True)

    images_dir = static_dir / "images"
    images_dir.mkdir(exist_ok=True)

    # Add custom CSS for enhanced styling
    app.add_css_file("haive-enhanced.css")

    # Connect autoapi hooks for cleaner URLs (disabled when autoapi is off)
    # app.connect("autoapi-skip-member", autoapi_skip_member)
    # app.connect("autodoc-process-docstring", autoapi_process_docstring)

    return {
        "version": "1.0",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }


# ==============================================================================
# Sphinx-Jinja2 Configuration for Agent Demos
# ==============================================================================

# Import agent demo data
import sys

sys.path.insert(0, str(conf_dir))
from agent_cache_loader import get_agent_demo_context, get_available_agent_types
from agent_demo_data import AVAILABLE_AGENTS, get_agent_context

# Configure Jinja2 contexts for sphinx-jinja2
jinja2_contexts = {
    "agent_demo": {
        "get_agent_context": get_agent_context,
        "available_agents": AVAILABLE_AGENTS,
        # New cached data functions
        "get_agent_demo_context": get_agent_demo_context,
        "get_available_agent_types": get_available_agent_types,
    }
}

# Enable debug mode for development
jinja2_debug = False
