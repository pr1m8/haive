# Agent Design Patterns — How to Build Haive Agents

**Created**: 2026-04-06
**Purpose**: Comprehensive guide for designing agents around BaseGraph, state schemas, and agent composition

## Core Architecture

```
Agent (Pydantic BaseModel)
├── engine: AugLLMConfig          # LLM + tools + routing
├── engines: dict[str, Engine]    # Named engine registry
├── state_schema: type            # Pydantic model for graph state
├── graph: BaseGraph              # Graph builder (→ LangGraph StateGraph)
├── _app: CompiledStateGraph      # Compiled LangGraph (from compile())
└── Methods:
    ├── build_graph() → BaseGraph  # Abstract: define nodes + edges
    ├── compile() → CompiledGraph  # BaseGraph.to_langgraph() + compile
    └── run(input) → result        # _prepare_input → _app.invoke → _process_output
```

## How Agents Work (The Flow)

```
1. __init__() → Pydantic validates fields
2. model_post_init() → _setup_schemas() generates state_schema
3. build_graph() → Creates BaseGraph with nodes + edges
4. compile() → graph.to_langgraph() → StateGraph → .compile() → _app
5. run(input) → _prepare_input → _app.invoke(input) → _process_output
```

### Key: State Schema Determines Everything

The `state_schema` defines what data flows through the graph. Each node receives
the full state and returns a partial update dict.

```python
# State = what flows through the graph
class MyState(LLMState):
    messages: list[BaseMessage]  # Inherited: conversation history
    engines: dict[str, Engine]   # Inherited: engine registry for tool_node
    custom_field: str = ""       # Your custom data

# Node = receives state, returns partial update
def my_node(state: MyState) -> dict:
    return {"custom_field": "updated"}
```

**Rule: If your agent has tools, use LLMState (or a subclass) as state_schema.**
LLMState includes `engines`, `tools`, `tool_routes` — required by tool_node.

## Building an Agent: Step by Step

### 1. SimpleAgent (no tools, just LLM)

```python
from haive.agents.simple.agent import SimpleAgent
from haive.core.engine.aug_llm import AugLLMConfig

agent = SimpleAgent(
    name="writer",
    engine=AugLLMConfig(
        temperature=0.8,
        system_message="You are a creative writer.",
    ),
)
result = agent.run("Write a haiku about AI")
```

Graph: `START → agent_node → END`

### 2. ReactAgent (LLM + tools, reasoning loop)

```python
from haive.agents.react.agent import ReactAgent
from langchain_core.tools import tool

@tool
def search(query: str) -> str:
    '''Search the web.'''
    return f"Results for: {query}"

agent = ReactAgent(
    name="researcher",
    engine=AugLLMConfig(tools=[search], system_message="Use search tool."),
    max_iterations=5,
)
result = agent.run("Find info about quantum computing")
```

Graph: `START → agent_node → [tool_calls?] → tool_node → agent_node → ... → END`

### 3. MemoryAgent (ReactAgent + persistent memory)

```python
from haive.agents.memory import create_memory_agent

agent = create_memory_agent(
    name="assistant",
    user_id="user123",
    connection_string="postgresql://haive:haive@localhost/haive",
)
```

### 4. MultiAgent (compose multiple agents)

```python
from haive.agents.multi.agent import MultiAgent

multi = MultiAgent(
    name="pipeline",
    agents=[researcher, writer, reviewer],
    execution_mode="sequential",  # or "parallel", "conditional"
)
result = multi.run("Create a report on AI safety")
```

## BaseGraph: The Graph Builder

BaseGraph wraps LangGraph's StateGraph with a higher-level API.

```python
from haive.core.graph.state_graph.base_graph2 import BaseGraph
from langgraph.graph import START, END

graph = BaseGraph(name="my_graph")
graph.set_state_schema(MyState)

# Add nodes (NodeConfig objects or callables)
graph.add_node("step1", my_node_function)
graph.add_node("step2", another_node)

# Add edges
graph.add_edge(START, "step1")
graph.add_edge("step1", "step2")
graph.add_edge("step2", END)

# Conditional routing
graph.add_conditional_edges("step1", routing_fn, {"a": "step2", "b": END})

# Compile
lg = graph.to_langgraph()  # → LangGraph StateGraph
app = lg.compile()         # → CompiledStateGraph
```

### BaseGraph vs Raw StateGraph

