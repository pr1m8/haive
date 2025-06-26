"""Modern Sphinx configuration for Haive documentation.

Simplified and optimized configuration following modern Sphinx best practices.
"""

from datetime import datetime
from pathlib import Path
import sys
import warnings


# Suppress warnings during build
warnings.filterwarnings("ignore", category=DeprecationWarning)

# ==============================================================================
# Project Information
# ==============================================================================

project = "Haive"
author = "William R. Astley"
copyright = f"2025-{datetime.now().year}, {author}"
version = "1.0"
release = "1.0.0"

# ==============================================================================
# Path Setup for Monorepo
# ==============================================================================

# Get paths
conf_dir = Path(__file__).parent
docs_dir = conf_dir.parent
workspace_dir = docs_dir.parent

# Add package source paths
packages_dir = workspace_dir / "packages"
package_names = [
    "haive-core", "haive-agents", "haive-tools", "haive-games",
    "haive-dataflow", "haive-prebuilt", "haive-mcp"
]

for package in package_names:
    src_path = packages_dir / package / "src"
    if src_path.exists():
        sys.path.insert(0, str(src_path))

# Add custom extensions
sys.path.insert(0, str(conf_dir / "_extensions"))

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

    # Enhanced documentation
    "sphinx_copybutton",
    "sphinx_design",
    "myst_parser",
    "sphinxcontrib.mermaid",

    # Custom Haive extension
    "haive_sphinx_ext",
]

# ==============================================================================
# Source File Configuration
# ==============================================================================

source_suffix = {
    ".rst": "restructuredtext",
    ".md": "markdown",
}

exclude_patterns = [
    "_build", "Thumbs.db", ".DS_Store", "**/.git", "**/node_modules",
    "**/__pycache__", "**/test_*.py", "**/tests/**", "**/*_test.py",
    "**/example.py", "**/examples/**", "**/ui.py", "**/demo.py",
    "**/*.egg-info/**", "generated/**"
    # Note: Notebooks remain in root /notebooks/ directory as preferred
]

# ==============================================================================
# HTML Theme Configuration
# ==============================================================================

html_theme = "furo"
html_title = "Haive Documentation"
html_short_title = "Haive"

# Static files
html_static_path = ["_static"]
html_css_files = ["modern.css"]
html_js_files = ["modern.js"]

# Modern theme options
html_theme_options = {
    # Branding
    "light_logo": "images/haive-logo-light.svg",
    "dark_logo": "images/haive-logo-dark.svg",

    # Colors - Clean modern palette
    "light_css_variables": {
        "color-brand-primary": "#0f62fe",      # IBM Blue
        "color-brand-content": "#0f62fe",
        "color-foreground-primary": "#161616",  # Near black
        "color-foreground-secondary": "#525252", # Gray 60
        "color-background-primary": "#ffffff",   # White
        "color-background-secondary": "#f4f4f4", # Gray 10
        "color-api-background": "#f8f9fa",
        "color-api-background-hover": "#e9ecef",
        "color-sidebar-background": "#f8f9fa",
        "color-sidebar-background-border": "#e5e5e5",
    },
    "dark_css_variables": {
        "color-brand-primary": "#4589ff",      # Blue 50
        "color-brand-content": "#4589ff",
        "color-foreground-primary": "#f4f4f4", # Gray 10
        "color-foreground-secondary": "#c6c6c6", # Gray 30
        "color-background-primary": "#161616",  # Gray 100
        "color-background-secondary": "#262626", # Gray 90
        "color-api-background": "#262626",
        "color-api-background-hover": "#393939",
        "color-sidebar-background": "#262626",
        "color-sidebar-background-border": "#393939",
    },

    # Navigation
    "sidebar_hide_name": False,
    "navigation_with_keys": True,
    "navigation_depth": 3,

    # Features
    "announcement": (
        '<div style="text-align: center;">'
        '🚧 Documentation is actively being improved - '
        '<a href="https://github.com/will-astley/haive/issues" style="color: inherit; text-decoration: underline;">'
        'feedback welcome</a>!'
        '</div>'
    ),

    # Footer
    "footer_icons": [
        {
            "name": "GitHub",
            "url": "https://github.com/will-astley/haive",
            "html": '<svg height="16" width="16" viewBox="0 0 16 16"><path fill="currentColor" d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"/></svg>',
        },
        {
            "name": "Discord",
            "url": "https://discord.gg/haive",
            "html": '<svg height="16" width="16" viewBox="0 0 24 24"><path fill="currentColor" d="M19.27 5.33C17.94 4.71 16.5 4.26 15 4a.09.09 0 0 0-.07.03c-.18.33-.39.76-.53 1.09a16.09 16.09 0 0 0-4.8 0c-.14-.34-.35-.76-.54-1.09c-.01-.02-.04-.03-.07-.03c-1.5.26-2.93.71-4.27 1.33c-.01 0-.02.01-.03.02c-2.72 4.07-3.47 8.03-3.1 11.95c0 .02.01.04.03.05c1.8 1.32 3.53 2.12 5.24 2.65c.03.01.06 0 .07-.02c.4-.55.76-1.13 1.07-1.74c.02-.04 0-.08-.04-.09c-.57-.22-1.11-.48-1.64-.78c-.04-.02-.04-.08-.01-.11c.11-.08.22-.17.33-.25c.02-.02.05-.02.07-.01c3.44 1.57 7.15 1.57 10.55 0c.02-.01.05-.01.07.01c.11.09.22.17.33.26c.04.03.04.09-.01.11c-.52.31-1.07.56-1.64.78c-.04.01-.05.06-.04.09c.32.61.68 1.19 1.07 1.74c.03.01.06.02.09.01c1.72-.53 3.45-1.33 5.25-2.65c.02-.01.03-.03.03-.05c.44-4.53-.73-8.46-3.1-11.95c-.01-.01-.02-.02-.04-.02zM8.52 14.91c-1.03 0-1.89-.95-1.89-2.12s.84-2.12 1.89-2.12c1.06 0 1.9.96 1.89 2.12c0 1.17-.84 2.12-1.89 2.12zm6.97 0c-1.03 0-1.89-.95-1.89-2.12s.84-2.12 1.89-2.12c1.06 0 1.9.96 1.89 2.12c0 1.17-.83 2.12-1.89 2.12z"/></svg>',
        }
    ],

    # Source links
    "source_repository": "https://github.com/will-astley/haive/",
    "source_branch": "main",
    "source_directory": "docs/source/",
}

