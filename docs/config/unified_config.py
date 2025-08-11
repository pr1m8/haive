"""Unified Sphinx configuration for PyAutoDoc monorepo.

This module provides a single, clean configuration system for all documentation
in the PyAutoDoc project, replacing the previous dual-config approach.
"""

import os
import sys
import logging
from pathlib import Path
from typing import Dict, Any, Optional, List
from dataclasses import dataclass

# Try to import tomllib (Python 3.11+) or fallback to tomli
try:
    import tomllib
except ImportError:
    import tomli as tomllib

logger = logging.getLogger(__name__)


@dataclass
class PackageColors:
    """Color scheme for a package."""
    primary: str
    content: str


# Package-specific color schemes
PACKAGE_THEMES = {
    'haive-core': PackageColors('#dc3545', '#c82333'),
    'haive-ml': PackageColors('#28a745', '#218838'),
    'haive-api': PackageColors('#007bff', '#0056b3'),
    'haive-cli': PackageColors('#6f42c1', '#5a32a3'),
    'haive-storage': PackageColors('#fd7e14', '#e8680f'),
    'haive-utils': PackageColors('#20c997', '#1aa085'),
}

# Core extensions that all packages use
CORE_EXTENSIONS = [
    # Sphinx built-ins
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'sphinx.ext.intersphinx',
    'sphinx.ext.githubpages',
    
    # Third-party essentials
    'myst_parser',
    'sphinx_copybutton',
    'seed_intersphinx_mapping',
]

# Optional extensions for enhanced functionality
OPTIONAL_EXTENSIONS = [
    'sphinx_design',
    'sphinx_togglebutton',
    'sphinx_tabs.tabs',
    'sphinxext.opengraph',
    'sphinx_sitemap',
]

# Package-specific extensions
PACKAGE_EXTENSIONS = {
    'haive-cli': ['sphinx_click'],
    'haive-api': ['sphinxcontrib.openapi'],
    'haive-ml': ['nbsphinx'],
}


def get_package_version(package_name: str, repo_root: Path) -> str:
    """Extract version from package pyproject.toml.
    
    Args:
        package_name: Name of the package
        repo_root: Repository root path
        
    Returns:
        Version string (defaults to '0.1.0' if not found)
    """
    try:
        if package_name == "pyautodoc":
            pyproject_path = repo_root / "pyproject.toml"
        else:
            package_dir = repo_root / "packages" / package_name
            pyproject_path = package_dir / "pyproject.toml"
        
        if pyproject_path.exists():
            with open(pyproject_path, 'rb') as f:
                data = tomllib.load(f)
                # Try Poetry format first
                version = data.get('tool', {}).get('poetry', {}).get('version')
                if version:
                    return version
                # Try PEP 621 format
                return data.get('project', {}).get('version', '0.1.0')
    except Exception as e:
        logger.warning(f"Could not extract version for {package_name}: {e}")
    
    return '0.1.0'


def discover_packages(repo_root: Path) -> List[Dict[str, Any]]:
    """Discover all packages in the monorepo.
    
    Args:
        repo_root: Repository root path
        
    Returns:
        List of package information dictionaries
    """
    packages = []
    packages_dir = repo_root / "packages"
    
    if packages_dir.exists():
        for pkg_dir in packages_dir.iterdir():
            if pkg_dir.is_dir() and (pkg_dir / "pyproject.toml").exists():
                packages.append({
                    'name': pkg_dir.name,
                    'path': pkg_dir,
                    'has_docs': (pkg_dir / "docs").exists(),
                })
    
    return packages


def get_intersphinx_mapping(package_name: str, repo_root: Path, is_root: bool = False) -> Dict[str, tuple]:
    """Generate intersphinx mappings for cross-references.
    
    Args:
        package_name: Name of the current package
        repo_root: Repository root path
        is_root: Whether this is root documentation
        
    Returns:
        Dictionary of intersphinx mappings
    """
    # Base mappings (cleared to avoid duplicates with seed-intersphinx-mapping)
    mappings = {}
    
    # Add cross-package mappings
    packages = discover_packages(repo_root)
    
    if is_root:
        # Root can reference all packages using relative paths
        for pkg_info in packages:
            pkg_name = pkg_info['name'].replace('-', '_')
            mappings[pkg_name] = (f'packages/{pkg_info["name"]}/index.html', None)
    else:
        # Packages reference each other and root
        mappings['pyautodoc'] = ('../../index.html', None)
        
        for pkg_info in packages:
            if pkg_info['name'] != package_name:
                pkg_name = pkg_info['name'].replace('-', '_')
                mappings[pkg_name] = (f'../{pkg_info["name"]}/index.html', None)
    
    return mappings


