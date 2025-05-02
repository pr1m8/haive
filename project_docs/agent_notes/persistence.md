# Persistence in Haive

## Overview

Haive uses persistence mechanisms for maintaining agent state, enabling features like checkpointing, state tracing, and history tracking. PostgreSQL is the default persistence layer, providing robust storage for agent execution.

## PostgreSQL Integration

### Configuration

```python
from haive.core.engine.agent.persistence.postgres_config import PostgresCheckpointerConfig
from haive.core.engine.agent.config import AgentConfig

# Configure PostgreSQL persistence
postgres_config = PostgresCheckpointerConfig(
    connection_string="postgresql://username:password@localhost:5432/haive",
    table_name="agent_checkpoints",
    trace_history=True,  # Enable history tracking
    checkpoint_interval=1  # Save after every step
)

# Add to agent config
agent_config = AgentConfig(
    name="my_agent",
    persistence_config=postgres_config,
    # other config...
)
```

### Connection String Formats

```
# Standard connection string
postgresql://username:password@hostname:port/database

# With SSL
postgresql://username:password@hostname:port/database?sslmode=require

# Using environment variables (recommended for production)
postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_DB}
```

### Schema Creation

Haive automatically creates the necessary tables in PostgreSQL. The default schema includes:

- `agent_checkpoints`: Stores agent state checkpoints
- `agent_traces`: Stores execution traces
- `agent_history`: Stores execution history

## Persistence Modes

### Checkpointing Modes

```python
from haive.core.persistence.types import CheckpointerMode

# Configure checkpointing mode
postgres_config = PostgresCheckpointerConfig(
    connection_string="postgresql://postgres:postgres@localhost:5432/haive",
    mode=CheckpointerMode.FULL,  # Full persistence with history
    checkpoint_interval=1  # Save after every step
)
```

Available modes:

- `CheckpointerMode.MINIMAL`: Store only the latest state
- `CheckpointerMode.STANDARD`: Store checkpoints at defined intervals
- `CheckpointerMode.FULL`: Store full history with traces and metadata

### History Tracking

```python
# Configure history tracking
postgres_config = PostgresCheckpointerConfig(
    connection_string="postgresql://postgres:postgres@localhost:5432/haive",
    trace_history=True,  # Enable execution traces
    state_history=True,  # Enable full state history
    max_history=100  # Limit history entries
)
```

## State Recovery

```python
from haive.core.engine.agent.persistence.manager import CheckpointManager

# Create checkpoint manager
manager = CheckpointManager(
    config=postgres_config
)

# Retrieve state by session ID
state = manager.get_state(session_id="session_123")

# List available checkpoints
checkpoints = manager.list_checkpoints(
    agent_id="agent_456",
    limit=10
)

# Resume agent from checkpoint
agent = agent_config.instantiate()
agent.load_checkpoint(checkpoint_id="checkpoint_789")
```

## Connection Pooling

Haive manages connection pooling automatically for performance:

```python
# Configure connection pooling
postgres_config = PostgresCheckpointerConfig(
    connection_string="postgresql://postgres:postgres@localhost:5432/haive",
    pool_size=10,  # Maximum connections in pool
    pool_timeout=30,  # Timeout in seconds
    pool_recycle=1800  # Connection recycle time in seconds
)
```

## Multi-tenant Configuration

For multi-tenant deployments:

```python
# Configure for multi-tenant use
postgres_config = PostgresCheckpointerConfig(
    connection_string="postgresql://postgres:postgres@localhost:5432/haive",
    tenant_id="customer_123",  # Tenant identifier
    tenant_isolation=True,  # Enforce tenant isolation
    schema_name="tenant_123"  # Optional separate schema
)
```

## Async Support

For async workflows:

```python
# Create agent with async persistence
agent = agent_config.instantiate()

# Async operations
async def process_async():
    # Invoke agent asynchronously
    result = await agent.ainvoke("Hello")

    # Save checkpoint asynchronously
    checkpoint_id = await agent.asave_checkpoint()

    # Load checkpoint asynchronously
    await agent.aload_checkpoint(checkpoint_id)
```

## Fallback to Memory Persistence

If PostgreSQL is unavailable, Haive can fall back to in-memory persistence:

```python
from haive.core.engine.agent.persistence.memory_config import MemoryCheckpointerConfig

# Configure memory persistence
memory_config = MemoryCheckpointerConfig(
    trace_history=True,
    checkpoint_interval=1
)

# Add to agent config
agent_config = AgentConfig(
    name="my_agent",
    persistence_config=memory_config,
    # other config...
)
```

## Configuration in Production

For production environments:

```python
# Production PostgreSQL configuration
postgres_config = PostgresCheckpointerConfig(
    connection_string="${POSTGRES_CONNECTION_STRING}",  # From environment
    pool_size=20,
    pool_timeout=60,
    pool_recycle=3600,
    trace_history=True,
    checkpoint_interval=5,
    ssl_mode="require",
    application_name="haive-agent"
)
```

## Database Maintenance

Haive includes utilities for database maintenance:

```python
from haive.core.persistence.postgres_maintenance import clean_old_checkpoints

# Clean up old checkpoints
clean_old_checkpoints(
    connection_string="postgresql://postgres:postgres@localhost:5432/haive",
    older_than_days=30,
    agent_id=None,  # Optional filter by agent
    dry_run=False
)
```

## Query Performance

Haive automatically creates indexes for optimal query performance:

```sql
-- Automatically created indexes
CREATE INDEX idx_agent_checkpoints_session_id ON agent_checkpoints(session_id);
CREATE INDEX idx_agent_checkpoints_agent_id ON agent_checkpoints(agent_id);
CREATE INDEX idx_agent_traces_checkpoint_id ON agent_traces(checkpoint_id);
CREATE INDEX idx_agent_history_agent_id_timestamp ON agent_history(agent_id, timestamp);
```

## Migrations

Haive handles schema migrations automatically. When upgrading:

```python
from haive.core.persistence.migrations import run_migrations

# Run migrations
run_migrations(
    connection_string="postgresql://postgres:postgres@localhost:5432/haive"
)
```
