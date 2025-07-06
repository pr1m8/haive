# Haive Coding Style Guide

This guide outlines the coding standards, project structure, and development practices for the Haive project.

## Project Structure

### Package Organization

```
haive/
├── packages/
│   ├── haive-core/          # Core engine, state management, and infrastructure
│   ├── haive-agents/        # Pre-built agent implementations
│   ├── haive-tools/         # Tool integrations and toolkits
│   ├── haive-games/         # Game environments and agents
│   ├── haive-dataflow/      # Streaming and data processing
│   ├── haive-mcp/           # Model Context Protocol integration
│   └── haive-prebuilt/      # Ready-to-use agent configurations
```

### Package Internal Structure

Each package follows this structure:

```
packages/haive-{name}/
├── src/
│   └── haive/
│       └── {name}/
│           ├── __init__.py      # Package exports and documentation
│           ├── agent.py         # Main agent implementation (if applicable)
│           ├── config.py        # Configuration classes
│           ├── state.py         # State schemas
│           ├── example.py       # Example usage (NOT in examples/)
│           └── README.md        # Module-specific documentation
├── tests/
│   ├── conftest.py             # Shared test fixtures
│   ├── test_agent.py           # Unit tests for agent
│   ├── test_integration.py     # Integration tests
│   └── test_examples.py        # Test the examples work
├── pyproject.toml              # Package configuration
└── README.md                   # Package documentation
```

## Code Style

### Python Code Standards

#### Imports

```python
# Standard library imports first
import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

# Third-party imports
import numpy as np
from langchain_core.messages import HumanMessage
from pydantic import BaseModel, Field

# Local imports (absolute imports for namespace packages)
from haive.core.engine import AugLLMConfig
from haive.agents.base import Agent
```

#### Type Hints

Always use type hints for function signatures and class attributes:

```python
from typing import Dict, List, Optional, Union, TypeVar, Generic

T = TypeVar('T')

class Agent(Generic[T]):
    def __init__(
        self,
        name: str,
        config: Optional[Dict[str, Any]] = None,
        tools: Optional[List[Tool]] = None
    ) -> None:
        ...

    async def arun(
        self,
        input_data: Union[str, Dict[str, Any]]
    ) -> T:
        ...
```

#### Docstrings

Use Google-style docstrings for all public functions, classes, and modules:

```python
"""Module for implementing ReAct pattern agents.

This module provides agents that use the Reasoning and Acting (ReAct)
pattern to solve problems by interleaving thought, action, and observation.
"""

class ReactAgent(Agent):
    """ReAct pattern agent with tool use capabilities.

    The ReactAgent implements the ReAct (Reasoning + Acting) pattern,
    allowing it to solve complex problems by thinking step-by-step
    and using tools when necessary.

    Attributes:
        tools: List of available tools for the agent to use.
        max_iterations: Maximum number of reasoning iterations.
        verbose: Whether to print reasoning traces.

    Example:
        >>> agent = ReactAgent(
        ...     name="researcher",
        ...     tools=[SearchTool(), CalculatorTool()],
        ...     max_iterations=5
        ... )
        >>> result = await agent.arun("What is the population of Tokyo?")
    """

    async def arun(
        self,
        query: str,
        config: Optional[RunnableConfig] = None
    ) -> AgentResponse:
        """Execute the agent with a query.

        Args:
            query: The input query to process.
            config: Optional configuration for the run, including
                thread_id for conversation continuity.

        Returns:
            AgentResponse containing the result and metadata.

        Raises:
            ToolExecutionError: If a tool fails during execution.
            MaxIterationsError: If max iterations exceeded.
        """
```

#### Class Structure

```python
class MyAgent(BaseAgent):
    """One-line class description.

    Detailed description of the agent's purpose and behavior.
    """

    # Class constants
    DEFAULT_TEMPERATURE = 0.7
    MAX_RETRIES = 3

    # Pydantic fields with descriptions
    model_name: str = Field(
        default="gpt-4",
        description="The LLM model to use"
    )

    temperature: float = Field(
        default=DEFAULT_TEMPERATURE,
        ge=0.0,
        le=1.0,
        description="Sampling temperature for generation"
    )

    # Private attributes use underscore prefix
    _client: Optional[AsyncOpenAI] = None

    def __init__(self, **kwargs):
        """Initialize the agent."""
        super().__init__(**kwargs)
        self._setup_client()

    # Public methods
    async def arun(self, input_data: str) -> str:
        """Main execution method."""
        ...

    # Private methods use underscore prefix
    def _setup_client(self) -> None:
        """Setup the API client."""
        ...
```

