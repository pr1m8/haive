# State Schema and Engine Refactoring Plan

## Current Issues

### 1. Engine Type System

- Engines are not properly generic (no type parameters for state)
- Field definitions are loosely coupled to actual state schemas
- No compile-time guarantees between engine I/O and state fields

### 2. Schema Composition

- SchemaComposer works but doesn't leverage type information
- Multi-agent schema composition is fragile
- No clear separation between shared and private fields

### 3. Multi-Agent Challenges

- State isolation between agents is not well defined
- Schema composition for SequentialAgent creates conflicts
- No clear pattern for parent-child state relationships

## Proposed Architecture

### 1. Generic Engine System

```python
# Make engines generic over their state type
class Engine(ABC, BaseModel, Generic[TState, TIn, TOut]):
    """Engine that knows its state schema type."""

    # Type-safe field definitions
    def get_input_fields(self) -> Dict[str, FieldDefinition[TState]]:
        """Return fields that must exist in TState."""
        pass

    def get_output_fields(self) -> Dict[str, FieldDefinition[TState]]:
        """Return fields this engine will write to TState."""
        pass
```

### 2. Registry Integration

```python
# Registry items with full type information
@dataclass
class EngineRegistryItem(Generic[TState]):
    engine_class: Type[Engine[TState, Any, Any]]
    state_requirements: Type[TState]
    field_definitions: List[FieldDefinition]
    metadata: Dict[str, Any]
```

### 3. Multi-Agent State Architecture

```python
# Clear separation of concerns
class MultiAgentState(BaseModel):
    # Shared fields accessible by all agents
    shared: SharedState

    # Private agent states
    agent_states: Dict[str, AgentPrivateState]

    # Meta information
    meta: MetaState

    # Parent-child relationships
    hierarchy: StateHierarchy
```

## Implementation Phases

### Phase 1: Engine Generics (Backward Compatible)

1. Add optional generic parameters to Engine base
2. Create migration path for existing engines
3. Add type-safe field definition methods
4. Maintain current get_input_fields/get_output_fields

### Phase 2: Enhanced Schema Composer

1. Create TypedSchemaComposer that uses generic information
2. Add compile-time validation of field compatibility
3. Better handling of shared vs private fields
4. Improved multi-agent composition

### Phase 3: Registry Enhancement

1. Add type information to registry entries
2. Create EngineRegistryItem with full metadata
3. Enable discovery based on state requirements
4. Better integration with prebuilt schemas

### Phase 4: Multi-Agent Refactor

1. Implement hierarchical state management
2. Clear parent-child state relationships
3. Better isolation of agent-private state
4. Improved message passing between agents

## Backward Compatibility Strategy

### 1. Gradual Migration

- Keep existing Engine class working as-is
- Add new TypedEngine as alternative
- Provide migration utilities
- Deprecate old patterns over time

### 2. Adapter Pattern

```python
class LegacyEngineAdapter(TypedEngine[Any, Any, Any]):
    """Adapts old engines to new type system."""
    def __init__(self, legacy_engine: Engine):
        self.legacy = legacy_engine
```

### 3. Schema Evolution

- Version schemas with migration paths
- Support both old and new patterns
- Provide clear upgrade documentation

## Multi-Agent Considerations

### 1. State Isolation Patterns

- **Shared State**: Messages, context, meta
- **Private State**: Agent-specific working memory
- **Hierarchical State**: Parent access to child summaries

### 2. Schema Composition Rules

- Explicit field ownership (which agent owns which field)
- Conflict resolution strategies
- Clear reducer patterns for shared fields

### 3. Prebuilt Integration

- Prebuilt schemas as first-class citizens
- Auto-discovery and registration
- Composition with custom schemas

## Risk Assessment

### High Risk

- Breaking existing agents
- Performance impact of additional type checking
- Complexity increase for simple use cases

### Medium Risk

- Migration effort for existing codebases
- Learning curve for new patterns
- Registry compatibility

### Low Risk

- Type safety improvements
- Better IDE support
- Clearer architecture

## Next Steps

1. **Prototype**: Create proof-of-concept for generic engines
2. **Test**: Validate with existing agents
3. **Benchmark**: Ensure no performance regression
4. **Document**: Create migration guide
5. **Implement**: Phase-by-phase rollout
