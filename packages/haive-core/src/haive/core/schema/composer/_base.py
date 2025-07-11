from __future__ import annotations

import inspect
import logging
from collections import defaultdict
from typing import TYPE_CHECKING, Any, Callable, Dict, List, Optional, Set, Type

from pydantic import create_model

# Rich UI components for visualization and debugging
from rich.console import Console

from haive.core.schema.field_definition import FieldDefinition
from haive.core.schema.state_schema import StateSchema

if TYPE_CHECKING:
    from haive.core.engine.base import Engine

# Configure rich logging
logger = logging.getLogger(__name__)
console = Console()


class _SchemaComposerBase:
    """Base class for SchemaComposer, containing core __init__ and build logic."""

    name: str
    include_engine_fields: bool
    fields: Dict[str, FieldDefinition]
    shared_fields: Set[str]
    field_sources: Dict[str, Set[str]]
    input_fields: Dict[str, Set[str]]
    output_fields: Dict[str, Set[str]]
    engine_io_mappings: Dict[str, Dict[str, List[str]]]
    structured_models: Dict[str, Type]
    structured_model_fields: Dict[str, Set[str]]
    nested_schemas: Dict[str, Type[StateSchema]]
    has_tools: bool
    has_messages: bool
    engines: Dict[str, Any]
    engines_by_type: Dict[str, List[str]]
    detected_base_class: Optional[Type]
    custom_base_schema: bool
    base_class_fields: Set[str]
    processing_history: List[Dict[str, Any]]
    metadata: Dict[str, Any]

    def __init__(
        self,
        name: str = "ComposedSchema",
        base_state_schema: Optional[Type[StateSchema]] = None,
        include_engine_fields: bool = True,
    ):
        """Initialize a new SchemaComposer.

        Args:
            name: The name for the composed schema class. Defaults to "ComposedSchema".
            base_state_schema: Optional custom base schema to use. If not provided,
                             the composer will auto-detect the appropriate base class.
            include_engine_fields: Whether to include engine and engines fields in the schema.
                                 Set to False for projected schemas used in multi-agent execution.
        """
        self.name = name
        self.include_engine_fields = include_engine_fields
        self.fields = {}
        self.shared_fields = set()
        self.field_sources = defaultdict(set)

        # Track input/output mappings for engines
        self.input_fields = defaultdict(set)
        self.output_fields = defaultdict(set)
        self.engine_io_mappings = {}

        # Track structured models separately
        self.structured_models = {}
        self.structured_model_fields = defaultdict(set)

        # Track nested state schemas
        self.nested_schemas = {}

        # Track if we found tools or messages
        self.has_tools = False
        self.has_messages = False

        # Store engines for later reference and updates
        self.engines = {}  # name -> engine mapping
        self.engines_by_type = defaultdict(list)  # type -> [engine names]

        # Base class detection (determined early)
        self.detected_base_class = base_state_schema
        self.custom_base_schema = base_state_schema is not None
        self.base_class_fields = set()

        # If custom base schema provided, extract its fields
        if base_state_schema and hasattr(base_state_schema, "model_fields"):
            self.base_class_fields = set(base_state_schema.model_fields.keys())
            # Check if the base schema has messages or tools
            if "messages" in self.base_class_fields:
                self.has_messages = True
            if "tools" in self.base_class_fields:
                self.has_tools = True

        # Debug tracking
        self.processing_history = []

        # Metadata storage for compatibility analysis
        self.metadata = {}

        logger.debug(f"Created SchemaComposer for '{name}'")
        self._visualize_creation()

    def build(self) -> Type[StateSchema]:
        """Build and return a StateSchema class with all defined fields and metadata.

        This method finalizes the schema composition process by generating a concrete
        StateSchema subclass with the appropriate base class and all the fields,
        metadata, and behaviors defined during composition.

        Returns:
            A StateSchema subclass with all defined fields, metadata, and behaviors.
        """
        if self.detected_base_class is None:
            self._detect_base_class_requirements()

        base_class = self.detected_base_class
        if base_class is None:
            # Should not happen if _detect_base_class_requirements is called
            base_class = StateSchema

        # Auto-add engine management if we have engines and using StateSchema base
        if self.engines and issubclass(base_class, StateSchema):
            self.add_engine_management()
            logger.debug(
                "Auto-added engine management fields based on detected engines"
            )

        logger.debug(
            f"Building {self.name} with {len(self.fields)} fields using base class {base_class.__name__}"
        )

        field_defs = {}
        for name, field_def in self.fields.items():
            if "." in name:
                continue
            if name in self.base_class_fields:
                continue
            field_type, field_info = field_def.to_field_info()
            field_defs[name] = (field_type, field_info)

        schema = create_model(self.name, __base__=base_class, **field_defs)

        is_state_schema_base = issubclass(base_class, StateSchema)

        if is_state_schema_base:
            base_shared = set(getattr(base_class, "__shared_fields__", []))
            schema.__shared_fields__ = list(base_shared | self.shared_fields)
            logger.debug(f"Shared fields: {getattr(schema, '__shared_fields__', [])}")

            schema.__serializable_reducers__ = {}
            schema.__reducer_fields__ = {}
            if hasattr(base_class, "__serializable_reducers__"):
                schema.__serializable_reducers__.update(
                    getattr(base_class, "__serializable_reducers__", {})
                )
            if hasattr(base_class, "__reducer_fields__"):
                schema.__reducer_fields__.update(
                    getattr(base_class, "__reducer_fields__", {})
                )

            for name, field_def in self.fields.items():
                if field_def.reducer:
                    reducer_name = field_def.get_reducer_name()
                    schema.__serializable_reducers__[name] = reducer_name
                    schema.__reducer_fields__[name] = field_def.reducer

            schema.__engine_io_mappings__ = {
                k: v.copy() for k, v in self.engine_io_mappings.items()
            }
            schema.__input_fields__ = {k: list(v) for k, v in self.input_fields.items()}
            schema.__output_fields__ = {
                k: list(v) for k, v in self.output_fields.items()
            }

            if self.structured_model_fields:
                schema.__structured_model_fields__ = {
                    k: list(v) for k, v in self.structured_model_fields.items()
                }

            if self.structured_models:
                schema.__structured_models__ = {
                    k: f"{v.__module__}.{v.__name__}"
                    for k, v in self.structured_models.items()
                }

            schema.engines = self.engines
            schema.engines_by_type = dict(self.engines_by_type)
            if "engines" in schema.model_fields:
                schema.model_fields["engines"].default_factory = lambda cls=schema: (
                    cls.engines.copy() if hasattr(cls, "engines") else {}
                )

        tool_schemas = {}
        output_schemas = {}
        for name, field_def in self.fields.items():
            if "." in name:
                parts = name.split(".", 1)
                if parts[0] == "tool_schemas":
                    tool_schemas[parts[1]] = field_def.default
                elif parts[0] == "output_schemas":
                    output_schemas[parts[1]] = field_def.default

        def schema_post_init(self, __context):
            if hasattr(super(self.__class__, self), "model_post_init"):
                super(self.__class__, self).model_post_init(__context)

            if hasattr(self.__class__, "engines"):
                if hasattr(self, "engines") and not self.engines:
                    self.engines = {k: v for k, v in self.__class__.engines.items()}

            if hasattr(self.__class__, "engines") and hasattr(self, "tools"):
                if self.tools is None:
                    self.tools = []
                for engine in self.__class__.engines.values():
                    if hasattr(engine, "tools") and engine.tools:
                        existing_tool_names = [
                            getattr(t, "name", str(t)) for t in self.tools
                        ]
                        for tool in engine.tools:
                            tool_name = getattr(tool, "name", str(tool))
                            if tool_name not in existing_tool_names:
                                self.tools.append(tool)

            if hasattr(self, "tool_schemas") and tool_schemas:
                for name, schema_cls in tool_schemas.items():
                    self.tool_schemas[name] = schema_cls

            if hasattr(self, "output_schemas") and output_schemas:
                for name, schema_cls in output_schemas.items():
                    self.output_schemas[name] = schema_cls

        schema.model_post_init = schema_post_init

        if is_state_schema_base and logger.level <= logging.DEBUG:
            self._display_schema_summary(schema)

        return schema
