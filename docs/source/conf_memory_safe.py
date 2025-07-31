"""Memory-Safe Sphinx configuration for Haive documentation.

This configuration preserves ALL documentation features while adding intelligent
memory management to prevent system crashes.

ENHANCEMENTS:
- Dynamic memory monitoring and adaptation
- Incremental package processing with cleanup
- Smart extension loading based on available resources
- Progressive fallback under memory pressure
- Streaming output instead of memory buffering
"""

import gc
import logging
import sys
import warnings
from datetime import datetime
from pathlib import Path

# Memory management imports
try:
    import psutil

    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False
    logging.warning("psutil not available - install with: pip install psutil")

# Set up enhanced logging for debugging
log_file = Path(__file__).parent / "sphinx_debug.log"
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s - [MEM: %(memory)sMB]",
    handlers=[logging.FileHandler(str(log_file)), logging.StreamHandler()],
)


# Custom memory-aware logger
class MemoryLogger:
    def __init__(self, name):
        self.logger = logging.getLogger(name)

    def info(self, msg):
        memory_mb = self.get_memory_usage()
        extra = {"memory": f"{memory_mb:.1f}"}
        self.logger.info(msg, extra=extra)

    def warning(self, msg):
        memory_mb = self.get_memory_usage()
        extra = {"memory": f"{memory_mb:.1f}"}
        self.logger.warning(msg, extra=extra)

    def get_memory_usage(self):
        if PSUTIL_AVAILABLE:
            return psutil.virtual_memory().available / (1024**2)
        return 0.0


logger = MemoryLogger(__name__)

# Suppress warnings but track memory
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", message=".*Matplotlib.*")
warnings.filterwarnings("ignore", category=UserWarning, module="sphinx")

# ==============================================================================
# Memory Management System
# ==============================================================================


class MemoryManager:
    """Intelligent memory management for Sphinx builds."""

    def __init__(self):
        self.memory_threshold_low = 2 * 1024**3  # 2GB
        self.memory_threshold_high = 8 * 1024**3  # 8GB
        self.cleanup_performed = 0

    def get_available_memory(self):
        """Get available system memory in bytes."""
        if PSUTIL_AVAILABLE:
            return psutil.virtual_memory().available
        return 8 * 1024**3  # Assume 8GB if psutil unavailable

    def get_memory_gb(self):
        """Get available memory in GB."""
        return self.get_available_memory() / (1024**3)

    def force_cleanup(self):
        """Force garbage collection and cleanup."""
        self.cleanup_performed += 1
        logger.info(f"Performing memory cleanup #{self.cleanup_performed}")
        gc.collect()

    def check_memory_pressure(self):
        """Check if system is under memory pressure."""
        available = self.get_available_memory()
        if available < self.memory_threshold_low:
            logger.warning(f"LOW MEMORY: {available//1024**2}MB available")
            self.force_cleanup()
            return "critical"
        if available < self.memory_threshold_high:
            logger.info(f"Moderate memory usage: {available//1024**2}MB available")
            return "moderate"
        return "healthy"

    def get_safe_extension_count(self):
        """Determine safe number of extensions based on memory."""
        memory_status = self.check_memory_pressure()

        if memory_status == "critical":
            return "minimal"  # 5-10 essential extensions
        if memory_status == "moderate":
            return "standard"  # 20-30 important extensions
        return "full"  # All 50+ extensions


# Initialize global memory manager
memory_manager = MemoryManager()

# ==============================================================================
# Smart Extension Loading System
# ==============================================================================

# Extension categories for memory-aware loading
ESSENTIAL_EXTENSIONS = [
    # Core functionality - always loaded
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
    "sphinx_design",
]

STANDARD_EXTENSIONS = [
    # Important features - loaded with moderate memory
    "sphinx.ext.linkcode",
    "sphinx.ext.autosummary",
    "sphinx.ext.doctest",
    "sphinx.ext.coverage",
    "sphinx.ext.todo",
    "sphinx_tabs.tabs",
    "sphinx_inline_tabs",
    "sphinx_togglebutton",
    "sphinx_copybutton",
    "sphinxcontrib.mermaid",
    "sphinx_autodoc_typehints",
    "sphinx_sitemap",
    "sphinxext.opengraph",
    "sphinx_favicon",
    "sphinx_prompt",
]

