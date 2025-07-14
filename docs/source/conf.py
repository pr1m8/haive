"""Sphinx configuration for Haive documentation.

Configuration for building documentation for the Haive namespaced monorepo.
Uses Google-style docstrings and works with poetry/nox build system.
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
package_names = [
    "haive-core",
    "haive-agents",
    "haive-tools",
    "haive-games",
    "haive-dataflow",
    "haive-prebuilt",
    "haive-mcp",
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
# Extensions Configuration
# ==============================================================================

extensions = [
    # Core Sphinx extensions
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.viewcode",
    "sphinx.ext.napoleon",
    "sphinx.ext.intersphinx",
    "sphinx.ext.githubpages",
    # Enhanced documentation
    "sphinx_copybutton",
    "sphinx_design",
    "myst_parser",
    "sphinxcontrib.mermaid",
    # Custom extensions  
    "games_autodoc",
]

# ==============================================================================
# Source File Configuration
# ==============================================================================

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
    "**/example.py",
    "**/examples/**",
    "examples/**",
    "**/ui.py",
    "**/demo.py",
    "**/*.egg-info/**",
    "generated/**",
    "_archive/**",
    "conf_*.py",
]

# ==============================================================================
# HTML Theme Configuration
# ==============================================================================

html_theme = "furo"
html_title = "Haive Documentation"
html_short_title = "Haive"

# Static files
html_static_path = ["_static"]

# Enhanced CSS for better styling and syntax highlighting
html_css_files = [
    "haive-docs-enhanced.css",  # Comprehensive styling fixes
    "api-showcase.css",  # Beautiful gradient cards (enhanced)
]

html_js_files = [
    "agent-visualization.js",  # Agent demos
]

# Modern theme options
html_theme_options = {
    # Branding
    "light_logo": "images/haive-logo-light.svg",
    "dark_logo": "images/haive-logo-dark.svg",
    # Colors
    "light_css_variables": {
        "color-brand-primary": "#0f62fe",
        "color-brand-content": "#4589ff",
        "color-foreground-primary": "#161616",
        "color-foreground-secondary": "#525252",
        "color-background-primary": "#ffffff",
        "color-background-secondary": "#f8f9fb",
    },
    "dark_css_variables": {
        "color-brand-primary": "#4589ff",
        "color-brand-content": "#8a3ffc",
        "color-foreground-primary": "#f4f4f4",
        "color-foreground-secondary": "#c6c6c6",
        "color-background-primary": "#161616",
        "color-background-secondary": "#1a1a1a",
    },
    # Navigation
    "sidebar_hide_name": False,
    "navigation_depth": 3,
    # Features
    "announcement": (
        '<div style="text-align: center; font-weight: 600;">'
        "🤖 <strong>Haive AI Agent Framework</strong> - "
        "Building intelligent agents with Google-style documentation"
        "</div>"
    ),
    # Footer
    "footer_icons": [
        {
            "name": "GitHub",
            "url": "https://github.com/will-astley/haive",
            "html": '<svg height="16" width="16" viewBox="0 0 16 16"><path fill="currentColor" d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"/></svg>',
        },
    ],
    # Source links
    "source_repository": "https://github.com/will-astley/haive/",
    "source_branch": "main",
    "source_directory": "docs/source/",
}

# ==============================================================================
# Extension Configurations
# ==============================================================================

# Autodoc settings - optimized for Google-style docstrings
autodoc_default_options = {
    "members": True,
    "undoc-members": True,
    "show-inheritance": True,
    "special-members": "__init__",
    "member-order": "bysource",
    "exclude-members": "__weakref__",
    "inherited-members": True,
}
autodoc_typehints = "both"  # Show types in signature AND description
autodoc_typehints_format = "short"
autodoc_class_signature = "separated"
autodoc_type_aliases = {
    # Simplify common Haive types
    "Agent": "haive.agents.base.Agent",
    "StateSchema": "haive.core.schema.StateSchema",
    "Engine": "haive.core.engine.Engine",
    "Tool": "haive.core.tools.Tool",
    "Graph": "haive.core.graph.BaseGraph",
    "RunnableConfig": "Dict[str, Any]",
}

# Mock imports for missing modules
autodoc_mock_imports = [
    # Known missing modules that don't exist
    "haive.tools.api",
    "haive.tools.utility",
    "haive.tools.code",
    "haive.tools.search",
    "haive.tools.math",
    "haive.tools.data",
    "haive.agents.rag.self_rag",
    "haive.core.schema.compatibility",
    "haive.agents.planning.llm_compiler",
    "haive.agents.reasoning_and_critique.reflection",
    "haive.agents.conversation.collaborative",
    "haive.agents.supervisor",
    "haive.core.engine.loaders",
    "haive.agents.document_modifiers.kg",
    "haive.agents.document_modifiers.kg.kg_base",
    "haive.agents.document_modifiers.kg.kg_iterative_refinement",
    "haive.agents.document_modifiers.kg.kg_map_merge",
    "haive.agents.document_modifiers.summarizer",
    "haive.agents.document_modifiers.summarizer.iterative_refinement",
    "haive.agents.rag.db_rag",
    "haive.agents.reasoning_and_critique",
    "haive.agents.research",
    "haive.core.engine.document",
    "haive.core.persistence.create_checkpointer",
    "haive.core.persistence.create_memory_checkpointer",
    "haive.core.persistence.create_postgres_checkpointer",
    # Only mock if they cause issues during build
    "torch",
    "tensorflow",
]

# Autosummary - fixed configuration for proper documentation generation
autosummary_generate = True
autosummary_generate_overwrite = True  # Overwrite to keep docs up to date
autosummary_imported_members = True  # Import members for proper documentation
autosummary_ignore_module_all = False
autosummary_filename_map = {}

# Make autosummary work properly with our module structure
autosummary_mock_imports = autodoc_mock_imports

# Tell autosummary to treat these as modules
def autosummary_get_type(app, obj, parent):
    """Force certain patterns to be recognized as modules."""
    if obj and hasattr(obj, "__name__"):
        name = obj.__name__
        # Force all haive.* submodules to be treated as modules
        for package in ["core", "agents", "tools", "games", "dataflow", "mcp", "prebuilt"]:
            if name.startswith(f"haive.{package}.") and "." in name[len(f"haive.{package}."):]:
                return "module"
    return None

# Force autosummary to generate proper module files
autosummary_context = {
    "fullname": lambda name: name,
    "module": lambda name: name,
    "objname": lambda name: name.split(".")[-1],
}

# Napoleon (Google docstrings) - optimized settings
napoleon_google_docstring = True
napoleon_numpy_docstring = False  # We use Google style, not NumPy
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
napoleon_type_aliases = {
    # Haive-specific type aliases
    "Agent": "haive.agents.base.Agent",
    "StateSchema": "haive.core.schema.StateSchema",
    "Engine": "haive.core.engine.Engine",
    "Tool": "haive.core.tools.Tool",
    "Graph": "haive.core.graph.BaseGraph",
    "RunnableConfig": "Dict[str, Any]",
}
napoleon_attr_annotations = True
napoleon_custom_sections = [
    ("Type Parameters", "params_style"),
    ("State Schema", "params_style"),
]

# Copy button
copybutton_prompt_text = r">>> |\.\.\. |\$ |In \[\d*\]: | {2,5}\.\.\.: | {5,8}: "
copybutton_prompt_is_regexp = True
copybutton_exclude = ".linenos"

# MyST Markdown
myst_enable_extensions = [
    "deflist",
    "tasklist",
    "colon_fence",
    "smartquotes",
    "linkify",
    "strikethrough",
    "dollarmath",
    "substitution",
]

# Intersphinx - link to other projects
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "pydantic": ("https://docs.pydantic.dev/latest/", None),
    "langchain": ("https://api.python.langchain.com/en/latest/", None),
}

# Mermaid diagrams
mermaid_version = "10.6.1"

# ==============================================================================
# Build Configuration
# ==============================================================================

# Performance
templates_path = ["_templates"]

# Autosummary template path
autosummary_template_path = ["_templates/autosummary"]

# Suppress specific warnings
suppress_warnings = [
    "autosummary.import_cycle",
    "autodoc.import_object",
    "ref.citation",
    "misc.highlighting_failure",
    "autosummary",
    "autodoc",
]

# Set autodoc to continue on import failure
autodoc_warningiserror = False
autodoc_inherit_docstrings = True

# Language
language = "en"

# Master document
master_doc = "index"

# ==============================================================================
# HTML Output Settings
# ==============================================================================

html_copy_source = False  # Don't include source files
html_show_sourcelink = True
html_show_sphinx = False
html_show_copyright = True

# Search
html_search_language = "en"

# ==============================================================================
# LaTeX Output (for PDF generation)
# ==============================================================================

latex_elements = {
    "papersize": "a4paper",
    "pointsize": "10pt",
    "preamble": r"""
