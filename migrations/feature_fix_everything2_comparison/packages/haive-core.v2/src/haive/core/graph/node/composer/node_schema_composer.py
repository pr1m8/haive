"""NodeSchemaComposer - Main composer for flexible node I/O configuration.

This module provides the main NodeSchemaComposer class that enables arbitrary
field mappings like "result → retrieved_documents" or "documents → potato"
with pluggable extract/update functions.

This solves the critical gap where you cannot easily modify node input/output
schemas or create composed nodes with custom field mappings.
"""

import logging
from collections.abc import Callable
from typing import Any, TypeVar

from pydantic import BaseModel

from haive.core.graph.node.composer.extract_functions import ExtractFunctions
from haive.core.graph.node.composer.field_mapping import FieldMapping
from haive.core.graph.node.composer.path_resolver import PathResolver
from haive.core.graph.node.composer.protocols import (
    ExtractFunction,
    TransformFunction,
    UpdateFunction,
)
from haive.core.graph.node.composer.update_functions import UpdateFunctions

logger = logging.getLogger(__name__)

# Type variables
TState = TypeVar("TState", bound=BaseModel)
TInput = TypeVar("TInput")
TOutput = TypeVar("TOutput")
TNode = TypeVar("TNode")


class NodeSchemaComposer:
    """Main composer for flexible node I/O configuration.

    This class enables "result → potato" style field mappings by:
    1. Registering custom extract/update functions
    2. Composing field mappings for nodes
    3. Wrapping existing nodes with new I/O schemas
    4. Creating adapters for type compatibility

    Examples:
        # Change retriever output from "documents" to "retrieved_documents"
        composer = NodeSchemaComposer()

        retriever_node = composer.compose_node(
            base_node=existing_retriever_node,
            output_mappings=[
                FieldMapping("documents", "retrieved_documents")
            ]
        )

        # Create callable node with custom field mapping
        check_node = composer.from_callable(
            func=lambda msgs: len(msgs) > 5,
            input_mappings=[
                FieldMapping("messages", "msgs")
            ],
            output_mappings=[
                FieldMapping("result", "should_continue", transform=["bool_to_str"])
            ]
        )
    """

    def __init__(self) -> None:
        """Initialize composer with built-in functions."""
        self.path_resolver = PathResolver()
        self.extract_functions = ExtractFunctions()
        self.update_functions = UpdateFunctions()

        # Registries for custom functions
        self._extract_registry: dict[str, ExtractFunction] = {}
        self._update_registry: dict[str, UpdateFunction] = {}
        self._transform_registry: dict[str, TransformFunction] = {}

        # Register built-in transforms
        self._register_builtin_transforms()

    def _register_builtin_transforms(self):
        """Register common transform functions."""
        self._transform_registry.update(
            {
                "strip": lambda x: str(x).strip() if x is not None else "",
                "uppercase": lambda x: str(x).upper() if x is not None else "",
                "lowercase": lambda x: str(x).lower() if x is not None else "",
                "bool_to_str": lambda x: "true" if x else "false",
                "str_to_bool": lambda x: str(x).lower() in ("true", "1", "yes"),
                "parse_int": lambda x: int(x) if x is not None else 0,
                "parse_float": lambda x: float(x) if x is not None else 0.0,
            }
        )

    def register_extract_function(self, name: str, func: ExtractFunction):
        """Register a custom extract function.

        Args:
            name: Name to register under
            func: Extract function that takes (state, config) -> value
        """
        self._extract_registry[name] = func
        logger.debug(f"Registered extract function: {name}")

    def register_update_function(self, name: str, func: UpdateFunction):
        """Register a custom update function.

        Args:
            name: Name to register under
            func: Update function that takes (result, state, config) -> dict
        """
        self._update_registry[name] = func
        logger.debug(f"Registered update function: {name}")

    def register_transform_function(self, name: str, func: TransformFunction):
        """Register a custom transform function.

        Args:
            name: Name to register under
            func: Transform function that takes value -> transformed_value
        """
        self._transform_registry[name] = func
        logger.debug(f"Registered transform function: {name}")

    def create_extract_function(
        self, mappings: list[FieldMapping], fallback_extract: str | None = None
    ) -> ExtractFunction:
        """Create extract function from field mappings.

        Args:
            mappings: List of field mappings for extraction
            fallback_extract: Name of fallback extract function if mappings fail

        Returns:
            Extract function that handles all mappings
        """

        def _extract(state: Any, config: dict[str, Any]) -> Any:
            """Extract values according to field mappings."""
            if len(mappings) == 1:
                # Single mapping - return value directly
                mapping = mappings[0]
                value = self.path_resolver.extract_value(
                    state, mapping.source_path, mapping.default
                )
                return self._apply_transforms(value, mapping.transform)
            # Multiple mappings - return dict
            result = {}
            for mapping in mappings:
                value = self.path_resolver.extract_value(
                    state, mapping.source_path, mapping.default
                )
                transformed = self._apply_transforms(value, mapping.transform)
                result[mapping.target_path] = transformed
            return result

        return _extract

    def create_update_function(
        self, mappings: list[FieldMapping], merge_mode: str = "replace"
    ) -> UpdateFunction:
        """Create update function from field mappings.

        Args:
            mappings: List of field mappings for updates
            merge_mode: How to merge updates ("replace", "merge", "append")

        Returns:
            Update function that handles all mappings
        """

        def _update(result: Any, state: Any, config: dict[str, Any]) -> dict[str, Any]:
            """Update state according to field mappings."""
            updates = {}

            for mapping in mappings:
                # Extract value from result using source_path
                if isinstance(result, dict):
                    value = result.get(mapping.source_path, mapping.default)
                # For single values, use source_path as key or the whole result
                elif mapping.source_path in {"result", ""}:
                    value = result
                else:
                    value = getattr(result, mapping.source_path, mapping.default)

                # Apply transforms
                transformed = self._apply_transforms(value, mapping.transform)

                # Update target path
                updates[mapping.target_path] = transformed

            return updates

        return _update

    def _apply_transforms(self, value: Any, transform_names: list[str] | None) -> Any:
        """Apply transform pipeline to value.

        Args:
            value: Value to transform
            transform_names: List of transform function names to apply

        Returns:
            Transformed value
        """
        if not transform_names:
            return value

        result = value
        for transform_name in transform_names:
            if transform_name in self._transform_registry:
                transform_func = self._transform_registry[transform_name]
                result = transform_func(result)
            else:
                logger.warning(f"Unknown transform function: {transform_name}")

        return result

    def compose_node(
        self,
        base_node: Any,
        input_mappings: list[FieldMapping] | None = None,
        output_mappings: list[FieldMapping] | None = None,
        name: str | None = None,
    ) -> "ComposedNode":
        """Compose a node with custom I/O mappings.

        Args:
            base_node: Existing node to wrap
            input_mappings: How to map state fields to node inputs
            output_mappings: How to map node outputs to state fields
            name: Optional name for the composed node

        Returns:
            ComposedNode with custom I/O mappings

        Examples:
            # Change retriever output key
            retriever = composer.compose_node(
                base_node=existing_retriever,
                output_mappings=[
                    FieldMapping("documents", "retrieved_documents")
                ]
            )

            # Add input/output transforms
            agent = composer.compose_node(
                base_node=existing_agent,
                input_mappings=[
                    FieldMapping("messages", "conversation", transform=["filter_human"])
                ],
                output_mappings=[
                    FieldMapping("response", "ai_response", transform=["strip"])
                ]
            )
        """
        return ComposedNode(
            base_node=base_node,
            input_mappings=input_mappings or [],
            output_mappings=output_mappings or [],
            name=name or f"composed_{getattr(base_node, 'name', 'node')}",
            composer=self,
        )

    def from_callable(
        self,
        func: Callable,
        input_mappings: list[FieldMapping] | None = None,
        output_mappings: list[FieldMapping] | None = None,
        name: str | None = None,
        **callable_kwargs,
    ) -> "ComposedCallableNode":
        """Create a composed node from a callable function.

        Args:
            func: Function to wrap as a node
            input_mappings: How to extract function parameters from state
            output_mappings: How to map function result to state updates
            name: Optional name for the node
            **callable_kwargs: Additional arguments for CallableNodeConfig

        Returns:
            ComposedCallableNode with custom I/O mappings

        Examples:
            # Simple boolean check with field mapping
            check_node = composer.from_callable(
                func=lambda msgs: len(msgs) > 5,
                input_mappings=[
                    FieldMapping("messages", "msgs")
                ],
                output_mappings=[
                    FieldMapping("result", "should_continue")
                ]
            )

            # Complex processing with transforms
            process_node = composer.from_callable(
                func=process_documents,
                input_mappings=[
                    FieldMapping("documents", "docs"),
                    FieldMapping("config.batch_size", "batch_size", default=10)
                ],
                output_mappings=[
                    FieldMapping("processed", "result", transform=["validate"])
                ]
            )
        """
        from haive.core.graph.node.callable_node import CallableNodeConfig

        # Create base callable node
        base_node = CallableNodeConfig(
            name=name or func.__name__, callable_func=func, **callable_kwargs
        )

        return ComposedCallableNode(
            base_node=base_node,
            input_mappings=input_mappings or [],
            output_mappings=output_mappings or [],
            name=name or f"composed_{func.__name__}",
            composer=self,
        )

    def create_adapter(
        self,
        source_schema: type[BaseModel],
        target_schema: type[BaseModel],
        field_mappings: list[FieldMapping],
        name: str | None = None,
    ) -> "SchemaAdapter":
        """Create an adapter between two schemas.

        Args:
            source_schema: Source Pydantic model
            target_schema: Target Pydantic model
            field_mappings: How to map fields between schemas
            name: Optional name for the adapter

        Returns:
            SchemaAdapter that converts between schemas

        Examples:
            # Adapt between different state schemas
            adapter = composer.create_adapter(
                source_schema=OldState,
                target_schema=NewState,
                field_mappings=[
                    FieldMapping("old_field", "new_field"),
                    FieldMapping("data", "processed_data", transform=["validate"])
                ]
            )
        """
        return SchemaAdapter(
            source_schema=source_schema,
            target_schema=target_schema,
            field_mappings=field_mappings,
            name=name
            or f"adapter_{source_schema.__name__}_to_{target_schema.__name__}",
            composer=self,
        )


