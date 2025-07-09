# Haive Store Module

## Overview

The Haive Store module provides a powerful, serializable wrapper around LangGraph's native store implementations (`InMemoryStore`, `PostgresStore`, `AsyncPostgresStore`). It adds critical features for production use including connection sharing, embedding integration, and full serialization support while maintaining compatibility with the Haive agent framework.

## Key Features

- 🔄 **Full Async Support**: Native support for both synchronous and asynchronous operations
- 🔗 **Connection Sharing**: Intelligent connection pool management prevents resource exhaustion
- 📦 **Complete Serialization**: Store configurations can be pickled/unpickled for distributed systems
- 🔍 **Semantic Search**: Built-in integration with Haive's embedding system for vector search
- 🤖 **Agent Integration**: Seamless integration with Haive agents for persistent memory
- 🏗️ **Multiple Backends**: Support for in-memory, PostgreSQL sync, and PostgreSQL async stores
- 🔧 **Lifecycle Management**: Context managers for proper resource cleanup

## Installation

```bash
# Core dependencies
pip install langgraph psycopg[pool]

# For async PostgreSQL support
pip install asyncpg

# For embeddings (optional)
pip install langchain openai sentence-transformers
```

## Quick Start

### Basic Usage

```python
from haive.core.persistence.store import create_store, StoreType

# Create an in-memory store
store = create_store(StoreType.MEMORY)

# Store data
store.put(("agent", "memory"), "key1", {"fact": "The sky is blue"})

# Retrieve data
data = store.get(("agent", "memory"), "key1")
print(data)  # {"fact": "The sky is blue"}
```

### PostgreSQL with Semantic Search

```python
# Create PostgreSQL store with embeddings
store = create_store(
    StoreType.POSTGRES_SYNC,
    host="localhost",
    database="haive",
    user="haive_user",
    password="secure_password",
    embedding_provider="openai:text-embedding-3-small",
    embedding_dims=1536,
    connection_id="main_db"  # Enables connection sharing
)

# Store documents
store.put(("docs",), "doc1", {"content": "Machine learning is fascinating"})
store.put(("docs",), "doc2", {"content": "Deep learning uses neural networks"})

# Semantic search
results = store.search(
    ("docs",),
    query="What is AI?",
    limit=5
)
```

## Agent Integration 🤖

The store module is designed to work seamlessly with Haive agents, providing persistent memory across conversations and restarts.

### Configuring Store in Agent

```python
from haive.agents.base import Agent, AgentConfig
from typing import Dict, Any

class MyAgentConfig(AgentConfig):
    """Agent configuration with store support."""

    # Enable store
    add_store: bool = True

    # Store configuration
    store_config: Dict[str, Any] = {
        "type": "postgres_sync",
        "connection_params": {
            "host": "localhost",
            "port": 5432,
            "database": "agent_memory",
            "user": "agent_user",
            "password": "secure_password"
        },
        "embedding_provider": "openai:text-embedding-3-small",
        "embedding_dims": 1536,
        "connection_id": "agent_db",  # Shared across agents
        "namespace_prefix": "production"  # Optional prefix
    }

class MemoryAgent(Agent):
    """Agent with persistent memory."""

    def build_graph(self):
        from langgraph.graph import StateGraph, START, END

        graph = StateGraph(self.state_schema)

        # Add nodes that use the store
        graph.add_node("remember", self.remember_node)
        graph.add_node("recall", self.recall_node)
        graph.add_node("respond", self.respond_node)

        # Define flow
        graph.add_edge(START, "recall")
        graph.add_edge("recall", "respond")
        graph.add_edge("respond", "remember")
        graph.add_edge("remember", END)

        self.graph = graph

    def remember_node(self, state, config):
        """Store important information in persistent memory."""
        store = config.get("store")

        if store and state.get("important_info"):
            thread_id = config["configurable"]["thread_id"]
            namespace = ("agent", self.name, thread_id, "facts")

            # Store with timestamp
            import time
            key = f"fact_{int(time.time())}"
            store.put(
                namespace,
                key,
                {
                    "content": state["important_info"],
                    "context": state.get("context", ""),
                    "timestamp": time.time()
                }
            )

        return state

    def recall_node(self, state, config):
        """Retrieve relevant memories."""
        store = config.get("store")

        if store and state.get("query"):
            thread_id = config["configurable"]["thread_id"]
            namespace = ("agent", self.name, thread_id, "facts")

            # Semantic search for relevant memories
            memories = store.search(
                namespace,
                query=state["query"],
                limit=5
            )

            state["recalled_memories"] = [m.value for m in memories]

        return state
```

