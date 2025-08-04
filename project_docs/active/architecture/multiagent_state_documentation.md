# MultiAgentState Documentation

**Version**: 1.0
**Purpose**: Comprehensive guide to MultiAgentState for multi-agent coordination
**Last Updated**: 2025-01-16

## 🎯 Overview

`MultiAgentState` is the foundation for coordinating multiple agents in Haive without schema flattening. It provides hierarchical state management, execution tracking, and recompilation support while maintaining type safety for each agent's individual schema.

## 🏗️ Architecture

### Core Concepts

- **No Schema Flattening**: Each agent maintains its own schema independently
- **Hierarchical State**: Agents stored as first-class fields with isolated states
- **Execution Tracking**: Full tracking of agent execution order and outputs
- **Recompilation Support**: Dynamic agent updates with recompilation management
- **Engine Syncing**: Automatic engine synchronization from agents to parent state

### Inheritance Hierarchy

```
MultiAgentState extends ToolState
├── Inherits from ToolState (tools + tool routing)
├── Inherits from MessagesStateWithTokenUsage (messages + token tracking)
├── Adds agent management capabilities
├── Adds execution coordination
└── Adds recompilation tracking
```

## 📋 Key Fields

### Agent Management

- `agents: Dict[str, Agent]` - Agent instances (auto-converts from list)
- `agent_states: Dict[str, Dict[str, Any]]` - Isolated state for each agent
- `active_agent: str | None` - Currently executing agent

### Execution Tracking

- `agent_outputs: Dict[str, Any]` - Outputs from each agent execution
- `agent_execution_order: List[str]` - Order of agent execution
- `agent_count: int` - Computed field for number of agents

### Recompilation Support

- `agents_needing_recompile: Set[str]` - Agents needing recompilation
- `recompile_count: int` - Total recompilations performed
- `recompile_history: List[Dict[str, Any]]` - Recompilation event history

## 💻 Usage Patterns

### 1. Basic Multi-Agent Setup

```python
from haive.core.schema.prebuilt.multi_agent_state import MultiAgentState
from haive.agents.simple.agent import SimpleAgent
from haive.agents.react.agent import ReactAgent

# Create agents
planner = SimpleAgent(name="planner")
executor = ReactAgent(name="executor", tools=[search_tool])

# Initialize with list (auto-converts to dict)
state = MultiAgentState(agents=[planner, executor])

# Or initialize with dict directly
state = MultiAgentState(agents={
    "plan": planner,
    "exec": executor
})

# Access agents
planner_agent = state.get_agent("plan")
print(f"Agent count: {state.agent_count}")
```

### 2. Hierarchical State Management

```python
# Get agent's isolated state
planner_state = state.get_agent_state("plan")

# Update agent state
state.update_agent_state("plan", {
    "current_step": 1,
    "tasks": ["research", "analyze", "summarize"]
})

# Record agent output
state.record_agent_output("plan", {
    "plan_created": True,
    "next_steps": ["execute_step_1", "execute_step_2"]
})

# Set active agent
state.set_active_agent("exec")
```

### 3. Execution Coordination

```python
# Track execution order
state.agent_execution_order = ["planner", "executor", "validator"]

# Check execution status
if state.has_active_agent:
    current = state.active_agent
    print(f"Currently executing: {current}")

# Get agent outputs
for agent_name in state.agent_execution_order:
    output = state.get_agent_output(agent_name)
    if output:
        print(f"{agent_name} completed: {output}")
```

### 4. Recompilation Management

```python
# Mark agent for recompilation
state.mark_agent_for_recompile("planner", "Tool configuration changed")

# Check recompilation status
if state.needs_any_recompile:
    agents_to_recompile = state.get_agents_needing_recompile()
    print(f"Agents needing recompile: {agents_to_recompile}")

# Resolve recompilation
state.resolve_agent_recompile("planner")
print(f"Total recompiles: {state.recompile_count}")
```

## 🚀 Plan and Execute Agent Example

The Plan and Execute agent demonstrates advanced MultiAgentState usage:

### P&E State Schema

