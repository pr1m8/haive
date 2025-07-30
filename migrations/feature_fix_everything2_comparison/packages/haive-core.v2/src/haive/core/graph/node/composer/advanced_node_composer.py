"""Advanced NodeSchemaComposer - Extended node logic and callable patterns.

from typing import Any
This module extends NodeSchemaComposer with advanced patterns for:
1. Different callable signatures (state, config variations)
2. Extended extraction/update logic
3. Type-aware callable handling
4. Command/Send return value handling
5. Automatic signature inspection
"""

import inspect
import logging
from collections.abc import Callable
from functools import wraps
from typing import Any, TypeVar, get_type_hints

from langgraph.types import Command, Send

from haive.core.graph.node.composer.field_mapping import FieldMapping
from haive.core.graph.node.composer.node_schema_composer import (
    ComposedNode,
    NodeSchemaComposer,
)
from haive.core.graph.node.composer.protocols import ExtractFunction, UpdateFunction

logger = logging.getLogger(__name__)

TState = TypeVar("TState")
TConfig = TypeVar("TConfig")
TResult = TypeVar("TResult")


class AdvancedNodeComposer(NodeSchemaComposer):
    """Extended NodeSchemaComposer with advanced callable handling.

    Supports:
    - Multiple callable signatures
    - Type-aware parameter mapping
    - Command/Send return handling
    - Extended extraction/update logic
    - Automatic signature detection
    """

    def from_callable_advanced(
        self,
        func: Callable,
        input_mappings: list[FieldMapping] | None = None,
        output_mappings: list[FieldMapping] | None = None,
        extract_logic: ExtractFunction | None = None,
        update_logic: UpdateFunction | None = None,
        name: str | None = None,
        auto_detect_signature: bool = True,
        handle_command: bool = True,
        **callable_kwargs,
    ) -> "AdvancedComposedNode":
        """Create advanced composed node from callable with flexible signatures.

        Args:
            func: Callable with various signature patterns
            input_mappings: Field mappings for inputs
            output_mappings: Field mappings for outputs
            extract_logic: Custom extraction function
            update_logic: Custom update function
            name: Node name
            auto_detect_signature: Auto-detect callable signature
            handle_command: Wrap non-Command returns in Command
            **callable_kwargs: Additional CallableNodeConfig args

        Returns:
            AdvancedComposedNode with smart handling

        Examples:
            # Simple function
            def process(state):
                return {"result": state.messages}

            # With config
            def process(state, config):
                return Command(update={"done": True})

            # With type hints
            def process(state: MessagesState, config: Dict[str, Any]) -> Command:
                return Command(update={"processed": True})

            # All are handled automatically!
        """
        # Analyze function signature
        sig_info = (
            self._analyze_callable_signature(func) if auto_detect_signature else {}
        )

        # Create wrapped function that normalizes signatures
        wrapped_func = self._create_normalized_callable(func, sig_info, handle_command)

        # Use base method to create node
        from haive.core.graph.node.callable_node import CallableNodeConfig

        base_node = CallableNodeConfig(
            name=name or func.__name__, callable_func=wrapped_func, **callable_kwargs
        )

        return AdvancedComposedNode(
            base_node=base_node,
            input_mappings=input_mappings or [],
            output_mappings=output_mappings or [],
            extract_logic=extract_logic,
            update_logic=update_logic,
            name=name or f"advanced_{func.__name__}",
            composer=self,
            original_func=func,
            signature_info=sig_info,
        )

    def _analyze_callable_signature(self, func: Callable) -> dict[str, Any]:
        """Analyze callable signature for parameter info.

        Returns dict with:
        - has_state: bool
        - has_config: bool
        - state_param: str (parameter name)
        - config_param: str (parameter name)
        - type_hints: dict
        - return_type: type hint
        """
        sig = inspect.signature(func)
        params = list(sig.parameters.values())
        type_hints = get_type_hints(func)

        info = {
            "has_state": False,
            "has_config": False,
            "state_param": None,
            "config_param": None,
            "type_hints": type_hints,
            "return_type": type_hints.get("return"),
            "params": params,
        }

        # Detect state parameter (first param or named 'state')
        if params:
            first_param = params[0]
            if first_param.name == "state" or len(params) == 1:
                info["has_state"] = True
                info["state_param"] = first_param.name

        # Detect config parameter
        for param in params[1:]:
            if param.name == "config" or "config" in param.name.lower():
                info["has_config"] = True
                info["config_param"] = param.name
                break

        return info

    def _create_normalized_callable(
        self, func: Callable, sig_info: dict[str, Any], handle_command: bool
    ) -> Callable:
        """Create normalized callable that handles different signatures.

        Normalizes to: (state, config) -> Any
        """

        @wraps(func)
        def normalized_wrapper(state: Any, config: dict[str, Any] | None = None) -> Any:
            config = config or {}

            # Build kwargs based on signature
            kwargs = {}

            if sig_info.get("has_state"):
                kwargs[sig_info["state_param"]] = state

            if sig_info.get("has_config") and sig_info.get("config_param"):
                kwargs[sig_info["config_param"]] = config

            # Handle different call patterns
            if not kwargs:
                # No recognized params, try positional
                if len(sig_info.get("params", [])) == 0:
                    result = func()
                elif len(sig_info.get("params", [])) == 1:
                    result = func(state)
                else:
                    result = func(state, config)
            else:
                # Use detected kwargs
                result = func(**kwargs)

            # Handle Command wrapping if needed
            if handle_command and not isinstance(result, Command | Send):
                # Auto-wrap in Command if it's a dict update
                if isinstance(result, dict):
                    return Command(update=result)
                # Wrap other values as single field update
                return Command(update={"result": result})

            return result

        return normalized_wrapper

    def create_typed_callable_node(
        self,
        func: Callable[[TState, TConfig], TResult],
        state_type: type[TState],
        config_type: type[TConfig] = dict[str, Any],
        result_type: type[TResult] | None = None,
        input_mappings: list[FieldMapping] | None = None,
        output_mappings: list[FieldMapping] | None = None,
        validate_types: bool = True,
        **kwargs,
    ) -> "TypedCallableNode":
        """Create type-safe callable node with validation.

        Args:
            func: Typed callable function
            state_type: Expected state type
            config_type: Expected config type
            result_type: Expected result type
            input_mappings: Input field mappings
            output_mappings: Output field mappings
            validate_types: Whether to validate types at runtime

        Returns:
            TypedCallableNode with type validation
        """

        # Create type-validating wrapper
        @wraps(func)
        def typed_wrapper(state: Any, config: Any) -> Any:
            # Validate input types if enabled
            if validate_types:
                if not isinstance(state, state_type):
                    logger.warning(
                        f"State type mismatch: expected {state_type}, got {
                            type(state)}"
                    )
                if not isinstance(config, config_type):
                    logger.warning(
                        f"Config type mismatch: expected {config_type}, got {
                            type(config)}"
                    )

            result = func(state, config)

            # Validate output type if specified
            if validate_types and result_type and not isinstance(result, result_type):
                logger.warning(
                    f"Result type mismatch: expected {result_type}, got {
                        type(result)}"
                )

            return result

        # Use advanced method to create node
        return TypedCallableNode(
            base_func=func,
            typed_func=typed_wrapper,
            state_type=state_type,
            config_type=config_type,
            result_type=result_type,
            input_mappings=input_mappings or [],
            output_mappings=output_mappings or [],
            composer=self,
            **kwargs,
        )

    def create_extract_update_node(
        self,
        extract_func: ExtractFunction,
        process_func: Callable[[Any], Any],
        update_func: UpdateFunction,
        name: str = "extract_update_node",
    ) -> ComposedNode:
        """Create node with custom extract/process/update pipeline.

        Args:
            extract_func: Function to extract data from state
            process_func: Function to process extracted data
            update_func: Function to update state with result
            name: Node name

        Returns:
            ComposedNode with custom pipeline

        Example:
            # Custom extraction
            def extract_recent_messages(state, config):
                messages = state.messages[-5:]  # Last 5 messages
                return {"messages": messages, "count": len(messages)}

            # Processing
            def summarize(data):
                return {"summary": f"Last {data['count']} messages processed"}

            # Custom update
            def update_with_summary(result, state, config):
                return {
                    "message_summary": result["summary"],
                    "summary_timestamp": datetime.now()
                }

            node = composer.create_extract_update_node(
                extract_recent_messages,
                summarize,
                update_with_summary
            )
        """

        # Create a callable that uses the pipeline
        def pipeline_callable(
            state: Any, config: dict[str, Any] | None = None
        ) -> Command:
            config = config or {}

            # Extract
            extracted = extract_func(state, config)

            # Process
            result = process_func(extracted)

            # Update
            updates = update_func(result, state, config)

            return Command(update=updates)

        # Create node from callable
        from haive.core.graph.node.callable_node import CallableNodeConfig

        base_node = CallableNodeConfig(name=name, callable_func=pipeline_callable)

        return ComposedNode(
            base_node=base_node,
            input_mappings=[],
            output_mappings=[],
            name=name,
            composer=self,
        )


