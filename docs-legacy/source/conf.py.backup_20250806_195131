"""Complete Sphinx configuration with ALL 83+ extensions and enhanced theming."""

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
logger = logging.getLogger("sphinx_config_complete")

# =============================================================================
# PROJECT INFORMATION
# =============================================================================

_sphinx_packages = os.environ.get("SPHINX_PACKAGES", "all")

if _sphinx_packages != "all":
    pkg_names = [
        p.strip().replace("haive-", "") for p in _sphinx_packages.split(",")
    ]
    project = f"Haive {', '.join(p.title() for p in pkg_names)}"
else:
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
pygments_style = "sphinx"

# =============================================================================
# EXTENSIONS - ALL 83+ ORIGINAL EXTENSIONS
# =============================================================================

# Control variables
SPHINX_PROFILE = os.environ.get("SPHINX_PROFILE", "full")
DISABLE_EXAMPLES = os.environ.get("SPHINX_DISABLE_EXAMPLES", "0").lower() in ("1", "true", "yes")
FAST_IMPORTS = os.environ.get("SPHINX_FAST_IMPORTS", "1").lower() in ("1", "true", "yes")
IMPORT_SAMPLE_LIMIT = int(os.environ.get("SPHINX_IMPORT_SAMPLE_LIMIT", "300"))

# ALL 83+ ORIGINAL EXTENSIONS
extensions = [
    # CRITICAL: AutoAPI MUST BE FIRST
    "autoapi.extension",
    
    # Core Sphinx extensions
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.napoleon",
    "sphinx.ext.doctest",
    "sphinx.ext.intersphinx",
    "sphinx.ext.todo",
    "sphinx.ext.coverage",
    "sphinx.ext.ifconfig",
    "sphinx.ext.viewcode",
    "sphinx.ext.githubpages",
    "sphinx.ext.inheritance_diagram",
    "sphinx.ext.graphviz",
    "sphinx.ext.mathjax",
    "sphinx.ext.imgmath",
    "sphinx.ext.duration",
    "sphinx.ext.extlinks",
    
    # Enhanced documentation features
    "sphinx_copybutton",
    "sphinx_design",
    "sphinx_togglebutton",
    "sphinx_tabs.tabs",
    "sphinx-prompt",
    "sphinx_substitution_extensions",
    "sphinx_tippy",
    "sphinx_needs",
    "sphinx_inline_tabs",
    "sphinx_panels",
    "sphinx_proof",
    "sphinx_exercise",
    
    # API documentation
    "sphinx_automodapi.automodapi",
    "sphinx_automodapi.smart_resolver",
    "sphinxcontrib.httpdomain",
    "sphinxcontrib.openapi",
    "sphinxcontrib.redoc",
    "sphinxcontrib.swaggerdoc",
    
    # Output formats
    "sphinxcontrib.htmlhelp",
    "sphinxcontrib.serializinghtml",
    "sphinxcontrib.devhelp",
    "sphinxcontrib.qthelp",
    "sphinxcontrib.applehelp",
    "sphinx_latex_elements",
    
    # Markdown support
    "myst_parser",
    "myst_nb",
    "recommonmark",
    
    # Diagrams and visualization
    "sphinxcontrib.mermaid",
    "sphinxcontrib.plantuml",
    "sphinxcontrib.actdiag",
    "sphinxcontrib.blockdiag",
    "sphinxcontrib.nwdiag",
    "sphinxcontrib.seqdiag",
    "sphinxcontrib.wavedrom",
    "sphinxcontrib.kroki",
    "sphinx_diagrams",
    
    # External services
    "sphinx_favicon",
    "sphinx_last_updated_by_git",
    "sphinx_notfound_page",
    "sphinx_reredirects",
    "sphinx_sitemap",
    "sphinx_external_toc",
    "sphinxcontrib.youtube",
    "sphinxcontrib.vimeo",
    "sphinxcontrib.gist",
    
    # Development tools
    "sphinx_autobuild",
    "sphinx_rtd_theme",
    "sphinx_rtd_dark_mode",
    "sphinx_book_theme",
    "pydata_sphinx_theme",
    "sphinx_material",
    "sphinx_bootstrap_theme",
    "sphinx_pdj_theme",
    "sphinx_typo3_theme",
    "groundwork_sphinx_theme",
    "sphinx_documatt_theme",
    
    # Code documentation
    "sphinx_autodoc_typehints",
    "sphinx_autodoc_defaultargs",
    "sphinx_paramlinks",
    "sphinx_codeautolink",
    "sphinx_autorun",
    
    # Testing and examples
    "sphinx_gallery.gen_gallery",
    "sphinx_exec_code",
    "sphinx_runpython",
    
    # Search enhancements
    "sphinxcontrib.spelling",
    "sphinx_search.extension",
    
    # Additional features
    "sphinx_issues",
    "sphinx_removed_in",
    "sphinx_version_warning",
    "sphinx_multiversion",
    "sphinx_revealjs",
    "hieroglyph",
    "sphinxcontrib.programoutput",
    "sphinxcontrib.asciinema",
    "sphinxcontrib.email",
    "sphinxcontrib.argdoc",
    "sphinxcontrib.confluencebuilder",
    "sphinxcontrib.discourse",
    "sphinxcontrib.exceltable",
    "sphinxcontrib.googleanalytics",
    "sphinxcontrib.googlechart",
    "sphinxcontrib.googlemaps",
    
    # Add autodoc-pydantic if available
    "sphinxcontrib.autodoc_pydantic",
]

