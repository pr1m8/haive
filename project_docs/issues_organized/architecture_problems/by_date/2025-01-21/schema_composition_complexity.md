# Schema Composition Complexity

**Date Discovered**: 2025-01-21 (ongoing issue)
**Priority**: Critical
**Status**: Active
**Package(s)**: haive-core

## Problem Description

The current schema composition system is overly complex, making it difficult to:

- Create new agent types
- Understand state flow between components
- Debug schema-related issues
- Extend existing schemas

## Impact

### Developer Experience

- **High Learning Curve**: New developers struggle with schema patterns
- **Development Speed**: Simple agent creation takes excessive time
- **Debugging Difficulty**: Schema errors are hard to trace and fix

### System Reliability

- **Runtime Errors**: Schema mismatches cause failures
- **Type Safety**: Weak type checking due to complex inheritance
- **Maintainability**: Changes to base schemas break dependent code

## Root Cause Analysis

### Historical Evolution

1. **Multiple Schema Systems**: Different approaches evolved independently
2. **Inheritance Overuse**: Deep inheritance hierarchies instead of composition
3. **Missing Abstraction**: No clear separation between schema concerns

### Specific Issues

1. **StateSchema Complexity**: Too many responsibilities in base class
2. **Field Flattening**: Schema composition loses type information
3. **Dynamic Composition**: Runtime schema building is error-prone

## Current Architecture Problems

### Schema Inheritance Chain

```python
# Current (problematic)
StateSchema -> MessagesState -> AgentState -> SpecificAgentState
```

**Problems:**

- Deep inheritance makes changes risky
- Field conflicts between levels
- Difficult to understand which fields come from where

### Field Composition Issues

```python
# Current (flattening problem)
composed_schema = compose_schemas([SchemaA, SchemaB])
# Result: Loses type information, field conflicts
```

## Proposed Solution: MetaStateSchema Pattern

### Key Innovation

Instead of complex inheritance, use **projection-based state containers**.

```python
class MetaStateSchema(StateSchema):
    # Shared state
    messages: List[BaseMessage]
    shared_context: Dict[str, Any]

    # Agent states (typed but stored as dicts)
    agent_states: Dict[str, Dict[str, Any]]
    agent_schemas: Dict[str, Type[StateSchema]]

    def get_agent_view(self, agent_name: str) -> AgentStateView:
        """Get type-safe projection for specific agent."""
```

### Benefits

1. **Type Safety**: Each agent gets typed view of its state
2. **Isolation**: Agent states don't interfere with each other
3. **Simplicity**: No complex inheritance chains
4. **Debuggability**: Clear state ownership and boundaries

## Implementation Progress

### Completed (2025-01-15)

- ✅ **MetaStateSchema Design**: Complete pattern documented
- ✅ **Basic Implementation**: Working proof of concept
- ✅ **Testing**: Validated with real LLM execution

### In Progress (2025-01-21)

- 🔄 **Multi-Agent Integration**: Sequential execution patterns
- 🔄 **Documentation**: Usage guides and examples
- 🔄 **Migration Plan**: Strategy for existing code

### Planned

- ⏳ **Performance Optimization**: Efficient state projections
- ⏳ **Advanced Patterns**: Dynamic schema composition
- ⏳ **Tooling**: Developer experience improvements

## Migration Strategy

### Phase 1: New Code

- All new agents use MetaStateSchema pattern
- Create templates and examples
- Document best practices

### Phase 2: Critical Paths

- Migrate most-used agent types
- Update core framework components
- Maintain backward compatibility

### Phase 3: Full Migration

- Convert remaining legacy code
- Remove deprecated patterns
- Simplify codebase

## Success Metrics

### Developer Experience

- **Agent Creation**: <10 lines for new agent with state
- **Learning Curve**: New developers productive in <1 day
- **Documentation**: Clear examples for all patterns

### Technical Quality

- **Type Safety**: 100% type checking on state access
- **Performance**: <1ms overhead for state projections
- **Reliability**: Zero schema-related runtime errors

## Related Issues

- **Multi-Agent Coordination**: Needs simplified state sharing
- **Performance**: Current patterns have overhead
- **Testing**: Complex schemas make testing difficult

## Resolution Notes

**2025-01-15**: MetaStateSchema pattern designed and tested with real components.
**2025-01-21**: Multi-agent sequential pattern in development.

_Continued updates as implementation progresses_
