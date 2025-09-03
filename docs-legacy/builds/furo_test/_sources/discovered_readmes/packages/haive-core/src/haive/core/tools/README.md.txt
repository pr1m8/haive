# Haive Core Tools Module

## Overview

This module provides LangChain-compatible tools for Haive agents, enabling memory management, store operations, and other utility functions.

## Components

### Store Tools (`store_tools.py`)

Memory management tools that enable agents to store, search, retrieve, update, and delete memories using the Haive store infrastructure.

**Key Features:**

- LangChain `@tool` decorator pattern for AugLLMConfig compatibility
- Comprehensive memory operations (CRUD + search)
- Namespace support for memory isolation
- Structured JSON responses with error handling
- Compatible with all Haive store backends (PostgreSQL, Memory, etc.)

**Available Tools:**

- `store_memory` - Store new memories with categorization
- `search_memory` - Search for relevant memories by query
- `retrieve_memory` - Get specific memory by ID
- `update_memory` - Modify existing memories
- `delete_memory` - Remove memories

### Store Manager (`store_manager.py`)

Centralized memory management with namespace support and high-level API for memory operations.

**Key Features:**

- Namespace creation utilities (user, agent, session namespaces)
- Memory CRUD operations
- MemoryEntry data model with validation
- Backend-agnostic store operations

## Quick Start

```python
from haive.core.tools.store_manager import StoreManager
from haive.core.tools.store_tools import create_memory_tools_suite
from haive.core.persistence.store.factory import create_store
from haive.core.persistence.store.types import StoreType

# Create store and manager
store = create_store(store_type=StoreType.POSTGRES)
store_manager = StoreManager(store=store)

# Create all memory tools
tools = create_memory_tools_suite(store_manager)

# Use with AugLLMConfig
from haive.core.engine.aug_llm import AugLLMConfig
config = AugLLMConfig(tools=tools)
```

## Tool Integration Pattern

**Important:** All tools use the `@tool` decorator pattern for LangChain compatibility:

```python
@tool(tool_name, args_schema=InputSchema)
def tool_function(...) -> str:
    """Tool description for LLM"""
    # implementation
    return json.dumps(result)
```

This pattern ensures compatibility with AugLLMConfig and avoids LangChain validation issues.

## Error Handling

All tools return consistent JSON responses:

```json
// Success
{"success": true, "result": "...", "message": "Operation successful"}

// Error
{"success": false, "error": "Error details", "message": "Operation failed"}
```

## Namespace Usage

```python
# Create user-specific namespace
user_ns = store_manager.create_user_namespace("alice")

# Create tools with namespace
tools = create_memory_tools_suite(store_manager, namespace=user_ns)
```

## Testing

Run the comprehensive test suite:

```bash
poetry run pytest packages/haive-core/tests/tools/ -v
```

## Examples

See `packages/haive-core/examples/` for complete usage examples:

- `store_memory_agent.py` - Memory-enabled agent
- `simple_store_test.py` - Basic store operations

## Documentation

- **Store Memory System**: `/project_docs/STORE_MEMORY_SYSTEM.md`
- **Technical Fix Details**: `/project_docs/technical_fixes/LANGCHAIN_TOOL_INTEGRATION_FIX.md`

## Contributing

When adding new tools:

1. Use `@tool` decorator pattern
2. Include comprehensive input schema validation
3. Return structured JSON responses
4. Add comprehensive tests
5. Update this README
