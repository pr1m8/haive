"""SchemaComposer for the Haive Schema System.

This module provides the SchemaComposer class, which offers a streamlined API for
building state schemas dynamically from various components. The SchemaComposer is
designed for schema composition, enabling the creation of complex state schemas by
combining fields from multiple sources.

The SchemaComposer is particularly useful for:
- Building schemas from heterogeneous components (engines, models, dictionaries)
- Dynamically creating schemas at runtime based on available components
- Composing schemas with proper field sharing, reducers, and engine I/O mappings
- Ensuring consistent state handling across complex agent architectures

Key features include:
- Automatic field extraction from components
- Field definition management with comprehensive metadata
- Support for shared fields between parent and child graphs
- Tracking of engine input/output relationships
- Integration with structured output models
- Rich visualization for debugging and analysis

Example:
    ```python
    from haive.core.schema import SchemaComposer
    from typing import List
    from langchain_core.messages import BaseMessage
    from pydantic import Field
    import operator

    # Create a new composer
    composer = SchemaComposer(name="ConversationState")

    # Add fields manually
    composer.add_field(
        name="messages",
        field_type=List[BaseMessage],
        default_factory=list,
        description="Conversation history",
        shared=True,
        reducer="add_messages"
    )

    composer.add_field(
        name="context",
        field_type=List[str],
        default_factory=list,
        description="Retrieved document contexts",
        reducer=operator.add
    )

    # Extract fields from components
    composer.add_fields_from_components([
        retriever_engine,
        llm_engine,
        memory_component
    ])

    # Build the schema
    ConversationState = composer.build()

    # Use the schema
    state = ConversationState()
    ```
"""

from __future__ import annotations

import inspect
import logging
import sys
from collections import defaultdict
from typing import TYPE_CHECKING, Any, Callable, Dict, List, Optional, Type, Union

from langchain_core.tools import BaseTool
from pydantic import BaseModel, create_model

# Rich UI components for visualization and debugging
from rich.console import Console
from rich.logging import RichHandler
from rich.table import Table
from rich.tree import Tree

from haive.core.schema.field_definition import FieldDefinition
from haive.core.schema.state_schema import StateSchema

if TYPE_CHECKING:
    from haive.core.schema.schema_manager import StateSchemaManager

# Configure rich logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)],
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)
console = Console()


