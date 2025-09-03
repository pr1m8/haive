# Supervisor Examples

This directory contains comprehensive examples demonstrating different supervisor patterns and usage scenarios. Examples are organized by complexity and use case.

## Directory Structure

### `/basic/`

Simple, straightforward examples for getting started:

- **basic_supervisor_example.py** - Basic supervisor with multiple agents

### `/advanced/`

Complex examples showing sophisticated patterns:

- **dynamic_activation_example.py** - Dynamic agent activation based on capabilities

### `/patterns/`

Architectural pattern demonstrations:

- **agent_execution_node_pattern.py** - Agent execution node pattern
- **dynamic_tool_generation_pattern.py** - Dynamic tool generation
- **state_synchronized_tools_pattern.py** - State-synchronized tool management
- **base_supervisor_pattern.py** - Base supervisor implementation
- **three_node_supervisor_pattern.py** - Three-node supervisor architecture
- **integrated_supervisor_with_handoff.py** - Integrated supervisor with handoffs
- **enhanced_supervisor_with_choice.py** - Enhanced supervisor with choice models

## Quick Start

### Basic Supervisor Usage

```python
from haive.agents.dynamic_supervisor import create_dynamic_supervisor
from haive.agents.simple import SimpleAgent

# Create supervisor
supervisor = create_dynamic_supervisor(name="task_router")

# Create state and add agents
state = supervisor.create_initial_state()
state.add_agent("math_agent", math_agent, "Mathematics expert")
state.add_agent("search_agent", search_agent, "Web search specialist")

# Route tasks
result = await supervisor.arun("Calculate 15 * 23", state=state)
```

### Running Examples

```bash
# Run basic example
poetry run python examples/supervisor/basic/basic_supervisor_example.py

# Run advanced example
poetry run python examples/supervisor/advanced/dynamic_activation_example.py

# Run pattern examples
poetry run python examples/supervisor/patterns/agent_execution_node_pattern.py
```

## Example Categories

### 1. Basic Examples

#### basic_supervisor_example.py

Demonstrates fundamental supervisor concepts:

- Creating specialized agents
- Setting up supervisor with factory function
- Adding agents to supervisor state
- Basic task routing
- Multi-step coordination

**Key Concepts:**

- Agent specialization
- Supervisor configuration
- State management
- Task routing

**Use Cases:**

- Simple task delegation
- Multi-agent coordination
- Basic routing decisions

### 2. Advanced Examples

#### dynamic_activation_example.py

Shows sophisticated agent lifecycle management:

- Starting with subset of active agents
- Keeping agents in registry but inactive
- Task analysis to identify required capabilities
- Dynamic agent activation based on need
- Resource-efficient multi-agent systems

**Key Concepts:**

- Capability-based routing
- Agent lifecycle management
- Resource optimization
- Dynamic activation

**Use Cases:**

- Resource-constrained environments
- Scalable multi-agent systems
- On-demand agent activation
- Cost-efficient agent management

### 3. Pattern Examples

#### agent_execution_node_pattern.py

Demonstrates clean agent execution architecture:

- Single generic execution node
- State-based routing decisions
- Clean separation of concerns
- Flexible agent selection

**Key Concepts:**

- Agent execution node
- State-based routing
- Generic execution patterns
- Clean architecture

#### dynamic_tool_generation_pattern.py

Shows dynamic tool creation and management:

- Registry-based tool generation
- Dynamic choice models
- Tool rebuilding on changes
- Validated agent selection

**Key Concepts:**

- Dynamic tool creation
- Registry patterns
- Choice model integration
- Tool lifecycle management

#### state_synchronized_tools_pattern.py

Demonstrates state-tool synchronization:

- Tools synchronized from state
- State-driven tool generation
- Complex state management
- Tool-state coordination

**Key Concepts:**

- State-tool synchronization
- Complex state management
- Tool generation patterns
- State coordination

## Running Examples

### Prerequisites

```bash
# Install dependencies
poetry install

# Set up environment variables (if needed)
export OPENAI_API_KEY=your_key_here
export ANTHROPIC_API_KEY=your_key_here
```

### Basic Execution

```bash
# Run from project root
poetry run python examples/supervisor/basic/basic_supervisor_example.py

# Run with verbose output
poetry run python examples/supervisor/basic/basic_supervisor_example.py --verbose

# Run specific pattern
poetry run python examples/supervisor/patterns/agent_execution_node_pattern.py
```

### Advanced Execution

```bash
# Run with custom configuration
poetry run python examples/supervisor/advanced/dynamic_activation_example.py --config custom_config.json

# Run with different models
poetry run python examples/supervisor/basic/basic_supervisor_example.py --model gpt-4-turbo

# Run with debugging
poetry run python examples/supervisor/patterns/dynamic_tool_generation_pattern.py --debug
```

## Example Modifications

### Customizing Agents

