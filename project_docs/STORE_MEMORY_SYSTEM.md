# Haive Store Memory System Documentation

## Overview

The Haive Store Memory System provides a comprehensive memory management solution for AI agents, similar to LangMem but built on our flexible store infrastructure. It enables agents to store, retrieve, search, and manage memories across conversations and sessions.

## Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Agent Tools   │────│  StoreManager    │────│ Store Wrappers  │
│  (LangChain)    │    │   (Memory API)   │    │  (PostgreSQL,   │
│                 │    │                  │    │   Memory, etc.) │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

### Core Components

1. **StoreManager**: Centralized memory management with namespace support
2. **Store Tools**: LangChain-compatible tools for agent integration
3. **Memory Entry**: Structured memory data model
4. **Store Wrappers**: Backend storage implementations

## Quick Start

### Basic Usage

```python
from haive.agents.simple import SimpleAgent
from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.persistence.store.factory import create_store
from haive.core.persistence.store.types import StoreType
from haive.core.tools.store_manager import StoreManager
from haive.core.tools.store_tools import create_memory_tools_suite

# Create store and manager
store = create_store(store_type=StoreType.POSTGRES)
store_manager = StoreManager(
    store=store,
    default_namespace=("haive", "users", "alice", "memories")
)

# Create memory tools
memory_tools = create_memory_tools_suite(store_manager)

# Create agent with memory tools
config = AugLLMConfig(tools=memory_tools)
agent = SimpleAgent(name="memory_agent", engine=config)

# Use the agent
response = await agent.arun("Remember that I love hiking and Thai food")
```

### Memory Tools Available

1. **store_memory**: Store new memories with categorization
2. **search_memory**: Search for relevant memories by query
3. **retrieve_memory**: Get specific memory by ID
4. **update_memory**: Modify existing memories
5. **delete_memory**: Remove memories (use with caution)

## Memory Entry Schema

```python
class MemoryEntry:
    id: str                           # Unique identifier
    content: str                      # Memory content
    category: str = "general"         # Category (user_preference, fact, event, etc.)
    importance: float = 0.5           # Importance score (0.0-1.0)
    tags: List[str] = []              # Optional tags for categorization
    metadata: Dict[str, Any] = {}     # Additional metadata
    created_at: datetime              # Creation timestamp
    updated_at: datetime              # Last update timestamp
```

## Namespace Management

Namespaces provide hierarchical organization and isolation of memories:

```python
# User-specific memories
user_namespace = store_manager.create_user_namespace("alice")
# ("haive", "users", "alice", "memories")

# Agent-specific memories
agent_namespace = store_manager.create_agent_namespace("assistant", "alice")
# ("haive", "users", "alice", "agents", "assistant", "memories")

# Session-specific memories
session_namespace = store_manager.create_session_namespace(
    session_id="session_123",
    agent_id="assistant", 
    user_id="alice"
)
# ("haive", "users", "alice", "agents", "assistant", "sessions", "session_123")
```

## Tool Integration Guide

### Individual Tool Creation

```python
from haive.core.tools.store_tools import (
    create_store_memory_tool,
    create_search_memory_tool,
    create_retrieve_memory_tool,
    create_update_memory_tool,
    create_delete_memory_tool
)

# Create individual tools
store_tool = create_store_memory_tool(store_manager)
search_tool = create_search_memory_tool(store_manager)

# With custom namespace
namespace = ("custom", "namespace")
store_tool = create_store_memory_tool(store_manager, namespace=namespace)
```

### Complete Tool Suite

```python
# All tools
all_tools = create_memory_tools_suite(store_manager)

# Subset of tools
essential_tools = create_memory_tools_suite(
    store_manager, 
    include_tools=["store", "search", "retrieve"]
)
```

## Memory Categories

Recommended categories for organizing memories:

- **user_preference**: User likes, dislikes, preferences
- **user_profile**: Basic user information (name, role, etc.)
- **fact**: Factual information
- **event**: Scheduled events, meetings, appointments
- **conversation**: Important conversation history
- **context**: Session or task context
- **general**: Default category for miscellaneous memories

## Best Practices

### Memory Storage

```python
# Good: Descriptive and categorized
store_manager.store_memory(
    content="Alice prefers Thai food over Italian",
    category="user_preference",
    importance=0.8,
    tags=["food", "cuisine"],
    metadata={"confidence": 0.9, "source": "direct_statement"}
)

# Avoid: Vague or uncategorized
store_manager.store_memory(
    content="Alice likes something",
    category="general"  # Too vague
)
```

### Search Strategies

```python
# Search with filters
memories = store_manager.search_memories(
    query="food preferences",
    category="user_preference",
    min_importance=0.7,
    tags=["food"],
    limit=10
)

# Broad search
memories = store_manager.search_memories(
    query="Alice",
    limit=20
)
```

### Importance Scoring