```python
from haive.core.schema.prebuilt.multi_agent_state import MultiAgentState
from haive.agents.planning.plan_and_execute.v2.models import Plan, Step

class PlanAndExecuteState(MultiAgentState):
    """State for Plan and Execute Agent v2."""

    # P&E specific fields
    input: str = Field(..., description="Original user query")
    plan: Optional[Plan] = Field(default=None, description="Current plan")
    past_steps: List[Step] = Field(default_factory=list, description="Completed steps")
    response: Optional[str] = Field(default=None, description="Current response")
    final_response: Optional[str] = Field(default=None, description="Final response")

    # Inherited from MultiAgentState:
    # - agents: Dict[str, Agent]
    # - agent_states: Dict[str, Dict[str, Any]]
    # - agent_outputs: Dict[str, Any]
    # - execution tracking fields
    # - recompilation fields

    def update_past_steps(self, step: Step) -> None:
        """Add completed step to past_steps."""
        if step.is_complete():
            self.past_steps.append(step)
            if self.plan:
                self.plan.update_status()
```

### P&E Agent Implementation

```python
from haive.agents.multi.proper_base import ProperMultiAgent
from haive.agents.simple.agent import SimpleAgent
from haive.agents.react.agent import ReactAgent

class PlanAndExecuteAgent(ProperMultiAgent):
    """Plan and Execute agent using multi-agent sequential pattern."""

    @classmethod
    def create_default(cls, tools: list = None, **kwargs):
        """Create P&E agent with default configuration."""

        # Create planner agent
        planner_agent = SimpleAgent(
            name="planner",
            engine=AugLLMConfig(
                prompt_template=PLANNER_PROMPT,
                structured_output_model=Plan,
                temperature=0.7
            )
        )

        # Create executor agent (ReactAgent with tools)
        executor_agent = ReactAgent(
            name="executor",
            engine=AugLLMConfig(
                prompt_template=EXECUTOR_PROMPT,
                structured_output_model=ExecutionResult,
                temperature=0.3
            ),
            tools=tools or []
        )

        # Create replanner agent
        replanner_agent = SimpleAgent(
            name="replanner",
            engine=AugLLMConfig(
                prompt_template=REPLANNER_PROMPT,
                structured_output_model=Act,
                temperature=0.5
            )
        )

        # Create sequential multi-agent
        name = kwargs.pop("name", "Plan and Execute Agent")
        return cls(
            name=name,
            agents=[planner_agent, executor_agent, replanner_agent],
            execution_mode="sequential",
            state_schema=PlanAndExecuteState,
            **kwargs
        )
```

### P&E Usage Example

```python
from haive.agents.planning.plan_and_execute.v2.agent import PlanAndExecuteAgent
from haive.tools.tools.search_tools import tavily_search_tool

# Create P&E agent
pe_agent = PlanAndExecuteAgent.create_default(
    tools=[tavily_search_tool],
    name="research_agent"
)

# Execute complex task
result = await pe_agent.arun("Research latest AI developments and create a summary")

# The MultiAgentState handles:
# 1. Sequential execution: planner → executor → replanner
# 2. State isolation: each agent has its own state
# 3. Output tracking: plan creation, execution results, final response
# 4. Engine management: all agent engines accessible hierarchically
```

## 🔄 Engine Synchronization

MultiAgentState automatically syncs engines from agents to parent state:

```python
# If agents have engines:
planner.engines = {"main": planner_engine}
executor.engines = {"main": executor_engine, "tool_router": tool_engine}

# MultiAgentState creates:
state.engines = {
    "planner.main": planner_engine,
    "executor.main": executor_engine,
    "executor.tool_router": tool_engine,
    "main": planner_engine,  # First main engine as default
    "tool_router": tool_engine  # Non-conflicting names
}
```

## 🐛 Debug Visualization

MultiAgentState provides rich debug visualization:

```python
# Display comprehensive debug info
state.display_debug_info("My Multi-Agent System")

# Display agent status table
state.display_agent_table()

# Create custom table
table = state.create_agent_table()
console.print(table)
```

The debug output includes:

- **Agent Overview**: Agent types, status, and indicators
- **State Hierarchy**: Global fields and agent-specific states
- **Execution Status**: Active agent, execution order, outputs
- **Engine Management**: Hierarchical engine organization
- **Recompilation Status**: Agents needing recompile and history

## 📊 State Lifecycle

### 1. Initialization

```python
state = MultiAgentState(agents=[agent1, agent2])
# Auto-converts to dict, initializes agent_states, syncs engines
```

### 2. Execution Phase

```python
state.set_active_agent("planner")
# Agent executes, state.record_agent_output() called
state.set_active_agent("executor")
# Next agent executes
```

### 3. State Management

```python
# Each agent has isolated state
planner_state = state.get_agent_state("planner")
state.update_agent_state("planner", {"status": "complete"})
```

### 4. Recompilation

