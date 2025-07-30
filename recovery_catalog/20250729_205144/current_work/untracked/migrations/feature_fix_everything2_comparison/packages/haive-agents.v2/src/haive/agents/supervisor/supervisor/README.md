# Supervisor Agents

Supervisor agents that coordinate and route between multiple specialized agents.

## Overview

The supervisor module provides agents that can manage and coordinate other agents:

- **SupervisorAgent**: Routes tasks to specialized agents based on context
- **DynamicSupervisor**: Adds runtime agent management and tool aggregation

Both supervisors extend ReactAgent to leverage its looping behavior for continuous routing decisions.

## Key Features

### SupervisorAgent

- Intelligent routing based on conversation context
- Agent registration and management
- Automatic tool aggregation from registered agents
- LLM-powered routing decisions
- Conversation history tracking

### DynamicSupervisor

All SupervisorAgent features plus:

- Add/remove agents at runtime
- Automatic graph rebuilding when agents change
- Dynamic tool discovery and aggregation
- Agent capability tracking
- Performance monitoring

## Usage Examples

### Basic SupervisorAgent

```python
from haive.agents.supervisor import SupervisorAgent
from haive.agents.simple import SimpleAgent
from haive.agents.research import ResearchAgent
from haive.core.engine.aug_llm import AugLLMConfig

# Create specialized agents
writer = SimpleAgent(name="writer", engine=AugLLMConfig())
researcher = ResearchAgent(name="researcher", engine=AugLLMConfig())

# Create supervisor
supervisor = SupervisorAgent(
    name="project_manager",
    engine=AugLLMConfig(temperature=0.3),
    registered_agents={
        "writer": writer,
        "researcher": researcher
    }
)

# Supervisor automatically routes to appropriate agent
result = await supervisor.arun("Research climate change and write a report")
```

### DynamicSupervisor with Runtime Management

```python
from haive.agents.supervisor import DynamicSupervisor
from haive.agents.simple import SimpleAgent

# Start with empty supervisor
supervisor = DynamicSupervisor(
    name="dynamic_manager",
    engine=AugLLMConfig()
)

# Add agents at runtime
await supervisor.add_agent("analyst", SimpleAgent(
    name="analyst",
    engine=AugLLMConfig(),
    system_message="You are a data analyst"
))

# Agent's tools are automatically available
await supervisor.add_agent("coder", SimpleAgent(
    name="coder",
    engine=AugLLMConfig(),
    tools=[python_repl_tool]
))

# Remove agents when no longer needed
await supervisor.remove_agent("analyst")

# List current agents
agents = supervisor.list_agents()
print(f"Active agents: {agents}")
```

### Custom Routing Logic

```python
class CustomSupervisor(SupervisorAgent):
    """Supervisor with custom routing rules."""

    def route_to_agent(self, query: str) -> str:
        """Custom routing logic."""
        if "urgent" in query.lower():
            return "priority_handler"
        elif "code" in query.lower():
            return "developer"
        else:
            # Fall back to LLM routing
            return super().route_to_agent(query)
```

## Architecture

### Routing Flow

1. User sends query to supervisor
2. Supervisor analyzes query and conversation history
3. Routing decision made (LLM or custom logic)
4. Query forwarded to selected agent
5. Agent response returned to user
6. Loop continues for multi-turn conversations

### Tool Aggregation

- Supervisor automatically discovers tools from registered agents
- Tools are prefixed with agent name to avoid conflicts
- Dynamic supervisors rebuild tool list when agents change

## Configuration

### Supervisor Settings

```python
supervisor = SupervisorAgent(
    name="supervisor",
    engine=AugLLMConfig(
        temperature=0.3,  # Lower temperature for consistent routing
        system_message="Route tasks to the most appropriate agent"
    ),
    max_iterations=10,  # From ReactAgent
    registered_agents={...}
)
```

### Dynamic Supervisor Settings

```python
supervisor = DynamicSupervisor(
    name="dynamic",
    engine=AugLLMConfig(),
    enable_monitoring=True,  # Track agent performance
    auto_rebuild=True,  # Rebuild graph on changes
    tool_prefix_format="{agent_name}_{tool_name}"  # Tool naming
)
```

## Testing

```bash
# Run supervisor tests
poetry run pytest packages/haive-agents/tests/supervisor/ -v

# Run specific dynamic supervisor tests
poetry run pytest packages/haive-agents/tests/supervisor/experiments/test_dynamic_supervisor.py -v
```

## Best Practices

1. **Agent Specialization**: Create agents with clear, focused roles
2. **Routing Instructions**: Provide clear system messages for routing
3. **Tool Management**: Be mindful of tool name conflicts
4. **Performance**: Monitor agent usage with DynamicSupervisor
5. **Error Handling**: Implement fallback routing strategies

## See Also

- [ReactAgent](../react/README.md) - Base class for supervisors
- [MultiAgent](../multi/README.md) - Alternative coordination pattern
- [SimpleAgent](../simple/README.md) - For creating specialized agents