### Async Patterns

Always use async/await for I/O operations:

```python
# Good
async def fetch_data(url: str) -> Dict[str, Any]:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()

# Bad - blocking I/O
def fetch_data(url: str) -> Dict[str, Any]:
    response = requests.get(url)
    return response.json()
```

### Error Handling

Use specific exceptions and always include context:

```python
class AgentError(Exception):
    """Base exception for agent errors."""
    pass

class ToolExecutionError(AgentError):
    """Raised when tool execution fails."""
    pass

# Usage
try:
    result = await tool.execute(query)
except ToolNotFoundError as e:
    logger.error(f"Tool {tool_name} not found: {e}")
    raise
except Exception as e:
    logger.error(f"Unexpected error in {self.__class__.__name__}: {e}")
    raise AgentError(f"Failed to execute tool {tool_name}") from e
```

## Testing

### Test Location

Tests MUST be in `packages/haive-{name}/tests/` directory, NOT in the source tree.

### Test Structure

```python
# tests/test_agent.py
import pytest
from unittest.mock import AsyncMock, Mock

from haive.agents.react import ReactAgent
from haive.tools import SearchTool


class TestReactAgent:
    """Test suite for ReactAgent."""

    @pytest.fixture
    def agent(self):
        """Create a test agent instance."""
        return ReactAgent(
            name="test_agent",
            tools=[SearchTool()],
            temperature=0  # Deterministic for tests
        )

    @pytest.mark.asyncio
    async def test_simple_query(self, agent):
        """Test agent handles simple queries."""
        result = await agent.arun("What is 2+2?")
        assert "4" in result.content

    @pytest.mark.asyncio
    async def test_tool_usage(self, agent, mock_search_tool):
        """Test agent correctly uses tools."""
        agent.tools = [mock_search_tool]
        result = await agent.arun("Search for Python tutorials")

        mock_search_tool.execute.assert_called_once()
        assert result.tool_calls[0].tool_name == "search"

    @pytest.mark.asyncio
    async def test_error_handling(self, agent):
        """Test agent handles errors gracefully."""
        with pytest.raises(ToolExecutionError):
            await agent.arun("Use nonexistent tool")
```

### Test Fixtures

Use `conftest.py` for shared fixtures:

```python
# tests/conftest.py
import pytest
from unittest.mock import AsyncMock

@pytest.fixture
def mock_llm():
    """Mock LLM for testing."""
    llm = AsyncMock()
    llm.ainvoke.return_value = AIMessage(content="Test response")
    return llm

@pytest.fixture
def mock_search_tool():
    """Mock search tool."""
    tool = AsyncMock()
    tool.name = "search"
    tool.execute.return_value = {"results": ["result1", "result2"]}
    return tool
```

### Integration Tests

```python
# tests/test_integration.py
import pytest
from haive.agents.rag import SimpleRAGAgent
from haive.core.retrieval import VectorRetriever

@pytest.mark.integration
@pytest.mark.asyncio
async def test_rag_with_real_retriever():
    """Test RAG agent with actual retriever."""
    # Use test collection
    retriever = VectorRetriever(collection="test_docs")
    agent = SimpleRAGAgent(retriever=retriever)

    result = await agent.arun("What is the main feature?")
    assert result.source_documents
    assert len(result.source_documents) > 0
```

## Examples

### Example Files

Each major module should have an `example.py` file in its directory (NOT in a separate examples folder):

```python
# packages/haive-agents/src/haive/agents/react/example.py
"""Example usage of ReactAgent.

This example demonstrates how to use the ReactAgent for
web research and calculation tasks.
"""

import asyncio
from haive.agents.react import ReactAgent
from haive.tools import SearchTool, CalculatorTool, WikipediaTool


async def main():
    """Run example ReactAgent usage."""
    # Create agent with tools
    agent = ReactAgent(
        name="research_assistant",
        tools=[
            SearchTool(),
            CalculatorTool(),
            WikipediaTool()
        ],
        verbose=True  # Show reasoning trace
    )

    # Example 1: Simple calculation
    print("Example 1: Calculation")
    result = await agent.arun("What is 15% of 2500?")
    print(f"Result: {result}")

    # Example 2: Research task
    print("\nExample 2: Research")
    result = await agent.arun(
        "What is the population of Tokyo and what percentage "
        "is it of Japan's total population?"
    )
    print(f"Result: {result}")

    # Example 3: Multi-step reasoning
    print("\nExample 3: Complex task")
    result = await agent.arun(
        "Find the three largest cities in Japan by population, "
        "calculate their combined population, and determine what "
        "percentage this is of Japan's total population."
    )
    print(f"Result: {result}")


if __name__ == "__main__":
    asyncio.run(main())
```

