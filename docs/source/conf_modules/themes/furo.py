"""Furo theme configuration.

This module provides comprehensive Furo theme configuration with:
- Advanced styling and CSS variables
- Navigation and sidebar configuration
- Light and dark mode support
- Professional typography and layout
"""
from __future__ import annotations

from typing import Any


def get_config(
    project_name: str = 'Haive',
    sidebar_width: str = '15rem',
    content_width: str = '50rem',
    enable_announcement: bool = False,
    github_url: str | None = None,
    pypi_url: str | None = None,
) -> dict[str, Any]:
    """Get Furo theme configuration.

    Args:
        project_name: Name of the project for titles
        sidebar_width: Width of the sidebar
        content_width: Width of the main content area
        enable_announcement: Show announcement banner
        github_url: GitHub repository URL
        pypi_url: PyPI package URL

    Returns:
        Dictionary with Furo theme configuration
    """
    config = {}

    # Basic theme settings
    config['html_theme'] = 'furo'
    config['html_title'] = f"🤖 {project_name} AI Agent Framework"
    config['html_short_title'] = project_name

    # Static files
    config['html_static_path'] = ['_static']

    # CSS and JS files
    config['html_css_files'] = [
        ('haive-minimal.css', {}),  # Custom styling
    ]

    config['html_js_files'] = [
        ('haive-graph-visualizations.js', {}),
        ('agent-visualization.js', {}),
        ('enhanced-search.js', {}),
        ('showcase-interactions.js', {}),
        ('enhanced-interface.js', {}),
        ('agent-demo-utils.js', {}),
    ]

    # Theme options
    config['html_theme_options'] = _get_theme_options(
        project_name,
        sidebar_width,
        content_width,
        enable_announcement,
        github_url,
        pypi_url,
    )

    # Sidebar configuration
    config['html_sidebars'] = {
        '**': [
            'sidebar/brand.html',
            'sidebar/search.html',
            'sidebar/scroll-start.html',
            'sidebar/navigation.html',
            'sidebar/scroll-end.html',
        ],
    }

    return config


def _get_theme_options(
    project_name: str,
    sidebar_width: str,
    content_width: str,
    enable_announcement: bool,
    github_url: str | None,
    pypi_url: str | None,
) -> dict[str, Any]:
    """Get Furo theme options."""
    options = {
        # === SIDEBAR ===
        'sidebar_hide_name':
        False,
        'navigation_with_keys':
        True,
        'top_of_page_buttons': ['edit', 'view'],
        'show_prev_next':
        True,
        # === NAVIGATION ===
        'navigation_depth':
        4,
        'collapse_navigation':
        False,
        'titles_only':
        False,
        # === TABLE OF CONTENTS ===
        'show_toc_level':
        3,
        'toc_title':
        'On this page',
        # === CSS VARIABLES ===
        'light_css_variables':
        _get_light_css_variables(sidebar_width, content_width),
        'dark_css_variables':
        _get_dark_css_variables(),
        # === PYGMENTS ===
        'pygments_light_style':
        'default',
        'pygments_dark_style':
        'github-dark',
        # === SOURCE REPOSITORY ===
        'source_repository':
        github_url or 'https://github.com/will-astley/haive',
        'source_branch':
        'main',
        'source_directory':
        'docs/source/',
    }

    # Add announcement if enabled
    if enable_announcement:
        options['announcement'] = (
            f"🤖 <strong>{project_name} AI Agent Framework</strong> - "
            'Build intelligent agents with ease! 🚀')

    # Add footer icons
    footer_icons = []
    if github_url:
        footer_icons.append(_get_github_icon(github_url))
    if pypi_url:
        footer_icons.append(_get_pypi_icon(pypi_url))

    if footer_icons:
        options['footer_icons'] = footer_icons

    return options


