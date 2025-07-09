# Haive Core: Agent Engine

## Overview

The Agent Engine provides the core architecture for all agent implementations in the Haive framework. It delivers consistent schema handling, execution flows, persistence management, and extensibility through patterns. The module implements protocol-based interfaces to ensure all agent implementations conform to consistent APIs.

## Key Features

- **Protocol-Based Architecture**: Consistent interfaces for all agent implementations
- **State Schema Management**: Fully dynamic and serializable state schemas
- **Persistence System**: Built-in state persistence and checkpointing
- **Configurable Execution**: Flexible execution flows with LangGraph integration
- **Streaming Support**: Real-time streaming of agent outputs
- **Graph Visualization**: Built-in tools for visualizing agent execution
- **Pattern System**: Reusable agent patterns for common implementations

## Installation

This module is part of the `haive-core` package. Install the full package with:

```bash
pip install haive-core
```

Or install via Poetry:

```bash
poetry add haive-core
```

## Quick Start

```python
from haive.core.engine.agent import Agent, AgentConfig
from haive.core.engine.aug_llm import AugLLMConfig

# Create a simple agent with default configuration
agent = Agent(
    name="my_agent",
    engine=AugLLMConfig(
        model="gpt-4"
    )
)

# Invoke the agent
result = agent.invoke("Hello, world!")
print(result)
```

## Components

### Agent Base Class

The core `Agent` class provides the foundational implementation with state management, execution flow, and interface methods.

```python
from haive.core.engine.agent import Agent

# Create a basic agent
agent = Agent(name="assistant")

# Invoke with text input
response = agent.invoke("What's the weather like today?")

# Invoke with structured input
response = agent.invoke({"query": "What's the weather like today?", "location": "New York"})

# Access agent state history
history = agent.state_history
```

### Agent Configuration

The `AgentConfig` class provides a comprehensive configuration system for agents with protocol validation.

```python
from haive.core.engine.agent import AgentConfig
from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.persistence.handlers import SqliteConfig

# Configure an agent with advanced options
config = AgentConfig(
    name="assistant",
    engine=AugLLMConfig(model="gpt-4"),
    persistence=SqliteConfig(db_path="agents.db"),
    streaming=True,
    verbose=True
)

# Create agent from config
agent = Agent(config=config)
```

### Agent Protocols

The agent system uses protocols to ensure consistent interfaces across implementations:

- `AgentProtocol`: Base protocol for all agents
- `StreamingAgentProtocol`: Protocol for agents with streaming capabilities
- `PersistentAgentProtocol`: Protocol for agents with persistence
- `VisualizationAgentProtocol`: Protocol for agents with visualization features
- `ExtensibilityAgentProtocol`: Protocol for agent extensibility

## Usage Patterns

### Basic Invocation

```python
# Create an agent
agent = Agent(
    name="assistant",
    engine=AugLLMConfig(model="gpt-4")
)

# Simple invocation
response = agent.invoke("Tell me about artificial intelligence")

# Structured invocation
response = agent.invoke({
    "query": "Tell me about artificial intelligence",
    "max_tokens": 100
})
```

### Streaming

```python
# Configure a streaming agent
agent = Agent(
    name="assistant",
    engine=AugLLMConfig(model="gpt-4"),
    streaming=True
)

# Stream responses
for chunk in agent.stream("Tell me a story about a robot"):
    print(chunk, end="", flush=True)
```

### Async Invocation

```python
import asyncio

# Create an agent
agent = Agent(
    name="assistant",
    engine=AugLLMConfig(model="gpt-4")
)

# Async invocation
async def run_agent():
    response = await agent.ainvoke("What is the meaning of life?")
    print(response)

asyncio.run(run_agent())
```

### Persistence

```python
from haive.core.persistence.handlers import SqliteConfig

# Create a persistent agent
agent = Agent(
    name="assistant",
    engine=AugLLMConfig(model="gpt-4"),
    persistence=SqliteConfig(
        db_path="agents.db",
        table_name="agent_states",
        auto_save=True
    )
)

# Invoke the agent - state is automatically saved
response = agent.invoke("Hello, I'm a user")

# Load a previous conversation
agent.load_state("conversation_id_123")
```

## Configuration

### Engine Configuration

```python
from haive.core.engine.aug_llm import AugLLMConfig

# Configure the underlying LLM engine
engine_config = AugLLMConfig(
    model="gpt-4",
    temperature=0.7,
    max_tokens=500,
    context_window=8000
)

# Create agent with engine config
agent = Agent(
    name="assistant",
    engine=engine_config
)
```

### Persistence Configuration