def create_sphinx_config(
    package_name: str,
    package_path: str,
    is_root: bool = False,
    enable_optional_extensions: bool = True,
    theme: str = 'furo'
) -> Dict[str, Any]:
    """Create Sphinx configuration for a package or root documentation.
    
    Args:
        package_name: Name of the package (use 'pyautodoc' for root)
        package_path: Path to package source code
        is_root: Whether this is root documentation
        enable_optional_extensions: Whether to enable optional extensions
        theme: Sphinx theme to use ('furo' or 'sphinx_rtd_theme')
        
    Returns:
        Dictionary of Sphinx configuration options
        
    Raises:
        ValueError: If package_path is invalid
    """
    # Validate inputs
    if not package_name:
        raise ValueError("package_name cannot be empty")
    
    package_path = Path(package_path)
    if not is_root and not package_path.exists():
        raise ValueError(f"Package path does not exist: {package_path}")
    
    # Determine repository root
    if is_root:
        repo_root = Path(package_path).parent
    else:
        repo_root = Path(package_path).parents[1]
    
    # Store original sys.path for cleanup
    original_syspath = sys.path.copy()
    
    try:
        # Add source paths to Python path
        if not is_root:
            src_path = package_path
            if src_path.exists() and src_path.is_dir():
                sys.path.insert(0, str(src_path))
                logger.debug(f"Added {src_path} to Python path")
        
        # Build extensions list
        extensions = CORE_EXTENSIONS.copy()
        
        if enable_optional_extensions:
            extensions.extend(OPTIONAL_EXTENSIONS)
        
        # Add package-specific extensions
        if package_name in PACKAGE_EXTENSIONS:
            extensions.extend(PACKAGE_EXTENSIONS[package_name])
        
        # Get version
        version = get_package_version(package_name, repo_root)
        
        # Base configuration
        config = {
            # Project information
            'project': package_name.replace('-', ' ').title() if not is_root else 'PyAutoDoc',
            'author': 'PyAutoDoc Team',
            'copyright': '2025, PyAutoDoc Team',
            'version': version,
            'release': version,
            
            # Extensions
            'extensions': extensions,
            
            # Paths
            'templates_path': ['_templates'],
            'exclude_patterns': ['_build', 'Thumbs.db', '.DS_Store'],
            
            # Source parsing
            'source_suffix': {
                '.rst': None,
                '.md': None,
            },
            'master_doc': 'index',
            'language': 'en',
            
            # Intersphinx
            'intersphinx_mapping': get_intersphinx_mapping(package_name, repo_root, is_root),
            
            # seed-intersphinx-mapping
            'pkg_requirements_source': 'pyproject',
            'repository_root': str(repo_root if is_root else package_path.parent),
            
            # Napoleon settings
            'napoleon_google_docstring': True,
            'napoleon_numpy_docstring': True,
            'napoleon_include_init_with_doc': True,
            'napoleon_include_private_with_doc': False,
            'napoleon_include_special_with_doc': True,
            'napoleon_use_admonition_for_examples': True,
            'napoleon_use_admonition_for_notes': True,
            'napoleon_use_param': True,
            'napoleon_use_rtype': True,
            
            # Autodoc settings
            'autodoc_default_options': {
                'members': True,
                'member-order': 'bysource',
                'special-members': '__init__',
                'undoc-members': True,
                'exclude-members': '__weakref__',
            },
            
            # MyST settings
            'myst_enable_extensions': [
                'deflist',
                'tasklist',
                'colon_fence',
                'linkify',
            ],
        }
        
        # Theme configuration
        if theme == 'furo':
            colors = PACKAGE_THEMES.get(package_name, PackageColors('#2563eb', '#1d4ed8'))
            
            config.update({
                'html_theme': 'furo',
                'html_theme_options': {
                    'sidebar_hide_name': False,
                    'navigation_depth': 4,
                    'light_css_variables': {
                        'color-brand-primary': colors.primary,
                        'color-brand-content': colors.content,
                    },
                    'dark_css_variables': {
                        'color-brand-primary': colors.primary,
                        'color-brand-content': colors.content,
                    },
                }
            })
        else:
            config.update({
                'html_theme': 'sphinx_rtd_theme',
                'html_theme_options': {
                    'navigation_depth': 4,
                    'collapse_navigation': True,
                    'sticky_navigation': True,
                }
            })
        
        # Add static paths if they exist
        static_path = Path(package_path).parent / 'docs' / '_static'
        if static_path.exists():
            config['html_static_path'] = ['_static']
        
        return config
        
    except Exception as e:
        # Restore original sys.path on error
        sys.path = original_syspath
        logger.error(f"Error creating config for {package_name}: {e}")
        raise


# Convenience function for backward compatibility
def get_base_config(package_name: str, package_path: str, is_root: bool = False) -> Dict[str, Any]:
    """Get base Sphinx configuration (backward compatible wrapper).
    
    Args:
        package_name: Name of the package
        package_path: Path to package source code
        is_root: Whether this is root documentation
        
    Returns:
        Dictionary of Sphinx configuration options
    """
    return create_sphinx_config(package_name, package_path, is_root)