# Final Schema Module Structure

**Memory Tag**: [MEM-101-J]  
**Parent**: [MEM-101] Schema Analysis  
**Date**: 2025-01-06  
**Status**: Completed

## 📁 Module Organization

### Schema Package Structure

```
haive/core/schema/
├── __init__.py                    # Main schema exports
├── state_schema.py                # Base StateSchema with engine management
├── schema_composer.py             # Enhanced with add_engine_management()
├── field_definition.py            # Field metadata and configuration
├── field_extractor.py             # Component field extraction
├── field_utils.py                 # Field manipulation utilities
├── multi_agent_state_schema.py    # Multi-agent state support
├── agent_schema_composer.py       # Agent-specific composer
├── schema_manager.py              # Runtime schema manipulation
├── preserve_messages_reducer.py   # Message preservation utility
├── ui.py                          # Rich UI components
└── prebuilt/                      # Ready-to-use schemas
    ├── __init__.py                # Prebuilt exports
    ├── basic_agent_state.py       # Simple agent state
    ├── messages_state.py          # Core conversation state
    ├── tool_state.py              # State with tool management
    ├── multi_agent_state.py       # Multi-agent architecture
    └── messages/                  # Messages module
        ├── __init__.py            # Messages submodule exports
        ├── token_usage.py         # TokenUsage model & functions
        ├── token_usage_mixin.py   # TokenUsageMixin for any schema
        ├── messages_with_token_usage.py  # Combined prebuilt
        ├── compatibility.py       # Enhanced features adapter
        └── utils.py               # Message utilities
```

## 🔧 Key Enhancements

### 1. StateSchema Base Class

- Added optional `engine` field for primary engine
- Added explicit `engines` dict field
- Added `sync_engine_fields()` validator
- Maintains full backward compatibility

### 2. SchemaComposer

- Added `add_engine_management()` method
- Auto-adds engine fields when engines detected
- Cleaner engine management pattern

### 3. Messages Module

Organized token usage and message utilities:

- `TokenUsage`: Comprehensive token tracking
- `TokenUsageMixin`: Add tracking to any schema
- `MessagesStateWithTokenUsage`: Ready-to-use combination
- Future: Enhanced message utilities

## 📦 Import Examples

### Basic Usage

```python
from haive.core.schema import StateSchema, SchemaComposer
from haive.core.schema.prebuilt import MessagesState, ToolState
```

### Token Usage

```python
from haive.core.schema.prebuilt.messages import (
    TokenUsage,
    TokenUsageMixin,
    MessagesStateWithTokenUsage,
    calculate_token_cost
)
```

### Creating Custom States

```python
# With mixin
from haive.core.schema import MessagesState
from haive.core.schema.prebuilt.messages import TokenUsageMixin

class MyState(MessagesState, TokenUsageMixin):
    custom_field: str = "default"

# With composer
composer = SchemaComposer("MyState")
composer.add_engine_management()  # Adds engine fields
composer.add_fields_from_components([my_engine])
MyState = composer.build()
```

## ✅ Benefits

1. **Cleaner Organization**: Token usage grouped with messages
2. **Modular Design**: Easy to extend with new utilities
3. **Backward Compatible**: All existing code continues to work
4. **Future Ready**: Messages module can grow with new features

## 🚀 Next Steps

1. Test with existing agents
2. Add more message utilities as needed
3. Consider similar organization for tool utilities
4. Update documentation and examples

---

**Status**: Module reorganization complete
