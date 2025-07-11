# Supabase Persistence System Guide

## Overview

The Haive framework uses Supabase PostgreSQL as its persistence backend for agent state management, conversation history, and checkpoint storage. This document explains how the system works, particularly around thread identification, naming conventions, and data organization.

## Core File Locations

### Main Persistence Files

- **Base Agent**: `/packages/haive-agents/src/haive/agents/base/agent.py`
  - Inherits from `PersistenceMixin` (line 48)
  - Calls `_setup_persistence_from_config()` during initialization (line 278)

- **Persistence Mixin**: `/packages/haive-agents/src/haive/agents/base/mixins/persistence_mixin.py`
  - Contains all persistence logic and Supabase integration
  - Thread ID generation logic (lines 375-414)
  - Default persistence setup with Supabase connection (lines 79-182)

- **Persistence Handlers**: `/packages/haive-core/src/haive/core/persistence/handlers.py`
  - High-level persistence utilities
  - Checkpointer setup functions (lines 36-159)
  - Thread registration logic (lines 656-731)

- **PostgreSQL Config**: `/packages/haive-core/src/haive/core/persistence/postgres_config.py`
  - PostgreSQL-specific configuration and connection management
  - Checkpointer creation methods (lines 236-599)

- **Environment Config**: `/.env`
  - Contains Supabase connection strings and credentials
  - Main connection string: `POSTGRES_CONNECTION_STRING` (line 393)

## Database Connection

### Environment Configuration

```bash
# From /.env line 393
POSTGRES_CONNECTION_STRING=postgresql://postgres.zkssazqhwcetsnbiuqik:[REDACTED]@aws-0-us-east-1.pooler.supabase.com:6543/postgres
```

### Connection Details

- **Host**: `aws-0-us-east-1.pooler.supabase.com`
- **Port**: `6543` (Supabase connection pooler)
- **Database**: `postgres`
- **Project ID**: `zkssazqhwcetsnbiuqik`
- **SSL**: Automatically handled
- **Pool Size**: Min 1, Max 2 connections per agent

## Execution Flow: How Persistence Works

### 1. Agent Initialization Flow

```
Agent.__init__()
├── [agent.py:261] complete_agent_setup() validator
├── [agent.py:272] setup_agent() - subclass hook
├── [agent.py:275] _setup_schemas() - generate schemas
├── [agent.py:278] _setup_persistence_from_config() - setup persistence
└── [agent.py:281] _build_initial_graph() - build workflow
```

### 2. Persistence Setup Flow

```
_setup_persistence_from_config() [persistence_mixin.py:26]
├── [persistence_mixin.py:34] _setup_default_persistence() - if no config
│   ├── [persistence_mixin.py:117] Check POSTGRES_CONNECTION_STRING env var
│   ├── [persistence_mixin.py:125] Create PostgresCheckpointerConfig
│   └── [persistence_mixin.py:137] Configure unique app name per agent
├── [persistence_mixin.py:38] _setup_checkpointer_from_fields()
│   ├── [persistence_mixin.py:192] Call handlers.setup_checkpointer()
│   ├── [handlers.py:90] Create checkpointer from config
│   └── [postgres_config.py:236] PostgresCheckpointerConfig.create_checkpointer()
└── [persistence_mixin.py:39] _setup_store_from_fields() - optional store
```

### 3. Database Connection Flow

```
PostgresCheckpointerConfig.create_checkpointer() [postgres_config.py:236]
├── [postgres_config.py:279] Import ConnectionPool from psycopg_pool
├── [postgres_config.py:305] Configure connection kwargs
│   ├── Force disable prepared statements (prepare_threshold=None)
│   ├── Enable autocommit
│   └── Set unique application_name
├── [postgres_config.py:316] Create ConnectionPool with Supabase URI
├── [postgres_config.py:327] pool.open() - establish connections
├── [postgres_config.py:335] Create PostgresSaver with pool
└── [postgres_config.py:339] checkpointer.setup() - create tables
```

## Thread ID Generation System

### Current Thread ID Logic

**Location**: `persistence_mixin.py:375-414`

The system generates thread IDs using a hash-based approach:

```python
def _generate_default_thread_id(self) -> str:
    """Generate a consistent thread_id based on agent identity."""
    identity_components = [
        getattr(self, "name", "UnnamedAgent"),
        self.__class__.__name__,
    ]

    # Add engine type if available
    if hasattr(self, "engine_type"):
        identity_components.append(str(self.engine_type))

    # Add engine name if available
    if hasattr(self, "engine") and self.engine:
        if hasattr(self.engine, "name"):
            identity_components.append(self.engine.name)

    # Add conversation-specific details
    if hasattr(self, "topic"):
        identity_components.append(str(self.topic))
    if hasattr(self, "speakers") and self.speakers:
        identity_components.append(",".join(sorted(self.speakers)))
    if hasattr(self, "participant_agents") and self.participant_agents:
        participant_names = sorted([name for name in self.participant_agents.keys()])
        identity_components.append(",".join(participant_names))

    # Create stable hash
    identity_string = ":".join(identity_components)
    hash_digest = hashlib.md5(identity_string.encode()).hexdigest()

    # Final thread_id format
    agent_name = getattr(self, "name", "agent")
    thread_id = f"{agent_name}_{hash_digest[:8]}"

    return thread_id
```

### Thread ID Examples

Based on agent configuration:

```bash
# Simple Agent
"Simple Agent_a1b2c3d4"

# Conversation Agent with topic
"Conversation Agent_e5f6g7h8"

# Agent with speakers
"Multi Speaker_i9j0k1l2"
```

### Why Hash-Based IDs?

1. **Consistency**: Same agent configuration always generates same thread ID
2. **Uniqueness**: Different configurations produce different IDs
3. **Persistence**: Thread continues across restarts with same config
4. **Collision Avoidance**: MD5 hash reduces chance of conflicts

## Database Schema & Table Creation

### Table Creation Process

**Location**: LangGraph PostgresSaver handles table creation automatically

```
checkpointer.setup() [postgres_config.py:339]
├── Called during PostgresCheckpointerConfig.create_checkpointer()
├── Creates tables if they don't exist
├── Sets up indexes for performance
└── Handles schema migrations
```

### Main Tables

#### 1. `checkpoints` Table

**Purpose**: Stores agent state snapshots and conversation history  
**Created by**: LangGraph PostgresSaver.setup()

```sql
CREATE TABLE checkpoints (
    thread_id TEXT,                    -- Generated by _generate_default_thread_id()
    checkpoint_ns TEXT DEFAULT '',     -- Namespace for multi-tenant scenarios
    checkpoint_id TEXT,                -- Unique checkpoint identifier (UUID)
    parent_checkpoint_id TEXT,         -- Links to previous checkpoint
    type TEXT,                         -- Usually "checkpoint"
    checkpoint JSONB,                  -- Complete state snapshot
    metadata JSONB,                    -- Step metadata and execution info
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (thread_id, checkpoint_ns, checkpoint_id)
);
```

#### 2. `checkpoint_blobs` Table

**Purpose**: Stores large binary data separate from main checkpoints  
**Created by**: LangGraph PostgresSaver.setup()

```sql
CREATE TABLE checkpoint_blobs (
    thread_id TEXT,                    -- Links to checkpoints table
    checkpoint_ns TEXT DEFAULT '',     -- Namespace matching checkpoints
    channel TEXT,                      -- State channel name (e.g., "messages")
    version TEXT,                      -- Version identifier
    type TEXT,                         -- Data type identifier
    blob BYTEA,                        -- Binary data
    PRIMARY KEY (thread_id, checkpoint_ns, channel, version)
);
```

#### 3. `threads` Table

**Purpose**: Thread registration and metadata tracking  
**Created by**: `handlers.py:656-731` during thread registration

```sql
CREATE TABLE threads (
    thread_id TEXT PRIMARY KEY,           -- Same as checkpoint thread_id
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    metadata JSONB DEFAULT '{}'::jsonb,   -- Human-readable thread info
    user_id TEXT,                         -- Optional user association
    last_access TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);
```

### Data Flow: Agent Execution to Database

#### 1. Agent Invocation Flow

```
agent.invoke(input_data) [agent.py:1004]
├── [agent.py:1016] Call ExecutionMixin.run()
├── [execution_mixin.py] Setup effective config
│   ├── [persistence_mixin.py:375] Generate thread_id if not provided
│   ├── [persistence_mixin.py:347] Build effective_runnable_config
│   └── [handlers.py:656] Register thread in database
├── [agent.py:772] Create/compile runnable if needed
├── [execution_mixin.py] Execute compiled graph
└── [PostgresSaver] Automatically saves checkpoints
```

#### 2. Thread Registration Flow

```
register_thread_if_needed() [handlers.py:656-731]
├── Check if checkpointer is memory-based (skip if true)
├── Open database connection from pool
├── Check if threads table exists
│   └── Create table if missing
├── Convert metadata to JSON
├── INSERT thread with ON CONFLICT DO UPDATE
└── Update last_access timestamp
```

#### 3. Checkpoint Storage Flow

```
PostgresSaver.put() [LangGraph internals]
├── Serialize state to JSONB
├── Generate checkpoint_id (UUID)
├── Link to parent_checkpoint_id
├── INSERT into checkpoints table
├── Store large data in checkpoint_blobs if needed
└── Return checkpoint reference
```

## Data Storage Process

### 1. Agent Initialization

