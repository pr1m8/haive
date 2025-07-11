# Python Docstring & Type Hints Guide for Haive

## Overview

This guide shows how to write comprehensive docstrings with proper type hints and examples for the Haive codebase.

## File-Level Docstrings

Every Python file should start with a module docstring:

```python
"""Agent execution engine with tool support.

This module provides the core execution engine for running agents with
integrated tool support, state management, and streaming capabilities.

Key components:
    - :class:`AgentEngine`: Main execution engine
    - :class:`EngineConfig`: Configuration management
    - :class:`ExecutionContext`: Runtime context

Example:
    Basic usage with tools::

        >>> from haive.core.engine import AgentEngine
        >>> from haive.tools import Calculator
        >>>
        >>> engine = AgentEngine(model="gpt-4", tools=[Calculator()])
        >>> result = await engine.execute("What is 25 * 4?")
        >>> print(result)
        '25 * 4 = 100'

    Streaming responses::

        >>> async for chunk in engine.stream("Tell me a story"):
        ...     print(chunk, end="", flush=True)
        'Once upon a time...'

Note:
    This module requires async context. All methods are async-first.

See Also:
    - :doc:`/guides/engines`: Engine usage guide
    - :mod:`haive.core.schema`: State management
"""
```

## Class Docstrings with Type Hints

```python
from typing import Dict, List, Optional, Any, Union, Callable, TypeVar, Generic
from typing_extensions import Literal, Protocol, TypedDict, Annotated
from pydantic import BaseModel, Field

T = TypeVar('T', bound=BaseModel)
StateT = TypeVar('StateT', bound='BaseState')


class AgentEngine(Generic[StateT]):
    """Execution engine for AI agents with tool support.

    The engine manages agent execution, tool calls, and state updates.
    It supports multiple LLM backends and streaming responses.

    Type Parameters:
        StateT: State schema type, must inherit from BaseState

    Args:
        model: Model identifier (e.g., "gpt-4", "claude-3")
        temperature: Sampling temperature between 0.0 and 2.0
        tools: Optional list of tools available to the agent
        state_schema: State schema class for type safety
        **kwargs: Additional model-specific parameters

    Example:
        With typed state::

            >>> from typing import List
            >>> from pydantic import Field
            >>>
            >>> class ConversationState(BaseState):
            ...     messages: List[Message] = Field(default_factory=list)
            ...     context: Dict[str, Any] = Field(default_factory=dict)
            >>>
            >>> engine: AgentEngine[ConversationState] = AgentEngine(
            ...     model="gpt-4",
            ...     state_schema=ConversationState,
            ...     temperature=0.7
            ... )
            >>>
            >>> # Type checker knows state.messages is List[Message]
            >>> state = engine.get_state()
            >>> state.messages.append(Message(role="user", content="Hi"))

        With tools::

            >>> engine = AgentEngine(
            ...     model="gpt-4",
            ...     tools=[WebSearch(), Calculator()],
            ...     tool_choice="auto"  # auto, none, required
            ... )
            >>> result = await engine.execute(
            ...     "Search for Python tutorials and calculate 2^10"
            ... )
    """

    def __init__(
        self,
        model: str,
        temperature: float = 0.7,
        tools: Optional[List['BaseTool']] = None,
        state_schema: Optional[type[StateT]] = None,
        **kwargs: Any
    ) -> None:
        """Initialize the engine with configuration."""
        ...
```

## Method Docstrings with Complex Types

