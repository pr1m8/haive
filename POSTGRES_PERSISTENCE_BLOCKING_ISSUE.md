# PostgreSQL Persistence Blocking Issue - Tree of Thoughts Testing

## Issue Summary

When trying to test the Tree of Thoughts implementation, ALL tests are blocked by a PostgreSQL persistence error. The error occurs when SimpleAgentV3 tries to save state to PostgreSQL, but the database requires a `user_id` that isn't being provided.

## Error Details

```
psycopg.errors.NotNullViolation: null value in column "user_id" of relation "threads" violates not-null constraint
DETAIL: Failing row contains (01932e5a-1c5e-7b62-9ddb-8b3e8c0e9c4e, null, {}, 2025-07-28 04:56:20.862266, 2025-07-28 04:56:20.862266).
```

## Root Cause Analysis

### 1. PostgreSQL Schema Requirement

The PostgreSQL threads table has a NOT NULL constraint on the `user_id` column:

```sql
CREATE TABLE threads (
    thread_id uuid PRIMARY KEY,
    user_id uuid NOT NULL,  -- This is causing the issue
    metadata jsonb,
    created_at timestamp,
    updated_at timestamp
);
```

### 2. Code Location

The error occurs in:

```
/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/persistence/postgres_saver_with_thread_creation.py
```

At line 166, where it tries to insert a thread record:

```python
cursor.execute(
    "INSERT INTO threads (thread_id, user_id, metadata, created_at, updated_at) VALUES (%s, %s, %s, %s, %s)",
    (thread_id, user_id, metadata, created_at, updated_at)  # user_id is None
)
```

### 3. Call Stack Analysis

The issue propagates through this chain:

1. **Test File**: `test_candidate_generator.py` creates a `SimpleAgentV3`
2. **SimpleAgentV3**: Initializes with persistence enabled
3. **Persistence System**: Tries to create a thread in PostgreSQL
4. **Database**: Rejects the insert due to NULL `user_id`

## Impact Assessment

### Critical Impact

- **ALL Tree of Thoughts tests are blocked**
- **Cannot test CandidateGenerator agents**
- **Cannot test SolutionScorer agents**
- **Blocks development of reasoning agents**

### Affected Components

- `SimpleAgentV3` (all instances)
- Tree of Thoughts implementation
- Any agent that uses PostgreSQL persistence
- Integration tests for multi-agent workflows

## Technical Investigation

### PostgreSQL Import Issue (RESOLVED)

Initially, there was also an import issue that prevented PostgreSQL persistence from loading:

```python
# WRONG (was causing import failure)
from core.persistence.postgres_config import PostgresCheckpointerConfig

# FIXED
from haive.core.persistence.postgres_config import PostgresCheckpointerConfig
```

This has been resolved, and PostgreSQL persistence now loads correctly.

### User ID Context Problem (ACTIVE ISSUE)

The core issue is that the persistence system doesn't have access to a valid `user_id`:

```python
# In postgres_saver_with_thread_creation.py
def create_thread(self, thread_id: str, user_id: Optional[str] = None) -> None:
    # user_id comes in as None
    # But database requires NOT NULL
    # This causes the constraint violation
```

## Proposed Solutions

### Solution 1: Default User ID (Quick Fix)

Add a default user ID when none is provided:

```python
def create_thread(self, thread_id: str, user_id: Optional[str] = None) -> None:
    if user_id is None:
        user_id = "default-user"  # or generate a UUID

    # Continue with insertion
```

### Solution 2: Test-Specific User ID (Recommended)

Modify the test setup to provide a user_id:

```python
# In test files
def create_candidate_generator(expansion_count: int = 5, temperature: float = 0.7) -> SimpleAgentV3:
    engine = AugLLMConfig(
        temperature=temperature,
        structured_output_model=CandidateGeneration,
        # Add persistence config with user_id
        persistence_config={
            "user_id": "test-user-001",
            "thread_id": f"test-thread-{uuid.uuid4()}"
        }
    )
    return SimpleAgentV3(name="candidate_generator", engine=engine)
```

### Solution 3: Make user_id Optional in Schema (Database Change)

Modify the PostgreSQL schema to allow NULL user_id:

```sql
ALTER TABLE threads ALTER COLUMN user_id DROP NOT NULL;
```

### Solution 4: Skip Persistence in Tests (Test-Only Fix)

Disable persistence for testing:

```python
# In test configuration
engine = AugLLMConfig(
    temperature=temperature,
    structured_output_model=CandidateGeneration,
    enable_persistence=False  # Skip PostgreSQL for tests
)
```

## Recommended Implementation Plan

### Phase 1: Immediate Fix (1 hour)

1. **Implement Solution 2**: Add test-specific user_id to all ToT tests
2. **Verify fix**: Run `test_candidate_generator.py` successfully
3. **Test other components**: Ensure no regressions

### Phase 2: Robust Solution (2-4 hours)

1. **Review persistence architecture**: Understand user_id requirements
2. **Design user context system**: How should user_id be provided?
3. **Implement proper user context**: Thread-local or dependency injection
4. **Update all affected code paths**

### Phase 3: Testing & Validation (1 hour)

1. **Run full ToT test suite**
2. **Run PostgreSQL persistence tests**
3. **Verify multi-agent workflows work**
4. **Document user_id requirements**

## Files That Need Changes

### High Priority (Immediate Fix)

1. `packages/haive-agents/tests/reasoning_and_critique/tot/agents/test_candidate_generator.py`
2. Any other ToT test files that create agents
3. `packages/haive-core/src/haive/core/persistence/postgres_saver_with_thread_creation.py`

### Medium Priority (Robust Solution)

1. `packages/haive-core/src/haive/core/engine/aug_llm.py` (if user context added)
2. `packages/haive-agents/src/haive/agents/simple/agent_v3.py` (user context integration)
3. All test configuration files

## Testing Strategy

### Before Fix

```bash
# This fails with user_id constraint violation
cd packages/haive-agents
poetry run python tests/reasoning_and_critique/tot/agents/test_candidate_generator.py
```

### After Fix

```bash
# This should pass
cd packages/haive-agents
poetry run python tests/reasoning_and_critique/tot/agents/test_candidate_generator.py

# Verify no PostgreSQL fallback warnings
# Should see: PostgreSQL persistence working correctly
# Should NOT see: "falling back to memory store"
```

### Integration Test

```bash
# Run full test suite to ensure no regressions
poetry run pytest packages/haive-agents/tests/reasoning_and_critique/tot/ -v
```

## Success Criteria

1. ✅ **PostgreSQL import working** (already fixed)
2. ⏳ **Tree of Thoughts tests pass** (needs user_id fix)
3. ⏳ **No constraint violations** (needs user_id fix)
4. ⏳ **Persistence saves correctly** (needs user_id fix)
5. ⏳ **All ToT components testable** (needs user_id fix)

## Next Steps

1. **Choose solution approach** (recommend Solution 2 for quick fix)
2. **Implement user_id provision** in test setup
3. **Test with real ToT workflow**
4. **Document user_id requirements** for future developers
5. **Consider long-term user context architecture**

## Additional Context

This issue represents a broader architectural question: **How should user context be provided to agents?** The current implementation assumes a user_id will always be available, but test environments and some use cases may not have clear user context.

Consider whether the system should:

- Always require explicit user_id
- Support anonymous/default users
- Use session-based user identification
- Allow user_id to be optional in some contexts

Resolving this will improve both the testing experience and the overall architecture of the persistence system.
