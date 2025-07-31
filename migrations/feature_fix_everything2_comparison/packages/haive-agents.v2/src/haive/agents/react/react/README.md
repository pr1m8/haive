# React Agent

The React Agent implements the ReAct (Reasoning and Acting) pattern, extending SimpleAgent with looping behavior for iterative reasoning and tool usage. It provides a clean, minimal implementation that forms the foundation for more complex agent patterns.

## Overview

The React Agent follows the ReAct paradigm where agents:

1. **Reason** about the current situation
2. **Act** by using tools or generating responses
3. **Observe** the results
4. **Loop** back to reasoning until the task is complete

This creates a powerful reasoning loop that allows agents to break down complex tasks, use tools iteratively, and refine their responses based on observations.

## Key Components

- **ReactAgent**: Main agent class extending SimpleAgent
- **ReAct Loop**: Graph modification for continuous reasoning
- **Tool Integration**: Seamless tool usage within the loop
- **State Management**: Maintains conversation and execution state

## Installation

This module is part of the `haive-agents` package. Install it using:

```bash
pip install haive-agents
```

## Usage Examples

### Basic Usage

```python
from haive.agents.react import ReactAgent
from haive.core.engine.aug_llm import AugLLMConfig
from langchain_core.tools import tool

@tool
def calculator(expression: str) -> str:
    \"\"\"Calculate mathematical expressions.\"\"\"
    try:
        result = eval(expression)
        return str(result)
    except:
        return "Error in calculation"

# Create React agent
agent = ReactAgent(
    name="reasoning_agent",
    engine=AugLLMConfig(
        model="gpt-4",
        tools=[calculator],
        system_message="You are a helpful assistant that thinks step by step."
    )
)

# Run with reasoning loop
result = await agent.arun("What is 15 * 23 + 7?")
```

### Advanced Multi-Tool Usage

```python
from haive.agents.react import ReactAgent
from haive.core.engine.aug_llm import AugLLMConfig

# Create agent with multiple tools
agent = ReactAgent(
    name="multi_tool_agent",
    engine=AugLLMConfig(
        model="gpt-4",
        tools=[search_tool, calculator_tool, file_tool],
        system_message=\"\"\"You are a research assistant. For each query:
        1. Think about what information you need
        2. Use appropriate tools to gather information
        3. Analyze the results
        4. Provide a comprehensive answer
        \"\"\"
    )
)

# Complex multi-step task
result = await agent.arun(
    "Find the current population of Tokyo and calculate the population density"
)
```

### Custom State Management

```python
from haive.core.schema import StateSchema
from pydantic import Field
from typing import List

class CustomReactState(StateSchema):
    reasoning_steps: List[str] = Field(default_factory=list)
    tool_usage_count: int = Field(default=0)
    current_objective: str = Field(default="")

agent = ReactAgent(
    name="custom_agent",
    engine=engine,
    state_schema=CustomReactState
)
```

## Architecture

### ReAct Loop Implementation

The React Agent modifies the SimpleAgent graph to create loops:

```python
def build_graph(self) -> BaseGraph:
    \"\"\"Build ReAct graph with proper looping.\"\"\"
    # Build base graph first
    graph = super().build_graph()

    # Modify connections for ReAct looping
    if self._needs_tool_node() and "tool_node" in graph.nodes:
        graph.remove_edge("tool_node", END)
        graph.add_edge("tool_node", "agent_node")  # Loop back

    return graph
```

### Execution Flow

1. **Agent Node**: Reasoning and decision making
2. **Tool Node**: Execute selected tools
3. **Parse Node**: Process tool results (if needed)
4. **Loop Back**: Return to agent node for continued reasoning
5. **End**: Complete when task is finished

## Testing

```bash
# Run React agent tests
poetry run pytest tests/react/ -v

# Run specific test
poetry run pytest tests/react/test_react_agent.py -v
```

## Best Practices

1. **Clear System Messages**: Provide explicit reasoning instructions
2. **Tool Design**: Create tools with clear descriptions and error handling
3. **Iteration Limits**: Set max_iterations to prevent infinite loops
4. **State Management**: Use appropriate state schemas for complex tasks
5. **Error Handling**: Implement robust error handling for tool failures

## Common Use Cases

- **Mathematical Problem Solving**: Break down complex calculations
- **Research and Analysis**: Gather information from multiple sources
- **Data Analysis**: Process and analyze data iteratively
- **Content Generation**: Create content with research and refinement
- **Code Development**: Write and test code iteratively

## API Reference

### ReactAgent

Main React agent class inheriting from SimpleAgent with ReAct loop capabilities.

For detailed API documentation, see the inline docstrings in the source code.

## See Also

- [SimpleAgent](../simple/) - Base agent implementation
- [Dynamic Supervisor](../dynamic_supervisor/) - Multi-agent coordination
- [Examples](../../../examples/react/) - Usage examples and patterns
- [Tests](../../../tests/react/) - Test implementations
