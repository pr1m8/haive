"""
Retry policy implementation.

This module provides utilities for implementing retry policies as described
in langgraph-retry.md.
"""

import logging
import random
import time
from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional, Type, TypeVar, Union

from langgraph.types import Command
from pydantic import BaseModel

from haive.core.graph.node.protocols import State
from haive.core.schema.state_schema import StateSchema

logger = logging.getLogger(__name__)


@dataclass
class RetryPolicy:
    """
    Retry policy configuration.
    
    Based on the RetryPolicy from langgraph-retry.md.
    """
    
    initial_interval: float = 0.5
    backoff_factor: float = 2.0
    max_interval: float = 128.0
    max_attempts: int = 3
    jitter: bool = True
    retry_exceptions: List[Type[Exception]] = None
    
    def __post_init__(self):
        """Initialize default retry_exceptions."""
        if self.retry_exceptions is None:
            self.retry_exceptions = [Exception]
    
    def should_retry(self, exception: Exception) -> bool:
        """
        Check if retry should be attempted for this exception.
        
        Args:
            exception: The exception that occurred
            
        Returns:
            True if retry should be attempted, False otherwise
        """
        return any(isinstance(exception, exc_type) for exc_type in self.retry_exceptions)
    
    def get_delay(self, attempt: int) -> float:
        """
        Calculate delay for a retry attempt.
        
        Args:
            attempt: Retry attempt number (1-based)
            
        Returns:
            Delay in seconds
        """
        delay = min(
            self.initial_interval * (self.backoff_factor ** (attempt - 1)),
            self.max_interval
        )
        
        if self.jitter:
            # Add jitter (±10%)
            jitter_factor = 1.0 + random.uniform(-0.1, 0.1)
            delay *= jitter_factor
        
        return delay


class RetryState:
    """Helper for managing retry state."""
    
    @staticmethod
    def get_retry_count(state: State) -> int:
        """
        Get retry count from state.
        
        Args:
            state: Current state
            
        Returns:
            Current retry count
        """
        if isinstance(state, dict) and "retry_count" in state:
            return state["retry_count"]
        elif hasattr(state, "retry_count"):
            return getattr(state, "retry_count", 0)
        return 0
    
    @staticmethod
    def update_retry_count(state: State, retry_count: int) -> State:
        """
        Update retry count in state.
        
        Args:
            state: Current state
            retry_count: New retry count
            
        Returns:
            Updated state
        """
        if isinstance(state, dict):
            updated_state = state.copy()
            updated_state["retry_count"] = retry_count
            return updated_state
        elif isinstance(state, BaseModel) and hasattr(state, "model_copy"):
            # Pydantic v2
            updated_state = state.model_copy()
            updated_state.retry_count = retry_count
            return updated_state
        elif isinstance(state, BaseModel) and hasattr(state, "copy"):
            # Pydantic v1
            updated_state = state.copy()
            updated_state.retry_count = retry_count
            return updated_state
        else:
            # Unknown state type
            return {"retry_count": retry_count}
    
    @staticmethod
    def add_error(state: State, error: Exception) -> State:
        """
        Add error information to state.
        
        Args:
            state: Current state
            error: The exception that occurred
            
        Returns:
            Updated state
        """
        error_info = {
            "error": str(error),
            "error_type": type(error).__name__,
        }
        
        if isinstance(state, dict):
            updated_state = state.copy()
            updated_state["error"] = error_info
            return updated_state
        elif isinstance(state, BaseModel) and hasattr(state, "model_copy"):
            # Pydantic v2
            # Just return error dict to avoid model errors
            return {"error": error_info}
        elif isinstance(state, BaseModel) and hasattr(state, "copy"):
            # Pydantic v1
            # Just return error dict to avoid model errors
            return {"error": error_info}
        else:
            # Unknown state type
            return {"error": error_info}


def with_retry(
    func: Callable,
    policy: RetryPolicy = None,
    failure_node: Optional[str] = None,
) -> Callable:
    """
    Wrap a function with retry logic.
    
    Args:
        func: Function to wrap
        policy: Retry policy to use
        failure_node: Node to go to if all retries fail
        
    Returns:
        Wrapped function with retry logic
    """
    # Use default policy if none provided
    if policy is None:
        policy = RetryPolicy()
    
    def retry_wrapper(state: State) -> Any:
        """Execute function with retry logic."""
        # Get current retry count
        retry_count = RetryState.get_retry_count(state)
        
        try:
            # Try to execute the function
            result = func(state)
            
            # If successful, reset retry count
            if retry_count > 0:
                if isinstance(result, dict):
                    result.pop("retry_count", None)
                elif hasattr(result, "retry_count") and (
                    hasattr(result, "model_copy") or hasattr(result, "copy")
                ):
                    # Set to 0 instead of removing to avoid schema errors
                    if hasattr(result, "model_copy"):
                        result = result.model_copy()
                    else:
                        result = result.copy()
                    result.retry_count = 0
            
            return result
            
        except Exception as e:
            logger.warning(f"Error in {func.__name__}: {str(e)}, attempt {retry_count + 1}/{policy.max_attempts}")
            
            # Check if we should retry this exception
            if not policy.should_retry(e):
                logger.info(f"Not retrying exception type: {type(e).__name__}")
                
                # Add error to state
                error_state = RetryState.add_error(state, e)
                
                # Route to failure node if specified
                if failure_node:
                    return Command(update=error_state, goto=failure_node)
                return error_state
            
            # Increment retry count
            retry_count += 1
            
            if retry_count < policy.max_attempts:
                # Calculate delay
                delay = policy.get_delay(retry_count)
                
                # Sleep for the calculated delay
                logger.debug(f"Sleeping for {delay:.2f}s before retry {retry_count}")
                time.sleep(delay)
                
                # Update retry count in state
                updated_state = RetryState.update_retry_count(state, retry_count)
                
                # Try again with updated state (recursively)
                return retry_wrapper(updated_state)
            else:
                # Max retries exceeded
                logger.error(f"Max retries ({policy.max_attempts}) exceeded for {func.__name__}")
                
                # Add error to state
                error_state = RetryState.add_error(state, e)
                
                # Route to failure node if specified
                if failure_node:
                    return Command(update=error_state, goto=failure_node)
                return error_state
    
    # Add metadata to the wrapper function
    retry_wrapper.__name__ = f"retry_{func.__name__}"
    retry_wrapper.__wrapped__ = func
    retry_wrapper.__retry_policy__ = policy
    
    return retry_wrapper


def create_retry_policy(
    initial_interval: float = 0.5,
    backoff_factor: float = 2.0,
    max_interval: float = 128.0,
    max_attempts: int = 3,
    jitter: bool = True,
    retry_exceptions: List[Type[Exception]] = None,
) -> RetryPolicy:
    """
    Create a retry policy.
    
    Args:
        initial_interval: Initial delay before first retry (seconds)
        backoff_factor: Factor to increase delay by on each attempt
        max_interval: Maximum delay between retries (seconds)
        max_attempts: Maximum number of retry attempts
        jitter: Whether to add random jitter to delays
        retry_exceptions: List of exception types to retry on
        
    Returns:
        RetryPolicy instance
    """
    return RetryPolicy(
        initial_interval=initial_interval,
        backoff_factor=backoff_factor,
        max_interval=max_interval,
        max_attempts=max_attempts,
        jitter=jitter,
        retry_exceptions=retry_exceptions,
    )