def _get_light_css_variables(sidebar_width: str,
                             content_width: str) -> dict[str, str]:
    """Get light mode CSS variables."""
    return {
        # === LAYOUT ===
        'sidebar-width': sidebar_width,
        'content-width': content_width,
        'content-padding': '2rem',
        # === TYPOGRAPHY ===
        'font-stack--headings':
        "'Inter', system-ui, -apple-system, sans-serif",
        'font-stack':
        "system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Noto Sans', 'Ubuntu', 'Cantarell', 'Helvetica Neue', sans-serif",
        'font-stack--monospace':
        "'JetBrains Mono', 'Consolas', 'Monaco', 'Courier New', monospace",
        'font-size--small--2': '0.75rem',
        'font-size--small--3': '0.6875rem',
        'font-size--small': '0.875rem',
        'font-size--normal': '1rem',
        'font-size--medium': '1.125rem',
        'line-height--normal': '1.7',
        'line-height--small': '1.5',
        # === COLORS ===
        'color-brand-primary': '#0066cc',
        'color-brand-content': '#0066cc',
        'color-foreground-primary': '#1a1a1a',
        'color-foreground-secondary': '#666666',
        'color-foreground-muted': '#6b7280',
        'color-background-primary': '#ffffff',
        'color-background-secondary': '#f8f9fa',
        'color-background-hover': '#f0f0f0',
        'color-background-hover--transparent': '#f3f4f6',
        'color-background-item': '#e5e7eb',
        'color-sidebar-background': '#fafafa',
        'color-sidebar-background-border': '#e1e4e8',
        'color-announcement-background': '#007acc',
        'color-announcement-text': '#ffffff',
        # === ADMONITIONS ===
        'color-admonition-background': '#f8f9fa',
        'admonition-font-size': '0.9rem',
        'admonition-title-font-size': '0.95rem',
        # === CODE ===
        'color-inline-code-background': '#f1f5f9',
        'color-inline-code-foreground': '#334155',
        'color-code-tab-size': '4',
        'color-code-max-lines': 'none',
        'font-size--code': '0.875rem',
        'font-size--code--small': '0.8125rem',
        'code-font-size': '0.85rem',
        # === API DOCUMENTATION ===
        'color-api-background': '#f8fafc',
        'color-api-background-hover': '#f1f5f9',
        'color-api-overall': '#64748b',
        'color-api-name': '#0f172a',
        'color-api-pre-name': '#475569',
        'color-api-paren': '#94a3b8',
        'color-api-keyword': '#7c3aed',
        'api-font-size': '0.9rem',
        # === CARDS AND BORDERS ===
        'color-card-border': '#e2e8f0',
        'color-card-marginals-background': '#f8fafc',
        # === SEARCH ===
        'color-search-background': '#ffffff',
        'color-search-foreground': '#1f2937',
        'color-search-border': '#d1d5db',
        'color-search-border--focus': '#3b82f6',
        # === SIDEBAR SPACING ===
        'sidebar-item-spacing-vertical': '0.5rem',
        'sidebar-item-spacing-horizontal': '1rem',
        'sidebar-item-font-size': '0.9rem',
        'sidebar-search-space-above': '1rem',
        # === TOC SPACING ===
        'toc-spacing-vertical': '0.5rem',
        'toc-spacing-horizontal': '1rem',
        'toc-font-size': '0.85rem',
        # === PROBLEMATIC COLOR ===
        'color-problematic': '#dc2626',
    }


def _get_dark_css_variables() -> dict[str, str]:
    """Get dark mode CSS variables."""
    return {
        # === COLORS ===
        'color-brand-primary': '#4da6ff',
        'color-brand-content': '#4da6ff',
        'color-foreground-primary': '#e2e8f0',
        'color-foreground-secondary': '#a0aec0',
        'color-foreground-muted': '#9ca3af',
        'color-background-primary': '#1a202c',
        'color-background-secondary': '#2d3748',
        'color-background-hover': '#4a5568',
        'color-background-hover--transparent': '#374151',
        'color-sidebar-background': '#1e2835',
        'color-sidebar-background-border': '#2d3748',
        'color-announcement-background': '#007acc',
        'color-announcement-text': '#ffffff',
        # === ADMONITIONS ===
        'color-admonition-background': '#2d3748',
        # === CODE ===
        'color-inline-code-background': '#1e293b',
        'color-inline-code-foreground': '#cbd5e1',
        # === API DOCUMENTATION ===
        'color-api-background': '#0f172a',
        'color-api-background-hover': '#1e293b',
        # === CARDS AND BORDERS ===
        'color-card-border': '#334155',
        'color-card-marginals-background': '#1e293b',
        # === SEARCH ===
        'color-search-background': '#1f2937',
        'color-search-foreground': '#f9fafb',
        'color-search-border': '#4b5563',
        'color-search-border--focus': '#60a5fa',
    }


def _get_github_icon(github_url: str) -> dict[str, str]:
    """Get GitHub footer icon configuration."""
    return {
        'name': 'GitHub',
        'url': github_url,
        'html': """
            <svg stroke="currentColor" fill="currentColor" stroke-width="0" viewBox="0 0 16 16">
                <path fill-rule="evenodd" d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0 0 16 8c0-4.42-3.58-8-8-8z"></path>
            </svg>
        """,
        'class': '',
    }


def _get_pypi_icon(pypi_url: str) -> dict[str, str]:
    """Get PyPI footer icon configuration."""
    return {
        'name': 'PyPI',
        'url': pypi_url,
        'html': """
            <svg stroke="currentColor" fill="currentColor" stroke-width="0" viewBox="0 0 24 24">
                <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"></path>
            </svg>
        """,
        'class': '',
    }


def get_minimal_config() -> dict[str, Any]:
    """Get minimal Furo theme configuration."""
    return get_config(
        project_name='Project',
        enable_announcement=False,
    )


def get_standard_config() -> dict[str, Any]:
    """Get standard Furo theme configuration."""
    return get_config(
        project_name='Haive',
        github_url='https://github.com/will-astley/haive',
        enable_announcement=False,
    )


def get_full_config() -> dict[str, Any]:
    """Get full Furo theme configuration."""
    return get_config(
        project_name='Haive',
        github_url='https://github.com/will-astley/haive',
        pypi_url='https://pypi.org/project/haive/',
        enable_announcement=True,
    )
