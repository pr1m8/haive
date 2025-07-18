# Agent Development Template

## Overview

This template provides a structured approach for developing new agents in the Haive framework. Follow this guide to ensure consistency and compatibility with the existing agent ecosystem.

## Basic Agent Template

```python
"""
Agent Name: MyCustomAgent
Purpose: [Brief description of what this agent does]
Category: [conversational/task/utility/specialized]
"""

from typing import Any, Dict, List, Optional
from haive.core.agent import BaseAgent
from haive.core.schema import AgentConfig, AgentState
from haive.core.decorators import log_execution, validate_input


class MyCustomAgentConfig(AgentConfig):
    """Configuration for MyCustomAgent."""

    # Add custom configuration fields
    custom_field: str = "default_value"
    max_retries: int = 3
    enable_feature_x: bool = False

    class Config:
        schema_extra = {
            "example": {
                "name": "my_agent",
                "model": "gpt-4",
                "custom_field": "custom_value",
                "max_retries": 5
            }
        }


class MyCustomAgent(BaseAgent):
    """
    A custom agent that [describe main functionality].

    This agent is designed to [explain use cases and benefits].

    Attributes:
        config: Agent configuration
        state: Current agent state

    Example:
        >>> agent = MyCustomAgent(
        ...     name="example",
        ...     model="gpt-4",
        ...     custom_field="value"
        ... )
        >>> result = await agent.execute("task description")
    """

    config_class = MyCustomAgentConfig

    def __init__(self, **kwargs):
        """Initialize the agent with configuration."""
        super().__init__(**kwargs)
        # Initialize custom attributes
        self._setup_custom_components()

    def _setup_custom_components(self):
        """Set up any custom components needed by the agent."""
        # Initialize tools, memory, or other components
        pass

    @validate_input
    @log_execution
    async def execute(self, input_data: Any) -> Dict[str, Any]:
        """
        Execute the main agent logic.

        Args:
            input_data: Input for the agent to process

        Returns:
            Dict containing the execution results

        Raises:
            AgentExecutionError: If execution fails
        """
        try:
            # Validate input
            validated_input = self._validate_input(input_data)

            # Main execution logic
            result = await self._process(validated_input)

            # Post-process results
            final_result = self._format_output(result)

            return final_result

        except Exception as e:
            return self._handle_error(e)

    async def _process(self, input_data: Any) -> Any:
        """Core processing logic."""
        # Implement main agent logic here

        # Example: Call LLM
        response = await self.llm.generate(
            prompt=self._build_prompt(input_data),
            **self.config.generation_kwargs
        )

        return response

    def _build_prompt(self, input_data: Any) -> str:
        """Build the prompt for LLM interaction."""
        return f"""
        System: {self.config.system_prompt}

        Task: {input_data}

        Instructions: [Specific instructions for the task]
        """

    def _validate_input(self, input_data: Any) -> Any:
        """Validate and preprocess input."""
        # Add validation logic
        if not input_data:
            raise ValueError("Input cannot be empty")
        return input_data

    def _format_output(self, result: Any) -> Dict[str, Any]:
        """Format the agent output."""
        return {
            "success": True,
            "result": result,
            "metadata": {
                "agent": self.config.name,
                "model": self.config.model,
                "timestamp": self._get_timestamp()
            }
        }

    def _handle_error(self, error: Exception) -> Dict[str, Any]:
        """Handle errors gracefully."""
        self.logger.error(f"Agent execution failed: {error}")
        return {
            "success": False,
            "error": str(error),
            "error_type": type(error).__name__
        }

    async def save_state(self) -> AgentState:
        """Save the current agent state."""
        return AgentState(
            config=self.config.dict(),
            memory=self.memory.serialize() if hasattr(self, 'memory') else None,
            custom_data=self._get_custom_state()
        )

    async def load_state(self, state: AgentState):
        """Load a saved agent state."""
        self.config = self.config_class(**state.config)
        if state.memory and hasattr(self, 'memory'):
            self.memory.deserialize(state.memory)
        self._load_custom_state(state.custom_data)

    def _get_custom_state(self) -> Dict[str, Any]:
        """Get custom state data."""
        return {}

    def _load_custom_state(self, state_data: Dict[str, Any]):
        """Load custom state data."""
        pass
```

## Testing Template

