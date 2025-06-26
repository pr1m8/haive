# Haive Database Module

Database integration for the Haive framework, providing persistence for the registry system.

## Overview

The database module provides connectivity and persistence for the Haive registry system. It primarily uses Supabase as the backend database, providing a scalable, managed solution for storing registry data.

## Key Components

### Supabase Integration

- `supabase.py`: Provides the Supabase client and connection management
- `get_supabase_client()`: Factory function to create a Supabase client
- Environment variable configuration for connection parameters

### Schema Management

- `schema.py`: Database schema definitions and migrations
- Table definitions for registry items, configurations, dependencies, etc.
- Schema initialization and upgrade functions

### Inspection Utilities

- `inspect_supabase.py`: Utilities for inspecting and debugging Supabase connections
- Connection testing and validation

## Configuration

The module uses the following environment variables for configuration:

- `SUPABASE_URL`: The URL of your Supabase instance
- `SUPABASE_KEY`: The API key for your Supabase instance
- `SUPABASE_SCHEMA`: The database schema to use (default: 'registry')

## Usage Examples

### Basic Supabase Connection

```python
from haive.dataflow.db.supabase import get_supabase_client

# Get a Supabase client
supabase = get_supabase_client()

# Query the registry items table
result = supabase.table('registry_items').select('*').execute()
items = result.data

print(f"Found {len(items)} registry items")
```

### Schema Management

```python
from haive.dataflow.db.schema import initialize_schema

# Initialize the database schema
initialize_schema(supabase)
```

## Error Handling

The module includes robust error handling to gracefully handle connection issues:

- Connection failures trigger fallback to in-memory storage
- Automatic retry mechanisms for transient errors
- Detailed logging for troubleshooting

## Security

Credentials are handled securely through:

- Environment variable loading
- Secrets management
- No hardcoded credentials in code