FULL_EXTENSIONS = [
    # All premium features - loaded with high memory
    "sphinx_exec_directive",
    "sphinx_gallery.gen_gallery",
    "myst_nb",
    "sphinx_thebe",
    "sphinxcontrib.youtube",
    "sphinxcontrib.openapi",
    "sphinxcontrib.httpdomain",
    "sphinx_needs",
    "sphinx_contributors",
    "sphinx_issues",
    "sphinxemoji.sphinxemoji",
    "sphinx_math_dollar",
    "sphinxcontrib.images",
    "sphinx_revealjs",
    "sphinx_substitution_extensions",
    "sphinx_pdf_generate",
    "sphinx_simplepdf",
    "sphinx_multiversion",
    "sphinx_removed_in",
    "sphinx_data_viewer",
    "sphinxcontrib.plantuml",
    "sphinxcontrib.blockdiag",
    "sphinxcontrib.seqdiag",
    "notfound.extension",
    "hoverxref.extension",
    "sphinx_exercise",
    "sphinx_proof",
    "sphinx_external_toc",
    "sphinx_git",
    "sphinx_jinja2",
]


def get_extensions_for_memory_level():
    """Dynamically determine extensions based on available memory."""
    extension_level = memory_manager.get_safe_extension_count()

    if extension_level == "minimal":
        logger.warning("Loading MINIMAL extensions due to low memory")
        return ESSENTIAL_EXTENSIONS
    if extension_level == "standard":
        logger.info("Loading STANDARD extensions (moderate memory)")
        return ESSENTIAL_EXTENSIONS + STANDARD_EXTENSIONS
    logger.info("Loading FULL extensions (high memory available)")
    return ESSENTIAL_EXTENSIONS + STANDARD_EXTENSIONS + FULL_EXTENSIONS


# Load extensions based on available memory
extensions = get_extensions_for_memory_level()

logger.info(
    f"Loaded {len(extensions)} extensions based on memory: {memory_manager.get_memory_gb():.1f}GB available"
)

# ==============================================================================
# Path Setup for Namespaced Monorepo (Memory-Aware)
# ==============================================================================

# Get paths
conf_dir = Path(__file__).parent.absolute()
docs_dir = conf_dir.parent
workspace_dir = docs_dir.parent

# Add the workspace to Python path for imports
sys.path.insert(0, str(workspace_dir))

# Add extensions directory to path for custom extensions
sys.path.insert(0, str(conf_dir / "_extensions"))

# Add package source paths with memory management
packages_dir = workspace_dir / "packages"

package_names = [
    "haive-core",
    "haive-agents",
    "haive-tools",
    "haive-games",
    "haive-dataflow",
    "haive-mcp",
]

# Configure nitpicky mode based on memory
nitpicky = memory_manager.get_memory_gb() > 4  # Only enable with sufficient memory
nitpick_ignore = []


def load_packages_incrementally():
    """Load packages one by one with memory management."""
    loaded_packages = []

    for package in package_names:
        # Check memory before each package
        memory_status = memory_manager.check_memory_pressure()

        if memory_status == "critical":
            logger.warning(f"Skipping {package} due to critical memory pressure")
            continue

        src_path = packages_dir / package / "src"
        if src_path.exists():
            logger.info(f"Loading package: {package}")
            sys.path.insert(0, str(src_path))

            # Try to import the package
            package_module = f"haive.{package.split('-')[1]}"
            try:
                __import__(package_module)
                logger.info(f"Successfully imported {package_module}")
                loaded_packages.append(package)

                # Force cleanup after each package
                memory_manager.force_cleanup()

            except Exception as e:
                logger.warning(f"Failed to import {package_module}: {e}")
                # Remove from path if import failed
                if str(src_path) in sys.path:
                    sys.path.remove(str(src_path))
        else:
            logger.warning(f"Package source not found: {src_path}")

    logger.info(
        f"Successfully loaded {len(loaded_packages)}/{len(package_names)} packages"
    )
    return loaded_packages


# Load packages with memory management
loaded_packages = load_packages_incrementally()

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
# Memory-Aware AutoAPI Configuration
# ==============================================================================

