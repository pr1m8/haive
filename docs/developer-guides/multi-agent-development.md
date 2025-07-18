# Multi-Agent Development Guide

_Comprehensive guide for building and orchestrating multi-agent systems with the Haive framework_

## Table of Contents

1. [Overview](#overview)
2. [Core Concepts](#core-concepts)
3. [Architecture](#architecture)
4. [Creating Multi-Agent Systems](#creating-multi-agent-systems)
5. [Execution Modes](#execution-modes)
6. [State Management](#state-management)
7. [Message Preservation](#message-preservation)
8. [Conditional Routing](#conditional-routing)
9. [Best Practices](#best-practices)
10. [Examples](#examples)
11. [Troubleshooting](#troubleshooting)

## Overview

Multi-agent systems in Haive allow you to orchestrate multiple specialized agents working together to solve complex tasks. Each agent focuses on a specific aspect of the problem, and the multi-agent system coordinates their execution with intelligent state management and message preservation.

### Key Features

- **Flexible Execution Patterns**: Sequential, parallel, conditional, and hierarchical modes
- **Intelligent State Management**: Automatic schema composition with field sharing
- **Message Preservation**: Maintains tool_call_id and other critical fields across agents
- **Engine Isolation**: Each agent maintains its own tools and engines
- **Conditional Routing**: Dynamic agent selection based on state content
- **Type Safety**: Proper validation and type checking throughout the system

## Core Concepts

### 1. MultiAgent Base Class

The `MultiAgent` class is the foundation for all multi-agent workflows:

```python
from haive.agents.multi.base import MultiAgent, ExecutionMode
from haive.agents.simple import SimpleAgent

class CustomMultiAgent(MultiAgent):
    def __init__(self, agents: List[Agent], execution_mode: ExecutionMode = "sequential"):
        super().__init__(
            agents=agents,
            execution_mode=execution_mode,
            name="custom_multi_agent"
        )
```

### 2. Agent Orchestration

Agents are orchestrated through a graph-based execution model:

```python
# Sequential execution
multi_agent = MultiAgent(
    agents=[planner_agent, executor_agent, reviewer_agent],
    execution_mode="sequential"
)

# Parallel execution
multi_agent = MultiAgent(
    agents=[research_agent, analysis_agent],
    execution_mode="parallel"
)

# Conditional execution
multi_agent = MultiAgent(
    agents=[fast_agent, thorough_agent],
    execution_mode="conditional",
    router_function=intent_router
)
```

## Architecture

### Component Hierarchy

```
MultiAgent
├── State Management (MetaAgentState)
├── Agent Coordination (ExecutionMixin)
├── Message Preservation (MessageHandler)
└── Graph Construction (BaseGraph)
```

### State Flow

1. **Input Validation**: Incoming state is validated against composed schema
2. **Agent Execution**: Agents execute according to execution mode
3. **State Merging**: Individual agent states are merged intelligently
4. **Message Preservation**: Critical message fields are maintained
5. **Output Generation**: Final state is returned to caller

## Creating Multi-Agent Systems

### Basic Multi-Agent

```python
from haive.agents.multi import MultiAgent
from haive.agents.simple import SimpleAgent
from haive.core.engine.aug_llm import AugLLMConfig

# Create individual agents
planner = SimpleAgent(
    engine=AugLLMConfig(
        name="planner",
        system_prompt="You are a planning specialist."
    ),
    name="planner"
)

executor = SimpleAgent(
    engine=AugLLMConfig(
        name="executor",
        system_prompt="You execute plans step by step."
    ),
    name="executor"
)

# Create multi-agent system
workflow = MultiAgent(
    agents=[planner, executor],
    execution_mode="sequential",
    name="planning_workflow"
)
```

### Advanced Multi-Agent with Validation

```python
from pydantic import BaseModel, Field, field_validator

class WorkflowConfig(BaseModel):
    """Configuration for multi-agent workflow."""
    agents: List[str] = Field(min_length=2)
    execution_mode: str = Field(default="sequential")
    enable_routing: bool = Field(default=False)

    # Computed fields
    agent_count: int = 0
    has_routing: bool = False

    @field_validator('execution_mode')
    @classmethod
    def validate_mode(cls, v):
        valid_modes = ["sequential", "parallel", "conditional"]
        if v not in valid_modes:
            raise ValueError(f"Mode must be one of {valid_modes}")
        return v

    def model_post_init(self, __context):
        """Post-init validation and setup."""
        self.agent_count = len(self.agents)
        self.has_routing = self.enable_routing and self.execution_mode == "conditional"

        if len(set(self.agents)) != len(self.agents):
            raise ValueError("Agent names must be unique")
```

## Execution Modes

### Sequential Mode

Agents execute one after another, with each agent receiving the output of the previous agent:

```python
multi_agent = MultiAgent(
    agents=[agent1, agent2, agent3],
    execution_mode="sequential"
)

# Execution flow: agent1 → agent2 → agent3
```

### Parallel Mode

Agents execute simultaneously with the same input:

```python
multi_agent = MultiAgent(
    agents=[research_agent, analysis_agent],
    execution_mode="parallel"
)

# Both agents process the same input concurrently
```

### Conditional Mode

Agents are selected dynamically based on routing logic:

```python
def intent_router(state):
    """Route based on query intent."""
    query = state.get("query", "").lower()
    if "urgent" in query:
        return "fast_agent"
    elif "detailed" in query:
        return "thorough_agent"
    return "default_agent"

multi_agent = MultiAgent(
    agents=[fast_agent, thorough_agent, default_agent],
    execution_mode="conditional",
    router_function=intent_router
)
```

## State Management

### Automatic Schema Composition

Multi-agent systems automatically compose schemas from individual agents:

```python
# Agent 1 has: MessagesState + CustomField1
# Agent 2 has: MessagesState + CustomField2
# Result: MessagesState + CustomField1 + CustomField2
```

### Field Sharing Rules

1. **Common fields** (like `messages`) are shared between agents
2. **Unique fields** are preserved from each agent
3. **Conflicting fields** trigger validation errors
4. **Reducer fields** (like `messages`) are merged automatically

### Meta State Management

Track agent execution and coordination:

```python
class MetaAgentState(StateSchema):
    current_agent: str = ""
    execution_history: List[str] = Field(default_factory=list)
    agent_states: Dict[str, Any] = Field(default_factory=dict)

    def track_agent_execution(self, agent_name: str, state: Dict):
        """Track individual agent execution."""
        self.current_agent = agent_name
        self.execution_history.append(agent_name)
        self.agent_states[agent_name] = state
```

## Message Preservation

### Critical Field Preservation

The system preserves important message fields across agent boundaries:

```python
class MessagePreserver:
    """Preserves critical message fields across agents."""

    PRESERVED_FIELDS = [
        'tool_call_id',
        'message_id',
        'thread_id',
        'additional_kwargs'
    ]

    def preserve_message_context(self, messages: List[Message]) -> List[Message]:
        """Ensure critical fields are maintained."""
        # Implementation preserves field integrity
```

### Tool Call Continuity

Tool calls and responses are properly linked across agents:

```python
# Agent 1 makes a tool call
tool_call = ToolCall(id="call_123", function="search", args={"query": "..."})

# Agent 2 receives the tool call context
# The tool_call_id is preserved for proper linking
```

## Conditional Routing

### Dynamic Agent Selection

Route to different agents based on state content:

```python
class ConditionalRouter:
    """Routes requests to appropriate agents."""

    def __init__(self):
        self.routes = {}
        self.conditions = {}

    def add_route(self, name: str, condition, destinations: Dict[str, str]):
        """Add conditional route."""
        self.routes[name] = destinations
        self.conditions[name] = condition

    def route(self, from_node: str, state: Dict) -> str:
        """Execute routing logic."""
        if from_node not in self.conditions:
            return "default"

        condition = self.conditions[from_node]
        result = condition(state)

        return self.routes[from_node].get(result, "default")

# Usage
router = ConditionalRouter()
router.add_route(
    "intent_router",
    lambda state: "urgent" if "urgent" in state.get("query", "") else "normal",
    {"urgent": "fast_agent", "normal": "thorough_agent"}
)
```

## Best Practices

### 1. Agent Design

- **Single Responsibility**: Each agent should have a clear, focused purpose
- **Stateless Design**: Agents should be stateless and rely on state parameter
- **Consistent Interfaces**: Use consistent input/output schemas across agents

### 2. State Management

- **Minimal State**: Keep state as minimal as possible
- **Clear Ownership**: Define which agent owns which state fields
- **Validation**: Always validate state transitions between agents

### 3. Error Handling

```python
class RobustMultiAgent(MultiAgent):
    def handle_agent_error(self, agent_name: str, error: Exception, state: Dict):
        """Handle individual agent errors gracefully."""
        # Log error
        logger.error(f"Agent {agent_name} failed: {error}")

        # Add error to state
        if "errors" not in state:
            state["errors"] = []
        state["errors"].append({
            "agent": agent_name,
            "error": str(error),
            "timestamp": datetime.now()
        })

        # Continue with next agent or fallback
        return self.get_fallback_agent(agent_name)
```

## Examples

### Example 1: RAG Multi-Agent Pipeline

```python
from haive.agents.rag import SimpleRAGAgent
from haive.agents.simple import SimpleAgent

# Create specialized agents
query_refiner = SimpleAgent(
    engine=AugLLMConfig(system_prompt="Refine queries for better search results"),
    name="query_refiner"
)

retriever = SimpleRAGAgent(
    vector_store=vector_store,
    name="retriever"
)

answer_generator = SimpleAgent(
    engine=AugLLMConfig(system_prompt="Generate comprehensive answers"),
    name="answer_generator"
)

# Create pipeline
rag_pipeline = MultiAgent(
    agents=[query_refiner, retriever, answer_generator],
    execution_mode="sequential",
    name="rag_pipeline"
)

# Execute
result = rag_pipeline.invoke({"query": "What is machine learning?"})
```

### Example 2: Conditional Research Pipeline

```python
def research_router(state):
    """Route based on research complexity."""
    complexity = analyze_query_complexity(state.get("query", ""))

    if complexity == "simple":
        return "quick_search"
    elif complexity == "complex":
        return "deep_research"
    else:
        return "standard_research"

research_system = MultiAgent(
    agents=[quick_agent, standard_agent, deep_agent],
    execution_mode="conditional",
    router_function=research_router,
    name="adaptive_research"
)
```

## Troubleshooting

### Common Issues

1. **Schema Conflicts**
   - **Problem**: Agents have incompatible schemas
   - **Solution**: Use explicit schema composition or field mapping

2. **State Loss**
   - **Problem**: Agent state is not preserved between executions
   - **Solution**: Ensure proper state sharing configuration

3. **Message Corruption**
   - **Problem**: Tool calls lose their IDs between agents
   - **Solution**: Enable message preservation in multi-agent configuration

### Debugging Tips

1. **Enable Logging**

   ```python
   import logging
   logging.getLogger("haive.agents.multi").setLevel(logging.DEBUG)
   ```

2. **State Inspection**

   ```python
   # Add state inspection between agents
   multi_agent.add_debug_callback(lambda state: print(f"State: {state}"))
   ```

3. **Agent Isolation Testing**
   ```python
   # Test each agent individually first
   for agent in multi_agent.agents:
       result = agent.invoke(test_state)
       print(f"{agent.name}: {result}")
   ```

## Related Documentation

- [System Architecture](../architecture/system-comprehensive-analysis.md)
- [Agent Patterns Guide](../guides/building_agents.rst)
- [State Management Guide](../guides/state_management.rst)
- [Testing Guide](../guides/documentation/documentation_process.rst)

---

_This guide consolidates information from multiple multi-agent documentation sources and provides comprehensive coverage of multi-agent development in the Haive framework._
