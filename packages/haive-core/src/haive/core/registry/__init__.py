# src/haive/core/registry/__init__.py

from haive.core.registry.base import AbstractRegistry
from haive.core.registry.manager import RegistryManager
from haive.core.registry.memory import MemoryRegistry

# Initialize registry types
RegistryManager.register_registry_type("memory", MemoryRegistry)

# Export primary classes
__all__ = ["AbstractRegistry", "MemoryRegistry", "RegistryManager"]
