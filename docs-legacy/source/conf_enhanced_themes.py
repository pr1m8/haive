"""Enhanced Sphinx configuration with all themes and professional styling."""

from __future__ import annotations

import os
from pathlib import Path
import sys

# Path setup
project_root = Path(__file__).parent.parent.parent
packages_dir = project_root / "packages"
sys.path.insert(0, str(packages_dir / "haive-core/src"))

# Logging
import logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger("sphinx_config_enhanced")

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
exclude_patterns = [
    "_build", 
    "Thumbs.db", 
    ".DS_Store",
    "agents/conversation/*.rst",
    "guides/agent_visualization.rst",
]

# =============================================================================
# EXTENSIONS - FULL SET WITH THEMES
# =============================================================================

extensions = [
    # CRITICAL: AutoAPI MUST BE FIRST
    "autoapi.extension",
    
    # Core Sphinx extensions
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
    "sphinx.ext.todo",
    "sphinx.ext.mathjax",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.inheritance_diagram",
    "sphinx.ext.graphviz",
    "sphinx.ext.githubpages",
    "sphinx.ext.duration",
    "sphinx.ext.extlinks",
    
    # Markdown support
    "myst_parser",
    
    # Enhanced documentation features - DESIGN & STYLING
    "sphinx_copybutton",
    "sphinx_design",  # Cards, grids, tabs, etc.
    "sphinx_togglebutton",  # Collapsible content
    "sphinx_tabs.tabs",  # Tabbed content
    "sphinx-prompt",  # Command prompt styling
    "sphinx_inline_tabs",  # Inline tabbed content
    "sphinx_panels",  # Panel layouts
    
    # Code and API enhancements
    "sphinx_autodoc_typehints",  # Better type hint rendering
    "sphinx_codeautolink",  # Link code to API docs
    
    # Diagrams
    "sphinxcontrib.mermaid",  # Mermaid diagrams
    
    # Search and navigation
    "sphinx_search.extension",  # Enhanced search
    
    # External services
    "sphinx_favicon",  # Favicon support
    "sphinx_last_updated_by_git",  # Git timestamps
]

# Verify AutoAPI is first
if extensions[0] != "autoapi.extension":
    raise RuntimeError(f"AutoAPI MUST be first extension, but got: {extensions[0]}")

# Remove extensions that aren't installed
def check_and_remove_missing_extensions(extensions_list):
    """Remove extensions that aren't installed."""
    available_extensions = []
    for ext in extensions_list:
        try:
            if ext == "autoapi.extension":
                import autoapi
            elif ext.startswith("sphinx.ext."):
                # Built-in extensions are always available
                pass
            else:
                # Try to import the extension
                if "." in ext:
                    module = ext.rsplit(".", 1)[0]
                else:
                    module = ext
                __import__(module)
            available_extensions.append(ext)
        except ImportError:
            logger.warning(f"⚠️ Extension '{ext}' not installed, skipping")
    return available_extensions

extensions = check_and_remove_missing_extensions(extensions)
logger.info(f"✅ Loaded {len(extensions)} extensions")

# =============================================================================
# AUTOAPI CONFIGURATION
# =============================================================================

ALL_PACKAGES = {
    "core": str(packages_dir / "haive-core/src"),
    "agents": str(packages_dir / "haive-agents/src"), 
    "tools": str(packages_dir / "haive-tools/src"),
    "games": str(packages_dir / "haive-games/src"),
    "dataflow": str(packages_dir / "haive-dataflow/src"),
    "mcp": str(packages_dir / "haive-mcp/src"),
    "prebuilt": str(packages_dir / "haive-prebuilt/src"),
}

autoapi_type = "python"
autoapi_dirs = list(ALL_PACKAGES.values())
autoapi_root = "api"
autoapi_add_toctree_entry = True
autoapi_generate_api_docs = True
autoapi_python_class_content = "both"
autoapi_member_order = "bysource"
autoapi_keep_files = True
autoapi_python_use_implicit_namespaces = True
autoapi_options = [
    "members",
    "undoc-members", 
    "show-inheritance",
    "special-members",
    "imported-members",
]

# =============================================================================
# HTML THEME CONFIGURATION - PYDATA WITH ENHANCED STYLING
# =============================================================================

# Try themes in order of preference
theme_preference = ["pydata_sphinx_theme", "sphinx_book_theme", "furo", "sphinx_rtd_theme", "alabaster"]
html_theme = None

for theme in theme_preference:
    try:
        if theme == "pydata_sphinx_theme":
            import pydata_sphinx_theme
        elif theme == "sphinx_book_theme":
            import sphinx_book_theme
        elif theme == "furo":
            import furo
        elif theme == "sphinx_rtd_theme":
            import sphinx_rtd_theme
        html_theme = theme
        logger.info(f"✅ Using theme: {theme}")
        break
    except ImportError:
        continue