```python
from asyncio import Queue
from collections.abc import AsyncIterator
from datetime import datetime


async def execute(
    self,
    prompt: Union[str, List[Dict[str, str]]],
    *,
    tools: Optional[List['BaseTool']] = None,
    tool_choice: Literal["auto", "none", "required"] = "auto",
    context: Optional[Dict[str, Any]] = None,
    callbacks: Optional[List[Callable[[str], None]]] = None,
    timeout: Optional[float] = None,
    max_retries: int = 3,
    metadata: Optional[Dict[str, Any]] = None
) -> 'ExecutionResult[StateT]':
    """Execute agent with prompt and return typed result.

    Args:
        prompt: User prompt as string or conversation history as list of dicts.
            When list, each dict must have 'role' and 'content' keys.
        tools: Override default tools for this execution. If None, uses engine tools.
        tool_choice: How to handle tool selection:
            - "auto": Model decides whether to use tools
            - "none": Prevent tool usage for this call
            - "required": Force tool usage
        context: Additional context merged into agent state
        callbacks: List of sync callbacks called with status updates
        timeout: Execution timeout in seconds (default: 30.0)
        max_retries: Maximum retry attempts for transient failures
        metadata: Custom metadata attached to result

    Returns:
        ExecutionResult containing:
            - content: Generated text response
            - tool_calls: List of tool calls made
            - state: Updated state after execution
            - usage: Token usage statistics
            - metadata: Execution metadata

    Raises:
        ValueError: If prompt format is invalid
        TimeoutError: If execution exceeds timeout
        ToolExecutionError: If required tool fails
        ModelError: If model API returns an error

    Example:
        Simple execution::

            >>> result = await engine.execute("What's the weather?")
            >>> print(result.content)
            'I need to check current weather data...'

        With conversation history::

            >>> history = [
            ...     {"role": "user", "content": "Hi"},
            ...     {"role": "assistant", "content": "Hello!"},
            ...     {"role": "user", "content": "What's 2+2?"}
            ... ]
            >>> result = await engine.execute(history)

        With tool override::

            >>> result = await engine.execute(
            ...     "Calculate something",
            ...     tools=[Calculator()],  # Only Calculator available
            ...     tool_choice="required"  # Must use a tool
            ... )

        With callbacks::

            >>> def print_status(msg: str) -> None:
            ...     print(f"[{datetime.now()}] {msg}")
            >>>
            >>> result = await engine.execute(
            ...     "Complex task",
            ...     callbacks=[print_status],
            ...     timeout=60.0
            ... )
            [2024-01-01 12:00:00] Starting execution...
            [2024-01-01 12:00:01] Calling tool: web_search
            [2024-01-01 12:00:03] Generating response...
    """
```

## Type Aliases and Protocols

```python
from typing import Protocol, runtime_checkable
from abc import abstractmethod

# Type aliases for clarity
MessageContent = Union[str, List[Union[str, Dict[str, Any]]]]
ToolCall = Dict[Literal["name", "arguments", "id"], Any]
ModelResponse = Union[str, Dict[str, Any]]

# Custom types with documentation
Temperature = Annotated[float, Field(ge=0.0, le=2.0)]
"""Temperature for sampling, constrained between 0.0 and 2.0.

Lower values (0.0-0.5) produce focused, deterministic outputs.
Higher values (1.0-2.0) produce creative, varied outputs.
"""

TokenLimit = Annotated[int, Field(gt=0, le=128000)]
"""Maximum tokens for generation, model-dependent.

Common limits:
- GPT-3.5: 4,096 tokens
- GPT-4: 8,192 tokens
- GPT-4-32k: 32,768 tokens
- Claude: 100,000 tokens
"""


@runtime_checkable
class ToolProtocol(Protocol):
    """Protocol for tool implementations.

    All tools must implement this interface to be used by agents.

    Example:
        >>> class MyTool:
        ...     @property
        ...     def name(self) -> str:
        ...         return "my_tool"
        ...
        ...     @property
        ...     def description(self) -> str:
        ...         return "Does something useful"
        ...
        ...     async def execute(self, **kwargs: Any) -> Any:
        ...         return {"result": "success"}
        >>>
        >>> # Runtime check
        >>> assert isinstance(MyTool(), ToolProtocol)
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """Unique tool identifier."""
        ...

    @property
    @abstractmethod
    def description(self) -> str:
        """Human-readable tool description."""
        ...

    @abstractmethod
    async def execute(self, **kwargs: Any) -> Any:
        """Execute tool with given arguments."""
        ...
```

## Return Type Documentation