class AdvancedComposedNode(ComposedNode):
    """Advanced composed node with extended capabilities."""

    def __init__(
        self,
        base_node: Any,
        input_mappings: list[FieldMapping],
        output_mappings: list[FieldMapping],
        extract_logic: ExtractFunction | None,
        update_logic: UpdateFunction | None,
        name: str,
        composer: NodeSchemaComposer,
        original_func: Callable | None = None,
        signature_info: dict[str, Any] | None = None,
    ):
        super().__init__(base_node, input_mappings, output_mappings, name, composer)
        self.extract_logic = extract_logic
        self.update_logic = update_logic
        self.original_func = original_func
        self.signature_info = signature_info

    def __call__(self, state: Any, config: dict[str, Any] | None = None) -> Any:
        """Execute with extended logic."""
        config = config or {}

        # Use custom extract logic if provided
        if self.extract_logic:
            extracted_input = self.extract_logic(state, config)
            # Merge with mapped inputs
            if self.extract_func:
                mapped_input = self.extract_func(state, config)
                if isinstance(mapped_input, dict) and isinstance(extracted_input, dict):
                    extracted_input.update(mapped_input)
        else:
            # Use standard extraction
            extracted_input = (
                self.extract_func(state, config) if self.extract_func else state
            )

        # Prepare state for node
        if isinstance(extracted_input, dict) and hasattr(state, "model_copy"):
            node_state = state.model_copy(update=extracted_input)
        elif isinstance(extracted_input, dict) and isinstance(state, dict):
            node_state = {**state, **extracted_input}
        else:
            node_state = extracted_input or state

        # Execute base node
        result = self.base_node(node_state, config)

        # Use custom update logic if provided
        if self.update_logic:
            updates = self.update_logic(result, state, config)
            # Merge with mapped updates if any
            if self.update_func:
                mapped_updates = self.update_func(result, state, config)
                updates.update(mapped_updates)

            # Return command with updates
            if hasattr(result, "update"):
                return result.model_copy(update={"update": updates})
            return Command(update=updates)
        # Use standard update logic
        return super().__call__(state, config)