\usepackage{lmodern}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
""",
    "fncychap": r"\usepackage[Bjornstrup]{fncychap}",
    "printindex": r"\footnotesize\raggedright\printindex",
}

latex_documents = [
    (master_doc, "haive.tex", "Haive Documentation", author, "manual"),
]

# ==============================================================================
# Custom Event Handlers
# ==============================================================================

def skip_submodules(app, what, name, obj, skip, options):  # noqa: PLR0913
    """Skip submodules to avoid duplication in autosummary."""
    if what == "module" and "." in name:
        # Skip submodules in autosummary
        return True
    return skip

def setup(app):
    """Setup function for custom modifications."""
    logger.info("Running Sphinx setup function")

    # Log what packages we're documenting
    logger.info(f"Package names configured: {package_names}")

    # Test import all packages
    for package in ["core", "agents", "tools", "games", "dataflow", "mcp", "prebuilt"]:
        try:
            module = __import__(f"haive.{package}")
            logger.info(f"haive.{package} imported successfully from: {module.__file__}")
            logger.info(
                f"haive.{package}.__all__ = {getattr(module, '__all__', 'NOT DEFINED')}"
            )
        except Exception as e:
            logger.exception(f"Failed to import haive.{package}: {type(e).__name__}: {e}")

    # Ensure directories exist
    static_dir = conf_dir / "_static"
    static_dir.mkdir(exist_ok=True)

    # Create images directory if it doesn't exist
    images_dir = static_dir / "images"
    images_dir.mkdir(exist_ok=True)

    # Add monorepo import failure handler
    def handle_import_failure(app, what, name, obj, options, lines):
        """Handle import failures gracefully with helpful messages."""
        if name in autodoc_mock_imports:
            if "haive.tools.api" in name:
                lines.insert(0, ".. warning::")
                lines.insert(1, "")
                lines.insert(
                    2, "   This module has been reorganized. API tools are now in:"
                )
                lines.insert(3, "   ``haive.tools.toolkits.{service_name}``")
                lines.insert(4, "")
            elif "haive.tools.code" in name:
                lines.insert(0, ".. warning::")
                lines.insert(1, "")
                lines.insert(2, "   Code tools have moved to:")
                lines.insert(3, "   ``haive.tools.toolkits.dev``")
                lines.insert(4, "")
            elif "haive.tools.utility" in name:
                lines.insert(0, ".. warning::")
                lines.insert(1, "")
                lines.insert(2, "   Utility tools are now in individual modules:")
                lines.insert(3, "   ``haive.tools.tools.{tool_name}``")
                lines.insert(4, "")

    app.connect("autodoc-process-docstring", handle_import_failure)
    
    # Connect event handlers
    app.connect("autodoc-skip-member", skip_submodules)

    return {
        "version": "1.0",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }