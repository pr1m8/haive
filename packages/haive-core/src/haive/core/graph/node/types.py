# src/haive/core/graph/node/types.py
"""
Core types and protocols for the node system.

This module defines the fundamental types, protocols, and enums used
throughout the node system, providing type safety and standardization.
"""


# src/haive/core/graph/node/types.py
from enum import Enum
from typing import (
    Any,
    Dict,
    List,
    Literal,
    Optional,
    Protocol,
    TypeVar,
    Union,
    runtime_checkable,
)

from langchain_core.runnables import RunnableConfig
from langgraph.types import Command, Send
from pydantic import BaseModel

# Type variables for better type safety
StateInput = TypeVar("StateInput", bound=Union[BaseModel, Dict[str, Any], Any])
StateOutput = TypeVar(
    "StateOutput", bound=Union[Dict[str, Any], Command, Send, List[Send], Any]
)
ConfigType = Union[RunnableConfig, Dict[str, Any], None]


class NodeType(str, Enum):
    """Types of nodes in the graph."""

    ENGINE = "engine"  # Nodes created from engines
    CALLABLE = "callable"  # Nodes created from callable functions
    TOOL = "tool"  # Tool nodes for handling tool calls
    VALIDATION = "validation"  # Validation nodes for schema validation
    # BRANCH = "branch"  # Branch nodes for conditional routing
    AGENT = "agent"  # Agent nodes for agent-specific behavior

    # Message handling nodes
    MESSAGE_TRANSFORMER = "message_transformer"
    # SEND = "send"  # Send nodes for dynamic routing
    CUSTOM = "custom"  # Custom node types
    PARSER = "parser"  # Parser nodes for parsing tool results


# Command destination types for better type checking
CommandGoto = Union[str, Literal["END"], Send, List[Union[Send, str]]]


@runtime_checkable
class NodeFunction(Protocol[StateInput, StateOutput]):
    """
    Protocol for node functions.

    A node function takes a state and optional config and returns an output.
    This output can be a dictionary (state update), Command, Send, or list of Send objects.
    """

    def __call__(
        self, state: StateInput, config: Optional[ConfigType] = None
    ) -> StateOutput:
        """Execute the node with the given state and configuration."""
        ...


@runtime_checkable
class AsyncNodeFunction(Protocol[StateInput, StateOutput]):
    """
    Protocol for async node functions.

    An async node function is like a regular node function but executes asynchronously.
    """

    async def __call__(
        self, state: StateInput, config: Optional[ConfigType] = None
    ) -> StateOutput:
        """Execute the node asynchronously."""
        ...
