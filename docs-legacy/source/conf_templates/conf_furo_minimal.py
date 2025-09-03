"""Ultra-minimal Furo test configuration - NO AutoAPI."""

from __future__ import annotations

# =============================================================================
# PROJECT INFORMATION
# =============================================================================

project = "Haive AI Agent Framework - Test"
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
    "api/*",       # Exclude any API docs
]

# Use simplified index
master_doc = "index_furo"

# =============================================================================
# EXTENSIONS - ULTRA MINIMAL
# =============================================================================

extensions = [
    # Core Sphinx extensions - ABSOLUTE MINIMUM
    "sphinx.ext.napoleon", 
    "sphinx.ext.viewcode",
    
    # Enhanced documentation
    "sphinx_copybutton",
    "myst_parser",
    # NOTE: NO AutoAPI, NO autodoc, NO autosummary
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

print("✅ Ultra-minimal Furo test configuration loaded")
print(f"🎨 Theme: {html_theme}")
print(f"🔧 Extensions: {len(extensions)} minimal extensions")