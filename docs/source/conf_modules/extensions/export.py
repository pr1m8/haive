"""Export and output extensions.

This module configures extensions for exporting documentation to different formats:
- PDF generation and export
- Presentation generation (reveal.js)
- Multi-version documentation
- Custom 404 pages
- Favicon support
- Data visualization
"""

from typing import Any


def get_config(
    enable_pdf: bool = False,
    enable_presentations: bool = False,
    enable_multiversion: bool = False,
    enable_404: bool = True,
    enable_favicon: bool = True,
    enable_data_viewer: bool = False,
    enable_git_integration: bool = True,
) -> dict[str, Any]:
    """Get export and output extension configuration.

    Args:
        enable_pdf: Enable PDF generation
        enable_presentations: Enable reveal.js presentations
        enable_multiversion: Enable multi-version documentation
        enable_404: Enable custom 404 pages
        enable_favicon: Enable custom favicon support
        enable_data_viewer: Enable interactive data visualization
        enable_git_integration: Enable advanced Git integration

    Returns:
        Dictionary with export configuration
    """
    config = {}
    extensions = []

    # PDF generation
    if enable_pdf:
        extensions.extend(
            [
                "sphinx_pdf_generate",  # PDF generation
                "sphinx_simplepdf",  # Simple PDF export
            ], )
        config.update(_get_pdf_config())

    # Presentation generation
    if enable_presentations:
        extensions.append("sphinx_revealjs")
        config.update(_get_revealjs_config())

    # Multi-version documentation
    if enable_multiversion:
        extensions.append("sphinx_multiversion")
        config.update(_get_multiversion_config())

    # Custom 404 pages
    if enable_404:
        extensions.append("notfound.extension")
        config.update(_get_404_config())

    # Favicon support
    if enable_favicon:
        extensions.append("sphinx_favicon")
        config.update(_get_favicon_config())

    # Data visualization
    if enable_data_viewer:
        extensions.append("sphinx_data_viewer")
        config.update(_get_data_viewer_config())

    # Git integration
    if enable_git_integration:
        extensions.append("sphinx_git")
        config.update(_get_git_config())

    config["extensions"] = extensions
    return config


def _get_pdf_config() -> dict[str, Any]:
    """Get PDF generation configuration."""
    return {
        # LaTeX configuration for PDF output
        "latex_engine":
        "pdflatex",
        "latex_elements": {
            "papersize":
            "letterpaper",
            "pointsize":
            "10pt",
            "preamble":
            r"""
\usepackage{charter}
\usepackage[defaultsans]{lato}
\usepackage{inconsolata}
""",
        },
        "latex_documents": [
            (
                "index",
                "haive.tex",
                "Haive AI Agent Framework Documentation",
                "William R. Astley",
                "manual",
            ),
        ],
        # SimplePDF configuration
        "simplepdf_vars": {
            "primary": "#0066cc",
            "secondary": "#666666",
            "cover": True,
            "back_cover": True,
        },
    }


def _get_revealjs_config() -> dict[str, Any]:
    """Get reveal.js presentation configuration."""
    return {
        "revealjs_script_conf": {
            "controls": True,
            "progress": True,
            "hash": True,
            "center": True,
            "transition": "slide",
        },
        "revealjs_script_plugins": [
            {
                "name": "RevealHighlight",
                "src": "revealjs4/plugin/highlight/highlight.js",
            },
            {
                "name": "RevealNotes",
                "src": "revealjs4/plugin/notes/notes.js",
            },
        ],
    }


def _get_multiversion_config() -> dict[str, Any]:
    """Get multi-version documentation configuration."""
    return {
        "smv_tag_whitelist": r"^v\d+\.\d+\.\d+$",  # Only version tags
        "smv_branch_whitelist":
        r"^(main|master|develop)$",  # Only main branches
        "smv_released_pattern": r"^tags/.*$",  # Released versions
        "smv_outputdir_format": "{config.release}",  # Output directory format
        "smv_prefer_remote_refs": False,  # Use local refs
    }


def _get_404_config() -> dict[str, Any]:
    """Get custom 404 page configuration."""
    return {
        "notfound_pagename": "404",
        "notfound_template": "404.html",
        "notfound_context": {
            "title":
            "Page Not Found",
            "body":
            "The page you're looking for doesn't exist. Try searching or check our main documentation.",
        },
        "notfound_urls_prefix": "/",
    }


def _get_favicon_config() -> dict[str, Any]:
    """Get favicon configuration."""
    return {
        "favicons": [
            {
                "rel": "icon",
                "sizes": "16x16",
                "href": "favicon-16x16.png",
                "type": "image/png",
            },
            {
                "rel": "icon",
                "sizes": "32x32",
                "href": "favicon-32x32.png",
                "type": "image/png",
            },
            {
                "rel": "apple-touch-icon",
                "sizes": "180x180",
                "href": "apple-touch-icon.png",
                "type": "image/png",
            },
        ],
    }


def _get_data_viewer_config() -> dict[str, Any]:
    """Get data viewer configuration."""
    return {
        "data_viewer_defaults": {
            "table_classes": ["table", "table-striped"],
            "show_index": True,
        },
    }


def _get_git_config() -> dict[str, Any]:
    """Get advanced Git integration configuration."""
    return {
        "git_commit_link": "https://github.com/pr1m8/haive/commit/{commit}",
        "git_last_updated_format": "%Y-%m-%d %H:%M:%S",
        "git_untracked_check_dependencies": False,
    }


def get_epub_config() -> dict[str, Any]:
    """Get EPUB e-book configuration."""
    return {
        "epub_title": "Haive AI Agent Framework",
        "epub_author": "William R. Astley",
        "epub_publisher": "Haive Project",
        "epub_copyright": "2025, William R. Astley",
        "epub_identifier": "haive-docs",
        "epub_scheme": "ISBN",
        "epub_uid": "haive-docs",
        "epub_cover": ("_static/haive-logo.png", "epub-cover.html"),
        "epub_pre_files": [("index.html", "Welcome")],
        "epub_post_files": [("genindex.html", "Index")],
        "epub_exclude_files": ["search.html"],
        "epub_tocdepth": 3,
        "epub_tocdup": True,
        "epub_tocscope": "default",
        "epub_fix_images": True,
        "epub_max_image_width": 0,
        "epub_show_urls": "footnote",
        "epub_use_index": True,
    }


def get_minimal_config() -> dict[str, Any]:
    """Get minimal export configuration."""
    return get_config(
        enable_pdf=False,
        enable_presentations=False,
        enable_multiversion=False,
        enable_404=True,
        enable_favicon=False,
        enable_data_viewer=False,
        enable_git_integration=False,
    )


def get_standard_config() -> dict[str, Any]:
    """Get standard export configuration."""
    return get_config(
        enable_pdf=False,
        enable_presentations=False,
        enable_multiversion=False,
        enable_404=True,
        enable_favicon=True,
        enable_data_viewer=False,
        enable_git_integration=True,
    )


def get_full_config() -> dict[str, Any]:
    """Get full export configuration."""
    config = get_config(
        enable_pdf=True,
        enable_presentations=True,
        enable_multiversion=True,
        enable_404=True,
        enable_favicon=True,
        enable_data_viewer=True,
        enable_git_integration=True,
    )

    # Add EPUB configuration
    config.update(get_epub_config())

    return config