# Verify AutoAPI is first
if extensions[0] != "autoapi.extension":
    raise RuntimeError(f"AutoAPI MUST be first extension, but got: {extensions[0]}")

# Remove extensions that aren't installed
def check_and_remove_missing_extensions(extensions_list):
    """Remove extensions that aren't installed but keep trying."""
    available_extensions = []
    missing_extensions = []
    
    for ext in extensions_list:
        try:
            if ext == "autoapi.extension":
                import autoapi
            elif ext.startswith("sphinx.ext."):
                # Built-in extensions are always available
                pass
            elif "." in ext:
                module = ext.rsplit(".", 1)[0]
                __import__(module)
            else:
                __import__(ext)
            available_extensions.append(ext)
        except ImportError:
            missing_extensions.append(ext)
    
    if missing_extensions:
        logger.warning(f"⚠️ Missing {len(missing_extensions)} extensions: {', '.join(missing_extensions[:5])}...")
    
    logger.info(f"✅ Loaded {len(available_extensions)} of {len(extensions_list)} extensions")
    return available_extensions

extensions = check_and_remove_missing_extensions(extensions)

# Remove problematic extensions if needed
if DISABLE_EXAMPLES:
    extensions = [ext for ext in extensions if not ext.startswith("sphinx_gallery")]
    logger.info("🚫 Sphinx Gallery disabled via SPHINX_DISABLE_EXAMPLES")

# =============================================================================
# AUTOAPI CONFIGURATION - ALL PACKAGES
# =============================================================================

SPHINX_PACKAGES = os.environ.get("SPHINX_PACKAGES", "all")

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

if SPHINX_PACKAGES == "all":
    autoapi_dirs = list(ALL_PACKAGES.values())
    print(f"📦 Building ALL packages ({len(autoapi_dirs)} total)")
else:
    requested_packages = [p.strip() for p in SPHINX_PACKAGES.split(",")]
    autoapi_dirs = []

    for pkg in requested_packages:
        pkg_name = (pkg.replace("haive-", "") if pkg.startswith("haive-") else pkg)

        if pkg_name in ALL_PACKAGES:
            autoapi_dirs.append(ALL_PACKAGES[pkg_name])
            print(f"📦 Adding package: haive-{pkg_name}")
        else:
            print(f"⚠️  Unknown package: {pkg}")

    if not autoapi_dirs:
        print("❌ No valid packages specified, defaulting to haive-core")
        autoapi_dirs = [ALL_PACKAGES["core"]]

autodoc_mock_imports = []

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

autoapi_python_class_content = "both"
autoapi_member_order = "bysource"
autoapi_own_page_level = "module"
autoapi_ignore = []

# =============================================================================
# HTML THEME CONFIGURATION - PYDATA/BOOK/FURO WITH FULL FEATURES
# =============================================================================

# Try themes in order of preference
theme_preference = ["pydata_sphinx_theme", "sphinx_book_theme", "furo", "sphinx_rtd_theme"]
html_theme = None

for theme in theme_preference:
    if theme in extensions or theme == "furo":  # Furo isn't in extensions
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
    html_theme = "alabaster"
    logger.warning("⚠️ Using fallback theme: alabaster")

