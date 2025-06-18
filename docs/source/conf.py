# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'haive'
copyright = '2025, William R. Astley'
author = 'William R. Astley'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = []

templates_path = ['_templates']
exclude_patterns = []



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']
# docs/source/conf.py
import os
import sys
from pathlib import Path
import warnings

# Suppress warnings
warnings.filterwarnings("ignore")

# -- Path setup --------------------------------------------------------------
# Get workspace root (docs/source/conf.py -> workspace root)
workspace_root = Path(__file__).resolve().parents[2]

# Add package paths
packages = ['haive-core', 'haive-agents', 'haive-tools', 'haive-games', 'haive-dataflow', 'haive-prebuilt']
for package in packages:
    package_src = workspace_root / 'packages' / package / 'src'
    if package_src.exists():
        sys.path.insert(0, str(package_src))
        print(f"Added: {package_src}")

# Add main src
main_src = workspace_root / "src"
if main_src.exists():
    sys.path.insert(0, str(main_src))

# -- Project information -----------------------------------------------------
project = 'Haive'
copyright = '2025, William R. Astley'
author = 'William R. Astley'
release = '1.0.0'

# -- General configuration ---------------------------------------------------
extensions = [
    # Sphinx built-in
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'sphinx.ext.intersphinx',
    'sphinx.ext.todo',
    'sphinx.ext.coverage',
    
    # Third-party extensions
    'sphinx_autodoc_typehints',
    'sphinx_copybutton',
    'sphinx_tabs.tabs',
    'sphinx_design',
    'myst_parser',
    'sphinxcontrib.mermaid',
    'sphinx_togglebutton',
]

# -- AutoAPI configuration (alternative to autodoc) --------------------------
# Comment out if you want to use autodoc instead
# extensions.append('autoapi.extension')
# autoapi_dirs = [
#     str(workspace_root / 'packages' / pkg / 'src') 
#     for pkg in packages
# ]
# autoapi_type = 'python'
# autoapi_options = [
#     'members',
#     'undoc-members',
#     'show-inheritance',
#     'show-module-summary',
#     'imported-members',
# ]

# -- Autodoc configuration ---------------------------------------------------
autodoc_default_options = {
    'members': True,
    'member-order': 'bysource',
    'special-members': '__init__',
    'undoc-members': True,
    'exclude-members': '__weakref__'
}

# Mock imports that might cause issues
autodoc_mock_imports = []

# Type hints configuration
typehints_fully_qualified = False
always_document_param_types = True
typehints_document_rtype = True

# -- Autosummary configuration -----------------------------------------------
autosummary_generate = True
autosummary_imported_members = True

# -- MyST configuration ------------------------------------------------------
myst_enable_extensions = [
    "deflist",
    "tasklist",
    "html_image",
    "colon_fence",
    "smartquotes",
    "replacements",
    "linkify",
    "strikethrough",
]

# -- Options for HTML output -------------------------------------------------
html_theme = 'furo'
html_static_path = ['_static']
html_title = "Haive Documentation"

# Theme options
html_theme_options = {
    "light_css_variables": {
        "color-brand-primary": "#2962ff",
        "color-brand-content": "#2962ff",
    },
    "dark_css_variables": {
        "color-brand-primary": "#4fc3f7",
        "color-brand-content": "#4fc3f7",
    },
}

# -- Intersphinx configuration -----------------------------------------------
intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
    'pydantic': ('https://docs.pydantic.dev/latest/', None),
    'langchain': ('https://python.langchain.com/', None),
}

# Suppress specific warnings
suppress_warnings = ['autosummary', 'autodoc.import_object']