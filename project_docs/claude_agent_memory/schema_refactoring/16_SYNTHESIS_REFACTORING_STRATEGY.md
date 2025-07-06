# Synthesis: The Best Way to Refactor Haive Schema System

## Executive Summary

After analyzing 15+ critical issues, here's the synthesized strategy for refactoring the haive schema system. This approach addresses the core problems while maintaining backwards compatibility.

## The Core Problems (Prioritized)

### **1. CRITICAL: Conceptual Confusion**

- Engine = Factory + Executable + Config (insane)
- Agent IS-A Engine but HAS Engines
- Node wraps anything (no type safety)
- Agent ≠ CompiledGraph (hidden compilation)

### **2. CRITICAL: Schema System Chaos**

- StateSchema (2,153 lines) - monolithic
- SchemaComposer (29,000+ tokens) - unmaintainable
- No type safety (everything is Any)
- Missing generics everywhere

### **3. HIGH: Engine Access Pattern Chaos**

- 3 different lookup patterns
- Engines stored in multiple places
- No single source of truth
- Node execution unpredictable

### **4. HIGH: Missing Pydantic Features**

- No model_post_init usage
- No TypeAdapter for standalone fields
- No discriminated unions for nodes
- No computed fields for composition

### **5. MEDIUM: Mixin/Inheritance Inconsistency**

- No standard initialization pattern
- Random mixin application
- Code duplication everywhere

## The Synthesis: A Phased Approach

### **Phase 1: Establish Core Concepts (Weeks 1-2)**

#### **1.1 Define Clear Boundaries**

```python
# schema_test/core/concepts.py

# EXECUTABLES - Things that actually run
class Executable(Protocol[TInput, TOutput]):
    """Anything that can be executed"""
    def execute(self, input: TInput) -> TOutput: ...

# CONFIGURATIONS - Things that create executables
class Configuration(BaseModel, Generic[T]):
    """Configuration for creating executables"""
    def create(self) -> T: ...

# GRAPHS - Structure that compiles to executables
class GraphStructure(BaseModel, Generic[TState]):
    """Graph structure before compilation"""
    nodes: Dict[str, 'GraphNode[TState]']
    edges: List[Edge]
    state_schema: Type[TState]

    def compile(self) -> 'CompiledGraph[TState]': ...

# COMPILED GRAPHS - The actual executable graphs
class CompiledGraph(Executable[TInput, TOutput], Generic[TState]):
    """Compiled, executable graph"""
    def execute(self, input: TInput) -> TOutput: ...
```

#### **1.2 Fix the Engine Concept**

```python
# Engines are CONFIGURATIONS, not executables
class EngineConfig(Configuration[Executable[TInput, TOutput]], Generic[TInput, TOutput]):
    """Engine configuration that creates executables"""
    name: str
    type: str
    input_schema: Type[TInput]
    output_schema: Type[TOutput]

    def create(self) -> Executable[TInput, TOutput]:
        """Create the actual executable"""
        # Returns executor, not self!
```

#### **1.3 Fix the Agent Concept**

```python
# Agents are GRAPH BUILDERS, not engines
class Agent(GraphBuilder[TState, TInput, TOutput], Generic[TState, TInput, TOutput]):
    """Agent builds and manages graphs"""
    name: str
    state_schema: Type[TState]
    engines: Dict[str, EngineConfig]  # Configurations, not executables

    def build_graph(self) -> GraphStructure[TState]:
        """Build the graph structure"""

    def create_executable(self) -> CompiledGraph[TState]:
        """Compile graph to executable"""
        graph = self.build_graph()
        return graph.compile()
```

### **Phase 2: Type-Safe Schema System (Weeks 3-4)**

#### **2.1 Modular Schema Components**

```python
# schema_test/core/components/

# Replace monolithic StateSchema
class FieldManager(BaseModel):
    """Manages field definitions with Pydantic features"""
    fields: Dict[str, FieldDefinition] = {}

    def model_post_init(self, __context: Any) -> None:
        """Auto-register fields after validation"""
        self._register_fields()
        self._setup_priorities()

class SchemaBuilder(BaseModel, Generic[T]):
    """Builds schemas dynamically"""
    field_manager: FieldManager

    @computed_field
    @cached_property
    def schema_class(self) -> Type[T]:
        """Dynamically build schema class"""
        return self._create_schema_class()

# Standalone field validation
class FieldValidator:
    """Validate fields without full schemas"""
    def __init__(self):
        self.adapters: Dict[str, TypeAdapter] = {}

    def validate_field(self, name: str, value: Any) -> Any:
        return self.adapters[name].validate_python(value)
```

#### **2.2 Type-Safe Node System**

```python
# Use discriminated unions for nodes
class EngineNode(BaseModel):
    node_type: Literal['engine'] = 'engine'
    config_ref: str  # Reference to engine config
    input_mapping: Dict[str, str]
    output_mapping: Dict[str, str]

class SubgraphNode(BaseModel):
    node_type: Literal['subgraph'] = 'subgraph'
    graph: GraphStructure[Any]  # Nested graph
    state_mapping: StateMapping

Node = Annotated[
    Union[EngineNode, SubgraphNode, CallableNode],
    Field(discriminator='node_type')
]
```

