# Supabase Integration Tests

This directory contains integration tests for Haive agents with Supabase persistence.

## Overview

These tests verify that Haive agents properly integrate with Supabase for conversation persistence and state management. They test the automatic Supabase configuration detection and data persistence functionality.

## Test Files

### Core Integration Tests

- **`test_supabase_complete.py`**: Comprehensive test demonstrating full Supabase integration
- **`test_direct_write.py`**: Direct database write test to verify Supabase connectivity
- **`check_recent_data.py`**: Utility to check recent data in Supabase tables

### Helper Scripts

- **`test_fresh_process.py`**: Tests agent in subprocess to avoid connection pooling issues
- **`test_supabase_working.py`**: Demonstrates working persistence despite prepared statement errors
- **`test_supabase_verification.py`**: Detailed verification of database writes
- **`fix_prepared_statements.py`**: Utility to clean up prepared statements

### Documentation

- **`SUPABASE_INTEGRATION_SUMMARY.md`**: Summary of integration test results and current status

## Prerequisites

### Environment Setup

1. **Supabase Connection**: Set your Supabase connection string:

   ```bash
   export POSTGRES_CONNECTION_STRING="postgresql://postgres.{project}:{password}@aws-0-{region}.pooler.supabase.com:6543/postgres"
   ```

2. **Database Tables**: Ensure these tables exist in your Supabase project:
   - `checkpoints`
   - `checkpoint_writes`
   - `checkpoint_blobs`

### Running Tests

From the root directory:

```bash
# Run all Supabase integration tests
poetry run pytest packages/haive-agents/tests/integration/supabase/ -v

# Run specific test
poetry run pytest packages/haive-agents/tests/integration/supabase/test_supabase_complete.py -v

# Run with detailed output
poetry run pytest packages/haive-agents/tests/integration/supabase/ -v -s
```

### Manual Test Scripts

You can also run the test scripts directly:

```bash
# Complete integration test
poetry run python packages/haive-agents/tests/integration/supabase/test_supabase_complete.py

# Direct database connectivity test
poetry run python packages/haive-agents/tests/integration/supabase/test_direct_write.py

# Check recent data
poetry run python packages/haive-agents/tests/integration/supabase/check_recent_data.py
```

## What These Tests Verify

### ✅ Automatic Configuration

- Agents detect `POSTGRES_CONNECTION_STRING` environment variable
- Automatic fallback to individual PostgreSQL environment variables
- Proper `PostgresCheckpointerConfig` initialization

### ✅ Conversation Persistence

- Messages are saved to Supabase tables
- Thread IDs maintain separate conversation histories
- State continuity across agent sessions

### ✅ Recursion Limit Handling

- Debug messages show correct recursion limit values
- Default limit of 100 is properly applied
- Custom limits can be overridden via configuration

### ✅ Error Handling

- Prepared statement errors don't prevent data persistence
- Data writes succeed despite connection pooling issues
- Graceful degradation when persistence fails

## Expected Results

### Successful Test Output

```
✅ Using Supabase connection
✅ Agent is using Supabase for persistence!
✅ Recursion limit: 100
✅ Agent completed successfully!
✅ SUCCESS! Data has been written to Supabase!
```

### Database Verification

After running tests, you should see:

- New entries in `checkpoint_writes` table
- Corresponding entries in `checkpoints` table
- Thread IDs matching your test runs

### Supabase Dashboard

View your test data:

- **URL**: `https://supabase.com/dashboard/project/{your-project-id}/editor/{table-id}`
- **SQL Query**: `SELECT * FROM checkpoint_writes ORDER BY idx DESC LIMIT 10;`

## Troubleshooting

### Common Issues

**❌ No POSTGRES_CONNECTION_STRING**

```bash
# Solution: Set environment variable
export POSTGRES_CONNECTION_STRING="your-supabase-connection-string"
```

**❌ Tables Don't Exist**

```sql
-- Run in Supabase SQL editor to create tables
-- (Tables are usually auto-created by LangGraph)
```

**⚠️ Prepared Statement Errors**

- **Expected behavior**: These errors don't prevent data persistence
- **Impact**: None - data is still saved correctly
- **Action**: Ignore these errors

### Debug Mode

Enable detailed logging:

```python
import logging
logging.getLogger('haive.agents.base.mixins').setLevel(logging.DEBUG)
logging.getLogger('haive.core.persistence').setLevel(logging.DEBUG)
```

### Health Check

Run a quick health check:

```bash
# Check if Supabase is accessible
poetry run python packages/haive-agents/tests/integration/supabase/test_direct_write.py
```

## Integration with CI/CD

These tests can be included in CI/CD pipelines with proper environment setup:

```yaml
# Example GitHub Actions
env:
  POSTGRES_CONNECTION_STRING: ${{ secrets.SUPABASE_CONNECTION_STRING }}

steps:
  - name: Run Supabase Integration Tests
    run: poetry run pytest packages/haive-agents/tests/integration/supabase/ -v
```

## Related Documentation

- [Supabase Integration Guide](../../../../project_docs/SUPABASE_INTEGRATION.md)
- [Troubleshooting Prepared Statements](../../../../project_docs/TROUBLESHOOTING_PREPARED_STATEMENTS.md)
- [Agent Mixins Documentation](../../src/haive/agents/base/mixins/README.md)