```python
# Mark for recompilation when needed
state.mark_agent_for_recompile("planner", "Tools changed")
# Graph rebuilds, then resolve
state.resolve_agent_recompile("planner")
```

## 🎯 Best Practices

### 1. State Schema Design

```python
# ✅ CORRECT - Inherit from MultiAgentState
class MyMultiAgentState(MultiAgentState):
    # Add your specific fields
    task_id: str = Field(...)
    progress: float = Field(default=0.0)

# ❌ WRONG - Don't inherit from StateSchema directly
class MyState(StateSchema):
    agents: Dict[str, Agent] = Field(...)  # Missing all the management logic
```

### 2. Agent Management

```python
# ✅ CORRECT - Use the management methods
state.update_agent_state("planner", {"step": 1})
state.record_agent_output("planner", result)

# ❌ WRONG - Direct state manipulation
state.agent_states["planner"]["step"] = 1  # Bypasses validation
```

### 3. Execution Tracking

```python
# ✅ CORRECT - Set execution order
state.agent_execution_order = ["planner", "executor", "validator"]

# ✅ CORRECT - Track active agent
state.set_active_agent("planner")

# ❌ WRONG - Direct assignment without validation
state.active_agent = "nonexistent_agent"  # Could cause errors
```

### 4. Recompilation Management

```python
# ✅ CORRECT - Provide reason for recompilation
state.mark_agent_for_recompile("planner", "Tool configuration changed")

# ✅ CORRECT - Check before recompiling
if state.needs_any_recompile:
    # Trigger recompilation
    state.resolve_agent_recompile("planner")
```

## 🚨 Common Pitfalls

### 1. Schema Flattening

```python
# ❌ WRONG - Trying to flatten schemas
class FlattenedState(MultiAgentState):
    planner_step: int = Field(...)  # Don't do this!
    executor_result: str = Field(...)  # Each agent should manage its own state

# ✅ CORRECT - Use hierarchical state
state.update_agent_state("planner", {"step": 1})
state.update_agent_state("executor", {"result": "..."})
```

### 2. Direct Agent State Access

```python
# ❌ WRONG - Direct access
state.agent_states["planner"]["step"] = 1

# ✅ CORRECT - Use methods
state.update_agent_state("planner", {"step": 1})
```

### 3. Engine Conflicts

```python
# ❌ WRONG - Engine name conflicts
agent1.engines = {"main": engine1}
agent2.engines = {"main": engine2}  # Conflict!

# ✅ CORRECT - Use namespaced access
engine1 = state.engines["agent1.main"]
engine2 = state.engines["agent2.main"]
```

## 📈 Performance Considerations

### 1. State Size Management

- Agent states are isolated - only update what's needed
- Use `get_agent_state()` to access specific agent data
- Avoid storing large objects in global state

### 2. Engine Efficiency

- Engines are synced once during initialization
- Namespaced access prevents conflicts
- Recompilation only affects agents that need it

### 3. Memory Usage

- Agents are stored as references, not copies
- State history is maintained for debugging
- Use `display_debug_info()` to monitor memory usage

## 🔗 Integration Points

### With ProperMultiAgent

```python
class MyMultiAgent(ProperMultiAgent):
    def setup_agent(self) -> None:
        # MultiAgentState is automatically used
        self.state_schema = MyMultiAgentState
        self.use_prebuilt_base = True
```

### With AgentNodeV3

```python
# AgentNodeV3 works seamlessly with MultiAgentState
# Agent execution is tracked automatically
# State updates are propagated correctly
```

### With Graph Execution

```python
# MultiAgentState integrates with LangGraph
# State updates follow graph execution patterns
# Recompilation triggers graph rebuilds
```

## 🎯 Summary

`MultiAgentState` provides:

1. **Hierarchical Management**: No schema flattening, isolated agent states
2. **Execution Coordination**: Track active agents, execution order, outputs
3. **Recompilation Support**: Dynamic agent updates with full history
4. **Engine Synchronization**: Automatic engine management with namespacing
5. **Debug Visualization**: Rich debug output for development and monitoring
6. **Type Safety**: Proper typing for all agent interactions

It's the foundation for all multi-agent patterns in Haive, providing the infrastructure needed for complex agent coordination while maintaining simplicity and type safety.

---

**See Also**:

- [ProperMultiAgent Documentation](proper_multi_agent_documentation.md)
- [Plan and Execute Agent v2](../../../packages/haive-agents/src/haive/agents/planning/plan_and_execute/v2/)
- [Agent-as-Tool Pattern](agent_as_tool_pattern.md)
