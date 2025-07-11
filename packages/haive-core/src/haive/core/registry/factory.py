# src/haive/core/registry/factory.py

import logging
import os

from haive.core.registry.base import AbstractRegistry
from haive.core.registry.memory import MemoryRegistry


class RegistryFactory:
    """Factory for creating registry instances."""

    registry_types = {}  # mapping of registry types to classes

    @classmethod
    def register_registry_type(cls, name: str, registry_class: type[AbstractRegistry]):
        """Register a registry implementation."""
        cls.registry_types[name] = registry_class

    @classmethod
    def create(cls, registry_type: str | None = None, **kwargs) -> AbstractRegistry:
        """Create a registry of the specified type."""
        # Default to environment variable or memory
        registry_type = registry_type or os.environ.get("HAIVE_REGISTRY_TYPE", "memory")

        if registry_type == "memory":
            return MemoryRegistry()

        registry_class = cls.registry_types.get(registry_type)
        if registry_class:
            try:
                return registry_class(**kwargs)
            except Exception as e:
                logging.exception(
                    f"Failed to create registry of type {registry_type}: {e}"
                )
                logging.warning("Falling back to memory registry")
                return MemoryRegistry()

        logging.warning(
            f"Unknown registry type: {registry_type}. Falling back to memory registry."
        )
        return MemoryRegistry()