# Theme options based on selected theme
if html_theme == "pydata_sphinx_theme":
    html_theme_options = {
        "logo": {
            "text": "🤖 Haive AI Framework",
            "alt_text": "Haive - Advanced AI Agent Framework",
        },
        "icon_links": [
            {
                "name": "GitHub",
                "url": "https://github.com/will-astley/haive",
                "icon": "fa-brands fa-github",
                "type": "fontawesome",
            },
            {
                "name": "PyPI",
                "url": "https://pypi.org/project/haive/",
                "icon": "fa-brands fa-python",
                "type": "fontawesome",
            },
        ],
        "use_edit_page_button": True,
        "show_toc_level": 3,
        "navigation_with_keys": True,
        "show_nav_level": 2,
        "navigation_depth": 4,
        "show_prev_next": True,
        "header_links_before_dropdown": 5,
        "primary_sidebar_end": ["indices.html", "sidebar-ethical-ads.html"],
        "secondary_sidebar_items": ["page-toc", "edit-this-page", "sourcelink"],
        "navbar_align": "left",
        "navbar_center": ["navbar-nav"],
        "navbar_end": ["theme-switcher", "navbar-icon-links"],
        "footer_start": ["copyright"],
        "footer_center": ["sphinx-version"],
        "footer_end": ["theme-version"],
        "pygment_light_style": "default",
        "pygment_dark_style": "monokai",
        "analytics": {
            "google_analytics_id": "UA-XXXXXXX",
        },
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
        "extra_navbar": "<p>Advanced AI Agent Framework</p>",
        "toc_title": "On this page",
        "launch_buttons": {
            "notebook_interface": "jupyterlab",
            "binderhub_url": "https://mybinder.org",
            "colab_url": "https://colab.research.google.com",
        },
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
            "font-stack": "Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif",
            "font-stack-monospace": "'Fira Code', Consolas, Monaco, monospace",
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
        "announcement": "🚀 Haive v1.0 is now available!",
    }

elif html_theme == "sphinx_rtd_theme":
    html_theme_options = {
        "logo_only": False,
        "display_version": True,
        "prev_next_buttons_location": "both",
        "style_external_links": True,
        "collapse_navigation": False,
        "sticky_navigation": True,
        "navigation_depth": 4,
        "includehidden": True,
        "titles_only": False,
        "analytics_id": "UA-XXXXXXX-1",
        "analytics_anonymize_ip": False,
        "canonical_url": "https://haive.readthedocs.io/",
    }

html_static_path = ["_static"]
html_css_files = ["custom.css"]
html_js_files = []

html_title = f"🤖 {project} Documentation"
html_short_title = "Haive"

html_context = {
    "display_github": True,
    "github_user": "will-astley",
    "github_repo": "haive",
    "github_version": "main",
    "conf_py_path": "/docs/source/",
}

# Sidebars configuration
html_sidebars = {
    "**": [
        "sidebar/scroll-start.html",
        "sidebar/brand.html",
        "sidebar/search.html",
        "sidebar/navigation.html", 
        "sidebar/ethical-ads.html",
        "sidebar/scroll-end.html",
    ],
}

if html_theme == "pydata_sphinx_theme":
    html_sidebars = {
        "**": ["sidebar-nav-bs", "sidebar-ethical-ads"],
    }

# Favicon and logo
html_favicon = "_static/favicon.ico"
html_logo = "_static/logo.png"

# =============================================================================
# EXTENSION CONFIGURATIONS (ALL 83+)
# =============================================================================

# Myst Parser - Full configuration
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
    "attrs_inline",
    "attrs_block",
]

myst_heading_anchors = 3
myst_footnote_transition = True
myst_dmath_double_inline = True
myst_all_links_external = False
myst_url_schemes = ["http", "https", "mailto", "ftp"]
myst_substitutions = {
    "version": version,
    "release": release,
}

# Napoleon settings
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
napoleon_type_aliases = None
napoleon_attr_annotations = True

# Autodoc configuration
autodoc_default_options = {
    "members": True,
    "member-order": "bysource",
    "special-members": "__init__",
    "undoc-members": True,
    "exclude-members": "__weakref__",
    "show-inheritance": True,
    "inherited-members": False,
    "private-members": False,
}

