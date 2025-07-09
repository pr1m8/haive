# src/haive/core/registry/manager.py

import logging
import os
from typing import Type

from haive.core.registry.base import AbstractRegistry
from haive.core.registry.memory import MemoryRegistry


class RegistryManager:
    """Manager for registry system access."""

    _instance = None
    _registry_types = {}  # Registry types

    @classmethod
    def register_registry_type(cls, name: str, registry_class: Type[AbstractRegistry]):
        """Register a registry implementation."""
        cls._registry_types[name] = registry_class

    @classmethod
    def get_instance(cls) -> "RegistryManager":
        """Get the singleton instance."""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        """Initialize the registry manager."""
        # Default to memory registry
        self._registry = MemoryRegistry()

    def get_registry(self) -> AbstractRegistry:
        """Get the current registry."""
        return self._registry

    def set_registry(self, registry: AbstractRegistry) -> None:
        """Set the current registry."""
        self._registry = registry

    def create_registry(self, registry_type: str = None, **kwargs) -> AbstractRegistry:
        """Create a registry of the specified type."""
        registry_type = registry_type or os.environ.get("HAIVE_REGISTRY_TYPE", "memory")

        if registry_type == "memory":
            return MemoryRegistry()

        registry_class = self._registry_types.get(registry_type)
        if registry_class:
            try:
                return registry_class(**kwargs)
            except Exception as e:
                logging.error(f"Failed to create registry of type {registry_type}: {e}")
                logging.warning("Falling back to memory registry")
                return MemoryRegistry()

        logging.warning(
            f"Unknown registry type: {registry_type}. Falling back to memory registry."
        )
        return MemoryRegistry()
