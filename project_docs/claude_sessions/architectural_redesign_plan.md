# Haive Architecture Redesign Plan

**Date**: 2025-01-09  
**Status**: Planning Phase  
**Goal**: Redesign state schema and schema composer to fix engine typing issues and enable dynamic workflows

## Current Problems Identified

### 1. Engine Typing Issues

- `engines: Dict[str, Engine]` causes "Can't instantiate abstract class Engine" errors
- Serialization/deserialization breaks because Engine is abstract
- Type safety is lost with current approach

### 2. Schema Composer Limitations

- Doing too much in one place
- Hard to extend or modify
- AgentSchemaComposer vs SchemaComposer separation unclear
- No clear taxonomy of responsibilities

### 3. State Schema Rigidity

- Can't easily add engine I/O fields to existing schemas
- No clean way to compose with different base schemas
- Engine fields are hardcoded rather than dynamic

### 4. Node Adaptation Missing

- No systematic way to handle schema mismatches
- Nodes don't intelligently adapt between incompatible I/O
- No conversion system for structured outputs

## Proposed Architecture

### 1. Generic Component Management System

```python
# Protocol for named components
class NamedComponent(Protocol):
    name: str

# Generic mixin for managing collections
class ComponentManager(Generic[T], BaseModel):
    components: Dict[str, T] = Field(default_factory=dict)

    def add_component(self, component: T) -> None
    def get_component(self, name: str) -> Optional[T]
    def remove_component(self, name: str) -> bool
```

**Applications:**

- `EngineManager(ComponentManager[Engine])` for engine collections
- `AgentManager(ComponentManager[Agent])` for multi-agent systems
- Natural analogue between engines and agents

### 2. Smart Schema Composer Redesign

**Core Philosophy**: Schema composer becomes intelligent factory that:

- Analyzes actual components passed to it
- Resolves generics based on concrete types
- Merges engine I/O fields with base schemas
- Handles field conflicts intelligently

**Key Features:**

```python
# Enhanced composition with engine I/O
StateSchema.from_engines(
    engines={"llm": aug_llm, "retriever": retriever},
    base_schema=MyTaskState,  # your desired base
    add_io_fields=True,       # auto-add engine I/O fields
    add_hooks=True,           # pre/post processing hooks
    resolve_generics=True     # make concrete types
)

# Result: MyTaskState + engine I/O fields + resolved generics
```

### 3. Node Adaptation Layer

**Nodes as Intelligent Adapters:**

- Wrap engines and handle execution
- Transform engine outputs to state updates
- Handle schema mismatches through conversion
- Support pre/post processing hooks

**Capabilities:**

- Type conversion (str → List[str], dict → Pydantic model)
- Schema adaptation (TaskResult → Summary)
- Output routing (same engine output to multiple fields)
- Dynamic field mapping

### 4. Dynamic Graph Modification

**Meta-State Concept:**

- Track graph structure in state
- Enable runtime node addition/removal
- Support graph recompilation
- Handle schema adaptation when graph changes

**Use Cases:**

- Add validation node after retrieval
- Insert summarization step in workflow
- Compose multi-agent workflows dynamically
- Runtime optimization of agent graphs

## Implementation Strategy

### Phase 1: Foundation (Current Focus)

1. **Fix immediate engine typing issue**
   - Implement generic ComponentManager system
   - Update schema composer to resolve generics intelligently
   - Test with existing SimpleAgent and multi-agent systems

2. **Schema Composer Refactoring**
   - Break down into specialized composers
   - Add engine I/O field integration
   - Implement smart base schema selection

### Phase 2: Node Intelligence

1. **Node Adaptation Layer**
   - Design conversion system for structured outputs
   - Implement schema compatibility checking
   - Add pre/post processing hooks

2. **Dynamic Capabilities**
   - Meta-state implementation
   - Runtime graph modification
   - Schema adaptation for graph changes

### Phase 3: Advanced Features

1. **Token-based Messages**
   - LLM-specific token representations
   - Private message filtering per engine
   - Prebuilt system integration

2. **Multi-Agent Enhancements**
   - Agent I/O compatibility analysis
   - Automatic adapter insertion
   - Workflow optimization

## Key Design Decisions

### 1. Engines Stay in State

- **Rationale**: Needed for dynamic graph modification and meta-state operations
- **Challenge**: Handle serialization without abstract type issues
- **Solution**: Smart generic resolution by schema composer

### 2. Nodes as Adaptation Layer

- **Rationale**: Flexibility to handle mismatched schemas
- **Challenge**: Maintain type safety while being adaptive
- **Solution**: Conversion protocols and compatibility checking

### 3. Compositional Design

- **Rationale**: Mix and match base schemas with engine capabilities
- **Challenge**: Avoid breaking existing code
- **Solution**: Enhanced composition, not replacement

### 4. Generic Component Management

- **Rationale**: Consistent patterns for engines and agents
- **Challenge**: Type safety with generics
- **Solution**: Protocol-based approach with runtime resolution

## Open Questions

1. **Backward Compatibility**: How to migrate existing agents without breaking changes?
2. **Performance**: Will dynamic schema generation impact performance?
3. **Type Safety**: How to maintain type safety with dynamic adaptation?
4. **Testing**: How to test dynamic graph modification effectively?
5. **Documentation**: How to document the new patterns clearly?

## Next Steps

1. **Create prototype** of ComponentManager system
2. **Test generic resolution** with schema composer
3. **Validate approach** with SimpleAgent and SequentialAgent
4. **Document patterns** for other developers
5. **Plan migration strategy** for existing code

## Success Criteria

- [ ] SequentialAgent runs without engine typing errors
- [ ] Schema composer can enhance existing schemas with engine I/O
- [ ] Nodes can adapt between incompatible schemas
- [ ] Dynamic graph modification works with meta-state
- [ ] Backward compatibility maintained
- [ ] Performance is acceptable
- [ ] Code is cleaner and more maintainable
