"""Preset configurations for common documentation scenarios.

This module provides ready-to-use configurations for common documentation needs:
- API-only documentation
- Tutorial-focused documentation
- Research/academic documentation
- Blog-style documentation
- Multi-language documentation
"""

from typing import Any

# Import from __init__ module in same directory
try:
    from __init__ import (
        create_custom_config,
        create_full_config,
        create_standard_config,
    )
except ImportError:
    # If that fails, try absolute imports
    from pathlib import Path
    import sys

    current_dir = Path(__file__).parent
    sys.path.insert(0, str(current_dir))

    from __init__ import (
        create_custom_config,
        create_full_config,
        create_standard_config,
    )


def create_api_only_config(
    project_name: str = "API Documentation",
    author: str = "Author",
    packages: list[str] | None = None,
    github_repo: str | None = None,
) -> dict[str, Any]:
    """Create configuration focused purely on API documentation.

    Features:
    - AutoAPI with comprehensive API generation
    - Enhanced type hints
    - Minimal content features
    - Professional theme optimized for API browsing

    Args:
        project_name: Name of the project
        author: Project author
        packages: List of packages to document
        github_repo: GitHub repository for source links

    Returns:
        API-focused configuration dictionary
    """
    return create_custom_config(
        project_name=project_name,
        author=author,
        packages=packages,
        enable_api_docs=True,
        enable_notebooks=False,
        enable_diagrams=False,
        enable_pdf=False,
        enable_presentations=False,
        github_repo=github_repo,
    )


def create_tutorial_config(
    project_name: str = "Tutorial Documentation",
    author: str = "Author",
    packages: list[str] | None = None,
    github_repo: str | None = None,
    base_url: str | None = None,
) -> dict[str, Any]:
    """Create configuration optimized for tutorials and learning.

    Features:
    - Jupyter notebook support
    - Interactive code execution
    - Example galleries
    - Copy buttons and enhanced UX
    - Minimal API documentation

    Args:
        project_name: Name of the project
        author: Project author
        packages: List of packages to document
        github_repo: GitHub repository
        base_url: Base URL for the documentation

    Returns:
        Tutorial-focused configuration dictionary
    """
    return create_custom_config(
        project_name=project_name,
        author=author,
        packages=packages,
        enable_api_docs=False,  # Minimal API docs
        enable_notebooks=True,
        enable_diagrams=True,
        enable_pdf=False,
        enable_presentations=False,
        github_repo=github_repo,
        base_url=base_url,
    )


def create_research_config(
    project_name: str = "Research Documentation",
    author: str = "Researcher",
    packages: list[str] | None = None,
    github_repo: str | None = None,
    base_url: str | None = None,
) -> dict[str, Any]:
    """Create configuration for research and academic documentation.

    Features:
    - Mathematical notation support
    - Citation management
    - Interactive exercises and proofs
    - Jupyter notebook integration
    - PDF export for papers
    - Presentation generation

    Args:
        project_name: Name of the research project
        author: Researcher name
        packages: List of packages to document
        github_repo: GitHub repository
        base_url: Base URL for the documentation

    Returns:
        Research-focused configuration dictionary
    """
    config = create_custom_config(
        project_name=project_name,
        author=author,
        packages=packages,
        enable_api_docs=True,
        enable_notebooks=True,
        enable_diagrams=True,
        enable_pdf=True,
        enable_presentations=True,
        github_repo=github_repo,
        base_url=base_url,
    )

    # Add research-specific extensions
    research_extensions = [
        "sphinx_exercise",  # Interactive exercises
        "sphinx_proof",  # Mathematical proofs
        "sphinxcontrib.bibtex",  # Bibliography support
        # "sphinx_math_dollar",  # DISABLED: Incompatible with Sphinx 8.2.3 - causes NotImplementedError
    ]

    config["extensions"].extend(research_extensions)

    # Research-specific configuration
    config.update(
        {
            "bibtex_bibfiles": ["references.bib"],
            "bibtex_default_style": "alpha",
            "math_number_all": True,
            "math_eqref_format": "Eq. {number}",
        },
    )

    return config


