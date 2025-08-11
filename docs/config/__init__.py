"""
Shared documentation configuration for Haive packages.

This module provides consistent Sphinx configuration across all packages
in the Haive monorepo, ensuring uniform documentation standards while
allowing for package-specific customizations.
"""

__version__ = "0.1.0"
__author__ = "Haive Team"

from .shared_config import get_base_config, discover_haive_packages

__all__ = ["get_base_config", "discover_haive_packages"]