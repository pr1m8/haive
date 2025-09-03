"""AutoAPI Namespace Fix Configuration for Haive Documentation.

This configuration addresses the 'core.engine' vs 'haive.core.engine' namespace issue
by properly configuring AutoAPI to discover modules with correct namespaces.

Key fixes implemented:
1. Correct autoapi_dirs pointing to namespace package root
2. Enable autoapi_python_use_implicit_namespaces
3. Proper sys.path configuration  
4. Import warning suppression
"""

from __future__ import annotations

import os
import sys
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
    "index.rst",   # Use index_furo.rst instead
]

# Use simplified index
master_doc = "index_furo"

# =============================================================================
# EXTENSIONS - AUTOAPI FOCUSED
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
    # NOTE: sphinx.ext.autosummary is COMPLETELY EXCLUDED to avoid conflicts
]

# =============================================================================
# AUTOAPI CONFIGURATION - NAMESPACE PACKAGE FIXES
# =============================================================================

# Test with core package only
SPHINX_PACKAGES = os.environ.get("SPHINX_PACKAGES", "core")

# CRITICAL FIX: Point autoapi_dirs to the haive package directory, not src/
# This ensures AutoAPI discovers modules as haive.core.* not core.*
ALL_PACKAGES = {
    "core": "/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive",
    "agents": "/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive", 
    "tools": "/home/will/Projects/haive/backend/haive/packages/haive-tools/src/haive",
    "games": "/home/will/Projects/haive/backend/haive/packages/haive-games/src/haive",
    "dataflow": "/home/will/Projects/haive/backend/haive/packages/haive-dataflow/src/haive",
    "mcp": "/home/will/Projects/haive/backend/haive/packages/haive-mcp/src/haive",
    "prebuilt": "/home/will/Projects/haive/backend/haive/packages/haive-prebuilt/src/haive",
}

autoapi_type = "python"

if SPHINX_PACKAGES == "all":
    autoapi_dirs = list(ALL_PACKAGES.values())
    print(f"📦 Building ALL packages ({len(autoapi_dirs)} total)")
else:
    requested_packages = [p.strip() for p in SPHINX_PACKAGES.split(",")]
    autoapi_dirs = []
    
    for pkg in requested_packages:
        pkg_name = pkg.replace("haive-", "") if pkg.startswith("haive-") else pkg
        if pkg_name in ALL_PACKAGES:
            autoapi_dirs.append(ALL_PACKAGES[pkg_name])
            print(f"📦 Adding package: haive.{pkg_name}")
        else:
            print(f"⚠️  Unknown package: {pkg}")

    if not autoapi_dirs:
        print("❌ No valid packages specified, defaulting to haive.core")
        autoapi_dirs = [ALL_PACKAGES["core"]]

# CRITICAL FIX: Add src/ directories to sys.path for imports, not haive/ directories
src_dirs = []
for autoapi_dir in autoapi_dirs:
    # Convert /path/to/packages/haive-core/src/haive -> /path/to/packages/haive-core/src
    src_dir = str(Path(autoapi_dir).parent)
    if src_dir not in src_dirs:
        src_dirs.append(src_dir)

for src_dir in src_dirs:
    if src_dir not in sys.path:
        sys.path.insert(0, src_dir)
        print(f"🐍 Added to Python path: {src_dir}")

print(f"📁 AutoAPI directories: {autoapi_dirs}")
print(f"🎯 This should generate proper haive.* namespace documentation!")

# CRITICAL FIX: Enable namespace package support
autoapi_python_use_implicit_namespaces = True

# AutoAPI settings - NAMESPACE AWARE
autoapi_root = "api"
autoapi_add_toctree_entry = False  # Manual control for better integration
autoapi_generate_api_docs = True
autoapi_python_class_content = "both"
autoapi_member_order = "bysource"
autoapi_keep_files = True

# Use simple templates without autosummary
autoapi_template_dir = "_templates/autoapi_simple"

# CRITICAL FIX: Options that work with namespace packages
autoapi_options = [
    "members",
    "undoc-members", 
    "show-inheritance",
    "imported-members",  # Helps with namespace package discovery
    # Autosummary options are DISABLED to prevent conflicts
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

# CRITICAL FIX: Suppress import resolution warnings during discovery
suppress_warnings = [
    "autoapi.python_import_resolution",
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
    "navigation_depth": 4,
    "collapse_navigation": False,
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

# Intersphinx
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "pydantic": ("https://docs.pydantic.dev/latest/", None),
}

# Copy button
copybutton_prompt_text = r">>> |\.\.\.\ |\$ "
copybutton_prompt_is_regexp = True

# Myst Parser
myst_enable_extensions = [
    "colon_fence",
    "deflist",
    "substitution",
    "tasklist",
]

# =============================================================================
# AUTOAPI SKIP MEMBER FUNCTION
# =============================================================================

def autoapi_skip_member(app, what, name, obj, skip, options):
    """Simple skip logic for cleaner documentation."""
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
# SETUP FUNCTION
# =============================================================================

def setup(app):
    """Setup function with AutoAPI skip member."""
    # Connect AutoAPI skip member
    app.connect("autoapi-skip-member", autoapi_skip_member)
    
    # Create custom CSS
    def create_custom_css(app):
        """Create minimal custom CSS."""
        static_dir = Path(app.srcdir) / "_static"
        static_dir.mkdir(exist_ok=True)
        
        css_content = """
/* Haive AutoAPI Documentation Fixes */

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

/* Better spacing for namespace documentation */
.content {
    line-height: 1.6;
}
"""
        
        css_file = static_dir / "custom.css"
        with open(css_file, 'w') as f:
            f.write(css_content)
    
    app.connect('builder-inited', create_custom_css)

print("✅ AutoAPI Namespace Fix configuration loaded")
print(f"📦 AutoAPI dirs: {len(autoapi_dirs)} packages")
print(f"🎨 Theme: {html_theme}")
print(f"🔧 Extensions: {len(extensions)} extensions")
print(f"🔬 Namespace package support: {autoapi_python_use_implicit_namespaces}")