def create_blog_config(
    project_name: str = "Blog",
    author: str = "Blogger",
    github_repo: str | None = None,
    base_url: str | None = None,
) -> dict[str, Any]:
    """Create configuration for blog-style documentation.

    Features:
    - Markdown-first writing
    - Social sharing (Open Graph)
    - SEO optimization
    - Minimal technical features
    - Clean, readable theme

    Args:
        project_name: Name of the blog
        author: Blog author
        github_repo: GitHub repository
        base_url: Base URL for the blog

    Returns:
        Blog-focused configuration dictionary
    """
    config = create_custom_config(
        project_name=project_name,
        author=author,
        packages=None,  # No packages for blog
        enable_api_docs=False,
        enable_notebooks=False,
        enable_diagrams=False,
        enable_pdf=False,
        enable_presentations=False,
        github_repo=github_repo,
        base_url=base_url,
    )

    # Blog-specific optimizations
    config.update(
        {
            "html_title": f"📝 {project_name}",
            "html_short_title": project_name.split()[0],  # Use first word
        },
    )

    # Enhanced social features
    blog_extensions = [
        "sphinxext.opengraph",  # Social sharing
        # "sphinx_sitemap",  # DISABLED: Incompatible with Sphinx 8.2.3 - is_directory_builder attribute error
        "ablog",  # Blog features (if available)
    ]

    existing_extensions = config.get("extensions", [])
    for ext in blog_extensions:
        if ext not in existing_extensions:
            existing_extensions.append(ext)

    return config


def create_multilang_config(
    project_name: str = "Multilingual Documentation",
    author: str = "Author",
    languages: list[str] = ["en", "es", "fr"],
    packages: list[str] | None = None,
    github_repo: str | None = None,
    base_url: str | None = None,
) -> dict[str, Any]:
    """Create configuration for multi-language documentation.

    Features:
    - Internationalization support
    - Language switching
    - Localized content
    - Standard documentation features

    Args:
        project_name: Name of the project
        author: Project author
        languages: List of language codes (e.g., ["en", "es", "fr"])
        packages: List of packages to document
        github_repo: GitHub repository
        base_url: Base URL for the documentation

    Returns:
        Multi-language configuration dictionary
    """
    config = create_standard_config(
        project_name=project_name,
        author=author,
        packages=packages,
        github_repo=github_repo,
        base_url=base_url,
    )

    # Add internationalization
    i18n_extensions = [
        "sphinx.ext.intl",
    ]

    config["extensions"].extend(i18n_extensions)

    # I18n configuration
    config.update(
        {
            "language": languages[0],  # Default language
            "locale_dirs": ["locale/"],
            "gettext_compact": False,
            "gettext_additional_targets": ["index"],
        },
    )

    return config


def create_corporate_config(
    project_name: str = "Corporate Documentation",
    author: str = "Company",
    packages: list[str] | None = None,
    github_repo: str | None = None,
    base_url: str | None = None,
) -> dict[str, Any]:
    """Create configuration for corporate/enterprise documentation.

    Features:
    - Professional appearance
    - PDF export for offline distribution
    - Comprehensive API documentation
    - Quality assurance tools
    - Version management

    Args:
        project_name: Name of the project
        author: Company name
        packages: List of packages to document
        github_repo: GitHub repository
        base_url: Base URL for the documentation

    Returns:
        Corporate-focused configuration dictionary
    """
    config = create_full_config(
        project_name=project_name,
        author=author,
        packages=packages,
        github_repo=github_repo,
        base_url=base_url,
    )

    # Corporate-specific enhancements
    config.update(
        {
            "html_show_sphinx": False,  # Hide "Created with Sphinx"
            "html_show_copyright": True,
            "html_last_updated_fmt": "%Y-%m-%d %H:%M:%S",
        },
    )

    # Add corporate extensions
    corporate_extensions = [
        "sphinx_multiversion",  # Version management
        "sphinx_pdf_generate",  # Professional PDF output
        "sphinxcontrib.spelling",  # Spell checking
    ]

    existing_extensions = config.get("extensions", [])
    for ext in corporate_extensions:
        if ext not in existing_extensions:
            existing_extensions.append(ext)

    return config


# Convenience mapping for easy access
PRESETS = {
    "api_only": create_api_only_config,
    "tutorial": create_tutorial_config,
    "research": create_research_config,
    "blog": create_blog_config,
    "multilang": create_multilang_config,
    "corporate": create_corporate_config,
}


def get_preset(preset_name: str, **kwargs) -> dict[str, Any]:
    """Get a preset configuration by name.

    Args:
        preset_name: Name of the preset (api_only, tutorial, research, etc.)
        **kwargs: Arguments to pass to the preset function

    Returns:
        Configuration dictionary for the preset

    Raises:
        ValueError: If preset_name is not recognized
    """
    if preset_name not in PRESETS:
        available = ", ".join(PRESETS.keys())
        raise ValueError(f"Unknown preset '{preset_name}'. Available: {available}")

    return PRESETS[preset_name](**kwargs)


def list_presets() -> list[str]:
    """Get list of available preset names.

    Returns:
        List of preset names
    """
    return list(PRESETS.keys())
