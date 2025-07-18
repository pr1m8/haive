# Debugging SimpleAgent Schema Issues

**Memory Tag**: [MEM-101-M]
**Parent**: [MEM-101] Schema Analysis
**Date**: 2025-01-06
**Status**: Investigating

## 🎯 Problem

User reported that `simple_agent.state_schema.engine` doesn't exist, but `simple_agent.state_schema.engines` does work. Need to understand why the `engine` field is missing.

## 🔍 Observations

From notebook `Untitled72.ipynb`:

1. **ReactAgent**: Has `engines_by_type` working properly
2. **SimpleAgent**: Missing `engine` field, but `engines` seems to work

## 🧐 Investigation Steps

### 1. Schema Composer Condition

Found issue in SchemaComposer line 1955:

```python
# Old (too restrictive)
if self.engines and hasattr(base_class, '__module__') and 'state_schema' in base_class.__module__:

# Fixed
if self.engines and issubclass(base_class, StateSchema):
```

### 2. MessagesState Validator Issue

Fixed MessagesState validator:

```python
# Fixed: Return self instead of instance
return self  # was: return instance
```

### 3. Added Convenience Properties

Added to StateSchema:

```python
@property
def llm(self) -> Optional["Engine"]:
    """Convenience property to access the LLM engine."""

@property
def main_engine(self) -> Optional["Engine"]:
    """Convenience property to access the main engine."""
```

## 🔧 Root Cause Analysis

The issue appears to be that:

1. SimpleAgent creates engine in `setup_agent()`
2. Parent Agent class calls `_setup_schemas()`
3. SchemaComposer builds schema with engines
4. But the condition for adding engine management was too restrictive

## 📝 Expected Results After Fix

After the fixes, SimpleAgent state schema should have:

- `engine` field (Optional[Engine])
- `engines` field (Dict[str, Any])
- Convenience properties: `llm`, `main_engine`
- Class-level engines and engines_by_type

## 🧪 Debug Script

Created debug output in notebook to check:

- Agent engine/engines values
- Schema field definitions
- State instance field availability
- Class-level engine attributes

---

**Next**: Run debug script to verify fixes worked
