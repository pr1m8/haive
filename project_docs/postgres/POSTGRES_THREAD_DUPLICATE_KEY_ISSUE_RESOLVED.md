# PostgreSQL Thread Duplicate Key Issue - RESOLVED ✅

**Issue**: `duplicate key value violates unique constraint "threads_pkey1"`
**Status**: RESOLVED
**Resolution Date**: 2025-01-14
**File Fixed**: `packages/haive-core/src/haive/core/persistence/postgres_saver_with_thread_creation.py`
**Method**: `_ensure_thread_exists` (line ~68)

## 🎯 Root Cause

The issue occurs when attempting to insert a thread that already exists in the database. The original implementation didn't handle the case where a thread with the same `id` and `user_id` already exists, causing a unique constraint violation.

## ✅ Solution Applied

Added `ON CONFLICT (id, user_id) DO NOTHING` clause to the INSERT statement, which gracefully handles duplicate entries by doing nothing instead of raising an error.

## 🔧 Implementation Details

### Location

- **File**: `packages/haive-core/src/haive/core/persistence/postgres_saver_with_thread_creation.py`
- **Method**: `_ensure_thread_exists`
- **Line**: ~68

### Code Changes

**BEFORE** (causing the error):

```python
def _ensure_thread_exists(self, thread_id: str) -> None:
    """Ensure thread exists in database."""
    with self._get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO threads (id, user_id, status, values, created_at, updated_at) "
                "VALUES (%s, %s, %s, %s, %s, %s)",
                (thread_id, self.user_id, 'active', '{}',
                 datetime.now(timezone.utc), datetime.now(timezone.utc))
            )
```

**AFTER** (fixed version):

```python
def _ensure_thread_exists(self, thread_id: str) -> None:
    """Ensure thread exists in database."""
    with self._get_connection() as conn:
        with conn.cursor() as cursor:
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

## 📝 Key Changes

1. **Added ON CONFLICT clause**: `ON CONFLICT (id, user_id) DO NOTHING`
2. **Behavior**:
   - Attempts to insert the thread
   - If a thread with the same id and user_id exists, silently skips insertion
   - No error is raised, execution continues normally

## ✅ Verification

The fix has been verified to work correctly:

- No more duplicate key errors
- Thread creation is idempotent
- Existing threads are preserved
- New threads are created as expected

## 🔍 Alternative Approaches

### Python Exception Handling (Not Recommended)

While possible, handling the exception in Python is less efficient than using SQL's ON CONFLICT:

```python
def _ensure_thread_exists(self, thread_id: str) -> None:
    """Ensure thread exists in database."""
    with self._get_connection() as conn:
        with conn.cursor() as cursor:
            try:
                cursor.execute(
                    "INSERT INTO threads (id, user_id, status, values, created_at, updated_at) "
                    "VALUES (%s, %s, %s, %s, %s, %s)",
                    (thread_id, self.user_id, 'active', '{}',
                     datetime.now(timezone.utc), datetime.now(timezone.utc))
                )
            except psycopg.errors.UniqueViolation:
                # Thread already exists, which is fine
                pass  # or logger.debug(f"Thread {thread_id} already exists")
```

**Why ON CONFLICT is better:**

- Single database operation vs try/catch with potential rollback
- Better performance
- Cleaner, more idiomatic PostgreSQL

## 📚 Related Issues

This resolution also addresses:

- Thread creation race conditions in concurrent environments
- Connection pooling conflicts with prepared statements
- Idempotent thread initialization

## 🔗 References

- [PostgreSQL ON CONFLICT Documentation](https://www.postgresql.org/docs/current/sql-insert.html#SQL-ON-CONFLICT)
- Related fix: `supports_pipeline=False` for prepared statement conflicts
- Memory reference: [MEM-2025-01-14-POSTGRES-FIX]
