"""Simplified SchemaComposer using modular mixins."""

import logging
from typing import Any, List, Type

from haive.core.schema.composer.engine.engine_detector import EngineDetectorMixin
from haive.core.schema.composer.engine.engine_manager import EngineComposerMixin
from haive.core.schema.composer.field.field_manager import FieldManagerMixin
from haive.core.schema.state_schema import StateSchema

logger = logging.getLogger(__name__)


class SchemaComposer(EngineComposerMixin, EngineDetectorMixin, FieldManagerMixin):
    """Streamlined schema composer using modular mixins.

    This is a much smaller, focused version of SchemaComposer that delegates
    most functionality to specialized mixins:

    - EngineComposerMixin: Engine management and tracking
    - EngineDetectorMixin: Base class detection from components
    - FieldManagerMixin: Field definition and metadata management

    The core class focuses only on:
    - Initialization and coordination
    - High-level composition workflows
    - Schema building and finalization
    """

    def __init__(self, name: str = "ComposedState"):
        """Initialize the schema composer.

        Args:
            name: Name for the generated schema class
        """
        self.name = name
        self.processing_history: List[dict] = []

        # Initialize all mixins
        super().__init__()

        logger.debug(f"SchemaComposer: {name}")

    def add_fields_from_components(self, components: List[Any]) -> "SchemaComposer":
        """Add fields from a list of components.

        Args:
            components: List of components to extract fields from

        Returns:
            Self for chaining
        """
        if not components:
            return self

        # Detect base class requirements from components
        self._detect_base_class_requirements(components)

        # Process each component
        for i, component in enumerate(components):
            if component is None:
                continue

            component_type = component.__class__.__name__
            component_id = getattr(component, "name", f"component_{i}")

            logger.debug(f"Processing component {i}: {component_id} ({component_type})")

            # Add tracking entry
            self.processing_history.append(
                {
                    "action": "process_component",
                    "component_type": component_type,
                    "component_id": component_id,
                }
            )

            # Process based on type
            if hasattr(component, "engine_type"):
                # It's an Engine
                logger.debug(f"Component {component_id} is an Engine")
                self.add_engine(component)
                self.add_fields_from_engine(component)

            elif hasattr(component, "model_fields"):
                # It's a Pydantic model
                logger.debug(f"Component {component_id} is a Pydantic model")
                self.add_fields_from_model(
                    component if isinstance(component, type) else component.__class__
                )

            elif isinstance(component, dict):
                # Dictionary
                logger.debug(f"Component {component_id} is a dictionary")
                self.add_fields_from_dict(component)

            else:
                logger.debug(f"Skipping unsupported component type: {component_type}")

        # Ensure standard fields are present
        self._ensure_standard_fields()

        return self

    def add_fields_from_engine(self, engine: Any) -> "SchemaComposer":
        """Extract fields from an engine component."""
        # This will be implemented by extracting from the original SchemaComposer
        # For now, just track that we processed it
        logger.debug(
            f"Would extract fields from engine: {getattr(engine, 'name', 'unnamed')}"
        )
        return self

    def add_fields_from_model(self, model: Type) -> "SchemaComposer":
        """Extract fields from a Pydantic model."""
        # This will be implemented by extracting from the original SchemaComposer
        logger.debug(f"Would extract fields from model: {model.__name__}")
        return self

    def add_fields_from_dict(self, fields_dict: dict) -> "SchemaComposer":
        """Add fields from a dictionary definition."""
        # This will be implemented by extracting from the original SchemaComposer
        logger.debug(f"Would add fields from dict with {len(fields_dict)} entries")
        return self

    def _ensure_standard_fields(self) -> None:
        """Ensure standard fields are present if needed."""
        # Add runnable_config if we have engines
        if (
            self.engines
            and "runnable_config" not in self.fields
            and "runnable_config" not in self.base_class_fields
        ):
            from typing import Dict, Optional

            self.add_field(
                name="runnable_config",
                field_type=Optional[Dict[str, Any]],
                default=None,
                description="Runtime configuration for engines",
                source="auto_added",
            )
            logger.debug("Added standard field 'runnable_config'")

    def build(self) -> Type[StateSchema]:
        """Build and return the final schema class.

        Returns:
            A StateSchema subclass with all defined fields and metadata
        """
        # Ensure base class is detected
        if self.detected_base_class is None:
            self._detect_base_class_requirements()

        base_class = self.detected_base_class

        # Auto-add engine management if we have engines and using StateSchema base
        if self.engines and issubclass(base_class, StateSchema):
            self.add_engine_management()
            logger.debug(
                "Auto-added engine management fields based on detected engines"
            )

        # Show what we're building
        logger.debug(
            f"Building {self.name} with {len(self.fields)} fields using base class {base_class.__name__}"
        )

        # Create field definitions for the model
        field_defs = {}
        for name, field_def in self.fields.items():
            # Skip fields that the base class provides
            if name in self.base_class_fields:
                logger.debug(f"Skipping field {name} - provided by base class")
                continue

            field_type, field_info = field_def.to_field_info()
            field_defs[name] = (field_type, field_info)

        # Create the schema using pydantic's create_model
        from pydantic import create_model

        schema = create_model(self.name, __base__=base_class, **field_defs)

        # Add StateSchema-specific attributes
        if issubclass(base_class, StateSchema):
            # Copy shared fields
            if hasattr(base_class, "__shared_fields__"):
                base_shared = set(getattr(base_class, "__shared_fields__", []))
                schema.__shared_fields__ = list(base_shared | self.shared_fields)
            else:
                schema.__shared_fields__ = list(self.shared_fields)

            # Add engine I/O mappings
            schema.__engine_io_mappings__ = dict(self.engine_io_mappings)

            # Store engines on the schema class
            schema.engines = self.engines
            schema.engines_by_type = dict(self.engines_by_type)

            logger.debug(f"Stored {len(schema.engines)} engines on schema class")

        return schema

    @classmethod
    def from_components(
        cls, components: List[Any], name: str = "ComposedState"
    ) -> Type[StateSchema]:
        """Create a schema from components using the class method interface.

        This maintains backward compatibility with the original API.

        Args:
            components: List of components to compose
            name: Name for the generated schema

        Returns:
            Generated schema class
        """
        composer = cls(name=name)
        composer.add_fields_from_components(components)
        return composer.build()
