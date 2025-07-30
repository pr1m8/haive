"""Protocols for extract and update functions in NodeSchemaComposer.

This module defines the protocol interfaces that extract and update functions must
implement to be compatible with the NodeSchemaComposer system.
"""

from typing import Any, Protocol, TypeVar

from pydantic import BaseModel

# Type variables for protocol generics
TState = TypeVar("TState", bound=BaseModel)
TInput = TypeVar("TInput")
TOutput = TypeVar("TOutput")


class ExtractFunction(Protocol[TState, TInput]):
    """Protocol for extract functions.

    Extract functions take a state object and configuration, returning the extracted
    input data that will be pass         field_name = config.get("field_name",
    "messages")         return getattr(state, field_name, [])

    def extract_with_projection(state: MultiAgentState, config: Dict[str, Any]) ->
    Dict[str, Any]:     # Complex projection logic     return projected_state
    """

    def __call__(self, state: TState, config: dict[str, Any]) -> TInput:
        """Extract input from state.

        Args:
            state: State object to extract from (Pydantic model, dict, etc.)
            config: Configuration dictionary with extraction parameters

        Returns:
            Extracted input data for the node
        """
        ...


class UpdateFunction(Protocol[TState, TOutput]):
    """Protocol for update functions.

    Update functions take the result from node processing along with the
    original state and configuration, returning a dictionary of state updates.

    Examples:
        def update_messages(result: AIMessage, state: MessagesState, config: Dict[str, Any]) -> Dict[str, Any]:
            messages = list(getattr(state, "messages", []))
            messages.append(result)
            return {"messages": messages}

        def update_type_aware(result: Any, state: BaseModel, config: Dict[str, Any]) -> Dict[str, Any]:
            # Smart type-based updates
            return update_dict
    """

    def __call__(
        self, result: TOutput, state: TState, config: dict[str, Any]
    ) -> dict[str, Any]:
        """Create state update from result.

        Args:
            result: Result from node processing (message, dict, model, etc.)
            state: Original state object for context
            config: Configuration dictionary with update parameters

        Returns:
            Dictionary of state field updates to apply
        """
        ...


class TransformFunction(Protocol):
    """Protocol for transform functions.

    Transform functions are used in field mapping pipelines to modify
    values during extraction or update operations.

    Examples:
        def uppercase(value: str) -> str:
            return value.upper() if isinstance(value, str) else str(value).upper()

        def parse_json(value: str) -> Any:
            import json
            return json.loads(value)
    """

    def __call__(self, value: Any) -> Any:
        """Transform a value.

        Args:
            value: Input value to transform

        Returns:
            Transformed value
        """
        ...
