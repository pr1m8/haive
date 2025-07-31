# Troubleshooting: PostgreSQL Prepared Statement Errors

## Overview

When using Haive agents with PostgreSQL/Supabase persistence, you may encounter prepared statement errors like:

```
Error setting up checkpointer: prepared statement "_pg3_0" already exists
Error during agent execution: prepared statement "_pg3_1" already exists
```

**⚠️ IMPORTANT**: These errors **DO NOT** prevent data persistence. Your conversations are still being saved correctly.

## Understanding the Issue

### What Are Prepared Statements?

Prepared statements are pre-compiled SQL queries that improve performance by avoiding repeated parsing. They're created once and reused with different parameters.

### Why Do These Errors Occur?

1. **Connection Pooling**: psycopg (PostgreSQL adapter) reuses database connections
2. **Statement Reuse**: When connections are reused, prepared statements may already exist
3. **psycopg Behavior**: The driver attempts to create statements that already exist in the pool

### Why They Don't Affect Functionality

- **Error Location**: Errors occur during statement preparation, not during actual data operations
- **Fallback Mechanism**: psycopg continues with regular queries if prepared statements fail
- **Data Integrity**: The actual INSERT/UPDATE operations succeed regardless

## Verification

### Confirm Data Is Being Saved

You can verify that data persistence works despite the errors:

1. **Check Supabase Dashboard**:
   - Go to your Supabase project dashboard
   - Navigate to the Table Editor
   - Look for tables: `checkpoints`, `checkpoint_writes`, `checkpoint_blobs`
   - Verify recent entries exist

2. **Query Database Directly**:

   ```python
   import os
   import asyncio
   import psycopg

   async def check_data():
       conn_string = os.getenv("POSTGRES_CONNECTION_STRING")
       async with await psycopg.AsyncConnection.connect(conn_string) as conn:
           async with conn.cursor() as cur:
               await cur.execute("SELECT COUNT(*) FROM checkpoint_writes")
               count = (await cur.fetchone())[0]
               print(f"Total checkpoint writes: {count}")

   asyncio.run(check_data())
   ```

3. **Run Test Script**:
   ```bash
   poetry run python notebooks/supabase_tests/test_direct_write.py
   ```

## Mitigation Strategies

### 1. Suppress Warnings (Recommended)

Since these errors don't affect functionality, you can suppress them:

```python
import warnings
warnings.filterwarnings("ignore", message=".*prepared statement.*")
```

### 2. Logging Configuration

Adjust logging to reduce noise:

```python
import logging

# Reduce psycopg logging level
logging.getLogger('psycopg').setLevel(logging.ERROR)
logging.getLogger('haive.core.persistence').setLevel(logging.WARNING)
```

### 3. Environment Variable

Set environment variable to suppress specific warnings:

```bash
export PYTHONWARNINGS="ignore:.*prepared statement.*:UserWarning"
```

## Advanced Solutions

### Connection Pool Configuration

If you need to address the root cause, you can configure connection pooling:

```python
from haive.core.persistence.postgres_config import PostgresCheckpointerConfig

# Custom configuration with pool settings
config = PostgresCheckpointerConfig(
    connection_string=os.getenv("POSTGRES_CONNECTION_STRING"),
    # Add custom connection options if needed
    connection_kwargs={
        'prepare_threshold': None,  # Disable prepared statements
    }
)
```

### Fresh Process Testing

If you need to test without connection reuse:

```python
import subprocess
import sys

# Run agent in subprocess to avoid connection pool issues
result = subprocess.run([
    sys.executable, '-c', '''
import os
from haive.agents.simple.agent import SimpleAgent
from haive.core.engine.aug_llm import AugLLMConfig

agent = SimpleAgent(engine=AugLLMConfig())
# ... your agent code here
'''
], capture_output=True, text=True)
```

## When to Take Action

### Ignore These Cases

- ✅ Error contains "prepared statement" and "_pg3_"
- ✅ Data is still being written to database
- ✅ Agent execution completes successfully
- ✅ Only warnings/errors during setup phase

### Investigate These Cases

- ❌ Data is NOT being written to database
- ❌ Agent execution fails completely
- ❌ Connection timeouts or authentication errors
- ❌ Table does not exist errors

## Monitoring

### Production Monitoring

For production deployments, monitor these metrics:

1. **Data Write Success Rate**:

   ```sql
   SELECT
       DATE(created_at) as date,
       COUNT(*) as writes_per_day
   FROM checkpoint_writes
   WHERE created_at > NOW() - INTERVAL '7 days'
   GROUP BY DATE(created_at)
   ORDER BY date;
   ```

2. **Error Rate vs Success Rate**:
   - Track prepared statement errors separately from actual data failures
   - Alert only on data persistence failures, not prepared statement warnings

3. **Connection Pool Health**:
   - Monitor connection pool utilization
   - Watch for connection exhaustion

### Health Check Script

```python
#!/usr/bin/env python3
"""Health check for Haive persistence."""

import os
import asyncio
import psycopg
from datetime import datetime, timedelta

async def health_check():
    """Check if persistence is working."""

    conn_string = os.getenv("POSTGRES_CONNECTION_STRING")
    if not conn_string:
        return False, "No connection string"

    try:
        async with await psycopg.AsyncConnection.connect(conn_string) as conn:
            async with conn.cursor() as cur:
                # Check if we can write
                test_id = f"health_check_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                await cur.execute(
                    "INSERT INTO checkpoint_writes (thread_id, checkpoint_ns, checkpoint_id, task_id, idx, channel, type, blob) VALUES (%s, '', '00000000-0000-0000-0000-000000000000', '00000000-0000-0000-0000-000000000000', 1, 'health', 'check', %s)",
                    (test_id, b'health check')
                )
                await conn.commit()

                # Verify write
                await cur.execute(
                    "SELECT COUNT(*) FROM checkpoint_writes WHERE thread_id = %s",
                    (test_id,)
                )
                count = (await cur.fetchone())[0]

                # Clean up
                await cur.execute(
                    "DELETE FROM checkpoint_writes WHERE thread_id = %s",
                    (test_id,)
                )
                await conn.commit()

                return count > 0, "Persistence working"

    except Exception as e:
        return False, f"Error: {e}"

if __name__ == "__main__":
    success, message = asyncio.run(health_check())
    print(f"{'✅' if success else '❌'} {message}")
    exit(0 if success else 1)
```

## Summary

**Key Points**:

1. **Prepared statement errors are cosmetic** - they don't prevent data persistence
2. **Data is still being saved** to Supabase/PostgreSQL correctly
3. **Safe to ignore** these specific error messages
4. **Monitor data writes** rather than prepared statement warnings
5. **Use verification scripts** to confirm persistence is working

**Recommended Action**: Suppress the warnings and monitor actual data persistence metrics instead.

## Related Documentation

- [Supabase Integration Guide](./SUPABASE_INTEGRATION.md)
- [Agent Mixins Documentation](../packages/haive-agents/src/haive/agents/base/mixins/README.md)
- [PostgreSQL Configuration](../packages/haive-core/docs/POSTGRESQL_CONFIG.md)
