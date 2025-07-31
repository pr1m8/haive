# Haive Multi-Agent System

A comprehensive framework for building and orchestrating multi-agent systems with intelligent state management, message preservation, and flexible execution patterns.

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Core Components](#core-components)
- [Execution Modes](#execution-modes)
- [State Management](#state-management)
- [Message Preservation](#message-preservation)
- [API Reference](#api-reference)
- [Examples](#examples)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)

## Overview

The Haive Multi-Agent System provides a powerful framework for coordinating multiple AI agents to solve complex tasks. Built on top of LangGraph and the Haive Schema System, it offers:

- **Flexible Execution Patterns**: Sequential, parallel, conditional, and hierarchical modes
- **Intelligent State Management**: Automatic schema composition with field sharing
- **Message Preservation**: Maintains tool_call_id and other critical fields across agents
- **Engine Isolation**: Each agent maintains its own tools and engines
- **Branching Support**: Conditional routing and decision-based agent selection

## Architecture

### System Overview

```
┌─────────────────────────────────────────────────────┐
│                  MultiAgent System                   │
├─────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐ │
│  │   Agent 1   │  │   Agent 2   │  │   Agent N   │ │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘ │
│         │                 │                 │        │
│  ┌──────┴─────────────────┴─────────────────┴──────┐│
│  │           AgentSchemaComposer                    ││
│  │  - Smart field separation                        ││
│  │  - Message preservation                          ││
│  │  - Engine I/O mapping                            ││
│  └──────────────────────┬───────────────────────────┘│
│                         │                            │
│  ┌──────────────────────┴───────────────────────────┐│
│  │              StateSchema                          ││
│  │  - Shared fields with reducers                   ││
│  │  - Private agent states                          ││
│  │  - Serialized engines                            ││
│  └──────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────┘
```

### Key Design Principles

1. **Agent Isolation**: Each agent maintains its own tools and state
2. **Message Preservation**: BaseMessage objects flow intact between agents
3. **Smart Composition**: Intelligent field sharing based on usage patterns
4. **Flexible Routing**: Support for complex execution patterns

## Installation

```bash
pip install haive-agents
```

## Quick Start

### Basic Sequential Multi-Agent

```python
from haive.agents.multi.base import SequentialAgent
from haive.agents.react.agent import ReactAgent
from haive.agents.simple.agent import SimpleAgent
from haive.core.engine.aug_llm import AugLLMConfig
from langchain_core.tools import tool

# Define tools
@tool
def search(query: str) -> str:
    """Search for information."""
    return f"Results for: {query}"

@tool
def calculate(expression: str) -> float:
    """Calculate mathematical expressions."""
    return eval(expression)

# Create engines
search_engine = AugLLMConfig(tools=[search])
calc_engine = AugLLMConfig(tools=[calculate])

# Create agents
researcher = SimpleAgent(name="Researcher", engine=search_engine)
calculator = ReactAgent(name="Calculator", engine=calc_engine)

# Create multi-agent system
system = SequentialAgent(
    name="Research and Calculate",
    agents=[researcher, calculator]
)

# Run the system
result = system.run({
    "messages": [HumanMessage(content="Find the GDP of France and calculate 10% of it")]
})
```

### Conditional Multi-Agent

```python
from haive.agents.multi.base import ConditionalAgent

# Create conditional system with branching
system = ConditionalAgent(
    name="Conditional System",
    agents=[classifier, processor_a, processor_b],
    branches={
        "classifier": {
            "condition": lambda state: "type_a" if "urgent" in str(state.messages[-1]) else "type_b",
            "mapping": {
                "type_a": "processor_a",
                "type_b": "processor_b"
            }
        }
    }
)
```

## Core Components

### MultiAgent Base Class

The abstract base class for all multi-agent systems:

```python
class MultiAgent(Agent):
    """Abstract base class for multi-agent systems.

    Provides:
    - Automatic schema composition from child agents
    - Support for various execution modes
    - Private agent state management
    - Complex routing patterns
    """

    agents: Sequence[Agent]  # Child agents
    execution_mode: ExecutionMode  # How to execute agents
    include_meta: bool  # Include coordination metadata
    schema_separation: Literal["smart", "shared", "namespaced"]
```

### Execution Mode Implementations

#### SequentialAgent

Executes agents one after another with state flowing between them:

```python
system = SequentialAgent(
    name="Step by Step",
    agents=[planner, executor, reviewer]
)
```

#### ParallelAgent

Executes all agents independently (future implementation):

```python
system = ParallelAgent(
    name="Parallel Processing",
    agents=[analyzer1, analyzer2, analyzer3]
)
```

#### ConditionalAgent

Routes execution based on conditions:

```python
system = ConditionalAgent(
    name="Smart Router",
    agents=[classifier, handler_a, handler_b],
    branches={...}  # Routing configuration
)
```

## Execution Modes

### Sequential Mode

Agents execute in order with state flowing from one to the next:

```
Agent1 → Agent2 → Agent3 → Result
```

**Use Cases:**

- Step-by-step workflows
- Pipeline processing
- Tasks with dependencies

### Parallel Mode

All agents execute independently with separate state spaces:

```
       ┌→ Agent1 →┐
Input →├→ Agent2 →├→ Merge → Result
       └→ Agent3 →┘
```

**Use Cases:**

- Independent analysis tasks
- Parallel data processing
- Consensus building

### Conditional Mode

Dynamic routing based on state or agent decisions:

```
         ┌→ Agent2 → Agent4 →┐
Input → Agent1                → Result
         └→ Agent3 → Agent5 →┘
```

**Use Cases:**

- Classification and routing
- Adaptive workflows
- Error handling paths

### Hierarchical Mode

Supervisor-worker patterns with parent-child relationships:

```
           Supervisor
          ╱    │    ╲
    Worker1  Worker2  Worker3
```

**Use Cases:**

- Task delegation
- Hierarchical planning
- Complex coordination

## State Management

### Schema Composition

The system automatically composes schemas from agents:

```python
# Automatic field detection and separation
schema = AgentSchemaComposer.from_agents(
    agents=[agent1, agent2],
    separation="smart"  # Intelligent field sharing
)
```

### Field Separation Strategies

#### Smart Separation (Default)

- Shared fields: Used by multiple agents
- Namespaced fields: Single-agent fields get prefixes
- Automatic detection of common fields

#### Shared Separation

- All fields are shared
- No namespacing
- Best for tightly coupled agents

#### Namespaced Separation

- Every field gets agent prefix
- Complete isolation
- Best for independent agents

### Private Agent States

Each agent can maintain private state:

```python
# Agent-specific state preserved
agent._private_state = {
    "context": "...",
    "history": [...]
}
```

## Message Preservation

### The Problem

LangGraph's default `add_messages` reducer converts BaseMessage objects to dicts, losing fields like `tool_call_id`:

```python
# Default behavior (problematic)
ToolMessage(tool_call_id="123") → dict → ToolMessage()  # tool_call_id lost!
```

### The Solution

Custom `preserve_messages_reducer` maintains BaseMessage objects:

```python
# Our solution
ToolMessage(tool_call_id="123") → ToolMessage(tool_call_id="123")  # Preserved!
```

This is automatically applied to all message fields in multi-agent systems.

## API Reference

### MultiAgent Class

```python
class MultiAgent(Agent):
    """Abstract base class for multi-agent systems.

    Args:
        name: System name
        agents: List of child agents
        execution_mode: How to execute agents
        include_meta: Include coordination metadata
        schema_separation: Field separation strategy
        branches: Conditional routing configuration
    """

    def add_agent(self, agent: Agent) -> None:
        """Add an agent to the system."""

    def remove_agent(self, agent_id: str) -> None:
        """Remove an agent by ID."""

    def get_agent_by_name(self, name: str) -> Optional[Agent]:
        """Get agent by name or ID."""

    @abstractmethod
    def build_custom_graph(self, graph: BaseGraph) -> BaseGraph:
        """Build custom execution graph (for CUSTOM mode)."""
```

### SequentialAgent

```python
class SequentialAgent(MultiAgent):
    """Execute agents in sequence.

    Example:
        >>> system = SequentialAgent(
        ...     agents=[researcher, writer, editor]
        ... )
        >>> result = system.run({"messages": [...]})
    """
```

### ConditionalAgent

```python
class ConditionalAgent(MultiAgent):
    """Route execution based on conditions.

    Example:
        >>> system = ConditionalAgent(
        ...     agents=[router, handler_a, handler_b],
        ...     branches={
        ...         "router": {
        ...             "condition": route_function,
        ...             "mapping": {"a": "handler_a", "b": "handler_b"}
        ...         }
        ...     }
        ... )
    """
```

## Examples

### Research and Analysis System

```python
# Create a system that researches a topic and analyzes findings
research_system = SequentialAgent(
    name="Research System",
    agents=[
        SimpleAgent(name="Query Expander", engine=expand_engine),
        ReactAgent(name="Researcher", engine=search_engine),
        SimpleAgent(name="Analyzer", engine=analysis_engine),
        SimpleAgent(name="Report Writer", engine=writing_engine)
    ]
)

result = research_system.run({
    "messages": [HumanMessage(content="Research climate change impacts")]
})
```

### Customer Support Router

```python
# Route customer queries to appropriate handlers
support_system = ConditionalAgent(
    name="Support Router",
    agents=[
        SimpleAgent(name="Classifier", engine=classify_engine),
        ReactAgent(name="Technical Support", engine=tech_engine),
        SimpleAgent(name="Billing Support", engine=billing_engine),
        SimpleAgent(name="General Support", engine=general_engine)
    ],
    branches={
        "Classifier": {
            "condition": classify_query,
            "mapping": {
                "technical": "Technical Support",
                "billing": "Billing Support",
                "general": "General Support"
            }
        }
    }
)
```

### Parallel Analysis System

```python
# Analyze data from multiple perspectives simultaneously
analysis_system = ParallelAgent(
    name="Multi-Perspective Analysis",
    agents=[
        SimpleAgent(name="Statistical Analyzer", engine=stats_engine),
        SimpleAgent(name="Trend Analyzer", engine=trend_engine),
        SimpleAgent(name="Anomaly Detector", engine=anomaly_engine)
    ]
)
```

## Best Practices

### 1. Agent Design

- **Single Responsibility**: Each agent should have a clear, focused purpose
- **Tool Isolation**: Don't share tools between agents directly
- **State Design**: Consider what state needs to be shared vs. private

### 2. Schema Management

- **Use Smart Separation**: Default option that handles most cases well
- **Explicit Sharing**: Use `shared_` prefix for clarity
- **Avoid Conflicts**: Check field names across agents

### 3. Message Handling

- **Preserve Messages**: Always use the enhanced schema composer
- **Tool Results**: Ensure tool_call_id preservation for proper routing
- **Message Types**: Use appropriate message types (Human, AI, Tool)

### 4. Error Handling

- **Graceful Degradation**: Design systems to handle agent failures
- **Conditional Paths**: Use branching for error recovery
- **Logging**: Enable debug logging for troubleshooting

### 5. Performance

- **Minimize State**: Only share necessary fields
- **Efficient Routing**: Use direct paths when possible
- **Batch Operations**: Group related agents together

## Troubleshooting

### Common Issues

#### 1. Missing tool_call_id Error

**Symptom:**

```
KeyError: 'tool_call_id'
```

**Solution:**
Ensure you're using the latest version with preserve_messages_reducer.

#### 2. Field Conflicts

**Symptom:**

```
ValueError: Field 'context' defined differently in multiple agents
```

**Solution:**
Use namespaced separation or rename conflicting fields.

#### 3. Serialization Errors

**Symptom:**

```
TypeError: Type is not msgpack serializable: ModelMetaclass
```

**Solution:**
Engines are automatically serialized. Don't store raw objects in state.

### Debug Tips

1. **Enable Detailed Logging:**

```python
import logging
logging.getLogger("haive.agents.multi").setLevel(logging.DEBUG)
logging.getLogger("haive.core.schema").setLevel(logging.DEBUG)
```

2. **Inspect State Schema:**

```python
print(system.state_schema.model_fields)
print(system.state_schema.__shared_fields__)
```

3. **Track Message Flow:**

```python
for i, msg in enumerate(state.messages):
    print(f"Message {i}: {type(msg).__name__}")
    if hasattr(msg, 'tool_call_id'):
        print(f"  tool_call_id: {msg.tool_call_id}")
```

## Contributing

We welcome contributions! Areas of interest:

1. **New Execution Modes**: Implement custom patterns
2. **Enhanced Routing**: More sophisticated conditional logic
3. **Performance Optimizations**: Parallel execution improvements
4. **Documentation**: Examples and tutorials

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

This project is licensed under the MIT License - see [LICENSE](LICENSE) for details.

## Acknowledgments

Built on top of:

- [LangGraph](https://github.com/langchain-ai/langgraph) for graph execution
- [LangChain](https://github.com/langchain-ai/langchain) for LLM integration
- [Pydantic](https://pydantic-docs.helpmanual.io/) for data validation