## Configuration

### Agent Configuration

Use Pydantic models for configuration:

```python
# config.py
from pydantic import BaseModel, Field
from typing import Optional, List

class ReactAgentConfig(BaseModel):
    """Configuration for ReactAgent."""

    model_config = ConfigDict(
        validate_assignment=True,
        extra="forbid"
    )

    max_iterations: int = Field(
        default=10,
        ge=1,
        le=50,
        description="Maximum reasoning iterations"
    )

    temperature: float = Field(
        default=0.7,
        ge=0.0,
        le=2.0,
        description="LLM sampling temperature"
    )

    tools: List[str] = Field(
        default_factory=list,
        description="List of tool names to load"
    )

    enable_caching: bool = Field(
        default=True,
        description="Cache tool results"
    )
```

## State Management

### State Schemas

Define clear state schemas using Pydantic:

```python
# state.py
from pydantic import BaseModel, Field
from typing import List, Dict, Any
from langchain_core.messages import BaseMessage

class ReactState(BaseModel):
    """State for ReAct agent execution."""

    messages: List[BaseMessage] = Field(
        default_factory=list,
        description="Conversation messages"
    )

    reasoning_steps: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="Reasoning trace"
    )

    tool_calls: List[ToolCall] = Field(
        default_factory=list,
        description="History of tool calls"
    )

    current_iteration: int = Field(
        default=0,
        description="Current reasoning iteration"
    )

    final_answer: Optional[str] = Field(
        default=None,
        description="Final answer when complete"
    )
```

## Logging

Use structured logging:

```python
from haive.core.logging import get_logger

logger = get_logger(__name__)

class MyAgent:
    def __init__(self, name: str):
        self.name = name
        logger.info(
            "Initializing agent",
            agent_name=name,
            agent_type=self.__class__.__name__
        )

    async def arun(self, query: str):
        logger.debug("Processing query", query=query[:100])

        try:
            result = await self._process(query)
            logger.info(
                "Query processed successfully",
                query_length=len(query),
                result_length=len(result)
            )
            return result
        except Exception as e:
            logger.error(
                "Failed to process query",
                error=str(e),
                query=query[:100]
            )
            raise
```

## Git Workflow

### Branch Naming

- `feat/description` - New features
- `fix/description` - Bug fixes
- `docs/description` - Documentation only
- `refactor/description` - Code refactoring
- `test/description` - Test additions/changes

### Commit Messages

Follow conventional commits:

```
feat(agents): add retry logic to ReactAgent

- Add exponential backoff for tool failures
- Make max retries configurable
- Add tests for retry behavior

Closes #123
```

### Pull Request Template

```markdown
## Description

Brief description of changes

## Type of Change

- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing

- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Example scripts run successfully

## Checklist

- [ ] Code follows style guide
- [ ] Self-review completed
- [ ] Comments added for complex logic
- [ ] Documentation updated
- [ ] No hardcoded secrets
```

## Performance Guidelines

1. **Async First**: Always use async for I/O operations
2. **Streaming**: Support streaming responses when possible
3. **Caching**: Cache expensive operations (with TTL)
4. **Batching**: Batch API calls when possible
5. **Resource Limits**: Set timeouts and token limits

## Security

1. **No Hardcoded Secrets**: Use environment variables
2. **Input Validation**: Always validate user input
3. **Rate Limiting**: Implement rate limits for external APIs
4. **Error Messages**: Don't expose internal details in errors
5. **Dependencies**: Keep dependencies up to date

## Documentation

Each module should have:

1. **Module docstring** explaining purpose
2. **Class/function docstrings** with examples
3. **README.md** with usage examples
4. **Type hints** for all public APIs
5. **Example file** showing real usage
