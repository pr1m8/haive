# MultiAgentBase Guide

A comprehensive guide to using the enhanced MultiAgentBase for flexible agent orchestration in the Haive framework.

## 📖 Table of Contents

- [Overview](#overview)
- [Key Concepts](#key-concepts)
- [API Reference](#api-reference)
- [Examples](#examples)
- [State Composition](#state-composition)
- [Build Modes](#build-modes)
- [Best Practices](#best-practices)
- [File Locations](#file-locations)

## Overview

The `MultiAgentBase` provides an elegant way to orchestrate multiple agents with conditional routing, shared state, and flexible schema composition. It combines the power of the Haive agent system with LangGraph's conditional edges.

### Key Features

- ✅ **Elegant API**: Simple `agents=[]`, `branches=[]` structure
- ✅ **Shared State**: Proper field sharing with BuildMode control
- ✅ **Conditional Routing**: Advanced branching logic from base_graph2
- ✅ **Schema Composition**: Automatic or manual state schema management
- ✅ **Tool Integration**: Works with existing Haive agents and tools

## Key Concepts

### 1. Agents

A list of Haive agents that will be orchestrated together:

```python
agents = [planner_agent, executor_agent, replanner_agent]
```

### 2. Branches

Conditional routing between agents using `(source, condition, destinations)` tuples:

```python
branches = [
    (executor, route_condition, {"continue": executor, "done": replanner}),
    (replanner, final_condition, {"restart": executor, END: END})
]
```

### 3. State Schema

Either automatically composed from agents or explicitly provided:

```python
state_schema_override = YourCustomState  # Optional
```

### 4. Build Modes

Control how agent schemas are composed:

- `BuildMode.PARALLEL` - Separate namespaces, shared fields where marked
- `BuildMode.SEQUENCE` - Sequential flow with state inheritance
- `BuildMode.HIERARCHICAL` - Parent-child relationships

## API Reference

### MultiAgentBase Constructor

```python
MultiAgentBase(
    agents: List[Agent],                              # Required: List of agents
    branches: Optional[List[tuple]] = None,           # Optional: Conditional routing
    state_schema_override: Optional[Type[StateSchema]] = None,  # Optional: Custom state
    schema_build_mode: BuildMode = BuildMode.SEQUENCE,          # Schema composition mode
    schema_separation: str = "smart",                 # Field separation strategy
    include_meta: bool = True,                        # Include coordination metadata
    entry_points: Optional[List[Union[str, Agent]]] = None,     # Entry points
    finish_points: Optional[List[Union[str, Agent]]] = None,    # Finish points
    workflow_nodes: Optional[Dict[str, Callable]] = None,      # Custom nodes
    create_missing_nodes: bool = False,               # Auto-create missing nodes
    name: str = "MultiAgentBase"                      # System name
)
```

### Branch Structure

Each branch is a tuple with 3-4 elements:

```python
(source_agent, condition_function, destinations, default)
```

- **source_agent**: Agent or agent name that triggers the condition
- **condition_function**: Function that takes state and returns routing key
- **destinations**: Dict mapping condition results to target agents
- **default**: Optional default destination if no condition matches

## Examples

### 1. Basic Plan & Execute System

```python
from haive.agents.multi.enhanced_base import MultiAgentBase
from haive.agents.simple.agent import SimpleAgent
from haive.agents.planning.p_and_e.state import PlanExecuteState
from haive.core.schema.agent_schema_composer import BuildMode
from langgraph.graph import END

# Create agents
planner = SimpleAgent(name="planner", engine=planner_engine)
executor = SimpleAgent(name="executor", engine=executor_engine)
replanner = SimpleAgent(name="replanner", engine=replanner_engine)

# Define routing functions
def route_after_execution(state) -> str:
    if hasattr(state, 'plan') and state.plan and state.plan.is_complete:
        return "replanner"
    elif hasattr(state, 'should_replan') and state.should_replan:
        return "replanner"
    else:
        return "executor"

def route_after_replan(state) -> str:
    if hasattr(state, 'final_answer') and state.final_answer:
        return END
    elif hasattr(state, 'plan') and state.plan:
        return "executor"
    return END

# Create the system
system = MultiAgentBase(
    agents=[planner, executor, replanner],
    branches=[
        (executor, route_after_execution, {
            "executor": executor,
            "replanner": replanner
        }),
        (replanner, route_after_replan, {
            "executor": executor,
            END: END
        })
    ],
    state_schema_override=PlanExecuteState,
    schema_build_mode=BuildMode.PARALLEL,
    name="Plan and Execute System"
)
```

### 2. Simple Sequential System

```python
# No branches = simple sequential flow
system = MultiAgentBase(
    agents=[agent1, agent2, agent3],
    schema_build_mode=BuildMode.SEQUENCE,
    name="Sequential System"
)
```

### 3. Custom Workflow with Tools

```python
# Add custom workflow nodes
def custom_processor(state):
    # Custom processing logic
    return {"processed": True}

system = MultiAgentBase(
    agents=[researcher, analyzer],
    workflow_nodes={"processor": custom_processor},
    branches=[
        (researcher, lambda s: "process", {"process": "processor"}),
        ("processor", lambda s: "analyze", {"analyze": analyzer})
    ],
    name="Research and Analysis System"
)
```

### 4. Convenience Functions

```python
from haive.agents.multi.enhanced_base import (
    create_plan_execute_multi_agent,
    create_sequential_multi_agent,
    create_branching_multi_agent
)

# Pre-configured Plan & Execute
pe_system = create_plan_execute_multi_agent(
    planner_agent=planner,
    executor_agent=executor,
    replanner_agent=replanner
)

# Simple sequential
seq_system = create_sequential_multi_agent(
    agents=[agent1, agent2, agent3]
)

# Custom branching
branch_system = create_branching_multi_agent(
    agents=[router, worker1, worker2],
    branches=[(router, condition, {"path1": worker1, "path2": worker2})]
)
```

## State Composition

The `AgentSchemaComposer` automatically creates state schemas from your agents:

### Automatic Composition

```python
# MultiAgentBase automatically composes state from agents
system = MultiAgentBase(agents=[agent1, agent2])
# Creates: MultiAgentBaseState with fields from both agents
```

### Manual Override

```python
# Use your own state schema
system = MultiAgentBase(
    agents=[agent1, agent2],
    state_schema_override=MyCustomState
)
```

### Shared Fields

Fields marked as shared are accessible to all agents:

```python
class MyState(StateSchema):
    __shared_fields__ = [
        "messages",
        "context",
        "results"
    ]
```

## Build Modes

### BuildMode.PARALLEL

- Agents conceptually execute in parallel
- Each agent gets separate namespace for non-shared fields
- Shared fields remain singular instances
- Best for: Independent agents with coordination points

```python
schema_build_mode=BuildMode.PARALLEL
```

### BuildMode.SEQUENCE

- Agents execute in sequence
- State flows from one agent to the next
- Fields are naturally shared in sequence
- Best for: Pipeline processing

```python
schema_build_mode=BuildMode.SEQUENCE
```

### BuildMode.HIERARCHICAL

- Parent-child agent relationships
- Supervisor patterns with delegation
- Hierarchical state management
- Best for: Supervisor-worker patterns

```python
schema_build_mode=BuildMode.HIERARCHICAL
```

## Best Practices

### 1. Naming Conventions

- Use descriptive agent names: `planner`, `executor`, `validator`
- Name systems clearly: `"Document Processing Pipeline"`
- Use consistent routing function names: `route_after_X`

### 2. State Management

- Always use `__shared_fields__` for coordinated data
- Keep agent-specific data separate when possible
- Use computed fields for derived state

### 3. Routing Functions

- Keep routing logic simple and testable
- Use clear return values: agent names or END
- Handle edge cases gracefully

### 4. Error Handling

- Validate state in routing functions
- Provide fallback routes for error conditions
- Log routing decisions for debugging

### 5. Testing

- Test routing logic independently
- Verify shared field behavior
- Mock agents for unit tests

## File Locations

### Core Implementation Files

- **MultiAgentBase**: [`packages/haive-agents/src/haive/agents/multi/enhanced_base.py`](../src/haive/agents/multi/enhanced_base.py)
- **AgentSchemaComposer**: [`packages/haive-core/src/haive/core/schema/agent_schema_composer.py`](../../haive-core/src/haive/core/schema/agent_schema_composer.py)
- **BaseGraph**: [`packages/haive-core/src/haive/core/graph/state_graph/base_graph2.py`](../../haive-core/src/haive/core/graph/state_graph/base_graph2.py)

### Example Files

- **Plan & Execute Example**: [`packages/haive-agents/examples/test_elegant_structure.py`](../examples/test_elegant_structure.py)
- **Working Test**: [`packages/haive-agents/examples/test_real_plan_execute_working.py`](../examples/test_real_plan_execute_working.py)
- **Comprehensive Tests**: [`packages/haive-agents/tests/test_planning/test_p_and_e_multi_agent.py`](../tests/test_planning/test_p_and_e_multi_agent.py)

### Related Components

- **Plan & Execute Engines**: [`packages/haive-agents/src/haive/agents/planning/p_and_e/engines.py`](../src/haive/agents/planning/p_and_e/engines.py)
- **Plan & Execute State**: [`packages/haive-agents/src/haive/agents/planning/p_and_e/state.py`](../src/haive/agents/planning/p_and_e/state.py)
- **Tools**: [`packages/haive-tools/src/haive/tools/tools/search_tools.py`](../../haive-tools/src/haive/tools/tools/search_tools.py)

## Quick Start Template

```python
#!/usr/bin/env python3
"""
Your Multi-Agent System Template
"""

import asyncio
from haive.agents.multi.enhanced_base import MultiAgentBase
from haive.agents.simple.agent import SimpleAgent
from haive.core.schema.agent_schema_composer import BuildMode
from langgraph.graph import END

async def main():
    # 1. Create your agents
    agent1 = SimpleAgent(name="agent1", engine=your_engine1)
    agent2 = SimpleAgent(name="agent2", engine=your_engine2)

    # 2. Define routing logic
    def route_between_agents(state) -> str:
        # Your routing logic here
        if some_condition(state):
            return "agent2"
        return END

    # 3. Create the system
    system = MultiAgentBase(
        agents=[agent1, agent2],
        branches=[
            (agent1, route_between_agents, {
                "agent2": agent2,
                END: END
            })
        ],
        schema_build_mode=BuildMode.PARALLEL,
        name="Your System"
    )

    # 4. Use it
    graph = system.build_graph()
    compiled = graph.compile()

    result = await compiled.ainvoke({
        "messages": [{"role": "user", "content": "Your input"}]
    })

    print(result)

if __name__ == "__main__":
    asyncio.run(main())
```

---

## 🚀 Ready to Build?

You now have everything you need to create sophisticated multi-agent systems with the elegant `MultiAgentBase` API. The combination of simple syntax and powerful functionality makes it easy to build complex agent orchestrations while maintaining clean, readable code.

For more examples and advanced patterns, check out the example files and tests linked above!