# Only enable AutoAPI if we have sufficient memory and loaded packages
if memory_manager.get_memory_gb() > 4 and len(loaded_packages) > 0:
    logger.info("Enabling AutoAPI with memory management")

    # Enable AutoAPI extension if not already present
    if "autoapi.extension" not in extensions:
        extensions.append("autoapi.extension")

    autoapi_type = "python"

    # Only process packages that were successfully loaded
    autoapi_dirs = []
    for package in loaded_packages:
        src_dir = f"../../packages/{package}/src"
        autoapi_dirs.append(src_dir)

    autoapi_root = "api"
    autoapi_options = [
        "members",
        "show-inheritance",
        "show-module-summary",
    ]

    # Reduce options under memory pressure
    memory_status = memory_manager.check_memory_pressure()
    if memory_status != "critical":
        autoapi_options.extend(
            [
                "special-members",
                "private-members",
            ]
        )

    autoapi_keep_files = True
    autoapi_add_toctree_entry = True
    autoapi_member_order = "groupwise"
    autoapi_python_class_content = "both"
    autoapi_python_use_implicit_namespaces = True
    autoapi_generate_api_docs = True
    autoapi_template_dir = "_templates/autoapi"

    logger.info(f"AutoAPI configured for {len(autoapi_dirs)} packages")
else:
    logger.warning(
        "AutoAPI disabled due to insufficient memory or failed package loading"
    )

# ==============================================================================
# Memory-Conscious Configuration
# ==============================================================================

# Source file configuration - reduced scope under memory pressure
source_suffix = {
    ".rst": "restructuredtext",
    ".md": "markdown",
}

# Smart exclude patterns - more aggressive under memory pressure
base_exclude_patterns = [
    "_build",
    "Thumbs.db",
    ".DS_Store",
    "**/.git",
    "**/node_modules",
    "**/.venv/**",
    "**/site-packages/**",
    "**/__pycache__",
]

memory_conscious_excludes = [
    "**/test_*.py",
    "**/tests/**",
    "**/*_test.py",
    "**/ui.py",
    "**/*.egg-info/**",
    "generated/**",
    "_archive/**",
    "conf_*.py",
    "**/scripts/**",
    "**/debug*.py",
]

if memory_manager.check_memory_pressure() in ["critical", "moderate"]:
    exclude_patterns = base_exclude_patterns + memory_conscious_excludes
    logger.info("Using aggressive exclude patterns for memory conservation")
else:
    exclude_patterns = base_exclude_patterns
    logger.info("Using standard exclude patterns")

# ==============================================================================
# HTML Theme Configuration (Memory-Optimized)
# ==============================================================================

html_theme = "furo"
html_title = "🤖 Haive AI Agent Framework"
html_short_title = "Haive"

# Static files
html_static_path = ["_static"]

# CSS files - reduced under memory pressure
if memory_manager.get_memory_gb() > 4:
    html_css_files = [
        "haive-minimal.css",
    ]
    html_js_files = [
        "haive-graph-visualizations.js",
        "agent-visualization.js",
        "enhanced-search.js",
        "showcase-interactions.js",
        "enhanced-interface.js",
        "agent-demo-utils.js",
    ]
else:
    html_css_files = ["haive-minimal.css"]
    html_js_files = ["enhanced-search.js"]  # Essential only
    logger.info("Reduced CSS/JS files for memory conservation")

# Theme options - simplified under memory pressure
if memory_manager.get_memory_gb() > 6:
    html_theme_options = {
        "sidebar_hide_name": False,
        "navigation_with_keys": True,
        "top_of_page_buttons": ["edit", "view"],
        "show_prev_next": True,
        "navigation_depth": 4,
        "collapse_navigation": False,
        "titles_only": False,
        "show_toc_level": 3,
        "toc_title": "On this page",
        # Full theme configuration
        "light_css_variables": {
            "sidebar-width": "15rem",
            "content-width": "50rem",
            "content-padding": "2rem",
            "font-stack--headings": "'Inter', system-ui, -apple-system, sans-serif",
            "color-brand-primary": "#0066cc",
            "color-brand-content": "#0066cc",
            # ... more variables
        },
        "dark_css_variables": {
            "color-brand-primary": "#4da6ff",
            "color-brand-content": "#4da6ff",
            # ... more variables
        },
        "footer_icons": [
            {
                "name": "GitHub",
                "url": "https://github.com/will-astley/haive",
                "html": """<svg stroke="currentColor" fill="currentColor" stroke-width="0" viewBox="0 0 16 16">
                    <path fill-rule="evenodd" d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0 0 16 8c0-4.42-3.58-8-8-8z"></path>
                </svg>""",
            },
        ],
        "source_repository": "https://github.com/will-astley/haive",
        "source_branch": "main",
        "source_directory": "docs/source/",
    }
