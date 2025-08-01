"""Modular Sphinx Configuration System.

This package provides a modular approach to Sphinx configuration,
breaking down complex configurations into focused, reusable modules.

Main functions:
- create_minimal_config(): Basic documentation setup
- create_standard_config(): Common features for most projects
- create_full_config(): All features including advanced extensions
- create_custom_config(): Mix and match specific features
"""

from typing import Any, Dict, List, Optional

# Import all configuration modules - relative imports within package
from .core import logging, paths, project
from .extensions import (api_generation, content, core_sphinx, diagrams,
                         enhancement, export, external, quality)
from .themes import furo


def create_minimal_config(
    project_name: str = "Project",
    author: str = "Author",
    packages: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """Create minimal Sphinx configuration.

    Includes only essential features:
    - Basic project info
    - Path setup
    - Core Sphinx extensions
    - Simple theme

    Args:
        project_name: Name of the project
        author: Project author
        packages: List of packages to document

    Returns:
        Complete Sphinx configuration dictionary
    """
    config = {}

    # Core configuration
    config.update(project.get_minimal_config())
    config.update(paths.get_config(packages=packages))
    config.update(logging.get_minimal_config())

    # Minimal extensions
    config.update(core_sphinx.get_minimal_config())
    config.update(api_generation.get_minimal_config())
    config.update(enhancement.get_minimal_config())

    # Simple theme
    config.update(furo.get_minimal_config())

    # Combine all extensions
    config["extensions"] = _combine_extensions(config)

    return config


def create_standard_config(
    project_name: str = "Haive",
    author: str = "William R. Astley",
    packages: Optional[List[str]] = None,
    github_repo: str = "pr1m8/haive",
    base_url: str = "https://haive.readthedocs.io/",
) -> Dict[str, Any]:
    """Create standard Sphinx configuration.

    Includes commonly used features:
    - All minimal features
    - API documentation generation
    - Content enhancements
    - Basic diagrams
    - Quality tools
    - External integrations

    Args:
        project_name: Name of the project
        author: Project author
        packages: List of packages to document
        github_repo: GitHub repository (format: "owner/repo")
        base_url: Base URL for the documentation site

    Returns:
        Complete Sphinx configuration dictionary
    """
    config = {}

    # Core configuration
    config.update(project.get_config(project_name, author))
    config.update(paths.get_config(packages=packages))
    config.update(logging.get_config())

    # Standard extensions
    config.update(core_sphinx.get_standard_config())
    config.update(api_generation.get_standard_config())
    config.update(enhancement.get_standard_config())
    config.update(diagrams.get_standard_config())
    config.update(quality.get_standard_config())
    config.update(
        external.get_standard_config(github_repo=github_repo, base_url=base_url)
    )
    config.update(content.get_standard_config(packages=packages))
    config.update(export.get_standard_config())

    # Professional theme
    config.update(furo.get_standard_config())

    # Combine all extensions
    config["extensions"] = _combine_extensions(config)

    return config


def create_full_config(
    project_name: str = "Haive",
    author: str = "William R. Astley",
    packages: Optional[List[str]] = None,
    github_repo: str = "pr1m8/haive",
    base_url: str = "https://haive.readthedocs.io/",
) -> Dict[str, Any]:
    """Create full-featured Sphinx configuration.

    Includes all available features:
    - Everything from standard config
    - Advanced diagrams and visualizations
    - Export formats (PDF, presentations)
    - Multi-version support
    - Interactive features

    Args:
        project_name: Name of the project
        author: Project author
        packages: List of packages to document
        github_repo: GitHub repository (format: "owner/repo")
        base_url: Base URL for the documentation site

    Returns:
        Complete Sphinx configuration dictionary
    """
    config = {}

    # Core configuration
    config.update(project.get_config(project_name, author))
    config.update(paths.get_config(packages=packages))
    config.update(logging.get_config())

    # Full-featured extensions
    config.update(core_sphinx.get_full_config())
    config.update(api_generation.get_full_config())
    config.update(enhancement.get_full_config())
    config.update(diagrams.get_full_config())
    config.update(quality.get_full_config())
    config.update(external.get_full_config(github_repo=github_repo, base_url=base_url))
    config.update(content.get_full_config(packages=packages))
    config.update(export.get_full_config())

    # Advanced theme
    config.update(furo.get_full_config())

    # Combine all extensions
    config["extensions"] = _combine_extensions(config)

    return config


def create_custom_config(
    # Core settings
    project_name: str = "Project",
    author: str = "Author",
    packages: Optional[List[str]] = None,
    # Feature flags
    enable_api_docs: bool = True,
    enable_notebooks: bool = False,
    enable_diagrams: bool = False,
    enable_pdf: bool = False,
    enable_presentations: bool = False,
    # External settings
    github_repo: Optional[str] = None,
    base_url: Optional[str] = None,
) -> Dict[str, Any]:
    """Create custom Sphinx configuration.

    Mix and match specific features based on needs.

    Args:
        project_name: Name of the project
        author: Project author
        packages: List of packages to document
        enable_api_docs: Enable API documentation generation
        enable_notebooks: Enable Jupyter notebook support
        enable_diagrams: Enable diagram support
        enable_pdf: Enable PDF export
        enable_presentations: Enable presentation generation
        github_repo: GitHub repository (format: "owner/repo")
        base_url: Base URL for the documentation site

    Returns:
        Complete Sphinx configuration dictionary
    """
    config = {}

    # Always include core
    config.update(project.get_config(project_name, author))
    config.update(paths.get_config(packages=packages))
    config.update(logging.get_config())
    config.update(core_sphinx.get_config())

    # Conditional features
    if enable_api_docs:
        config.update(api_generation.get_config())
    else:
        config.update(api_generation.get_minimal_config())

    if enable_notebooks:
        config.update(content.get_config(enable_jupyter=True))
    else:
        config.update(content.get_minimal_config())

    if enable_diagrams:
        config.update(diagrams.get_config())
    else:
        config.update(diagrams.get_minimal_config())

    if enable_pdf or enable_presentations:
        config.update(
            export.get_config(
                enable_pdf=enable_pdf, enable_presentations=enable_presentations
            )
        )
    else:
        config.update(export.get_minimal_config())

    # Always include basic enhancements and theme
    config.update(enhancement.get_standard_config())
    config.update(furo.get_standard_config())

    # Optional external integrations
    if github_repo and base_url:
        config.update(external.get_config(github_repo=github_repo, base_url=base_url))

    # Combine all extensions
    config["extensions"] = _combine_extensions(config)

    return config


def _combine_extensions(config: Dict[str, Any]) -> List[str]:
    """Combine and deduplicate extensions from all modules.

    Args:
        config: Configuration dictionary containing extension lists

    Returns:
        Deduplicated list of all extensions
    """
    all_extensions = []

    # Find all extension lists in the config
    for key, value in config.items():
        if key == "extensions" and isinstance(value, list):
            all_extensions.extend(value)

    # Remove duplicates while preserving order
    seen = set()
    unique_extensions = []
    for ext in all_extensions:
        if ext not in seen:
            seen.add(ext)
            unique_extensions.append(ext)

    return unique_extensions


def get_all_available_extensions() -> Dict[str, List[str]]:
    """Get all available extensions organized by category.

    Returns:
        Dictionary mapping categories to lists of extensions
    """
    return {
        "core_sphinx": [
            "sphinx.ext.autodoc",
            "sphinx.ext.napoleon",
            "sphinx.ext.viewcode",
            "sphinx.ext.intersphinx",
            "sphinx.ext.todo",
        ],
        "api_generation": [
            "autoapi.extension",
            "sphinx.ext.autodoc",
            "sphinx.ext.napoleon",
            "sphinx.ext.linkcode",
            "sphinx.ext.autosummary",
            "sphinx_autodoc_typehints",
        ],
        "enhancement": [
            "sphinx_design",
            "sphinx_tabs.tabs",
            "sphinx_inline_tabs",
            "sphinx_togglebutton",
            "sphinx_copybutton",
            "sphinx_exec_directive",
            "sphinx_math_dollar",
            "sphinxemoji.sphinxemoji",
            "sphinx_prompt",
            "sphinx_substitution_extensions",
            "sphinx_removed_in",
        ],
        "diagrams": [
            "sphinxcontrib.mermaid",
            "sphinxcontrib.plantuml",
            "sphinxcontrib.blockdiag",
            "sphinxcontrib.seqdiag",
            "sphinxcontrib.images",
        ],
        "quality": [
            "sphinx.ext.doctest",
            "sphinx.ext.coverage",
            "sphinx.ext.todo",
            "sphinxcontrib.spelling",
        ],
        "external": [
            "sphinx.ext.intersphinx",
            "sphinxext.opengraph",
            "sphinx_sitemap",
            "sphinx_issues",
            "sphinx_contributors",
            "sphinxcontrib.youtube",
            "sphinxcontrib.openapi",
            "sphinxcontrib.httpdomain",
            "hoverxref.extension",
            "sphinx_needs",
        ],
        "content": [
            "myst_nb",
            "sphinx_gallery.gen_gallery",
            "sphinx_jinja2",
            "sphinx_external_toc",
            "sphinx_thebe",
            "sphinx_exercise",
            "sphinx_proof",
        ],
        "export": [
            "sphinx_pdf_generate",
            "sphinx_simplepdf",
            "sphinx_revealjs",
            "sphinx_multiversion",
            "notfound.extension",
            "sphinx_favicon",
            "sphinx_data_viewer",
            "sphinx_git",
        ],
    }


# Convenience aliases for backward compatibility
get_minimal_config = create_minimal_config
get_standard_config = create_standard_config
get_full_config = create_full_config
get_custom_config = create_custom_config
