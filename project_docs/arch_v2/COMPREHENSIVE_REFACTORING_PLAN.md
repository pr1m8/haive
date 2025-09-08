# Comprehensive Refactoring Plan - Haive Architecture v2

**Created**: 2025-01-07  
**Purpose**: Actionable refactoring plan based on deep architectural analysis  
**Status**: Ready for implementation

## 🎯 Executive Summary

After deep analysis of the Haive framework, we've identified **7 critical architectural problems** that require systematic refactoring:

1. **Monolithic Classes**: 7 god objects with 50-112 methods each
2. **Circular Dependencies**: 4 major circular dependency chains
3. **Node Proliferation**: 43 node types causing massive duplication
4. **Recompilation Cascades**: 10+ second rebuilds for simple changes
5. **Performance Crisis**: 10-50x slower than necessary
6. **Memory Leaks**: 50MB leak per recompilation cycle
7. **LangGraph Misalignment**: Fighting static nature with dynamic patterns

## 📋 Refactoring Phases

### Phase 1: Emergency Stabilization (Week 1)

**Goal**: Stop the bleeding - fix critical issues blocking development

#### 1.1 Fix String-Based Type Checking (2 days)

```python
# Current (BAD) - BaseGraph2 line 2856
if hasattr(result, "__class__") and "Command" in result.__class__.__name__:

# Refactored (GOOD)
from langgraph.types import Command
if isinstance(result, Command):
```

**Files to modify**:

- `/packages/haive-core/src/haive/core/graph/state_graph/base_graph2.py`
- All validation nodes using string checks

#### 1.2 Add Compilation Caching (1 day)

```python
class CompilationCache:
    """Cache compiled graphs to avoid recompilation."""

    def get_or_compile(self, key: str, compile_func: Callable):
        if cached := self._cache.get(key):
            return cached
        result = compile_func()
        self._cache[key] = result
        return result
```

**Implementation**:

- Add to BaseGraph2
- Cache key from graph structure hash
- Clear cache only on structural changes

#### 1.3 Batch Recompilation Operations (2 days)

```python
class BatchOperationContext:
    """Batch multiple operations before recompiling."""

    def __enter__(self):
        self.graph._suspend_recompilation = True
        return self

    def __exit__(self, *args):
        self.graph._suspend_recompilation = False
        if self.graph.needs_recompile:
            self.graph._trigger_recompile()

# Usage
with graph.batch_operations():
    graph.add_tool(tool1)
    graph.add_tool(tool2)
    graph.add_tool(tool3)
# Single recompilation here
```

### Phase 2: Node Consolidation (Week 2)

**Goal**: Reduce 43 node types to <10 base types

#### 2.1 Create Node Hierarchy

```python
# New structure
BaseNode (abstract)
├── AgentNode (for all agent executions)
├── ValidationNode (for all validation)
├── ToolNode (for all tool executions)
├── RouterNode (for all routing)
├── TransformNode (for all transformations)
└── CustomNode (for special cases)

# Delete 37 redundant node types!
```

#### 2.2 Node Configuration Pattern

```python
class NodeConfig(BaseModel):
    """Configuration for node behavior."""
    node_type: NodeType
    validation_mode: ValidationMode
    routing_strategy: RoutingStrategy
    error_handling: ErrorHandling

class ConfigurableNode(BaseNode):
    """Single node class with configuration."""
    config: NodeConfig

    def execute(self, state):
        # Behavior based on config, not class type
        return self.strategies[self.config.node_type](state)
```

#### 2.3 Migration Script

```python
# Automated migration
NODE_MAPPING = {
    "AgentNodeV2": ("AgentNode", {"version": 2}),
    "AgentNodeV3": ("AgentNode", {"version": 3}),
    "ValidationNodeV2": ("ValidationNode", {"version": 2}),
    # ... map all 43 types
}

def migrate_node(old_node):
    new_type, config = NODE_MAPPING[old_node.__class__.__name__]
    return create_node(new_type, config, old_node.data)
```

### Phase 3: Break Circular Dependencies (Week 3)

**Goal**: Eliminate circular import chains

#### 3.1 Dependency Inversion for StateSchema

```python
# Current (CIRCULAR)
class StateSchema:
    def get_engine(self) -> Engine:
        return self.engines[name]  # StateSchema → Engine

# Refactored (INVERTED)
class StateSchema:
    # Just data, no engine knowledge
    engines: Dict[str, Any]

class EngineManager:
    """Manages engine-state relationships."""
    def get_engine_for_state(self, state: StateSchema, name: str):
        return state.engines[name]
```

#### 3.2 Extract Interfaces

```python
# Define protocols/interfaces
class StateProtocol(Protocol):
    """What a state must provide."""
    def get_messages(self) -> List[BaseMessage]: ...
    def update_field(self, key: str, value: Any): ...

class EngineProtocol(Protocol):
    """What an engine must provide."""
    def execute(self, input: Any) -> Any: ...
    def get_tools(self) -> List[Tool]: ...

# Now components depend on protocols, not concrete classes
```