class TypedCallableNode:
    """Type-safe callable node with runtime validation."""

    def __init__(
        self,
        base_func: Callable,
        typed_func: Callable,
        state_type: type,
        config_type: type,
        result_type: type | None,
        input_mappings: list[FieldMapping],
        output_mappings: list[FieldMapping],
        composer: NodeSchemaComposer,
        **kwargs,
    ):
        self.base_func = base_func
        self.typed_func = typed_func
        self.state_type = state_type
        self.config_type = config_type
        self.result_type = result_type
        self.input_mappings = input_mappings
        self.output_mappings = output_mappings
        self.composer = composer
        self.kwargs = kwargs

        # Create node
        self.node = composer.from_callable(
            typed_func,
            input_mappings=input_mappings,
            output_mappings=output_mappings,
            **kwargs,
        )

    def __call__(self, state: Any, config: dict[str, Any] | None = None) -> Any:
        """Execute typed node."""
        return self.node(state, config)


# Factory functions for common patterns
def callable_to_node(
    func: Callable, composer: AdvancedNodeComposer | None = None, **kwargs
) -> AdvancedComposedNode:
    """Quick conversion of any callable to node.

    Handles:
    - func(state)
    - func(state, config)
    - func() with no args
    - Typed and untyped versions
    - Command/Send returns

    Examples:
        @callable_to_node
        def my_node(state):
            return {"processed": True}

        # Or explicit
        node = callable_to_node(my_function)
    """
    if composer is None:
        composer = AdvancedNodeComposer()

    return composer.from_callable_advanced(func, **kwargs)


def node_with_custom_logic(
    name: str,
    extract: ExtractFunction,
    process: Callable[[Any], Any],
    update: UpdateFunction,
    composer: AdvancedNodeComposer | None = None,
) -> ComposedNode:
    """Create node with custom extract/process/update pipeline."""
    if composer is None:
        composer = AdvancedNodeComposer()

    return composer.create_extract_update_node(extract, process, update, name)


# Decorator for creating nodes
def as_node(
    input_mappings: list[FieldMapping] | None = None,
    output_mappings: list[FieldMapping] | None = None,
    **kwargs,
):
    """Decorator to convert function to node.

    Examples:
        @as_node(
            input_mappings=[FieldMapping("messages", "conversation")],
            output_mappings=[FieldMapping("result", "should_continue")]
        )
        def check_conversation_length(conversation: List[Message]) -> bool:
            return len(conversation) > 10
    """

    def decorator(func: Callable) -> AdvancedComposedNode:
        composer = AdvancedNodeComposer()
        return composer.from_callable_advanced(
            func,
            input_mappings=input_mappings,
            output_mappings=output_mappings,
            **kwargs,
        )

    return decorator