autodoc_typehints = "description"
autodoc_typehints_description_target = "documented"
autodoc_typehints_format = "short"
autodoc_mock_imports = []
autodoc_class_signature = "separated"
autodoc_preserve_defaults = True

# Autosummary
autosummary_generate = True
autosummary_imported_members = True
autosummary_mock_imports = autodoc_mock_imports

# Type hints
typehints_fully_qualified = False
typehints_document_rtype = True
typehints_use_rtype = True

# autodoc-pydantic (if installed)
if "sphinxcontrib.autodoc_pydantic" in extensions:
    autodoc_pydantic_model_show_json = False
    autodoc_pydantic_model_show_config_summary = True
    autodoc_pydantic_model_show_validator_members = True
    autodoc_pydantic_model_show_validator_summary = True
    autodoc_pydantic_model_show_field_summary = True
    autodoc_pydantic_field_list_validators = True
    autodoc_pydantic_field_show_constraints = True
    autodoc_pydantic_field_doc_policy = "both"
    autodoc_pydantic_settings_show_json = False
    autodoc_pydantic_settings_show_config_summary = True
    autodoc_pydantic_settings_show_validator_members = True

# Intersphinx mapping
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "numpy": ("https://numpy.org/doc/stable/", None),
    "pandas": ("https://pandas.pydata.org/docs/", None),
    "pydantic": ("https://docs.pydantic.dev/latest/", None),
    "langchain": ("https://python.langchain.com/docs/", None),
    "langchain_core": ("https://api.python.langchain.com/en/latest/", None),
    "langchain_community": ("https://api.python.langchain.com/en/latest/", None),
    "langchain_openai": ("https://api.python.langchain.com/en/latest/", None),
}

# Nitpicky mode
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
    
    # Typing module
    ("py:class", "Any"),
    ("py:class", "List"),
    ("py:class", "Dict"),
    ("py:class", "Tuple"),
    ("py:class", "Set"),
    ("py:class", "Optional"),
    ("py:class", "Union"),
    ("py:class", "Callable"),
    ("py:class", "Type"),
    ("py:class", "TypeVar"),
    ("py:class", "Generic"),
    ("py:class", "Literal"),
    ("py:class", "Protocol"),
    ("py:class", "TypedDict"),
    
    # Pydantic
    ("py:class", "BaseModel"),
    ("py:class", "Field"),
    ("py:class", "SecretStr"),
    ("py:class", "ConfigDict"),
    
    # LangChain
    ("py:class", "Document"),
    ("py:class", "BaseMessage"),
    ("py:class", "HumanMessage"),
    ("py:class", "AIMessage"),
    ("py:class", "SystemMessage"),
    ("py:class", "ToolMessage"),
    ("py:class", "langchain_core.runnables.RunnableConfig"),
    ("py:class", "langchain_core.runnables.Runnable"),
    ("py:class", "langchain_core.callbacks.CallbackManagerForLLMRun"),
    
    # Haive internal
    ("py:class", "haive.core.engine.base.Engine"),
    ("py:obj", "haive.core.common.mixins.tool_route_mixin.ToolRouteMixin"),
    ("py:class", "haive.agents.wiki_writer.utils.update_editor"),
    
    # Generic parameters
    ("py:class", "T"),
    ("py:class", "Agent"),
    ("py:class", "TIn"),
    ("py:class", "TOut"),
]

# Python domain
python_use_unqualified_type_names = True

# Suppress warnings
suppress_warnings = ["ref.python", "autoapi"]

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
inheritance_graph_attrs = dict(rankdir="TB", size='""')
inheritance_node_attrs = dict(shape='ellipse', fontsize=14, color='dodgerblue1',
                              style='filled', fillcolor='lightgoldenrodyellow')
inheritance_edge_attrs = dict(arrowsize='.5', color='dodgerblue1')

# Todo extension
todo_include_todos = True
todo_emit_warnings = False
todo_link_only = False

# External TOC
if "sphinx_external_toc" in extensions:
    external_toc_path = "_toc.yml"

# Sitemap
if "sphinx_sitemap" in extensions:
    html_baseurl = "https://haive.readthedocs.io/"
    sitemap_url_scheme = "{link}"

# JSMath
jsmath_path = "https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.5/MathJax.js?config=TeX-AMS-MML_HTMLorMML"