```python
from dataclasses import dataclass
from enum import Enum


class ExecutionStatus(Enum):
    """Status of execution result."""
    SUCCESS = "success"
    PARTIAL = "partial"  # Some tools failed
    FAILED = "failed"
    TIMEOUT = "timeout"


@dataclass
class ExecutionResult(Generic[StateT]):
    """Result of agent execution with full context.

    Attributes:
        content: Generated text response
        tool_calls: List of tool calls made during execution
        state: Updated agent state after execution
        status: Execution status indicator
        usage: Token usage breakdown
        metadata: Additional execution metadata

    Example:
        >>> result = await engine.execute("Hello")
        >>> print(f"Response: {result.content}")
        Response: Hello! How can I help you?
        >>> print(f"Tokens used: {result.usage.total_tokens}")
        Tokens used: 42
        >>> if result.tool_calls:
        ...     print(f"Tools used: {[tc['name'] for tc in result.tool_calls]}")
    """
    content: str
    tool_calls: List[ToolCall] = field(default_factory=list)
    state: StateT = field(default_factory=dict)
    status: ExecutionStatus = ExecutionStatus.SUCCESS
    usage: 'TokenUsage' = field(default_factory=lambda: TokenUsage())
    metadata: Dict[str, Any] = field(default_factory=dict)

    @property
    def success(self) -> bool:
        """Check if execution was fully successful.

        Returns:
            True if status is SUCCESS, False otherwise

        Example:
            >>> if result.success:
            ...     process_response(result.content)
            ... else:
            ...     handle_error(result.status)
        """
        return self.status == ExecutionStatus.SUCCESS
```

## Exception Documentation

```python
class EngineError(Exception):
    """Base exception for engine errors.

    All engine-specific exceptions inherit from this class.

    Attributes:
        message: Human-readable error description
        code: Machine-readable error code
        details: Additional error context

    Example:
        >>> try:
        ...     result = await engine.execute("test")
        ... except EngineError as e:
        ...     print(f"Error: {e.message}")
        ...     print(f"Code: {e.code}")
        ...     if e.details:
        ...         print(f"Details: {e.details}")
    """

    def __init__(
        self,
        message: str,
        code: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ) -> None:
        """Initialize error with context.

        Args:
            message: Error description
            code: Error code (e.g., "TOOL_NOT_FOUND")
            details: Additional context
        """
        super().__init__(message)
        self.message = message
        self.code = code or "ENGINE_ERROR"
        self.details = details or {}


class ToolExecutionError(EngineError):
    """Raised when tool execution fails.

    Example:
        >>> try:
        ...     await engine.execute_tool("calculator", {"expr": "1/0"})
        ... except ToolExecutionError as e:
        ...     print(f"Tool {e.tool_name} failed: {e.message}")
        ...     print(f"Arguments: {e.tool_args}")
        Tool calculator failed: Division by zero
        Arguments: {'expr': '1/0'}
    """

    def __init__(
        self,
        tool_name: str,
        tool_args: Dict[str, Any],
        message: str,
        original_error: Optional[Exception] = None
    ) -> None:
        """Initialize with tool context."""
        super().__init__(
            message=f"Tool '{tool_name}' failed: {message}",
            code="TOOL_EXECUTION_ERROR",
            details={
                "tool_name": tool_name,
                "tool_args": tool_args,
                "original_error": str(original_error) if original_error else None
            }
        )
        self.tool_name = tool_name
        self.tool_args = tool_args
        self.original_error = original_error
```

## Async Iterator Documentation

```python
async def stream(
    self,
    prompt: str,
    **kwargs: Any
) -> AsyncIterator[Union[str, Dict[str, Any]]]:
    """Stream response chunks as they're generated.

    Yields:
        String chunks of generated text, or dicts with metadata
        for special events (tool calls, status updates).

    Example:
        Basic streaming::

            >>> async for chunk in engine.stream("Tell a joke"):
            ...     if isinstance(chunk, str):
            ...         print(chunk, end="", flush=True)
            ...     else:
            ...         print(f"\\nEvent: {chunk['type']}")
            Why did the chicken
            Event: tool_call
            cross the road?

        With full events::

            >>> chunks = []
            >>> async for chunk in engine.stream("Calculate 2+2", full_events=True):
            ...     chunks.append(chunk)
            >>>
            >>> # Analyze events
            >>> tool_events = [c for c in chunks if isinstance(c, dict) and c['type'] == 'tool_call']
            >>> print(f"Tools used: {len(tool_events)}")
            Tools used: 1
    """
    # Implementation
    ...
```

## Configuration with Complex Validation

