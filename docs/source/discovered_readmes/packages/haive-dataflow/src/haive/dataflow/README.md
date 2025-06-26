# Haive Dataflow

The core registry and discovery system for the Haive framework, providing component management, serialization, and persistence.

## Module Structure

```
haive/dataflow/
├── registry/                # Core registry system
│   ├── core.py              # Registry system implementation
│   ├── models.py            # Data models for registry items
│   ├── discovery.py         # Component discovery mechanisms
│   ├── serialization.py     # Object serialization utilities
│   ├── providers/           # Entity type-specific providers
│   └── importers/           # Data importers for external sources
├── db/                      # Database integration
│   ├── supabase.py          # Supabase client and operations
│   └── schema.py            # Database schema definitions
├── api/                     # API endpoints
│   ├── routes/              # Route definitions
│   └── middleware/          # API middleware components
├── auth/                    # Authentication utilities
│   └── supabase.py          # Supabase authentication
├── persistence/             # Data persistence
│   └── supabase_adapter.py  # Supabase adapter for persistence
└── providers/               # Provider implementations
    └── base.py              # Base provider classes
```

## Key Components

### Registry System

The central registry system for managing components in the Haive ecosystem:

- Component registration and retrieval
- Configuration management
- Dependency tracking
- Serialization of complex objects
- Automatic component discovery

### Database Integration

Database connectivity and persistence for the registry system:

- Supabase client and connection management
- Schema initialization and management
- Data persistence and retrieval

### API Layer

RESTful API endpoints for accessing registry data:

- Component listing and retrieval
- Configuration management
- Discovery operations

## Core Modules

### Registry Module

The registry module (`registry/`) is the heart of the dataflow system, providing:

- Entity registration and management
- Configuration storage and retrieval
- Dependency tracking
- Component discovery
- Object serialization and deserialization

### DB Module

The database module (`db/`) handles persistence and storage:

- Supabase client configuration
- Table operations
- Schema management
- Data migration

### Providers Module

The providers module (`providers/`) implements entity-specific logic:

- Entity discovery
- Registration logic
- Metadata extraction
- Type-specific operations

## Usage Examples

### Registry Operations

```python
from haive.dataflow import registry_system, EntityType

# Register a component
entity_id = registry_system.register_entity(
    name="TextAnalyzer",
    type=EntityType.TOOL,
    description="Analyzes text content",
    module_path="haive.tools.analyzers",
    class_name="TextAnalyzerTool"
)

# Query for components
tools = registry_system.get_entities_by_type(EntityType.TOOL)
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

### Database Operations

```python
from haive.dataflow.db.supabase import get_supabase_client

# Get a Supabase client
supabase = get_supabase_client()

# Query the registry items table
result = supabase.table('registry_items').select('*').execute()
```