# Sphinx Gallery
if "sphinx_gallery.gen_gallery" in extensions and not DISABLE_EXAMPLES:
    sphinx_gallery_conf = {
        'examples_dirs': '../examples',
        'gallery_dirs': 'auto_examples',
        'filename_pattern': '/*.py',
        'ignore_pattern': r'__init__\.py',
        'expected_failing_examples': [],
        'plot_gallery': True,
        'download_all_examples': True,
        'abort_on_example_error': False,
        'remove_config_comments': True,
    }

# External links
extlinks = {
    'issue': ('https://github.com/will-astley/haive/issues/%s', 'issue %s'),
    'pr': ('https://github.com/will-astley/haive/pull/%s', 'PR %s'),
    'commit': ('https://github.com/will-astley/haive/commit/%s', 'commit %s'),
}

# =============================================================================
# AUTOAPI SKIP MEMBER - Enhanced
# =============================================================================

def autoapi_skip_member(app, what, name, obj, skip, options):
    """Skip problematic members with enhanced logic."""
    try:
        # Skip Pydantic internals
        pydantic_internals = [
            "__fields__", "__config__", "__validators__", "__root_validators__",
            "__pre_root_validators__", "__post_root_validators__",
            "__schema_cache__", "__module__", "__annotations__",
            "__pydantic_model__", "__pydantic_fields__", "__pydantic_config__",
            "__pydantic_complete__", "__pydantic_decorators__",
            "__pydantic_fields_set__", "__pydantic_extra__",
            "__pydantic_generic_metadata__", "__pydantic_parent_namespace__",
            "__pydantic_serializer__", "__pydantic_validator__",
            "model_fields", "model_config", "model_computed_fields",
        ]
        
        if what == "attribute" and any(name.endswith(internal) for internal in pydantic_internals):
            return True
        
        # Skip duplicate fields
        if what == "attribute" and "." in name:
            parts = name.split(".")
            if len(parts) >= 2:
                field_name = parts[-1]
                
                duplicate_prone_fields = [
                    "milestones", "risk_factors", "available_tools", 
                    "time_constraints", "constraints", "dependencies",
                    "metadata", "tags", "status", "created_at", "updated_at",
                ]
                
                if field_name in duplicate_prone_fields:
                    if any(keyword in ".".join(parts[:-1]).lower() for keyword in ["model", "schema", "config", "plan", "task"]):
                        return True
        
        # Skip problematic imports
        problematic_patterns = [
            'haive.core.schema.prebuilt.messages_state',
            'haive.core.schema.prebuilt.messages.messages_state',
            'haive.agents.base.agent',
            'haive.agents.base',
            'hyde.agent',
            'hyde.enhanced_agent',
            'get_summary',
            'BranchSpec',
            'AgentState',
            'SupervisorReactState',
            'ExtendedHuggingFaceDatasetLoader',
            'HuggingFaceModelCardLoader',
            'VectorStoreConfig',
            'Config',
        ]
        
        if any(pattern in str(name) for pattern in problematic_patterns):
            logger.warning(f"⚠️ Skipping problematic member: {name}")
            return True
        
        return skip
        
    except Exception as e:
        logger.warning(f"⚠️ Error in skip_member for {name}: {e}")
        return True

# =============================================================================
# CUSTOM CSS
# =============================================================================