### Using Async Stores with Agents

```python
class AsyncMemoryAgent(Agent):
    """Agent using async PostgreSQL store."""

    def __init__(self, **kwargs):
        # Force async store type
        if "config" in kwargs and hasattr(kwargs["config"], "store_config"):
            kwargs["config"].store_config["type"] = "postgres_async"
        super().__init__(**kwargs)

    async def recall_node_async(self, state, config):
        """Async node for memory recall."""
        store_wrapper = getattr(self, "store_wrapper", None)

        if store_wrapper and state.get("query"):
            thread_id = config["configurable"]["thread_id"]
            namespace = ("agent", self.name, thread_id, "memories")

            # Async semantic search
            memories = await store_wrapper.asearch(
                namespace,
                query=state["query"],
                limit=10,
                filter={"type": "long_term"}
            )

            state["memories"] = memories

        return state
```

### Cross-Thread Memory Sharing

```python
def setup_shared_memory_agent():
    """Agent that can access memories across threads."""

    config = AgentConfig(
        name="shared_memory_agent",
        add_store=True,
        store_config={
            "type": "postgres_sync",
            "connection_params": {
                "host": "localhost",
                "database": "shared_memory"
            },
            "connection_id": "shared_pool",  # Critical for sharing!
            "embedding_provider": "openai:text-embedding-3-small"
        }
    )

    agent = Agent(config=config)

    # In nodes, access cross-thread memories
    def cross_thread_recall(state, config):
        store = config.get("store")
        user_id = config["configurable"].get("user_id")

        if store and user_id:
            # Search across all threads for this user
            namespace = ("users", user_id, "global_memory")

            memories = store.search(
                namespace,
                query=state.get("query", ""),
                limit=20
            )

            state["global_memories"] = memories

        return state

    return agent
```

## Configuration Options

### StoreConfig Schema

```python
from haive.core.persistence.store.types import StoreConfig, StoreType

config = StoreConfig(
    # Basic settings
    type=StoreType.POSTGRES_SYNC,  # or MEMORY, POSTGRES_ASYNC
    namespace_prefix="production",  # Optional prefix for all namespaces
    connection_id="main_db",       # ID for connection sharing

    # Connection parameters (PostgreSQL)
    connection_params={
        "host": "localhost",
        "port": 5432,
        "database": "haive",
        "user": "haive_user",
        "password": "password",
        "sslmode": "require",      # SSL mode
        "connect_timeout": 10,      # Connection timeout
        "application_name": "haive_agent"
    },

    # Embedding configuration (for semantic search)
    embedding_provider="openai:text-embedding-3-small",
    embedding_dims=1536,
    embedding_fields=["content", "summary"],  # Fields to embed

    # Connection pool settings
    pool_config={
        "min_size": 2,
        "max_size": 20,
        "max_idle": 300,  # seconds
        "max_lifetime": 3600  # seconds
    },

    # Behavior
    setup_on_init=True  # Auto-create tables
)
```

### Embedding Providers

The store module integrates with Haive's embedding system and supports:

- **OpenAI**: `"openai:text-embedding-3-small"`, `"openai:text-embedding-3-large"`
- **HuggingFace**: `"huggingface:sentence-transformers/all-MiniLM-L6-v2"`
- **Cohere**: `"cohere:embed-english-v3.0"`
- **Custom**: Any provider supported by Haive's embedding system

## Advanced Features

### Connection Sharing

Connection sharing prevents connection pool exhaustion when multiple stores connect to the same database:

```python
# These stores share the same connection pool
store1 = create_store(
    StoreType.POSTGRES_SYNC,
    connection_id="shared_db",
    host="localhost"
)

store2 = create_store(
    StoreType.POSTGRES_SYNC,
    connection_id="shared_db",  # Same ID = shared pool
    host="localhost"
)

# Different ID = different pool
store3 = create_store(
    StoreType.POSTGRES_SYNC,
    connection_id="other_db",
    host="localhost"
)
```

### Serialization Support

Store configurations are fully serializable:

