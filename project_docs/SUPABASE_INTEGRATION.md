# Supabase Integration Guide

## Overview

Haive agents automatically integrate with Supabase for conversation persistence and state management. This document covers the configuration, implementation, and troubleshooting of Supabase integration.

## Quick Start

### 1. Environment Setup

Set the Supabase connection string in your environment:

```bash
export POSTGRES_CONNECTION_STRING="postgresql://postgres.your-project:password@aws-0-region.pooler.supabase.com:6543/postgres"
```

Or in your `.env` file:

```env
POSTGRES_CONNECTION_STRING=postgresql://postgres.your-project:password@aws-0-region.pooler.supabase.com:6543/postgres
```

### 2. Agent Creation

Agents automatically detect and use Supabase configuration:

```python
from haive.agents.simple.agent import SimpleAgent
from haive.core.engine.aug_llm import AugLLMConfig

# Agent automatically uses Supabase for persistence
engine = AugLLMConfig()
agent = SimpleAgent(engine=engine, name="My Agent")

# Run with conversation persistence
result = agent.run(
    {'messages': [HumanMessage(content="Hello!")]},
    config={'configurable': {'thread_id': 'unique-conversation-id'}}
)
```

### 3. Verification

Check that your agent is using Supabase:

```python
if hasattr(agent, 'persistence') and agent.persistence:
    if "supabase.com" in agent.persistence.connection_string:
        print("✅ Using Supabase for persistence!")
```

## Architecture

### Database Schema

Supabase stores conversation data in three main tables:

#### `checkpoints`

- **Purpose**: Conversation state snapshots
- **Key Fields**: `thread_id`, `checkpoint_id`, `parent_checkpoint_id`, `type`
- **Usage**: Tracks conversation flow and branching

#### `checkpoint_writes`

- **Purpose**: Individual state changes and writes
- **Key Fields**: `thread_id`, `idx`, `channel`, `type`, `blob`
- **Usage**: Records each step in conversation processing

#### `checkpoint_blobs`

- **Purpose**: Large data storage (messages, state)
- **Key Fields**: `thread_id`, `channel`, `type`, `blob`
- **Usage**: Stores actual conversation content and agent state

### Configuration Flow

1. **Environment Detection**: `PersistenceMixin` checks for `POSTGRES_CONNECTION_STRING`
2. **Auto-Configuration**: If found, creates `PostgresCheckpointerConfig` with Supabase connection
3. **Fallback**: If not found, uses default PostgreSQL configuration
4. **Validation**: Connection string is validated for Supabase compatibility

## Implementation Details

### Modified Components

#### PersistenceMixin (`packages/haive-agents/src/haive/agents/base/mixins/persistence_mixin.py`)

**Change**: Added automatic Supabase detection

```python
def _setup_default_persistence(self):
    # Check for connection string from environment
    connection_string = os.getenv("POSTGRES_CONNECTION_STRING")

    if connection_string:
        # Use the connection string from environment (likely Supabase)
        self.persistence = PostgresCheckpointerConfig(
            connection_string=connection_string,
            mode=CheckpointerMode.SYNC,
            storage_mode=CheckpointStorageMode.FULL
        )
        logger.info(f"Using PostgreSQL persistence from environment")
    else:
        # Fall back to default configuration
        self.persistence = PostgresCheckpointerConfig()
```

#### ExecutionMixin (`packages/haive-agents/src/haive/agents/base/mixins/execution_mixin.py`)

**Change**: Fixed recursion limit debug display

```python
# Before (incorrect)
recursion_limit = base_config.get("recursion_limit")

# After (correct)
recursion_limit = base_config.get("configurable", {}).get("recursion_limit")
```

### Configuration Options

#### PostgresCheckpointerConfig

When using Supabase, the following configuration is automatically applied:

```python
PostgresCheckpointerConfig(
    connection_string=os.getenv("POSTGRES_CONNECTION_STRING"),
    mode=CheckpointerMode.SYNC,           # Synchronous operations
    storage_mode=CheckpointStorageMode.FULL  # Full state storage
)
```

#### Recursion Limits

Default recursion limit is set to `100` in agent base configuration:

```python
runnable_config = {
    'configurable': {
        'recursion_limit': 100
    }
}
```

## Usage Patterns

### Basic Conversation

```python
from haive.agents.simple.agent import SimpleAgent
from haive.core.engine.aug_llm import AugLLMConfig
from langchain_core.messages import HumanMessage

engine = AugLLMConfig()
agent = SimpleAgent(engine=engine)

# Each thread_id represents a separate conversation
result = agent.run(
    {'messages': [HumanMessage(content="Start conversation")]},
    config={'configurable': {'thread_id': 'conversation-1'}}
)
```

### Resuming Conversations

```python
# Continue existing conversation by using same thread_id
result = agent.run(
    {'messages': [HumanMessage(content="Continue conversation")]},
    config={'configurable': {'thread_id': 'conversation-1'}}
)
```