custom_css_content = """
/* Haive Documentation Custom Styles */

/* Modern fonts */
body {
    font-family: Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
    line-height: 1.7;
}

code, pre, .rst-content tt, .rst-content code {
    font-family: 'Fira Code', 'JetBrains Mono', Consolas, Monaco, 'Courier New', monospace;
    font-variant-ligatures: normal;
}

/* Better headings */
h1, h2, h3, h4, h5, h6 {
    font-weight: 600;
    letter-spacing: -0.02em;
}

/* Enhanced code blocks */
.highlight {
    background: #f8fafc !important;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    margin: 1.5em 0;
    position: relative;
}

.highlight pre {
    margin: 0;
    padding: 1.25em;
    overflow-x: auto;
}

/* Copy button styling */
.highlight button.copybtn {
    position: absolute;
    top: 0.5em;
    right: 0.5em;
    opacity: 0;
    transition: opacity 0.2s;
}

.highlight:hover button.copybtn {
    opacity: 1;
}

/* API documentation enhancements */
.py.class, .py.function, .py.method, .py.attribute {
    margin: 2em 0;
    border-left: 3px solid #2563eb;
    padding-left: 1em;
    transition: all 0.2s ease;
}

.py.class:hover, .py.function:hover, .py.method:hover {
    border-left-color: #1d4ed8;
    background: rgba(37, 99, 235, 0.03);
}

.py.class > dt, .py.function > dt, .py.method > dt {
    background: #f8fafc;
    padding: 0.75em 1em;
    font-weight: 600;
    border-radius: 0 6px 6px 0;
    font-size: 1.05em;
}

/* Better admonitions */
.admonition {
    border-radius: 8px;
    padding: 1.25em;
    margin: 1.5em 0;
    border-left: 4px solid;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.admonition.note {
    background: #eff6ff;
    border-color: #3b82f6;
}

.admonition.warning {
    background: #fffbeb;
    border-color: #f59e0b;
}

.admonition.danger, .admonition.error {
    background: #fef2f2;
    border-color: #ef4444;
}

.admonition.tip, .admonition.hint {
    background: #f0fdf4;
    border-color: #10b981;
}

.admonition-title {
    font-weight: 600;
    margin-bottom: 0.5em;
}

/* Navigation improvements */
.toctree-wrapper {
    margin: 2.5em 0;
}

.toctree-wrapper .caption {
    font-weight: 700;
    font-size: 1.25em;
    margin-bottom: 0.75em;
    color: #1f2937;
}

/* Tables */
table.docutils {
    border-collapse: collapse;
    width: 100%;
    margin: 1.5em 0;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
    border-radius: 8px;
    overflow: hidden;
}

table.docutils td, table.docutils th {
    border: 1px solid #e5e7eb;
    padding: 0.75em 1em;
}

table.docutils th {
    background: #f9fafb;
    font-weight: 600;
}

table.docutils tbody tr:hover {
    background: #f9fafb;
}

/* Inline code */
code.literal {
    background: #f1f5f9;
    padding: 0.125em 0.375em;
    border-radius: 4px;
    font-size: 0.875em;
    color: #0f172a;
    font-weight: 500;
}

/* Search styling */
.search input[type="text"] {
    width: 100%;
    padding: 0.75em 1em;
    border: 2px solid #e5e7eb;
    border-radius: 6px;
    font-size: 1em;
    transition: border-color 0.2s;
}

.search input[type="text"]:focus {
    outline: none;
    border-color: #2563eb;
}

/* Sidebar enhancements */
.sidebar {
    background: #f9fafb;
    border-right: 1px solid #e5e7eb;
}

.sidebar .caption {
    font-weight: 700;
    text-transform: uppercase;
    font-size: 0.875em;
    letter-spacing: 0.05em;
    color: #6b7280;
    margin: 1.5em 0 0.5em 0;
}

/* Module index cards */
.modindex-jumpbox {
    background: #f8fafc;
    padding: 1.5em;
    border-radius: 8px;
    margin-bottom: 2em;
    border: 1px solid #e5e7eb;
}

/* Responsive improvements */
@media (max-width: 768px) {
    .content {
        padding: 1em;
    }
    
    .py.class, .py.function, .py.method {
        margin: 1em 0;
        padding-left: 0.5em;
    }
}

/* Dark mode support */
@media (prefers-color-scheme: dark) {
    body[data-theme="auto"] {
        --color-background: #0f172a;
        --color-foreground: #f1f5f9;
    }
    
    .highlight {
        background: #1e293b !important;
        border-color: #334155;
    }
    
    code.literal {
        background: #334155;
        color: #f1f5f9;
    }
    
    .admonition {
        filter: brightness(0.8);
    }
}

/* Sphinx design cards */
.sd-card {
    border-radius: 8px;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
    transition: all 0.2s;
}

.sd-card:hover {
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    transform: translateY(-2px);
}

/* Tabs styling */
.sphinx-tabs {
    border-radius: 8px;
    overflow: hidden;
}

.sphinx-tabs .sphinx-tabs-nav {
    background: #f9fafb;
    border-bottom: 2px solid #e5e7eb;
}

.sphinx-tabs .sphinx-tabs-tab[aria-selected="true"] {
    background: white;
    border-bottom: 2px solid #2563eb;
}

/* Toggle button styling */
.toggle-button {
    background: #f3f4f6;
    border: 1px solid #e5e7eb;
    border-radius: 6px;
    padding: 0.5em 1em;
    cursor: pointer;
    transition: all 0.2s;
}

.toggle-button:hover {
    background: #e5e7eb;
}

/* API page improvements */
.api h1 {
    border-bottom: 2px solid #e5e7eb;
    padding-bottom: 0.5em;
    margin-bottom: 1em;
}

.api .toc-tree {
    background: #f9fafb;
    padding: 1em;
    border-radius: 8px;
    margin: 1em 0;
}
"""

