# Agent Base Update Plan

**Memory Tag**: [MEM-101-K]  
**Parent**: [MEM-101] Schema Analysis  
**Date**: 2025-01-06  
**Status**: Planning

## 🎯 Issues to Address

### 1. Engine Management Confusion

- Agent has both `engine` and `engines` fields (duplicating StateSchema pattern)
- Schema generation doesn't leverage new engine management
- No use of the new `add_engine_management()` method

### 2. Schema Generation Issues

- Uses `SchemaComposer.from_components()` class method
- Doesn't leverage the new engine management features
- No token usage tracking integration
- Doesn't use the enhanced SchemaComposer properly

### 3. Complex Schema Setup

- `_setup_schemas()` method is overly complex
- Tries to handle too many edge cases
- Doesn't use the new prebuilt schemas effectively

### 4. Backward Compatibility

- Need to ensure existing agents continue to work
- Gradual migration path to new patterns

## 📋 Proposed Changes

### 1. Simplify Engine Fields

```python
# Remove duplicate engine/engines from Agent
# Let StateSchema handle this through schema generation
```

### 2. Update Schema Generation

```python
def _setup_schemas(self) -> None:
    """Generate schemas using enhanced SchemaComposer."""
    if not self.state_schema:
        # Create composer instance
        composer = SchemaComposer(name=f"{self.__class__.__name__}State")

        # Add engines
        if self.engine:
            composer.add_engine(self.engine)
        for name, engine in self.engines.items():
            composer.add_engine(engine)

        # Let composer detect and add engine management
        # This will add engine/engines fields automatically

        # Build schema
        self.state_schema = composer.build()
```

### 3. Add Token Usage Support

```python
# Option 1: Use MessagesStateWithTokenUsage as default
# Option 2: Add TokenUsageMixin dynamically
# Option 3: Let user choose via configuration
```

### 4. Cleaner I/O Schema Derivation

```python
# Use StateSchema's built-in methods better
# Leverage the enhanced field extraction
```

## 🔄 Migration Strategy

1. **Phase 1**: Update SchemaComposer usage
2. **Phase 2**: Remove duplicate engine fields
3. **Phase 3**: Add token usage support
4. **Phase 4**: Simplify I/O schema generation

## ✅ Benefits

1. Cleaner code with less duplication
2. Automatic engine management
3. Token usage tracking out of the box
4. Better integration with schema system
5. Easier to understand and maintain

---

**Next**: Implement changes incrementally