```python
# Create custom agents for your use case
custom_agent = SimpleAgent(
    name="custom_agent",
    engine=AugLLMConfig(
        model="gpt-4",
        tools=[your_custom_tools],
        system_message="Your custom system message"
    )
)

# Add to supervisor
state.add_agent("custom", custom_agent, "Custom agent description")
```

### Modifying Supervisor Configuration

```python
# Create custom supervisor
supervisor = DynamicSupervisorAgent(
    name="custom_supervisor",
    engine=AugLLMConfig(
        model="gpt-4",
        temperature=0.0,
        system_message="Custom supervisor instructions"
    ),
    enable_agent_builder=True,
    auto_sync_tools=True
)
```

### Adding Custom Tools

```python
from langchain_core.tools import tool

@tool
def custom_tool(input_data: str) -> str:
    \"\"\"Custom tool for specific functionality.\"\"\"
    # Your tool implementation
    return processed_result

# Add to agent
agent = SimpleAgent(
    name="tool_agent",
    engine=AugLLMConfig(tools=[custom_tool])
)
```

## Common Patterns

### 1. Multi-Domain Coordination

```python
# Agents for different domains
agents = {
    "math": create_math_agent(),
    "search": create_search_agent(),
    "code": create_code_agent(),
    "analysis": create_analysis_agent()
}

# Supervisor coordinates across domains
for name, agent in agents.items():
    state.add_agent(name, agent, f"{name.title()} specialist")
```

### 2. Hierarchical Supervision

```python
# Create sub-supervisors for specific domains
research_supervisor = create_research_supervisor()
analysis_supervisor = create_analysis_supervisor()

# Main supervisor coordinates sub-supervisors
state.add_agent("research", research_supervisor, "Research coordination")
state.add_agent("analysis", analysis_supervisor, "Analysis coordination")
```

### 3. Conditional Agent Activation

```python
# Activate agents based on task analysis
task_analysis = analyze_task(user_request)

for capability in task_analysis.required_capabilities:
    if capability == "search" and not state.is_agent_active("search"):
        state.activate_agent("search")
    elif capability == "calculation" and not state.is_agent_active("math"):
        state.activate_agent("math")
```

### 4. Error Handling and Recovery

```python
try:
    result = await supervisor.arun(task, state=state)
except AgentExecutionError as e:
    # Handle agent execution errors
    logger.error(f"Agent execution failed: {e}")
    # Implement retry logic or fallback
    result = await supervisor.arun(simplified_task, state=state)
```

## Best Practices

### 1. Agent Design

- **Specialized agents** for specific tasks
- **Clear agent descriptions** for routing
- **Robust error handling** in agent implementations
- **Appropriate tool selection** for each agent

### 2. Supervisor Configuration

- **Clear system messages** for routing logic
- **Appropriate model selection** for complexity
- **Proper state management** for multi-turn interactions
- **Resource optimization** for cost efficiency

### 3. State Management

- **Minimal state** for performance
- **Clear state transitions** for debugging
- **Proper state persistence** for long conversations
- **State validation** for correctness

### 4. Error Handling

- **Graceful degradation** when agents fail
- **Retry logic** for transient failures
- **Fallback agents** for critical functions
- **Comprehensive logging** for debugging

## Performance Considerations

### 1. Agent Activation

- **Lazy loading** - Only activate agents when needed
- **Resource pooling** - Share resources between agents
- **Caching** - Cache agent results when appropriate
- **Monitoring** - Track agent performance and usage

### 2. State Management

- **State size** - Keep state minimal for performance
- **State updates** - Batch updates when possible
- **State persistence** - Use appropriate storage
- **State cleanup** - Clean up old state regularly

### 3. Tool Management

- **Tool caching** - Cache tool results when appropriate
- **Tool optimization** - Optimize tool implementations
- **Tool monitoring** - Track tool usage and performance
- **Tool updates** - Keep tools synchronized with state

## Troubleshooting

### Common Issues

1. **Agent not found** - Check agent registration and activation
2. **Tool generation fails** - Verify agent descriptions and state
3. **Execution errors** - Check agent implementations and tool definitions
4. **Performance issues** - Monitor agent usage and state size

### Debug Tips

```python
# Enable debug logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Check agent registry
print(state.list_agents())

# Verify tool generation
tools = state.get_all_tools()
print([tool.name for tool in tools])

# Monitor execution
supervisor.auto_sync_tools = True
```

## Contributing

When adding new examples:

1. Follow the existing structure and naming conventions
2. Include comprehensive docstrings and comments
3. Test examples thoroughly before submission
4. Update this README with new example descriptions
5. Ensure examples work with current API versions

## Related Documentation

- [Supervisor Implementation](../../src/haive/agents/supervisor/) - Main supervisor code
- [Dynamic Supervisor](../../src/haive/agents/dynamic_supervisor/) - Dynamic supervisor implementation
- [Tests](../../tests/supervisor/) - Test implementations
- [Documentation](../../docs/supervisor/) - Architecture and patterns