| Feature | BaseGraph | Raw StateGraph |
|---------|-----------|----------------|
| Node configs | GenericEngineNodeConfig, ToolNodeConfig | Plain callables |
| State schema | set_state_schema() | StateGraph(schema) |
| Engine integration | Automatic via node configs | Manual |
| Tool routing | ValidationNode + ToolNode | Build yourself |
| Compilation | to_langgraph() → compile() | compile() |

**Use BaseGraph** for agents (has engine/tool integration).
**Use raw StateGraph** only for simple workflows without LLM engines.

## State Schema Design

### For Agents with Tools → Use LLMState

```python
from haive.core.schema.prebuilt.llm_state import LLMState

class MyAgentState(LLMState):
    """Extends LLMState with custom fields."""
    plan: str = ""
    iteration: int = 0
```

LLMState inherits: messages, engines, tools, tool_routes, token_usage, etc.

### For Tool-less Agents → MessagesState is fine

```python
from haive.core.schema.prebuilt.messages_state import MessagesState

class SimpleState(MessagesState):
    custom_data: str = ""
```

### For MultiAgent → MultiAgentState

```python
from haive.core.schema.prebuilt.multi_agent_state import MultiAgentState

# Already has: agents dict, agent_states, agent_outputs, execution tracking
```

### State Schema Rules

1. **All fields need defaults** — state is initialized empty, nodes return partial updates
2. **messages uses Annotated reducer** — appends instead of replaces
3. **engines must be in state** for tool_node to work (LLMState includes this)
4. **Custom fields** are simple Pydantic fields with defaults

## MultiAgent Patterns

### Sequential: A → B → C

```python
multi = MultiAgent(
    name="pipeline",
    agents=[planner, executor, reviewer],
    execution_mode="sequential",
)
```

Each agent sees messages from all prior agents.

### Parallel: [A, B, C] → merge

```python
multi = MultiAgent(
    name="research",
    agents=[analyst1, analyst2, analyst3],
    execution_mode="parallel",
)
```

All agents run concurrently, results merged.

### Dynamic (DynamicSupervisor)

```python
from haive.agents.supervisor.dynamic.dynamic_supervisor import DynamicSupervisor

supervisor = DynamicSupervisor(
    name="coordinator",
    engine=AugLLMConfig(system_message="Route tasks to agents."),
)
supervisor.add_agent(math_agent)
supervisor.add_agent(writer_agent)
# Supervisor decides which agent to call based on input
```

### How State Flows in MultiAgent

```
MultiAgentState
├── messages: list[BaseMessage]         # Shared across all agents
├── agents: dict[str, Agent]            # Agent instances
├── agent_states: dict[str, dict]       # Per-agent state snapshots
├── agent_outputs: dict[str, Any]       # Per-agent outputs
└── execution_tracking: dict            # Execution metadata

_create_agent_wrapper():
  1. Extracts messages from MultiAgentState
  2. Injects agent's engines dict
  3. Invokes agent._app.invoke({"messages": [...], "engines": {...}})
  4. Returns updated messages + agent_states + agent_outputs
```

## Custom Agent Pattern

```python
class MyCustomAgent(ReactAgent):
    """Custom agent with specific behavior."""

    # Custom config fields
    my_param: str = Field(default="value")

    # Custom state
    # (override state_schema in build_graph or via set_schema=True)

    def build_graph(self) -> BaseGraph:
        # Start with parent's graph
        graph = super().build_graph()

        # Add custom nodes
        graph.add_node("my_custom_step", self._custom_node)
        graph.add_edge("agent_node", "my_custom_step")
        graph.add_edge("my_custom_step", END)

        return graph

    def _custom_node(self, state):
        # Your custom logic
        return {"messages": [...]}

    def run(self, input_data, **kwargs):
        # Custom pre/post processing
        result = super().run(input_data, **kwargs)
        # Post-processing
        return result
```

## Anti-Patterns to Avoid

1. **Don't override `__init__`** — use `model_post_init()` or Pydantic Fields
2. **Don't use raw StateGraph** when you need tools — use BaseGraph
3. **Don't auto-compose schemas** when tools are present — use LLMState
4. **Don't pass tools via `self.tools`** — pass via `AugLLMConfig(tools=[...])`
5. **Don't call `state.dict()`** in nodes — it serializes BaseMessage to dicts
6. **Don't forget engines in state** — tool_node needs `state.engines[name].tools`

## Debug & Trace

```python
from haive.agents.utils.trace import run_traced

# Pretty-print any agent execution
result = run_traced(agent, "Hello", save_to="traces/")
```