class SchemaComposer:
    """Utility for building state schemas dynamically from component fields.

    The SchemaComposer provides a high-level, builder-style API for creating state
    schemas by combining fields from various sources. It handles the complex details
    of field extraction, metadata management, and schema generation, providing a
    streamlined interface for schema composition.

    Key capabilities include:
    - Dynamically extracting fields from components (engines, models, dictionaries)
    - Adding and configuring fields individually with comprehensive options
    - Tracking field relationships, shared status, and reducer functions
    - Managing engine I/O mappings for proper state handling
    - Building optimized schema classes with the right configuration
    - Supporting nested state schemas and structured output models
    - Providing rich visualization for debugging and analysis

    This class is the primary builder interface for dynamic schema creation in the
    Haive Schema System, offering a more declarative approach than StateSchemaManager.
    It's particularly useful for creating schemas at runtime based on available
    components, ensuring consistent state handling across complex agent architectures.

    SchemaComposer is designed to be used either directly or through class methods
    like from_components() for simplified schema creation from a list of components.
    """

    def __init__(
        self,
        name: str = "ComposedSchema",
        base_state_schema: Optional[Type[StateSchema]] = None,
    ):
        """Initialize a new SchemaComposer.

        Args:
            name: The name for the composed schema class. Defaults to "ComposedSchema".
            base_state_schema: Optional custom base state schema to use. If not provided,
                             the composer will auto-detect the appropriate base class.

        Example:
            Creating a schema composer for a conversational agent::

                composer = SchemaComposer(name="ConversationState")
                composer.add_field("messages", List[BaseMessage], default_factory=list)
                schema_class = composer.build()

            Using a custom base schema::

                from haive.core.schema.prebuilt import MessagesStateWithTokenUsage
                composer = SchemaComposer(
                    name="TokenAwareState",
                    base_state_schema=MessagesStateWithTokenUsage
                )
        """
        self.name = name
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

    def _visualize_creation(self):
        """Display creation information using Rich."""
        tree = Tree(
            f"[bold green]SchemaComposer[/bold green]: [blue]{self.name}[/blue]"
        )
        tree.add("[yellow]Ready to compose schema[/yellow]")
        console.print(tree)

    def _detect_base_class_requirements(
        self, components: Optional[List[Any]] = None
    ) -> None:
        """
        Detect which base class should be used based on components and current fields.
        Must be called before adding fields to avoid duplicates.

        Priority order:
        1. Use custom base schema if provided
        2. Check for AugLLM engines and agents first
        3. Check for tools
        4. Check for messages (use token-aware version)
        5. Default to StateSchema
        """
        logger.debug("Detecting base class requirements")

        # If custom base schema was provided, skip detection
        if self.custom_base_schema:
            logger.debug(
                f"Using custom base schema: {self.detected_base_class.__name__}"
            )
            return

        # Check current fields first
        if "messages" in self.fields or self.has_messages:
            self.has_messages = True

        if "tools" in self.fields or self.has_tools:
            self.has_tools = True

        # Enhanced component analysis - prioritize engine type detection
        if components:
            for component in components:
                if component is None:
                    continue

                # PRIORITY 1: Check for AugLLM engines specifically
                if hasattr(component, "engine_type"):
                    engine_type_value = getattr(
                        component.engine_type, "value", component.engine_type
                    )
                    engine_type_str = str(engine_type_value).lower()

                    if engine_type_str == "llm":
                        logger.debug(
                            f"Found AugLLM engine: {getattr(component, 'name', 'unnamed')}"
                        )
                        self.has_messages = True

                        # Check if this AugLLM has tools
                        if hasattr(component, "tools") and component.tools:
                            logger.debug("AugLLM has tools - will use ToolState")
                            self.has_tools = True

                # PRIORITY 2: Check for agent-like components
                elif hasattr(component, "agent") or getattr(
                    component, "__class__", None
                ).__name__.lower().endswith("agent"):
                    logger.debug(
                        f"Found agent component: {getattr(component, 'name', getattr(component, '__class__', {}).get('__name__', 'unnamed'))}"
                    )
                    self.has_messages = True

                    # Check if agent has tools
                    if hasattr(component, "tools") and component.tools:
                        logger.debug("Agent has tools - will use ToolState")
                        self.has_tools = True

                # PRIORITY 3: Check for standalone tools
                elif hasattr(component, "tools") and component.tools:
                    logger.debug("Found component with tools")
                    self.has_tools = True

                # PRIORITY 4: Check for messages in engine I/O
                if hasattr(component, "get_input_fields") and callable(
                    component.get_input_fields
                ):
                    try:
                        input_fields = component.get_input_fields()
                        if "messages" in input_fields:
                            self.has_messages = True
                            logger.debug("Found 'messages' in input fields")
                    except Exception:
                        pass

                if hasattr(component, "get_output_fields") and callable(
                    component.get_output_fields
                ):
                    try:
                        output_fields = component.get_output_fields()
                        if "messages" in output_fields:
                            self.has_messages = True
                            logger.debug("Found 'messages' in output fields")
                    except Exception:
                        pass

        # Determine base class with proper priority
        # NEW LOGIC: Always use LLMState as foundation for LLM engines
        has_llm_engine = False

        # Check for LLM engines in components or current engines
        if components:
            for component in components:
                if component is None:
                    continue
                if hasattr(component, "engine_type"):
                    engine_type_value = getattr(
                        component.engine_type, "value", component.engine_type
                    )
                    engine_type_str = str(engine_type_value).lower()
                    if engine_type_str == "llm":
                        has_llm_engine = True
                        break

        # Also check current engines
        for engine_name in self.engines_by_type.get("llm", []):
            has_llm_engine = True
            break

        # Priority: LLMState for LLM engines (includes messages + tools + token tracking)
        if has_llm_engine:
            from haive.core.schema.prebuilt.llm_state import LLMState

            base_class = LLMState
            logger.debug(
                "Using LLMState as base class (found LLM engine - includes messages, tools, and token tracking)"
            )
        elif self.has_tools:
            from haive.core.schema.prebuilt.tool_state import ToolState

            base_class = ToolState
            logger.debug("Using ToolState as base class (found tools without LLM)")
        elif self.has_messages:
            # Use token-aware messages state for better tracking
            from haive.core.schema.prebuilt.messages.messages_with_token_usage import (
                MessagesStateWithTokenUsage,
            )

            base_class = MessagesStateWithTokenUsage
            logger.debug(
                "Using MessagesStateWithTokenUsage as base class (found messages without LLM/tools)"
            )
        else:
            from haive.core.schema.state_schema import StateSchema

            base_class = StateSchema
            logger.debug("Using StateSchema as base class (default)")

        self.detected_base_class = base_class

        # Extract fields from base class to avoid duplicates
        if hasattr(base_class, "model_fields"):
            self.base_class_fields = set(base_class.model_fields.keys())
            logger.debug(f"Base class provides fields: {self.base_class_fields}")
        else:
            self.base_class_fields = set()

    def add_engine(self, engine: Any) -> "SchemaComposer":
        """
        Add an engine to the composer for tracking and later updates.

        Args:
            engine: Engine to add

        Returns:
            Self for chaining
        """
        if engine is None:
            return self

        # Get engine name and type
        engine_name = getattr(engine, "name", f"engine_{id(engine)}")
        engine_type = getattr(engine, "engine_type", None)

        # Store engine
        self.engines[engine_name] = engine

        # Track by type if available - avoid duplicates
        if engine_type:
            engine_type_str = (
                engine_type.value if hasattr(engine_type, "value") else str(engine_type)
            )
            # Only add if not already in the list (avoid duplicates)
            if engine_name not in self.engines_by_type[engine_type_str]:
                self.engines_by_type[engine_type_str].append(engine_name)
                logger.debug(
                    f"Added engine '{engine_name}' of type '{engine_type_str}'"
                )
            else:
                logger.debug(
                    f"Engine '{engine_name}' already exists in engines_by_type for type '{engine_type_str}'"
                )

        # Add tracking entry
        self.processing_history.append(
            {
                "action": "add_engine",
                "engine_name": engine_name,
                "engine_type": engine_type,
            }
        )

        return self

    def resolve_engine_types(self) -> Dict[str, type]:
        """Resolve engine types from added engines for generic typing.

        Returns:
            Dictionary mapping engine names to their concrete types
        """
        resolved_types = {}

        for engine_name, engine in self.engines.items():
            if engine is not None:
                resolved_types[engine_name] = type(engine)
                logger.debug(
                    f"Resolved engine '{engine_name}' to type {type(engine).__name__}"
                )

        return resolved_types

    def get_engine_union_type(self):
        """Get a Union type of all concrete engine types."""
        from typing import Union

        from haive.core.engine.base import Engine

        resolved_types = self.resolve_engine_types()
        unique_types = list(set(resolved_types.values()))

        if not unique_types:
            return Engine  # Fallback to base Engine type
        elif len(unique_types) == 1:
            return unique_types[0]
        else:
            return Union[tuple(unique_types)]

    def build_with_engine_generics(self, name: str = None) -> Type[StateSchema]:
        """Build a StateSchema with resolved engine generics.

        Args:
            name: Optional name for the schema class

        Returns:
            StateSchema class with concrete engine types
        """
        from typing import Dict

        from haive.core.schema.state_schema import StateSchema

        # Resolve engine types
        engine_union_type = self.get_engine_union_type()
        engines_dict_type = Dict[str, engine_union_type]

        # Build the schema with generic resolution
        schema_class = self.build()

        # Create a concrete version with resolved generics
        class_name = name or f"{schema_class.__name__}WithResolvedEngines"

        # Create type annotations for the resolved schema
        resolved_annotations = {
            "engine": Optional[engine_union_type],
            "engines": engines_dict_type,
        }

        # Add existing field annotations
        if hasattr(schema_class, "__annotations__"):
            resolved_annotations.update(schema_class.__annotations__)

        # Create the resolved schema class
        resolved_schema = type(
            class_name,
            (schema_class,),
            {
                "__annotations__": resolved_annotations,
                "__module__": schema_class.__module__,
            },
        )

        logger.debug(f"Built schema with resolved engine generics: {class_name}")
        logger.debug(f"Engine type: {engine_union_type}")
        logger.debug(f"Engines type: {engines_dict_type}")

        return resolved_schema

    def update_engine_provider(
        self, engine_type: str, updates: Dict[str, Any]
    ) -> "SchemaComposer":
        """
        Update configuration for all engines of a specific type.

        Args:
            engine_type: Type of engines to update (e.g., "llm", "retriever")
            updates: Dictionary of updates to apply

        Returns:
            Self for chaining
        """
        logger.debug(f"Updating all {engine_type} engines with: {updates}")

        updated_count = 0
        for engine_name in self.engines_by_type.get(engine_type, []):
            if engine_name in self.engines:
                engine = self.engines[engine_name]

                # For LLM engines, update llm_config field
                if engine_type == "llm" and hasattr(engine, "llm_config"):
                    for key, value in updates.items():
                        if hasattr(engine.llm_config, key):
                            setattr(engine.llm_config, key, value)
                            logger.debug(
                                f"Updated {engine_name}.llm_config.{key} = {value}"
                            )
                            updated_count += 1

                # For other engine types, update directly
                else:
                    for key, value in updates.items():
                        if hasattr(engine, key):
                            setattr(engine, key, value)
                            logger.debug(f"Updated {engine_name}.{key} = {value}")
                            updated_count += 1

        logger.info(
            f"Updated {updated_count} fields across {len(self.engines_by_type.get(engine_type, []))} {engine_type} engines"
        )

        # Add tracking entry
        self.processing_history.append(
            {
                "action": "update_engine_provider",
                "engine_type": engine_type,
                "updates": updates,
                "affected_engines": updated_count,
            }
        )

        return self

    def get_engines_by_type(self, engine_type: str) -> List[Any]:
        """
        Get all engines of a specific type.

        Args:
            engine_type: Type of engines to retrieve

        Returns:
            List of engines of the specified type
        """
        engine_names = self.engines_by_type.get(engine_type, [])
        return [self.engines[name] for name in engine_names if name in self.engines]

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
    ) -> "SchemaComposer":
        """Add a field definition to the schema.

        This method adds a field to the schema being composed, with comprehensive
        configuration for type, default values, sharing behavior, reducer functions,
        and engine I/O relationships. It handles special cases like fields provided
        by the base class and nested StateSchema fields.

        The method performs validation on the field type and ensures proper tracking
        of metadata for schema generation. It's the core building block for schema
        composition, allowing fine-grained control over field properties.

        Args:
            name: Field name
            field_type: Type of the field (e.g., str, List[int], Optional[Dict[str, Any]])
            default: Default value for the field
            default_factory: Optional factory function for creating default values
            description: Optional field description for documentation
            shared: Whether field is shared with parent graph (enables state synchronization)
            reducer: Optional reducer function for merging field values during state updates
            source: Optional source identifier (component or module name)
            input_for: Optional list of engines this field is input for
            output_from: Optional list of engines this field is output from

        Returns:
            Self for method chaining to enable fluent API style

        Example:
            ```python
            composer = SchemaComposer(name="MyState")
            composer.add_field(
                name="messages",
                field_type=List[BaseMessage],
                default_factory=list,
                description="Conversation history",
                shared=True,
                reducer=add_messages,
                input_for=["memory_engine"],
                output_from=["llm_engine"]
            )
            ```
        """
        # Skip special fields
        if name == "__runnable_config__" or name == "runnable_config":
            logger.warning(f"Skipping special field {name}")
            return self

        # Ensure field_type is a valid type
        if field_type is None:
            field_type = Any
        elif not isinstance(field_type, type) and not hasattr(field_type, "__origin__"):
            # Handle non-type values (like from tuple unpacking or invalid inputs)
            if isinstance(field_type, (dict, list, tuple)) and not hasattr(
                field_type, "__origin__"
            ):
                logger.warning(
                    f"Invalid field type for '{name}': {field_type}, using Any"
                )
                field_type = Any
            # Allow typing constructs like Union, Optional, etc.
            elif not hasattr(field_type, "__module__") or "typing" not in str(
                getattr(field_type, "__module__", "")
            ):
                logger.warning(
                    f"Invalid field type for '{name}': {field_type}, using Any"
                )
                field_type = Any

        # Check if field is provided by base class
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

        # Check if field is a StateSchema type - mark for special handling
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

        # Check if we're adding messages field
        if name == "messages":
            self.has_messages = True
            logger.debug(
                "Added 'messages' field - will use MessagesState as base class"
            )

        # Check if we're adding tools field
        if name == "tools":
            self.has_tools = True
            logger.debug("Added 'tools' field - will use ToolState as base class")

        # Store the field
        self.fields[name] = field_def

        # Track input/output relationships
        if input_for:
            for engine in input_for:
                self.input_fields[engine].add(name)
                # Make sure engine io mapping exists
                if engine not in self.engine_io_mappings:
                    self.engine_io_mappings[engine] = {"inputs": [], "outputs": []}
                # Add to inputs list if not already there
                if name not in self.engine_io_mappings[engine]["inputs"]:
                    self.engine_io_mappings[engine]["inputs"].append(name)

        if output_from:
            for engine in output_from:
                self.output_fields[engine].add(name)
                # Make sure engine io mapping exists
                if engine not in self.engine_io_mappings:
                    self.engine_io_mappings[engine] = {"inputs": [], "outputs": []}
                # Add to outputs list if not already there
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

    def add_standard_field(self, field_name: str, **kwargs) -> "SchemaComposer":
        """Add a standard field from the field registry.

        Args:
            field_name: Name of the standard field (e.g., 'messages', 'context')
            **kwargs: Additional arguments to pass to the field factory

        Returns:
            Self for chaining
        """
        from haive.core.schema.field_registry import StandardFields

        # Get the field factory method
        field_method = getattr(StandardFields, field_name, None)
        if not field_method:
            raise ValueError(f"Unknown standard field: {field_name}")

        # Get the field definition
        field_def = field_method(**kwargs)

        # Get metadata but filter out unsupported keys
        metadata = getattr(field_def, "metadata", {})
        supported_metadata = {}

        # Only pass metadata that add_field supports
        for key, value in metadata.items():
            if key in ["input_for", "output_from", "source"]:
                supported_metadata[key] = value

        # Add using the field definition
        self.add_field(
            name=field_def.name,
            field_type=field_def.field_type,
            default=field_def.default,
            default_factory=field_def.default_factory,
            description=field_def.description,
            shared=getattr(field_def, "shared", False),
            reducer=getattr(field_def, "reducer", None),
            **supported_metadata,
        )

        return self

    def add_fields_from_dict(self, fields_dict: Dict[str, Any]) -> "SchemaComposer":
        """
        Add fields from a dictionary definition.

        Args:
            fields_dict: Dictionary mapping field names to type/value information

        Returns:
            Self for chaining
        """
        logger.debug(f"Adding fields from dictionary with {len(fields_dict)} entries")

        for field_name, field_info in fields_dict.items():
            # Skip special fields
            if field_name == "__runnable_config__" or field_name == "runnable_config":
                logger.warning(f"Skipping special field {field_name}")
                continue

            # Handle different field info formats
            if isinstance(field_info, tuple) and len(field_info) >= 2:
                # (type, default) format
                field_type, default = field_info[0], field_info[1]

                # Look for extra params in a third item
                description = None
                shared = False
                reducer = None
                if len(field_info) >= 3 and isinstance(field_info[2], dict):
                    extra_params = field_info[2]
                    description = extra_params.get("description")
                    shared = extra_params.get("shared", False)
                    reducer = extra_params.get("reducer")

                # Add the field
                self.add_field(
                    name=field_name,
                    field_type=field_type,
                    default=default,
                    description=description,
                    shared=shared,
                    reducer=reducer,
                    source="dict",
                )
                logger.debug(f"Added field '{field_name}' from dict tuple format")

            elif isinstance(field_info, dict) and "type" in field_info:
                # Dictionary with type key
                field_type = field_info.pop("type")
                default = field_info.pop("default", None)
                default_factory = field_info.pop("default_factory", None)
                description = field_info.pop("description", None)
                shared = field_info.pop("shared", False)
                reducer = field_info.pop("reducer", None)

                # Add the field
                self.add_field(
                    name=field_name,
                    field_type=field_type,
                    default=default,
                    default_factory=default_factory,
                    description=description,
                    shared=shared,
                    reducer=reducer,
                    source="dict",
                )
                logger.debug(f"Added field '{field_name}' from dict with type key")

            else:
                # Assume it's a type with no default
                # Ensure it's a valid type for add_field
                if not isinstance(field_info, type) and not hasattr(
                    field_info, "__origin__"
                ):
                    logger.warning(
                        f"Unexpected field_info type for '{field_name}': {type(field_info)}, using Any"
                    )
                    field_info = Any

                self.add_field(
                    name=field_name, field_type=field_info, default=None, source="dict"
                )
                logger.debug(
                    f"Added field '{field_name}' from dict with type-only format"
                )

        return self

    def add_fields_from_model(self, model: Type[BaseModel]) -> "SchemaComposer":
        """
        Extract fields from a Pydantic model with improved handling of nested schemas.

        Args:
            model: Pydantic model to extract fields from

        Returns:
            Self for chaining
        """
        source = model.__name__
        logger.debug(f"Extracting fields from model: {source}")

        # Keep track of field metadata for schema
        shared_fields = []
        reducers = {}
        engine_io = {}

        # Check if model is a StateSchema
        is_state_schema = inspect.isclass(model) and issubclass(model, StateSchema)

        if is_state_schema:
            logger.debug(f"Model {source} is a StateSchema - will extract metadata")

            # Extract shared fields
            if hasattr(model, "__shared_fields__"):
                shared_fields = getattr(model, "__shared_fields__", [])
                logger.debug(f"Found shared fields: {shared_fields}")

            # Extract reducer info
            if hasattr(model, "__serializable_reducers__"):
                reducers = getattr(model, "__serializable_reducers__", {})
                logger.debug(f"Found reducers: {reducers}")

            # Extract engine IO mappings
            if hasattr(model, "__engine_io_mappings__"):
                engine_io = getattr(model, "__engine_io_mappings__", {})
                logger.debug(f"Found engine IO mappings: {len(engine_io)} engines")

                # Update our engine mappings
                for engine_name, mapping in engine_io.items():
                    if engine_name not in self.engine_io_mappings:
                        self.engine_io_mappings[engine_name] = {
                            "inputs": [],
                            "outputs": [],
                        }

                    # Add inputs
                    for field_name in mapping.get("inputs", []):
                        if (
                            field_name
                            not in self.engine_io_mappings[engine_name]["inputs"]
                        ):
                            self.engine_io_mappings[engine_name]["inputs"].append(
                                field_name
                            )
                            self.input_fields[engine_name].add(field_name)

                    # Add outputs
                    for field_name in mapping.get("outputs", []):
                        if (
                            field_name
                            not in self.engine_io_mappings[engine_name]["outputs"]
                        ):
                            self.engine_io_mappings[engine_name]["outputs"].append(
                                field_name
                            )
                            self.output_fields[engine_name].add(field_name)

        # Extract fields based on Pydantic version
        if hasattr(model, "model_fields"):
            # Pydantic v2
            logger.debug(
                f"Processing Pydantic v2 model: {len(model.model_fields)} fields"
            )

            for field_name, field_info in model.model_fields.items():
                # Skip special fields and private fields
                if field_name.startswith("__") or field_name.startswith("_"):
                    continue

                # Get field type and defaults
                field_type = field_info.annotation

                # Ensure we have a valid type
                if field_type is None:
                    field_type = Any

                # Handle default vs default_factory
                if field_info.default_factory is not None:
                    # Ensure default_factory is callable
                    if callable(field_info.default_factory):
                        default_factory = field_info.default_factory
                        default = None
                    else:
                        logger.warning(
                            f"Invalid default_factory for field '{field_name}', ignoring"
                        )
                        default_factory = None
                        default = field_info.default
                else:
                    default_factory = None
                    default = field_info.default

                # Check if this field is shared
                is_shared = field_name in shared_fields if is_state_schema else False

                # Check if this field has a reducer
                reducer_name = reducers.get(field_name)
                reducer = None
                if reducer_name:
                    try:
                        # Try to resolve the reducer from common places
                        if reducer_name == "add_messages":
                            from langgraph.graph import add_messages

                            reducer = add_messages
                        elif reducer_name.startswith("operator."):
                            import operator

                            op_name = reducer_name.split(".", 1)[1]
                            reducer = getattr(operator, op_name, None)
                        logger.debug(
                            f"Resolved reducer '{reducer_name}' for field '{field_name}'"
                        )
                    except ImportError:
                        logger.warning(f"Could not import reducer {reducer_name}")

                # Check if field is a nested StateSchema
                if inspect.isclass(field_type) and issubclass(field_type, StateSchema):
                    logger.debug(
                        f"Field '{field_name}' is a StateSchema: {field_type.__name__}"
                    )
                    self.nested_schemas[field_name] = field_type

                # Get input/output information
                input_for = []
                output_from = []
                for engine_name, mapping in engine_io.items():
                    if field_name in mapping.get("inputs", []):
                        input_for.append(engine_name)
                    if field_name in mapping.get("outputs", []):
                        output_from.append(engine_name)

                # Add the field
                self.add_field(
                    name=field_name,
                    field_type=field_type,
                    default=default,
                    default_factory=default_factory,
                    description=field_info.description,
                    shared=is_shared,
                    reducer=reducer,
                    source=source,
                    input_for=input_for,
                    output_from=output_from,
                )

        # If a StateSchema, check for structured_models
        if is_state_schema and hasattr(model, "__structured_models__"):
            structured_models_dict = getattr(model, "__structured_models__", {})
            for model_name, model_path in structured_models_dict.items():
                logger.debug(f"Found structured model: {model_name} -> {model_path}")

                # Try to import the model
                try:
                    module_path, class_name = model_path.rsplit(".", 1)
                    module = __import__(module_path, fromlist=[class_name])
                    structured_model = getattr(module, class_name)

                    # Add to our structured models
                    self.structured_models[model_name] = structured_model

                    # Get field names if available
                    if hasattr(model, "__structured_model_fields__"):
                        structured_model_fields_dict = getattr(
                            model, "__structured_model_fields__", {}
                        )
                        if model_name in structured_model_fields_dict:
                            fields = structured_model_fields_dict[model_name]
                            for field in fields:
                                self.structured_model_fields[model_name].add(field)

                    logger.debug(
                        f"Imported structured model {model_name}: {structured_model.__name__}"
                    )
                except (ImportError, AttributeError, ValueError) as e:
                    logger.warning(
                        f"Could not import structured model {model_name}: {e}"
                    )

        return self

    def add_fields_from_engine(self, engine: Any) -> "SchemaComposer":
        """
        Extract fields from an Engine object with enhanced nested schema handling.

        Args:
            engine: Engine to extract fields from

        Returns:
            Self for chaining
        """
        source = getattr(engine, "name", str(engine))
        logger.debug(f"Extracting fields from engine: {source}")

        # Add the engine for tracking
        self.add_engine(engine)

        # Add tracking entry
        self.processing_history.append(
            {"action": "add_fields_from_engine", "engine": source}
        )

        # Get engine name for tracking
        engine_name = getattr(engine, "name", str(engine))

        # Initialize engine IO mapping
        if engine_name not in self.engine_io_mappings:
            self.engine_io_mappings[engine_name] = {"inputs": [], "outputs": []}

        # Check if it's an AugLLM engine
        is_aug_llm = (
            hasattr(engine, "engine_type")
            and str(getattr(engine.engine_type, "value", engine.engine_type)).lower()
            == "llm"
        )

        # Determine output behavior for AugLLM
        aug_llm_output_field = None
        has_structured_output = False

        if is_aug_llm:
            # Check for structured output model
            has_structured_output = (
                hasattr(engine, "structured_output_model")
                and engine.structured_output_model is not None
            )

            # Check for explicit output field configuration
            if hasattr(engine, "output_field_name") and engine.output_field_name:
                aug_llm_output_field = engine.output_field_name
                logger.debug(
                    f"AugLLM {engine_name} has explicit output field: {aug_llm_output_field}"
                )
            elif not has_structured_output:
                # Default to messages for conversational agents without structured output
                aug_llm_output_field = "messages"
                logger.debug(
                    f"AugLLM {engine_name} defaulting output to 'messages' field"
                )

        # Process steps:
        # 1. First, check for input/output schemas
        # 2. Then check for structured output model
        # 3. Fall back to get_input_fields/get_output_fields methods
        # 4. Handle tools

        # 1. Check for input/output schema properties or methods
        input_schema = None
        output_schema = None

        # 1.1 Try to get input schema
        if hasattr(engine, "input_schema") and isinstance(
            engine.input_schema, BaseModel
        ):
            input_schema = engine.input_schema
            logger.debug(f"Using input_schema from engine: {input_schema.__name__}")
        elif hasattr(engine, "derive_input_schema") and callable(
            engine.derive_input_schema
        ):
            try:
                input_schema = engine.derive_input_schema()
                logger.debug(f"Using derived input schema: {input_schema.__name__}")
            except Exception as e:
                logger.warning(f"Error deriving input schema from {engine_name}: {e}")

        # 1.2 Try to get output schema (but respect AugLLM behavior)
        if not is_aug_llm or has_structured_output:
            if hasattr(engine, "output_schema") and isinstance(
                engine.output_schema, BaseModel
            ):
                output_schema = engine.output_schema
                logger.debug(
                    f"Using output_schema from engine: {output_schema.__name__}"
                )
            elif hasattr(engine, "derive_output_schema") and callable(
                engine.derive_output_schema
            ):
                try:
                    output_schema = engine.derive_output_schema()
                    logger.debug(
                        f"Using derived output schema: {output_schema.__name__}"
                    )
                except Exception as e:
                    logger.warning(
                        f"Error deriving output schema from {engine_name}: {e}"
                    )

        # 1.3 Process input schema if found
        if input_schema and not isinstance(input_schema, dict):
            logger.debug(f"Processing input schema for {engine_name}")

            # Extract fields from the schema
            self.add_fields_from_model(input_schema)

            # Mark fields as inputs for this engine
            if hasattr(input_schema, "model_fields"):
                for field_name in input_schema.model_fields:
                    if (
                        field_name not in self.fields
                        and field_name not in self.base_class_fields
                    ):
                        logger.warning(
                            f"Field {field_name} from {engine_name} input schema not found in fields"
                        )
                        continue

                    # Add to input fields
                    self.input_fields[engine_name].add(field_name)

                    # Add to engine IO mapping
                    if field_name not in self.engine_io_mappings[engine_name]["inputs"]:
                        self.engine_io_mappings[engine_name]["inputs"].append(
                            field_name
                        )
                        logger.debug(
                            f"Marked field '{field_name}' as input for engine '{engine_name}'"
                        )

        # 1.4 Process output schema if found (skip for AugLLM without structured output)
        if (
            output_schema
            and not isinstance(output_schema, dict)
            and (not is_aug_llm or has_structured_output)
        ):
            logger.debug(f"Processing output schema for {engine_name}")

            # Extract fields from the schema
            self.add_fields_from_model(output_schema)

            # Mark fields as outputs for this engine
            if hasattr(output_schema, "model_fields"):
                for field_name in output_schema.model_fields:
                    if (
                        field_name not in self.fields
                        and field_name not in self.base_class_fields
                    ):
                        logger.warning(
                            f"Field {field_name} from {engine_name} output schema not found in fields"
                        )
                        continue

                    # Add to output fields
                    self.output_fields[engine_name].add(field_name)

                    # Add to engine IO mapping
                    if (
                        field_name
                        not in self.engine_io_mappings[engine_name]["outputs"]
                    ):
                        self.engine_io_mappings[engine_name]["outputs"].append(
                            field_name
                        )
                        logger.debug(
                            f"Marked field '{field_name}' as output for engine '{engine_name}'"
                        )

        # 2. Process structured output model if available
        if has_structured_output and hasattr(engine, "structured_output_model"):
            model = engine.structured_output_model

            # Use proper field naming utilities
            from haive.core.schema.field_utils import get_field_info_from_model

            field_info_dict = get_field_info_from_model(model)
            model_name = field_info_dict["field_name"]

            logger.debug(
                f"Found structured_output_model in {source}: {model.__name__} -> {model_name}"
            )

            # Store structured model
            self.structured_models[model_name] = model

            # Track model fields for reference
            if hasattr(model, "model_fields"):
                for field_name in model.model_fields:
                    self.structured_model_fields[model_name].add(field_name)

                logger.debug(
                    f"Added {len(model.model_fields)} fields to structured_model_fields for {model_name}"
                )

            # Add a single field for the entire model
            if (
                model_name not in self.fields
                and model_name not in self.base_class_fields
            ):
                from typing import Optional

                field_type = Optional[model]
                if engine.structured_output_version == "v1":

                    self.add_field(
                        name=model_name,
                        field_type=field_type,
                        default=None,
                        description=f"Output in {model.__name__} format",
                        source=f"{source}.structured_output_model",
                        output_from=[engine_name],
                    )
                else:
                    self.add_field(
                        name=model_name,
                        field_type=field_type,
                        default=None,
                        description=f"Output in {model.__name__} format",
                        # source=f"{source}.structured_output_model",
                        # output_from=[engine_name],
                    )
                    self.engine_io_mappings[engine_name]["outputs"].append("messages")

                logger.debug(f"Added field '{model_name}' for structured output model")

        # 3. Use get_input_fields/get_output_fields methods if needed

        # 3.1 Extract input fields if needed
        if (
            not input_schema
            and hasattr(engine, "get_input_fields")
            and callable(engine.get_input_fields)
        ):
            try:
                input_fields = engine.get_input_fields()
                logger.debug(
                    f"Engine {engine_name} has {len(input_fields)} input fields from get_input_fields()"
                )

                for field_name, (field_type, field_info) in input_fields.items():
                    # Skip if already has this field or in base class
                    if (
                        field_name in self.fields
                        or field_name in self.base_class_fields
                    ):
                        # Just mark as input if it exists
                        self.input_fields[engine_name].add(field_name)
                        if (
                            field_name
                            not in self.engine_io_mappings[engine_name]["inputs"]
                        ):
                            self.engine_io_mappings[engine_name]["inputs"].append(
                                field_name
                            )
                        logger.debug(
                            f"Field '{field_name}' already exists, marked as input for '{engine_name}'"
                        )
                        continue

                    # Skip special fields
                    if (
                        field_name == "__runnable_config__"
                        or field_name == "runnable_config"
                    ):
                        logger.warning(f"Skipping special field {field_name}")
                        continue

                    # Get default and default_factory
                    if hasattr(field_info, "default") and field_info.default is not ...:
                        default = field_info.default
                    else:
                        default = None

                    default_factory = getattr(field_info, "default_factory", None)
                    description = getattr(field_info, "description", None)

                    # Add the field
                    self.add_field(
                        name=field_name,
                        field_type=field_type,
                        default=default,
                        default_factory=default_factory,
                        description=description,
                        source=source,
                        input_for=[engine_name],
                    )

                    logger.debug(
                        f"Added input field '{field_name}' from engine '{engine_name}'"
                    )

            except Exception as e:
                logger.warning(
                    f"Error getting input_fields from {engine_name}: {e}", exc_info=True
                )

        # 3.2 Extract output fields if needed (handle AugLLM special case)
        if (
            not output_schema
            and hasattr(engine, "get_output_fields")
            and callable(engine.get_output_fields)
        ):
            try:
                # For AugLLM without structured output, just mark the output field
                if is_aug_llm and aug_llm_output_field and not has_structured_output:
                    # Don't extract new fields, just mark the existing field as output
                    if (
                        aug_llm_output_field in self.fields
                        or aug_llm_output_field in self.base_class_fields
                    ):
                        self.output_fields[engine_name].add(aug_llm_output_field)
                        if (
                            aug_llm_output_field
                            not in self.engine_io_mappings[engine_name]["outputs"]
                        ):
                            self.engine_io_mappings[engine_name]["outputs"].append(
                                aug_llm_output_field
                            )
                        logger.debug(
                            f"Marked '{aug_llm_output_field}' as output for AugLLM '{engine_name}'"
                        )
                    else:
                        logger.warning(
                            f"AugLLM output field '{aug_llm_output_field}' not found in schema"
                        )
                else:
                    # Normal output field extraction for non-AugLLM engines
                    output_fields = engine.get_output_fields()
                    logger.debug(
                        f"Got {len(output_fields)} output fields from get_output_fields()"
                    )

                    for field_name, (field_type, field_info) in output_fields.items():
                        # Skip if already has this field or in base class
                        if (
                            field_name in self.fields
                            or field_name in self.base_class_fields
                        ):
                            # Just mark as output if it exists
                            self.output_fields[engine_name].add(field_name)
                            if (
                                field_name
                                not in self.engine_io_mappings[engine_name]["outputs"]
                            ):
                                self.engine_io_mappings[engine_name]["outputs"].append(
                                    field_name
                                )
                            logger.debug(
                                f"Field '{field_name}' already exists, marked as output for '{engine_name}'"
                            )
                            continue

                        # Skip special fields
                        if (
                            field_name == "__runnable_config__"
                            or field_name == "runnable_config"
                        ):
                            logger.warning(f"Skipping special field {field_name}")
                            continue

                        # Get default and default_factory
                        if (
                            hasattr(field_info, "default")
                            and field_info.default is not ...
                        ):
                            default = field_info.default
                        else:
                            default = None

                        default_factory = getattr(field_info, "default_factory", None)
                        description = getattr(field_info, "description", None)

                        # Add the field
                        self.add_field(
                            name=field_name,
                            field_type=field_type,
                            default=default,
                            default_factory=default_factory,
                            description=description,
                            source=source,
                            output_from=[engine_name],
                        )

                        logger.debug(
                            f"Added output field '{field_name}' from engine '{engine_name}'"
                        )

            except Exception as e:
                logger.warning(
                    f"Error getting output_fields from {engine_name}: {e}",
                    exc_info=True,
                )

        # For AugLLM, ensure messages is marked as output if that's the default
        if is_aug_llm and aug_llm_output_field == "messages":
            # Ensure messages field exists
            if (
                "messages" not in self.fields
                and "messages" not in self.base_class_fields
            ):
                from haive.core.schema.field_registry import StandardFields

                # Use the enhanced MessageList from StandardFields
                messages_field = StandardFields.messages(use_enhanced=True)

                self.add_field(
                    name=messages_field.name,
                    field_type=messages_field.field_type,
                    default_factory=messages_field.default_factory,
                    description=messages_field.description,
                    shared=True,  # Override to ensure it's shared
                    output_from=[engine_name],
                )
                self.has_messages = True
            else:
                # Just mark as output
                self.output_fields[engine_name].add("messages")
                if "messages" not in self.engine_io_mappings[engine_name]["outputs"]:
                    self.engine_io_mappings[engine_name]["outputs"].append("messages")

            logger.debug(
                f"Ensured 'messages' is output field for AugLLM '{engine_name}'"
            )

        # 4. Check for tools
        if hasattr(engine, "tools") and engine.tools:
            tools = engine.tools
            logger.debug(f"Engine {engine_name} has {len(tools)} tools")

            # Extract tool schemas
            self.extract_tool_schemas(tools)

            # Mark that we found tools
            self.has_tools = True

            # Add tools field if not present and not in base class
            if "tools" not in self.fields and "tools" not in self.base_class_fields:
                from typing import List

                self.add_field(
                    name="tools",
                    field_type=List[Any],
                    default_factory=list,
                    description="Tools for this engine",
                    source=source,
                )

                logger.debug(f"Added 'tools' field for engine '{engine_name}'")

        # 5. Check for tool routes (from ToolRouteMixin)
        if hasattr(engine, "tool_routes") and engine.tool_routes:
            tool_routes = engine.tool_routes
            logger.debug(f"Engine {engine_name} has {len(tool_routes)} tool routes")

            # Add tool_routes field if not present and not in base class
            if (
                "tool_routes" not in self.fields
                and "tool_routes" not in self.base_class_fields
            ):
                from haive.core.schema.field_registry import StandardFields

                # Use StandardFields to get the tool_routes field definition
                tool_routes_field = StandardFields.tool_routes()

                self.add_field(
                    name=tool_routes_field.name,
                    field_type=tool_routes_field.field_type,
                    default_factory=tool_routes_field.default_factory,
                    description=tool_routes_field.description,
                    source=source,
                )

                logger.debug(f"Added 'tool_routes' field for engine '{engine_name}'")

        # Update engine IO mapping
        if self.input_fields[engine_name]:
            self.engine_io_mappings[engine_name]["inputs"] = list(
                self.input_fields[engine_name]
            )

        if self.output_fields[engine_name]:
            self.engine_io_mappings[engine_name]["outputs"] = list(
                self.output_fields[engine_name]
            )

        logger.debug(
            f"Engine '{engine_name}' IO mappings: {len(self.input_fields[engine_name])} inputs, "
            f"{len(self.output_fields[engine_name])} outputs"
        )

        return self

    def extract_tool_schemas(self, tools: List[Any]) -> None:
        """
        Extract input and output schemas from tools with improved parsing detection.

        Args:
            tools: List of tools to analyze
        """
        logger.debug(f"Extracting schemas from {len(tools)} tools")

        # Track tools with structured schemas
        tools_with_parse_output = []

        for tool in tools:
            # Get tool name
            tool_name = getattr(tool, "name", None)
            if not tool_name and hasattr(tool, "__name__"):
                tool_name = tool.__name__
            if not tool_name:
                tool_name = f"tool_{id(tool)}"

            logger.debug(f"Processing tool: {tool_name}")

            # Check for structured_output_model - tools with this go to parse_output
            if (
                hasattr(tool, "structured_output_model")
                and tool.structured_output_model
            ):
                tools_with_parse_output.append(tool_name)
                logger.debug(
                    f"Tool {tool_name} has structured_output_model - marked for parse_output"
                )

            # Extract input schema
            input_schema = None

            # Check for args_schema on instance or class
            if hasattr(tool, "args_schema"):
                input_schema = tool.args_schema
                logger.debug(f"Using args_schema from tool {tool_name}")

            # For class types, try to instantiate
            elif isinstance(tool, type):
                if issubclass(tool, BaseTool):
                    try:
                        instance = tool()
                        if hasattr(instance, "args_schema"):
                            input_schema = instance.args_schema
                            logger.debug(
                                f"Using args_schema from instantiated {tool_name}"
                            )
                    except Exception as e:
                        logger.warning(
                            f"Could not instantiate tool class {tool_name}: {e}"
                        )

            # For BaseModel types, use directly
            if isinstance(tool, type) and issubclass(tool, BaseModel):
                input_schema = tool
                logger.debug(f"Using tool class as schema for {tool_name}")

            # Add input schema field if found
            if (
                input_schema
                and isinstance(input_schema, type)
                and issubclass(input_schema, BaseModel)
            ):
                # Create field path for tools dictionary
                field_name = f"tool_schemas.{tool_name}"
                logger.debug(f"Adding schema for tool {tool_name}")

                # Add to tool_schemas dictionary in state
                self.add_field(
                    name=field_name,
                    field_type=Type[BaseModel],
                    default=input_schema,
                    description=f"Schema for {tool_name}",
                )

                # Try to find matching output schema
                input_class_name = input_schema.__name__

                # Common naming patterns for output schemas
                possible_names = [
                    f"{tool_name.capitalize()}Result",
                    f"{tool_name.capitalize()}Output",
                    f"{input_class_name}Result",
                    f"{input_class_name}Output",
                    f"{input_class_name.replace('Input', '')}Result",
                    f"{input_class_name.replace('Query', '')}Result",
                ]

                # Look in surrounding module
                if hasattr(input_schema, "__module__"):
                    module = sys.modules.get(input_schema.__module__)
                    if module:
                        for name in possible_names:
                            if hasattr(module, name):
                                output_class = getattr(module, name)
                                if isinstance(output_class, type) and issubclass(
                                    output_class, BaseModel
                                ):
                                    # Add to output_schemas
                                    output_field_name = f"output_schemas.{name}"
                                    self.add_field(
                                        name=output_field_name,
                                        field_type=Type[BaseModel],
                                        default=output_class,
                                        description=f"Output schema for {tool_name}",
                                    )

                                    # Mark this tool for parse_output
                                    if tool_name not in tools_with_parse_output:
                                        tools_with_parse_output.append(tool_name)
                                        logger.debug(
                                            f"Tool {tool_name} has output schema - marked for parse_output"
                                        )

                                    # Note: Cannot assign tool_name attribute to BaseModel class
                                    # This will be handled at runtime in ToolState
                                    logger.debug(
                                        f"Found output schema {name} for {tool_name}"
                                    )
                                    break

        # Add tool type fields
        # logger.debug("Adding tool_types_dict field")
        # self.add_field(
        #    name="tool_types_dict",
        #    field_type=Dict[str, str],
        #    default_factory=dict,
        #    description="Dictionary mapping tool names to their routing destinations",
        # )

        # If we have tools marked for parse_output, add them to the schema
        if tools_with_parse_output:
            # Initialize tool_types_dict
            for tool_name in tools_with_parse_output:
                # Create routing entries
                logger.debug(f"Setting routing for {tool_name} -> parse_output")

                # Use this for demo purposes, it will be rebuilt at runtime in ToolState
                # but this gives visibility into what will happen
                if "tool_types_dict" in self.fields:
                    tool_field = self.fields["tool_types_dict"]
                    if tool_field.default is None:
                        tool_field.default = {}

                    tool_field.default[tool_name] = "parse_output"

        # Add tools field if not present and not in base class
        if "tools" not in self.fields and "tools" not in self.base_class_fields:
            self.add_field(
                name="tools",
                field_type=List[Any],
                default_factory=list,
                description="Tool instances indexed by name",
            )
            self.has_tools = True

        # Add tool_schemas field if not present
        if not any(name.startswith("tool_schemas.") for name in self.fields):
            self.add_field(
                name="tool_schemas",
                field_type=Dict[str, Type[BaseModel]],
                default_factory=dict,
                description="Tool schemas indexed by name",
            )

        # Add output_schemas field if not present
        if not any(name.startswith("output_schemas.") for name in self.fields):
            self.add_field(
                name="output_schemas",
                field_type=Dict[str, Type[BaseModel]],
                default_factory=dict,
                description="Output schemas indexed by name",
            )

    def add_fields_from_components(self, components: List[Any]) -> "SchemaComposer":
        """Add fields from multiple components to the schema.

        This method intelligently processes a list of heterogeneous components, automatically
        detecting their types and extracting fields using the appropriate extraction strategy.
        It supports engines, Pydantic models, dictionaries, and other component types,
        providing a unified interface for schema composition from diverse sources.

        The method first detects base class requirements (such as the need for messages or
        tools fields) and then processes each component individually, delegating to specialized
        field extraction methods based on component type. After processing all components,
        it ensures standard fields are present and properly configured.

        Args:
            components: List of components to extract fields from, which can include:
                - Engine instances (with engine_type attribute)
                - Pydantic BaseModel instances or classes
                - Dictionaries of field definitions
                - Other component types with field information

        Returns:
            Self for method chaining to enable fluent API style

        Example:
            ```python
            # Create a schema from multiple components
            composer = SchemaComposer(name="AgentState")
            composer.add_fields_from_components([
                llm_engine,          # Engine instance
                retriever_engine,    # Engine instance
                MemoryConfig,        # Pydantic model class
                {"context": (List[str], list, {"description": "Retrieved documents"})}
            ])
            ```

        Note:
            This is one of the most powerful methods in SchemaComposer, as it can
            automatically build a complete schema from a list of components without
            requiring manual field definition. It's particularly useful for dynamic
            composition of schemas at runtime.
        """
        logger.debug(f"Extracting fields from {len(components)} components")

        # Detect base class requirements early
        self._detect_base_class_requirements(components)

        # Track number of fields before
        field_count_before = len(self.fields)

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
                # Looks like an Engine
                logger.debug(f"Component {component_id} is an Engine")
                self.add_fields_from_engine(component)

            elif isinstance(component, BaseModel):
                # BaseModel instance
                logger.debug(f"Component {component_id} is a BaseModel instance")
                self.add_fields_from_model(component.__class__)

            elif isinstance(component, type) and issubclass(component, BaseModel):
                # BaseModel class
                logger.debug(f"Component {component_id} is a BaseModel class")
                self.add_fields_from_model(component)

            elif isinstance(component, dict):
                # Dictionary
                logger.debug(f"Component {component_id} is a dictionary")
                self.add_fields_from_dict(component)

            else:
                logger.debug(f"Skipping unsupported component type: {component_type}")

        # Report results
        field_count_after = len(self.fields)
        field_count_added = field_count_after - field_count_before

        logger.debug(
            f"Added {field_count_added} fields from components (total: {field_count_after})"
        )

        # Always ensure we have 'messages' and 'runnable_config' if we found engines
        self._ensure_standard_fields()

        return self

    def _ensure_standard_fields(self) -> None:
        """
        Ensure standard fields are present if not already added.
        """
        # Ensure runnable_config if we found engines
        has_engines = any(
            entry.get("action") == "process_component"
            and hasattr(entry.get("component_type"), "engine_type")
            for entry in self.processing_history
        )

        if (
            has_engines
            and "runnable_config" not in self.fields
            and "runnable_config" not in self.base_class_fields
        ):
            from typing import Any, Dict, Optional

            self.add_field(
                name="runnable_config",
                field_type=Optional[Dict[str, Any]],
                default=None,
                description="Runtime configuration for engines",
                source="auto_added",
            )
            logger.debug("Added standard field 'runnable_config'")

        # Ensure engines field if we have engines
        if (
            self.engines
            and "engines" not in self.fields
            and "engines" not in self.base_class_fields
        ):
            from typing import Any, Dict

            # Create a default factory that returns the class engines
            def get_class_engines():
                # This will be bound to the schema class later
                return {}

            self.add_field(
                name="engines",
                field_type=Dict[str, Any],
                default_factory=get_class_engines,
                description="Engine instances indexed by name",
                source="auto_added",
            )
            logger.debug("Added standard field 'engines' with engine factory")

        # Ensure we have messages field for chat agents
        engines_with_messages = [
            entry
            for entry in self.processing_history
            if entry.get("action") == "process_component"
            and entry.get("component_type") == "AugLLMConfig"
        ]

        if (
            engines_with_messages
            and "messages" not in self.fields
            and "messages" not in self.base_class_fields
        ):
            self.configure_messages_field(with_reducer=True, force_add=True)
            logger.debug("Added standard field 'messages' with reducer")

    def add_engine_management(self) -> "SchemaComposer":
        """Add standardized engine management fields to the schema.

        This method adds the new engine management pattern to support:
        - Optional 'engine' field for primary/main engine
        - Explicit 'engines' dict field (was implicit before)
        - Automatic synchronization between the two

        This is part of the schema simplification effort to provide clearer
        patterns for engine management while maintaining backward compatibility.

        Returns:
            Self for chaining
        """
        logger.debug("Adding standardized engine management fields")

        # Import engine type if available
        engine_type = Any
        try:
            from haive.core.engine.base import Engine

            engine_type = Optional[Engine]
        except ImportError:
            logger.debug("Could not import Engine type, using Any")

        # Add optional engine field if not present
        if "engine" not in self.fields and "engine" not in self.base_class_fields:
            self.add_field(
                name="engine",
                field_type=engine_type,
                default=None,
                description="Optional main/primary engine for convenience",
                source="engine_management",
            )
            logger.debug("Added 'engine' field for primary engine")

        # Add explicit engines dict if not present
        if "engines" not in self.fields and "engines" not in self.base_class_fields:
            self.add_field(
                name="engines",
                field_type=Dict[str, Any],
                default_factory=dict,
                description="Engine registry for this state (backward compatible)",
                source="engine_management",
            )
            logger.debug("Added 'engines' dict field for engine registry")

        return self

    def configure_messages_field(
        self, with_reducer: bool = True, force_add: bool = False
    ) -> "SchemaComposer":
        """
        Configure a messages field with appropriate settings if it exists or if requested.

        Args:
            with_reducer: Whether to add a reducer for the messages field
            force_add: Whether to add the messages field if it doesn't exist

        Returns:
            Self for chaining
        """
        logger.debug(
            f"Configuring messages field (with_reducer={with_reducer}, force_add={force_add})"
        )

        # Check if messages will be provided by base class
        if self.detected_base_class and "messages" in self.base_class_fields:
            logger.debug("Messages field will be provided by base class")
            # Still mark as shared if requested
            self.shared_fields.add("messages")
            return self

        # Only proceed if the field exists or we're forcing its addition
        if "messages" in self.fields or force_add:
            from typing import List

            # Try to use langgraph's add_messages if requested
            if with_reducer:
                try:
                    from langchain_core.messages import BaseMessage
                    from langgraph.graph import add_messages

                    # If force_add is True and the field doesn't exist, add it
                    if force_add and "messages" not in self.fields:
                        self.add_field(
                            name="messages",
                            field_type=List[BaseMessage],
                            default_factory=list,
                            description="Messages for agent conversation",
                            reducer=add_messages,
                            shared=True,  # Usually want messages to be shared
                        )
                        self.has_messages = True
                        logger.debug(
                            "Added 'messages' field with add_messages reducer and shared=True"
                        )

                    # Otherwise, just set the reducer if the field exists
                    elif "messages" in self.fields:
                        self.fields["messages"].reducer = add_messages
                        # Also mark as shared if not already
                        if "messages" not in self.shared_fields:
                            self.shared_fields.add("messages")
                            self.fields["messages"].shared = True
                            logger.debug(
                                "Added add_messages reducer to existing messages field and marked as shared"
                            )

                except ImportError:
                    # Fallback if add_messages is not available
                    from typing import Any

                    # Create simple concat lists reducer
                    def concat_lists(a, b):
                        return (a or []) + (b or [])

                    # If force_add is True and the field doesn't exist, add it
                    if force_add and "messages" not in self.fields:
                        self.add_field(
                            name="messages",
                            field_type=List[Any],
                            default_factory=list,
                            description="Messages for agent conversation",
                            reducer=concat_lists,
                            shared=True,
                        )
                        self.has_messages = True
                        logger.debug(
                            "Added 'messages' field with concat_lists reducer (fallback) and shared=True"
                        )

                    # Otherwise, just set the reducer if the field exists
                    elif "messages" in self.fields:
                        self.fields["messages"].reducer = concat_lists
                        # Also mark as shared if not already
                        if "messages" not in self.shared_fields:
                            self.shared_fields.add("messages")
                            self.fields["messages"].shared = True
                            logger.debug(
                                "Added concat_lists reducer to existing messages field and marked as shared"
                            )

        return self

    def mark_as_input_field(
        self, field_name: str, engine_name: str
    ) -> "SchemaComposer":
        """
        Mark a field as input field for a specific engine.

        Args:
            field_name: Name of the field
            engine_name: Name of the engine

        Returns:
            Self for chaining
        """
        # Check field exists
        if field_name not in self.fields and field_name not in self.base_class_fields:
            logger.warning(f"Cannot mark non-existent field '{field_name}' as input")
            return self

        logger.debug(
            f"Marking field '{field_name}' as input for engine '{engine_name}'"
        )

        # Initialize engine mapping if not exists
        if engine_name not in self.engine_io_mappings:
            self.engine_io_mappings[engine_name] = {"inputs": [], "outputs": []}

        # Add field to inputs for this engine
        self.input_fields[engine_name].add(field_name)

        # Make sure field is in engine mapping inputs
        if field_name not in self.engine_io_mappings[engine_name]["inputs"]:
            self.engine_io_mappings[engine_name]["inputs"].append(field_name)

        return self

    def mark_as_output_field(
        self, field_name: str, engine_name: str
    ) -> "SchemaComposer":
        """
        Mark a field as output field for a specific engine.

        Args:
            field_name: Name of the field
            engine_name: Name of the engine

        Returns:
            Self for chaining
        """
        # Check field exists
        if field_name not in self.fields and field_name not in self.base_class_fields:
            logger.warning(f"Cannot mark non-existent field '{field_name}' as output")
            return self

        logger.debug(
            f"Marking field '{field_name}' as output for engine '{engine_name}'"
        )

        # Initialize engine mapping if not exists
        if engine_name not in self.engine_io_mappings:
            self.engine_io_mappings[engine_name] = {"inputs": [], "outputs": []}

        # Add field to outputs for this engine
        self.output_fields[engine_name].add(field_name)

        # Make sure field is in engine mapping outputs
        if field_name not in self.engine_io_mappings[engine_name]["outputs"]:
            self.engine_io_mappings[engine_name]["outputs"].append(field_name)

        return self

    def build(self) -> Type[StateSchema]:
        """Build and return a StateSchema class with all defined fields and metadata.

        This method finalizes the schema composition process by generating a concrete
        StateSchema subclass with the appropriate base class (determined by detected
        requirements) and all the fields, metadata, and behaviors defined during
        composition. It performs comprehensive setup of the schema class, including:

        1. Field generation with proper types, defaults, and metadata
        2. Configuration of shared fields for parent-child graph relationships
        3. Setup of reducer functions for state merging
        4. Engine I/O tracking for proper state routing
        5. Structured output model integration
        6. Schema post-initialization for nested fields, dictionaries, and engine tool synchronization
        7. Rich visualization for debugging (when debug logging is enabled)

        The generated schema is a fully functional Pydantic model subclass that can
        be instantiated directly or used as a state schema in a LangGraph workflow.

        Engine Tool Synchronization:
        --------------------------
        This method stores engines directly on the schema class and implements an
        enhanced model_post_init that ensures:

        1. Class-level engines are made available on instances
        2. For ToolState subclasses, tools from class-level engines are automatically synced
           to the instance's tools list

        This functionality bridges the gap between class-level engine storage and
        instance-level tool management, ensuring that tools from engines stored by
        SchemaComposer are properly synchronized with ToolState instances.

        Returns:
            A StateSchema subclass with all defined fields, metadata, and behaviors
        """
        # Make sure we've detected base class requirements
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

        # Create field definitions for the model (excluding base class fields)
        field_defs = {}
        for name, field_def in self.fields.items():
            # Skip schema dictionary entries for now (handle nested dictionaries later)
            if "." in name:
                logger.debug(f"Skipping nested field {name} for now")
                continue

            # Skip fields that the base class provides
            if name in self.base_class_fields:
                logger.debug(f"Skipping field {name} - provided by base class")
                continue

            field_type, field_info = field_def.to_field_info()
            field_defs[name] = (field_type, field_info)

        # Create the base schema
        schema = create_model(self.name, __base__=base_class, **field_defs)

        # Only add StateSchema-specific attributes if the base class is a StateSchema
        is_state_schema_base = issubclass(base_class, StateSchema)

        # Copy attributes from base class if they exist
        if is_state_schema_base and hasattr(base_class, "__shared_fields__"):
            # Merge with our shared fields
            base_shared = set(getattr(base_class, "__shared_fields__", []))
            schema.__shared_fields__ = list(base_shared | self.shared_fields)
        elif is_state_schema_base:
            schema.__shared_fields__ = list(self.shared_fields)

        if is_state_schema_base:
            logger.debug(f"Shared fields: {getattr(schema, '__shared_fields__', [])}")

        # Handle reducers - merge base class reducers with ours
        if is_state_schema_base:
            schema.__serializable_reducers__ = {}
            schema.__reducer_fields__ = {}

            # Copy base class reducers first
            if hasattr(base_class, "__serializable_reducers__"):
                schema.__serializable_reducers__.update(
                    getattr(base_class, "__serializable_reducers__", {})
                )
            if hasattr(base_class, "__reducer_fields__"):
                schema.__reducer_fields__.update(
                    getattr(base_class, "__reducer_fields__", {})
                )

            # Add our reducers (potentially overriding base class)
            for name, field_def in self.fields.items():
                if field_def.reducer:
                    reducer_name = field_def.get_reducer_name()
                    schema.__serializable_reducers__[name] = reducer_name
                    schema.__reducer_fields__[name] = field_def.reducer

        # Make sure to deep copy the engine I/O mappings to avoid reference issues
        if is_state_schema_base:
            schema.__engine_io_mappings__ = {}
            for engine_name, mapping in self.engine_io_mappings.items():
                schema.__engine_io_mappings__[engine_name] = mapping.copy()

            # Same for input/output fields - convert sets to lists and deep copy
            schema.__input_fields__ = {}
            for engine_name, fields in self.input_fields.items():
                schema.__input_fields__[engine_name] = list(fields)

            schema.__output_fields__ = {}
            for engine_name, fields in self.output_fields.items():
                schema.__output_fields__[engine_name] = list(fields)

            # Add structured model fields metadata safely - use field names instead of class references
            if self.structured_model_fields:
                schema.__structured_model_fields__ = {
                    k: list(v) for k, v in self.structured_model_fields.items()
                }

            # Add structured models safely - use string identifiers instead of class references
            if self.structured_models:
                schema.__structured_models__ = {
                    k: f"{v.__module__}.{v.__name__}"
                    for k, v in self.structured_models.items()
                }

            # CRITICAL: Store engines directly on the schema class (not private)
            schema.engines = self.engines
            schema.engines_by_type = dict(self.engines_by_type)
            logger.debug(f"Stored {len(schema.engines)} engines on schema class")

            # Update the engines field default factory to return class engines
            if "engines" in schema.model_fields:
                # Create a factory that returns the class engines
                def engines_factory(cls=schema):
                    return cls.engines.copy() if hasattr(cls, "engines") else {}

                # Update the field's default_factory
                schema.model_fields["engines"].default_factory = engines_factory
                logger.debug(
                    "Updated engines field default_factory to return class engines"
                )

        # Now handle nested fields like tool_schemas.xyz
        # We need to build nested dictionaries for these

        tool_schemas = {}
        output_schemas = {}

        for name, field_def in self.fields.items():
            # Look for dot notation
            if "." in name:
                parts = name.split(".", 1)

                if parts[0] == "tool_schemas":
                    logger.debug(f"Adding tool schema: {parts[1]}")
                    tool_schemas[parts[1]] = field_def.default

                elif parts[0] == "output_schemas":
                    logger.debug(f"Adding output schema: {parts[1]}")
                    output_schemas[parts[1]] = field_def.default

        # Create post_init method to handle nested fields and engine setup
        def schema_post_init(self, __context):
            """Enhanced post-init to sync tools from engines."""
            # IMPORTANT: In Pydantic v2, model_post_init takes a context parameter
            logger.debug(f"schema_post_init called for {self.__class__.__name__}")

            # Call parent post_init if it exists
            if hasattr(super(self.__class__, self), "model_post_init"):
                super(self.__class__, self).model_post_init(__context)

            # Initialize instance-level engines from class-level engines
            if hasattr(self.__class__, "engines"):
                # If engines field exists, populate it from class engines
                if hasattr(self, "engines"):
                    if not self.engines:  # Only populate if empty
                        self.engines = {}
                    # Copy class engines to instance field
                    for engine_name, engine in self.__class__.engines.items():
                        self.engines[engine_name] = engine
                    logger.debug(
                        f"Populated instance engines field with {len(self.engines)} engines from class"
                    )

            # Sync tools from class engines if available
            if hasattr(self.__class__, "engines"):
                logger.debug(
                    f"Found {len(self.__class__.engines)} class-level engines (legacy)"
                )

                # If this is a ToolState subclass or has tools field, sync tools
                if hasattr(self, "tools"):
                    logger.debug(f"Syncing tools for {self.__class__.__name__}")

                    # Initialize tools list if it's None
                    if self.tools is None:
                        self.tools = []

                    for engine_name, engine in self.__class__.engines.items():
                        logger.debug(f"Checking engine '{engine_name}' for tools")

                        if hasattr(engine, "tools") and engine.tools:
                            logger.debug(
                                f"Engine '{engine_name}' has {len(engine.tools)} tools"
                            )

                            # For ToolState, use add_tool method if available
                            if hasattr(self, "add_tool"):
                                for tool in engine.tools:
                                    # Get tool name
                                    tool_name = getattr(
                                        tool,
                                        "name",
                                        getattr(tool, "__name__", str(tool)),
                                    )

                                    # Check if tool already exists
                                    existing_tool_names = []
                                    for t in self.tools:
                                        t_name = getattr(
                                            t, "name", getattr(t, "__name__", str(t))
                                        )
                                        existing_tool_names.append(t_name)

                                    if tool_name not in existing_tool_names:
                                        self.add_tool(tool)
                                        logger.debug(
                                            f"Added tool '{tool_name}' from engine '{engine_name}'"
                                        )
                                    else:
                                        logger.debug(
                                            f"Tool '{tool_name}' already exists, skipping"
                                        )
                            else:
                                # For basic tools list, just append
                                for tool in engine.tools:
                                    if tool not in self.tools:
                                        self.tools.append(tool)
                                        tool_name = getattr(tool, "name", str(tool))
                                        logger.debug(
                                            f"Appended tool '{tool_name}' from engine '{engine_name}'"
                                        )

            # Initialize tool_schemas (existing code)
            if hasattr(self, "tool_schemas") and tool_schemas:
                for name, schema_cls in tool_schemas.items():
                    self.tool_schemas[name] = schema_cls

            # Initialize output_schemas (existing code)
            if hasattr(self, "output_schemas") and output_schemas:
                for name, schema_cls in output_schemas.items():
                    self.output_schemas[name] = schema_cls

        # Properly set the method on the schema class
        schema.model_post_init = schema_post_init

        # Print summary
        logger.debug(f"Created schema {schema.__name__} with {len(field_defs)} fields")
        if is_state_schema_base:
            logger.debug(
                f"Engine mappings: {len(getattr(schema, '__engine_io_mappings__', {})) } engines"
            )
            if getattr(schema, "__serializable_reducers__", {}):
                logger.debug(
                    f"Reducers: {len(getattr(schema, '__serializable_reducers__', {}))} fields have reducers"
                )

        # Create rich table for field display (only for StateSchema bases)
        if is_state_schema_base:
            self._display_schema_summary(schema)

        return schema

    def _display_schema_summary(self, schema: Type[StateSchema]) -> None:
        """Display a visual summary of the created schema."""
        # Only display if debug logging is enabled
        if logger.level > logging.DEBUG:
            return

        # Check if this is a StateSchema
        is_state_schema = issubclass(schema, StateSchema)

        # Create a table for field display
        table = Table(title=f"{schema.__name__} Schema Fields", show_header=True)
        table.add_column("Field Name", style="cyan")
        table.add_column("Type", style="yellow")
        table.add_column("Description", style="blue")
        table.add_column("Metadata", style="magenta")

        for field_name, field_info in schema.model_fields.items():
            if field_name.startswith("__"):
                continue

            field_type = str(field_info.annotation).replace("typing.", "")
            desc = field_info.description or ""

            # Build metadata string
            metadata = []
            if is_state_schema:
                shared_fields = getattr(schema, "__shared_fields__", [])
                if field_name in shared_fields:
                    metadata.append("[green]shared[/green]")

                serializable_reducers = getattr(schema, "__serializable_reducers__", {})
                if field_name in serializable_reducers:
                    metadata.append(
                        f"[yellow]reducer={serializable_reducers[field_name]}[/yellow]"
                    )

                # Check if field is input or output for any engine
                engine_io_mappings = getattr(schema, "__engine_io_mappings__", {})
                for engine_name, mapping in engine_io_mappings.items():
                    if field_name in mapping.get("inputs", []):
                        metadata.append(f"[cyan]input({engine_name})[/cyan]")
                    if field_name in mapping.get("outputs", []):
                        metadata.append(f"[blue]output({engine_name})[/blue]")

            table.add_row(field_name, field_type, desc, ", ".join(metadata))

        console.print(table)

        if is_state_schema:
            engine_io_mappings = getattr(schema, "__engine_io_mappings__", {})
            if engine_io_mappings:
                console.print("\n[bold green]Engine I/O Mappings:[/bold green]")
                for engine_name, mapping in engine_io_mappings.items():
                    inputs = ", ".join(mapping["inputs"]) if mapping["inputs"] else "-"
                    outputs = (
                        ", ".join(mapping["outputs"]) if mapping["outputs"] else "-"
                    )
                    console.print(f"  [bold]{engine_name}[/bold]:")
                    console.print(f"    [cyan]Inputs[/cyan]: {inputs}")
                    console.print(f"    [blue]Outputs[/blue]: {outputs}")

            # Display engines if any
            engines = getattr(schema, "engines", {})
            if engines:
                console.print("\n[bold yellow]Registered Engines:[/bold yellow]")
                engine_table = Table(show_header=True)
                engine_table.add_column("Name", style="cyan")
                engine_table.add_column("Type", style="yellow")
                engine_table.add_column("Config", style="green")

                for engine_name, engine in engines.items():
                    engine_type = getattr(engine, "engine_type", "unknown")
                    if hasattr(engine_type, "value"):
                        engine_type = str(engine_type.value)
                    else:
                        engine_type = str(engine_type)

                    # Get key config info
                    config_info = []
                    if engine_type == "llm" and hasattr(engine, "llm_config"):
                        if hasattr(engine.llm_config, "model"):
                            config_info.append(f"model={engine.llm_config.model}")
                    elif hasattr(engine, "model"):
                        config_info.append(f"model={engine.model}")

                    engine_table.add_row(
                        engine_name,
                        engine_type,
                        ", ".join(config_info) if config_info else "-",
                    )

                console.print(engine_table)

    def to_manager(self) -> "StateSchemaManager":
        """
        Convert to a StateSchemaManager for further manipulation.

        Returns:
            StateSchemaManager instance
        """
        from haive.core.schema.schema_manager import StateSchemaManager

        return StateSchemaManager(self)

    @classmethod
    def merge(
        cls,
        first: "SchemaComposer",
        second: "SchemaComposer",
        name: str = "MergedSchema",
    ) -> "SchemaComposer":
        """
        Merge two SchemaComposer instances.

        Args:
            first: First composer
            second: Second composer
            name: Name for merged composer

        Returns:
            New merged SchemaComposer
        """
        logger.debug(f"Merging composers: {first.name} + {second.name} -> {name}")
        merged = cls(name=name)

        # Detect base class requirements from both composers
        if first.has_messages or second.has_messages:
            merged.has_messages = True
        if first.has_tools or second.has_tools:
            merged.has_tools = True
        merged._detect_base_class_requirements()

        # Add fields from first composer
        for field_name, field_def in first.fields.items():
            merged.add_field(
                name=field_name,
                field_type=field_def.field_type,
                default=field_def.default,
                default_factory=field_def.default_factory,
                description=field_def.description,
                shared=field_def.shared,
                reducer=field_def.reducer,
                source=f"first_composer_{field_def.name}",
            )

        # Add fields from second composer (overwriting if they exist)
        for field_name, field_def in second.fields.items():
            merged.add_field(
                name=field_name,
                field_type=field_def.field_type,
                default=field_def.default,
                default_factory=field_def.default_factory,
                description=field_def.description,
                shared=field_def.shared,
                reducer=field_def.reducer,
                source=f"second_composer_{field_def.name}",
            )

        # Merge shared fields
        merged.shared_fields.update(first.shared_fields)
        merged.shared_fields.update(second.shared_fields)

        # Merge field sources
        for field_name, sources in first.field_sources.items():
            merged.field_sources[field_name].update(sources)
        for field_name, sources in second.field_sources.items():
            merged.field_sources[field_name].update(sources)

        # Merge input/output tracking
        for engine, fields in first.input_fields.items():
            merged.input_fields[engine].update(fields)
        for engine, fields in second.input_fields.items():
            merged.input_fields[engine].update(fields)

        for engine, fields in first.output_fields.items():
            merged.output_fields[engine].update(fields)
        for engine, fields in second.output_fields.items():
            merged.output_fields[engine].update(fields)

        # Merge engine mappings
        merged.engine_io_mappings.update(first.engine_io_mappings)
        merged.engine_io_mappings.update(second.engine_io_mappings)

        # Merge structured models
        merged.structured_models.update(first.structured_models)
        merged.structured_models.update(second.structured_models)

        # Merge structured model fields
        for model_name, fields in first.structured_model_fields.items():
            merged.structured_model_fields[model_name].update(fields)
        for model_name, fields in second.structured_model_fields.items():
            merged.structured_model_fields[model_name].update(fields)

        # Merge engines
        merged.engines.update(first.engines)
        merged.engines.update(second.engines)

        # Merge engines by type
        for engine_type, engine_names in first.engines_by_type.items():
            merged.engines_by_type[engine_type].extend(engine_names)
        for engine_type, engine_names in second.engines_by_type.items():
            merged.engines_by_type[engine_type].extend(engine_names)

        # Remove duplicates from engines_by_type
        for engine_type in merged.engines_by_type:
            merged.engines_by_type[engine_type] = list(
                set(merged.engines_by_type[engine_type])
            )

        # Merge metadata
        merged.has_messages = first.has_messages or second.has_messages
        merged.has_tools = first.has_tools or second.has_tools

        # Merge tracking
        merged.processing_history = first.processing_history + second.processing_history

        logger.debug(f"Merged composers: {len(merged.fields)} total fields")

        return merged

    @classmethod
    def from_components(
        cls,
        components: List[Any],
        name: str = "ComposedSchema",
        base_state_schema: Optional[Type[StateSchema]] = None,
    ) -> Type[StateSchema]:
        """Create and build a StateSchema directly from a list of components.

        This convenience class method provides a simplified, one-step approach to schema
        creation from components. It creates a SchemaComposer instance, processes all
        components to extract fields, ensures standard fields are present, and builds
        the final StateSchema in a single operation.

        This is the recommended entry point for most schema composition needs, as it
        handles all the details of schema composition in a single method call. It's
        particularly useful when you want to quickly create a schema from existing
        components without detailed customization.

        Args:
            components: List of components to extract fields from, which can include:
                - Engine instances (with engine_type attribute)
                - Pydantic BaseModel instances or classes
                - Dictionaries of field definitions
                - Other component types with field information
            name: Name for the generated schema class
            base_state_schema: Optional custom base state schema to use. If not provided,
                             the composer will auto-detect the appropriate base class.

        Returns:
            A fully constructed StateSchema subclass ready for instantiation

        Example:
            ```python
            # Create a schema from components in one step
            ConversationState = SchemaComposer.from_components(
                [llm_engine, retriever_engine, memory_component],
                name="ConversationState"
            )

            # Use the schema
            state = ConversationState()

            # With custom base schema for token tracking
            from haive.core.schema.prebuilt import MessagesStateWithTokenUsage
            TokenAwareState = SchemaComposer.from_components(
                [llm_engine],
                name="TokenAwareState",
                base_state_schema=MessagesStateWithTokenUsage
            )
            ```

        Note:
            This method automatically detects which base class to use (StateSchema,
            MessagesStateWithTokenUsage, or ToolState) based on the components provided,
            ensuring the schema has the appropriate functionality for the detected requirements.
            When messages are detected, it now uses MessagesStateWithTokenUsage by default
            for better token tracking.
        """
        logger.debug(f"Creating schema {name} from {len(components)} components")
        composer = cls(name=name, base_state_schema=base_state_schema)

        # Detect base class requirements early
        composer._detect_base_class_requirements(components)

        # Process each component
        for component in components:
            if component is None:
                continue

            # Process based on type
            if hasattr(component, "engine_type"):
                # Looks like an Engine
                composer.add_fields_from_engine(component)
            elif isinstance(component, BaseModel):
                # BaseModel instance
                composer.add_fields_from_model(component.__class__)
            elif isinstance(component, type) and issubclass(component, BaseModel):
                # BaseModel class
                composer.add_fields_from_model(component)
            elif isinstance(component, dict):
                # Dictionary
                composer.add_fields_from_dict(component)
            else:
                logger.debug(f"Skipping unsupported component: {type(component)}")

        # Ensure standard fields if needed
        composer._ensure_standard_fields()

        # Build the schema
        schema = composer.build()

        return schema

    def show_engines(self) -> None:
        """Display a summary of all registered engines."""
        if not self.engines:
            console.print("[yellow]No engines registered[/yellow]")
            return

        tree = Tree("[bold green]Registered Engines[/bold green]")

        for engine_type, engine_names in self.engines_by_type.items():
            type_node = tree.add(
                f"[bold cyan]{engine_type}[/bold cyan] ({len(engine_names)} engines)"
            )

            for engine_name in engine_names:
                if engine_name in self.engines:
                    engine = self.engines[engine_name]

                    # Build info string
                    info_parts = []
                    if engine_type == "llm" and hasattr(engine, "llm_config"):
                        if hasattr(engine.llm_config, "model"):
                            info_parts.append(f"model={engine.llm_config.model}")
                    elif hasattr(engine, "model"):
                        info_parts.append(f"model={engine.model}")

                    info_str = (
                        f" [dim]({', '.join(info_parts)})[/dim]" if info_parts else ""
                    )
                    type_node.add(f"[yellow]{engine_name}[/yellow]{info_str}")

        console.print(tree)

    # Add these methods to your SchemaComposer class

    @classmethod
    def compose_input_schema(
        cls, components: List[Any], name: str = "InputSchema"
    ) -> Type[BaseModel]:
        """
        Create an input schema from components, focusing on input fields.

        Args:
            components: List of components to extract fields from
            name: Name for the schema

        Returns:
            BaseModel subclass optimized for input
        """
        composer = cls(name=name)

        # Process each component
        for component in components:
            if component is None:
                continue

            # Only extract input fields from engines
            if hasattr(component, "engine_type") and hasattr(
                component, "get_input_fields"
            ):
                try:
                    # Extract input fields
                    input_fields = component.get_input_fields()
                    engine_name = getattr(component, "name", str(component))

                    for field_name, (field_type, field_info) in input_fields.items():
                        # Skip if already has this field
                        if field_name in composer.fields:
                            continue

                        # Skip special fields
                        if (
                            field_name == "__runnable_config__"
                            or field_name == "runnable_config"
                        ):
                            continue

                        # Get default and default_factory
                        if (
                            hasattr(field_info, "default")
                            and field_info.default is not ...
                        ):
                            default = field_info.default
                        else:
                            default = None

                        default_factory = getattr(field_info, "default_factory", None)
                        description = getattr(field_info, "description", None)

                        # Add the field
                        composer.add_field(
                            name=field_name,
                            field_type=field_type,
                            default=default,
                            default_factory=default_factory,
                            description=description,
                            source=engine_name,
                        )

                        # Track as input field
                        composer.input_fields[engine_name].add(field_name)

                    # Update engine IO mapping
                    composer.engine_io_mappings[engine_name] = {
                        "inputs": list(composer.input_fields[engine_name]),
                        "outputs": [],
                    }
                except Exception as e:
                    logger.warning(
                        f"Error extracting input fields from {component}: {e}"
                    )

            # Handle BaseModel components differently - only extract specific input-related fields
            elif isinstance(component, BaseModel) or (
                isinstance(component, type) and issubclass(component, BaseModel)
            ):
                model = (
                    component if isinstance(component, type) else component.__class__
                )
                source = model.__name__

                # Focus on common input field names
                input_field_names = [
                    "input",
                    "query",
                    "question",
                    "messages",
                    "text",
                    "content",
                ]

                # Extract differently based on Pydantic version
                if hasattr(model, "model_fields"):
                    # Pydantic v2
                    for field_name, field_info in model.model_fields.items():
                        # Only include common input fields and skip special fields
                        if (
                            field_name not in input_field_names
                            or field_name.startswith("__")
                        ):
                            continue

                        # Skip runnable_config
                        if (
                            field_name == "__runnable_config__"
                            or field_name == "runnable_config"
                        ):
                            continue

                        # Get field type and defaults
                        field_type = field_info.annotation

                        # Handle default vs default_factory
                        if field_info.default_factory is not None:
                            default_factory = field_info.default_factory
                            default = None
                        else:
                            default_factory = None
                            default = field_info.default

                        # Add the field
                        composer.add_field(
                            name=field_name,
                            field_type=field_type,
                            default=default,
                            default_factory=default_factory,
                            description=field_info.description,
                            source=source,
                        )
                elif hasattr(model, "__fields__"):
                    # Pydantic v1
                    for field_name, field_info in model.__fields__.items():
                        # Only include common input fields and skip special fields
                        if (
                            field_name not in input_field_names
                            or field_name.startswith("__")
                        ):
                            continue

                        # Skip runnable_config
                        if (
                            field_name == "__runnable_config__"
                            or field_name == "runnable_config"
                        ):
                            continue

                        # Get field type and defaults
                        field_type = field_info.type_

                        # Handle default vs default_factory
                        if field_info.default_factory is not None:
                            default_factory = field_info.default_factory
                            default = None
                        else:
                            default_factory = None
                            default = field_info.default

                        # Add the field
                        composer.add_field(
                            name=field_name,
                            field_type=field_type,
                            default=default,
                            default_factory=default_factory,
                            description=field_info.description,
                            source=source,
                        )

        # Add standard input fields if not already present
        from typing import List, Optional

        from langchain_core.messages import BaseMessage

        # Always ensure we have a messages field
        if "messages" not in composer.fields:
            composer.add_field(
                name="messages",
                field_type=List[BaseMessage],
                default_factory=list,
                description="Messages for agent conversation",
            )

        # Create model directly instead of using StateSchema as base
        field_defs = {}
        for name, field_def in composer.fields.items():
            field_type, field_info = field_def.to_field_info()
            field_defs[name] = (field_type, field_info)

        # Create the input schema
        return create_model(name, **field_defs)

    @classmethod
    def compose_output_schema(
        cls, components: List[Any], name: str = "OutputSchema"
    ) -> Type[BaseModel]:
        """
        Create an output schema from components, focusing on output fields.

        Args:
            components: List of components to extract fields from
            name: Name for the schema

        Returns:
            BaseModel subclass optimized for output
        """
        composer = cls(name=name)

        # Process each component
        for component in components:
            if component is None:
                continue

            # Only extract output fields from engines
            if hasattr(component, "engine_type") and hasattr(
                component, "get_output_fields"
            ):
                try:
                    # Extract output fields
                    output_fields = component.get_output_fields()
                    engine_name = getattr(component, "name", str(component))

                    for field_name, (field_type, field_info) in output_fields.items():
                        # Skip if already has this field
                        if field_name in composer.fields:
                            continue

                        # Skip special fields
                        if (
                            field_name == "__runnable_config__"
                            or field_name == "runnable_config"
                        ):
                            continue

                        # Get default and default_factory
                        if (
                            hasattr(field_info, "default")
                            and field_info.default is not ...
                        ):
                            default = field_info.default
                        else:
                            default = None

                        default_factory = getattr(field_info, "default_factory", None)
                        description = getattr(field_info, "description", None)

                        # Add the field
                        composer.add_field(
                            name=field_name,
                            field_type=field_type,
                            default=default,
                            default_factory=default_factory,
                            description=description,
                            source=engine_name,
                        )

                        # Track as output field
                        composer.output_fields[engine_name].add(field_name)

                    # Add structured output model if available
                    if (
                        hasattr(component, "structured_output_model")
                        and component.structured_output_model
                    ):
                        model = component.structured_output_model
                        model_name = model.__name__.lower()

                        # Store the model
                        composer.structured_models[model_name] = model

                        # Add field for the model
                        from typing import Optional

                        composer.add_field(
                            name=model_name,
                            field_type=Optional[model],
                            default=None,
                            description=f"Output in {model.__name__} format",
                            source=engine_name,
                        )

                        # Track as output field
                        composer.output_fields[engine_name].add(model_name)

                    # Update engine IO mapping
                    composer.engine_io_mappings[engine_name] = {
                        "inputs": [],
                        "outputs": list(composer.output_fields[engine_name]),
                    }
                except Exception as e:
                    logger.warning(
                        f"Error extracting output fields from {component}: {e}"
                    )

        # Add standard output fields if not already present
        from typing import Any, Dict, List, Optional

        from langchain_core.messages import BaseMessage

        # Always ensure we have a messages field
        if "messages" not in composer.fields:
            composer.add_field(
                name="messages",
                field_type=List[BaseMessage],
                default_factory=list,
                description="Messages from agent conversation",
            )

        # Add a content field if no structured output model is present
        has_structured_output = any(composer.structured_models)

        # Create model directly instead of using StateSchema as base
        field_defs = {}
        for name, field_def in composer.fields.items():
            field_type, field_info = field_def.to_field_info()
            field_defs[name] = (field_type, field_info)

        # Create the output schema
        return create_model(name, **field_defs)

    @classmethod
    def create_message_state(
        cls,
        additional_fields: Optional[Dict[str, Any]] = None,
        name: str = "MessageState",
    ) -> Type[StateSchema]:
        """
        Create a schema with messages field and additional fields.

        Args:
            additional_fields: Optional dictionary of additional fields to add
            name: Name for the schema

        Returns:
            StateSchema subclass with messages field
        """
        # Create composer
        composer = cls(name=name)

        # Add messages field with reducer
        from typing import List, Sequence

        try:
            from langchain_core.messages import BaseMessage
            from langgraph.graph import add_messages

            # Add messages field with reducer
            composer.add_field(
                name="messages",
                field_type=Sequence[BaseMessage],
                default_factory=list,
                description="Messages for conversation",
                reducer=add_messages,
            )
        except ImportError:
            # Fallback if add_messages is not available
            from typing import Any

            # Create simple concat lists reducer
            def concat_lists(a, b):
                return (a or []) + (b or [])

            composer.add_field(
                name="messages",
                field_type=List[Any],
                default_factory=list,
                description="Messages for conversation",
                reducer=concat_lists,
            )

        # Add additional fields
        if additional_fields:
            for name, value in additional_fields.items():
                if isinstance(value, tuple) and len(value) >= 2:
                    field_type, default = value[0], value[1]

                    # Check if default is a factory
                    default_factory = None
                    if callable(default) and not isinstance(default, type):
                        default_factory = default
                        default = None

                    composer.add_field(
                        name=name,
                        field_type=field_type,
                        default=default,
                        default_factory=default_factory,
                    )
                else:
                    # Infer type from value
                    composer.add_field(name=name, field_type=type(value), default=value)

        # Build schema
        return composer.build()

    @classmethod
    def create_state_from_io_schemas(
        cls,
        input_schema: Type[BaseModel],
        output_schema: Type[BaseModel],
        name: str = "ComposedStateSchema",
    ) -> Type[StateSchema]:
        """
        Create a state schema that combines input and output schemas.

        Args:
            input_schema: Input schema class
            output_schema: Output schema class
            name: Name for the composed schema

        Returns:
            StateSchema subclass that inherits from both input and output schemas
        """
        from typing import List

        from langchain_core.messages import BaseMessage

        # Create composer
        composer = cls(name=name)

        # Add a messages field with reducer first
        try:
            from langgraph.graph import add_messages

            composer.add_field(
                name="messages",
                field_type=List[BaseMessage],
                default_factory=list,
                description="Messages for conversation",
                reducer=add_messages,
                shared=True,
            )
        except ImportError:
            # Fallback if add_messages is not available
            def concat_lists(a, b):
                return (a or []) + (b or [])

            composer.add_field(
                name="messages",
                field_type=List[BaseMessage],
                default_factory=list,
                description="Messages for conversation",
                reducer=concat_lists,
                shared=True,
            )

        # Add fields from input schema
        composer.add_fields_from_model(input_schema)

        # Add fields from output schema
        composer.add_fields_from_model(output_schema)

        # Create field definitions for the model including the base classes
        field_defs = {}
        for name, field_def in composer.fields.items():
            # Skip if field is already in a base class
            if (
                hasattr(input_schema, "model_fields")
                and name in input_schema.model_fields
            ):
                continue
            if (
                hasattr(output_schema, "model_fields")
                and name in output_schema.model_fields
            ):
                continue

            field_type, field_info = field_def.to_field_info()
            field_defs[name] = (field_type, field_info)

        # Create the schema that inherits from both input and output schemas
        schema = create_model(
            name, __base__=(StateSchema, input_schema, output_schema), **field_defs
        )

        # Configure StateSchema features
        schema.__shared_fields__ = list(composer.shared_fields)

        # Add reducers
        schema.__serializable_reducers__ = {}
        schema.__reducer_fields__ = {}

        for name, field_def in composer.fields.items():
            if field_def.reducer:
                reducer_name = field_def.get_reducer_name()
                schema.__serializable_reducers__[name] = reducer_name
                schema.__reducer_fields__[name] = field_def.reducer

        # Deep copy the engine I/O mappings
        schema.__engine_io_mappings__ = {}
        for engine_name, mapping in composer.engine_io_mappings.items():
            schema.__engine_io_mappings__[engine_name] = mapping.copy()

        # Convert sets to lists for input/output fields
        schema.__input_fields__ = {}
        for engine_name, fields in composer.input_fields.items():
            schema.__input_fields__[engine_name] = list(fields)

        schema.__output_fields__ = {}
        for engine_name, fields in composer.output_fields.items():
            schema.__output_fields__[engine_name] = list(fields)

        # Set structured model info
        if composer.structured_model_fields:
            schema.__structured_model_fields__ = {
                k: list(v) for k, v in composer.structured_model_fields.items()
            }

        if composer.structured_models:
            schema.__structured_models__ = {
                k: f"{v.__module__}.{v.__name__}"
                for k, v in composer.structured_models.items()
            }

        return schema

    def compose_state_from_io(
        self, input_schema: Type[BaseModel], output_schema: Type[BaseModel]
    ) -> Type[StateSchema]:
        """
        Compose a state schema from input and output schemas using this composer.

        Args:
            input_schema: Input schema class
            output_schema: Output schema class

        Returns:
            StateSchema subclass
        """
        # Add fields from input schema if not already present
        for field_name, field_def in self.fields.items():
            if (
                field_name not in input_schema.model_fields
                and field_name not in output_schema.model_fields
            ):
                continue

        # Add remaining fields from input schema
        self.add_fields_from_model(input_schema)

        # Add remaining fields from output schema
        self.add_fields_from_model(output_schema)

        # Build the final schema
        return self.build()

    # src/haive/core/schema/schema_composer.py

    # Add this method to the SchemaComposer class

    def extract_tool_schemas(self, tools: List[Any]) -> None:
        """
        Extract input and output schemas from tools.

        Args:
            tools: List of tools to analyze
        """
        for tool in tools:
            # Get tool name
            tool_name = getattr(tool, "name", None)
            if not tool_name and hasattr(tool, "__name__"):
                tool_name = tool.__name__

            if not tool_name:
                continue

            # Extract input schema
            input_schema = None

            # Check for args_schema on instance or class
            if hasattr(tool, "args_schema"):
                input_schema = tool.args_schema

            # For class types, try to instantiate
            elif isinstance(tool, type):
                if issubclass(tool, BaseTool):
                    try:
                        instance = tool()
                        if hasattr(instance, "args_schema"):
                            input_schema = instance.args_schema
                    except Exception:
                        pass

            # For BaseModel types
            if isinstance(tool, type) and issubclass(tool, BaseModel):
                input_schema = tool

            # Add input schema field if found
            if (
                input_schema
                and isinstance(input_schema, type)
                and issubclass(input_schema, BaseModel)
            ):
                # Add to tool_schemas dictionary in state
                self.add_field(
                    name=f"tool_schemas.{tool_name}",
                    field_type=Type[BaseModel],
                    default=input_schema,
                    description=f"Schema for {tool_name}",
                )

                # Try to find matching output schema
                output_class_name = None
                input_class_name = input_schema.__name__

                # Common naming patterns for output schemas
                possible_names = [
                    f"{tool_name.capitalize()}Result",
                    f"{tool_name.capitalize()}Output",
                    f"{input_class_name}Result",
                    f"{input_class_name}Output",
                    f"{input_class_name.replace('Input', '')}Result",
                    f"{input_class_name.replace('Query', '')}Result",
                ]

                # Look in surrounding module
                if hasattr(input_schema, "__module__"):
                    module = sys.modules.get(input_schema.__module__)
                    if module:
                        for name in possible_names:
                            if hasattr(module, name):
                                output_class = getattr(module, name)
                                if isinstance(output_class, type) and issubclass(
                                    output_class, BaseModel
                                ):
                                    # Add to output_schemas
                                    self.add_field(
                                        name=f"output_schemas.{name}",
                                        field_type=Type[BaseModel],
                                        default=output_class,
                                        description=f"Output schema for {tool_name}",
                                    )

                                    # Add tool_name attribute to schema
                                    setattr(output_class, "tool_name", tool_name)
                                    break

        # Add tool field to track tool instances
        self.add_field(
            name="tools",
            field_type=Dict[str, Any],
            default_factory=dict,
            description="Tool instances indexed by name",
        )
