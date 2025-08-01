"""Clean, modular Sphinx configuration for Haive project.

This is the new modular version of the original 1101-line conf.py file.
The original has been backed up as conf.backup.py.

All 40+ extensions and configurations are now imported from the conf_modules/
directory with procedural testing and rich debugging UI.
"""

import sys
from pathlib import Path

# Add conf_modules to Python path for imports
conf_modules_dir = Path(__file__).parent / "conf_modules"
sys.path.insert(0, str(conf_modules_dir))

from extension_configs import (get_all_extension_configs,
                               get_conditional_configs)
# Import extensions with rich debugging
from extensions import get_all_extensions, test_extension_compatibility
from import_diagnostics import get_autodoc_mock_imports_from_diagnosis
from memory import get_memory_safe_sphinx_config, monitor_sphinx_build

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

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = "sphinx"

# =============================================================================
# EXTENSIONS - IMPORTED FROM MODULAR STRUCTURE WITH TESTING
# =============================================================================

# Get all extensions procedurally with rich debugging
extensions = get_all_extensions()

# Apply memory-safe configuration with extension optimization
memory_config = get_memory_safe_sphinx_config(extensions)
extensions = memory_config["extensions"]  # Use memory-optimized extensions
build_recommendations = memory_config["build_recommendations"]

# Get extension-specific configurations
extension_configs = get_all_extension_configs(extensions)
conditional_configs = get_conditional_configs(extensions)

# Apply all configurations to global namespace
globals().update(memory_config)
globals().update(extension_configs)
globals().update(conditional_configs)

# Test extension compatibility (optional, uncomment for detailed testing)
# compatibility_results = test_extension_compatibility()

# =============================================================================
# AUTOAPI CONFIGURATION
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

# Automatically diagnose and configure mock imports
autodoc_mock_imports = get_autodoc_mock_imports_from_diagnosis(autoapi_dirs, str(Path(__file__).parent))
autoapi_root = "api"
autoapi_add_toctree_entry = False
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

# Skip patterns to avoid problematic files during documentation generation
autoapi_ignore = [
    # We'll use sphinx-toolbox to handle generic classes instead
]

# Preprocessing hook to handle Agent[T] pattern
def autoapi_skip_member(app, what, name, obj, skip, options):
    """Skip or modify problematic members."""
    # Let everything through - sphinx-toolbox handles generics
    return skip

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
    "enhanced-docs.css",  # Enhanced styles leveraging 86+ extensions
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
autosummary_generate = True
# Type hint configuration to handle generics
typehints_fully_qualified = False
autodoc_typehints_format = "short"  # Use shorter format
autodoc_type_aliases = {
    'Agent': 'Agent',  # Map problematic generics
    'T': 'T',
}


# =============================================================================
# INTERSPHINX MAPPING
# =============================================================================

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "numpy": ("https://numpy.org/doc/stable/", None),
    "pandas": ("https://pandas.pydata.org/docs/", None),
    "pydantic": ("https://docs.pydantic.dev/latest/", None),
    "langchain": ("https://python.langchain.com/docs/", None),
    "openai": ("https://platform.openai.com/docs/", None),
}

# =============================================================================
# ENHANCED DOCUMENTATION FEATURES (Using 86+ Extensions)
# =============================================================================

# Napoleon settings for Google/NumPy style docstrings
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = False
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = False
napoleon_use_admonition_for_notes = False
napoleon_use_admonition_for_references = False
napoleon_use_ivar = False
napoleon_use_param = True
napoleon_use_rtype = True

# Enhanced template directory (leveraging sphinx-design and other extensions)
templates_path = ["_templates"]

# Enhanced autosummary configuration (using autodocsumm)
if "autodocsumm" in extensions:
    autosummary_generate = True
    autosummary_generate_overwrite = True
    autosummary_imported_members = True
    autodocsumm_generate = True
    autodocsumm_imported_members = True
    autodocsumm_member_order = "bysource"

# Enhanced autodoc configuration (optimized for Pydantic models)
autodoc_default_options.update(
    {
        "show-inheritance": True,
        "member-order": "bysource",
        "special-members": "__init__, __call__, __enter__, __exit__",
    }
)

# Sphinx-design configuration (enhanced UI components)  
if "sphinx_design" in extensions:
    sd_fontawesome_latex = True
    # Removed sd_custom_directives to avoid configuration warnings
    # sd_custom_directives = {
    #     "dropdown": {"inherit": "note"},
    #     "tab-set": {"inherit": "container"},
    #     "grid": {"inherit": "container"},
    # }

# Enhanced copybutton configuration
if "sphinx_copybutton" in extensions:
    copybutton_prompt_text = r">>> |\.\.\. |\$ |In \[\d*\]: | {2,5}\.\.\.: | {5,8}: "
    copybutton_prompt_is_regexp = True
    copybutton_line_continuation_character = "\\"
    copybutton_here_doc_delimiter = "EOT"
    copybutton_selector = "div.highlight > pre"

# Enhanced diagrams (using multiple diagram extensions)
if "sphinxcontrib.mermaid" in extensions:
    mermaid_output_format = "svg"
    mermaid_init_js = """
    mermaid.initialize({
        startOnLoad: true,
        theme: 'default',
        themeVariables: {
            primaryColor: '#2563eb',
            primaryTextColor: '#1f2937',
            primaryBorderColor: '#1d4ed8',
            lineColor: '#374151'
        }
    });
    """

