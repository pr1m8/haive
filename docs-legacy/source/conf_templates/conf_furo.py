"""Clean Furo-based Sphinx configuration for Haive documentation.

This is a minimal, clean configuration that avoids autosummary issues
and focuses on getting documentation built quickly with the Furo theme.
"""

from __future__ import annotations

import os
from pathlib import Path

# Path setup
project_root = Path(__file__).parent.parent.parent
packages_dir = project_root / "packages"

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
    "packages/*",  # Exclude package docs with autosummary
    "index.rst",   # Exclude main index (use index_furo.rst instead)
]

# Use simplified index
master_doc = "index_furo"

# =============================================================================
# EXTENSIONS - MINIMAL SET FOR CLEAN BUILD
# =============================================================================

extensions = [
    # CRITICAL: AutoAPI MUST BE FIRST
    "autoapi.extension",
    
    # Core Sphinx extensions - MINIMAL SET
    "sphinx.ext.napoleon", 
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
    
    # Enhanced documentation
    "sphinx_copybutton",
    "myst_parser",
    # NOTE: sphinx.ext.autosummary AND sphinx.ext.autodoc are EXCLUDED 
    # to prevent autosummary import errors
]

# =============================================================================
# AUTOAPI CONFIGURATION - CLEAN AND SIMPLE
# =============================================================================

SPHINX_PACKAGES = os.environ.get("SPHINX_PACKAGES", "core")

# Point to src directories so AutoAPI sees haive.core (not just core)
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

# Add the Python paths to sys.path for proper imports
import sys

# Add src directories to Python path
for autoapi_dir in autoapi_dirs:
    if autoapi_dir not in sys.path:
        sys.path.insert(0, autoapi_dir)
        print(f"🐍 Added to Python path: {autoapi_dir}")

# AutoAPI settings - CLEAN
autoapi_root = "api"
autoapi_add_toctree_entry = True
autoapi_generate_api_docs = True
autoapi_python_class_content = "both"
autoapi_member_order = "bysource"
autoapi_keep_files = True

# Use simple templates without autosummary
autoapi_template_dir = "_templates/autoapi_simple"

# CRITICAL: Disable autosummary in autoapi options to avoid import errors
autoapi_options = [
    "members",
    "undoc-members", 
    "show-inheritance",
    "special-members",
    "imported-members",
    # "show-module-summary",  # DISABLED - This causes autosummary import errors
]

# Suppress import resolution warnings (these are just warnings, not errors)
suppress_warnings = [
    "autoapi.python_import_resolution",
]

autoapi_ignore = [
    "*/test_*.py",
    "*/tests/*",
    "*_test.py",
    "*/conftest.py",
    "*/examples/*",
    "*/example_*.py",
    "*_example.py",
    "*_demo.py",
    "*/__pycache__/*",
    "*.pyc",
]

# =============================================================================
# THEME CONFIGURATION - FURO
# =============================================================================

html_theme = "furo"

html_theme_options = {
    "light_css_variables": {
        "color-brand-primary": "#2563eb",
        "color-brand-content": "#2563eb",
        "color-admonition-background": "#f8fafc",
    },
    "dark_css_variables": {
        "color-brand-primary": "#60a5fa",
        "color-brand-content": "#60a5fa",
    },
    "sidebar_hide_name": False,
    "navigation_with_keys": True,
    "top_of_page_buttons": ["view", "edit"],
    "source_repository": "https://github.com/will-astley/haive",
    "source_branch": "main",
    "source_directory": "docs/source/",
}

html_static_path = ["_static"]
html_title = f"🤖 {project} Documentation"

# =============================================================================
# EXTENSION CONFIGURATIONS - MINIMAL
# =============================================================================

# Napoleon settings
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = True
napoleon_use_param = True
napoleon_use_rtype = True

# Autodoc
autodoc_default_options = {
    "members": True,
    "member-order": "bysource",
    "special-members": "__init__",
    "undoc-members": True,
    "exclude-members": "__weakref__",
    "show-inheritance": True,
}

# Intersphinx
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "pydantic": ("https://docs.pydantic.dev/latest/", None),
}

# Copy button
copybutton_prompt_text = r">>> |\.\.\. |\$ "
copybutton_prompt_is_regexp = True

# Myst Parser
myst_enable_extensions = [
    "colon_fence",
    "deflist",
    "substitution",
    "tasklist",
]

# =============================================================================
# SKIP MEMBER FUNCTION - SIMPLE
# =============================================================================

def autoapi_skip_member(app, what, name, obj, skip, options):
    """Simple skip logic without complex filtering."""
    # Skip Pydantic internals
    pydantic_internals = [
        "__fields__", "__config__", "__validators__",
        "__pydantic_model__", "__pydantic_fields__",
        "model_fields", "model_config",
    ]
    
    if what == "attribute" and any(name.endswith(internal) for internal in pydantic_internals):
        return True
    
    return skip

# =============================================================================
# SETUP FUNCTION - MINIMAL
# =============================================================================

def setup(app):
    """Minimal setup function."""
    # Connect AutoAPI skip member
    app.connect("autoapi-skip-member", autoapi_skip_member)
    
    # Create simple custom CSS
    def create_simple_css(app):
        """Create minimal custom CSS."""
        static_dir = Path(app.srcdir) / "_static"
        static_dir.mkdir(exist_ok=True)
        
        css_content = """
/* Haive Furo Theme Customizations */

/* Better code highlighting */
.highlight {
    border-radius: 6px;
    margin: 1em 0;
}

/* API documentation improvements */
.py.class, .py.function, .py.method {
    margin: 1.5em 0;
    border-left: 3px solid var(--color-brand-primary);
    padding-left: 1em;
}

.py.class > dt, .py.function > dt, .py.method > dt {
    background: var(--color-background-secondary);
    padding: 0.75em;
    border-radius: 4px;
    font-weight: 600;
}

/* Better spacing */
.content {
    line-height: 1.6;
}
"""
        
        css_file = static_dir / "custom.css"
        with open(css_file, 'w') as f:
            f.write(css_content)
    
    app.connect('builder-inited', create_simple_css)
    html_css_files = ["custom.css"]

print("✅ Clean Furo configuration loaded")
print(f"📦 AutoAPI dirs: {len(autoapi_dirs)} packages")
print(f"🎨 Theme: {html_theme}")
print(f"🔧 Extensions: {len(extensions)} minimal extensions")