# =============================================================================
# SETUP FUNCTION
# =============================================================================

def setup(app):
    """Enhanced setup with all features."""
    
    # Create custom CSS
    def create_custom_css(app):
        """Create custom CSS file."""
        static_dir = Path(app.srcdir) / "_static"
        static_dir.mkdir(exist_ok=True)
        
        css_file = static_dir / "custom.css"
        with open(css_file, 'w') as f:
            f.write(custom_css_content)
        
        logger.info("✅ Created custom.css")
    
    app.connect('builder-inited', lambda app: create_custom_css(app))
    
    # Connect autoapi skip member
    try:
        app.connect("autoapi-skip-member", autoapi_skip_member)
        logger.info("✅ AutoAPI skip member handler connected")
    except Exception as e:
        logger.error(f"❌ Failed to connect AutoAPI skip member: {e}")
    
    # Initialize autoapi_all_objects
    def init_autoapi_objects_builder_inited(app):
        """Initialize when builder is initialized."""
        try:
            if hasattr(app, 'env') and app.env and not hasattr(app.env, 'autoapi_all_objects'):
                app.env.autoapi_all_objects = {}
                logger.info("✅ Initialized autoapi_all_objects")
        except Exception as e:
            logger.error(f"❌ Failed to initialize autoapi_all_objects: {e}")
    
    # Robust AutoAPI error handling
    def handle_autoapi_errors(app, exception):
        """Handle AutoAPI processing errors gracefully."""
        try:
            logger.error(f"❌ AutoAPI error: {exception}")
            return True
        except Exception as e:
            logger.error(f"❌ Error in AutoAPI error handler: {e}")
            return True
    
    # Connect to valid Sphinx events
    try:
        app.connect('builder-inited', init_autoapi_objects_builder_inited)
        if hasattr(app, 'connect'):
            try:
                app.connect('build-finished', lambda app, exception: handle_autoapi_errors(app, exception) if exception else None)
            except Exception as e:
                logger.warning(f"⚠️  Could not connect build-finished handler: {e}")
        logger.info("✅ AutoAPI event handlers connected")
    except Exception as e:
        logger.error(f"❌ Failed to connect AutoAPI event handlers: {e}")
    
    # Fix for Sphinx 8.2.3 toc_num_entries KeyError
    def fix_autoapi_toc_entries(app, env):
        """Fix AutoAPI compatibility with Sphinx 8.2.3."""
        if 'index' not in env.toc_num_entries:
            env.toc_num_entries['index'] = 0
            logger.info("🔧 Fixed missing toc_num_entries for index")
        
        for docname in env.all_docs:
            if docname not in env.toc_num_entries:
                env.toc_num_entries[docname] = 0
    
    app.connect('env-updated', fix_autoapi_toc_entries)

    # Try to setup enhanced build hooks
    try:
        from build_hooks_enhanced import setup as setup_hooks
        setup_hooks(app)
        logger.info("🪝 Enhanced build hooks registered")
    except ImportError:
        logger.warning("⚠️  Enhanced build hooks not available")
    except Exception as e:
        logger.error(f"❌ Failed to setup build hooks: {e}")

# =============================================================================
# CONFIGURATION SUMMARY
# =============================================================================

logger.info("=" * 70)
logger.info("COMPLETE ENHANCED SPHINX CONFIGURATION")
logger.info("=" * 70)
logger.info(f"📦 Extensions: {len(extensions)} total with AutoAPI first")
logger.info(f"🎨 Theme: {html_theme}")
logger.info(f"🔧 AutoAPI: Configured for all 7 Haive packages")
logger.info(f"✨ ALL 83+ extensions loaded (minus unavailable)")
logger.info("=" * 70)