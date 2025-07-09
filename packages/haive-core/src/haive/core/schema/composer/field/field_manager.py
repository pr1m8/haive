"""Field management for schema composition."""

import logging
from collections import defaultdict
from typing import Any, Callable, Dict, List, Optional, Type

from haive.core.schema.field_definition import FieldDefinition

logger = logging.getLogger(__name__)


class FieldManagerMixin:
    """Mixin that handles field management in SchemaComposer.

    This mixin provides:
    - Field definition storage and management
    - Field metadata tracking (sources, sharing, reducers)
    - Field validation and processing
    - Engine I/O field mapping
    """

    def __init__(self, *args, **kwargs):
        """Initialize field tracking structures."""
        super().__init__(*args, **kwargs)

        # Core field storage
        self.fields: Dict[str, FieldDefinition] = {}

        # Field metadata tracking
        self.shared_fields: set = set()
        self.field_sources: Dict[str, set] = defaultdict(set)
        self.nested_schemas: Dict[str, Type] = {}

        # Engine I/O tracking
        self.input_fields: Dict[str, set] = defaultdict(set)
        self.output_fields: Dict[str, set] = defaultdict(set)
        self.engine_io_mappings: Dict[str, Dict[str, List[str]]] = defaultdict(
            lambda: {"inputs": [], "outputs": []}
        )

        # Structured output tracking
        self.structured_models: Dict[str, Type] = {}
        self.structured_model_fields: Dict[str, List[str]] = defaultdict(list)

    def add_field(
        self,
        name: str,
        field_type: Type,
        default: Any = None,
        default_factory: Optional[Callable[[], Any]] = None,
        description: Optional[str] = None,
        shared: bool = False,
        reducer: Optional[Callable] = None,
        source: Optional[str] = None,
        input_for: Optional[List[str]] = None,
        output_from: Optional[List[str]] = None,
    ) -> "FieldManagerMixin":
        """Add a field definition to the schema.

        Args:
            name: Field name
            field_type: Type of the field
            default: Default value for the field
            default_factory: Optional factory function for creating default values
            description: Optional field description for documentation
            shared: Whether field is shared with parent graph
            reducer: Optional reducer function for merging field values
            source: Optional source identifier
            input_for: Optional list of engines this field is input for
            output_from: Optional list of engines this field is output from

        Returns:
            Self for method chaining
        """
        # Skip special fields
        if name == "__runnable_config__" or name == "runnable_config":
            logger.warning(f"Skipping special field {name}")
            return self

        # Validate field type
        if field_type is None:
            field_type = Any
        elif not isinstance(field_type, type) and not hasattr(field_type, "__origin__"):
            if isinstance(field_type, (dict, list, tuple)) and not hasattr(
                field_type, "__origin__"
            ):
                logger.warning(
                    f"Invalid field type for '{name}': {field_type}, using Any"
                )
                field_type = Any
            elif not hasattr(field_type, "__module__") or "typing" not in str(
                getattr(field_type, "__module__", "")
            ):
                logger.warning(
                    f"Invalid field type for '{name}': {field_type}, using Any"
                )
                field_type = Any

        # Check if field is provided by base class
        if hasattr(self, "detected_base_class") and hasattr(self, "base_class_fields"):
            if self.detected_base_class and name in self.base_class_fields:
                logger.debug(
                    f"Field '{name}' is provided by base class, updating metadata only"
                )

                # Still track metadata for the field
                if shared:
                    self.shared_fields.add(name)
                if source:
                    self.field_sources[name].add(source)
                if input_for:
                    for engine in input_for:
                        self.input_fields[engine].add(name)
                        if engine not in self.engine_io_mappings:
                            self.engine_io_mappings[engine] = {
                                "inputs": [],
                                "outputs": [],
                            }
                        if name not in self.engine_io_mappings[engine]["inputs"]:
                            self.engine_io_mappings[engine]["inputs"].append(name)
                if output_from:
                    for engine in output_from:
                        self.output_fields[engine].add(name)
                        if engine not in self.engine_io_mappings:
                            self.engine_io_mappings[engine] = {
                                "inputs": [],
                                "outputs": [],
                            }
                        if name not in self.engine_io_mappings[engine]["outputs"]:
                            self.engine_io_mappings[engine]["outputs"].append(name)

                return self

        # Create field definition
        field_def = FieldDefinition(
            name=name,
            field_type=field_type,
            default=default,
            default_factory=default_factory,
            description=description,
            shared=shared,
            reducer=reducer,
            input_for=input_for or [],
            output_from=output_from or [],
        )

        # Check for nested schemas
        import inspect
        from typing import Union

        from haive.core.schema.state_schema import StateSchema

        if inspect.isclass(field_type) and issubclass(field_type, StateSchema):
            logger.debug(f"Field '{name}' is a StateSchema type: {field_type.__name__}")
            self.nested_schemas[name] = field_type
        elif getattr(field_type, "__origin__", None) is Union and any(
            inspect.isclass(arg) and issubclass(arg, StateSchema)
            for arg in field_type.__args__
            if inspect.isclass(arg)
        ):
            # Handle Optional[StateSchema] and Union types containing StateSchema
            for arg in field_type.__args__:
                if inspect.isclass(arg) and issubclass(arg, StateSchema):
                    logger.debug(
                        f"Field '{name}' contains StateSchema type: {arg.__name__}"
                    )
                    self.nested_schemas[name] = arg
                    break

        # Update detection flags
        if name == "messages":
            self.has_messages = True
            logger.debug(
                "Added 'messages' field - will use MessagesState as base class"
            )

        if name == "tools":
            self.has_tools = True
            logger.debug("Added 'tools' field - will use ToolState as base class")

        # Store the field
        self.fields[name] = field_def

        # Track input/output relationships
        if input_for:
            for engine in input_for:
                self.input_fields[engine].add(name)
                if engine not in self.engine_io_mappings:
                    self.engine_io_mappings[engine] = {"inputs": [], "outputs": []}
                if name not in self.engine_io_mappings[engine]["inputs"]:
                    self.engine_io_mappings[engine]["inputs"].append(name)

        if output_from:
            for engine in output_from:
                self.output_fields[engine].add(name)
                if engine not in self.engine_io_mappings:
                    self.engine_io_mappings[engine] = {"inputs": [], "outputs": []}
                if name not in self.engine_io_mappings[engine]["outputs"]:
                    self.engine_io_mappings[engine]["outputs"].append(name)

        # Track additional metadata
        if shared:
            self.shared_fields.add(name)
            logger.debug(f"Marked field '{name}' as shared")

        if source:
            self.field_sources[name].add(source)
            logger.debug(f"Field '{name}' source: {source}")

        # Add tracking entry
        if hasattr(self, "processing_history"):
            self.processing_history.append(
                {
                    "action": "add_field",
                    "field_name": name,
                    "field_type": str(field_type),
                    "shared": shared,
                    "has_reducer": reducer is not None,
                }
            )

        logger.debug(f"Added field '{name}' of type {field_type}")
        return self

    def get_field_count(self) -> int:
        """Get the number of fields defined."""
        return len(self.fields)

    def has_field(self, name: str) -> bool:
        """Check if a field is defined."""
        return name in self.fields

    def get_field_names(self) -> List[str]:
        """Get list of all field names."""
        return list(self.fields.keys())

    def get_shared_fields(self) -> List[str]:
        """Get list of shared field names."""
        return list(self.shared_fields)

    def get_engine_io_mapping(self, engine_name: str) -> Dict[str, List[str]]:
        """Get input/output mapping for a specific engine."""
        return self.engine_io_mappings.get(engine_name, {"inputs": [], "outputs": []})