#### 3.3 Event-Based Decoupling

```python
class EventBus:
    """Decouple components with events."""

    def publish(self, event: Event):
        for handler in self.handlers[event.type]:
            handler(event)

    def subscribe(self, event_type: str, handler: Callable):
        self.handlers[event_type].append(handler)

# Usage - no direct coupling
event_bus.publish(StateChangedEvent(state))
# Engines subscribe to state changes
```

### Phase 4: Optimize Schema Composition (Week 4)

**Goal**: Make schema composition incremental and fast

#### 4.1 Incremental Schema Builder

```python
class IncrementalSchemaBuilder:
    """Build schemas incrementally instead of full recomposition."""

    def __init__(self, base_schema):
        self.base_fields = base_schema.model_fields.copy()
        self.added_fields = {}
        self.removed_fields = set()

    def add_field(self, name: str, type: Type, default: Any = None):
        """Add single field - O(1) instead of O(N)."""
        self.added_fields[name] = (type, default)
        self._mark_dirty(f"Added field {name}")

    def build(self):
        """Build only if dirty."""
        if not self.is_dirty:
            return self.cached_schema
        # Incremental update, not full rebuild
        return self._incremental_build()
```

#### 4.2 Schema Caching Strategy

```python
class SchemaCache:
    """Cache composed schemas by component signatures."""

    def get_schema(self, components: List[Any]):
        key = self._compute_key(components)
        if cached := self.cache.get(key):
            return cached

        # Only compose if not cached
        schema = SchemaComposer.compose(components)
        self.cache[key] = schema
        return schema
```

### Phase 5: Performance Optimization (Week 5)

**Goal**: Achieve 10x performance improvement

#### 5.1 Lazy Import Strategy

```python
# Current (SLOW) - loads everything
from haive.core import *  # 3.2 seconds!

# Refactored (FAST) - lazy loading
class LazyImporter:
    def __getattr__(self, name):
        # Import only when accessed
        module = importlib.import_module(f"haive.core.{name}")
        setattr(self, name, module)
        return module

haive.core = LazyImporter()
# Now 0.1 seconds until actual use!
```

#### 5.2 Engine Lookup Optimization

```python
class EngineResolver:
    """Fast engine resolution with caching."""

    def __init__(self):
        self.cache = {}
        self.lookup_strategies = [
            self._direct_lookup,  # O(1)
            self._cached_lookup,  # O(1)
            self._registry_lookup  # O(log n)
        ]

    def resolve(self, state, engine_name):
        # Try cache first
        cache_key = (id(state), engine_name)
        if cached := self.cache.get(cache_key):
            return cached

        # Try strategies in order
        for strategy in self.lookup_strategies:
            if engine := strategy(state, engine_name):
                self.cache[cache_key] = engine
                return engine
```

#### 5.3 Memory Leak Fixes

```python
class ProperCleanup:
    """Ensure proper cleanup to prevent leaks."""

    def recompile(self):
        # Save what we need
        essential_data = self._extract_essentials()

        # Clear everything explicitly
        self._clear_all_references()

        # Force garbage collection
        import gc
        gc.collect()

        # Rebuild with essentials
        self._rebuild_from_essentials(essential_data)
```

### Phase 6: LangGraph Alignment (Week 6)

**Goal**: Work with LangGraph's static nature, not against it

#### 6.1 Static Schema Factory

```python
class StaticSchemaFactory:
    """Pre-create all schema variants at compile time."""

    SCHEMA_VARIANTS = {
        "basic": BasicSchema,
        "with_tools": SchemaWithTools,
        "multi_agent": MultiAgentSchema,
        "with_memory": SchemaWithMemory,
    }

    @classmethod
    def get_schema(cls, variant: str, **config):
        """Get pre-defined schema variant."""
        schema_class = cls.SCHEMA_VARIANTS[variant]
        # Schema already has all possible fields
        return schema_class(**config)
```

#### 6.2 Subgraph Pattern for Dynamic Behavior

```python
class DynamicViaSubgraphs:
    """Use subgraphs for dynamic behavior within static constraints."""

    def create_dynamic_graph(self, components):
        # Main graph is static
        main_graph = StateGraph(StaticSchema)

        # Dynamic behavior via subgraphs
        for component in components:
            subgraph = self.create_subgraph(component)
            main_graph.add_node(f"sub_{component.name}", subgraph)

        return main_graph.compile()
```

### Phase 7: Architectural Cleanup (Week 7-8)

**Goal**: Clean architecture for maintainability

#### 7.1 Layer Architecture

