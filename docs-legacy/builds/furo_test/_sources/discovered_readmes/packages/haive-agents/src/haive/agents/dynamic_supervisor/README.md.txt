# Dynamic Supervisor Agent

The Dynamic Supervisor Agent is a powerful multi-agent orchestration system that extends ReactAgent to provide runtime agent management capabilities. It can dynamically add, remove, activate, and coordinate specialized agents based on task requirements.

## Overview

The Dynamic Supervisor uses a tool-based approach where handoff tools execute agents directly within the ReAct loop. This provides flexible, runtime agent coordination without requiring pre-compiled graph structures.

## Key Features

- **Dynamic Agent Management**: Add/remove agents at runtime
- **Tool-Based Execution**: Agents execute directly through tools
- **ReAct Loop Integration**: Inherits reasoning and acting capabilities
- **State Management**: Maintains agent registry and execution state
- **Capability-Based Routing**: Route tasks based on agent capabilities

## Quick Start

### Basic Usage

```python
from haive.agents.dynamic_supervisor import create_dynamic_supervisor
from haive.agents.simple import SimpleAgent
from haive.core.engine.aug_llm import AugLLMConfig

# Create specialized agents
math_agent = SimpleAgent(
    name="math_agent",
    engine=AugLLMConfig(tools=[calculator_tool])
)

# Create supervisor
supervisor = create_dynamic_supervisor(
    name="task_router",
    model="gpt-4"
)

# Add agents to supervisor
state = supervisor.create_initial_state()
state.add_agent("math_agent", math_agent, "Mathematics expert")

# Run task
result = await supervisor.arun("Calculate 15 * 23", state=state)
```

### Advanced Usage

```python
from haive.agents.dynamic_supervisor import DynamicSupervisorAgent
from haive.core.engine.aug_llm import AugLLMConfig

# Create custom supervisor
supervisor = DynamicSupervisorAgent(
    name="advanced_supervisor",
    engine=AugLLMConfig(
        model="gpt-4",
        temperature=0.0,
        system_message="You are an intelligent task coordinator"
    ),
    enable_agent_builder=True,
    auto_sync_tools=True
)

# Add default agents that are always available
supervisor.add_default_agent("general", general_agent, "General assistant")

# Create state and add task-specific agents
state = supervisor.create_initial_state()
state.add_agent("specialist", specialist_agent, "Domain specialist")

# Run complex task
result = await supervisor.arun(
    "Analyze this data and provide insights",
    state=state
)
```

## Architecture

### Core Components

1. **DynamicSupervisorAgent**: Main supervisor class extending ReactAgent
2. **SupervisorStateWithTools**: State management with dynamic tool generation
3. **AgentInfo**: Metadata container for agent information
4. **Tool Creation**: Utilities for generating handoff tools

### Execution Flow

1. **Task Analysis**: Supervisor analyzes incoming task
2. **Agent Selection**: Chooses appropriate agent based on capabilities
3. **Tool Execution**: Handoff tool executes selected agent
4. **Result Integration**: Supervisor processes and returns results
5. **State Update**: Updates registry and execution history

### Tool-Based Agent Execution

```python
# Handoff tools are created dynamically
@tool
def handoff_to_math_agent(task: str) -> str:
    """Transfer task to math agent for calculation."""
    result = await math_agent.arun(task)
    return f"Math agent result: {result}"
```

## State Management

### SupervisorStateWithTools

The state class provides:

- **Agent Registry**: Dynamic agent storage and retrieval
- **Tool Generation**: Automatic creation of handoff tools
- **Execution History**: Track of agent interactions
- **Metadata**: Agent capabilities and descriptions

```python
# State operations
state = SupervisorStateWithTools()
state.add_agent("name", agent, "description")
state.remove_agent("name")
state.activate_agent("name")
state.deactivate_agent("name")
```

## Configuration Options

### DynamicSupervisorAgent Parameters

