# Schema-Engine Refactoring Implementation Plan

## Starting Point: Engine-Node-State Triangle

The core issue is that we have three overlapping systems trying to do the same thing:

1. **Engines** - Define I/O and execution
2. **Nodes** - Map state and execute engines
3. **StateSchema** - Links engine I/O mappings

## Key Problems to Solve

### 1. Engine-Node Confusion

Currently:

```python
# Engines are executed BY nodes
class EngineNodeConfig:
    engine: Engine
    def execute(state) -> state

# But engines already have execution
class Engine:
    def run(input) -> output
```

**Solution Direction**: Nodes should BE engines or engines should BE nodes

### 2. State Mapping Duplication

Currently:

```python
# StateSchema has engine I/O mappings
class StateSchema:
    __engine_io_mappings__ = {
        'engine_name': {'input': 'state.field', 'output': 'state.other'}
    }

# But NodeConfig also maps state
class NodeConfig:
    def get_input(state) -> engine_input
    def update_state(state, output) -> state
```

**Solution Direction**: Single source of truth for state mapping

### 3. Tool System Chaos

Currently:

```python
# Tools are... everything?
Tool (base concept)
ToolEngine (executes tools?)
StructuredTool (Pydantic model as tool?)
ToolNodeConfig (minimal implementation)
tool_node() (factory function)
```

**Solution Direction**: Tools are just functions with schemas

## Proposed Refactoring Approach

### Phase 1: Create Unified Engine Concept

```python
# New unified interface
class ExecutableUnit(Protocol):
    """Base protocol for anything that can process state"""

    @property
    def input_schema(self) -> type[BaseModel]:
        """What this unit expects as input"""

    @property
    def output_schema(self) -> type[BaseModel]:
        """What this unit produces as output"""

    def execute(self, state: BaseModel) -> BaseModel:
        """Execute on state, return modified state"""

# Everything is an ExecutableUnit
class Engine(ExecutableUnit):
    """LLM or other stateful processor"""

class Tool(ExecutableUnit):
    """Stateless function with schema"""

class Node(ExecutableUnit):
    """Graph node that may contain other units"""
```

### Phase 2: State Mapping Strategy

```python
# Single state mapper
class StateMapper:
    """Maps between state and unit I/O"""

    def extract_input(
        self,
        state: BaseModel,
        unit: ExecutableUnit
    ) -> BaseModel:
        """Extract input for unit from state"""

    def merge_output(
        self,
        state: BaseModel,
        output: BaseModel,
        unit: ExecutableUnit
    ) -> BaseModel:
        """Merge unit output back into state"""

# Use TypeAdapter for conversions
from pydantic import TypeAdapter

class SmartStateMapper(StateMapper):
    def __init__(self):
        self._adapters: dict[tuple[type, type], TypeAdapter] = {}

    def extract_input(self, state, unit):
        adapter = self._get_adapter(type(state), unit.input_schema)
        # Smart extraction with type conversion
```

### Phase 3: Backwards Compatible Layer

```python
# Adapter for old Engine interface
class LegacyEngineAdapter(ExecutableUnit):
    def __init__(self, engine: OldEngine):
        self.engine = engine

    @property
    def input_schema(self):
        # Extract from engine.input_schema
        return self.engine.get_input_schema()

    def execute(self, state):
        # Use old engine with state mapping
        input_data = self.engine.prepare_input(state)
        output = self.engine.run(input_data)
        return self.engine.update_state(state, output)

# Keep old interfaces working
def create_node(engine: OldEngine | ExecutableUnit):
    if isinstance(engine, OldEngine):
        engine = LegacyEngineAdapter(engine)
    return Node(engine)
```

## Implementation Steps

### Week 1: Create Core Protocols

1. Define ExecutableUnit protocol
2. Create StateMapper interface
3. Write comprehensive tests for protocols
4. Document new concepts clearly

### Week 2: Implement Tool System

1. Redefine Tool as simple ExecutableUnit
2. Create ToolAdapter for legacy tools
3. Fix tool execution (currently broken)
4. Add structured output support properly

### Week 3: Engine Refactoring

1. Create new Engine base class
2. Implement LegacyEngineAdapter
3. Update engine registry to handle both
4. Test with existing engines

### Week 4: Node System Update

1. Make Node an ExecutableUnit
2. Remove duplicate state mapping
3. Create NodeAdapter for old configs
4. Test graph compilation

### Week 5: State Schema Simplification

1. Move I/O mappings to StateMapper
2. Simplify StateSchema to just fields
3. Add backwards compatible property
4. Update schema generation

### Week 6: Integration Testing

1. Test all agent types
2. Verify backwards compatibility
3. Performance benchmarking
4. Fix edge cases

## Code Organization

```
packages/haive-core/src/haive/core/
├── executable/          # New unified system
│   ├── __init__.py
│   ├── protocols.py     # ExecutableUnit protocol
│   ├── engine.py        # New Engine implementation
│   ├── tool.py          # New Tool implementation
│   ├── node.py          # New Node implementation
│   └── state_mapper.py  # State mapping logic
├── legacy/              # Backwards compatibility
│   ├── __init__.py
│   ├── adapters.py      # Legacy adapters
│   └── compat.py        # Compatibility helpers
└── schema_v2/           # Simplified schema system
    ├── __init__.py
    ├── state.py         # New StateSchema
    └── composer.py      # New SchemaComposer
```

## Key Decisions Needed

### 1. Node vs Engine Identity

**Option A**: Nodes ARE engines

- Pro: Simpler concept model
- Con: Major breaking change

**Option B**: Nodes CONTAIN engines

- Pro: Backwards compatible
- Con: Keeps some complexity

**Recommendation**: Option B with migration path to A

### 2. State Mapping Location

**Option A**: All in StateMapper

- Pro: Single source of truth
- Con: New abstraction layer

**Option B**: Keep in multiple places

- Pro: No new concepts
- Con: Continued duplication

**Recommendation**: Option A with adapters

### 3. Tool System Design

**Option A**: Tools are just functions

- Pro: Simple and clear
- Con: Loses some features

**Option B**: Tools remain complex

- Pro: All features kept
- Con: Continues confusion

**Recommendation**: Option A with extensions

## Success Criteria

1. **All tests pass** with new system
2. **Backwards compatibility** maintained
3. **Tool execution works** (currently broken)
4. **Type safety** improved (generics added)
5. **Performance** same or better
6. **Concepts clear** (what is what)

## Next Immediate Steps

1. Review and refine this plan
2. Create ExecutableUnit protocol
3. Write tests for desired behavior
4. Start with Tool system (most broken)
5. Build up from there

## Questions to Resolve

1. Should nodes be engines or contain engines?
2. Where should state mapping live?
3. How to handle structured output tools?
4. What's the difference between meta/multi agents?
5. How to make branches modifiable?

Let's start with defining the ExecutableUnit protocol and fixing the tool system since that's completely broken right now.
