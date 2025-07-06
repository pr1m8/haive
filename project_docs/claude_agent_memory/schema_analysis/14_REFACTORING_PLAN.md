# File Size Refactoring Plan

**Memory Tag**: [MEM-101-N]  
**Parent**: [MEM-101] Schema Analysis  
**Date**: 2025-01-06  
**Status**: Planning

## 📊 Current File Sizes

- `state_schema.py`: 2,236 lines (HUGE!)
- `schema_composer.py`: 3,174 lines (MASSIVE!)
- `agent.py`: 1,534 lines (Large)
- `simple/agent.py`: 478 lines (Reasonable)

## 🎯 Refactoring Strategy

### 1. StateSchema (2,236 lines → ~300 lines)

**Current Responsibilities:**

- Base model with engine fields
- Field sharing logic
- Reducer management
- Engine I/O tracking
- Message handling
- Serialization methods
- State manipulation
- Visualization methods

**Proposed Mixins:**

```
StateSchema (base: ~150 lines)
├── EngineManagementMixin (~100 lines)
├── FieldSharingMixin (~150 lines)
├── SerializationMixin (~200 lines)
├── StateManipulationMixin (~300 lines)
├── MessageHandlingMixin (~400 lines)
└── VisualizationMixin (~600 lines)
```

### 2. SchemaComposer (3,174 lines → ~400 lines)

**Current Responsibilities:**

- Field extraction from components
- Engine management
- Base class detection
- Schema building
- Tool synchronization
- Visualization
- Complex field processing

**Proposed Structure:**

```
SchemaComposer (core: ~400 lines)
├── ComponentExtractorMixin (~500 lines)
├── EngineComposerMixin (~300 lines)
├── FieldComposerMixin (~600 lines)
├── SchemaBuilderMixin (~400 lines)
├── ToolSyncMixin (~300 lines)
└── ComposerVisualizationMixin (~500 lines)
```

### 3. Agent (1,534 lines → ~300 lines)

**Current Responsibilities:**

- Engine management
- Schema generation
- Graph building
- Persistence setup
- I/O schema derivation
- Complex validation

**Proposed Structure:**

```
Agent (core: ~300 lines)
├── AgentSchemaMixin (~400 lines)
├── AgentPersistenceMixin (~300 lines)
├── AgentExecutionMixin (~200 lines)
└── AgentValidationMixin (~300 lines)
```

## 🏗 Implementation Strategy

### Phase 1: StateSchema Refactoring

1. Create mixins for major functionality areas
2. Keep StateSchema as composition of mixins
3. Maintain all existing functionality
4. Add comprehensive tests

### Phase 2: SchemaComposer Refactoring

1. Extract component processing logic
2. Separate engine-specific logic
3. Modularize field composition
4. Split visualization code

### Phase 3: Agent Refactoring

1. Extract schema generation logic
2. Separate persistence handling
3. Modularize I/O schema logic
4. Clean up validation

## ✅ Benefits

1. **Maintainability**: Smaller, focused files
2. **Reusability**: Mixins can be used independently
3. **Testing**: Easier to test individual components
4. **Understanding**: Clearer separation of concerns
5. **Extensibility**: Easy to add new capabilities

## 🔒 Constraints

1. **Zero Breaking Changes**: All existing APIs must work
2. **Import Compatibility**: All imports must remain the same
3. **Functionality Preservation**: No feature loss
4. **Performance**: No significant performance impact

---

**Goal**: Reduce total lines from 7,422 to ~2,000 while improving maintainability
