# Layered Architecture Analysis: Engine → Node → Schema → Graph → Agent

**Date**: 2025-06-28
**Focus**: Understanding the flow from engines up through the full agent stack

## The 5-Layer Architecture

### **Layer 1: ENGINE (Foundation)**

```python
# From engine/base/base.py
class Engine(ABC, BaseModel, Generic[TIn, TOut]):
    """Abstract base class for all engine configurations."""

    # Core identification
    id: str
    name: str
    engine_type: EngineType

    # Schema definitions (optional)
    input_schema: type[BaseModel] | None = Field(default=None, exclude=True)
    output_schema: type[BaseModel] | None = Field(default=None, exclude=True)

    @abstractmethod
    def get_input_fields(self) -> dict[str, tuple[type, Any]]:
        """Return input field definitions as field_name -> (type, default) pairs."""

    @abstractmethod
    def get_output_fields(self) -> dict[str, tuple[type, Any]]:
        """Return output field definitions as field_name -> (type, default) pairs."""

    @abstractmethod
    def create_runnable(self, config: RunnableConfig | None = None) -> Any:
        """Create the actual runtime object."""
```

**Engine Layer Responsibilities**:

- Define input/output field contracts
- Provide typed interfaces for I/O
- Create runtime objects (LLMs, retrievers, etc.)
- **Type safety foundation**

### **Layer 2: NODE (Execution Wrapper)**

```python
# From graph/node/base_config.py
class NodeConfig(ABC, BaseModel):
    """Base configuration for a node in a graph."""

    # Core identification
    id: str
    name: str
    node_type: NodeType

    # ===== DYNAMIC ROUTING CAPABILITIES (OPTIONAL) =====
    routing_enabled: bool = Field(default=False)
    routing_strategy: Optional[Any] = Field(default=None)  # <-- Problem: ANY

    # I/O Schema Configuration
    input_schema: Optional[Type[BaseModel]] = Field(default=None)
    output_schema: Optional[Type[BaseModel]] = Field(default=None)

    # State field extraction/mapping
    extract_fields: Optional[Union[List[str], Dict[str, str]]] = Field(default=None)
    result_fields: Optional[Union[str, List[str], Dict[str, str]]] = Field(default=None)

    @abstractmethod
    def __call__(self, state: dict[str, Any], config: dict[str, Any] | None = None) -> Any:
        """Execute the node."""
```

**Node Layer Problems**:

- **Feature creep**: routing + I/O + processing all mixed
- **Everything optional**: no clear contracts
- **ANY types**: loses type safety from Engine layer
- **Unclear responsibilities**: what does each node actually do?

### **Layer 3: SCHEMA (State Composition)**

```python
# From schema/schema_composer.py
class SchemaComposer:
    """Streamlined API for building state schemas dynamically from components."""

    def add_field(self, name, field_type, default=None, **kwargs):
        """Add a field to the schema."""

    def add_fields_from_components(self, components):
        """Extract fields from engines/components."""

    def build(self) -> type[BaseModel]:
        """Build the final state schema."""
```

**Schema Layer Responsibilities**:

- Compose state schemas from multiple engines
- Handle field conflicts and merging
- Create typed state models
- **Bridge between engine contracts and graph state**

### **Layer 4: GRAPH (Workflow Orchestration)**

```python
# From graph/state_graph/base_graph2.py
class BaseGraph(BaseModel, ValidationMixin):
    """Base class for graph management."""

    # Core components
    nodes: dict[str, Node | NodeConfig | Any | None] = Field(default_factory=dict)  # <-- ANY!
    edges: list[Edge] = Field(default_factory=list)
    branches: dict[str, Branch] = Field(default_factory=dict)

    # Schema
    state_schema: Any | None = None  # <-- ANY!

    def to_langgraph(self, **schema_kwargs) -> StateGraph:
        """Convert to LangGraph with schemas."""
```

**Graph Layer Problems**:

