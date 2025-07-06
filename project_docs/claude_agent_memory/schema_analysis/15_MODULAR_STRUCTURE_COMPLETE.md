# Modular Schema System Structure

**Memory Tag**: [MEM-101-O]  
**Parent**: [MEM-101] Schema Analysis  
**Date**: 2025-01-06  
**Status**: Implemented

## 📁 New Module Organization

### Core Schema Structure

```
haive/core/schema/
├── __init__.py                    # Main exports (backward compatible)
├── state_schema.py                # Original file (kept for compatibility)
├── schema_composer.py             # Original file (kept for compatibility)
│
├── composer/                      # Schema composition (NEW)
│   ├── __init__.py               # Composer exports
│   ├── schema_composer.py        # Simplified composer (~400 lines)
│   ├── engine/                   # Engine management
│   │   ├── __init__.py
│   │   ├── engine_manager.py     # Engine tracking & updates
│   │   ├── engine_detector.py    # Base class detection
│   │   └── engine_extractor.py   # Field extraction from engines
│   ├── field/                    # Field management
│   │   ├── __init__.py
│   │   ├── field_manager.py      # Field definitions & metadata
│   │   ├── field_extractor.py    # Extract from components
│   │   └── field_validator.py    # Field validation logic
│   ├── builder/                  # Schema building
│   │   ├── __init__.py
│   │   ├── schema_builder.py     # Core build logic
│   │   └── post_processor.py     # Schema post-processing
│   └── utils/                    # Utilities
│       ├── __init__.py
│       ├── visualization.py      # Rich display tools
│       └── helpers.py            # Utility functions
│
├── state/                        # State schema (NEW)
│   ├── __init__.py               # State exports
│   ├── base_state.py             # Core BaseStateSchema (~150 lines)
│   ├── engine/                   # Engine capabilities
│   │   ├── __init__.py
│   │   └── engine_state_mixin.py # Engine management for states
│   ├── serialization/            # Serialization
│   │   ├── __init__.py
│   │   └── serialization_mixin.py # JSON/dict conversion
│   ├── manipulation/             # State operations
│   │   ├── __init__.py
│   │   └── state_manipulation_mixin.py # Update/merge/diff
│   └── visualization/            # Display tools
│       ├── __init__.py
│       └── visualization_mixin.py # Rich display
│
├── agents/                       # Agent-specific (NEW)
│   ├── __init__.py               # Agent schema exports
│   ├── agent_schema_mixin.py     # Agent schema generation
│   ├── agent_persistence_mixin.py # Persistence handling
│   └── agent_validation_mixin.py  # Agent validation
│
└── prebuilt/                     # Prebuilt schemas (EXISTING)
    ├── __init__.py               # Updated exports
    ├── messages_state.py         # Enhanced with engine mgmt
    ├── tool_state.py             # Tool management
    ├── multi_agent_state.py      # Multi-agent support
    └── messages/                 # Messages utilities
        ├── __init__.py
        ├── token_usage.py        # Token tracking
        ├── token_usage_mixin.py  # Token mixin
        └── messages_with_token_usage.py # Combined schema
```

## 🎯 File Size Reduction

### Before

- `state_schema.py`: 2,236 lines
- `schema_composer.py`: 3,174 lines
- `agent.py`: 1,534 lines
- **Total**: 6,944 lines

### After (Projected)

- `composer/schema_composer.py`: ~400 lines
- `state/base_state.py`: ~150 lines
- `composer/engine/engine_manager.py`: ~200 lines
- `composer/field/field_manager.py`: ~300 lines
- `composer/engine/engine_detector.py`: ~150 lines
- **New Total**: ~1,200 lines core + mixins

## ✅ Key Benefits

### 1. **Maintainability**

- Each file has a single, clear responsibility
- Easy to find and modify specific functionality
- Reduced cognitive load when working with code

### 2. **Reusability**

- Mixins can be used independently
- Easy to compose custom schemas with specific capabilities
- Modular testing and development

### 3. **Backward Compatibility**

- All existing imports continue to work
- Original large files kept as fallbacks
- Gradual migration path available

### 4. **Extensibility**

- Easy to add new engine types via mixins
- Simple to extend field processing
- Clear patterns for new capabilities

## 🔄 Migration Strategy

### Phase 1: Core Implementation ✅

- [x] Created modular structure
- [x] Implemented EngineComposerMixin
- [x] Implemented FieldManagerMixin
- [x] Implemented EngineDetectorMixin
- [x] Created simplified SchemaComposer

### Phase 2: Complete Extraction (Next)

- [ ] Extract all field processing logic
- [ ] Create state manipulation mixins
- [ ] Extract visualization components
- [ ] Implement agent-specific mixins

### Phase 3: Testing & Validation

- [ ] Comprehensive testing of new structure
- [ ] Performance validation
- [ ] Backward compatibility verification

## 📝 Usage Examples

### Using New Modular Composer

```python
# Same API, new implementation
from haive.core.schema.composer import SchemaComposer

composer = SchemaComposer("MyState")
composer.add_engine(my_engine)
composer.add_field("custom_field", str, default="test")
schema = composer.build()
```

### Using Individual Mixins

```python
from haive.core.schema.composer.engine import EngineComposerMixin
from haive.core.schema.composer.field import FieldManagerMixin

class CustomComposer(EngineComposerMixin, FieldManagerMixin):
    # Custom composition logic
    pass
```

### Backward Compatibility

```python
# This still works exactly as before
from haive.core.schema import SchemaComposer
schema = SchemaComposer.from_components([engine1, engine2])
```

---

**Status**: Modular structure implemented, ready for complete extraction
