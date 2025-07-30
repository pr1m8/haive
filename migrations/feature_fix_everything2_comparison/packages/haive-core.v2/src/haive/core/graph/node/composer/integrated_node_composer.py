"""Integrated NodeSchemaComposer - Unified with core schema system.

from typing import Any
This module integrates NodeSchemaComposer with the core schema system,
providing consistent patterns for node I/O configuration that work with
StateSchema, SchemaComposer, and the broader Haive architecture.
"""

import logging
from collections.abc import Callable
from typing import Any, TypeVar

from haive.core.common.schema.field_definition import FieldDefinition
from haive.core.graph.node.base_config import NodeConfig
from haive.core.graph.node.composer.field_mapping import FieldMapping
from haive.core.graph.node.composer.node_schema_composer import NodeSchemaComposer
from haive.core.schema import StateSchema
from haive.core.schema.schema_composer import SchemaComposer

logger = logging.getLogger(__name__)

TState = TypeVar("TState", bound=StateSchema)
TNode = TypeVar("TNode", bound=NodeConfig)


class IntegratedNodeComposer(NodeSchemaComposer):
    """NodeSchemaComposer integrated with core schema system.

    This class bridges NodeSchemaComposer's flexible I/O mapping with:
    - StateSchema's field sharing and reducers
    - SchemaComposer's dynamic schema building
    - FieldDefinition metadata system
    - Engine I/O tracking

    Key features:
    - Automatic StateSchema generation for composed nodes
    - Field definition preservation through mappings
    - Integration with engine I/O mappings
    - Support for shared fields and reducers
    """

    def __init__(self) -> None:
        """Initialize with schema composer integration."""
        super().__init__()
        self.schema_composer = SchemaComposer()
        self._composed_schemas: dict[str, type[StateSchema]] = {}

    def compose_node_with_schema(
        self,
        base_node: TNode,
        input_mappings: list[FieldMapping] | None = None,
        output_mappings: list[FieldMapping] | None = None,
        state_schema: type[StateSchema] | None = None,
        preserve_field_metadata: bool = True,
        name: str | None = None,
    ) -> "SchemaAwareComposedNode":
        """Compose node with automatic schema generation.

        Args:
            base_node: Node to wrap
            input_mappings: Input field mappings
            output_mappings: Output field mappings
            state_schema: Optional state schema to use
            preserve_field_metadata: Keep field definitions
            name: Node name

        Returns:
            SchemaAwareComposedNode with integrated schema support
        """
        # Generate or use provided schema
        if state_schema is None:
            state_schema = self._generate_state_schema(
                base_node, input_mappings, output_mappings, preserve_field_metadata
            )

        # Create composed node
        composed = SchemaAwareComposedNode(
            base_node=base_node,
            input_mappings=input_mappings or [],
            output_mappings=output_mappings or [],
            state_schema=state_schema,
            name=name or f"composed_{base_node.name}",
            composer=self,
        )

        # Store schema for reuse
        self._composed_schemas[composed.name] = state_schema

        return composed

    def _generate_state_schema(
        self,
        base_node: TNode,
        input_mappings: list[FieldMapping] | None,
        output_mappings: list[FieldMapping] | None,
        preserve_metadata: bool,
    ) -> type[StateSchema]:
        """Generate StateSchema for composed node.

        This creates a dynamic StateSchema that includes:
        - Mapped fields from input/output mappings
        - Field definitions with proper metadata
        - Engine I/O mappings for tracking
        - Reducer functions where applicable
        """
        # Start with base schema if node has one
        if hasattr(base_node, "input_schema") and base_node.input_schema:
            self.schema_composer.from_schema(base_node.input_schema)

        # Add fields from mappings
        all_mappings = (input_mappings or []) + (output_mappings or [])

        for mapping in all_mappings:
            # Create field definition
            field_def = self._create_field_definition(
                mapping, base_node, preserve_metadata
            )

            # Add to schema composer
            self.schema_composer.add_field(
                name=mapping.target_path,
                field_type=Any,  # Type will be inferred
                field_definition=field_def,
                default=mapping.default,
            )

        # Add engine I/O mapping if applicable
        if hasattr(base_node, "engine_name"):
            engine_name = base_node.engine_name

            # Track input fields
            if input_mappings:
                for mapping in input_mappings:
                    self.schema_composer.add_engine_input_mapping(
                        engine_name, mapping.target_path
                    )

            # Track output fields
            if output_mappings:
                for mapping in output_mappings:
                    self.schema_composer.add_engine_output_mapping(
                        engine_name, mapping.target_path
                    )

        # Build the schema
        schema_name = f"{base_node.name}ComposedState"
        return self.schema_composer.build_state_schema(schema_name)

    def _create_field_definition(
        self, mapping: FieldMapping, base_node: TNode, preserve_metadata: bool
    ) -> FieldDefinition:
        """Create field definition for mapped field.

        Preserves metadata from original field if available.
        """
        # Try to find original field definition
        original_def = None

        if preserve_metadata and hasattr(base_node, "field_definitions"):
            # Look for source field definition
            for field_def in base_node.field_definitions:
                if field_def.name == mapping.source_path:
                    original_def = field_def
                    break

        # Create new definition
        if original_def:
            # Preserve original metadata
            return FieldDefinition(
                name=mapping.target_path,
                type_=original_def.type_,
                description=f"Mapped from {
                    mapping.source_path}: {
                    original_def.description}",
                owner=base_node.name,
                sharing_strategy=original_def.sharing_strategy,
                persistence_strategy=original_def.persistence_strategy,
                is_private=original_def.is_private,
            )
        # Create basic definition
        return FieldDefinition(
            name=mapping.target_path,
            type_=Any,
            description=f"Mapped from {mapping.source_path}",
            owner=base_node.name,
        )

    def create_schema_adapter(
        self,
        source_schema: type[StateSchema],
        target_schema: type[StateSchema],
        field_mappings: list[FieldMapping],
        preserve_reducers: bool = True,
        preserve_sharing: bool = True,
        name: str | None = None,
    ) -> "StateSchemaAdapter":
        """Create adapter between StateSchema types.

        Args:
            source_schema: Source StateSchema
            target_schema: Target StateSchema
            field_mappings: How to map fields
            preserve_reducers: Keep reducer functions
            preserve_sharing: Keep field sharing settings
            name: Adapter name

        Returns:
            StateSchemaAdapter that converts between schemas
        """
        return StateSchemaAdapter(
            source_schema=source_schema,
            target_schema=target_schema,
            field_mappings=field_mappings,
            preserve_reducers=preserve_reducers,
            preserve_sharing=preserve_sharing,
            name=name
            or f"adapter_{source_schema.__name__}_to_{target_schema.__name__}",
            composer=self,
        )

    def from_callable_with_schema(
        self,
        func: Callable,
        input_schema: type[StateSchema] | None = None,
        output_schema: type[StateSchema] | None = None,
        input_mappings: list[FieldMapping] | None = None,
        output_mappings: list[FieldMapping] | None = None,
        generate_schema: bool = True,
        **kwargs,
    ) -> "SchemaAwareComposedNode":
        """Create node from callable with schema support.

        Args:
            func: Function to wrap
            input_schema: Expected input schema
            output_schema: Expected output schema
            input_mappings: Input field mappings
            output_mappings: Output field mappings
            generate_schema: Auto-generate schema if not provided
            **kwargs: Additional node configuration

        Returns:
            SchemaAwareComposedNode with proper schemas
        """
        # Create base callable node
        from haive.core.graph.node.callable_node import CallableNodeConfig

        base_node = CallableNodeConfig(
            name=kwargs.pop("name", func.__name__),
            callable_func=func,
            input_schema=input_schema,
            output_schema=output_schema,
            **kwargs,
        )

        # Generate state schema if needed
        if generate_schema and not input_schema:
            state_schema = self._generate_state_schema(
                base_node, input_mappings, output_mappings, preserve_metadata=True
            )
        else:
            state_schema = input_schema

        return self.compose_node_with_schema(
            base_node=base_node,
            input_mappings=input_mappings,
            output_mappings=output_mappings,
            state_schema=state_schema,
        )


