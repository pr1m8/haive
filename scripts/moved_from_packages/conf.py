"""Sphinx configuration for haive-mcp documentation.

This file configures Sphinx to generate documentation for the haive-mcp package
using autodoc, autosummary, and Google-style docstrings with comprehensive
type hint support.
"""

import sys
from datetime import datetime
from pathlib import Path

# Add source to path
docs_dir = Path(__file__).parent
package_dir = docs_dir.parent
src_dir = package_dir / "src"
sys.path.insert(0, str(src_dir.absolute()))

# Also add haive-core to path for proper imports
haive_backend_dir = package_dir.parent.parent
sys.path.insert(0, str(haive_backend_dir.absolute()))

# Project information
project = "haive-mcp"
copyright = f"{datetime.now().year}, Haive Team"
author = "Haive Team"
version = "0.1.0"
release = "0.1.0"

# Extensions
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
    "sphinx.ext.coverage",
    "sphinx.ext.todo",
    "sphinx_autodoc_typehints",
    "sphinx_copybutton",
    "myst_parser",
    "sphinx_tabs.tabs",
    "sphinx_design",
]

# Autodoc settings
autodoc_default_options = {
    "members": True,
    "member-order": "bysource",
    "special-members": "__init__",
    "undoc-members": True,
    "exclude-members": "__weakref__",
    "show-inheritance": True,
    "private-members": False,
    "inherited-members": False,
}

autodoc_typehints = "both"
autodoc_typehints_format = "short"
autodoc_class_signature = "separated"
autodoc_mock_imports = ["mcp", "fastmcp"]  # Mock MCP imports if not available

# Autosummary settings
autosummary_generate = True
autosummary_imported_members = False
autosummary_generate_overwrite = True
autosummary_mockup_modules = ["haive.mcp"]

# Napoleon settings (for Google-style docstrings)
napoleon_google_docstring = True
napoleon_numpy_docstring = False
napoleon_include_init_with_doc = True
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = True
napoleon_use_admonition_for_notes = True
napoleon_use_admonition_for_references = True
napoleon_use_ivar = False
napoleon_use_param = True
napoleon_use_rtype = True
napoleon_preprocess_types = True
napoleon_type_aliases = {
    "MCPConfig": "haive.mcp.config.MCPConfig",
    "MCPServerConfig": "haive.mcp.config.MCPServerConfig",
    "MCPTransport": "haive.mcp.config.MCPTransport",
}
napoleon_attr_annotations = True

# Type hints settings
typehints_defaults = "comma"
typehints_document_rtype = True
typehints_use_rtype = True
typehints_use_signature = True
typehints_use_signature_return = True

# MyST settings (for Markdown)
myst_enable_extensions = [
    "colon_fence",
    "deflist",
    "tasklist",
    "html_admonition",
    "html_image",
    "replacements",
    "smartquotes",
    "strikethrough",
]

myst_heading_anchors = 3

# Intersphinx mapping
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "pydantic": ("https://docs.pydantic.dev", None),
    "langchain": ("https://python.langchain.com/docs", None),
    "haive-core": ("https://haive.readthedocs.io/projects/core", None),
}

# Add any paths that contain templates here
templates_path = ["_templates"]

# List of patterns to exclude
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store", "**.ipynb_checkpoints"]

# The name of the Pygments style to use
pygments_style = "sphinx"
pygments_dark_style = "monokai"

# HTML output options
html_theme = "sphinx_rtd_theme"
html_theme_options = {
    "navigation_depth": 4,
    "collapse_navigation": False,
    "sticky_navigation": True,
    "includehidden": True,
    "titles_only": False,
    "display_version": True,
    "prev_next_buttons_location": "bottom",
    "style_external_links": True,
}

# Add any paths that contain custom static files
html_static_path = ["_static"]

# Custom CSS files
html_css_files = [
    "custom.css",
]

# HTML title
html_title = f"{project} v{version}"

# HTML logo
# html_logo = "_static/logo.png"

# HTML favicon
# html_favicon = "_static/favicon.ico"

# Output file base name for HTML help builder
htmlhelp_basename = "haivemcpdoc"

# LaTeX output options
latex_elements = {
    "papersize": "a4paper",
    "pointsize": "10pt",
    "preamble": r"""
\usepackage{inconsolata}
\setcounter{tocdepth}{2}
""",
}

# Grouping the document tree into LaTeX files
latex_documents = [
    ("index", "haive-mcp.tex", "haive-mcp Documentation", "Haive Team", "manual"),
]

# Man pages output
man_pages = [("index", "haive-mcp", "haive-mcp Documentation", ["Haive Team"], 1)]

# Texinfo output
texinfo_documents = [
    (
        "index",
        "haive-mcp",
        "haive-mcp Documentation",
        "Haive Team",
        "haive-mcp",
        "Model Context Protocol integration for Haive",
        "Miscellaneous",
    ),
]

# Source suffix
source_suffix = {
    ".rst": "restructuredtext",
    ".md": "markdown",
}

# Master doc
master_doc = "index"

# Language
language = "en"

# TODO extension settings
todo_include_todos = True

# Copy button settings
copybutton_prompt_text = r">>> |\.\.\. |\$ |In \[\d*\]: | {2,5}\.\.\.: | {5,8}: "
copybutton_prompt_is_regexp = True

# Suppress specific warnings
suppress_warnings = ["autosummary", "autosummary.import_cycle"]


# Custom setup
def setup(app):
    """Custom Sphinx setup."""
    app.add_css_file("custom.css")