```python
# Agent creates persistence config
self.persistence = PostgresCheckpointerConfig(
    connection_string=connection_string,
    mode=CheckpointerMode.SYNC,
    storage_mode=CheckpointStorageMode.FULL,
    prepare_threshold=None,  # Disabled for Supabase
    auto_commit=True,
    min_pool_size=1,
    max_pool_size=2,
    connection_kwargs={
        "prepare_threshold": None,
        "application_name": f"haive_{agent_name}_{id(self)}"
    }
)
```

### 2. Thread Registration

**Location**: `handlers.py:656-731`

```python
def register_thread_if_needed(checkpointer, thread_id, metadata=None):
    # Create threads table if not exists
    # Insert thread with metadata
    # Update last_access timestamp
```

### 3. State Checkpointing

Each agent interaction creates a checkpoint:

```python
# Checkpoint data structure
checkpoint_data = {
    "thread_id": "Simple Agent_a1b2c3d4",
    "checkpoint_id": "1ef4-8b9a-8000-8001-123456789abc",
    "parent_checkpoint_id": "1ef4-8b9a-8000-8000-987654321def",
    "type": "checkpoint",
    "checkpoint": {
        "v": 1,
        "ts": "2025-01-07T10:30:00.000Z",
        "id": "1ef4-8b9a-8000-8001-123456789abc",
        "channel_values": {
            "messages": [...],
            "agent_state": {...},
            "conversation_context": {...}
        },
        "channel_versions": {
            "messages": "1ef4-8b9a-8000-8001-123456789abc",
            "agent_state": "1ef4-8b9a-8000-8001-123456789abc"
        },
        "versions_seen": {
            "__start__": {},
            "agent_node": {
                "messages": "1ef4-8b9a-8000-8001-123456789abc"
            }
        }
    },
    "metadata": {
        "source": "update",
        "step": 2,
        "writes": {
            "agent_node": {
                "messages": [...]
            }
        }
    }
}
```

## Thread ID vs Names Explanation

### Current System: Hash-Based IDs

- **Thread ID**: `"Simple Agent_a1b2c3d4"`
- **Purpose**: Unique identifier for database storage
- **Benefits**: Consistent, collision-resistant, programmatically generated

### Why Not Human-Readable Names?

1. **Collision Risk**: "ChatBot" could have multiple instances
2. **Special Characters**: Names might contain SQL-unsafe characters
3. **Length Limits**: Very long names could exceed database limits
4. **Consistency**: Hash ensures same config = same ID always

### Thread Metadata Storage

Human-readable information is stored in the `metadata` field:

```json
{
  "agent_name": "Simple Agent",
  "agent_class": "SimpleAgent",
  "topic": "Customer Support Chat",
  "speakers": ["user", "assistant"],
  "created_by": "user_123",
  "description": "Customer support conversation about billing"
}
```

## Conversation vs Agent Threads

### Single Agent Threads

```python
thread_id = "Simple Agent_a1b2c3d4"
metadata = {
    "agent_name": "Simple Agent",
    "agent_type": "SimpleAgent",
    "engine_type": "AGENT"
}
```

### Conversation Agent Threads

```python
thread_id = "Conversation Agent_e5f6g7h8"
metadata = {
    "agent_name": "Conversation Agent",
    "topic": "Product Strategy Discussion",
    "speakers": ["alice", "bob", "charlie"],
    "participant_agents": ["ResearchAgent", "AnalysisAgent"]
}
```

### Multi-Agent System Threads

```python
thread_id = "Multi Agent System_i9j0k1l2"
metadata = {
    "system_name": "Multi Agent System",
    "sub_agents": {
        "researcher": "Research Agent_x1y2z3a4",
        "analyst": "Analysis Agent_b5c6d7e8"
    }
}
```

## Data Retrieval Patterns

### By Thread ID (Exact Match)

```sql
SELECT * FROM checkpoints
WHERE thread_id = 'Simple Agent_a1b2c3d4'
ORDER BY created_at DESC;
```

### By Agent Name Pattern

```sql
SELECT DISTINCT thread_id, metadata
FROM threads
WHERE thread_id LIKE 'Simple Agent_%';
```

### By Metadata Search

```sql
SELECT thread_id, metadata
FROM threads
WHERE metadata->>'topic' = 'Customer Support Chat';
```

### Recent Conversations

```sql
SELECT thread_id, metadata, last_access
FROM threads
ORDER BY last_access DESC
LIMIT 10;
```

## Persistence Configuration Options

### Full History Mode

```python
storage_mode = CheckpointStorageMode.FULL
# Stores complete conversation history
# Allows for full replay and analysis
# Higher storage usage
```

### Shallow Mode

```python
storage_mode = CheckpointStorageMode.SHALLOW
# Only stores latest state
# Minimal storage usage
# No historical replay
```