class SchemaAwareComposedNode:
    """Composed node with StateSchema integration.

    This node type:
    - Uses StateSchema for type-safe state management
    - Preserves field metadata through mappings
    - Integrates with engine I/O tracking
    - Supports field sharing and reducers
    """

    def __init__(
        self,
        base_node: NodeConfig,
        input_mappings: list[FieldMapping],
        output_mappings: list[FieldMapping],
        state_schema: type[StateSchema],
        name: str,
        composer: IntegratedNodeComposer,
    ):
        self.base_node = base_node
        self.input_mappings = input_mappings
        self.output_mappings = output_mappings
        self.state_schema = state_schema
        self.name = name
        self.composer = composer

        # Create extract/update functions
        self.extract_func = (
            composer.create_extract_function(input_mappings) if input_mappings else None
        )
        self.update_func = (
            composer.create_update_function(output_mappings)
            if output_mappings
            else None
        )

    def __call__(
        self,
        state: StateSchema | dict[str, Any],
        config: dict[str, Any] | None = None,
    ) -> Any:
        """Execute with StateSchema support."""
        config = config or {}

        # Ensure state is StateSchema instance
        if not isinstance(state, StateSchema):
            if isinstance(state, dict) and self.state_schema:
                state = self.state_schema(**state)
            else:
                # Fallback to dict
                pass
            if hasattr(result, "update") and result.update:
                actual_result = result.update
            elif hasattr(result, "arg"):
                actual_result = result.arg

            # Apply mappings
            mapped_updates = self.update_func(actual_result, state, config)

            # Apply reducers if using StateSchema
            if isinstance(state, StateSchema) and hasattr(state, "__reducer_fields__"):
                for field, updates in mapped_updates.items():
                    if field in state.__reducer_fields__:
                        reducer = state.__reducer_fields__[field]
                        current = getattr(state, field, None)
                        mapped_updates[field] = reducer(current, updates)

            # Return with proper structure
            if hasattr(result, "update") and result.update:
                final_updates = {**result.update, **mapped_updates}
                if hasattr(result, "model_copy"):
                    return result.model_copy(update={"update": final_updates})
                result.update = final_updates
                return result
            return Command(update=mapped_updates, goto=getattr(result, "goto", None))

        return result

    @property
    def input_schema(self) -> type[StateSchema] | None:
        """Get input schema for this node."""
        return self.state_schema

    @property
    def output_schema(self) -> type[StateSchema] | None:
        """Get output schema for this node."""
        return self.state_schema


