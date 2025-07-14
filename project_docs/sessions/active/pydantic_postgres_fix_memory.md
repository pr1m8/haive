# Pydantic PostgreSQL Serialization Fix - Memory Guide

**Date**: 2025-01-14  
**Status**: ✅ Fixed, Tested, and Cleaned Up  
**Impact**: Critical - Enables PostgreSQL persistence with Pydantic models

## 🎯 Quick Summary

Fixed `TypeError: Object of type X is not JSON serializable` when using LangGraph with PostgreSQL persistence and Pydantic models. Solution: Configure psycopg connections to use a Pydantic-aware JSON encoder.

## 🚨 The Problem

When using SimpleAgentV2 with structured output (Pydantic models):
```python
TypeError: Object of type Simple Agent V2Input is not JSON serializable
```

### Root Cause
1. LangGraph stores raw Pydantic models in checkpoint metadata's `writes["__start__"]`
2. PostgreSQL uses JSONB columns for metadata storage
3. psycopg uses Python's standard `json.dumps()` which doesn't handle Pydantic models
4. The serialization chain breaks when psycopg tries to save the metadata

## ✅ The Solution

Configure psycopg connections to handle Pydantic models:

```python
# In postgres_saver_override.py
def pydantic_aware_json_dumps(obj):
    """JSON encoder that handles Pydantic models."""
    class PydanticEncoder(json.JSONEncoder):
        def default(self, o):
            if isinstance(o, BaseModel):
                return o.model_dump()
            return super().default(o)
    
    return json.dumps(obj, cls=PydanticEncoder)

def configure_postgres_json(connection):
    """Configure a PostgreSQL connection for Pydantic."""
    from psycopg.types.json import set_json_dumps
    set_json_dumps(pydantic_aware_json_dumps, context=connection)

# In postgres_config.py - configure each connection in the pool
pool = ConnectionPool(
    conninfo=connection_uri,
    configure=configure_postgres_json,  # ← The key fix!
    # ... other params
)
```

## 📍 Implementation Locations

### Core Utilities
**File**: `/packages/haive-core/src/haive/core/persistence/postgres_saver_override.py`
- `pydantic_aware_json_dumps()` - The JSON encoder
- `configure_postgres_json()` - Helper to configure connections
- Minimal override classes for backward compatibility

### Connection Pool Configuration
**File**: `/packages/haive-core/src/haive/core/persistence/postgres_config.py`
- Added `configure=configure_postgres_json` to ConnectionPool creation
- Applied to both sync and async pools
- Ensures every connection in the pool handles Pydantic models

## 🧪 Testing

Verified with `test_basic.py`:
```bash
poetry run pytest packages/haive-agents/tests/test_basic.py -v
```

Results:
- ✅ No serialization errors
- ✅ SimpleAgentV2 works with structured output
- ✅ PostgreSQL persistence saves checkpoints correctly
- ✅ State history can be retrieved

## 🔑 Key Insights

1. **Pydantic has native JSON serialization** - We just needed to connect it to psycopg
2. **Simple solutions are better** - One-line fix vs complex workarounds
3. **Fix at the right layer** - JSON encoding, not checkpoint serialization

## ⚠️ Important Notes

1. **Connection-specific** - Must be set on each connection/pool
2. **Both sync and async** - Applied to both saver versions
3. **No performance impact** - Only affects JSON encoding
4. **Preserves functionality** - Doesn't change agent behavior

## 🚫 What NOT to Do

- Don't modify SecureSecretStrSerializer for Pydantic handling
- Don't try to intercept metadata before saving
- Don't convert models to dicts in agent execution
- Don't create complex PostgresSaver overrides

## 📚 References

- [psycopg3 JSON adaptation](https://www.psycopg.org/psycopg3/docs/api/types.html#json-adaptation)
- [Pydantic JSON serialization](https://docs.pydantic.dev/latest/concepts/json/)
- [LangGraph checkpoint metadata](https://langchain-ai.github.io/langgraph/reference/checkpoints/)

## 🔄 Future Considerations

1. **Alternative location** - Could also be set in `postgres_config.py` when creating pools
2. **Custom serializers** - Might want field-level control in future
3. **Performance optimization** - Consider caching encoder instances

## 💡 Lessons Learned

The error message "not JSON serializable" led us down a complex path of trying to fix it in the checkpoint serialization layer. The real issue was simply that psycopg didn't know about Pydantic's built-in serialization. Sometimes the simplest solution is the right one.

---

**Remember**: When you see serialization errors, check if the types already have serialization methods before building complex workarounds!