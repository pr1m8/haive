"""Extension Manager for Sphinx Documentation.

This module provides a clean, modular approach to managing Sphinx extensions
with automatic dependency checking, configuration loading, and conflict resolution.
"""

import importlib
import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Set

logger = logging.getLogger(__name__)


@dataclass
class ExtensionSpec:
    """Specification for a Sphinx extension."""

    # Core identification
    name: str  # Extension name for Sphinx
    package: str  # PyPI package name
    module_check: str  # Import name to verify availability

    # Metadata
    description: str = ""  # What this extension does
    category: str = "misc"  # Category for organization
    priority: int = 100  # Load priority (lower = earlier)

    # Dependencies and conflicts
    requires: List[str] = field(default_factory=list)  # Required extensions
    conflicts: List[str] = field(default_factory=list)  # Conflicting extensions

    # Configuration
    config_func: Optional[Callable] = None  # Function to apply configuration
    config_vars: Dict[str, Any] = field(default_factory=dict)  # Config variables

    # Conditional loading
    enabled_by_default: bool = True  # Whether to load by default
    condition_func: Optional[Callable] = None  # Custom condition check


class ExtensionManager:
    """Manages Sphinx extensions with dependency resolution and configuration."""

    def __init__(self):
        self.extensions: Dict[str, ExtensionSpec] = {}
        self.loaded_extensions: Set[str] = set()
        self.failed_extensions: Dict[str, str] = {}  # name -> error
        self.config_vars: Dict[str, Any] = {}

    def register(self, spec: ExtensionSpec) -> None:
        """Register an extension specification."""
        self.extensions[spec.name] = spec

    def bulk_register(self, specs: List[ExtensionSpec]) -> None:
        """Register multiple extension specifications."""
        for spec in specs:
            self.register(spec)

    def is_available(self, spec: ExtensionSpec) -> bool:
        """Check if an extension is available for loading."""
        try:
            importlib.import_module(spec.module_check)
            return True
        except ImportError as e:
            logger.debug(f"Extension {spec.name} not available: {e}")
            return False

    def check_condition(self, spec: ExtensionSpec) -> bool:
        """Check if extension's custom condition is met."""
        if spec.condition_func is None:
            return True
        try:
            return spec.condition_func()
        except Exception as e:
            logger.warning(f"Condition check failed for {spec.name}: {e}")
            return False

    def resolve_dependencies(self, requested: Set[str]) -> List[str]:
        """Resolve extension dependencies and return load order."""
        resolved = []
        visited = set()
        visiting = set()

        def visit(name: str) -> None:
            if name in visiting:
                raise ValueError(f"Circular dependency detected involving {name}")
            if name in visited:
                return

            if name not in self.extensions:
                logger.warning(f"Unknown extension referenced: {name}")
                return

            spec = self.extensions[name]
            visiting.add(name)

            # Visit dependencies first
            for dep in spec.requires:
                if dep in requested:  # Only resolve if actually requested
                    visit(dep)

            visiting.remove(name)
            visited.add(name)

            if name in requested:
                resolved.append(name)

        # Sort by priority first, then resolve dependencies
        sorted_requested = sorted(
            requested,
            key=lambda name: (
                self.extensions[name].priority if name in self.extensions else 999
            ),
        )

        for name in sorted_requested:
            visit(name)

        return resolved

    def get_extensions_by_category(self, category: str) -> List[ExtensionSpec]:
        """Get all extensions in a specific category."""
        return [spec for spec in self.extensions.values() if spec.category == category]

    def load_extensions(
        self,
        categories: Optional[List[str]] = None,
        specific: Optional[List[str]] = None,
        exclude: Optional[List[str]] = None,
    ) -> tuple[List[str], Dict[str, Any]]:
        """Load extensions based on criteria.

        Args:
            categories: Extension categories to load
            specific: Specific extensions to load
            exclude: Extensions to exclude

        Returns:
            Tuple of (extension_names, config_variables)
        """
        # Determine which extensions to load
        requested = set()

        if specific:
            requested.update(specific)
        elif categories:
            for category in categories:
                requested.update(
                    spec.name
                    for spec in self.get_extensions_by_category(category)
                    if spec.enabled_by_default
                )
        else:
            # Load all enabled by default
            requested.update(
                spec.name
                for spec in self.extensions.values()
                if spec.enabled_by_default
            )

        # Remove excluded
        if exclude:
            requested -= set(exclude)

        # Filter by availability and conditions
        available_requested = set()
        for name in requested:
            if name not in self.extensions:
                logger.warning(f"Unknown extension: {name}")
                continue

            spec = self.extensions[name]

            if not self.is_available(spec):
                self.failed_extensions[name] = "Package not installed"
                continue

            if not self.check_condition(spec):
                self.failed_extensions[name] = "Condition not met"
                continue

            available_requested.add(name)

        # Resolve dependencies and get load order
        try:
            load_order = self.resolve_dependencies(available_requested)
        except ValueError as e:
            logger.error(f"Dependency resolution failed: {e}")
            load_order = list(available_requested)  # Fallback to unsorted

        # Collect configuration
        config_vars = {}
        for name in load_order:
            spec = self.extensions[name]

            # Add extension-specific config vars
            config_vars.update(spec.config_vars)

            # Apply configuration function if present
            if spec.config_func:
                try:
                    additional_config = spec.config_func() or {}
                    config_vars.update(additional_config)
                except Exception as e:
                    logger.error(f"Configuration function failed for {name}: {e}")

            self.loaded_extensions.add(name)

        self.config_vars.update(config_vars)
        return load_order, config_vars

    def get_status_report(self) -> Dict[str, Any]:
        """Get status report of extension loading."""
        return {
            "total_registered": len(self.extensions),
            "loaded": len(self.loaded_extensions),
            "failed": len(self.failed_extensions),
            "loaded_extensions": sorted(self.loaded_extensions),
            "failed_extensions": self.failed_extensions,
            "categories": {
                category: len(self.get_extensions_by_category(category))
                for category in set(spec.category for spec in self.extensions.values())
            },
        }


def create_extension_spec(
    name: str, package: str = None, module_check: str = None, **kwargs
) -> ExtensionSpec:
    """Helper to create ExtensionSpec with sensible defaults."""
    if package is None:
        package = name.replace(".", "-").replace("_", "-")

    if module_check is None:
        module_check = name.split(".")[0]

    return ExtensionSpec(
        name=name, package=package, module_check=module_check, **kwargs
    )
