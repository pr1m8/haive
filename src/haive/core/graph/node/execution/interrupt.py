"""
Interrupt handling implementation.

This module provides utilities for handling interrupts in node execution,
based on the patterns in langgraph-branching-interrupts.md.
"""

import asyncio
import logging
from typing import Any, Callable, Dict, List, Optional, TypeVar, Union

from langgraph.types import Command
from pydantic import BaseModel

from haive.core.graph.node.protocols import State
from haive.core.schema.state_schema import StateSchema

logger = logging.getLogger(__name__)


class InterruptData(BaseModel):
    """Data structure for interrupt information."""
    
    status: str = "interrupted"
    message: str = "Node execution interrupted"
    payload: Optional[Any] = None
    timestamp: float = 0.0
    node_id: Optional[str] = None


class NodeInterrupt(Exception):
    """
    Exception raised to interrupt a node's execution.
    
    This is used to implement the interrupt handling pattern in LangGraph.
    """
    
    def __init__(
        self, 
        payload: Any = None, 
        message: str = "Node execution interrupted"
    ):
        """
        Initialize a node interrupt.
        
        Args:
            payload: Data to be passed to the resumption handler
            message: Human-readable interrupt message
        """
        self.payload = payload
        self.message = message
        self.timestamp = asyncio.get_event_loop().time() if asyncio.get_event_loop_policy().get_event_loop().is_running() else 0.0
        super().__init__(message)


def interrupt(payload: Any = None, message: str = "Node execution interrupted") -> None:
    """
    Interrupt the current node execution.
    
    This function raises a NodeInterrupt exception which will be caught by
    an interruptible node wrapper.
    
    Args:
        payload: Data to be passed to the resumption handler
        message: Human-readable interrupt message
        
    Raises:
        NodeInterrupt: Always raised to signal interruption
    """
    raise NodeInterrupt(payload, message)


def is_interrupted(state: State) -> bool:
    """
    Check if the state contains an interrupt.
    
    Args:
        state: Current state
        
    Returns:
        True if the state contains an interrupt, False otherwise
    """
    if isinstance(state, dict) and "interrupt_status" in state:
        return state["interrupt_status"] == "interrupted"
    elif hasattr(state, "interrupt_status"):
        return getattr(state, "interrupt_status") == "interrupted"
    return False


def get_interrupt_data(state: State) -> Optional[InterruptData]:
    """
    Get interrupt data from state.
    
    Args:
        state: Current state
        
    Returns:
        InterruptData if the state contains an interrupt, None otherwise
    """
    if not is_interrupted(state):
        return None
    
    if isinstance(state, dict):
        return InterruptData(
            status=state.get("interrupt_status", "interrupted"),
            message=state.get("interrupt_message", "Node execution interrupted"),
            payload=state.get("interrupt_payload"),
            timestamp=state.get("interrupt_timestamp", 0.0),
            node_id=state.get("interrupt_node_id"),
        )
    elif isinstance(state, (BaseModel, StateSchema)):
        return InterruptData(
            status=getattr(state, "interrupt_status", "interrupted"),
            message=getattr(state, "interrupt_message", "Node execution interrupted"),
            payload=getattr(state, "interrupt_payload", None),
            timestamp=getattr(state, "interrupt_timestamp", 0.0),
            node_id=getattr(state, "interrupt_node_id", None),
        )
    
    return None


def create_resume_command(
    state: State,
    resume_data: Any = None,
    resume_node: Optional[str] = None,
    clear_interrupt: bool = True,
) -> Command:
    """
    Create a Command to resume execution after an interrupt.
    
    Args:
        state: Current state
        resume_data: Data to pass to the resumed node
        resume_node: Node to resume execution at
        clear_interrupt: Whether to clear interrupt data from state
        
    Returns:
        Command object for resumption
    """
    # Get interrupt data
    interrupt_data = get_interrupt_data(state)
    if not interrupt_data and not resume_node:
        raise ValueError("No interrupt found in state and no resume_node provided")
    
    # Determine resume node
    target_node = resume_node or getattr(interrupt_data, "node_id", None)
    if not target_node:
        raise ValueError("No resume node specified or found in interrupt data")
    
    # Prepare updated state
    if isinstance(state, dict):
        updated_state = state.copy()
        
        # Add resume data
        updated_state["resume_data"] = resume_data
        
        # Clear interrupt data if requested
        if clear_interrupt:
            updated_state.pop("interrupt_status", None)
            updated_state.pop("interrupt_message", None)
            updated_state.pop("interrupt_payload", None)
            updated_state.pop("interrupt_timestamp", None)
            updated_state.pop("interrupt_node_id", None)
    
    elif isinstance(state, BaseModel) and hasattr(state, "model_copy"):
        # Pydantic v2
        updated_state = state.model_copy()
        
        # Add resume data
        if hasattr(updated_state, "resume_data"):
            updated_state.resume_data = resume_data
        
        # Clear interrupt data if requested
        if clear_interrupt:
            if hasattr(updated_state, "interrupt_status"):
                updated_state.interrupt_status = None
            if hasattr(updated_state, "interrupt_message"):
                updated_state.interrupt_message = None
            if hasattr(updated_state, "interrupt_payload"):
                updated_state.interrupt_payload = None
            if hasattr(updated_state, "interrupt_timestamp"):
                updated_state.interrupt_timestamp = None
            if hasattr(updated_state, "interrupt_node_id"):
                updated_state.interrupt_node_id = None
    
    elif isinstance(state, BaseModel) and hasattr(state, "copy"):
        # Pydantic v1
        updated_state = state.copy()
        
        # Add resume data
        if hasattr(updated_state, "resume_data"):
            updated_state.resume_data = resume_data
        
        # Clear interrupt data if requested
        if clear_interrupt:
            if hasattr(updated_state, "interrupt_status"):
                updated_state.interrupt_status = None
            if hasattr(updated_state, "interrupt_message"):
                updated_state.interrupt_message = None
            if hasattr(updated_state, "interrupt_payload"):
                updated_state.interrupt_payload = None
            if hasattr(updated_state, "interrupt_timestamp"):
                updated_state.interrupt_timestamp = None
            if hasattr(updated_state, "interrupt_node_id"):
                updated_state.interrupt_node_id = None
    
    else:
        # Unknown state type, create dict with resume data
        updated_state = {
            "resume_data": resume_data,
        }
    
    # Create Command to resume execution
    return Command(update=updated_state, goto=target_node)