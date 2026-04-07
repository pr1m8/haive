# MultiAgent State Design Guide

**Created**: 2026-04-06
**Purpose**: How to design complex state schemas for multi-agent systems

## MultiAgent Architecture

```
MultiAgent(Agent)
├── agents: list[Agent]              # Child agents
├── execution_mode: str              # "sequential" | "parallel" | "conditional"
├── state_schema: MultiAgentState    # Pre-built, NOT auto-composed
├── build_graph() → BaseGraph        # Creates wrapper nodes per agent
└── _create_agent_wrapper()          # Bridges MultiAgentState ↔ child state
```

## How MultiAgent State Works

### MultiAgentState (default)

```python
class MultiAgentState(ToolState):
    """State for multi-agent coordination."""
    messages: Annotated[list[BaseMessage], add_messages]  # Shared conversation
    agents: dict[str, Agent] = {}                         # Agent instances
    agent_states: dict[str, dict] = {}                    # Per-agent snapshots
    agent_outputs: dict[str, Any] = {}                    # Per-agent results
    current_agent: str = ""                               # Currently executing
    execution_order: list[str] = []                        # Execution history
```

### State Flow: Sequential Mode

```
Input: {"messages": [HumanMessage("Write a report")]}

Step 1: Agent "researcher"
  Input:  {"messages": [HumanMessage], "engines": researcher.engines}
  Output: {"messages": [HumanMessage, AIMessage("Research findings...")]}

Step 2: Agent "writer"
  Input:  {"messages": [HumanMessage, AIMessage("Research findings...")], "engines": writer.engines}
  Output: {"messages": [HumanMessage, AIMessage, AIMessage("Report: ...")]}

Final: {"messages": [HumanMessage, AIMessage, AIMessage], "agent_outputs": {...}}
```

### State Flow: Parallel Mode

```
Input: {"messages": [HumanMessage("Analyze X")]}

Parallel:
  Agent "analyst1" → [HumanMessage, AIMessage("Analysis A")]
  Agent "analyst2" → [HumanMessage, AIMessage("Analysis B")]

Merge: {"messages": [HumanMessage, AIMessage("A"), AIMessage("B")]}
```

## Designing Custom Multi-Agent States

### Pattern 1: Shared Context

```python
class ResearchPipelineState(MultiAgentState):
    """State with shared research context."""
    research_topic: str = ""
    findings: list[str] = Field(default_factory=list)
    current_phase: str = "planning"  # planning → research → writing → review

    # Shared across all agents
    domain: str = ""
    constraints: list[str] = Field(default_factory=list)
```

### Pattern 2: Agent-Specific Sub-States

```python
class TeamState(MultiAgentState):
    """State with per-agent typed sub-states."""
    # Shared
    project_goal: str = ""
    deadline: str = ""

    # Agent-specific (stored in agent_states dict)
    # Access: state.agent_states["planner"]["plan"]
    # Access: state.agent_states["coder"]["code"]
```

Agent wrappers read from `agent_states[name]` and write back:

```python
def _custom_wrapper(state, config):
    my_state = state.agent_states.get("planner", {})
    plan = my_state.get("plan", "")
    # ... execute with plan context ...
    return {
        "messages": [...],
        "agent_states": {**state.agent_states, "planner": {"plan": new_plan}}
    }
```

### Pattern 3: Conditional Routing State

```python
class RouterState(MultiAgentState):
    """State for conditional agent routing."""
    task_type: str = ""       # "math" | "writing" | "research"
    complexity: float = 0.0   # 0-1, determines which agent handles it
    requires_tools: bool = False

# Routing function
def route_task(state: RouterState) -> str:
    if state.task_type == "math":
        return "math_agent"
    elif state.complexity > 0.7:
        return "expert_agent"
    else:
        return "simple_agent"
```

### Pattern 4: Accumulator State (Map-Reduce)

```python
class MapReduceState(MultiAgentState):
    """State for parallel processing with accumulation."""
    chunks: list[str] = Field(default_factory=list)    # Input chunks
    chunk_results: list[str] = Field(default_factory=list)  # Per-chunk results
    final_result: str = ""                              # Reduced output
    current_chunk_idx: int = 0
```

## MultiAgent with Tools

When child agents have tools, engines must flow through:

```python
# The wrapper automatically injects engines now:
agent_input = {"messages": messages}
if hasattr(agent, "engines") and agent.engines:
    agent_input["engines"] = agent.engines
```

So child ReactAgents with tools work correctly in MultiAgent.

## Building Complex Multi-Agent Systems

### Research Pipeline Example

```python
from haive.agents.react.agent import ReactAgent
from haive.agents.simple.agent import SimpleAgent
from haive.agents.multi.agent import MultiAgent
from langchain_core.tools import tool

@tool
def web_search(query: str) -> str:
    '''Search the web.'''
    return f"Results for {query}"

# Step 1: Researcher (ReactAgent with tools)
researcher = ReactAgent(
    name="researcher",
    engine=AugLLMConfig(
        tools=[web_search],
        system_message="Research the topic thoroughly. Use web_search.",
    ),
    max_iterations=3,
)

# Step 2: Analyzer (SimpleAgent, structured output)
analyzer = SimpleAgent(
    name="analyzer",
    engine=AugLLMConfig(
        temperature=0.2,
        system_message="Analyze the research findings. Identify key insights.",
    ),
)

# Step 3: Writer (SimpleAgent)
writer = SimpleAgent(
    name="writer",
    engine=AugLLMConfig(
        temperature=0.7,
        system_message="Write a clear, engaging report based on the analysis.",
    ),
)

# Compose
pipeline = MultiAgent(
    name="research_pipeline",
    agents=[researcher, analyzer, writer],
    execution_mode="sequential",
)

result = pipeline.run("Research AI safety approaches in 2025")
```

### Dynamic Supervisor Example

```python
from haive.agents.supervisor.dynamic.dynamic_supervisor import DynamicSupervisor

supervisor = DynamicSupervisor(
    name="team_lead",
    engine=AugLLMConfig(
        system_message="You coordinate a team. Route tasks to the right agent.",
    ),
)

# Add agents dynamically
supervisor.add_agent(researcher, description="Researches topics using web search")
supervisor.add_agent(writer, description="Writes reports and content")
supervisor.add_agent(coder, description="Writes and debugs code")

# Supervisor decides routing
result = supervisor.run("Write a Python script that fetches weather data")
```

## State Schema Checklist

When designing a multi-agent state:

- [ ] Extend `MultiAgentState` (or `ToolState` if custom)
- [ ] Include `messages: Annotated[list, add_messages]` for conversation
- [ ] All fields have defaults (state starts empty)
- [ ] Shared data in top-level fields
- [ ] Per-agent data in `agent_states` dict
- [ ] If routing needed, add routing fields (task_type, complexity, etc.)
- [ ] If accumulating, add accumulator fields (chunks, results, etc.)

## Common Pitfalls

1. **Schema flattening** — Don't merge all agent schemas into one flat schema. Use `agent_states` dict for per-agent data.

2. **Missing engines** — If child agent has tools but state doesn't have `engines`, tool_node fails. Fixed: wrapper now injects engines.

3. **Message ordering** — In parallel mode, message order is non-deterministic. Don't rely on position.

4. **State mutation** — Don't mutate state directly. Return update dicts from nodes.

5. **Circular dependencies** — Agent A needs output of Agent B, and B needs A. Use conditional routing or iterative patterns instead.
