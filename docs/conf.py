# conf.py with enhanced styling options
import os
import sys

# Add the src directory to the path so sphinx can find your modules
sys.path.insert(0, os.path.abspath('../../src'))

# Project information
project = 'Haive'
copyright = '2025, Your Name'
author = 'Your Name'
release = '0.1.0'

# Extensions
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
    'sphinx.ext.intersphinx',
    'sphinx.ext.autosectionlabel',
    'sphinx.ext.todo',
    'myst_parser',
    'sphinx.ext.autosummary',
    'sphinx_copybutton',  # Add copy button to code blocks
]

# Theme configuration
html_theme = 'furo'  # A clean, modern theme (install with: poetry add sphinx-furo)
# Alternative: 'pydata_sphinx_theme' for a more feature-rich theme

# Theme options
html_theme_options = {
    # Furo theme options
    "sidebar_hide_name": False,
    "light_css_variables": {
        "color-brand-primary": "#3776ab",  # Python blue
        "color-brand-content": "#3776ab",
        "color-admonition-background": "#f8f9fb",
        "font-stack": "system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue', sans-serif",
        "font-stack--monospace": "SFMono-Regular, Menlo, Monaco, Consolas, 'Liberation Mono', 'Courier New', monospace",
    },
    "dark_css_variables": {
        "color-brand-primary": "#5994ce",  # Lighter blue for dark mode
        "color-brand-content": "#5994ce",
    },
    "footer_icons": [
        {
            "name": "GitHub",
            "url": "https://github.com/yourusername/haive",
            "html": """
                <svg stroke="currentColor" fill="currentColor" stroke-width="0" viewBox="0 0 16 16">
                    <path fill-rule="evenodd" d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0 0 16 8c0-4.42-3.58-8-8-8z"></path>
                </svg>
            """,
            "class": "",
        },
    ],
}

# HTML configuration
html_static_path = ['_static']
html_css_files = ['custom.css']
html_js_files = ['custom.js']
html_title = f"{project} Documentation"
html_short_title = project
html_favicon = '_static/favicon.ico'  # Add your favicon
html_logo = '_static/logo.png'  # Add your logo

# autodoc configuration
autodoc_typehints = 'description'
autodoc_member_order = 'bysource'
autodoc_default_options = {
    'members': True,
    'show-inheritance': True,
    'undoc-members': True,
    'special-members': '__init__',
}

# Napoleon settings for docstring formats
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = True
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = True
napoleon_use_admonition_for_notes = True
napoleon_use_admonition_for_references = True
napoleon_use_rtype = True

# intersphinx configuration
intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
}

# MyST parser options
myst_enable_extensions = [
    "colon_fence",
    "deflist",
    "dollarmath",
    "amsmath",
    "html_image",
]
myst_heading_anchors = 3

# Enable todo directives
todo_include_todos = True

# Enable autosummary
autosummary_generate = True