```python
import pickle

# Create store
store = create_store(
    StoreType.POSTGRES_SYNC,
    host="localhost",
    connection_id="main"
)

# Serialize
serialized = pickle.dumps(store)

# Later, deserialize
restored_store = pickle.loads(serialized)
# Connection pools are automatically reused!
```

### Context Managers

For proper resource management:

```python
from haive.core.persistence.store import StoreFactory, StoreConfig

# Sync context manager
config = StoreConfig(type=StoreType.POSTGRES_SYNC)
with StoreFactory.create_with_lifecycle(config) as store:
    store.put(("temp",), "key", {"data": "value"})
    # Resources cleaned up automatically

# Async context manager
async def async_operation():
    config = StoreConfig(type=StoreType.POSTGRES_ASYNC)
    async with StoreFactory.create_async_with_lifecycle(config) as store:
        await store.aput(("temp",), "key", {"data": "value"})
        # Resources cleaned up automatically
```

### Namespace Patterns

Best practices for organizing data:

```python
# Agent memories
namespace = ("agent", agent_name, thread_id, "memories")

# User data
namespace = ("users", user_id, "preferences")

# Global knowledge
namespace = ("knowledge", "facts", category)

# Temporary data
namespace = ("temp", session_id, "working_memory")

# With prefix (automatically prepended)
store = create_store(
    StoreType.MEMORY,
    namespace_prefix="production"
)
store.put(("agent", "data"), "key", value)
# Actually stores at: ("production", "agent", "data")
```

## Performance Tips

1. **Use Connection Sharing**: Always set `connection_id` for PostgreSQL stores
2. **Batch Operations**: When possible, batch multiple operations
3. **Index Strategy**: Use embedding fields wisely - index only what you search
4. **Async When Possible**: Use async stores for better concurrency
5. **Connection Pool Sizing**: Size pools based on concurrent agent count

## Troubleshooting

### Common Issues

**Connection Pool Exhaustion**

```python
# Problem: Too many connections
# Solution: Use connection sharing
store = create_store(
    StoreType.POSTGRES_SYNC,
    connection_id="shared",  # Critical!
    pool_config={"max_size": 50}
)
```

**Embedding Errors**

```python
# Problem: Embedding provider not found
# Solution: Check provider string and dependencies
try:
    store = create_store(
        StoreType.POSTGRES_SYNC,
        embedding_provider="openai:text-embedding-3-small"
    )
except Exception as e:
    print(f"Embedding error: {e}")
    # Fallback to store without embeddings
    store = create_store(StoreType.POSTGRES_SYNC)
```

**Async Context Issues**

```python
# Problem: Using sync store in async context
# Solution: Use appropriate store type
async def agent_node(state, config):
    store_wrapper = getattr(self, "store_wrapper", None)
    if store_wrapper:
        # Use async methods
        await store_wrapper.aput(namespace, key, value)
        result = await store_wrapper.aget(namespace, key)
```

### Debug Logging

Enable debug logging to troubleshoot:

```python
import logging

# Enable store module logging
logging.getLogger("haive.core.persistence.store").setLevel(logging.DEBUG)

# See connection pool activity
logging.getLogger("haive.core.persistence.store.connection").setLevel(logging.DEBUG)
```

## Migration Guide

### From Raw LangGraph Stores

```python
# Before: Raw LangGraph
from langgraph.store.postgres import PostgresStore
from psycopg_pool import ConnectionPool

pool = ConnectionPool("postgresql://...")
store = PostgresStore(pool)

# After: Haive wrapper
from haive.core.persistence.store import create_store, StoreType

store = create_store(
    StoreType.POSTGRES_SYNC,
    host="localhost",
    database="haive"
)
```

### From Agent Memory Systems

```python
# Before: Custom memory in agent
class OldAgent:
    def __init__(self):
        self.memory = {}

    def remember(self, key, value):
        self.memory[key] = value

# After: Persistent store
class NewAgent(Agent):
    def remember_node(self, state, config):
        store = config.get("store")
        if store:
            namespace = ("agent", self.name, "memory")
            store.put(namespace, key, value)
```

## Contributing

The store module is part of the Haive framework. To contribute:

1. Follow the existing patterns for new store implementations
2. Ensure serialization support is maintained
3. Add appropriate tests
4. Update documentation

## License

Part of the Haive framework. See main LICENSE file.