```python
class EngineConfig(BaseModel):
    """Configuration for AgentEngine with validation.

    Example:
        >>> config = EngineConfig(
        ...     model="gpt-4",
        ...     temperature=0.5,
        ...     tools=["web_search", "calculator"],
        ...     retry_config={"max_attempts": 3, "backoff": 2.0}
        ... )
        >>>
        >>> # Validation happens automatically
        >>> try:
        ...     bad_config = EngineConfig(temperature=3.0)  # Too high
        ... except ValidationError as e:
        ...     print(e)
        temperature: ensure this value is less than or equal to 2.0
    """

    model: str = Field(
        ...,
        description="Model identifier",
        regex="^(gpt-4|gpt-3.5|claude|llama).*"
    )

    temperature: Temperature = Field(
        default=0.7,
        description="Sampling temperature for randomness"
    )

    max_tokens: Optional[TokenLimit] = Field(
        default=None,
        description="Maximum tokens to generate"
    )

    tools: List[str] = Field(
        default_factory=list,
        description="List of tool names to enable"
    )

    retry_config: Dict[str, Any] = Field(
        default_factory=lambda: {"max_attempts": 3, "backoff": 2.0},
        description="Retry configuration for transient failures"
    )

    @validator('tools')
    def validate_tools(cls, v: List[str]) -> List[str]:
        """Ensure tools are registered.

        Example:
            >>> # This will fail if 'unknown_tool' isn't registered
            >>> config = EngineConfig(tools=["unknown_tool"])
            ValidationError: Unknown tool: unknown_tool
        """
        from haive.tools import tool_registry

        unknown = [t for t in v if t not in tool_registry]
        if unknown:
            raise ValueError(f"Unknown tools: {', '.join(unknown)}")
        return v

    class Config:
        """Pydantic configuration."""
        validate_assignment = True
        extra = "forbid"

        schema_extra = {
            "example": {
                "model": "gpt-4",
                "temperature": 0.7,
                "max_tokens": 1000,
                "tools": ["web_search", "calculator"],
                "retry_config": {
                    "max_attempts": 3,
                    "backoff": 2.0
                }
            }
        }
```

## Property Documentation

```python
@property
def total_tokens_used(self) -> int:
    """Total tokens used across all executions.

    Returns:
        Cumulative token count

    Example:
        >>> engine = AgentEngine(model="gpt-4")
        >>> await engine.execute("Hello")
        >>> await engine.execute("How are you?")
        >>> print(f"Total tokens: {engine.total_tokens_used}")
        Total tokens: 156

    Note:
        Token counts are estimates for some models.
    """
    return sum(r.usage.total_tokens for r in self._execution_history)


@property
def available_tools(self) -> Dict[str, 'BaseTool']:
    """Currently available tools mapped by name.

    Returns:
        Dictionary of tool name to tool instance

    Example:
        >>> engine = AgentEngine(tools=[Calculator(), WebSearch()])
        >>> print(list(engine.available_tools.keys()))
        ['calculator', 'web_search']
        >>>
        >>> # Check if specific tool is available
        >>> if "calculator" in engine.available_tools:
        ...     calc = engine.available_tools["calculator"]
        ...     result = await calc.execute(expr="2+2")
    """
    return {tool.name: tool for tool in self._tools}


@property
def state(self) -> StateT:
    """Current agent state (type-safe).

    Returns:
        Current state instance

    Example:
        >>> class MyState(BaseState):
        ...     counter: int = 0
        ...     messages: List[str] = Field(default_factory=list)
        >>>
        >>> engine = AgentEngine(state_schema=MyState)
        >>> engine.state.counter += 1
        >>> engine.state.messages.append("Hello")
        >>>
        >>> # Type checker knows the exact types
        >>> print(f"Count: {engine.state.counter}")  # int
        >>> print(f"Messages: {len(engine.state.messages)}")  # List[str]
    """
    return self._state
```

## Best Practices Summary

1. **Always include**:
   - Brief one-line summary
   - Detailed description if needed
   - Args/Returns/Raises sections
   - At least one example
   - Type hints for all parameters

2. **Use `>>>` for doctest examples**:

   ```python
   >>> result = function(param)
   >>> print(result)
   expected_output
   ```

3. **Document complex types**:
   - Use type aliases for readability
   - Add inline comments for type parameters
   - Document TypedDict and Protocol classes

4. **Include practical examples**:
   - Show common use cases
   - Demonstrate error handling
   - Show integration with other components

5. **Cross-reference related items**:
   - Use `:class:`, `:func:`, `:mod:` for links
   - Add "See Also" sections
   - Reference guides and tutorials