class ComposedNode:
    """A node composed with custom I/O mappings.

    This wraps an existing node and applies field mappings to transform inputs and
    outputs according to the "result → potato" pattern.
    """

    def __init__(
        self,
        base_node: Any,
        input_mappings: list[FieldMapping],
        output_mappings: list[FieldMapping],
        name: str,
        composer: NodeSchemaComposer,
    ):
        self.base_node = base_node
        self.input_mappings = input_mappings
        self.output_mappings = output_mappings
        self.name = name
        self.composer = composer

        # Create I/O functions
        if input_mappings:
            self.extract_func = composer.create_extract_function(input_mappings)
        else:
            self.extract_func = None

        if output_mappings:
            self.update_func = composer.create_update_function(output_mappings)
        else:
            self.update_func = None

    def __call__(self, state: Any, config: dict[str, Any] | None = None) -> Any:
        """Execute the composed node with I/O mappings."""
        config = config or {}

        # Extract inputs if mappings provided
        if self.extract_func:
            node_input = self.extract_func(state, config)
            # If it's a single value, pass directly; if dict, merge with state
            if isinstance(node_input, dict):
                # Create modified state with mapped inputs
                if hasattr(state, "model_copy"):
                    # Pydantic model
                    node_state = state.model_copy(update=node_input)
                elif isinstance(state, dict):
                    # Dictionary state
                    node_state = {**state, **node_input}
                else:
                    # Other state types - use dict
                    node_state = node_input
            else:
                node_state = state
        else:
            node_state = state

        # Execute base node
        result = self.base_node(node_state, config)

        # Apply output mappings if provided
        if self.update_func:
            # Extract the actual result from Command/Send if needed
            actual_result = result
            if hasattr(result, "update") and result.update:
                actual_result = result.update
            elif hasattr(result, "arg"):
                actual_result = result.arg

            # Apply mappings
            mapped_updates = self.update_func(actual_result, state, config)

            # Merge with existing updates
            if hasattr(result, "update") and result.update:
                # It's a Command - merge updates
                final_updates = {**result.update, **mapped_updates}
                if hasattr(result, "model_copy"):
                    return result.model_copy(update={"update": final_updates})
                # Reconstruct command-like object
                result.update = final_updates
                return result
            # Return new Command with mapped updates
            from langgraph.types import Command

            return Command(update=mapped_updates, goto=getattr(result, "goto", None))

        return result