### Sync vs Async

```python
# Synchronous (default)
mode = CheckpointerMode.SYNC
checkpointer = config.create_checkpointer()

# Asynchronous
mode = CheckpointerMode.ASYNC
checkpointer = await config.create_async_checkpointer()
```

## Connection Pool Management

### Per-Agent Isolation

Each agent gets its own connection pool to prevent conflicts:

```python
app_name = f"haive_{agent_name}_{id(self)}"
connection_kwargs = {
    "application_name": app_name,
    "prepare_threshold": None,  # Disable prepared statements
    "autocommit": True
}
```

### Pool Configuration

```python
pool = ConnectionPool(
    conninfo=connection_string,
    min_size=1,      # Minimum connections
    max_size=2,      # Maximum connections
    max_lifetime=1800,  # 30 minutes
    kwargs=connection_kwargs
)
```

## Debugging and Monitoring

### Check Active Threads

```sql
SELECT
    thread_id,
    metadata->>'agent_name' as agent_name,
    metadata->>'topic' as topic,
    created_at,
    last_access
FROM threads
ORDER BY last_access DESC;
```

### Checkpoint Count by Thread

```sql
SELECT
    thread_id,
    COUNT(*) as checkpoint_count,
    MAX(created_at) as latest_checkpoint
FROM checkpoints
GROUP BY thread_id
ORDER BY checkpoint_count DESC;
```

### Storage Usage

```sql
SELECT
    thread_id,
    COUNT(*) as checkpoint_count,
    pg_size_pretty(SUM(length(checkpoint::text))) as checkpoint_size,
    pg_size_pretty(SUM(length(metadata::text))) as metadata_size
FROM checkpoints
GROUP BY thread_id
ORDER BY SUM(length(checkpoint::text)) DESC;
```

### Recent Activity

```sql
SELECT
    c.thread_id,
    t.metadata->>'agent_name' as agent_name,
    COUNT(*) as recent_checkpoints,
    MAX(c.created_at) as latest_activity
FROM checkpoints c
JOIN threads t ON c.thread_id = t.thread_id
WHERE c.created_at > NOW() - INTERVAL '24 hours'
GROUP BY c.thread_id, t.metadata->>'agent_name'
ORDER BY latest_activity DESC;
```

## Best Practices

### Thread Management

1. **Let the system generate thread IDs** - they're designed for consistency
2. **Use metadata for human-readable information** - store names, topics, descriptions
3. **Monitor thread proliferation** - clean up old/unused threads periodically
4. **Use meaningful agent names** - they become part of the thread ID

### Performance Optimization

1. **Use shallow mode for high-volume agents** - reduces storage overhead
2. **Implement thread cleanup** - remove old conversations to maintain performance
3. **Monitor connection pools** - ensure proper resource management
4. **Index metadata fields** - for faster searching by topic/name

### Error Handling

1. **Graceful fallback to memory** - if Supabase connection fails
2. **Connection retry logic** - handle temporary network issues
3. **Pool management** - ensure connections are properly released
4. **Prepared statement avoidance** - Supabase compatibility requirement

## Summary

The Haive persistence system uses a sophisticated thread ID generation mechanism that prioritizes consistency and uniqueness over human readability. While the thread IDs look cryptic (`Simple Agent_a1b2c3d4`), they serve important technical purposes:

- **Consistency**: Same agent config always gets same thread ID
- **Uniqueness**: Prevents conflicts between similar agents
- **Persistence**: Conversations continue across restarts
- **Database Safety**: Avoids special character issues

Human-readable information is preserved in the metadata fields, allowing for meaningful organization and retrieval while maintaining the technical benefits of hash-based identification.

## Key File Responsibilities Summary

### Core Persistence Components

- **`agent.py`**: Entry point, inherits persistence capabilities
- **`persistence_mixin.py`**: Main persistence logic, thread ID generation, Supabase connection
- **`handlers.py`**: High-level persistence utilities, thread registration
- **`postgres_config.py`**: PostgreSQL-specific configuration, connection pool management
- **`.env`**: Contains Supabase credentials and connection strings

### Execution Flow Summary

1. **Agent Init** → Persistence Mixin → Supabase Connection → Table Setup
2. **Agent Invoke** → Thread Registration → State Execution → Checkpoint Storage
3. **Thread ID Generation** → Hash-based consistent naming → Database storage
4. **Metadata Storage** → Human-readable info in JSON fields → Easy querying

### Database Operations

- **Table Creation**: Automatic via LangGraph PostgresSaver
- **Thread Registration**: Custom logic in `handlers.py`
- **Checkpoint Storage**: LangGraph handles state serialization
- **Connection Management**: Pool-based with Supabase-specific optimizations
