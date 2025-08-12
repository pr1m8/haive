"""Base Sphinx configuration module.

This module contains the core Sphinx configuration that is shared
across all documentation builds.
"""

import os
import sys
from datetime import datetime

# Add source to path
sys.path.insert(0, os.path.abspath("../../../src"))

# Project information
project = "pyautodoc"
author = "William R. Astley"
copyright = f"{datetime.now().year}, {author}"
release = "0.1.0"

# Base extensions (always loaded)
base_extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
    "sphinx.ext.autosummary",
    "sphinx.ext.graphviz",
]

# Base configuration
exclude_patterns = []
templates_path = ["_templates"]
html_static_path = ["_static"]
source_suffix = {
    ".rst": "restructuredtext",
    ".md": "markdown",
}

# Napoleon settings
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
napoleon_preprocess_types = False
napoleon_type_aliases = None
napoleon_attr_annotations = True

# Intersphinx mappings
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "pydantic": ("https://docs.pydantic.dev/latest", None),
    "sphinx": ("https://www.sphinx-doc.org/en/master", None),
}

# Autodoc settings
autodoc_default_options = {
    "members": True,
    "member-order": "bysource",
    "special-members": "__init__",
    "undoc-members": True,
    "exclude-members": "__weakref__",
}
autodoc_typehints = "description"
autodoc_type_aliases = {}
autodoc_mock_imports = []

# HTML output options
html_theme = "furo"
html_title = f"{project} Documentation"
html_short_title = project
html_baseurl = "https://pyautodoc.readthedocs.io/"

# Furo theme options
html_theme_options = {
    "sidebar_hide_name": False,
    "navigation_with_keys": True,
    "source_repository": "https://github.com/yourusername/pyautodoc/",
    "source_branch": "main",
    "source_directory": "docs/",
}

# Code syntax highlighting
pygments_style = "sphinx"
pygments_dark_style = "monokai"