# ==============================================================================
# Extension Configurations
# ==============================================================================

# Autodoc settings
autodoc_default_options = {
    "members": True,
    "undoc-members": True,
    "show-inheritance": True,
    "special-members": "__init__",
    "member-order": "bysource",
}
autodoc_typehints = "description"
autodoc_typehints_format = "short"

# Autosummary
autosummary_generate = True
autosummary_generate_overwrite = True

# Napoleon (Google docstrings)
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = True
napoleon_include_private_with_doc = False
napoleon_use_admonition_for_examples = True
napoleon_use_admonition_for_notes = True

# Copy button
copybutton_prompt_text = r">>> |\.\.\. |\$ |In \[\d*\]: | {2,5}\.\.\.: | {5,8}: "
copybutton_prompt_is_regexp = True

# MyST Markdown
myst_enable_extensions = [
    "deflist", "tasklist", "colon_fence", "smartquotes",
    "linkify", "strikethrough"
]

# Intersphinx
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "pydantic": ("https://docs.pydantic.dev/latest/", None),
}

# Mermaid
mermaid_version = "10.6.1"

# ==============================================================================
# Build Configuration
# ==============================================================================

# Performance
templates_path = ["_templates"]
exclude_patterns.extend([
    "**/.tox", "**/.pytest_cache", "**/build", "**/dist"
])

# Suppress specific warnings
suppress_warnings = [
    "autosummary.import_cycle",
    "autodoc.import_object",
    "ref.citation",
    "misc.highlighting_failure"
]

# Language
language = "en"

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
# Custom Event Handlers
# ==============================================================================

def setup(app):
    """Setup function for custom modifications."""
    # Ensure directories exist
    static_dir = conf_dir / "_static"
    static_dir.mkdir(exist_ok=True)

    # Create minimal custom files if they don't exist
    modern_css = static_dir / "modern.css"
    if not modern_css.exists():
        modern_css.write_text("""
/* Modern Haive Documentation Styles */
:root {
    --font-stack: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    --font-stack-monospace: 'SF Mono', Monaco, 'Cascadia Code', 'Roboto Mono', Consolas, monospace;
}

body {
    font-family: var(--font-stack);
    line-height: 1.7;
}

code, pre {
    font-family: var(--font-stack-monospace);
}

/* Improved code blocks */
.highlight {
    border-radius: 8px;
    overflow: hidden;
}

/* Clean card styles */
.sd-card {
    border-radius: 12px;
    border: 1px solid var(--color-background-secondary);
    transition: all 0.2s ease;
}

.sd-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(0,0,0,0.12);
}
""")

    modern_js = static_dir / "modern.js"
    if not modern_js.exists():
        modern_js.write_text("""
// Modern Haive Documentation JavaScript
document.addEventListener('DOMContentLoaded', function() {
    console.log('🤖 Haive Documentation loaded');
    
    // Smooth scrolling
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const href = this.getAttribute('href');
            if (href !== '#') {
                e.preventDefault();
                document.querySelector(href)?.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });
    
    // Copy button feedback
    document.querySelectorAll('.copybtn').forEach(btn => {
        btn.addEventListener('click', function() {
            const original = this.textContent;
            this.textContent = '✓';
            setTimeout(() => this.textContent = original, 1000);
        });
    });
});
""")

    return {
        "version": "1.0",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
