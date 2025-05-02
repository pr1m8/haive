"""
Specialized node decorators.

These decorators create specialized nodes for validation, retry, and interrupt
handling, based on the patterns in LangGraph documentation.
"""

import asyncio
import functools
import logging
from typing import Any, Callable, Dict, List, Optional, Tuple, Type, TypeVar, Union

from langgraph.types import Command, Send
from pydantic import BaseModel, ValidationError

from haive.core.graph.node.config import NodeConfig
from haive.core.graph.node.factory import NodeFactory
from haive.core.graph.node.protocols import State
from haive.core.schema.state_schema import StateSchema

logger = logging.getLogger(__name__)


def validation_node(
    validation_schema: Type[Union[StateSchema, BaseModel]],
    success_node: Optional[str] = None,
    failure_node: Optional[str] = None,
    name: Optional[str] = None,
    preserve_schema: bool = True,
    auto_register: bool = True,
):
    """
    Create a validation node that validates state against a schema.
    
    Args:
        validation_schema: Schema class to validate against
        success_node: Node to go to if validation succeeds
        failure_node: Node to go to if validation fails
        name: Name for the node
        preserve_schema: Whether to preserve StateSchema instances
        auto_register: Whether to automatically register the node
        
    Returns:
        A validation node function
    """
    node_name = name or f"validate_{validation_schema.__name__}"
    
    def validator_func(state: State) -> Any:
        """Validate state against schema."""
        try:
            # Convert state to validation schema instance
            if isinstance(state, validation_schema):
                # Already the right type
                validated = state
            elif isinstance(state, dict):
                # Convert dict to schema
                validated = validation_schema(**state)
            elif isinstance(state, BaseModel) or isinstance(state, StateSchema):
                # Convert from one model to another
                if hasattr(state, "model_dump"):
                    # Pydantic v2
                    state_dict = state.model_dump()
                else:
                    # Pydantic v1
                    state_dict = state.dict()
                validated = validation_schema(**state_dict)
            else:
                # Can't validate
                raise ValueError(f"Cannot convert {type(state).__name__} to {validation_schema.__name__}")
            
            # Success case - use the validated schema as the new state
            logger.debug(f"Validation succeeded for {node_name}")
            
            if success_node:
                return Command(update=validated if preserve_schema else validated.dict(), goto=success_node)
            return validated if preserve_schema else validated.dict()
            
        except ValidationError as e:
            # Validation failed
            logger.debug(f"Validation failed for {node_name}: {str(e)}")
            
            # Create error result
            error_info = {
                "validation_error": str(e),
                "error_details": e.errors() if hasattr(e, "errors") else [],
                "schema": validation_schema.__name__,
            }
            
            if isinstance(state, dict):
                # Add error to state dict
                result = state.copy()
                result["validation_error"] = error_info
            elif hasattr(state, "model_copy"):
                # Pydantic v2
                result = state.model_copy()
                try:
                    result.validation_error = error_info
                except AttributeError:
                    # No validation_error field, create a dict
                    result = {"validation_error": error_info}
            elif hasattr(state, "copy"):
                # Pydantic v1
                result = state.copy()
                try:
                    result.validation_error = error_info
                except AttributeError:
                    # No validation_error field, create a dict
                    result = {"validation_error": error_info}
            else:
                # Unknown state type
                result = {"validation_error": error_info}
            
            if failure_node:
                return Command(update=result, goto=failure_node)
            return result
            
        except Exception as e:
            # Other error
            logger.error(f"Error in validation node {node_name}: {str(e)}")
            
            # Create error result
            error_info = {
                "error": str(e),
                "schema": validation_schema.__name__,
            }
            
            if isinstance(state, dict):
                # Add error to state dict
                result = state.copy()
                result["error"] = error_info
            elif hasattr(state, "model_copy") or hasattr(state, "copy"):
                # Just return error dict
                result = {"error": error_info}
            else:
                # Unknown state type
                result = {"error": error_info}
            
            if failure_node:
                return Command(update=result, goto=failure_node)
            return result
    
    # Create node config
    config = NodeConfig(
        name=node_name,
        engine=validator_func,
        preserve_schema=preserve_schema,
    )
    
    # Create node function
    node_func = NodeFactory.create_node(config)
    
    # Auto-register if requested
    if auto_register:
        registry = NodeFactory.get_registry()
        registry.register_node(node_name, node_func)
    
    # Add metadata for introspection
    node_func.__validation_schema__ = validation_schema
    node_func.__node_config__ = config
    
    return node_func


