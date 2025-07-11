"""
Core types for the Haive graph system.

This module defines fundamental types, protocols, and enums used throughout
the graph system, providing a strong typing foundation for graph components.

The system is built on several key concepts:
1. Protocols: Define structural interfaces (like NamedEntity)
2. Type aliases: Simplify complex type combinations
3. Enums: Define constants for node/edge types and states
4. Policies: Define configuration objects like RetryPolicy

These types ensure consistency and type safety across the system while
enabling IDE auto-completion and static type checking.
"""

from enum import Enum
from typing import (
    Any,
    Callable,
    Dict,
    List,
    Literal,
    Optional,
    Protocol,
    Type,
    TypeVar,
    Union,
    runtime_checkable,
)

from langchain_core.runnables import RunnableConfig
from langchain_core.tools import BaseTool, StructuredTool, Tool
from langgraph.types import Command, Send
from pydantic import BaseModel, Field

from haive.core.schema.state_schema import StateSchema

# State type
StateType = Union[StateSchema, Dict[str, Any]]
ConfigType = Optional[Union[RunnableConfig, Dict[str, Any]]]
NodeReturnType = Union[Dict[str, Any], Command, Send, List[Send], str, bool, Any]
CommandGoto = Union[str, Literal["END"], Send, List[Union[Send, str]]]

# Tool type
ToolType = Union[BaseTool, BaseModel, StructuredTool, Tool]
ToolsType = Union[List[ToolType], List[List[ToolType]]]

# Node callable signature
NodeCallable = Callable[[StateType, Optional[ConfigType]], NodeReturnType]

# Branch condition function signatures
BranchStringConditionFunc = Callable[[StateType, Optional[ConfigType]], str]
BranchBoolConditionFunc = Callable[[StateType, Optional[ConfigType]], bool]
BranchDictConditionFunc = Callable[[StateType, Optional[ConfigType]], Dict[str, Any]]
BranchSendConditionFunc = Callable[
    [StateType, Optional[ConfigType]], Union[Send, List[Send]]
]
BranchCommandConditionFunc = Callable[[StateType, Optional[ConfigType]], Command]

# Combined branch function type
BranchConditionFunc = Union[
    BranchStringConditionFunc,
    BranchBoolConditionFunc,
    BranchDictConditionFunc,
    BranchSendConditionFunc,
    BranchCommandConditionFunc,
]


# Protocol for named entities
@runtime_checkable
class NamedEntity(Protocol):
    """
    Protocol that requires a name property.

    Any object implementing this protocol must have a name property
    that returns a string. This allows for consistent naming across
    different entity types in the graph system.
    """

    @property
    def name(self) -> str: ...


# Type variable for nodes, bounded by NamedEntity
N = TypeVar("N", bound=NamedEntity)


# Edge types
class EdgeType(str, Enum):
    """
    Types of edges in the graph.

    Attributes:
        DIRECT: Simple direct edge from one node to another
        CONDITIONAL: Edge with conditional routing based on state
        WAITING: Edge that waits for a condition to be satisfied
    """

    DIRECT = "direct"
    CONDITIONAL = "conditional"
    WAITING = "waiting"


# Edge states
class EdgeState(str, Enum):
    """
    States for edges with waiting conditions.

    Attributes:
        INACTIVE: Edge has not started waiting
        WAITING: Edge is currently waiting for condition
        ACTIVE: Edge condition is satisfied, ready to traverse
        COMPLETED: Edge has been traversed successfully
        FAILED: Edge waiting failed (e.g., timeout)
    """

    INACTIVE = "inactive"
    WAITING = "waiting"
    ACTIVE = "active"
    COMPLETED = "completed"
    FAILED = "failed"


# Node types
class NodeType(str, Enum):
    """
    Types of nodes in the graph.

    Attributes:
        FUNCTION: Node containing a simple callable function
        ENGINE: Node containing an engine (includes agent subgraphs)
        TOOL: Node containing a tool or collection of tools
    """

    FUNCTION = "function"
    ENGINE = "engine"  # Includes both regular engines and subgraphs (agent engines)
    TOOL = "tool"


# Retry policy for node execution
class RetryPolicy(BaseModel):
    """
    Policy for retrying node execution on failure.

    This model defines how and when to retry a failed node execution,
    including backoff strategy and exception filtering.

    Attributes:
        max_attempts: Maximum number of retry attempts
        backoff_factor: Multiplier for successive retry delays
        initial_delay: Initial delay before first retry (seconds)
        max_delay: Maximum delay between retries (seconds)
        retry_on: List of exception types to retry on
        jitter: Whether to add random jitter to delays

    Example:
        ```python
        # Retry up to 3 times with exponential backoff
        retry_policy = RetryPolicy(
            max_attempts=3,
            backoff_factor=2.0,
            initial_delay=1.0,
            retry_on=[ConnectionError, TimeoutError]
        )
        ```
    """

    max_attempts: int = Field(
        default=3,
        ge=1,
        description="Maximum number of retry attempts (including initial attempt)",
    )
    backoff_factor: float = Field(
        default=2.0, gt=0, description="Multiplier for successive retry delays"
    )
    initial_delay: float = Field(
        default=1.0, ge=0, description="Initial delay before first retry (seconds)"
    )
    max_delay: Optional[float] = Field(
        default=None, description="Maximum delay between retries (seconds)"
    )
    retry_on: List[Union[Type[Exception], str]] = Field(
        default_factory=list, description="Exception types or names to retry on"
    )
    jitter: bool = Field(
        default=True, description="Whether to add random jitter to delays"
    )

    def should_retry(self, exception: Exception, attempt: int) -> bool:
        """
        Determine if an exception should trigger a retry.

        Args:
            exception: The exception that occurred
            attempt: Current attempt number (1-based)

        Returns:
            True if should retry, False otherwise
        """
        # Check attempt count
        if attempt >= self.max_attempts:
            return False

        # If no specific exceptions are specified, retry on any exception
        if not self.retry_on:
            return True

        # Check if exception matches any in retry_on
        for exc_type in self.retry_on:
            if isinstance(exc_type, str):
                # Match by name
                if exception.__class__.__name__ == exc_type:
                    return True
            elif isinstance(exception, exc_type):
                # Match by type
                return True

        return False

    def get_delay(self, attempt: int) -> float:
        """
        Calculate the delay for a retry attempt.

        Args:
            attempt: Current attempt number (1-based)

        Returns:
            Delay in seconds
        """
        import random

        # Calculate base delay with exponential backoff
        delay = self.initial_delay * (self.backoff_factor ** (attempt - 1))

        # Apply max delay if specified
        if self.max_delay is not None:
            delay = min(delay, self.max_delay)

        # Apply jitter if enabled
        if self.jitter:
            # Add up to 10% random jitter
            jitter_factor = 1.0 + random.uniform(-0.1, 0.1)
            delay *= jitter_factor

        return delay