if html_theme is None:
    html_theme = "alabaster"  # Fallback
    logger.warning("⚠️ Using fallback theme: alabaster")

# Theme-specific configuration
if html_theme == "pydata_sphinx_theme":
    html_theme_options = {
        "logo": {
            "text": "🤖 Haive AI Framework",
            "alt_text": "Haive Documentation",
        },
        "icon_links": [
            {
                "name": "GitHub",
                "url": "https://github.com/will-astley/haive",
                "icon": "fa-brands fa-github",
                "type": "fontawesome",
            },
        ],
        "use_edit_page_button": True,
        "show_toc_level": 2,
        "navigation_with_keys": True,
        "show_nav_level": 2,
        "navigation_depth": 4,
        "show_prev_next": True,
        "header_links_before_dropdown": 5,
        "primary_sidebar_end": ["indices.html", "sidebar-ethical-ads.html"],
        "secondary_sidebar_items": ["page-toc", "edit-this-page", "sourcelink"],
        "navbar_align": "left",
        "navbar_center": ["navbar-nav"],
        "navbar_end": ["theme-switcher", "navbar-icon-links", "version-switcher"],
        "footer_start": ["copyright"],
        "footer_center": ["sphinx-version"],
        "footer_end": ["theme-version"],
        "pygment_light_style": "default",
        "pygment_dark_style": "monokai",
    }
    
    html_context = {
        "github_user": "will-astley",
        "github_repo": "haive",
        "github_version": "main",
        "doc_path": "docs/source",
        "default_mode": "auto",  # auto, light, dark
    }
    
elif html_theme == "sphinx_book_theme":
    html_theme_options = {
        "repository_url": "https://github.com/will-astley/haive",
        "use_repository_button": True,
        "use_edit_page_button": True,
        "use_source_button": True,
        "use_issues_button": True,
        "use_download_button": True,
        "use_fullscreen_button": True,
        "path_to_docs": "docs/source",
        "repository_branch": "main",
        "home_page_in_toc": True,
        "show_navbar_depth": 2,
        "show_toc_level": 3,
        "navigation_with_keys": True,
        "logo": {
            "text": "🤖 Haive AI Framework",
        },
        "extra_navbar": "",
        "extra_footer": "",
        "toc_title": "On this page",
    }
    
elif html_theme == "furo":
    html_theme_options = {
        "light_css_variables": {
            "color-background-primary": "#ffffff",
            "color-background-secondary": "#f8fafc",
            "color-background-border": "#e2e8f0",
            "color-background-hover": "#f1f5f9",
            "color-background-item": "#e2e8f0",
            "color-brand-primary": "#2563eb",
            "color-brand-content": "#2563eb",
            "color-foreground-primary": "#1f2937",
            "color-foreground-secondary": "#6b7280",
            "color-foreground-muted": "#9ca3af",
            "color-foreground-border": "#d1d5db",
            "color-sidebar-background": "#f8fafc",
            "color-sidebar-background-border": "#e2e8f0",
            "color-api-background": "#f8fafc",
            "color-api-background-hover": "#f1f5f9",
            "color-api-overall": "#6b7280",
            "color-api-name": "#1f2937",
            "color-api-pre-name": "#6b7280",
            "color-inline-code-background": "#f1f5f9",
            "color-inline-code-foreground": "#374151",
            "color-admonition-background": "#f8fafc",
            "color-search-background": "#ffffff",
            "color-search-foreground": "#1f2937",
            "color-search-border": "#d1d5db",
            "color-link": "#2563eb",
            "color-link-underline": "#2563eb",
            "color-link-hover": "#1d4ed8",
            "font-stack": "Inter, -apple-system, BlinkMacSystemFont, Segoe UI, Helvetica, Arial, sans-serif",
            "font-stack-monospace": "Fira Code, Consolas, Monaco, Courier, monospace",
        },
        "dark_css_variables": {
            "color-background-primary": "#0f172a",
            "color-background-secondary": "#1e293b",
            "color-background-border": "#334155",
            "color-background-hover": "#475569",
            "color-background-item": "#334155",
            "color-brand-primary": "#60a5fa",
            "color-brand-content": "#60a5fa",
            "color-foreground-primary": "#f1f5f9",
            "color-foreground-secondary": "#cbd5e1",
            "color-foreground-muted": "#94a3b8",
            "color-foreground-border": "#64748b",
            "color-sidebar-background": "#1e293b",
            "color-sidebar-background-border": "#334155",
            "color-api-background": "#1e293b",
            "color-api-background-hover": "#475569",
            "color-api-overall": "#cbd5e1",
            "color-api-name": "#f1f5f9",
            "color-api-pre-name": "#cbd5e1",
            "color-inline-code-background": "#475569",
            "color-inline-code-foreground": "#e2e8f0",
            "color-admonition-background": "#1e293b",
            "color-search-background": "#0f172a",
            "color-search-foreground": "#f1f5f9",
            "color-search-border": "#334155",
            "color-link": "#60a5fa",
            "color-link-underline": "#60a5fa",
            "color-link-hover": "#93c5fd",
        },
        "sidebar_hide_name": False,
        "navigation_with_keys": True,
        "top_of_page_buttons": ["view", "edit"],
        "source_repository": "https://github.com/will-astley/haive",
        "source_branch": "main", 
        "source_directory": "docs/source/",
    }

