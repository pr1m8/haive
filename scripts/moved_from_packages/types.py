"""Type definitions for the state graph system.

This module contains type definitions and constants used throughout
the state graph system.
"""

import enum
from collections.abc import Callable
from typing import Any, TypeVar, Union

from langgraph.graph import END, START  # Import the actual constants
from langgraph.types import Command, Send

# Define type variables for generic parameters
StateLike = TypeVar("StateLike")
ConfigLike = TypeVar("ConfigLike")
NodeOutput = TypeVar("NodeOutput")


class EdgeType(str, enum.Enum):
    """Types of edges in a graph."""

    DIRECT = "direct"  # Simple direct connection
    CONDITIONAL = "conditional"  # Edge with condition
    DYNAMIC = "dynamic"  # Created dynamically at runtime


class BranchType(str, enum.Enum):
    """Types of branches for conditional routing."""

    FUNCTION = "function"  # Uses a callable function
    KEY_VALUE = "key_value"  # Compares a state key with a value
    SEND = "send"  # Uses Send objects for routing
    COMMAND = "command"  # Uses Command objects for routing


# Simple edge: (source_node_name, target_node_name)
SimpleEdge = tuple[str, str]

# Complete edge type - now just simple edges
Edge = SimpleEdge

# Define a type for branch result types
BranchResultType = Union[
    str,  # Node name
    bool,  # Boolean condition
    list[str],  # List of node names
    list[Send],  # List of Send objects
    Send,  # Single Send object
    Command,  # Command object
    None,  # Default case
]

# Type for node functions
NodeFunc = Callable[[Any, dict[str, Any] | None], Any]

# Constants
GRAPH_CONSTANTS = {
    "START": START,
    "END": END,
}
