# Entity Providers

Entity providers are specialized components that handle the discovery, registration, and management of specific entity types in the Haive registry system.

## Overview

Each entity type (agent, tool, engine, etc.) has its own provider that implements the discovery and registration logic specific to that entity type. Providers handle the unique requirements and conventions of their respective entity types, ensuring consistent registration and management.

## Provider Architecture

The provider system follows a plugin-like architecture:

- `EntityProvider`: Abstract base class defining the common interface
- Type-specific implementations:
  - `AgentProvider`: Discovers and registers agent components
  - `ToolProvider`: Discovers and registers tool components
  - `ToolkitProvider`: Discovers and registers toolkit components
  - `EngineProvider`: Discovers and registers engine components
  - `GameProvider`: Discovers and registers game components

## Core Functionality

Each provider implements:

1. **Discovery Logic**: Search for components of a specific type in the codebase
2. **Registration Logic**: Register discovered components in the registry system
3. **Metadata Extraction**: Extract metadata from discovered components
4. **Configuration Handling**: Register component configurations
5. **Dependency Management**: Track dependencies between components

## Implementing a Custom Provider

To implement a custom provider:

```python
from haive.dataflow.registry.providers.base import EntityProvider
from haive.dataflow.registry.models import EntityType

class CustomProvider(EntityProvider):
    def __init__(self):
        super().__init__(EntityType.CUSTOM)

    def discover(self, module_paths=None):
        # Custom discovery logic
        paths = module_paths or self.get_default_search_paths()
        discovered_ids = []

        # Implementation...

        return discovered_ids

    def get_default_search_paths(self):
        return [
            "haive.custom_components",
            "my_package.custom_components"
        ]
```

## Usage

Entity providers are typically used through the discovery functions in the registry module:

```python
from haive.dataflow.registry import discover_agents, discover_tools, discover_all

# Discover and register all agents
discovered_agents = discover_agents()
print(f"Discovered {len(discovered_agents)} agents")

# Discover all components
all_components = discover_all()
```

These functions internally instantiate the appropriate providers and call their discovery methods.
