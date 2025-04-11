"""
Haive Registry System

This package provides a comprehensive registry system for Haive components,
enabling discovery, registration, and management of various components like
agents, tools, engines, and more.
"""

from src.haive.dataflow.registry.models import (
    EntityType,
    ConfigType,
    DependencyType,
    ImportStatus,
    RegistryItem,
    Configuration,
    GraphDefinition,
    Dependency,
    EnvironmentVar,
    ImportLogItem
)

from src.haive.dataflow.registry.core import registry_system

# Import discovery functions
from src.haive.dataflow.registry.discovery import (
    discover_all,
    discover_agents,
    discover_tools,
    discover_toolkits,
    discover_engines,
    discover_games
)

# Import serialization utilities
from src.haive.dataflow.registry.serialization import (
    serialize_object,
    deserialize_object,
    SerializationRegistry
)

# Export for convenient imports
__all__ = [
    # Core registry system
    'registry_system',
    
    # Models
    'EntityType',
    'ConfigType',
    'DependencyType',
    'ImportStatus',
    'RegistryItem',
    'Configuration',
    'GraphDefinition',
    'Dependency',
    'EnvironmentVar',
    'ImportLogItem',
    
    # Discovery
    'discover_all',
    'discover_agents',
    'discover_tools',
    'discover_toolkits',
    'discover_engines',
    'discover_games',
    
    # Serialization
    'serialize_object',
    'deserialize_object',
    'SerializationRegistry'
]