- `enable_agent_builder`: Enable dynamic agent creation capabilities
- `auto_sync_tools`: Automatically sync tools when state changes
- `state_schema_override`: Custom state schema (default: SupervisorStateWithTools)

### Factory Function Options

```python
supervisor = create_dynamic_supervisor(
    name="supervisor",
    model="gpt-4",
    temperature=0.0,
    force_tool_use=True,
    enable_agent_builder=False
)
```

## Examples

### Basic Task Routing

```python
import asyncio
from haive.agents.dynamic_supervisor import create_dynamic_supervisor

async def main():
    supervisor = create_dynamic_supervisor(name="router")
    state = supervisor.create_initial_state()

    # Add agents
    state.add_agent("math", math_agent, "Mathematics expert")
    state.add_agent("search", search_agent, "Web search specialist")

    # Route tasks
    math_result = await supervisor.arun("What is 15 * 23?", state=state)
    search_result = await supervisor.arun("Find information about AI", state=state)

asyncio.run(main())
```

### Dynamic Agent Activation

```python
# Start with minimal agents
state = supervisor.create_initial_state()
state.add_agent("general", general_agent, "General assistant")

# Add specialized agents as needed
if task_requires_math:
    state.add_agent("math", math_agent, "Mathematics expert")

if task_requires_search:
    state.add_agent("search", search_agent, "Web search specialist")
```

### Agent Capabilities

```python
# Register agents with capabilities
state.add_agent("math", math_agent, "Mathematics expert",
               capabilities=["calculation", "algebra", "statistics"])
state.add_agent("search", search_agent, "Web search specialist",
               capabilities=["web_search", "fact_checking", "research"])

# Query by capability
math_agents = state.get_agents_by_capability("calculation")
```

## Testing

```bash
# Run all dynamic supervisor tests
poetry run pytest tests/test_dynamic_supervisor/ -v

# Run specific test
poetry run pytest tests/test_dynamic_supervisor/test_supervisor_real.py -v
```

## Best Practices

1. **Agent Specialization**: Create focused agents for specific tasks
2. **Clear Descriptions**: Provide detailed agent descriptions for routing
3. **Capability Tags**: Use capabilities for intelligent routing
4. **Error Handling**: Implement proper error handling in agent tools
5. **State Management**: Keep state minimal and focused
6. **Testing**: Use real components, avoid mocks

## Common Patterns

### Multi-Step Tasks

```python
# Supervisor can coordinate multi-step workflows
result = await supervisor.arun(
    "First research the topic, then summarize findings, finally create a presentation",
    state=state
)
```

### Conditional Agent Activation

```python
# Activate agents based on task analysis
if "calculation" in task_analysis:
    state.activate_agent("math_agent")
if "research" in task_analysis:
    state.activate_agent("search_agent")
```

## Troubleshooting

### Common Issues

1. **Agent Not Found**: Ensure agent is added to state and active
2. **Tool Generation Fails**: Check agent descriptions and capabilities
3. **Execution Errors**: Verify agent implementations are correct
4. **State Persistence**: Use proper state management between calls

### Debug Tips

```python
# Check agent registry
print(state.list_agents())

# Verify tool generation
tools = state.get_all_tools()
print([tool.name for tool in tools])

# Monitor execution
supervisor.auto_sync_tools = True  # Enable automatic tool sync
```

## Related Documentation

- [Examples](../../../../examples/supervisor/) - Usage examples and patterns
- [Tests](../../../../tests/supervisor/) - Test implementations
- [Patterns](../../../../docs/supervisor/) - Architecture patterns and guides

## API Reference

### DynamicSupervisorAgent

Main supervisor class with full API documentation.

### SupervisorStateWithTools

State management class with agent registry and tool generation.

### create_dynamic_supervisor

Factory function for creating configured supervisors.

For detailed API documentation, see the inline docstrings in the source code.