def retry_node(
    max_attempts: int = 3,
    initial_delay: float = 0.5,
    backoff_factor: float = 2.0,
    max_delay: float = 10.0,
    jitter: bool = True,
    failure_node: Optional[str] = None,
    name: Optional[str] = None,
    preserve_schema: bool = True,
    auto_register: bool = True,
):
    """
    Create a retry node decorator.
    
    This decorator adds retry capabilities to a node function based on
    the patterns in langgraph-retry.md.
    
    Args:
        max_attempts: Maximum number of retry attempts
        initial_delay: Initial delay before first retry (seconds)
        backoff_factor: Factor to increase delay by on each attempt
        max_delay: Maximum delay between retries (seconds)
        jitter: Whether to add random jitter to delays
        failure_node: Node to go to if all retries fail
        name: Name for the node
        preserve_schema: Whether to preserve StateSchema instances
        auto_register: Whether to automatically register the node
        
    Returns:
        A decorator that adds retry capabilities to a node
    """
    def decorator(func: Callable) -> Callable:
        """Decorator implementation."""
        # Use provided name or generate from function
        node_name = name or f"retry_{func.__name__}"
        
        # Create retry wrapper function
        def retry_wrapper(state: State) -> Any:
            """Execute function with retry logic."""
            # Get or initialize retry count
            retry_count = 0
            
            if isinstance(state, dict) and "retry_count" in state:
                retry_count = state["retry_count"]
            elif hasattr(state, "retry_count"):
                retry_count = getattr(state, "retry_count", 0)
            
            try:
                # Try to execute the function
                result = func(state)
                
                # If successful, reset retry count and return result
                if isinstance(result, dict):
                    if "retry_count" in result:
                        del result["retry_count"]
                elif hasattr(result, "retry_count") and hasattr(result, "model_copy"):
                    # Pydantic v2
                    result = result.model_copy()
                    result.retry_count = 0
                elif hasattr(result, "retry_count") and hasattr(result, "copy"):
                    # Pydantic v1
                    result = result.copy()
                    result.retry_count = 0
                
                return result
                
            except Exception as e:
                logger.warning(f"Error in {node_name}: {str(e)}, attempt {retry_count + 1}/{max_attempts}")
                
                # Increment retry count
                retry_count += 1
                
                if retry_count < max_attempts:
                    # Calculate delay with exponential backoff
                    delay = min(initial_delay * (backoff_factor ** (retry_count - 1)), max_delay)
                    
                    # Add jitter if enabled (±10%)
                    if jitter:
                        import random
                        jitter_factor = 1.0 + random.uniform(-0.1, 0.1)
                        delay *= jitter_factor
                    
                    # Sleep for the calculated delay
                    logger.debug(f"Sleeping for {delay:.2f}s before retry {retry_count}")
                    import time
                    time.sleep(delay)
                    
                    # Update retry count in state
                    if isinstance(state, dict):
                        updated_state = state.copy()
                        updated_state["retry_count"] = retry_count
                    elif hasattr(state, "model_copy"):
                        # Pydantic v2
                        updated_state = state.model_copy()
                        updated_state.retry_count = retry_count
                    elif hasattr(state, "copy"):
                        # Pydantic v1
                        updated_state = state.copy()
                        updated_state.retry_count = retry_count
                    else:
                        # Unknown state type
                        updated_state = {"retry_count": retry_count}
                    
                    # Try again with updated state (recursively)
                    return retry_wrapper(updated_state)
                else:
                    # Max retries exceeded, handle failure
                    logger.error(f"Max retries ({max_attempts}) exceeded for {node_name}")
                    
                    # Create error result
                    error_info = {
                        "error": str(e),
                        "retry_count": retry_count,
                        "max_attempts": max_attempts,
                    }
                    
                    if isinstance(state, dict):
                        # Add error to state dict
                        result = state.copy()
                        result["error"] = error_info
                    elif hasattr(state, "model_copy"):
                        # Pydantic v2
                        result = state.model_copy()
                        try:
                            result.error = error_info
                        except AttributeError:
                            # No error field, create a dict
                            result = {"error": error_info}
                    elif hasattr(state, "copy"):
                        # Pydantic v1
                        result = state.copy()
                        try:
                            result.error = error_info
                        except AttributeError:
                            # No error field, create a dict
                            result = {"error": error_info}
                    else:
                        # Unknown state type
                        result = {"error": error_info}
                    
                    if failure_node:
                        return Command(update=result, goto=failure_node)
                    return result
        
        # Create node config
        config = NodeConfig(
            name=node_name,
            engine=retry_wrapper,
            preserve_schema=preserve_schema,
        )
        
        # Create node function
        node_func = NodeFactory.create_node(config)
        
        # Auto-register if requested
        if auto_register:
            registry = NodeFactory.get_registry()
            registry.register_node(node_name, node_func)
        
        # Add metadata for introspection
        node_func.__original_func__ = func
        node_func.__retry_config__ = {
            "max_attempts": max_attempts,
            "initial_delay": initial_delay,
            "backoff_factor": backoff_factor,
            "max_delay": max_delay,
            "jitter": jitter,
        }
        node_func.__node_config__ = config
        
        return node_func
    
    return decorator


