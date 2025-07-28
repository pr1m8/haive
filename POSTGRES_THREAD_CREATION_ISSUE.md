# PostgreSQL Thread Creation Issue

**Date**: 2025-01-28  
**Status**: Active Bug  
**Severity**: High - Blocks agent execution with PostgreSQL persistence

## Issue Summary

Agent execution fails with PostgreSQL persistence enabled due to a unique constraint violation when trying to create threads. The error occurs in `PostgresSaverWithThreadCreation` when it attempts to insert a thread record.

## Error Details

```
ERROR: duplicate key value violates unique constraint "threads_id_key"
DETAIL:  Key (id)=(Simple Agent_d8dacb95-075d-4455-af68-2fc6d7aa1b9a) already exists.
```

## Root Cause

The `PostgresSaverWithThreadCreation` class uses an incorrect `ON CONFLICT` clause that doesn't match the actual database constraint:

**Current Code** (lines 71 and 83 in `postgres_saver_with_thread_creation.py`):

```sql
INSERT INTO threads (id, user_id, created_at, updated_at, last_access)
VALUES (%s, %s, NOW(), NOW(), NOW())
ON CONFLICT (id, user_id) DO NOTHING
```

**Problem**: The code expects a composite unique constraint on `(id, user_id)`, but the actual database constraint is only on `id`.

## File Locations

1. **Main Issue File**: `/packages/haive-core/src/haive/core/persistence/postgres_saver_with_thread_creation.py`
   - Lines 67-74 (connection pool path)
   - Lines 79-86 (direct connection path)

2. **Where It's Used**:
   - `/packages/haive-core/src/haive/core/persistence/postgres_config.py` (line 328)
   - Called via `create_postgres_saver_with_thread_creation()`

3. **Triggered By**: Any agent execution with PostgreSQL persistence enabled

## Stack Trace Path

1. Agent execution starts (`SimpleAgentV3.arun()`)
2. → `ExecutionMixin.run()`
3. → `LangGraph.invoke()`
4. → Checkpointer tries to save state
5. → `PostgresSaverWithThreadCreation.put()`
6. → `_ensure_thread_exists()`
7. → SQL INSERT fails on unique constraint

## Proposed Solutions

### Solution 1: Fix the ON CONFLICT Clause (Recommended)

Change both occurrences from:

```sql
ON CONFLICT (id, user_id) DO NOTHING
```

To:

```sql
ON CONFLICT (id) DO NOTHING
```

This matches the actual database constraint.

### Solution 2: Update Thread on Conflict

If you want to update the thread record when it exists:

```sql
ON CONFLICT (id) DO UPDATE SET
    user_id = EXCLUDED.user_id,
    updated_at = NOW(),
    last_access = NOW()
```

### Solution 3: Check Before Insert

Add a SELECT query to check if the thread exists before attempting INSERT:

```python
# Check if thread exists
cursor.execute("SELECT 1 FROM threads WHERE id = %s", (thread_id,))
if not cursor.fetchone():
    # Only insert if it doesn't exist
    cursor.execute(...)
```

## Temporary Workarounds

1. **Disable Persistence**: Set `persistence=False` when creating agents
2. **Use Memory Persistence**: Set `persistence=None` to use in-memory checkpointer
3. **Clear Thread Cache**: The class maintains a cache that might need clearing

## Test Case to Reproduce

```python
from haive.agents.simple.agent_v3 import SimpleAgentV3
from haive.core.engine.aug_llm import AugLLMConfig

# This will fail if PostgreSQL is configured
agent = SimpleAgentV3(
    name="test_agent",
    engine=AugLLMConfig(),
    persistence=True  # Or any PostgreSQL config
)

# First run might work, second run will fail
result = await agent.arun("Hello")  # Error on duplicate thread ID
```

## Impact

- All agents using PostgreSQL persistence are affected
- Prevents running the same agent multiple times
- Blocks testing and development when PostgreSQL is configured
- Affects both sync and async execution paths

## Related Files

- `/packages/haive-agents/src/haive/agents/base/mixins/persistence_mixin.py` - Sets up persistence
- `/packages/haive-core/src/haive/core/persistence/handlers.py` - Creates checkpointer
- `/packages/haive-core/src/haive/core/persistence/postgres_config.py` - PostgreSQL configuration

## Database Schema Note

The `threads` table appears to have:

- Primary key or unique constraint on `id` column only
- Not a composite key on `(id, user_id)` as the code assumes

This needs to be verified against the actual database schema.