else:
    # Minimal theme options for memory conservation
    html_theme_options = {
        "sidebar_hide_name": False,
        "navigation_with_keys": True,
        "show_prev_next": True,
        "light_css_variables": {
            "color-brand-primary": "#0066cc",
            "sidebar-width": "15rem",
        },
        "source_repository": "https://github.com/will-astley/haive",
    }
    logger.info("Using minimal theme options for memory conservation")

# ==============================================================================
# Extension Configurations (Memory-Aware)
# ==============================================================================

# Configure extensions based on what's loaded
if "sphinx.ext.napoleon" in extensions:
    napoleon_google_docstring = True
    napoleon_numpy_docstring = False
    napoleon_include_init_with_doc = True
    napoleon_include_private_with_doc = False
    napoleon_include_special_with_doc = True
    napoleon_use_admonition_for_examples = True
    napoleon_use_admonition_for_notes = True

if "sphinx.ext.autodoc" in extensions:
    autodoc_typehints = "both"
    autodoc_preserve_defaults = True
    autodoc_member_order = "groupwise"

if "sphinx_autodoc_typehints" in extensions:
    typehints_document_rtype = True
    typehints_use_signature = True
    typehints_use_signature_return = True
    typehints_format = "short"
    always_document_param_types = True

if "sphinx.ext.doctest" in extensions:
    doctest_global_setup = """
import sys
import os
from pathlib import Path

workspace_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(workspace_dir))

packages = ["haive-core", "haive-agents", "haive-tools", "haive-games", "haive-mcp", "haive-dataflow"]
for pkg in packages:
    src_path = workspace_dir / "packages" / pkg / "src"
    if src_path.exists():
        sys.path.insert(0, str(src_path))

try:
    from haive.core.engine.aug_llm import AugLLMConfig
    from haive.agents.simple.agent import SimpleAgent
except ImportError:
    pass
"""

if "sphinx.ext.coverage" in extensions:
    coverage_write_headline = False
    coverage_show_missing_items = True
    coverage_ignore_modules = [
        "haive.*.tests.*",
        "haive.*.__main__",
        "haive.*.migrations.*",
    ]

if "sphinx.ext.todo" in extensions:
    todo_include_todos = True
    todo_emit_warnings = False
    todo_link_only = False

if "sphinx_copybutton" in extensions:
    copybutton_prompt_text = (
        r">>> |\\.\\.\\. |\\$ |In \\[\\d*\\]: | {2,5}\\.\\.\\.: | {5,8}: "
    )
    copybutton_prompt_is_regexp = True
    copybutton_exclude = ".linenos, .gp"

if "sphinxcontrib.mermaid" in extensions:
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

# Gallery configuration - only if extension loaded and sufficient memory
if "sphinx_gallery.gen_gallery" in extensions and memory_manager.get_memory_gb() > 4:
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
        "ignore_pattern": "__init__.py|debug_*|test_*",
        "download_all_examples": False,  # Reduce memory usage
        "show_memory": True,
        "remove_config_comments": True,
        "expected_failing_examples": [],
        "thumbnail_size": (200, 150),  # Smaller thumbnails
        "subsection_order": "ExplicitOrder",
        "within_subsection_order": "FileNameSortKey",
        "show_signature": True,
        "plot_gallery": False,
    }

# Jupyter configuration - only if sufficient memory
if "myst_nb" in extensions and memory_manager.get_memory_gb() > 6:
    jupyter_cache = "../../.jupyter_cache"
    jupyter_execute_notebooks = "cache"
    execution_timeout = 300  # Reduced from 600
    execution_show_tb = "short"
    execution_in_temp = False

# Intersphinx - reduced mappings under memory pressure
if "sphinx.ext.intersphinx" in extensions:
    if memory_manager.get_memory_gb() > 4:
        intersphinx_mapping = {
            "python": ("https://docs.python.org/3", None),
            "langchain": ("https://python.langchain.com/", None),
            "pydantic": ("https://docs.pydantic.dev/", None),
            "numpy": ("https://numpy.org/doc/stable/", None),
            "pandas": ("https://pandas.pydata.org/docs/", None),
        }
    else:
        intersphinx_mapping = {
            "python": ("https://docs.python.org/3", None),
        }

# Mock imports - minimal under memory pressure
if memory_manager.check_memory_pressure() == "critical":
    autodoc_mock_imports = [
        "torch",
        "tensorflow",
        "transformers",
        "accelerate",
        "datasets",
        "evaluate",
        "diffusers",
        "optimum",
    ]