- **ANY types**: `nodes: dict[str, Any]` loses all type safety
- **No schema contracts**: state_schema can be anything
- **Loose coupling**: unclear how nodes relate to schema

### **Layer 5: AGENT (High-Level Interface)**

```python
# From agents/base/agent.py
class Agent(InvokableEngine, ExecutionMixin, StateMixin, ABC):
    """Abstract base agent class."""

    # Engine management
    engines: dict[str, Engine] = Field(default_factory=dict)
    engine: Engine | None = Field(default=None)

    # Schema definitions
    state_schema: type[StateSchema] | type[BaseModel] | dict[str, Any] | None
    input_schema: type[BaseModel] | dict[str, Any] | None
    output_schema: type[BaseModel] | dict[str, Any] | None

    def _setup_schemas(self) -> None:
        """Generate schemas from available engines."""
        if agent_list:
            # Use AgentSchemaComposer for agents
            self.state_schema = AgentSchemaComposer.from_agents(...)
        elif engine_list:
            # Use SchemaComposer for engines
            self.state_schema = SchemaComposer.from_components(...)

    @abstractmethod
    def build_graph(self) -> BaseGraph:
        """Build the workflow graph."""
```

**Agent Layer Responsibilities**:

- Orchestrate multiple engines
- Generate schemas from engines
- Build graphs from nodes
- Provide high-level interface

## The Flow Problems

### **Type Safety Degradation**

```
Engine (Typed) → Node (ANY) → Schema (Composed) → Graph (ANY) → Agent (Mixed)
   ✅ Strong      ❌ Lost     ✅ Recovered    ❌ Lost     ⚠️ Inconsistent
```

### **Responsibility Confusion**

- **Engine**: Clear contracts ✅
- **Node**: Everything optional, unclear purpose ❌
- **Schema**: Clear purpose ✅
- **Graph**: Loose typing, unclear contracts ❌
- **Agent**: Mixed patterns ⚠️

### **Information Loss**

1. **Engine** defines typed input/output fields
2. **Node** wraps with `Optional[Any]` - **loses typing**
3. **Schema** tries to recover from components
4. **Graph** stores as `dict[str, Any]` - **loses typing again**
5. **Agent** has inconsistent schema handling

## The Core Issue

**Each layer loses information from the previous layer instead of building on it.**

## Proposed Layered Contracts

### **Layer 1: Engine Contract**

```python
class TypedEngine(Protocol):
    input_schema: Type[BaseModel]
    output_schema: Type[BaseModel]

    def get_input_fields(self) -> Dict[str, FieldInfo]
    def get_output_fields(self) -> Dict[str, FieldInfo]
    def create_runnable(self) -> Invocable
```

### **Layer 2: Node Contract**

```python
class TypedNode(Protocol):
    engine: TypedEngine
    input_mapping: InputMapping
    output_mapping: OutputMapping

    def execute(self, state: TypedState) -> TypedResult
```

### **Layer 3: Schema Contract**

```python
class TypedSchemaComposer:
    def add_engine(self, engine: TypedEngine, mapping: FieldMapping)
    def compose(self) -> Type[TypedState]
```

### **Layer 4: Graph Contract**

```python
class TypedGraph:
    nodes: Dict[str, TypedNode]
    state_schema: Type[TypedState]

    def validate_flow(self) -> bool
    def compile(self) -> TypedRunnable
```

### **Layer 5: Agent Contract**

```python
class TypedAgent:
    engines: Dict[str, TypedEngine]
    graph: TypedGraph

    def invoke(self, input: AgentInput) -> AgentOutput
```

## Key Insights

1. **Type safety starts strong** (Engine) but **gets lost** (Node, Graph)
2. **Each layer should build on the previous** instead of starting over
3. **Contracts should flow upward** maintaining type information
4. **Separation of concerns** is lost in the middle layers
5. **Information preservation** is key to good architecture

The fix is to **maintain type contracts** through each layer instead of falling back to `Any` types.