### **Phase 3: Unified Access Patterns (Weeks 5-6)**

#### **3.1 Single Engine Registry**

```python
class EngineRegistry:
    """Single source of truth for engines"""
    _configs: Dict[str, EngineConfig] = {}

    def register(self, name: str, config: EngineConfig) -> None:
        self._configs[name] = config

    def get_config(self, name: str) -> EngineConfig:
        if name not in self._configs:
            raise EngineNotFoundError(f"Engine '{name}' not found")
        return self._configs[name]

    def create_executable(self, name: str) -> Executable:
        config = self.get_config(name)
        return config.create()
```

#### **3.2 Standardized Node Execution**

```python
class NodeExecutor(BaseModel):
    """Unified node execution with single pattern"""
    registry: EngineRegistry

    def execute_node(
        self,
        node: Node,
        state: TState,
        context: ExecutionContext
    ) -> Any:
        """Single execution pattern for all nodes"""
        if isinstance(node, EngineNode):
            return self._execute_engine_node(node, state, context)
        elif isinstance(node, SubgraphNode):
            return self._execute_subgraph_node(node, state, context)
        # Type checker ensures exhaustive handling
```

### **Phase 4: Advanced Pydantic Integration (Weeks 7-8)**

#### **4.1 Consistent Mixin Pattern**

```python
class SchemaMixin:
    """Base mixin with consistent initialization"""

    def model_post_init(self, __context: Any) -> None:
        # Always call parent
        if hasattr(super(), 'model_post_init'):
            super().model_post_init(__context)

        # Then initialize mixin
        self._init_schema_features()

class FieldSyncMixin(SchemaMixin):
    """Field syncing capabilities"""
    _sync_rules: Dict[str, List[str]] = {}

    def _init_schema_features(self):
        self._setup_sync_rules()

class PriorityMixin(SchemaMixin):
    """Field priority management"""
    _priorities: Dict[str, int] = {}

    def _init_schema_features(self):
        self._setup_priorities()
```

#### **4.2 Context-Aware Schemas**

```python
class ContextSchema(BaseModel):
    """Schema that adapts to context"""
    fields: Dict[str, Any]
    context: str = "default"

    @field_validator('fields', mode='before')
    @classmethod
    def adapt_for_context(cls, v: Any, info: ValidationInfo) -> Any:
        """Adapt fields based on context"""
        context = info.data.get('context', 'default')
        return ContextAdapter.adapt_fields(v, context)
```

### **Phase 5: Migration Strategy (Weeks 9-12)**

#### **5.1 Adapter Layer**

```python
# schema_test/adapters/

class StateSchemaAdapter:
    """Makes new system look like old StateSchema"""
    def __init__(self):
        self._builder = SchemaBuilder()
        self._field_manager = FieldManager()

    # Old API
    def share_field(self, name: str) -> None:
        # Delegate to new system
        self._field_manager.mark_shared(name)

    # Compatibility
    def __getattr__(self, name: str) -> Any:
        # Handle old special attributes
        if name == "__shared_fields__":
            return self._field_manager.get_shared_fields()
```

#### **5.2 Feature Flags**

```python
# Gradual rollout
USE_NEW_SCHEMA = os.getenv('HAIVE_NEW_SCHEMA', 'false') == 'true'

if USE_NEW_SCHEMA:
    from schema_test import StateSchema
else:
    from schema import StateSchema  # Old system
```

## Implementation Priorities

### **Must Have (MVP)**

1. Clear conceptual model (Executable vs Configuration)
2. Type-safe nodes with discriminated unions
3. Single engine registry pattern
4. Basic schema builder with field management
5. Adapter layer for backwards compatibility

### **Should Have (V1)**

1. Full generic type support
2. Advanced Pydantic features (computed fields, validators)
3. Context-aware schema adaptation
4. Comprehensive mixin system
5. Migration tooling

### **Nice to Have (V2)**

1. Performance optimizations
2. Advanced alias generation
3. Schema visualization
4. Development tools

## Success Metrics

### **Technical**

- Zero engine lookup failures
- Full type safety (no Any)
- Sub-1000 lines per component
- 100% backwards compatibility

### **Developer Experience**

- Clear concepts (can explain in one sentence)
- IDE autocomplete works
- Predictable behavior
- Easy to test

## Key Decisions

### **1. Separate Configuration from Execution**

- Engines are configurations, not executables
- Agents build graphs, not execute directly
- Clear compilation step

### **2. Embrace Pydantic v2 Features**

- model_post_init for initialization
- TypeAdapter for standalone validation
- Discriminated unions for type safety
- Computed fields for dynamic composition

### **3. Type Safety First**

- Full generics throughout
- No Any types
- Discriminated unions for variants
- Type-safe state flow

### **4. Modular Architecture**

- Small, focused components
- Clear single responsibilities
- Composable patterns
- Testable units

## Next Steps

1. **Validate Approach**: Does this synthesis address your concerns?
2. **Start Phase 1**: Create conceptual model in schema_test/
3. **Prototype Core**: Build EngineConfig and Agent base
4. **Test Integration**: Ensure it works with existing graphs
5. **Iterate**: Refine based on real usage

This synthesis provides a clear path from the current chaos to a well-architected, type-safe, maintainable system!