class StateSchemaAdapter:
    """Adapter between different StateSchema types.

    Handles:
    - Field mappings with metadata preservation
    - Reducer function compatibility
    - Shared field settings
    - Engine I/O mappings
    """

    def __init__(
        self,
        source_schema: type[StateSchema],
        target_schema: type[StateSchema],
        field_mappings: list[FieldMapping],
        preserve_reducers: bool,
        preserve_sharing: bool,
        name: str,
        composer: IntegratedNodeComposer,
    ):
        self.source_schema = source_schema
        self.target_schema = target_schema
        self.field_mappings = field_mappings
        self.preserve_reducers = preserve_reducers
        self.preserve_sharing = preserve_sharing
        self.name = name
        self.composer = composer

    def adapt(self, source_instance: StateSchema) -> StateSchema:
        """Adapt from source to target schema.

        Preserves:
        - Field values through mappings
        - Reducer compatibility
        - Shared field settings
        - Type safety
        """
        # Extract mapped values
        mapped_data = {}

        for mapping in self.field_mappings:
            value = self.composer.path_resolver.extract_value(
                source_instance, mapping.source_path, mapping.default
            )

            # Apply transforms
            transformed = self.composer._apply_transforms(value, mapping.transform)

            # Handle reducer if preserving
            if (
                self.preserve_reducers
                and hasattr(self.target_schema, "__reducer_fields__")
                and mapping.target_path in self.target_schema.__reducer_fields__
            ):
                reducer = self.target_schema.__reducer_fields__[mapping.target_path]
                current = getattr(self.target_schema, mapping.target_path, None)
                transformed = reducer(current, transformed)

            mapped_data[mapping.target_path] = transformed

        # Create target instance
        return self.target_schema(**mapped_data)


# Factory functions for common patterns
def integrate_node_with_schema(
    node: NodeConfig,
    schema: type[StateSchema],
    input_mappings: list[FieldMapping] | None = None,
    output_mappings: list[FieldMapping] | None = None,
) -> SchemaAwareComposedNode:
    """Quick function to integrate node with StateSchema.

    Args:
        node: Node to integrate
        schema: StateSchema to use
        input_mappings: Optional input mappings
        output_mappings: Optional output mappings

    Returns:
        SchemaAwareComposedNode with schema integration
    """
    composer = IntegratedNodeComposer()
    return composer.compose_node_with_schema(
        base_node=node,
        input_mappings=input_mappings,
        output_mappings=output_mappings,
        state_schema=schema,
    )


def create_schema_aware_node(
    func: Callable, schema: type[StateSchema], **kwargs
) -> SchemaAwareComposedNode:
    """Create node from callable with StateSchema.

    Args:
        func: Function to wrap
        schema: StateSchema to use
        **kwargs: Additional configuration

    Returns:
        SchemaAwareComposedNode
    """
    composer = IntegratedNodeComposer()
    return composer.from_callable_with_schema(
        func=func, input_schema=schema, generate_schema=False, **kwargs
    )


# Decorator for schema-aware nodes
def with_state_schema(
    schema: type[StateSchema],
    input_mappings: list[FieldMapping] | None = None,
    output_mappings: list[FieldMapping] | None = None,
    **kwargs,
):
    """Decorator to create schema-aware nodes.

    Examples:
        @with_state_schema(MyStateSchema)
        def process(state: MyStateSchema) -> Dict[str, Any]:
            return {"result": state.value * 2}

        @with_state_schema(
            MyStateSchema,
            output_mappings=[FieldMapping("result", "processed_value")]
        )
        def process(state):
            return {"result": "done"}
    """

    def decorator(func: Callable) -> SchemaAwareComposedNode:
        composer = IntegratedNodeComposer()
        return composer.from_callable_with_schema(
            func=func,
            input_schema=schema,
            input_mappings=input_mappings,
            output_mappings=output_mappings,
            generate_schema=False,
            **kwargs,
        )

    return decorator