class ComposedCallableNode(ComposedNode):
    """A callable function composed as a node with custom I/O mappings."""

    def __init__(
        self,
        base_node: Any,  # CallableNodeConfig
        input_mappings: list[FieldMapping],
        output_mappings: list[FieldMapping],
        name: str,
        composer: NodeSchemaComposer,
    ):
        super().__init__(base_node, input_mappings, output_mappings, name, composer)


class SchemaAdapter:
    """Adapter between two Pydantic schemas with field mappings."""

    def __init__(
        self,
        source_schema: type[BaseModel],
        target_schema: type[BaseModel],
        field_mappings: list[FieldMapping],
        name: str,
        composer: NodeSchemaComposer,
    ):
        self.source_schema = source_schema
        self.target_schema = target_schema
        self.field_mappings = field_mappings
        self.name = name
        self.composer = composer

    def adapt(self, source_instance: BaseModel) -> BaseModel:
        """Adapt from source schema to target schema."""
        # Extract mapped values
        mapped_data = {}
        for mapping in self.field_mappings:
            value = self.composer.path_resolver.extract_value(
                source_instance, mapping.source_path, mapping.default
            )
            transformed = self.composer._apply_transforms(value, mapping.transform)
            mapped_data[mapping.target_path] = transformed

        # Create target instance
        return self.target_schema(**mapped_data)


