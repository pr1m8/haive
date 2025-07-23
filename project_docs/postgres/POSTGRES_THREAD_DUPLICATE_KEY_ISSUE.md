# PostgreSQL Thread Duplicate Key Issue

**Issue Type**: Database Constraint Violation  
**Severity**: Medium (affects execution but not agent functionality)  
**First Observed**: 2025-01-21 during LLM Compiler V3 testing  
**Status**: Active

## 🚨 Error Details

### Error Message

```
ERROR: Failed to ensure thread test_compiler_planner_d6294381-73f3-44b8-962e-31235e23bb58 exists:
duplicate key value violates unique constraint "threads_pkey1"
DETAIL: Key (id, user_id)=(test_compiler_planner_d6294381-73f3-44b8-962e-31235e23bb58, 5335c7e6-1d51-42d2-b958-0ad2ad2c269b) already exists.
```

### Stack Trace Location

```python
File "/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/persistence/postgres_saver_with_thread_creation.py", line 68, in _ensure_thread_exists
    cursor.execute(
psycopg.errors.UniqueViolation: duplicate key value violates unique constraint "threads_pkey1"
```

## 📋 Issue Analysis

### Root Cause

The `PostgresSaverWithThreadCreation` class is attempting to create a thread that already exists in the database, violating the unique constraint on `(id, user_id)`.

### When It Occurs

- During agent execution when using PostgreSQL persistence
- Specifically when the checkpointer tries to ensure a thread exists
- Most commonly with agent names that generate consistent thread IDs

### Impact

- Agent execution continues but state persistence fails
- Error messages clutter output
- Potential loss of conversation history/state

## 🔧 Potential Fixes

### 1. **Check Before Insert (Recommended)**

Modify `_ensure_thread_exists` to check if thread exists before inserting:

```python
def _ensure_thread_exists(self, thread_id: str) -> None:
    """Ensure thread exists, creating if necessary."""
    with self._get_connection() as conn:
        with conn.cursor() as cursor:
            # First check if thread exists
            cursor.execute(
                "SELECT 1 FROM threads WHERE id = %s AND user_id = %s",
                (thread_id, self.user_id)
            )

            if cursor.fetchone() is None:
                # Only insert if thread doesn't exist
                cursor.execute(
                    "INSERT INTO threads (id, user_id, status, values, created_at, updated_at) "
                    "VALUES (%s, %s, %s, %s, %s, %s)",
                    (thread_id, self.user_id, 'active', '{}',
                     datetime.now(timezone.utc), datetime.now(timezone.utc))
                )
```

### 2. **Use INSERT ON CONFLICT**

PostgreSQL-specific solution using UPSERT:

```python
cursor.execute(
    """
    INSERT INTO threads (id, user_id, status, values, created_at, updated_at)
    VALUES (%s, %s, %s, %s, %s, %s)
    ON CONFLICT (id, user_id) DO NOTHING
    """,
    (thread_id, self.user_id, 'active', '{}',
     datetime.now(timezone.utc), datetime.now(timezone.utc))
)
```

### 3. **Catch and Handle Exception**

Wrap the insert in try-except:

```python
try:
    cursor.execute(
        "INSERT INTO threads (id, user_id, status, values, created_at, updated_at) "
        "VALUES (%s, %s, %s, %s, %s, %s)",
        (thread_id, self.user_id, 'active', '{}',
         datetime.now(timezone.utc), datetime.now(timezone.utc))
    )
except psycopg.errors.UniqueViolation:
    # Thread already exists, which is fine
    logger.debug(f"Thread {thread_id} already exists for user {self.user_id}")
```

## 🔍 Debugging Steps

### 1. Check Existing Threads

```sql
-- Check if specific thread exists
SELECT * FROM threads
WHERE id = 'test_compiler_planner_d6294381-73f3-44b8-962e-31235e23bb58'
AND user_id = '5335c7e6-1d51-42d2-b958-0ad2ad2c269b';

-- List all threads for user
SELECT id, created_at, updated_at, status
FROM threads
WHERE user_id = '5335c7e6-1d51-42d2-b958-0ad2ad2c269b'
ORDER BY created_at DESC;
```

### 2. Check Constraint Definition

```sql
-- View the constraint
\d threads

-- Or query constraint info
SELECT conname, contype, conkey
FROM pg_constraint
WHERE conrelid = 'threads'::regclass;
```

## 🚀 Quick Workarounds

### 1. **Use Unique Thread IDs**

Add timestamp or random suffix to thread IDs:

```python
import uuid
thread_id = f"{agent_name}_{uuid.uuid4()}"
```

### 2. **Disable Persistence Temporarily**

For testing, use in-memory checkpointer:

```python
from langgraph.checkpoint.memory import MemorySaver
checkpointer = MemorySaver()
```

### 3. **Clean Up Old Threads**

```sql
-- Delete old test threads (BE CAREFUL!)
DELETE FROM threads
WHERE id LIKE 'test_%'
AND created_at < NOW() - INTERVAL '1 day';
```

## 📍 File Locations

- **Error Source**: `packages/haive-core/src/haive/core/persistence/postgres_saver_with_thread_creation.py`
- **Related Files**:
  - `packages/haive-agents/src/haive/agents/base/mixins/execution_mixin.py`
  - LangGraph checkpointer integration

## 🎯 Recommended Solution

The best approach is **Option 2: Use INSERT ON CONFLICT** as it's:

- PostgreSQL native
- Atomic operation
- No race conditions
- Clean and simple

This change should be made in the `_ensure_thread_exists` method of `PostgresSaverWithThreadCreation`.

## 📝 Notes

- This issue doesn't affect agent functionality, only state persistence
- The agent continues to work correctly despite the error
- It's a concurrency/idempotency issue in the persistence layer
- Similar issues reported in project docs under resolved issues
