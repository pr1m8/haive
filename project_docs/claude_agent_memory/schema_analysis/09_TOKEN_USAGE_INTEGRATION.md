# Token Usage Integration

**Memory Tag**: [MEM-101-I]  
**Parent**: [MEM-101] Schema Analysis  
**Date**: 2025-01-06  
**Status**: Completed

## 🎯 What We've Implemented

### 1. Token Usage Core Schema

Created `token_usage.py` with:

- `TokenUsage` dataclass with comprehensive metrics
- Support for input/output/total tokens
- Advanced token types (cached, audio, reasoning)
- Cost calculation with provider pricing
- Capacity percentage tracking
- Helper functions for extraction and aggregation

### 2. Token Usage Mixin

Created `token_usage_mixin.py` with:

- `TokenUsageMixin` for adding token tracking to any schema
- Automatic token extraction from messages
- Token usage history tracking
- Cost calculation methods
- Usage statistics and summaries
- Capacity status reporting

### 3. MessagesStateWithTokenUsage

Created `messages_with_token_usage.py` with:

- Prebuilt schema combining MessagesState + TokenUsageMixin
- Automatic token tracking on message addition
- Conversation cost analysis
- Enhanced usage reporting

### 4. SchemaComposer Enhancement

Added to `schema_composer.py`:

- `add_engine_management()` method
- Automatic engine management for schemas with engines
- Support for optional `engine` field
- Explicit `engines` dict field
- Maintains backward compatibility

## 📋 Integration Pattern

### Using the Mixin

```python
from haive.core.schema import MessagesState, TokenUsageMixin

class MyMessagesState(MessagesState, TokenUsageMixin):
    """Custom state with token tracking."""
    pass
```

### Using the Prebuilt

```python
from haive.core.schema import MessagesStateWithTokenUsage

# Direct usage
state = MessagesStateWithTokenUsage()
state.add_message(ai_message)

# Get usage info
summary = state.get_token_usage_summary()
print(f"Total tokens: {summary['total_tokens']}")
print(f"Total cost: ${summary['total_cost']:.4f}")
```

### Cost Calculation

```python
# Calculate costs with provider pricing
state.calculate_costs(
    input_cost_per_1k=0.003,   # $0.003 per 1k input tokens
    output_cost_per_1k=0.015,  # $0.015 per 1k output tokens
    cached_input_cost_per_1k=0.0015  # Optional cached pricing
)
```

## 🔄 Engine Management Pattern

The SchemaComposer now automatically adds engine management fields when engines are detected:

```python
composer = SchemaComposer("MyState")
composer.add_fields_from_components([my_engine])

# Automatically gets:
# - engine: Optional[Engine] field
# - engines: Dict[str, Any] field
# - Synchronization between them

# Or manually add:
composer.add_engine_management()
```

## ✅ Export Updates

Updated `__init__.py` files to export:

- TokenUsage and helper functions
- TokenUsageMixin
- MessagesStateWithTokenUsage

## 🧪 Next Steps

1. Test with existing agents
2. Add token usage to agent examples
3. Consider adding to BasicAgentState
4. Update documentation

---

**Status**: TokenUsage integration complete, SchemaComposer enhanced