# Factory functions for common patterns
def change_output_key(node: Any, old_key: str, new_key: str) -> ComposedNode:
    """Quick function to change a node's output key.

    Args:
        node: Existing node
        old_key: Current output field name
        new_key: New output field name

    Returns:
        ComposedNode with remapped output

    Examples:
        # Change retriever output from "documents" to "retrieved_documents"
        retriever = change_output_key(base_retriever, "documents", "retrieved_documents")

        # Change agent output from "response" to "ai_message"
        agent = change_output_key(base_agent, "response", "ai_message")
    """
    composer = NodeSchemaComposer()
    return composer.compose_node(
        base_node=node, output_mappings=[FieldMapping(old_key, new_key)]
    )


def change_input_key(node: Any, old_key: str, new_key: str) -> ComposedNode:
    """Quick function to change a node's input key.

    Args:
        node: Existing node
        old_key: Expected input field name
        new_key: Actual field name in state

    Returns:
        ComposedNode with remapped input
    """
    composer = NodeSchemaComposer()
    return composer.compose_node(
        base_node=node, input_mappings=[FieldMapping(new_key, old_key)]
    )


def remap_fields(
    node: Any,
    input_mapping: dict[str, str] | None = None,
    output_mapping: dict[str, str] | None = None,
) -> ComposedNode:
    """Quick function to remap multiple fields.

    Args:
        node: Existing node
        input_mapping: Dict of state_field -> node_field mappings
        output_mapping: Dict of node_field -> state_field mappings

    Returns:
        ComposedNode with remapped fields

    Examples:
        # Remap both input and output
        adapted = remap_fields(
            node=base_node,
            input_mapping={"current_query": "query", "context": "background"},
            output_mapping={"result": "processed_result", "metadata": "info"}
        )
    """
    composer = NodeSchemaComposer()

    input_mappings = []
    if input_mapping:
        for state_field, node_field in input_mapping.items():
            input_mappings.append(FieldMapping(state_field, node_field))

    output_mappings = []
    if output_mapping:
        for node_field, state_field in output_mapping.items():
            output_mappings.append(FieldMapping(node_field, state_field))

    return composer.compose_node(
        base_node=node, input_mappings=input_mappings, output_mappings=output_mappings
    )
