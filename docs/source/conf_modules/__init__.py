"""Modular Sphinx configuration system for Haive.

This package provides a modular approach to Sphinx configuration,
breaking down complex configurations into manageable, reusable components.
"""

from typing import Any, Dict, List, Optional


def create_full_config() -> Dict[str, Any]:
    """Create a full Sphinx configuration with all features enabled.

    Returns:
        Dictionary of all configuration values to be applied to conf.py
    """
    config = {}

    # Import all modules
    from .core import logging, paths, project
    from .extensions import (api_generation, core_sphinx, documentation,
                             enhancement, external, testing)
    from .processing import autoapi, markdown, notebooks
    from .quality import coverage, doctest, spelling
    from .themes import furo
    from .utilities import mock_imports, warnings

    # Apply configurations in order
    config.update(logging.get_config())
    config.update(warnings.get_config())
    config.update(paths.get_config())
    config.update(project.get_config())

    # Extensions
    config.update(core_sphinx.get_config())
    config.update(api_generation.get_config())
    config.update(documentation.get_config())
    config.update(testing.get_config())
    config.update(enhancement.get_config())
    config.update(external.get_config())

    # Processing
    config.update(markdown.get_config())
    config.update(notebooks.get_config())
    config.update(autoapi.get_config())

    # Quality
    config.update(doctest.get_config())
    config.update(coverage.get_config())
    config.update(spelling.get_config())

    # Theme
    config.update(furo.get_config())

    # Utilities
    config.update(mock_imports.get_config())

    return config


def create_minimal_config() -> Dict[str, Any]:
    """Create a minimal Sphinx configuration for simple projects.

    Returns:
        Dictionary of minimal configuration values
    """
    config = {}

    from .core import paths, project
    from .extensions import core_sphinx
    from .themes import furo

    config.update(paths.get_config(minimal=True))
    config.update(project.get_config())
    config.update(core_sphinx.get_config(minimal=True))
    config.update(furo.get_config(minimal=True))

    return config


def create_api_focused_config(packages: Optional[List[str]] = None) -> Dict[str, Any]:
    """Create configuration focused on API documentation.

    Args:
        packages: List of packages to document

    Returns:
        Dictionary of API-focused configuration
    """
    config = {}

    from .core import paths, project
    from .extensions import api_generation, core_sphinx
    from .processing import autoapi
    from .themes import furo

    config.update(paths.get_config())
    config.update(project.get_config())
    config.update(core_sphinx.get_config())
    config.update(api_generation.get_config())
    config.update(autoapi.get_config(packages=packages))
    config.update(furo.get_config())

    return config
