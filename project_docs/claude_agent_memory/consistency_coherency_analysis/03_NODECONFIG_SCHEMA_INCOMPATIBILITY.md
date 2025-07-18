# NodeConfig-Schema Incompatibility Issues

## Core Problem: Two Disconnected Systems

### System 1: NodeConfig (Graph Level)

**Location**: `packages/haive-core/src/haive/core/graph/node/`

```python
# EngineNodeConfig operates at engine level
class EngineNodeConfig(BaseModel):
    engine_name: str  # String reference to engine
    node_name: str | None = None
    # No schema awareness
    # No field mapping information
    # No type safety for state fields
```

### System 2: SchemaComposer (State Level)

**Location**: `packages/haive-core/src/haive/core/schema/`

```python
# SchemaComposer operates at state schema level
class SchemaComposer:
    def from_components(components: list[Engine]):
        # Extracts fields from engines
        # Creates unified state schema
        # But NO connection to node execution
```

**The Gap**: NodeConfig and SchemaComposer don't communicate

## Current Incompatibilities

### 1. **Engine Reference vs Engine Object**

```python
# NodeConfig uses string references
node_config = EngineNodeConfig(engine_name="my_llm")

# SchemaComposer needs actual engine objects
schema = SchemaComposer.from_components([actual_engine_object])

# NO BRIDGE between string reference and object
```

### 2. **No Field Mapping in Nodes**

```python
# Schema knows about fields:
state_schema.model_fields["messages"]  # Available
state_schema.__engine_io_mappings__["my_llm"]  # Input/output mapping

# But node execution doesn't use this information:
def execute_node(state):
    # Manually extracts data - no schema awareness
    messages = state.get("messages", [])
    # No validation against schema
    # No automatic field routing
```

### 3. **Type Safety Lost in Graph Execution**

```python
# Schema composition creates type-safe state:
class ComposedState(StateSchema):
    messages: list[BaseMessage] = Field(...)
    engine_output: EngineResult = Field(...)

# But graph nodes receive untyped state:
def node_function(state: dict):  # Should be ComposedState!
    # Type information lost
    # No IDE support
    # Runtime errors possible
```

### 4. **Engine I/O Mappings Ignored**

```python
# Schema has engine I/O mappings:
__engine_io_mappings__ = {
    "llm_engine": {
        "input_fields": ["messages", "context"],
        "output_fields": ["response", "tool_calls"]
    }
}

# But node execution doesn't use mappings:
def llm_node(state):
    # Manually extracts ALL state - inefficient
    # Doesn't know which fields are actually needed
    # Can't validate input requirements
```

## Required Integration Points

### 1. **Schema-Aware NodeConfig**

```python
class SchemaAwareNodeConfig(BaseModel):
    engine_name: str
    state_schema: type[StateSchema] = Field(...)
    input_fields: list[str] = Field(...)  # From schema I/O mapping
    output_fields: list[str] = Field(...)  # From schema I/O mapping

    @classmethod
    def from_schema_mapping(cls, engine_name: str, schema: StateSchema):
        """Create NodeConfig from schema I/O mappings"""
        mappings = getattr(schema, "__engine_io_mappings__", {})
        engine_mapping = mappings.get(engine_name, {})

        return cls(
            engine_name=engine_name,
            state_schema=schema,
            input_fields=engine_mapping.get("input_fields", []),
            output_fields=engine_mapping.get("output_fields", [])
        )
```

### 2. **Type-Safe Node Execution**

```python
def create_typed_node_function(node_config: SchemaAwareNodeConfig):
    """Create type-safe node function from schema"""

    def typed_node_function(state: node_config.state_schema) -> dict:
        # Extract only required input fields
        input_data = {
            field: getattr(state, field)
            for field in node_config.input_fields
        }

        # Execute engine with typed input
        engine = get_engine(node_config.engine_name)
        result = engine.invoke(input_data)

        # Return only mapped output fields
        return {
            field: result.get(field)
            for field in node_config.output_fields
        }

    return typed_node_function
```

### 3. **Schema-Graph Bridge**

```python
class SchemaGraphBridge:
    """Bridge between schema composition and graph execution"""

    def __init__(self, state_schema: StateSchema):
        self.state_schema = state_schema
        self.engine_mappings = getattr(state_schema, "__engine_io_mappings__", {})

    def create_node_configs(self) -> dict[str, SchemaAwareNodeConfig]:
        """Create node configs from schema I/O mappings"""
        configs = {}
        for engine_name, mapping in self.engine_mappings.items():
            configs[engine_name] = SchemaAwareNodeConfig.from_schema_mapping(
                engine_name, self.state_schema
            )
        return configs

    def validate_graph_compatibility(self, graph: BaseGraph) -> list[str]:
        """Validate that graph nodes match schema expectations"""
        issues = []
        for node_name in graph.nodes:
            if node_name not in self.engine_mappings:
                issues.append(f"Node {node_name} not in schema mappings")
        return issues
```

## Agent Integration Solution

### 1. **Update Agent Schema Setup**

```python
class Agent:
    def _setup_schemas(self):
        """Enhanced schema setup with NodeConfig integration"""
        # Existing schema composition...
        self.state_schema = SchemaComposer.from_components(...)

        # NEW: Create schema-graph bridge
        self.schema_bridge = SchemaGraphBridge(self.state_schema)
        self.node_configs = self.schema_bridge.create_node_configs()

    def build_graph(self) -> BaseGraph:
        """Schema-aware graph building"""
        graph = BaseGraph(name=self.name)

        # Use schema-aware node configs
        for engine_name, node_config in self.node_configs.items():
            typed_node_fn = create_typed_node_function(node_config)
            graph.add_node(engine_name, typed_node_fn)

        return graph
```

### 2. **MultiAgent Schema Integration**

```python
class MultiAgent:
    def _setup_multi_agent_nodes(self):
        """Create nodes that respect agent schema boundaries"""
        for agent in self.agents:
            # Each agent contributes its schema-aware nodes
            agent_bridge = SchemaGraphBridge(agent.state_schema)
            agent_configs = agent_bridge.create_node_configs()

            # Namespace node configs to prevent conflicts
            for engine_name, config in agent_configs.items():
                namespaced_name = f"{agent.name}_{engine_name}"
                self.combined_node_configs[namespaced_name] = config
```

### 3. **ChainAgent Fix with Schema Integration**

```python
class ChainAgent:
    def build_graph(self) -> BaseGraph:
        """Schema-aware chain building"""
        # Use schema bridge instead of manual data passing
        self.schema_bridge = SchemaGraphBridge(self.state_schema)

        graph = BaseGraph(name=self.name)
        prev_node = None

        for i, engine_name in enumerate(self.engine_names):
            node_config = self.schema_bridge.get_node_config(engine_name)
            typed_node_fn = create_typed_node_function(node_config)

            current_node = f"step_{i}"
            graph.add_node(current_node, typed_node_fn)

            if prev_node:
                graph.add_edge(prev_node, current_node)
            prev_node = current_node

        return graph
```

## Benefits of Integration

### 1. **Type Safety Throughout**

- Schema types preserved in node execution
- IDE support for state field access
- Compile-time error detection

### 2. **Efficient Field Routing**

- Nodes only receive required input fields
- No unnecessary data copying
- Clear input/output contracts

### 3. **Schema Validation**

- Graph structure validated against schema expectations
- Missing field mappings detected early
- Incompatible node connections prevented

### 4. **Unified Development Model**

- Single source of truth for state structure
- Schema drives both composition and execution
- Consistent patterns across all agent types

This integration resolves the current disconnect between schema composition and graph execution, enabling type-safe and efficient node operations.
