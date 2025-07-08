# Haive Agent Building Patterns - Compact Summary

## Core Agent Architecture

### 1. Base Agent Class (`Agent[TState]`)

```python
class MyAgent(Agent[MyState]):
    def setup_agent(self) -> None:
        # Initialize engines, sync fields, setup schemas

    def build_graph(self) -> BaseGraph:
        # Define workflow with nodes and edges
```

**Key Methods**:

- `setup_agent()` - Initialize components
- `build_graph()` - Define workflow
- `invoke()`/`ainvoke()` - Execute agent

### 2. State Management

Every agent needs a state schema:

```python
class MyState(StateSchema):
    messages: List[BaseMessage] = Field(default_factory=list)
    custom_field: str = Field(default="")
```

**Schema Composition**:

- `SchemaComposer` - Dynamically builds schemas
- `AgentSchemaComposer` - Multi-agent schema merging
- Fields auto-sync from engines

### 3. Engine System

**AugLLMEngine** is the core:

- Handles LLM + tools
- Provides structured output
- Routes tools (langchain_tool, pydantic_model, function)
- Must be registered in EngineRegistry

### 4. Graph Building Patterns

```python
def build_graph(self) -> BaseGraph:
    graph = BaseGraph()

    # Add nodes
    graph.add_node("agent", EngineNodeConfig(engine=self.engine))
    graph.add_node("tools", ToolNodeConfig(engine_name=self.engine.name))

    # Add edges
    graph.add_edge(START, "agent")
    graph.add_conditional_edges("agent", route_function, routing_map)

    return graph
```

**Node Types**:

- `EngineNodeConfig` - LLM execution
- `ToolNodeConfig` - Tool execution
- `ValidationNodeConfig` - Output validation
- `ParserNodeConfig` - Output parsing

### 5. Multi-Agent Composition

```python
# Pattern 1: Sequential
agents = [agent1, agent2, agent3]
multi = MultiAgent(agents=agents, coordination_mode="sequential")

# Pattern 2: Wrapper (like StructuredOutputAgent)
class WrapperAgent(MultiAgent):
    def __init__(self, inner_agent, **kwargs):
        transform_agent = self._create_transformer()
        super().__init__(agents=[inner_agent, transform_agent])
```

### 6. Tool Integration

```python
# Tools become part of engine
@tool
def my_tool(param: str) -> str:
    """Tool description"""
    return result

engine = AugLLMConfig(tools=[my_tool])
```

**Tool Routes**:

- `langchain_tool` → ToolNode
- `pydantic_model` → ParserNode
- `function` → Direct call

### 7. Structured Output

**Three approaches**:

1. **Engine-level**: `structured_output_model` in AugLLMConfig
2. **Mixin-level**: Use OutputMixin for transformation
3. **Wrapper-level**: StructuredOutputAgent composition

### 8. Common Patterns

**SimpleAgent Pattern**:

- Modifies engine schema for structured output
- Auto-detects needed nodes (tool, parser, validation)
- Handles routing based on tool calls

**RAG Pattern**:

- State includes `query` and `retrieved_documents`
- Simple linear flow: retrieve → output

**React Pattern**:

- Reasoning + action loop
- Tool use with reflection
- Iterative until solution

### 9. Key Infrastructure

**Mixins** provide capabilities:

- `ExecutionMixin` - run/stream/invoke
- `StateMixin` - state management
- `PersistenceMixin` - checkpointing
- `OutputMixin` - output transformation

**Registries** manage global state:

- `EngineRegistry` - Engine discovery
- `ToolRegistry` - Tool management

### 10. Development Workflow

1. Define state schema
2. Create/configure engine
3. Build graph (nodes + edges)
4. Test with real inputs
5. Add error handling
6. Document patterns

## Key Insights

- **Composition over inheritance** - Use mixins and wrappers
- **Schema-first design** - State drives everything
- **Graph-based workflows** - Explicit control flow
- **Type safety everywhere** - Pydantic validates all
- **Engine abstraction** - Swappable LLM backends

This is the foundation for building any agent in Haive!
