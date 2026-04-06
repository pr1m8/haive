# Custom Nodes & Graph Design Guide

**Created**: 2026-04-06
**Purpose**: How to build custom nodes, graphs, and extend agent functionality

## Node Types in Haive

### 1. GenericEngineNodeConfig (LLM execution)

The standard node for LLM calls. Used by SimpleAgent's `agent_node`.

```python
from haive.core.graph.node.engine_node_generic import GenericEngineNodeConfig

agent_node = GenericEngineNodeConfig(
    name="agent_node",
    engine=my_augllm_config,  # Direct engine reference
)
```

What it does:
- Extracts messages from state
- Invokes LLM with system message + tools
- Returns `{"messages": [AIMessage(...)]}`

### 2. ToolNodeConfig (Tool execution)

Handles tool calls from AIMessage. Used after validation routing.

```python
from haive.core.graph.node.tool_node_config_v2 import ToolNodeConfig

tool_node = ToolNodeConfig(
    name="tool_node",
    engine_name="engine_abc123",  # Looks up state.engines[name].tools
    # OR
    tools=[my_tool1, my_tool2],   # Direct tool list (preferred)
)
```

What it does:
- Gets tools from state.engines or direct list
- Filters by tool_routes (langchain_tool, function, etc.)
- Delegates to LangGraph's ToolNode for execution
- Returns `{"messages": [ToolMessage(...)]}`

### 3. ValidationNodeConfigV2 (Routing)

Routes based on AIMessage content: tool_calls → tool_node, end → END.

```python
from haive.core.graph.node.validation_node_config_v2 import ValidationNodeConfigV2

validation = ValidationNodeConfigV2(
    name="validation",
    engine_name="engine_abc123",
    tool_node="tool_node",
    parser_node="parse_output",
)
```

### 4. Custom Callable Nodes

Any function or callable that takes state and returns a dict update.

```python
def my_custom_node(state):
    """Custom processing node."""
    messages = state.get("messages", []) if isinstance(state, dict) else getattr(state, "messages", [])

    # Your logic here
    processed = do_something(messages)

    # Return partial state update
    return {"custom_field": processed}
```

## Building a Custom Graph

### Step 1: Define State Schema

```python
from haive.core.schema.prebuilt.llm_state import LLMState
from pydantic import Field

class MyWorkflowState(LLMState):
    """State for my custom workflow."""
    plan: str = ""
    iteration: int = 0
    max_iterations: int = 3
    done: bool = False
```

### Step 2: Define Nodes

```python
def plan_node(state: dict) -> dict:
    """Create a plan from the user's request."""
    messages = state.get("messages", [])
    # Use LLM to create plan (could use agent internally)
    return {"plan": "Step 1: ..., Step 2: ...", "iteration": 0}

def execute_node(state: dict) -> dict:
    """Execute one step of the plan."""
    plan = state.get("plan", "")
    iteration = state.get("iteration", 0)
    # Execute step
    return {"iteration": iteration + 1}

def check_done(state: dict) -> str:
    """Route: continue or finish."""
    if state.get("iteration", 0) >= state.get("max_iterations", 3):
        return "done"
    if state.get("done", False):
        return "done"
    return "continue"
```

### Step 3: Build Graph

```python
from haive.core.graph.state_graph.base_graph2 import BaseGraph
from langgraph.graph import START, END

graph = BaseGraph(name="plan_execute")
graph.set_state_schema(MyWorkflowState)

# Add nodes
graph.add_node("plan", plan_node)
graph.add_node("execute", execute_node)

# Add edges
graph.add_edge(START, "plan")
graph.add_edge("plan", "execute")

# Conditional routing
graph.add_conditional_edges("execute", check_done, {
    "continue": "execute",  # Loop
    "done": END,
})

# Compile
lg = graph.to_langgraph()
app = lg.compile()

# Run
result = app.invoke({"messages": [HumanMessage(content="Build a web app")]})
```

### Step 4: Wrap in Agent Class