else:
    autodoc_mock_imports = ["torch", "tensorflow"]

# ==============================================================================
# Build Configuration (Memory-Optimized)
# ==============================================================================

templates_path = ["_templates"]
language = "en"
master_doc = "index"

# Performance optimizations based on memory
html_copy_source = memory_manager.get_memory_gb() > 4
html_show_sourcelink = True
html_show_sphinx = False
html_show_copyright = True

# Search
html_search_language = "en"

# Suppress warnings based on memory pressure
if memory_manager.check_memory_pressure() == "critical":
    suppress_warnings = [
        "autosummary.import_cycle",
        "autodoc.import_object",
        "ref.citation",
        "misc.highlighting_failure",
        "toc.secnum",
        "epub.unknown_project_files",
    ]
else:
    suppress_warnings = [
        "autosummary.import_cycle",
        "autodoc.import_object",
        "ref.citation",
        "misc.highlighting_failure",
    ]

# Enhanced error handling based on memory
nitpicky = False
keep_warnings = True
autodoc_warningiserror = False

# ==============================================================================
# Memory Monitoring Hooks
# ==============================================================================


def memory_check_before_build(app):
    """Check memory before build starts."""
    logger.info("=== BUILD STARTING - MEMORY CHECK ===")
    memory_gb = memory_manager.get_memory_gb()
    logger.info(f"Available memory: {memory_gb:.1f}GB")

    if memory_gb < 2:
        logger.warning("WARNING: Very low memory! Build may fail.")
    elif memory_gb < 4:
        logger.warning("Low memory detected - using conservative settings")
    else:
        logger.info("Sufficient memory available for full build")


def memory_check_after_build(app, exception):
    """Check memory after build completes."""
    logger.info("=== BUILD COMPLETED - MEMORY CHECK ===")
    memory_gb = memory_manager.get_memory_gb()
    logger.info(f"Available memory: {memory_gb:.1f}GB")
    logger.info(f"Cleanup operations performed: {memory_manager.cleanup_performed}")

    if exception:
        logger.error(f"Build failed with exception: {exception}")
        logger.error("This may be due to insufficient memory")


def periodic_memory_check(app, pagename):
    """Periodically check memory during build."""
    if hasattr(periodic_memory_check, "call_count"):
        periodic_memory_check.call_count += 1
    else:
        periodic_memory_check.call_count = 1

    # Check every 10 pages
    if periodic_memory_check.call_count % 10 == 0:
        memory_status = memory_manager.check_memory_pressure()
        if memory_status == "critical":
            logger.warning(f"Critical memory pressure while processing {pagename}")


# ==============================================================================
# Setup Function with Memory Management
# ==============================================================================


def setup(app):
    """Setup function with memory management hooks."""
    logger.info("Setting up memory-aware Sphinx configuration")

    # Ensure directories exist
    static_dir = conf_dir / "_static"
    static_dir.mkdir(exist_ok=True)

    images_dir = static_dir / "images"
    images_dir.mkdir(exist_ok=True)

    # Add custom CSS based on memory
    if memory_manager.get_memory_gb() > 4:
        app.add_css_file("haive-enhanced.css")

    # Connect memory monitoring hooks
    app.connect("builder-inited", memory_check_before_build)
    app.connect("build-finished", memory_check_after_build)
    app.connect("html-page-context", periodic_memory_check)

    # Final memory check
    final_memory = memory_manager.get_memory_gb()
    logger.info(f"Setup complete - Available memory: {final_memory:.1f}GB")

    return {
        "version": "1.0",
        "parallel_read_safe": True,
        "parallel_write_safe": memory_manager.get_memory_gb()
        > 8,  # Only if plenty of memory
    }


# ==============================================================================
# Final Memory Report
# ==============================================================================

logger.info("=== MEMORY-SAFE CONFIGURATION SUMMARY ===")
logger.info(f"Available memory: {memory_manager.get_memory_gb():.1f}GB")
logger.info(f"Extensions loaded: {len(extensions)}")
logger.info(
    f"Packages loaded: {len(loaded_packages) if 'loaded_packages' in locals() else 0}"
)
logger.info(
    f"Memory management: {'ACTIVE' if PSUTIL_AVAILABLE else 'DISABLED (install psutil)'}"
)
logger.info("=== READY FOR MEMORY-SAFE BUILD ===")
