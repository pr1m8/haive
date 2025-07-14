# Haive Core - Persistence Documentation

**Package**: haive-core  
**Component**: persistence  
**Last Updated**: 2025-01-14

## Overview

This directory contains documentation for Haive's persistence system, including checkpointers, stores, and database integrations.

## Components

### Store System
- **PostgreSQL Store**: Production-ready store with connection pooling support
- **Memory Store**: In-memory store for development and testing  
- **Store Factory**: Unified creation and fallback mechanism

### Checkpointer System  
- **PostgreSQL Checkpointer**: Persistent conversation state
- **Memory Checkpointer**: In-memory conversation state
- **Configuration Management**: Unified config system

## Documentation Files

### Implementation Guides
- **[POSTGRES_STORE_IMPLEMENTATION_SUCCESS.md](POSTGRES_STORE_IMPLEMENTATION_SUCCESS.md)** - Complete PostgreSQL store implementation with prepared statement fix

### Test Documentation
- **Test Location**: `/packages/haive-core/tests/persistence/store/`
- **Test Coverage**: PostgreSQL store, factory, fallback mechanisms
- **Integration Tests**: Agent persistence and store integration

## Quick Reference

### Store Creation
```python
from haive.core.persistence.store.factory import create_store
from haive.core.persistence.store.types import StoreType

# PostgreSQL store (with automatic fallback)
store = create_store(
    store_type=StoreType.POSTGRES_SYNC,
    connection_string="postgresql://..."
)

# Memory store
store = create_store(store_type=StoreType.MEMORY)
```

### Agent Persistence
```python
from haive.agents.simple import SimpleAgent
from haive.core.persistence.postgres_config import PostgresCheckpointerConfig

# Agent with PostgreSQL persistence + store
agent = SimpleAgent(
    name="persistent_agent",
    persistence=PostgresCheckpointerConfig(
        connection_string="postgresql://..."
    ),
    add_store=True
)
```

## Known Issues (Resolved)

- ✅ **PostgreSQL Prepared Statement Conflicts** (2025-01-14)
  - Issue: `prepared statement '_pg3_X' already exists` with connection pooling
  - Solution: Disable pipeline mode + clear existing statements + `prepare_threshold=None`
  - Status: Production ready

## Testing

### Run Store Tests
```bash
# All store tests
poetry run pytest packages/haive-core/tests/persistence/store/ -v

# PostgreSQL specific (requires POSTGRES_CONNECTION_STRING env var)
poetry run pytest packages/haive-core/tests/persistence/store/test_postgres_store.py -v

# Factory tests (no external dependencies)
poetry run pytest packages/haive-core/tests/persistence/store/test_store_factory.py -v
```

### Test Configuration
- **Environment Variables**: `POSTGRES_CONNECTION_STRING` for PostgreSQL tests
- **Test Isolation**: Each test uses unique namespaces
- **Real Components**: No mocks, actual PostgreSQL connections tested

## File Locations

### Source Code
```
packages/haive-core/src/haive/core/persistence/
├── store/
│   ├── postgres.py              # PostgreSQL store implementation
│   ├── factory.py               # Store factory with fallback
│   ├── base.py                  # Base store wrapper
│   └── types.py                 # Store configuration types
├── postgres_config.py           # PostgreSQL checkpointer config  
└── memory.py                    # Memory persistence config
```

### Tests
```
packages/haive-core/tests/persistence/
├── store/
│   ├── test_postgres_store.py   # PostgreSQL store tests
│   ├── test_store_factory.py    # Factory tests
│   └── conftest.py              # Test configuration
└── ...                          # Other persistence tests
```

## Production Deployment

### Supported Databases
- **PostgreSQL**: Direct connections, connection pools, Supabase, AWS RDS
- **Memory**: Development and testing environments

### Connection Pooling  
- ✅ **pgBouncer** (transaction mode): Fully supported
- ✅ **Supavisor**: Supabase connection pooling supported
- ✅ **AWS RDS Proxy**: Compatible
- ✅ **Direct Connections**: Full feature support

### Configuration Best Practices
```python
# Production PostgreSQL config
PostgresCheckpointerConfig(
    connection_string="postgresql://user:pass@host:port/db",
    prepare_threshold=None,      # Automatically set
    auto_commit=True,           # Recommended for pooling
    mode=CheckpointerMode.ASYNC  # For high-throughput apps
)
```

---

**Status**: Production ready with comprehensive test coverage and fallback mechanisms.