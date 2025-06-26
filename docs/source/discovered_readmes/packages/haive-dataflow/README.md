# Haive Dataflow

A comprehensive registry and discovery system for the Haive framework that provides component management, serialization, and persistence.

## Overview

The `haive-dataflow` package provides a powerful registry system for discovering, registering, and managing various components in the Haive ecosystem, such as:

- Agents
- Tools and Toolkits
- Engines
- Games
- LLM Models and Providers
- Embedding Models and Providers

The package handles component discovery, serialization/deserialization, dependency management, and both in-memory and database persistence via Supabase.

## Installation

```bash
pip install haive-dataflow
```

For development:

```bash
poetry add haive-dataflow
```

## Key Features

- **Component Registry**: Centralized system for tracking and managing Haive components
- **Automatic Discovery**: Find and register components in the Haive ecosystem
- **Serialization**: Convert complex Python objects to/from storable formats
- **Dependency Management**: Track dependencies between components
- **Database Integration**: Store registry data in Supabase (optional)
- **API Endpoints**: Access registry data through RESTful API routes

## Usage Examples

### Basic Registry Usage

```python
from haive.dataflow import registry_system, EntityType

# Register a new component
registry_system.register_entity(
    name="TextClassifier",
    type=EntityType.AGENT,
    description="Classifies text into categories",
    module_path="haive.agents.classifiers",
    class_name="TextClassifierAgent"
)

# Query registered components
agents = registry_system.get_entities_by_type(EntityType.AGENT)
```

### Component Discovery

```python
from haive.dataflow import discover_agents, discover_tools, discover_all

# Discover and register all agents
discovered_agents = discover_agents()
print(f"Discovered {len(discovered_agents)} agents")

# Discover everything
all_components = discover_all()
```

### Serialization

```python
from haive.dataflow import serialize_object, deserialize_object

# Serialize a complex object
serialized = serialize_object(my_complex_object)

# Deserialize it later
restored_object = deserialize_object(serialized)
```

## Core Components

- `registry_system`: Singleton instance of the registry system
- `EntityType`: Enum of supported entity types (AGENT, TOOL, ENGINE, etc.)
- `ConfigType`: Enum of configuration types (STATE_SCHEMA, INPUT_SCHEMA, etc.)
- `DependencyType`: Enum of dependency relationships (REQUIRES, USES, EXTENDS)
- `RegistryItem`: Base model for registry entries
- `discover_*`: Functions for component discovery
- `SerializationRegistry`: Registry for custom serializers and deserializers

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT
