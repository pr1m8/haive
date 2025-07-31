"""Callable Node - Wrap any callable as a graph node.

from typing import Any
This module provides a way to wrap any Python callable (function, method, lambda)
as a proper graph node that returns Command or Send objects.
"""

import inspect
import logging
from collections.abc import Callable
from typing import Any, Self, TypeVar

from langgraph.types import Command
from pydantic import BaseModel, Field, model_validator

from haive.core.graph.common.types import ConfigLike, NodeType, StateLike
from haive.core.graph.node.base_node_config import BaseNodeConfig
from haive.core.schema.field_definition import FieldDefinition

logger = logging.getLogger(__name__)

# Type for the wrapped callable
TCallable = TypeVar("TCallable", bound=Callable)
TState = TypeVar("TState", bound=BaseModel)


class CallableNodeConfig(BaseNodeConfig):
    """Configuration for wrapping a callable as a node.

    This allows any function to be used as a graph node by:
    1. Extracting required parameters from state
    2. Calling the function
    3. Wrapping the result in Command/Send

    Examples:
        Simple boolean check::

            def check_threshold(messages: List[BaseMessage], threshold: int = 100) -> bool:
                total_length = sum(len(msg.content) for msg in messages)
                return total_length > threshold

            node = CallableNodeConfig(
                name="check_threshold",
                callable_func=check_threshold,
                goto_on_true="summarize",
                goto_on_false="continue"
            )

        State function::

            def needs_summarization(state: MessagesState) -> bool:
                return state.token_count > 1000

            node = CallableNodeConfig(
                name="check_summary",
                callable_func=needs_summarization,
                extract_full_state=True
            )
    """

    node_type: NodeType = Field(default=NodeType.CALLABLE)

    # The callable to wrap
    callable_func: Callable = Field(..., description="The function to wrap as a node")

    # How to handle the result
    result_key: str | None = Field(
        default=None,
        description="State key to store result in. If None, result is not stored.",
    )

    # Routing based on boolean results
    goto_on_true: str | None = Field(
        default=None, description="Node to go to if callable returns True"
    )

    goto_on_false: str | None = Field(
        default=None, description="Node to go to if callable returns False"
    )

    # For non-boolean results
    goto_mapping: dict[Any, str] | None = Field(
        default=None, description="Map function results to node names"
    )

    # Default goto if no mapping matches
    default_goto: str | None = Field(
        default=None, description="Default node if no mapping matches"
    )

    # State extraction options
    extract_full_state: bool = Field(
        default=False, description="Pass the full state object as first parameter"
    )

    parameter_mapping: dict[str, str] | None = Field(
        default=None,
        description="Map function parameters to state fields. {'param': 'state.field'}",
    )

    # For complex extraction
    extraction_paths: dict[str, str] | None = Field(
        default=None,
        description="Advanced extraction paths like 'param': 'state.nested.field[0].value'",
    )

    # Error handling
    on_error: str = Field(
        default="raise",
        description="What to do on error: 'raise', 'return_none', 'goto_error'",
    )

    error_goto: str | None = Field(
        default=None, description="Node to go to on error (if on_error='goto_error')"
    )

    @model_validator(mode="after")
    def validate_config(self) -> Self:
        """Validate the configuration."""
        # Check that we have some way to route
        if not any(
            [
                self.goto_on_true,
                self.goto_on_false,
                self.goto_mapping,
                self.default_goto,
                self.command_goto,
            ]
        ):
            raise ValueError(
                "Must specify at least one of: goto_on_true/false, goto_mapping, "
                "default_goto, or command_goto"
            )

        return self

    def get_default_input_fields(self) -> list[FieldDefinition]:
        """Get input fields based on callable signature."""
        if self.extract_full_state:
            # We need all fields if passing full state
            return []

        # Analyze the callable signature
        sig = inspect.signature(self.callable_func)
        fields = []

        for param_name, param in sig.parameters.items():
            if param_name == "self" or param.kind == inspect.Parameter.VAR_KEYWORD:
                continue

            # Map parameter to state field
            if self.parameter_mapping and param_name in self.parameter_mapping:
                field_name = self.parameter_mapping[param_name]
            else:
                field_name = param_name

            # Try to get type from annotations
            field_type = Any
            if param.annotation != inspect.Parameter.empty:
                field_type = param.annotation

            # Create field definition
            field = FieldDefinition(
                name=field_name,
                field_type=field_type,
                required=(param.default == inspect.Parameter.empty),
                description=f"Parameter {param_name} for {self.callable_func.__name__}",
            )
            fields.append(field)

        return fields

    def __call__(self, state: StateLike, config: ConfigLike | None = None) -> Command:
        """Execute the callable and return appropriate Command."""
        try:
            # Extract parameters
            if self.extract_full_state:
                # Pass the entire state
                result = self.callable_func(state)
            else:
                # Extract specific parameters
                kwargs = self._extract_parameters(state)
                result = self.callable_func(**kwargs)

            # Handle the result
            update = {}
            if self.result_key:
                update[self.result_key] = result

            # Determine routing
            goto = self._determine_goto(result)

            return Command(update=update, goto=goto)

        except Exception as e:
            logger.exception(f"Error in callable node '{self.name}': {e}")

            if self.on_error == "raise":
                raise
            if self.on_error == "return_none":
                return Command(
                    update={self.result_key: None} if self.result_key else {},
                    goto=self.default_goto or self.command_goto,
                )
            if self.on_error == "goto_errof":
                return Command(
                    update={"error": str(e)},
                    goto=self.error_goto or self.default_goto or self.command_goto,
                )

    def _extract_parameters(self, state: StateLike) -> dict[str, Any]:
        """Extract function parameters from state."""
        sig = inspect.signature(self.callable_func)
        kwargs = {}

        for param_name, param in sig.parameters.items():
            if param_name == "self":
                continue

            # Determine state field to extract from
            if self.extraction_paths and param_name in self.extraction_paths:
                # Use advanced path extraction
                path = self.extraction_paths[param_name]
                value = self._extract_by_path(state, path)
            elif self.parameter_mapping and param_name in self.parameter_mapping:
                # Use simple mapping
                field_name = self.parameter_mapping[param_name]
                value = self._get_state_value(state, field_name)
            else:
                # Direct parameter name
                value = self._get_state_value(state, param_name)

            # Use default if not found and available
            if value is None and param.default != inspect.Parameter.empty:
                value = param.default

            kwargs[param_name] = value

        return kwargs

    def _extract_by_path(self, state: StateLike, path: str) -> Any:
        """Extract value using a path like 'messages[0].content'."""
        # This could use the PathResolver from NodeSchemaComposer
        # For now, simple implementation
        parts = path.split(".")
        current = state

        for part in parts:
            if "[" in part and "]" in part:
                # Array access
                field, index = part.split("[")
                index = int(index.rstrip("]"))
                current = self._get_state_value(current, field)
                if current and hasattr(current, "__getitem__"):
                    current = current[index]
                else:
                    return None
            else:
                # Regular field access
                current = self._get_state_value(current, part)

            if current is None:
                return None

        return current

    def _get_state_value(self, obj: Any, field: str) -> Any:
        """Get value from state object."""
        if hasattr(obj, field):
            return getattr(obj, field)
        if hasattr(obj, "__getitem__"):
            try:
                return obj[field]
            except (KeyError, TypeError):
                pass
        return None

    def _determine_goto(self, result: Any) -> str | None:
        """Determine which node to go to based on result."""
        # Boolean routing
        if isinstance(result, bool):
            if result and self.goto_on_true:
                return self.goto_on_true
            if not result and self.goto_on_false:
                return self.goto_on_false

        # Mapped routing
        if self.goto_mapping and result in self.goto_mapping:
            return self.goto_mapping[result]

        # Default routing
        return self.default_goto or self.command_goto


def wrap_callable(
    func: Callable, name: str | None = None, **kwargs
) -> CallableNodeConfig:
    """Convenience function to wrap a callable as a node.

    Args:
        func: The function to wrap
        name: Node name (defaults to function name)
        **kwargs: Additional CallableNodeConfig parameters

    Returns:
        Configured CallableNodeConfig

    Example:
        node = wrap_callable(
            check_threshold,
            goto_on_true="summarize",
            goto_on_false="continue"
        )
    """
    if name is None:
        name = func.__name__

    return CallableNodeConfig(name=name, callable_func=func, **kwargs)


# Decorator version
def as_node(**kwargs) -> Any:
    """Decorator to turn a function into a node.

    Example:
        @as_node(goto_on_true="next", goto_on_false="retry")
        def should_continue(messages: List[BaseMessage]) -> bool:
            return len(messages) > 5
    """

    def decorator(func: Callable) -> CallableNodeConfig:
        return wrap_callable(func, **kwargs)

    return decorator
