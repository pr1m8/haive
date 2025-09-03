"""AutoAPI Namespace Fix - FAST VERSION for testing.

This is the same namespace fix but with aggressive file limiting to speed up builds.
Use this to quickly test that the namespace discovery is working properly.

The namespace fix has been VERIFIED - AutoAPI now generates haive.* instead of core.*
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

project = "Haive AI Agent Framework - Fast Test"
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
]

# Use simplified index
master_doc = "index_furo"

# =============================================================================
# EXTENSIONS - MINIMAL FOR SPEED
# =============================================================================

extensions = [
    # CRITICAL: AutoAPI MUST BE FIRST
    "autoapi.extension",
    
    # Only essential extensions for fast testing
    "sphinx.ext.napoleon",
    "myst_parser",
]

# =============================================================================
# AUTOAPI CONFIGURATION - FAST TESTING
# =============================================================================

# Test with core package only
SPHINX_PACKAGES = os.environ.get("SPHINX_PACKAGES", "core")

# VERIFIED FIX: Point to haive package directory for proper namespace
autoapi_dirs = ["/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive"]

# Add src directory to Python path for imports
src_dir = "/home/will/Projects/haive/backend/haive/packages/haive-core/src"
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)
    print(f"🐍 Added to Python path: {src_dir}")

print(f"📁 AutoAPI directories: {autoapi_dirs}")
print(f"🎯 VERIFIED: This generates proper haive.* namespace documentation!")

# CRITICAL: Enable namespace package support
autoapi_python_use_implicit_namespaces = True

# AutoAPI settings - FAST
autoapi_type = "python"
autoapi_root = "api"
autoapi_add_toctree_entry = False
autoapi_generate_api_docs = True
autoapi_python_class_content = "both"
autoapi_member_order = "bysource"
autoapi_keep_files = True

# Minimal options for speed
autoapi_options = [
    "members",
    "undoc-members", 
    "show-inheritance",
]

# AGGRESSIVE IGNORE LIST for speed testing
autoapi_ignore = [
    # Test files and directories
    "*/test_*.py",
    "*/tests/*",
    "*_test.py",
    "*/conftest.py",
    
    # Example files
    "*/examples/*",
    "*/example_*.py",
    "*_example.py",
    "*_demo.py",
    
    # Build artifacts
    "*/__pycache__/*",
    "*.pyc",
    
    # SPEED OPTIMIZATION: Skip large/complex modules for testing
    "*/engine/document/*",           # Large document processing modules
    "*/engine/embedding/*",          # Embedding modules can be complex
    "*/models/llm/providers/*",      # Skip individual provider files for speed
    "*/persistence/store/*",         # Skip store implementations
    "*/utils/visualize_graph_utils.py", # Skip visualization utilities
    "*/graph/state_graph/components/*",  # Skip complex graph components
]

# Suppress warnings for clean output
suppress_warnings = [
    "autoapi.python_import_resolution",
]

# =============================================================================
# THEME CONFIGURATION - MINIMAL FURO
# =============================================================================

html_theme = "furo"

html_theme_options = {
    "light_css_variables": {
        "color-brand-primary": "#2563eb",
        "color-brand-content": "#2563eb",
    },
    "sidebar_hide_name": False,
    "navigation_with_keys": True,
}

html_static_path = ["_static"]
html_title = f"🤖 {project} Documentation - NAMESPACE TEST"

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

# Myst Parser
myst_enable_extensions = [
    "colon_fence",
    "deflist",
]

# =============================================================================
# SKIP MEMBER FUNCTION - SIMPLE
# =============================================================================

def autoapi_skip_member(app, what, name, obj, skip, options):
    """Simple skip logic for fast testing."""
    # Skip Pydantic internals only
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
    """Minimal setup function for fast testing."""
    # Connect AutoAPI skip member
    app.connect("autoapi-skip-member", autoapi_skip_member)
    
    # Create minimal custom CSS
    def create_minimal_css(app):
        """Create minimal custom CSS."""
        static_dir = Path(app.srcdir) / "_static"
        static_dir.mkdir(exist_ok=True)
        
        css_content = """
/* Minimal Haive Test CSS */
.highlight {
    border-radius: 6px;
    margin: 1em 0;
}

.py.class, .py.function, .py.method {
    margin: 1.5em 0;
    border-left: 3px solid var(--color-brand-primary);
    padding-left: 1em;
}
"""
        
        css_file = static_dir / "custom.css"
        with open(css_file, 'w') as f:
            f.write(css_content)
    
    app.connect('builder-inited', create_minimal_css)

print("✅ Fast AutoAPI Namespace Test configuration loaded")
print(f"📦 AutoAPI dirs: {len(autoapi_dirs)} packages")
print(f"🎨 Theme: {html_theme}")
print(f"🔧 Extensions: {len(extensions)} extensions")
print(f"🔬 Namespace package support: {autoapi_python_use_implicit_namespaces}")
print("🚀 AGGRESSIVE optimization for speed testing - many modules skipped!")