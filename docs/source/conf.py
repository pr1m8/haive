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
    # Core API documentation - USING YOUR POWERFUL EXTENSIONS!
    "autoapi.extension",              # 🚀 Better than autodoc+autosummary
    "sphinx.ext.napoleon",            # Google docstrings - PROPERLY CONFIGURED
    "sphinx.ext.viewcode",            # Source code links - CRITICAL FOR HYPERLINKS
    "sphinx.ext.linkcode",            # GitHub source links - ADDED FOR GITHUB LINKS
    "sphinx.ext.intersphinx",         # Cross-references (disabled offline)
    
    # Enhanced display - YOUR INSTALLED EXTENSIONS
    "sphinx_autodoc_typehints",       # 🎨 Beautiful type hints - WORKS WITH GOOGLE STYLE
    "sphinx_copybutton",              # Copy code blocks
    "sphinx_design",                  # 🎨 Cards, grids, badges
    "sphinx_tabs",                    # 📑 Tabbed content
    "sphinx_togglebutton",            # 🔽 Collapsible sections
    "sphinx_exec_directive",          # ⚡ Live code execution
    "myst_parser",                    # Markdown support
    "sphinxcontrib.mermaid",          # 📊 Diagrams
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
    "**/scripts/**",  # Exclude script directories
    "**/debug*.py",   # Exclude debug files
]

# ==============================================================================
# HTML Theme Configuration
# ==============================================================================

# Choose PyData Sphinx Theme - User preference!
html_theme = "pydata_sphinx_theme"
html_title = "Haive Documentation"
html_short_title = "Haive"

# Static files
html_static_path = ["_static"]

# Enhanced CSS for better contrast and styling
html_css_files = [
    "custom.css",  # Keep existing custom styles
]

html_js_files = [
    "agent-visualization.js",  # Agent demos
]

# PyData theme options - Professional & Scientific with enhanced navigation
html_theme_options = {
    # Fix navigation and contrast issues
    "navbar_align": "left",
    "navbar_center": ["navbar-nav"],
    "secondary_sidebar_items": ["page-toc", "edit-this-page"],
    
    # GitHub integration
    "github_url": "https://github.com/will-astley/haive",
    "use_edit_page_button": True,
    
    # Enhanced navigation for better visibility
    "show_toc_level": 2,
    "navigation_depth": 4,
    "collapse_navigation": False,
    "navigation_with_keys": True,
    
    # Search improvements
    "search_bar_text": "Search Haive docs...",
    "search_bar_position": "navbar",
    
    # Header with theme switcher
    "navbar_end": ["navbar-icon-links", "theme-switcher"],
    "icon_links": [
        {
            "name": "GitHub", 
            "url": "https://github.com/will-astley/haive",
            "icon": "fa-brands fa-github",
        },
    ],
    
    # Theme switching for better contrast
    "switcher": {
        "json_url": "_static/switcher.json",
        "version_match": "latest"
    },
    
    # Better contrast with accessible pygments
    "pygments_light_style": "default",
    "pygments_dark_style": "github-dark",
    
    # Announcement banner
    "announcement": "🤖 <b>Haive AI Agent Framework</b> - Build intelligent agents with ease!",
    
    # Footer
    "footer_items": ["copyright", "sphinx-version"],
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
# Type hints configuration - makes types clickable!
autodoc_typehints = "description"  # Show in description for cleaner signatures
typehints_document_rtype = True
typehints_use_signature = True
typehints_use_signature_return = True
always_document_param_types = True
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

# AutoAPI - MUCH BETTER than autosummary!
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
autoapi_options = [
    "members",
    "undoc-members",
    "show-inheritance", 
    "show-module-summary",
    "imported-members",
]
autoapi_keep_files = True
autoapi_add_toctree_entry = True
autoapi_member_order = "bysource"
autoapi_python_class_content = "both"
autoapi_ignore = [
    "**/tests/**",
    "**/test_*.py", 
    "**/*_test.py",
    "**/scripts/**",
    "**/debug*.py",
    "**/example*.py",
    "**/demo*.py",
]

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

# Intersphinx - disabled temporarily due to network issues
# intersphinx_mapping = {
#     "python": ("https://docs.python.org/3", None),
#     "pydantic": ("https://docs.pydantic.dev/latest/", None), 
#     "langchain": ("https://api.python.langchain.com/en/latest/", None),
# }

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


# ==============================================================================
# GitHub Source Links Configuration (for sphinx.ext.linkcode)
# ==============================================================================

def linkcode_resolve(domain, info):
    """Resolve function to link to GitHub source code.
    
    This enables [source] links next to every function/class that link
    directly to the GitHub repository source code.
    """
    if domain != 'py':
        return None
    if not info['module']:
        return None
    
    # Extract package name from module path
    module_parts = info['module'].split('.')
    if len(module_parts) < 2 or module_parts[0] != 'haive':
        return None
    
    # Map haive.package to packages/haive-package structure
    package_name = module_parts[1]
    package_dir = f"haive-{package_name}"
    
    # Build the file path
    submodule_path = '/'.join(module_parts[2:]) if len(module_parts) > 2 else ''
    if submodule_path:
        filename = f"packages/{package_dir}/src/haive/{package_name}/{submodule_path}.py"
    else:
        filename = f"packages/{package_dir}/src/haive/{package_name}/__init__.py"
    
    # Return GitHub link
    return f"https://github.com/will-astley/haive/blob/main/{filename}"


# ==============================================================================
# Pygments Configuration for Better Code Contrast
# ==============================================================================

# Enhanced pygments styling for better code readability
pygments_style = "default"  # Light mode - good contrast
pygments_dark_style = "github-dark"  # Dark mode - accessible colors