# Haive Registry System - Modular Structure

## Directory Structure
```
src/haive/dataflow/
├── db/
│   ├── __init__.py
│   ├── supabase.py             # Your existing Supabase client
│   └── schema.py               # Database schema definitions/migrations
├── registry/
│   ├── __init__.py             # Package exports
│   ├── core.py                 # Core registry functionality
│   ├── models.py               # Pydantic models for registry items
│   ├── serialization.py        # Serialization utilities
│   ├── discovery.py            # Discovery mechanisms
│   ├── providers/              # Entity type-specific providers
│   │   ├── __init__.py
│   │   ├── base.py             # Base provider class
│   │   ├── agent_provider.py
│   │   ├── tool_provider.py
│   │   ├── engine_provider.py
│   │   ├── toolkit_provider.py
│   │   └── game_provider.py
│   ├── importers/              # Data importers
│   │   ├── __init__.py
│   │   └── litellm_importer.py # LiteLLM model importer
│   └── utils/
│       ├── __init__.py
│       └── logging.py          # Logging utilities
└── bin/
    └── registry_cli.py         # Command-line interface (improved version)
```

## Logging Structure
```
logs/
└── registry/
    ├── discovery/              # Logs for component discovery
    ├── import/                 # Logs for data imports
    └── operations/             # Logs for registry operations
```

## Key Components

### Models
- `EntityType` - Enum for entity types
- `RegistryItem` - Base class for registry items
- `ConfigurationType` - Enum for configuration types
- `Configuration` - Class for configurations
- `DependencyType` - Enum for dependency types
- `Dependency` - Class for dependencies

### Core Registry
- `RegistrySystem` - Main registry system class
- Entity registration methods
- Serialization and deserialization
- Database interactions

### Providers
- `EntityProvider` - Base class for entity providers
- Type-specific providers for specialized handling
- Discovery mechanisms

### CLI
- Improved CLI with better formatting and options
- Support for all registry operations