```python
"""Tests for MyCustomAgent."""

import pytest
from unittest.mock import Mock, patch
from haive.agents.custom import MyCustomAgent


class TestMyCustomAgent:
    """Test suite for MyCustomAgent."""

    @pytest.fixture
    def agent(self):
        """Create a test agent instance."""
        return MyCustomAgent(
            name="test_agent",
            model="gpt-4",
            custom_field="test_value"
        )

    @pytest.fixture
    def mock_llm(self):
        """Mock LLM for testing."""
        with patch('haive.agents.custom.LLM') as mock:
            yield mock

    @pytest.mark.asyncio
    async def test_execute_success(self, agent, mock_llm):
        """Test successful execution."""
        mock_llm.generate.return_value = "Expected result"

        result = await agent.execute("test input")

        assert result["success"] is True
        assert result["result"] == "Expected result"
        assert "metadata" in result

    @pytest.mark.asyncio
    async def test_execute_empty_input(self, agent):
        """Test execution with empty input."""
        result = await agent.execute("")

        assert result["success"] is False
        assert "error" in result

    @pytest.mark.asyncio
    async def test_state_persistence(self, agent):
        """Test state save and load."""
        # Modify agent state
        agent.config.custom_field = "modified"

        # Save state
        state = await agent.save_state()

        # Create new agent and load state
        new_agent = MyCustomAgent(name="new")
        await new_agent.load_state(state)

        assert new_agent.config.custom_field == "modified"

    def test_configuration(self):
        """Test agent configuration."""
        config = MyCustomAgentConfig(
            name="config_test",
            custom_field="custom",
            max_retries=5
        )

        assert config.custom_field == "custom"
        assert config.max_retries == 5
        assert config.enable_feature_x is False
```

## Documentation Template

````markdown
# MyCustomAgent

## Overview

MyCustomAgent is designed to [primary purpose]. It excels at [key strengths] and is particularly useful for [use cases].

## Installation

```bash
pip install haive-agents
```
````

## Quick Start

```python
from haive.agents import MyCustomAgent

# Create agent
agent = MyCustomAgent(
    name="assistant",
    model="gpt-4",
    custom_field="value"
)

# Execute task
result = await agent.execute("Your task here")
print(result)
```

## Configuration

| Parameter        | Type | Default   | Description                 |
| ---------------- | ---- | --------- | --------------------------- |
| name             | str  | required  | Agent identifier            |
| model            | str  | "gpt-4"   | LLM model to use            |
| custom_field     | str  | "default" | Description of custom field |
| max_retries      | int  | 3         | Maximum retry attempts      |
| enable_feature_x | bool | False     | Enable experimental feature |

## Advanced Usage

### With Custom Tools

```python
from haive.tools import CustomTool

agent = MyCustomAgent(
    tools=[CustomTool()],
    tool_selection="auto"
)
```

### With Memory

```python
agent = MyCustomAgent(
    memory_type="conversation_buffer",
    memory_size=1000
)
```

### Error Handling

```python
try:
    result = await agent.execute(task)
except AgentExecutionError as e:
    print(f"Execution failed: {e}")
```

## API Reference

### Methods

#### execute(input_data: Any) -> Dict[str, Any]

Main execution method for the agent.

**Parameters:**

- `input_data`: Task or query to process

**Returns:**

- Dictionary with execution results

#### save_state() -> AgentState

Save current agent state for persistence.

#### load_state(state: AgentState)

Load a previously saved state.

## Examples

### Example 1: Basic Usage

```python
agent = MyCustomAgent(name="basic")
result = await agent.execute("Analyze this data")
```

### Example 2: Complex Configuration

```python
agent = MyCustomAgent(
    name="advanced",
    model="gpt-4",
    temperature=0.7,
    max_tokens=2000,
    custom_field="advanced_mode",
    enable_feature_x=True
)
```

### Example 3: Integration with Other Agents

```python
from haive.agents import ChainAgent

pipeline = ChainAgent([
    MyCustomAgent(name="processor"),
    ValidationAgent(name="validator")
])
```

## Best Practices

1. Always validate input data
2. Handle errors gracefully
3. Use appropriate models for your use case
4. Monitor token usage and costs
5. Test thoroughly with edge cases

## Troubleshooting

### Common Issues

1. **Import Error**: Ensure haive-agents is installed
2. **Configuration Error**: Check required parameters
3. **Execution Timeout**: Increase timeout or optimize prompts

## See Also

- [Agent Development Guide](../guides/agent_development.md)
- [API Reference](../api/agents/custom.rst)
- [Examples](../examples/agents/custom_agent.py)

```

## Checklist

Before submitting your agent:

- [ ] **Code Quality**
  - [ ] Follows PEP 8 style guide
  - [ ] Includes comprehensive docstrings
  - [ ] Has type hints for all methods
  - [ ] Handles errors gracefully

- [ ] **Testing**
  - [ ] Unit tests cover main functionality
  - [ ] Integration tests with real LLM (optional)
  - [ ] Edge cases are tested
  - [ ] Tests pass in CI/CD

- [ ] **Documentation**
  - [ ] README.md is complete
  - [ ] API documentation is generated
  - [ ] Examples are provided
  - [ ] Configuration options are documented

- [ ] **Integration**
  - [ ] Compatible with existing tools
  - [ ] Follows schema conventions
  - [ ] Registers with agent registry
  - [ ] Works with standard workflows

- [ ] **Performance**
  - [ ] Efficient token usage
  - [ ] Appropriate timeout handling
  - [ ] Memory management considered
  - [ ] Concurrent execution safe

## Next Steps

1. Copy this template to start your agent
2. Implement the core logic in `_process()`
3. Add custom configuration fields
4. Write comprehensive tests
5. Document usage and examples
6. Submit PR with your agent

## Support

For questions or assistance:
- Check existing agents for examples
- Review the [Agent Development Guide](../guides/agent_development.md)
- Ask in the development channel
- Open an issue for bugs or features
```