```python
from haive.core.persistence.handlers import (
    MemoryConfig,
    SqliteConfig,
    PostgresConfig
)

# In-memory persistence (default)
memory_config = MemoryConfig()

# SQLite persistence
sqlite_config = SqliteConfig(
    db_path="agents.db",
    table_name="agent_states",
    auto_save=True
)

# PostgreSQL persistence
postgres_config = PostgresConfig(
    connection_string="postgresql://user:password@localhost:5432/mydb",
    table_name="agent_states",
    auto_save=True
)

# Create agent with persistence
agent = Agent(
    name="assistant",
    engine=AugLLMConfig(model="gpt-4"),
    persistence=sqlite_config
)
```

## Integration with Other Modules

### Integration with Graph System

```python
from haive.core.graph.dynamic_graph_builder import DynamicGraphBuilder
from haive.core.engine.agent import Agent

# Create an agent
agent = Agent(name="assistant", engine=AugLLMConfig(model="gpt-4"))

# Access the agent's graph
graph = agent.graph

# Modify the graph
builder = DynamicGraphBuilder(graph)
builder.add_node("memory_node", memory_function)
builder.add_edge("agent_node", "memory_node")

# Update the agent with the modified graph
agent.graph = builder.build()
```

### Integration with Schema System

```python
from haive.core.schema.schema_composer import SchemaComposer
from haive.core.engine.agent import Agent

# Create a custom state schema
composer = SchemaComposer(name="CustomAgentState")
composer.add_field("messages", List[BaseMessage], default_factory=list)
composer.add_field("context", List[str], default_factory=list)
composer.add_field("query", str, default="")
composer.add_field("response", str, default="")
CustomAgentState = composer.build()

# Create agent with custom schema
agent = Agent(
    name="assistant",
    engine=AugLLMConfig(model="gpt-4"),
    state_type=CustomAgentState
)
```

## Best Practices

- **Use Protocol Validation**: Always validate agent implementations against protocols to ensure consistent behavior
- **Implement State Persistence**: Enable state persistence for production agents to maintain conversation history
- **Configure Proper Engine**: Choose the appropriate engine configuration for your use case (e.g., AugLLM for general purpose, RAG for knowledge-based)
- **Enable Streaming**: For interactive applications, enable streaming to provide real-time responses
- **Visualize Agent Graphs**: Use the built-in visualization tools to understand agent execution flows
- **Leverage Patterns**: Use pre-built agent patterns for common use cases instead of building from scratch

## Advanced Usage

### Custom Agent Implementation

```python
from haive.core.engine.agent import Agent, AgentConfig
from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.schema.schema_composer import SchemaComposer
from typing import Dict, Any, List

# Create custom state schema
composer = SchemaComposer(name="CustomAgentState")
composer.add_field("messages", List[BaseMessage], default_factory=list)
composer.add_field("query", str, default="")
composer.add_field("context", List[str], default_factory=list)
composer.add_field("response", str, default="")
CustomAgentState = composer.build()

# Create custom agent class
class CustomAgent(Agent):
    def __init__(self, name: str, **kwargs):
        # Configure custom graph
        super().__init__(
            name=name,
            engine=AugLLMConfig(model="gpt-4"),
            state_type=CustomAgentState,
            **kwargs
        )

        # Customize the graph
        builder = DynamicGraphBuilder(self.graph)
        builder.add_node("retrieval_node", self._retrieve_context)
        builder.add_edge("agent_node", "retrieval_node")
        builder.add_edge("retrieval_node", "agent_node")
        self.graph = builder.build()

    def _retrieve_context(self, state: CustomAgentState) -> CustomAgentState:
        """Custom retrieval function to get context for the query."""
        # Implement context retrieval logic
        state.context = ["Context item 1", "Context item 2"]
        return state

# Use the custom agent
agent = CustomAgent(name="retrieval_agent")
result = agent.invoke("Tell me about quantum physics")
```

### Pattern-Based Agent

```python
from haive.core.engine.agent import Agent
from haive.core.engine.agent.pattern import ReActPattern
from haive.core.engine.aug_llm import AugLLMConfig

# Create a ReAct pattern agent
agent = Agent(
    name="react_agent",
    engine=AugLLMConfig(model="gpt-4"),
    pattern=ReActPattern()
)

# Invoke the agent
result = agent.invoke("Search for information about climate change")
```

### Visualization

```python
from haive.core.engine.agent import Agent
from haive.core.engine.aug_llm import AugLLMConfig

# Create an agent
agent = Agent(
    name="assistant",
    engine=AugLLMConfig(model="gpt-4")
)

# Run the agent
result = agent.invoke("Tell me about neural networks")

# Visualize the agent's execution graph
agent.visualize_graph()

# Save the visualization
agent.save_graph("agent_graph.png")
```

## API Reference

For full API details, see the [documentation](https://docs.haive.ai/core/engine/agent).

## Related Modules

- **Engine System**: Provides the underlying execution engines for agents
- **Graph System**: Manages the execution flow and state transitions
- **Schema System**: Handles state schema definition and validation
- **Persistence System**: Enables state persistence and checkpointing
