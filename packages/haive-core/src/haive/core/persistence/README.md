# Agent Persistence System

## Overview

The Haive agent persistence system provides a flexible and extensible framework for storing agent state, including checkpoints, messages, and metadata. This module supports multiple backend options, including in-memory storage, SQLite, and PostgreSQL databases.

## Key Components

The persistence system consists of these core components:

- **CheckpointerConfig**: Abstract base class defining the interface for all checkpointers
- **MemoryCheckpointerConfig**: In-memory implementation suitable for testing and development
- **SQLiteCheckpointerConfig**: SQLite-based implementation for local persistence
- **PostgresCheckpointerConfig**: PostgreSQL-based implementation for production use
- **Utility functions**: For handling state operations and compatibility with LangGraph

## Usage

### Creating a Checkpointer

The module provides factory functions for creating checkpointers:

```python
from src.haive.core.engine.agent.persistence import (
    create_memory_checkpointer,
    create_sqlite_checkpointer,
    create_postgres_checkpointer,
    create_checkpointer,
    CheckpointerType
)

# Create in-memory checkpointer
memory_config = create_memory_checkpointer()

# Create SQLite checkpointer
sqlite_config = create_sqlite_checkpointer(db_path="./checkpoints.db")

# Create PostgreSQL checkpointer
postgres_config = create_postgres_checkpointer(
    db_host="localhost",
    db_port=5432,
    db_name="postgres",
    db_user="postgres",
    db_pass="postgres"
)

# Or use the generic factory function
config = create_checkpointer(
    CheckpointerType.postgres,
    db_host="localhost",
    db_port=5432
)
```

### Using with Agent Configuration

The checkpointer configuration can be added to agent config:

```python
from src.haive.core.engine.agent.agent import AgentConfig
from src.haive.core.engine.agent.persistence import create_sqlite_checkpointer

agent_config = AgentConfig(
    name="my_agent",
    persistence=create_sqlite_checkpointer(db_path="./agent_state.db")
)
```

### Manually Working with Checkpointers

You can also use checkpointers directly:

```python
from src.haive.core.engine.agent.persistence import create_memory_checkpointer

# Create checkpointer config
config = create_memory_checkpointer()

# Get the actual checkpointer implementation
checkpointer = config.create_checkpointer()

# Register a thread
thread_id = "conversation-123"
config.register_thread(thread_id, metadata={"user": "user-456"})

# Create a checkpoint
checkpoint_config = {"configurable": {"thread_id": thread_id}}
data = {"messages": [...], "context": {...}}
updated_config = config.put_checkpoint(checkpoint_config, data)

# Retrieve a checkpoint
checkpoint_id = updated_config["configurable"]["checkpoint_id"]
retrieval_config = {"configurable": {"thread_id": thread_id, "checkpoint_id": checkpoint_id}}
result = config.get_checkpoint(retrieval_config)
```

## Setting Up PostgreSQL

To use the PostgreSQL backend:

1. Install dependencies: `pip install psycopg[binary] langgraph[postgres]`
2. Ensure PostgreSQL server is running
3. Create database and user with appropriate permissions
4. Configure the connection parameters

## Integrating with LangGraph

This system is designed to work with LangGraph checkpointers:

```python
from langgraph.checkpoint.base import BaseCheckpointSaver
from src.haive.core.engine.agent.persistence import create_sqlite_checkpointer
from src.haive.core.persistencehandlers import setup_checkpointer

# Create agent config with persistence
agent_config = AgentConfig(
    name="my_agent",
    persistence=create_sqlite_checkpointer(db_path="./agent_state.db")
)

# Get LangGraph-compatible checkpointer
checkpointer: BaseCheckpointSaver = setup_checkpointer(agent_config)

# Use with StateGraph
from langgraph.graph import StateGraph
graph = StateGraph(state_schema, checkpointer=checkpointer)
```

## Thread and Checkpoint Management

The system maintains both threads (conversations) and checkpoints:

- **Threads**: Represent conversations or interaction sessions
- **Checkpoints**: Specific states within a thread, typically created after each step

The `handlers.py` module provides utility functions for working with thread state:

```python
from src.haive.core.persistencehandlers import (
    prepare_merged_input,
    process_input,
    register_thread_if_needed
)

# Register a thread if needed
register_thread_if_needed(checkpointer, "thread-123")

# Process user input into appropriate format
processed_input = process_input("Hello agent", input_schema=MyInputSchema)

# Merge new input with previous state
merged_state = prepare_merged_input(
    "New message",
    previous_state=previous_checkpoint,
    state_schema=MyStateSchema
)
```

## Extending the System

The system is designed to be extensible. To add a new backend type:

1. Add a new type to `CheckpointerType` enum in `types.py`
2. Create a new implementation class that extends `CheckpointerConfig`
3. Implement the required methods: `create_checkpointer()`, `register_thread()`, etc.
4. Add a factory function in `__init__.py`
5. Update the `create_checkpointer()` function to handle the new type

## Error Handling

The persistence system is designed to be resilient:

- If PostgreSQL dependencies are missing, it falls back to other backends
- If database connection fails, it falls back to in-memory storage
- All operations are wrapped in exception handling to prevent crashes

## Compatibility

The system is designed to work with both older and newer versions of LangGraph by adapting to the available API methods:

- It supports the newer LangGraph checkpointer API that requires metadata and versioning
- It falls back to older APIs when needed
- It provides a consistent interface regardless of the underlying implementation