- **0.9-1.0**: Critical information (user identity, core preferences)
- **0.7-0.8**: Important information (key facts, preferences)
- **0.5-0.6**: Useful information (context, secondary facts)
- **0.3-0.4**: Background information
- **0.0-0.2**: Temporary or low-value information

## Error Handling

All tools return JSON responses with consistent error handling:

```json
// Success response
{
    "success": true,
    "memory_id": "mem_123",
    "message": "Successfully stored memory with ID: mem_123"
}

// Error response
{
    "success": false,
    "error": "Memory not found",
    "message": "Memory with ID mem_456 not found"
}
```

## Performance Considerations

### Memory Store Selection

- **MemoryStore**: Fast, temporary storage for testing/development
- **PostgresStore**: Persistent, production-ready with semantic search capabilities
- Choose based on persistence needs and scale requirements

### Search Optimization

- Use specific categories and tags for faster filtering
- Limit search results appropriately (default: 10, max: 50)
- Consider importance thresholds for relevance filtering

## Troubleshooting

### Common Issues

#### 1. Tool Integration Errors

**Problem**: `'Tool' object has no attribute 'get'` when creating AugLLMConfig

**Solution**: Use the `@tool` decorator pattern (already implemented in our tools)

```python
# ✅ Correct (our implementation)
@tool(tool_name, args_schema=StoreMemoryInput)
def store_memory_func(...):
    # implementation

# ❌ Incorrect (causes LangChain validation errors)
Tool(name=tool_name, func=store_memory_func, ...)
```

#### 2. Namespace Conflicts

**Problem**: Memories from different users/sessions mixing

**Solution**: Use proper namespace isolation

```python
# Create user-specific namespaces
user_ns = store_manager.create_user_namespace("user_id")
tools = create_memory_tools_suite(store_manager, namespace=user_ns)
```

#### 3. Search Returns No Results

**Problem**: Search queries not finding relevant memories

**Solutions**:
- Check if backend supports semantic search
- Verify memory categories and tags
- Try broader queries without filters
- Check memory actually exists with `retrieve_memory`

### Debugging

Enable debug logging to troubleshoot issues:

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Store manager operations will log debug information
logger = logging.getLogger("haive.core.tools.store_manager")
logger.setLevel(logging.DEBUG)
```

## Migration from LangMem

The Haive Store Memory System is designed as a drop-in replacement for LangMem:

### LangMem Compatibility

```python
# LangMem style (alias functions provided)
manage_tool = create_manage_memory_tool(store_manager)  # alias for store_memory
search_tool = create_search_memory_tool_alias(store_manager)
```

### Key Differences

1. **Namespace Support**: Hierarchical memory organization
2. **Backend Flexibility**: Multiple store implementations
3. **Enhanced Metadata**: Rich memory annotations
4. **Better Error Handling**: Structured JSON responses
5. **Category System**: Organized memory classification

## Examples

### Simple Memory Agent

See `packages/haive-core/examples/store_memory_agent.py` for a complete working example.

### Custom Store Implementation

```python
# Using specific store type
postgres_store = create_store(
    store_type=StoreType.POSTGRES,
    connection_string="postgresql://user:pass@localhost/db"
)

memory_store = create_store(store_type=StoreType.MEMORY)
```

### Advanced Tool Configuration

```python
# Agent-specific tools with custom namespace
agent_namespace = ("company", "department", "agent_v1")
agent_tools = create_memory_tools_suite(
    store_manager,
    namespace=agent_namespace,
    include_tools=["store", "search", "retrieve"]  # Exclude delete for safety
)
```

## API Reference

### StoreManager Methods

- `store_memory(content, category, importance, tags, metadata, namespace) -> str`
- `search_memories(query, category, min_importance, tags, limit, namespace) -> List[MemoryEntry]`
- `retrieve_memory(memory_id, namespace) -> Optional[MemoryEntry]`
- `update_memory(memory_id, content, category, importance, tags, metadata, namespace) -> bool`
- `delete_memory(memory_id, namespace) -> bool`

### Tool Functions

- `create_store_memory_tool(store_manager, namespace, tool_name) -> Tool`
- `create_search_memory_tool(store_manager, namespace, tool_name) -> Tool`
- `create_retrieve_memory_tool(store_manager, namespace, tool_name) -> Tool`
- `create_update_memory_tool(store_manager, namespace, tool_name) -> Tool`
- `create_delete_memory_tool(store_manager, namespace, tool_name) -> Tool`
- `create_memory_tools_suite(store_manager, namespace, include_tools) -> List[Tool]`

## Contributing

When extending the memory system:

1. Maintain backward compatibility with existing tools
2. Add comprehensive tests for new functionality
3. Update documentation with examples
4. Follow the established error handling patterns
5. Use proper typing throughout

## Support

For issues or questions:

1. Check this documentation first
2. Review the test files for usage examples
3. Enable debug logging for troubleshooting
4. Check the store wrapper implementations for backend-specific issues