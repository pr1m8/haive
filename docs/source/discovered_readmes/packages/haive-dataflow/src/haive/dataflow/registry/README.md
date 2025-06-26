# Haive Registry Module

The core registry system for managing components in the Haive framework.

## Overview

The registry module provides the fundamental functionality for registering, querying, and managing various components in the Haive ecosystem. It serves as a central repository of information about agents, tools, engines, and other components.

## Directory Structure

```
registry/
├── __init__.py             # Package exports
├── core.py                 # Core registry functionality
├── models.py               # Pydantic models for registry items
├── serialization.py        # Serialization utilities
├── discovery.py            # Discovery mechanisms
├── providers/              # Entity type-specific providers
│   ├── __init__.py
│   ├── base.py             # Base provider class
│   ├── agent_provider.py
│   ├── tool_provider.py
│   ├── engine_provider.py
│   ├── toolkit_provider.py
│   └── game_provider.py
├── importers/              # Data importers
│   ├── __init__.py
│   └── litellm_importer.py # LiteLLM model importer
└── utils/
    ├── __init__.py
    └── logging.py          # Logging utilities
```

## Key Components

### Core Registry System

The `RegistrySystem` class provides the central functionality:

- Component registration and retrieval
- Configuration management
- Dependency tracking
- Optional database persistence via Supabase

### Data Models

- `RegistryItem`: Base model for all registry entries
- `Configuration`: Configuration data for registry items
- `GraphDefinition`: Graph structure definitions for components
- `Dependency`: Dependency relationships between components
- `EnvironmentVar`: Environment variable requirements

### Type Enumerations

- `EntityType`: Types of entities (AGENT, TOOL, ENGINE, etc.)
- `ConfigType`: Types of configurations (STATE_SCHEMA, INPUT_SCHEMA, etc.)
- `DependencyType`: Types of dependencies (REQUIRES, USES, EXTENDS)
- `ImportStatus`: Status of import operations

### Discovery Mechanisms

Functions for automatically discovering components:

- `discover_all()`: Discover all component types
- `discover_agents()`: Discover agent components
- `discover_tools()`: Discover tool components
- `discover_engines()`: Discover engine components
- `discover_games()`: Discover game components

### Serialization Utilities

Tools for handling complex object serialization:

- `SerializationRegistry`: Registry for custom serializers
- `serialize_object()`: Serialize objects to JSON-compatible format
- `deserialize_object()`: Restore objects from serialized format

### Providers

- `EntityProvider`: Base class for entity providers
- Type-specific providers for specialized handling of different entity types
- Custom discovery and registration logic for each entity type

## Usage Examples

### Basic Registry Operations

```python
from haive.dataflow import registry_system, EntityType

# Register a component
registry_system.register_entity(
    name="MyComponent",
    type=EntityType.TOOL,
    description="A useful tool",
    module_path="my_module.tools",
    class_name="MyTool"
)

# Add configuration
registry_system.add_configuration(
    registry_id="component-id",
    config_type=ConfigType.INPUT_SCHEMA,
    config_data={"type": "object", "properties": {...}}
)

# Query components
tools = registry_system.get_entities_by_type(EntityType.TOOL)
```

### Discovery Example

```python
from haive.dataflow.registry.discovery import discover_tools

# Discover and register all tools
discovered_tools = discover_tools()
print(f"Discovered {len(discovered_tools)} tools")
```

### Serialization Example

```python
from haive.dataflow.registry.serialization import serialize_object, deserialize_object

# Register a custom serializer
from haive.dataflow.registry.serialization import SerializationRegistry

SerializationRegistry.register(
    type_name="my_module.CustomClass",
    serializer=lambda obj: {"data": obj.to_dict()},
    deserializer=lambda data: CustomClass.from_dict(data["data"])
)

# Serialize a complex object
serialized = serialize_object(my_complex_object)

# Deserialize it later
restored = deserialize_object(serialized)
```