elif html_theme == "sphinx_rtd_theme":
    html_theme_options = {
        "logo_only": False,
        "display_version": True,
        "prev_next_buttons_location": "bottom",
        "style_external_links": True,
        "collapse_navigation": False,
        "sticky_navigation": True,
        "navigation_depth": 4,
        "includehidden": True,
        "titles_only": False,
    }

# Common HTML settings
html_title = f"🤖 {project}"
html_short_title = "Haive"
html_static_path = ["_static"]
html_css_files = [
    "custom.css",  # We'll create this
]
html_js_files = []
html_show_sourcelink = True
html_show_sphinx = False
html_show_copyright = True

# Favicon
html_favicon = "_static/favicon.ico" if Path("docs/source/_static/favicon.ico").exists() else None

# Logo
html_logo = "_static/logo.png" if Path("docs/source/_static/logo.png").exists() else None

# =============================================================================
# CUSTOM CSS FOR BETTER STYLING
# =============================================================================

custom_css_content = """
/* Custom CSS for Haive Documentation */

/* Better fonts */
body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
    line-height: 1.6;
}

code, pre {
    font-family: 'Fira Code', 'Consolas', 'Monaco', 'Courier New', monospace;
}

/* Better code blocks */
.highlight {
    background: #f6f8fa !important;
    border: 1px solid #e1e4e8;
    border-radius: 6px;
    margin: 1em 0;
}

.highlight pre {
    margin: 0;
    padding: 1em;
}

/* API documentation styling */
.py.class, .py.function, .py.method {
    margin-bottom: 2em;
}

.py.class > dt, .py.function > dt, .py.method > dt {
    background: #f6f8fa;
    border-left: 3px solid #2563eb;
    padding: 0.5em 1em;
    font-weight: 600;
    border-radius: 0 4px 4px 0;
}

/* Better admonitions */
.admonition {
    border-radius: 6px;
    padding: 1em;
    margin: 1em 0;
    border-left: 4px solid;
}

.admonition.note {
    background: #e3f2fd;
    border-color: #2196f3;
}

.admonition.warning {
    background: #fff3cd;
    border-color: #ff9800;
}

.admonition.danger {
    background: #ffebee;
    border-color: #f44336;
}

/* Better navigation */
.toctree-wrapper {
    margin: 2em 0;
}

.toctree-wrapper .caption {
    font-weight: 700;
    font-size: 1.2em;
    margin-bottom: 0.5em;
}

/* Improve readability */
.content {
    max-width: 900px;
    margin: 0 auto;
    padding: 2em;
}

/* Better tables */
table.docutils {
    border-collapse: collapse;
    width: 100%;
    margin: 1em 0;
}

table.docutils td, table.docutils th {
    border: 1px solid #ddd;
    padding: 0.5em;
}

table.docutils th {
    background: #f6f8fa;
    font-weight: 600;
}

/* Better inline code */
code.literal {
    background: #f6f8fa;
    padding: 0.2em 0.4em;
    border-radius: 3px;
    font-size: 0.9em;
}

/* Module index improvements */
.modindex-jumpbox {
    background: #f6f8fa;
    padding: 1em;
    border-radius: 6px;
    margin-bottom: 2em;
}

/* Search improvements */
.search {
    margin-bottom: 2em;
}

#searchbox input[type="text"] {
    width: 100%;
    padding: 0.5em;
    border: 1px solid #ddd;
    border-radius: 4px;
}

/* Responsive improvements */
@media (max-width: 768px) {
    .content {
        padding: 1em;
    }
}
"""

# Create custom CSS file
def create_custom_css(app):
    """Create custom CSS file for better styling."""
    static_dir = Path(app.srcdir) / "_static"
    static_dir.mkdir(exist_ok=True)
    
    css_file = static_dir / "custom.css"
    with open(css_file, 'w') as f:
        f.write(custom_css_content)
    
    logger.info("✅ Created custom.css for enhanced styling")

# =============================================================================
# EXTENSION CONFIGURATIONS
# =============================================================================

# Myst Parser
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

# Napoleon
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = False
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = True
napoleon_use_admonition_for_notes = True
napoleon_use_admonition_for_references = False
napoleon_use_ivar = False
napoleon_use_param = True
napoleon_use_rtype = True
napoleon_type_aliases = {
    "ndarray": "numpy.ndarray",
    "DataFrame": "pandas.DataFrame",
}

