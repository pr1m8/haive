"""
Core protocols for the node system.

This module defines the fundamental interfaces that all nodes in the system
must adhere to, ensuring strong typing and consistent behavior.
"""

from typing import Any, Callable, Dict, List, Optional, Protocol, TypeVar, Union, runtime_checkable

from langgraph.types import Command, Send
from pydantic import BaseModel

from haive.core.schema.state_schema import StateSchema

# Define state types - StateSchema is our preferred state container
State = Union[StateSchema, Dict[str, Any], BaseModel]

# Define return types for nodes (StateSchema, dict, Command, Send, or list of Send)
NodeReturn = Union[State, Command, Send, List[Send]]

@runtime_checkable
class NodeProtocol(Protocol):
    """Protocol for synchronous node functions."""
    
    def __call__(self, state: State, config: Optional[Dict[str, Any]] = None) -> NodeReturn:
        """Execute the node with given state and config."""
        ...

@runtime_checkable
class AsyncNodeProtocol(Protocol):
    """Protocol for asynchronous node functions."""
    
    async def __call__(self, state: State, config: Optional[Dict[str, Any]] = None) -> NodeReturn:
        """Execute the node asynchronously."""
        ...