### Multiple Conversations

```python
# Different thread_ids maintain separate conversation histories
result1 = agent.run(messages, config={'configurable': {'thread_id': 'user-123-session-1'}})
result2 = agent.run(messages, config={'configurable': {'thread_id': 'user-456-session-1'}})
```

## Monitoring and Debugging

### Supabase Dashboard

Monitor your data in the Supabase dashboard:

**URL Pattern**: `https://supabase.com/dashboard/project/{project-id}/editor/{table-id}`

### SQL Queries

#### Recent Conversations

```sql
SELECT thread_id, COUNT(*) as message_count, MAX(idx) as latest_idx
FROM checkpoint_writes
GROUP BY thread_id
ORDER BY latest_idx DESC
LIMIT 20;
```

#### Specific Conversation

```sql
SELECT * FROM checkpoint_writes
WHERE thread_id = 'your-thread-id'
ORDER BY idx;
```

#### Conversation Statistics

```sql
SELECT
    COUNT(DISTINCT thread_id) as total_conversations,
    COUNT(*) as total_writes,
    MAX(idx) as highest_idx
FROM checkpoint_writes;
```

### Debug Logging

Enable debug logging to monitor persistence operations:

```python
import logging
logging.getLogger('haive.agents.base.mixins').setLevel(logging.DEBUG)
```

## Troubleshooting

### Common Issues

#### 1. Prepared Statement Errors

**Error**: `prepared statement "_pg3_X" already exists`

**Cause**: psycopg connection pooling reuses prepared statements

**Impact**: ⚠️ Does NOT prevent data from being saved

**Solution**: These errors can be safely ignored. Data persistence continues to work correctly.

#### 2. Connection String Format

**Error**: Connection failures or wrong database

**Cause**: Incorrect connection string format

**Solution**: Ensure connection string follows this format:

```
postgresql://postgres.{project-ref}:{password}@aws-0-{region}.pooler.supabase.com:6543/postgres
```

#### 3. Missing Environment Variable

**Error**: Using default PostgreSQL instead of Supabase

**Cause**: `POSTGRES_CONNECTION_STRING` not set

**Solution**:

```bash
export POSTGRES_CONNECTION_STRING="your-supabase-connection-string"
```

#### 4. Table Permissions

**Error**: Permission denied on tables

**Cause**: Supabase RLS (Row Level Security) policies

**Solution**: Ensure your database user has appropriate permissions:

```sql
-- Grant permissions to postgres user
GRANT ALL ON checkpoints TO postgres;
GRANT ALL ON checkpoint_writes TO postgres;
GRANT ALL ON checkpoint_blobs TO postgres;
```

### Verification Steps

1. **Check Environment**:

   ```bash
   echo $POSTGRES_CONNECTION_STRING
   ```

2. **Test Connection**:

   ```python
   import psycopg
   import os

   conn_string = os.getenv("POSTGRES_CONNECTION_STRING")
   with psycopg.connect(conn_string) as conn:
       print("✅ Connection successful")
   ```

3. **Verify Tables**:
   ```python
   with psycopg.connect(conn_string) as conn:
       with conn.cursor() as cur:
           cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
           tables = cur.fetchall()
           print("Available tables:", [t[0] for t in tables])
   ```

## Performance Considerations

### Connection Pooling

Supabase uses connection pooling via PgBouncer. Consider these settings:

- **Pool Mode**: Transaction (default)
- **Max Connections**: Adjust based on your plan
- **Connection Timeout**: Configure appropriate timeouts

### Optimization Tips

1. **Thread ID Strategy**: Use meaningful, hierarchical thread IDs:

   ```python
   thread_id = f"user-{user_id}-session-{session_id}-{timestamp}"
   ```

2. **Batch Operations**: Group related operations when possible

3. **Cleanup**: Periodically clean old conversation data:
   ```sql
   DELETE FROM checkpoint_writes WHERE created_at < NOW() - INTERVAL '30 days';
   ```

## Security

### Connection Security

- Use SSL connections (default with Supabase)
- Store connection strings in secure environment variables
- Never commit connection strings to version control

### Data Privacy

- Consider data retention policies
- Implement appropriate RLS policies if needed
- Monitor access patterns in Supabase dashboard

## Migration

### From Local PostgreSQL

1. Export existing data from local PostgreSQL
2. Update environment variables to point to Supabase
3. Import data to Supabase if needed
4. Verify agent operations work correctly

### Backup Strategy

Consider implementing regular backups:

```sql
-- Export conversation data
COPY (SELECT * FROM checkpoint_writes WHERE thread_id LIKE 'important-%')
TO '/path/to/backup.csv' WITH CSV HEADER;
```

## Related Documentation

- [Agent Persistence Guide](./AGENT_PERSISTENCE.md)
- [PostgreSQL Configuration](../packages/haive-core/docs/POSTGRESQL_CONFIG.md)
- [Environment Setup](./ENVIRONMENT_SETUP.md)