# Autodoc
autodoc_default_options = {
    "members": True,
    "member-order": "bysource",
    "special-members": "__init__",
    "undoc-members": True,
    "exclude-members": "__weakref__",
    "show-inheritance": True,
    "inherited-members": False,
}

autodoc_typehints = "description"
autodoc_typehints_description_target = "documented"
autodoc_typehints_format = "short"
autodoc_mock_imports = []

# Copy button
if "sphinx_copybutton" in extensions:
    copybutton_prompt_text = r">>> |\.\.\. |\$ |In \[\d*\]: | {2,5}\.\.\.: | {5,8}: "
    copybutton_prompt_is_regexp = True
    copybutton_line_continuation_character = "\\"
    copybutton_here_doc_delimiter = "EOT"
    copybutton_selector = "div.highlight > pre"

# Mermaid
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
            lineColor: '#374151',
            secondaryColor: '#f3f4f6',
            tertiaryColor: '#e5e7eb'
        }
    });
    """

# Graphviz
graphviz_output_format = "svg"

# Todo
todo_include_todos = True
todo_emit_warnings = False

# Intersphinx
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "numpy": ("https://numpy.org/doc/stable/", None),
    "pandas": ("https://pandas.pydata.org/docs/", None),
    "pydantic": ("https://docs.pydantic.dev/latest/", None),
    "langchain": ("https://python.langchain.com/docs/", None),
    "langchain_core": ("https://api.python.langchain.com/en/latest/", None),
}

# =============================================================================
# NITPICK CONFIGURATION
# =============================================================================

nitpicky = True
nitpick_ignore = [
    # Basic Python types
    ("py:class", "str"),
    ("py:class", "int"),
    ("py:class", "bool"),
    ("py:class", "float"),
    ("py:class", "list"),
    ("py:class", "dict"),
    ("py:class", "tuple"),
    ("py:class", "set"),
    ("py:class", "bytes"),
    ("py:class", "None"),
    ("py:class", "type"),
    ("py:class", "object"),
    # Add more as needed...
]

# =============================================================================
# AUTOAPI SKIP MEMBER
# =============================================================================

def autoapi_skip_member(app, what, name, obj, skip, options):
    """Skip problematic members and duplicates."""
    try:
        # Skip Pydantic internals
        pydantic_internals = [
            "__fields__", "__config__", "__validators__", "__root_validators__",
            "model_fields", "model_config", "model_computed_fields",
        ]
        
        if what == "attribute" and any(name.endswith(internal) for internal in pydantic_internals):
            return True
        
        # Skip problematic patterns
        problematic_patterns = [
            'haive.core.schema.prebuilt.messages_state',
            'haive.agents.base.agent',
            'hyde.agent',
        ]
        
        if any(pattern in str(name) for pattern in problematic_patterns):
            return True
        
        return skip
        
    except Exception:
        return True

# =============================================================================
# SETUP FUNCTION
# =============================================================================

def setup(app):
    """Setup function with custom styling and enhancements."""
    
    # Create custom CSS
    app.connect('builder-inited', lambda app: create_custom_css(app))
    
    # Connect autoapi skip member
    app.connect("autoapi-skip-member", autoapi_skip_member)
    
    # Initialize autoapi_all_objects
    def init_autoapi_objects_builder_inited(app):
        """Initialize when builder is initialized."""
        try:
            if hasattr(app, 'env') and app.env and not hasattr(app.env, 'autoapi_all_objects'):
                app.env.autoapi_all_objects = {}
                logger.info("✅ Initialized autoapi_all_objects")
        except Exception as e:
            logger.error(f"❌ Failed to initialize autoapi_all_objects: {e}")
    
    app.connect('builder-inited', init_autoapi_objects_builder_inited)
    
    # Fix toc_num_entries
    def fix_autoapi_toc_entries(app, env):
        """Fix AutoAPI compatibility with Sphinx 8.2.3."""
        if 'index' not in env.toc_num_entries:
            env.toc_num_entries['index'] = 0
        
        for docname in env.all_docs:
            if docname not in env.toc_num_entries:
                env.toc_num_entries[docname] = 0
    
    app.connect('env-updated', fix_autoapi_toc_entries)
    
    logger.info("✅ All setup handlers connected")

# =============================================================================
# CONFIGURATION SUMMARY
# =============================================================================

logger.info("=" * 70)
logger.info("ENHANCED SPHINX CONFIGURATION")
logger.info("=" * 70)
logger.info(f"📦 Extensions: {len(extensions)} loaded")
logger.info(f"🎨 Theme: {html_theme}")
logger.info(f"🔧 AutoAPI: Processing {len(autoapi_dirs)} packages")
logger.info("=" * 70)