def interruptible_node(
    resume_node: Optional[str] = None,
    name: Optional[str] = None,
    preserve_schema: bool = True,
    auto_register: bool = True,
):
    """
    Create an interruptible node decorator.
    
    This decorator adds interrupt capabilities to a node function based on
    the patterns in langgraph-branching-interrupts.md.
    
    Args:
        resume_node: Node to go to when resuming from interrupt
        name: Name for the node
        preserve_schema: Whether to preserve StateSchema instances
        auto_register: Whether to automatically register the node
        
    Returns:
        A decorator that adds interrupt capabilities to a node
    """
    def decorator(func: Callable) -> Callable:
        """Decorator implementation."""
        # Use provided name or generate from function
        node_name = name or f"interruptible_{func.__name__}"
        
        def interrupt_wrapper(state: State) -> Any:
            """Execute function with interrupt handling."""
            # Check if we're resuming from an interrupt
            is_resuming = False
            resume_payload = None
            
            if isinstance(state, dict) and "interrupt_resume" in state:
                is_resuming = True
                resume_payload = state["interrupt_resume"]
            elif hasattr(state, "interrupt_resume"):
                is_resuming = True
                resume_payload = getattr(state, "interrupt_resume")
            
            try:
                if is_resuming:
                    logger.debug(f"Resuming {node_name} with payload")
                    
                    # Clear resume flag from state
                    if isinstance(state, dict):
                        state_copy = state.copy()
                        state_copy.pop("interrupt_resume", None)
                        state_copy.pop("interrupt_status", None)
                    elif hasattr(state, "model_copy"):
                        # Pydantic v2
                        state_copy = state.model_copy()
                        state_copy.interrupt_resume = None
                        state_copy.interrupt_status = None
                    elif hasattr(state, "copy"):
                        # Pydantic v1
                        state_copy = state.copy()
                        state_copy.interrupt_resume = None
                        state_copy.interrupt_status = None
                    else:
                        # Unknown state type, just pass through
                        state_copy = state
                    
                    # Add resume payload to state
                    if isinstance(state_copy, dict):
                        state_copy["resume_payload"] = resume_payload
                    elif hasattr(state_copy, "resume_payload"):
                        state_copy.resume_payload = resume_payload
                    
                    # Execute with resume handling
                    return func(state_copy)
                else:
                    # Normal execution
                    return func(state)
                    
            except NodeInterrupt as interrupt:
                logger.info(f"Node {node_name} interrupted")
                
                # Store interrupt state
                interrupt_info = {
                    "interrupt_status": "interrupted",
                    "interrupt_message": interrupt.message,
                    "interrupt_payload": interrupt.payload,
                    "interrupt_timestamp": interrupt.timestamp,
                }
                
                if isinstance(state, dict):
                    # Add interrupt info to state dict
                    result = state.copy()
                    result.update(interrupt_info)
                elif hasattr(state, "model_copy"):
                    # Pydantic v2
                    result = state.model_copy()
                    for key, value in interrupt_info.items():
                        setattr(result, key, value)
                elif hasattr(state, "copy"):
                    # Pydantic v1
                    result = state.copy()
                    for key, value in interrupt_info.items():
                        setattr(result, key, value)
                else:
                    # Unknown state type
                    result = interrupt_info
                
                # Return interrupt info
                if resume_node:
                    # We'll come back to the resume node later
                    return Command(update=result, goto=resume_node)
                return result
                
            except Exception as e:
                logger.error(f"Error in {node_name}: {str(e)}")
                
                # Create error result
                error_info = {
                    "error": str(e),
                    "node": node_name,
                }
                
                if isinstance(state, dict):
                    # Add error to state dict
                    result = state.copy()
                    result["error"] = error_info
                elif hasattr(state, "model_copy") or hasattr(state, "copy"):
                    # Just return error dict to avoid model errors
                    result = {"error": error_info}
                else:
                    # Unknown state type
                    result = {"error": error_info}
                
                return result
        
        # Create node config
        config = NodeConfig(
            name=node_name,
            engine=interrupt_wrapper,
            preserve_schema=preserve_schema,
        )
        
        # Create node function
        node_func = NodeFactory.create_node(config)
        
        # Auto-register if requested
        if auto_register:
            registry = NodeFactory.get_registry()
            registry.register_node(node_name, node_func)
        
        # Add metadata for introspection
        node_func.__original_func__ = func
        node_func.__interrupt_config__ = {
            "resume_node": resume_node,
        }
        node_func.__node_config__ = config
        
        return node_func
    
    return decorator


class NodeInterrupt(Exception):
    """
    Exception raised to interrupt a node's execution.
    
    This is used to implement interrupt handling as described in
    langgraph-branching-interrupts.md.
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
    the interruptible_node decorator.
    
    Args:
        payload: Data to be passed to the resumption handler
        message: Human-readable interrupt message
        
    Raises:
        NodeInterrupt: Always raised to signal interruption
    """
    raise NodeInterrupt(payload, message)