# Enhanced inheritance diagrams
graphviz_output_format = "svg"
inheritance_graph_attrs = {
    "rankdir": "TB",
    "size": '"8.0, 12.0"',
    "fontname": '"Helvetica"',
    "fontsize": "14",
}
inheritance_node_attrs = {
    "color": '"#2563eb"',
    "fillcolor": '"#eff6ff"',
    "style": '"filled"',
    "fontname": '"Helvetica"',
    "fontsize": "12",
}

# Todo extension settings
todo_include_todos = True
todo_emit_warnings = False

# Copy button settings (if sphinx_copybutton is available)
if "sphinx_copybutton" in extensions:
    copybutton_prompt_text = r">>> |\.\.\. |\$ |In \[\d*\]: | {2,5}\.\.\.: | {5,8}: "
    copybutton_prompt_is_regexp = True

# External TOC (if sphinx_external_toc is available)
if "sphinx_external_toc" in extensions:
    external_toc_path = "_toc.yml"

# Sitemap (if sphinx_sitemap is available)
if "sphinx_sitemap" in extensions:
    html_baseurl = "https://haive.readthedocs.io/"
    sitemap_url_scheme = "{link}"

# =============================================================================
# LATEX CONFIGURATION
# =============================================================================

latex_elements = {
    "preamble": r"""
\usepackage[utf8]{inputenc}
\DeclareUnicodeCharacter{00A0}{\nobreakspace}
\usepackage{charter}
\usepackage[defaultsans]{lato}
\usepackage{inconsolata} 
""",
    "fncychap": r"\usepackage[Bjornstrup]{fncychap}",
    "printindex": r"\footnotesize\raggedright\printindex",
}

latex_documents = [
    (
        "index",
        "haive.tex",
        "Haive AI Agent Framework Documentation",
        "Haive Team",
        "manual",
    ),
]

# =============================================================================
# EPUB CONFIGURATION
# =============================================================================

epub_title = project
epub_author = author
epub_publisher = author
epub_copyright = copyright
epub_exclude_files = ["search.html"]

# =============================================================================
# CUSTOM EVENT HANDLERS
# =============================================================================

# Connect the event handler
def setup(app):
    """Setup function for custom Sphinx configuration."""
    app.connect("autoapi-skip-member", autoapi_skip_member)

# =============================================================================
# CONFIGURATION SUMMARY
# =============================================================================

print("✅ Memory-optimized Sphinx configuration loaded successfully!")
print(f"📦 Total extensions: {len(extensions)} (memory-optimized)")
print(f"🎨 Theme: {html_theme}")
print(f"📝 MyST enabled with {len(myst_enable_extensions)} extensions")
print("🔧 AutoAPI configured for all 7 Haive packages")
print(f"⚙️  Extension configs applied: {len(extension_configs)} settings")
print(f"🔄 Conditional configs: {len(conditional_configs)} optimizations")
print(
    f"💾 Memory management: Active with {build_recommendations['parallel_jobs']} parallel jobs"
)
print(f"📊 Recommended formats: {', '.join(build_recommendations['build_formats'])}")
print("📚 Full documentation build configuration active")
print("💾 Original 1101-line conf.py backed up as conf.backup.py")
print("🚀 Extensions loaded procedurally with rich debugging and memory management!")

# Show extension categories for debugging
extension_categories = {
    "UI/UX": [
        "sphinx_copybutton",
        "sphinx_design",
        "sphinx_tabs",
        "sphinx_togglebutton",
        "sphinx_collapse",
        "sphinx_carousel",
    ],
    "Diagrams": [
        "sphinxcontrib.mermaid",
        "sphinxcontrib.plantuml",
        "sphinxcontrib.blockdiag",
        "sphinx_uml",
        "sphinx_mindmap",
        "sphinx_diagrams",
    ],
    "API Docs": [
        "sphinxcontrib.openapi",
        "sphinxcontrib.redoc",
        "sphinxcontrib.httpdomain",
        "sphinx_argparse",
        "sphinx_click",
    ],
    "AutoDoc": [
        "sphinx_autoapi",
        "sphinx_autodoc2",
        "sphinx_autodocgen",
        "sphinx_automodapi",
        "sphinx_autopackagesummary",
    ],
    "Interactive": [
        "sphinx_charts",
        "sphinx_data_viewer",
        "sphinx_hoverxref",
        "sphinx_tippy",
        "sphinx_thebe",
        "sphinx_thebelab",
    ],
    "Themes": [
        "sphinx_book_theme",
        "sphinx_rtd_theme",
        "sphinx_modern_theme",
        "sphinx_library",
        "sphinx_typlog_theme",
    ],
    "Content": [
        "sphinx_gallery",
        "sphinx_examples",
        "sphinx_timeline",
        "sphinx_changelog",
        "sphinx_contributors",
    ],
    "Export": [
        "sphinx_pdf_generate",
        "sphinx_simplepdf",
        "sphinx_revealjs",
        "sphinxcontrib.applehelp",
        "sphinxcontrib.htmlhelp",
    ],
    "Versioning": [
        "sphinx_multiversion",
        "sphinx_polyversion",
        "sphinx_versions",
        "sphinx_version_warning",
    ],
    "Development": [
        "sphinx_autodoc_typehints",
        "sphinx_lint",
        "sphinx_debuginfo",
        "sphinx_reports",
        "sphinx_watch",
    ],
}

for category, exts in extension_categories.items():
    available = [ext for ext in exts if ext in extensions]
    if available:
        print(f"   {category}: {len(available)}/{len(exts)} available")
