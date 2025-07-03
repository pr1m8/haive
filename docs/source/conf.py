"""Sphinx configuration for Haive documentation.

Configuration for building documentation for the Haive namespaced monorepo.
Uses Google-style docstrings and works with poetry/nox build system.
"""

import sys
import warnings
from datetime import datetime
from pathlib import Path

# Suppress specific warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", message=".*Matplotlib.*")

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
# Path Setup for Namespaced Monorepo
# ==============================================================================

# Get paths
conf_dir = Path(__file__).parent.absolute()
docs_dir = conf_dir.parent
workspace_dir = docs_dir.parent

# Add the workspace to Python path for imports
sys.path.insert(0, str(workspace_dir))

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
for package in package_names:
    src_path = packages_dir / package / "src"
    if src_path.exists():
        sys.path.insert(0, str(src_path))

# Add custom extensions
extensions_path = conf_dir / "_extensions"
if extensions_path.exists():
    sys.path.insert(0, str(extensions_path))

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
    "sphinx.ext.githubpages",
    # Enhanced documentation
    "sphinx_copybutton",
    "sphinx_design",
    "myst_parser",
    "sphinxcontrib.mermaid",
    # Custom Haive extension (if available)
]

# Try to load custom extension if it exists
# Temporarily disabled for faster builds
#     pass

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
    "**/__pycache__",
    "**/test_*.py",
    "**/tests/**",
    "**/*_test.py",
    "**/example.py",
    "**/examples/**",
    "**/ui.py",
    "**/demo.py",
    "**/*.egg-info/**",
    "generated/**",
    "_archive/**",
    "conf_*.py",
]

# ==============================================================================
# HTML Theme Configuration
# ==============================================================================

html_theme = "furo"
html_title = "Haive Documentation"
html_short_title = "Haive"

# Static files
html_static_path = ["_static"]
html_css_files = ["modern.css", "sidebar-fix.css"]
html_js_files = ["modern.js", "sidebar-fix.js"]

# Disable showcase files - they override all pages
# if (static_dir / "showcase.css").exists():
# if (static_dir / "showcase.js").exists():

# Modern theme options
html_theme_options = {
    # Branding
    "light_logo": "images/haive-logo-light.svg",
    "dark_logo": "images/haive-logo-dark.svg",
    # Colors - Professional palette
    "light_css_variables": {
        "color-brand-primary": "#0f62fe",  # IBM Blue
        "color-brand-content": "#4589ff",  # Lighter blue
        "color-foreground-primary": "#161616",
        "color-foreground-secondary": "#525252",
        "color-background-primary": "#ffffff",
        "color-background-secondary": "#fafbff",
        "color-api-background": "#f8faff",
        "color-api-background-hover": "#e6f0ff",
        "color-sidebar-background": "#f8faff",
        "color-sidebar-background-border": "#e0e7ff",
    },
    "dark_css_variables": {
        "color-brand-primary": "#4589ff",
        "color-brand-content": "#8a3ffc",  # Purple accent
        "color-foreground-primary": "#f4f4f4",
        "color-foreground-secondary": "#c6c6c6",
        "color-background-primary": "#0a0a0a",
        "color-background-secondary": "#1a1a1a",
        "color-api-background": "#1a1a1a",
        "color-api-background-hover": "#2a2a2a",
        "color-sidebar-background": "#1a1a1a",
        "color-sidebar-background-border": "#2a2a2a",
    },
    # Navigation
    "sidebar_hide_name": False,
    "navigation_with_keys": True,
    "navigation_depth": 3,
    # Features
    "announcement": (
        '<div style="text-align: center; font-weight: 600;">'
        "🤖 <strong>Haive AI Agent Framework</strong> - "
        "Building intelligent agents with Google-style documentation"
        "</div>"
    ),
    # Footer
    "footer_icons": [
        {
            "name": "GitHub",
            "url": "https://github.com/will-astley/haive",
            "html": '<svg height="16" width="16" viewBox="0 0 16 16"><path fill="currentColor" d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"/></svg>',
        },
    ],
    # Source links
    "source_repository": "https://github.com/will-astley/haive/",
    "source_branch": "main",
    "source_directory": "docs/source/",
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
}
autodoc_typehints = "description"
autodoc_typehints_format = "short"
autodoc_class_signature = "separated"

# Autosummary - disabled due to import errors
autosummary_generate = False
autosummary_generate_overwrite = False
autosummary_imported_members = False

# Napoleon (Google docstrings) - optimized settings
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = True
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = True
napoleon_use_admonition_for_notes = True
napoleon_use_admonition_for_references = False
napoleon_use_ivar = True
napoleon_use_param = True
napoleon_use_rtype = True
napoleon_use_keyword = True
napoleon_preprocess_types = True
napoleon_type_aliases: dict[str, str] = {
    # Add common type aliases if needed
}
napoleon_attr_annotations = True

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

# Intersphinx - link to other projects
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "pydantic": ("https://docs.pydantic.dev/latest/", None),
    "langchain": ("https://python.langchain.com/", None),
}

# Mermaid diagrams
mermaid_version = "10.6.1"

# ==============================================================================
# Build Configuration
# ==============================================================================

# Performance
templates_path = ["_templates"]
exclude_patterns.extend(["**/.tox", "**/.pytest_cache", "**/build", "**/dist"])

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
    # Ensure directories exist
    static_dir = conf_dir / "_static"
    static_dir.mkdir(exist_ok=True)

    # Create images directory if it doesn't exist
    images_dir = static_dir / "images"
    images_dir.mkdir(exist_ok=True)

    # Create minimal custom files if they don't exist
    modern_css = static_dir / "modern.css"
    if not modern_css.exists():
        modern_css.write_text(
            """
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

/* Google-style docstring formatting */
.sig-param .n {
    font-weight: 600;
}

.sig-return-typehint {
    font-style: italic;
}

/* Module and class headers */
.py.class, .py.function, .py.method {
    margin-top: 2rem;
    padding-top: 1rem;
    border-top: 1px solid var(--color-background-border);
}

/* Better spacing for docstring sections */
.rubric {
    margin-top: 1.5rem;
    margin-bottom: 0.5rem;
    font-weight: 600;
}
"""
        )

    modern_js = static_dir / "modern.js"
    if not modern_js.exists():
        modern_js.write_text(
            """
// Modern Haive Documentation JavaScript
document.addEventListener('DOMContentLoaded', function() {
    console.log('🤖 Haive Documentation loaded');

    // Smooth scrolling
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const href = this.getAttribute('href');
            if (href !== '#') {
                e.preventDefault();
                const target = document.querySelector(href);
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            }
        });
    });

    // Copy button feedback
    document.querySelectorAll('.copybtn').forEach(btn => {
        btn.addEventListener('click', function() {
            const original = this.textContent;
            this.textContent = '✓ Copied!';
            setTimeout(() => this.textContent = original, 1000);
        });
    });

    // Highlight current section in sidebar
    const observer = new IntersectionObserver(
        entries => {
            entries.forEach(entry => {
                const id = entry.target.getAttribute('id');
                if (id) {
                    const link = document.querySelector(`nav a[href="#${id}"]`);
                    if (entry.intersectionRatio > 0) {
                        link?.classList.add('current');
                    } else {
                        link?.classList.remove('current');
                    }
                }
            });
        },
        { rootMargin: '0px 0px -50% 0px' }
    );

    // Observe all sections with IDs
    document.querySelectorAll('section[id]').forEach(section => {
        observer.observe(section);
    });
});
"""
        )

    # Connect event handlers
    app.connect("autodoc-skip-member", skip_submodules)

    return {
        "version": "1.0",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
