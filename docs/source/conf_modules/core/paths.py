"""Path configuration for Sphinx documentation.

This module handles all path setup including:
- Working directory paths
- Package discovery
- sys.path management
- Extension paths
"""

from __future__ import annotations

import logging
from pathlib import Path
import sys
from typing import Any

logger = logging.getLogger(__name__)


def get_config(
    packages: list[str] | None = None,
    minimal: bool = False,
) -> dict[str, Any]:
    """Get path configuration for Sphinx.

    Args:
        packages: List of packages to add to path. If None, uses default list.
        minimal: If True, only adds essential paths

    Returns:
        Dictionary with path configuration and globals
    """
    config = {}

    # Get paths
    conf_dir = Path(__file__).parent.parent.parent.absolute()
    docs_dir = conf_dir.parent
    workspace_dir = docs_dir.parent

    # Store paths in config
    config["_conf_dir"] = conf_dir
    config["_docs_dir"] = docs_dir
    config["_workspace_dir"] = workspace_dir

    # Add workspace to Python path
    sys.path.insert(0, str(workspace_dir))

    # Add extensions directory if it exists
    extensions_dir = conf_dir / "_extensions"
    if extensions_dir.exists():
        sys.path.insert(0, str(extensions_dir))
        logger.info(f"Added custom extensions directory: {extensions_dir}")

    if minimal:
        return config

    # Default package list
    if packages is None:
        packages = [
            "haive-core",
            "haive-agents",
            "haive-tools",
            "haive-games",
            "haive-dataflow",
            "haive-mcp",
            # "haive-prebuilt",  # Excluded - contains generated content
        ]

    # Add package source paths
    packages_dir = workspace_dir / "packages"
    config["_packages_dir"] = packages_dir

    if packages_dir.exists():
        logger.info(f"Found packages directory: {packages_dir}")

        for package in packages:
            src_path = packages_dir / package / "src"
            if src_path.exists():
                sys.path.insert(0, str(src_path))
                logger.info(f"Added to sys.path: {src_path}")

                # Try to import the package
                if not minimal:
                    package_module = f"haive.{package.split('-')[1]}"
                    try:
                        __import__(package_module)
                        logger.info(f"Successfully imported {package_module}")
                    except Exception as e:
                        logger.warning(
                            f"Failed to import {package_module}: {e}")

    # Exclude patterns
    config["exclude_patterns"] = [
        "_build",
        "Thumbs.db",
        ".DS_Store",
        "**/__pycache__",
        "**/test_*.py",
        "**/tests/**",
        "**/.pytest_cache",
        "**/.ruff_cache",
        "**/node_modules",
        "**/.git",
    ]

    # Templates path
    config["templates_path"] = ["_templates"]

    # Static files
    config["html_static_path"] = ["_static"]

    return config


def get_package_paths(workspace_dir: Path) -> list[Path]:
    """Get all package source paths in the workspace.

    Args:
        workspace_dir: Root workspace directory

    Returns:
        List of package source paths
    """
    packages_dir = workspace_dir / "packages"
    paths = []

    if packages_dir.exists():
        for package_dir in packages_dir.iterdir():
            if package_dir.is_dir():
                src_path = package_dir / "src"
                if src_path.exists():
                    paths.append(src_path)

    return paths
