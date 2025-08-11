"""Simplified shared Sphinx configuration for Haive monorepo packages.

This module provides a clean, simple configuration system for individual
packages in the Haive monorepo to use for their documentation.
"""

import os
import sys
from pathlib import Path
from typing import Dict, Any, List

# Package-specific color schemes for Haive ecosystem
HAIVE_PACKAGE_THEMES = {
    'haive-core': {'primary': '#dc3545', 'content': '#c82333'},      # Red - Core system
    'haive-agents': {'primary': '#28a745', 'content': '#218838'},    # Green - AI agents  
    'haive-dataflow': {'primary': '#007bff', 'content': '#0056b3'},  # Blue - Data flow
    'haive-games': {'primary': '#6f42c1', 'content': '#5a32a3'},     # Purple - Games
    'haive-mcp': {'primary': '#fd7e14', 'content': '#e8680f'},       # Orange - MCP
    'haive-tools': {'primary': '#20c997', 'content': '#1aa085'},     # Teal - Tools
    'haive-prebuilt': {'primary': '#e83e8c', 'content': '#d91a72'},  # Pink - Prebuilt
}

# Core extensions that all Haive packages should use
HAIVE_CORE_EXTENSIONS = [
    # Sphinx built-ins
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'sphinx.ext.intersphinx',
    'sphinx.ext.githubpages',
    
    # Essential third-party
    'autoapi.extension',
    'myst_parser',
    'sphinx_design',
    'sphinx_copybutton',
    'sphinx_togglebutton',
    'sphinxcontrib.autodoc_pydantic',
    'sphinx_autodoc_typehints',
]

def get_base_config(package_name: str, package_path: str, is_root: bool = False) -> Dict[str, Any]:
    """Get base Sphinx configuration for a Haive package.
    
    Args:
        package_name: Name of the package (e.g., 'haive-core')
        package_path: Absolute path to the package source
        is_root: Whether this is root documentation (aggregates all packages)
    
    Returns:
        Dictionary of Sphinx configuration settings
    """
    
    # Basic project information
    config = {
        'project': f'Haive {package_name.replace("haive-", "").title()}' if not is_root else 'Haive Ecosystem',
        'author': 'Haive Team', 
        'copyright': '2025, Haive Team',
        'release': '1.0.0',
        
        # Extensions
        'extensions': HAIVE_CORE_EXTENSIONS.copy(),
        
        # General configuration
        'templates_path': ['_templates'],
        'html_static_path': ['_static'],
        'exclude_patterns': ['_build', 'Thumbs.db', '.DS_Store'],
        'add_module_names': False,
        
        # AutoAPI configuration
        'autoapi_type': 'python',
        'autoapi_dirs': [package_path],
        'autoapi_template_dir': '_autoapi_templates',
        'autoapi_add_toctree_entry': True,
        'autoapi_generate_api_docs': True,
        'autoapi_options': [
            'members',
            'undoc-members', 
            'show-inheritance',
            'show-module-summary',
        ],
        
        # Napoleon (Google/NumPy docstring support)
        'napoleon_google_docstring': True,
        'napoleon_numpy_docstring': True,
        'napoleon_include_init_with_doc': False,
        
        # MyST parser configuration
        'myst_enable_extensions': [
            'deflist',
            'tasklist', 
            'html_image',
            'colon_fence',
            'smartquotes',
        ],
        
        # HTML theme configuration
        'html_theme': 'furo',
        'html_theme_options': {
            'sidebar_hide_name': False,
        },
        
        # Copy button configuration  
        'copybutton_prompt_text': r'>>> |\.\.\. |\$ |In \[\d*\]: | {2,5}\.\.\.: | {5,8}: ',
        'copybutton_prompt_is_regexp': True,
        'copybutton_remove_prompts': True,
        
        # Type hints configuration
        'typehints_fully_qualified': False,
        'typehints_use_signature': True,
        
        # Intersphinx mappings (links to external docs)
        'intersphinx_mapping': {
            'python': ('https://docs.python.org/3', None),
            'pydantic': ('https://docs.pydantic.dev/latest', None),
            'sphinx': ('https://www.sphinx-doc.org/en/master', None),
        },
    }
    
    # Apply package-specific theme if available
    if package_name in HAIVE_PACKAGE_THEMES:
        theme = HAIVE_PACKAGE_THEMES[package_name]
        config['html_theme_options'].update({
            'light_css_variables': {
                'color-brand-primary': theme['primary'],
                'color-brand-content': theme['content'],
            },
            'dark_css_variables': {
                'color-brand-primary': theme['primary'], 
                'color-brand-content': theme['content'],
            }
        })
    
    # Root documentation gets additional configuration
    if is_root:
        # Root docs should aggregate all packages
        config['html_title'] = 'Haive Documentation'
        config['html_short_title'] = 'Haive'
        
        # Add intersphinx mappings for all Haive packages
        for pkg_name in HAIVE_PACKAGE_THEMES.keys():
            config['intersphinx_mapping'][pkg_name] = (f'../{pkg_name}/_build/html', None)
    
    return config