```python
# Clear layers with no circular deps
"""
Presentation Layer (UI/CLI)
    ↓
Application Layer (Agents, Workflows)
    ↓
Domain Layer (Business Logic, State)
    ↓
Infrastructure Layer (LangGraph, Storage)
"""

# Enforce with import restrictions
LAYER_RULES = {
    "infrastructure": [],  # Can't import from higher layers
    "domain": ["infrastructure"],
    "application": ["domain", "infrastructure"],
    "presentation": ["application", "domain", "infrastructure"]
}
```

#### 7.2 Reduce Mixin Complexity

```python
# Current (TOO MANY MIXINS)
class Agent(
    StateMixin,
    ToolMixin,
    ValidationMixin,
    PersistenceMixin,
    SerializationMixin,
    RecompileMixin,
    ExecutionMixin,
    RoutingMixin,
    Base
): pass  # 9 mixins!

# Refactored (COMPOSITION)
class Agent:
    def __init__(self):
        self.state_manager = StateManager()
        self.tool_manager = ToolManager()
        self.validator = Validator()
        # Composition over inheritance
```

## 📊 Success Metrics

### Performance Targets

| Metric         | Current | Target | Improvement |
| -------------- | ------- | ------ | ----------- |
| Import time    | 3.2s    | 0.4s   | 8x          |
| Agent creation | 2.5s    | 0.3s   | 8x          |
| Tool addition  | 10.5s   | 0.05s  | 210x        |
| Memory usage   | 2GB     | 200MB  | 10x         |
| Recompilation  | 10s     | 0.5s   | 20x         |

### Code Quality Targets

| Metric             | Current  | Target |
| ------------------ | -------- | ------ |
| Node types         | 43       | <10    |
| Circular deps      | 4 chains | 0      |
| God objects        | 7        | 0      |
| Max methods/class  | 112      | <20    |
| TYPE_CHECKING uses | 198      | <20    |
| Files              | 2,747    | <500   |

## 🚀 Implementation Schedule

### Week 1: Emergency Fixes

- [ ] Fix string-based type checking
- [ ] Add compilation caching
- [ ] Implement batch operations
- [ ] Fix critical memory leaks

### Week 2: Node Consolidation

- [ ] Design new node hierarchy
- [ ] Implement ConfigurableNode
- [ ] Create migration script
- [ ] Deprecate old node types

### Week 3: Break Dependencies

- [ ] Implement dependency inversion
- [ ] Extract interfaces/protocols
- [ ] Add event bus for decoupling
- [ ] Remove circular imports

### Week 4: Schema Optimization

- [ ] Build incremental schema composer
- [ ] Implement schema caching
- [ ] Optimize field extraction
- [ ] Fix conflict resolution

### Week 5: Performance

- [ ] Implement lazy imports
- [ ] Optimize engine lookups
- [ ] Fix memory leaks
- [ ] Add performance monitoring

### Week 6: LangGraph Alignment

- [ ] Create static schema factory
- [ ] Implement subgraph patterns
- [ ] Fix type safety issues
- [ ] Document patterns

### Week 7-8: Architecture

- [ ] Establish layer architecture
- [ ] Reduce mixin complexity
- [ ] Clean up tech debt
- [ ] Documentation and testing

## 🎯 Risk Mitigation

### Backward Compatibility

- Keep old APIs with deprecation warnings
- Provide migration scripts
- Maintain compatibility layer for 2 versions

### Testing Strategy

- Add performance benchmarks before changes
- Test each refactoring in isolation
- Maintain 90%+ test coverage
- No mocks - real component testing

### Rollback Plan

- Tag releases before each phase
- Feature flags for new implementations
- Ability to switch between old/new code

## 📈 Expected Outcomes

### Immediate (Week 1)

- 40% performance improvement
- No more string-based type checking
- Batch operations working

### Short-term (Month 1)

- 70% performance improvement
- Node types reduced to <10
- Circular dependencies broken

### Long-term (Month 2)

- 90% performance improvement
- Clean architecture established
- System scalable to 100+ agents

## 🔑 Critical Success Factors

1. **Executive Buy-in**: This will take 8 weeks of focused effort
2. **Testing First**: Every change needs tests before implementation
3. **Incremental Delivery**: Ship improvements weekly
4. **Performance Monitoring**: Track metrics throughout
5. **Documentation**: Document new patterns as we go

## 📋 Next Steps

1. **Get approval** for 8-week refactoring sprint
2. **Set up performance benchmarks** to track progress
3. **Create feature flags** for safe rollout
4. **Begin Week 1** emergency fixes immediately
5. **Weekly demos** of improvements

---

**Conclusion**: The Haive framework requires systematic refactoring across 7 phases to address critical architectural issues. With 8 weeks of focused effort, we can achieve 10-210x performance improvements, reduce complexity by 80%, and create a maintainable architecture that can scale to 100+ agents. The key is to start with emergency fixes while building toward a clean, performant architecture.