```python
class PlanExecuteAgent(ReactAgent):
    """Agent that plans and executes iteratively."""

    max_plan_iterations: int = Field(default=3)

    def build_graph(self) -> BaseGraph:
        graph = BaseGraph(name=f"{self.name}_graph")
        graph.set_state_schema(MyWorkflowState)

        # LLM node for planning
        plan_config = GenericEngineNodeConfig(
            name="planner", engine=self.engine,
        )
        graph.add_node("planner", plan_config)

        # Custom execution node
        graph.add_node("executor", self._execute_step)

        # Routing
        graph.add_edge(START, "planner")
        graph.add_edge("planner", "executor")
        graph.add_conditional_edges("executor", self._check_done, {
            "continue": "planner",
            "done": END,
        })

        return graph

    def _execute_step(self, state):
        # Custom logic
        return {"iteration": state.get("iteration", 0) + 1}

    def _check_done(self, state):
        if state.get("iteration", 0) >= self.max_plan_iterations:
            return "done"
        return "continue"
```

## Advanced Graph Patterns

### Branching (Conditional Fan-Out)

```python
graph.add_conditional_edges("classifier", classify_fn, {
    "simple": "simple_handler",
    "complex": "complex_handler",
    "error": "error_handler",
})
```

### Parallel Processing (LangGraph Send)

```python
from langgraph.constants import Send

def fan_out(state):
    """Send work to multiple parallel nodes."""
    chunks = state.get("chunks", [])
    return [Send("process_chunk", {"chunk": c, "index": i})
            for i, c in enumerate(chunks)]

graph.add_conditional_edges("splitter", fan_out)
```

### Sub-Graphs (Agent as Node)

```python
def agent_as_node(state):
    """Run a full agent as a single node."""
    sub_agent = ReactAgent(name="sub", engine=config, tools=[...])
    result = sub_agent.run(state.get("messages", []))
    return {"messages": result.messages if hasattr(result, "messages") else []}

graph.add_node("sub_agent", agent_as_node)
```

### Reflection Loop

```python
# Pattern: generate → reflect → revise → check → (loop or end)

graph.add_edge(START, "generate")
graph.add_edge("generate", "reflect")
graph.add_edge("reflect", "revise")
graph.add_conditional_edges("revise", quality_check, {
    "good": END,
    "needs_work": "reflect",  # Loop back
})
```

## Node Design Rules

1. **Input**: Receives full state (dict or Pydantic model)
2. **Output**: Returns **partial** update dict (only changed fields)
3. **Messages**: Use `add_messages` reducer — append, don't replace
4. **Errors**: Catch and return error state, don't raise (graph will halt)
5. **Side effects**: OK for logging, store writes, API calls
6. **Idempotent**: Nodes may be retried — design for idempotency

## Integration with Agent System

### NodeConfig Objects

For LLM/tool nodes, use NodeConfig instead of plain functions:

```python
# LLM node
agent_node = GenericEngineNodeConfig(name="agent", engine=config)

# Tool node
tool_node = ToolNodeConfig(name="tools", tools=[my_tools])

# Validation/routing
validation = ValidationNodeConfigV2(name="route", engine_name=config.name)
```

### Using in Agent.build_graph()

```python
class MyAgent(Agent):
    def build_graph(self) -> BaseGraph:
        graph = BaseGraph(name=f"{self.name}_graph")
        graph.set_state_schema(LLMState)

        # Mix NodeConfig and custom functions
        graph.add_node("llm", GenericEngineNodeConfig(name="llm", engine=self.engine))
        graph.add_node("custom", self._my_custom_logic)
        graph.add_node("tools", ToolNodeConfig(name="tools", tools=self.engine.tools))

        graph.add_edge(START, "llm")
        graph.add_edge("llm", "custom")
        graph.add_edge("custom", "tools")
        graph.add_edge("tools", END)

        return graph
```

## Related Guides

- [Agent Design Patterns](AGENT_DESIGN_PATTERNS.md) — How to build agents
- [MultiAgent State Design](MULTIAGENT_STATE_DESIGN.md) — Complex state for multi-agent
- [Memory Agent Guide](MEMORY_AGENT_GUIDE.md) — Memory + KG integration
- [State Schema Notes](STATE_SCHEMA_NOTES.md) — State schema research and bugs
- [State Schema Engine Gap](../../active/architecture/state_schema_engine_gap.md) — Architecture analysis
