"""State schema base class for the Haive framework.

This module provides the StateSchema base class that extends Pydantic's BaseModel
with features specifically designed for AI agent state management and graph-based
workflows. The StateSchema class adds powerful capabilities including field sharing
between parent and child graphs, reducer functions for state updates, engine I/O
tracking, and extensive serialization support.

StateSchema serves as the foundation of the Haive Schema System, enabling fully
dynamic and serializable state schemas that can be composed, modified, and extended
at runtime. This flexibility makes it ideal for complex agent architectures and
nested workflows.

Key features include:
- Field sharing: Share state between parent and child graphs with explicit control
- Reducer functions: Define how field values should be combined during state updates
- Engine I/O tracking: Map which fields are inputs and outputs for specific engines
- Message handling: Built-in methods for working with message fields
- Serialization: Comprehensive support for converting to/from dictionaries and JSON
- State manipulation: Methods for updating, merging, and comparing states
- Pretty printing: Rich visualization of state content
- Engine integration: Prepare inputs and process outputs for specific engines

Example:
    ```python
    from typing import List
    from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
    from pydantic import Field
    from haive.core.schema import StateSchema
    from langgraph.graph import add_messages

    class ConversationState(StateSchema):
        messages: List[BaseMessage] = Field(default_factory=list)
        query: str = Field(default="")
        response: str = Field(default="")
        context: List[str] = Field(default_factory=list)

        # Define which fields should be shared with parent graphs
        __shared_fields__ = ["messages"]

        # Define reducer functions for each field
        __reducer_fields__ = {
            "messages": add_messages,
            "context": lambda a, b: (a or []) + (b or [])
        }

        # Define which fields are inputs/outputs for which engines
        __engine_io_mappings__ = {
            "retriever": {
                "inputs": ["query"],
                "outputs": ["context"]
            },
            "llm": {
                "inputs": ["query", "context", "messages"],
                "outputs": ["response"]
            }
        }
    ```
"""

from __future__ import annotations

import copy
import json
import logging
import uuid
from typing import (
    TYPE_CHECKING,
    Any,
    Awaitable,
    Callable,
    Dict,
    Generic,
    List,
    Optional,
    Set,
    Tuple,
    Type,
    TypeVar,
    Union,
    cast,
    overload,
)

from langchain_core.messages import BaseMessage
from langchain_core.runnables import RunnableConfig
from pydantic import BaseModel, Field, create_model, field_validator, model_validator
from rich.panel import Panel
from rich.syntax import Syntax
from rich.table import Table
from rich.tree import Tree
from typing_extensions import (
    Literal,
    NotRequired,
    Required,
    Self,
    TypeAlias,
    TypedDict,
    TypeGuard,
)

from haive.core.logging.rich_logger import RichLogger, get_logger

# Get logger instance
logger = get_logger(__name__)

if TYPE_CHECKING:
    from haive.core.schema.schema_manager import StateSchemaManager

# Import Engine at runtime for type resolution in postponed annotations
# This is needed because with __future__ annotations, type hints become strings
# and LangGraph's get_type_hints() needs Engine in the global namespace
from haive.core.engine.base import Engine

# Type variables for generic state schema
T = TypeVar("T", bound=BaseModel)
TEngine = TypeVar("TEngine", bound=Engine)
TEngines = TypeVar("TEngines", bound=Dict[str, Engine])
TStateSchema = TypeVar("TStateSchema", bound="StateSchema")

# Type aliases for better API clarity
FieldName: TypeAlias = str
FieldValue: TypeAlias = Any
FieldMapping: TypeAlias = Dict[FieldName, FieldValue]
ReducerFunction: TypeAlias = Callable[[Any, Any], Any]
ValidatorFunction: TypeAlias = Callable[[Any], Any]
EngineMapping: TypeAlias = Dict[str, Engine]
FieldList: TypeAlias = List[FieldName]
IOMapping: TypeAlias = Dict[str, Dict[str, FieldList]]


# Structured configuration types
class EngineIOConfig(TypedDict, total=False):
    """Configuration for engine input/output mappings."""

    inputs: NotRequired[FieldList]
    outputs: NotRequired[FieldList]


class StateConfig(TypedDict, total=False):
    """Configuration for state schema metadata."""

    shared_fields: NotRequired[FieldList]
    reducers: NotRequired[Dict[FieldName, str]]
    engine_io: NotRequired[Dict[str, EngineIOConfig]]
    structured_models: NotRequired[Dict[str, str]]


class StateSchema(BaseModel, Generic[TEngine, TEngines]):
    """Enhanced base class for state schemas in the Haive framework.

    StateSchema extends Pydantic's BaseModel with features for AI agent state management
    and graph-based workflows. It serves as the core component of the Haive Schema System,
    providing extensive capabilities for state management in complex agent architectures.

    Key Features:
        - Field sharing: Control which fields are shared between parent and child graphs
        - Reducer functions: Define how field values are combined during state updates
        - Engine I/O tracking: Map which fields are inputs/outputs for which engines
        - Message handling: Methods for working with conversation message fields
        - Serialization: Convert states to/from dictionaries and JSON
        - State manipulation: Update, merge, compare, and diff state objects
        - Integration: Support for LangGraph and engine components
        - Visualization: Rich display options for state inspection

    Special Class Variables:
        __shared_fields__ (List[str]): Fields to share with parent graphs
        __serializable_reducers__ (Dict[str, str]): Serializable reducer function names
        __engine_io_mappings__ (Dict[str, Dict[str, List[str]]]): Engine I/O mappings
        __input_fields__ (Dict[str, List[str]]): Input fields for each engine
        __output_fields__ (Dict[str, List[str]]): Output fields for each engine
        __structured_models__ (Dict[str, str]): Paths to structured output models
        __structured_model_fields__ (Dict[str, List[str]]): Fields for structured models
        __reducer_fields__ (Dict[str, Callable]): Runtime reducer functions (not stored)

    Field sharing enables parent and child graphs to maintain synchronized state for
    specific fields, which is critical for nested graph execution. Reducer functions
    define how field values are combined during updates, enabling sophisticated state
    merging operations beyond simple assignment.

    Example:
        ```python
        from typing import List
        from langchain_core.messages import BaseMessage
        from pydantic import Field
        from haive.core.schema import StateSchema

        class MyState(StateSchema):
            messages: List[BaseMessage] = Field(default_factory=list)
            query: str = Field(default="")
            result: str = Field(default="")

            # Share only messages with parent graphs
            __shared_fields__ = ["messages"]

            # Define reducer for messages
            __reducer_fields__ = {
                "messages": add_messages  # From langgraph.graph
            }

        # Create state instance
        state = MyState()

        # Add a message
        state.add_message(HumanMessage(content="Hello"))

        # Convert to dictionary
        state_dict = state.to_dict()

        # Create from dictionary
        new_state = MyState.from_dict(state_dict)
        ```
    """

    # Class variables to track field sharing and reducers
    __shared_fields__: FieldList = []
    __serializable_reducers__: Dict[FieldName, str] = {}
    __engine_io_mappings__: IOMapping = {}
    __input_fields__: Dict[str, FieldList] = {}
    __output_fields__: Dict[str, FieldList] = {}
    __structured_models__: Dict[str, str] = {}
    __structured_model_fields__: Dict[str, FieldList] = {}

    # Note: __reducer_fields__ is created dynamically and not part of instance properties

    # Optional convenience fields for better engine management
    # Generic typing allows concrete engine types to be resolved
    engine: Optional[TEngine] = Field(
        default=None, description="Optional main/primary engine for convenience"
    )

    engines: TEngines = Field(
        default_factory=dict,  # type: ignore[arg-type]
        description="Engine registry for this state - supports easy addition",
    )

    @field_validator("engine", mode="before")
    @classmethod
    def validate_engine(cls, v):
        """Handle both serialized dict and actual Engine instances.

        This validator allows the engine field to accept both:
        - Actual Engine instances (for runtime use)
        - Serialized dicts (for state passing between agents)

        This prevents the "Can't instantiate abstract class Engine" error
        when deserializing state in multi-agent systems.
        """
        if v is None:
            return None
        if isinstance(v, dict):
            # It's a serialized engine - keep as dict to avoid instantiation
            return v
        # Otherwise assume it's an actual Engine instance
        return v

    @field_validator("engines", mode="before")
    @classmethod
    def validate_engines(cls, v):
        """Handle both serialized dicts and actual Engine instances in engines dict.

        Similar to validate_engine but for the engines dictionary.
        Each value can be either a serialized dict or an actual Engine instance.
        """
        if not isinstance(v, dict):
            return v

        # Process each engine in the dict
        result = {}
        for key, engine in v.items():
            if isinstance(engine, dict) or engine is None:
                # Keep serialized engines as dicts
                result[key] = engine
            else:
                # Keep actual Engine instances as-is
                result[key] = engine

        return result

    # Convenience properties for accessing engines
    @property
    def llm(self) -> Optional[Engine]:
        """Convenience property to access the LLM engine."""
        # First check the main engine field
        if self.engine and hasattr(self.engine, "engine_type"):
            engine_type_str = str(self.engine.engine_type).lower()
            if "llm" in engine_type_str:
                return self.engine

        # Then check engines dict for LLM
        for name, eng in self.engines.items():
            if hasattr(eng, "engine_type"):
                engine_type_str = str(eng.engine_type).lower()
                if "llm" in engine_type_str:
                    return eng

        return None

    @property
    def main_engine(self) -> Optional[Engine]:
        """Convenience property to access the main engine."""
        return self.engine or self.engines.get("main")

    def add_engine(self, name: str, engine: Engine) -> None:
        """Add an engine to the engines registry.

        Args:
            name: Name/key for the engine
            engine: Engine instance to add
        """
        if not hasattr(self, "engines") or self.engines is None:
            self.engines = {}
        self.engines[name] = engine

    def get_engine(self, name: str) -> Optional[Engine]:
        """Get an engine by name.

        Args:
            name: Name of the engine to retrieve

        Returns:
            Engine instance if found, None otherwise
        """
        if hasattr(self, "engines") and self.engines:
            return self.engines.get(name)
        return None

    def has_engine(self, name: str) -> bool:
        """Check if an engine exists.

        Args:
            name: Name of the engine to check

        Returns:
            True if engine exists, False otherwise
        """
        return self.get_engine(name) is not None

    def remove_engine(self, name: str) -> bool:
        """Remove an engine from the registry.

        Args:
            name: Name of the engine to remove

        Returns:
            True if engine was removed, False if not found
        """
        if hasattr(self, "engines") and self.engines and name in self.engines:
            del self.engines[name]
            return True
        return False

    def list_engines(self) -> List[str]:
        """Get list of all engine names.

        Returns:
            List of engine names
        """
        if hasattr(self, "engines") and self.engines:
            return list(self.engines.keys())
        return []

    def model_dump(self, **kwargs: Any) -> FieldMapping:
        """
        Override model_dump to exclude internal fields and handle special types.

        Args:
            **kwargs: Keyword arguments for model_dump

        Returns:
            Dictionary representation of the state
        """
        # Get the base model_dump result from Pydantic v2
        data = super().model_dump(**kwargs)

        # Filter out internal fields
        internal_fields = [
            "__shared_fields__",
            "__serializable_reducers__",
            "__reducer_fields__",
            "__engine_io_mappings__",
            "__input_fields__",
            "__output_fields__",
            "__structured_models__",
            "__structured_model_fields__",
        ]
        for field in internal_fields:
            if field in data:
                data.pop(field)

        return data

    @model_validator(mode="after")
    def setup_engines_and_tools(self) -> Self:
        """
        Setup engines and sync their tools, structured output models, and add engine to state.

        This validator runs after the model is created and:
        1. Finds all engine fields in the state
        2. Syncs engine to main engine field and engines dict
        3. Syncs tools from engine to state tools field
        4. Syncs structured output models
        5. Sets up parent-child relationships for nested state schemas
        """
        logger.debug(f"Setting up engines for {self.__class__.__name__}")

        # Track engines for debugging
        found_engines = []

        # Find engine fields
        for field_name, field_value in self.__dict__.items():
            # Skip None values and non-engine fields
            if field_value is None:
                continue

            # Check if field is an engine
            if hasattr(field_value, "engine_type"):
                engine_name = getattr(field_value, "name", field_name)
                found_engines.append(engine_name)

                # 1. Add engine to engines dict
                if engine_name not in self.engines:
                    self.engines[engine_name] = field_value
                    logger.debug(f"Added engine '{engine_name}' to engines dict")

                # 2. Set as main engine if we don't have one
                if self.engine is None:
                    self.engine = field_value
                    logger.debug(f"Set engine '{engine_name}' as main engine")

                # 3. Sync tools if engine has tools and we have a tools field
                if hasattr(field_value, "tools") and hasattr(self, "tools"):
                    engine_tools = getattr(field_value, "tools", [])
                    logger.debug(
                        f"Found engine '{engine_name}' with {len(engine_tools)} tools"
                    )

                    # Initialize tools list if None
                    if self.tools is None:
                        self.tools = []

                    # Add engine tools to our tools list if not already there
                    for tool in engine_tools:
                        if tool not in self.tools:
                            tool_name = getattr(tool, "name", str(tool))
                            logger.debug(
                                f"Adding tool '{tool_name}' from engine '{engine_name}'"
                            )
                            self.tools.append(tool)

                # 4. Sync structured output model if present
                if (
                    hasattr(field_value, "structured_output_model")
                    and field_value.structured_output_model
                ):
                    if hasattr(self, "structured_output_model"):
                        if self.structured_output_model is None:
                            self.structured_output_model = (
                                field_value.structured_output_model
                            )
                            logger.debug(
                                f"Synced structured output model from engine '{engine_name}'"
                            )

            # Check if field is another StateSchema for recursive handling
            elif isinstance(field_value, StateSchema):
                nested_schema_name = field_value.__class__.__name__
                logger.debug(
                    f"Found nested schema '{nested_schema_name}' in field '{field_name}'"
                )

                # Handle shared fields between parent and child schemas
                self._sync_shared_fields(field_value, field_name)

        if found_engines:
            logger.debug(
                f"Found engines in {self.__class__.__name__}: {', '.join(found_engines)}"
            )

        return self

    def _sync_shared_fields(self, child_schema: "StateSchema", field_name: str) -> None:
        """
        Sync shared fields between parent and child schemas.

        Args:
            child_schema: Child StateSchema instance
            field_name: Field name in the parent schema
        """
        # Get shared fields from child schema
        child_shared = getattr(child_schema.__class__, "__shared_fields__", [])

        for shared_field in child_shared:
            # Check if child has this field
            if hasattr(child_schema, shared_field):
                # Get child field value
                child_value = getattr(child_schema, shared_field)

                # Check if parent has this field
                if hasattr(self, shared_field):
                    # Get parent field value
                    parent_value = getattr(self, shared_field)

                    # Check for reducers
                    reducer_fields = getattr(self.__class__, "__reducer_fields__", {})

                    if shared_field in reducer_fields:
                        # Apply reducer to combine values
                        reducer = reducer_fields[shared_field]
                        try:
                            combined_value = reducer(parent_value, child_value)
                            # Update both parent and child
                            setattr(self, shared_field, combined_value)
                            setattr(child_schema, shared_field, combined_value)
                            logger.debug(
                                f"Synced shared field '{shared_field}' between parent and '{field_name}' using reducer"
                            )
                        except Exception as e:
                            logger.warning(
                                f"Error applying reducer for shared field '{shared_field}': {e}"
                            )
                    else:
                        # Default to parent value for now (will be overridden by reducer later if needed)
                        setattr(child_schema, shared_field, parent_value)
                        logger.debug(
                            f"Synced shared field '{shared_field}' from parent to '{field_name}'"
                        )

    @model_validator(mode="after")
    def sync_engine_fields(self) -> "StateSchema":
        """Sync between engine and engines dict for backward compatibility.

        This validator ensures that:
        1. If 'engine' is set, it's available in engines dict
        2. If engines dict has items but no engine, set main engine
        3. Both access patterns work seamlessly
        """
        # If engine is provided, ensure it's in engines dict
        if self.engine:
            # Add as 'main' if not already there
            if "main" not in self.engines:
                self.engines["main"] = self.engine

            # Add by engine name if available
            if hasattr(self.engine, "name") and self.engine.name:
                if self.engine.name not in self.engines:
                    self.engines[self.engine.name] = self.engine

            # Add by engine type if available
            if hasattr(self.engine, "engine_type"):
                engine_type = str(self.engine.engine_type)
                # Remove "EngineType." prefix if present
                if "." in engine_type:
                    engine_type = engine_type.split(".")[-1].lower()
                if engine_type not in self.engines:
                    self.engines[engine_type] = self.engine

        # If no engine but engines dict has 'main', sync back
        elif not self.engine and self.engines.get("main"):
            self.engine = self.engines["main"]

        # If no engine but engines dict has one item, use it as main
        elif not self.engine and len(self.engines) == 1:
            self.engine = next(iter(self.engines.values()))

        return self

    def model_post_init(self, __context: Any) -> None:
        """Sync engines from class level to instance level after initialization.

        This ensures that engines stored at the class level (via SchemaComposer)
        are available on state instances.
        """
        # Check if class has engines and sync them to instance
        if hasattr(self.__class__, "engines") and self.__class__.engines:
            logger.debug(
                f"Syncing {len(self.__class__.engines)} engines from class to instance"
            )

            # Update instance engines dict with class engines
            for engine_name, engine in self.__class__.engines.items():
                if engine_name not in self.engines:
                    self.engines[engine_name] = engine
                    logger.debug(f"Synced engine '{engine_name}' from class")

            # Set main engine if not already set
            if self.engine is None and self.engines:
                # Try 'main' first, then any engine
                if "main" in self.engines:
                    self.engine = self.engines["main"]
                    logger.debug("Set main engine from class engines")
                else:
                    # Use first available engine
                    first_engine = next(iter(self.engines.values()))
                    self.engine = first_engine
                    logger.debug(
                        f"Set first available engine as main: {getattr(first_engine, 'name', 'unnamed')}"
                    )

    def dict(self, **kwargs) -> Dict[str, Any]:
        """
        Backwards compatibility alias for model_dump.

        Args:
            **kwargs: Keyword arguments for model_dump

        Returns:
            Dictionary representation of the state
        """
        return self.model_dump(**kwargs)

    def to_dict(self) -> FieldMapping:
        """
        Convert the state to a clean dictionary.

        Returns:
            Dictionary representation of the state
        """
        return self.model_dump()

    def to_json(self) -> str:
        """
        Convert state to JSON string.

        Returns:
            JSON string representation of the state
        """
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> "StateSchema":
        """
        Create state from JSON string.

        Args:
            json_str: JSON string to parse

        Returns:
            New StateSchema instance
        """
        data = json.loads(json_str)
        return cls.from_dict(data)

    @classmethod
    def from_dict(cls, data: FieldMapping) -> Self:
        """
        Create a state from a dictionary.

        Args:
            data: Dictionary with field values

        Returns:
            New StateSchema instance
        """
        # Filter out internal fields if present
        internal_fields = [
            "__shared_fields__",
            "__serializable_reducers__",
            "__reducer_fields__",
            "__engine_io_mappings__",
            "__input_fields__",
            "__output_fields__",
            "__structured_models__",
            "__structured_model_fields__",
        ]
        clean_data = {k: v for k, v in data.items() if k not in internal_fields}

        # Use Pydantic v2 method for validation
        return cls.model_validate(clean_data)

    @classmethod
    def from_partial_dict(cls, data: Dict[str, Any]) -> "StateSchema":
        """
        Create a state from a partial dictionary, filling in defaults.

        Args:
            data: Partial dictionary with field values

        Returns:
            New StateSchema instance with defaults applied
        """
        # Get defaults from model fields
        full_data = {}
        for field_name, field_info in cls.model_fields.items():
            # Get default and default_factory
            default = field_info.default
            default_factory = field_info.default_factory

            # Apply defaults
            if default is not ...:
                full_data[field_name] = default
            elif default_factory is not None:
                full_data[field_name] = default_factory()

        # Update with provided data
        full_data.update(data)

        # Create instance with Pydantic v2 method
        return cls.model_validate(full_data)

    def get_engine(self, name: str) -> Optional[Any]:
        """
        Get an engine by name from any engine fields.

        Args:
            name: Name of the engine to retrieve

        Returns:
            Engine instance if found, None otherwise
        """
        logger.debug(f"Looking for engine: {name}")

        # First check engines dict
        if name in self.engines:
            logger.debug(f"Found engine '{name}' in engines dict")
            return self.engines[name]

        # Then try by field name
        if hasattr(self, name):
            field_value = getattr(self, name)
            if hasattr(field_value, "engine_type"):
                logger.debug(f"Found engine '{name}' by field name")
                return field_value

        # Then try by engine name attribute
        for field_name, field_value in self.__dict__.items():
            if field_value is None:
                continue

            if hasattr(field_value, "engine_type") and field_name not in [
                "engine",
                "engines",
            ]:
                engine_name = getattr(field_value, "name", "")
                if engine_name == name:
                    logger.debug(f"Found engine '{name}' in field '{field_name}'")
                    return field_value

        logger.debug(f"Engine '{name}' not found")
        return None

    def get_engines(self) -> Dict[str, Any]:
        """
        Get all engines in this state.

        Returns:
            Dictionary mapping engine names to engine instances
        """
        engines = {}

        # First add engines from the engines dict
        engines.update(self.engines)

        # Then find engine fields (for backward compatibility)
        for field_name, field_value in self.__dict__.items():
            if field_value is None:
                continue

            if hasattr(field_value, "engine_type") and field_name not in [
                "engine",
                "engines",
            ]:
                engine_name = getattr(field_value, "name", field_name)
                engines[engine_name] = field_value

        return engines

    def has_engine(self, name: str) -> bool:
        """
        Check if an engine exists in this state.

        Args:
            name: Name of the engine to check

        Returns:
            True if engine exists, False otherwise
        """
        return self.get_engine(name) is not None

    @classmethod
    def get_class_engine(cls, name: str) -> Optional[Any]:
        """
        Get a class-level engine by name.

        Args:
            name: Name of the engine to retrieve

        Returns:
            Engine instance if found, None otherwise
        """
        if hasattr(cls, "engines") and name in cls.engines:
            return cls.engines[name]
        return None

    @classmethod
    def get_all_class_engines(cls) -> Dict[str, Any]:
        """
        Get all class-level engines.

        Returns:
            Dictionary of all engines
        """
        if hasattr(cls, "engines"):
            return cls.engines
        return {}

    def get_instance_engine(self, name: str) -> Optional[Any]:
        """
        Get an engine from instance or class level.

        Args:
            name: Name of the engine to retrieve

        Returns:
            Engine instance if found, None otherwise
        """
        # First check instance fields
        if hasattr(self, name):
            field_value = getattr(self, name)
            if hasattr(field_value, "engine_type"):
                return field_value

        # Then check class-level engines
        if hasattr(self.__class__, "engines") and name in self.__class__.engines:
            return self.__class__.engines[name]

        # Then try by engine name attribute in instance fields
        for field_name, field_value in self.__dict__.items():
            if field_value is None:
                continue
            if hasattr(field_value, "engine_type"):
                engine_name = getattr(field_value, "name", "")
                if engine_name == name:
                    return field_value

        return None

    def get_all_instance_engines(self) -> Dict[str, Any]:
        """
        Get all engines from both instance and class level.

        Returns:
            Dictionary mapping engine names to engine instances
        """
        engines = {}

        # Get class-level engines first
        if hasattr(self.__class__, "engines"):
            engines.update(self.__class__.engines)

        # Then add instance-level engines (may override class engines)
        for field_name, field_value in self.__dict__.items():
            if field_value is None:
                continue
            if hasattr(field_value, "engine_type"):
                engine_name = getattr(field_value, "name", field_name)
                engines[engine_name] = field_value

        return engines

    def get_state_values(
        self, keys: Union[List[str], Dict[str, str], None] = None
    ) -> Dict[str, Any]:
        """
        Extract specified state values into a dictionary.

        Args:
            keys: Can be:
                - List[str]: List of field names to extract
                - Dict[str, str]: Mapping of output keys to state field names
                - None: Extract all fields

        Returns:
            Dictionary containing the requested state values
        """
        result = {}

        # Handle dictionary mapping case
        if isinstance(keys, dict):
            for output_key, field_name in keys.items():
                if hasattr(self, field_name):
                    result[output_key] = getattr(self, field_name)
                else:
                    # Optional: add warning/default handling for missing fields
                    logger.debug(f"Field not found: {field_name}")
                    result[output_key] = None
            return result

        # Handle list of keys case
        elif isinstance(keys, list):
            for field_name in keys:
                if hasattr(self, field_name):
                    result[field_name] = getattr(self, field_name)

        # Handle None case - extract all fields
        else:
            # Use model_dump to get all fields
            result = self.model_dump()

            # Filter out internal fields and other excluded fields
            excluded_fields = ["tool_types_dict"]
            for field in list(result.keys()):
                if field.startswith("__") or field in excluded_fields:
                    result.pop(field, None)

        return result

    @classmethod
    def extract_values(
        cls,
        state: Union["StateSchema", Dict[str, Any]],
        keys: Union[List[str], Dict[str, str], None] = None,
    ) -> Dict[str, Any]:
        """
        Class method to extract values from a state object or dictionary.

        Args:
            state: State object or dictionary to extract values from
            keys: Can be:
                - List[str]: List of field names to extract
                - Dict[str, str]: Mapping of output keys to state field names
                - None: Extract all fields

        Returns:
            Dictionary containing the requested values
        """
        # Log extraction request
        key_str = str(keys) if keys else "all fields"
        logger.debug(f"Extracting values ({key_str}) from {type(state).__name__}")

        # If state is already a StateSchema instance, use its get_state_values method
        if isinstance(state, cls):
            return state.get_state_values(keys)

        # If state is a dictionary
        if isinstance(state, dict):
            result = {}

            # Handle dictionary mapping case
            if isinstance(keys, dict):
                for output_key, field_name in keys.items():
                    result[output_key] = state.get(field_name)
                return result

            # Handle list of keys case
            elif isinstance(keys, list):
                for field_name in keys:
                    if field_name in state:
                        result[field_name] = state[field_name]
                return result

            # Handle None case - return all fields
            else:
                # Make a copy to avoid modifying the original
                result = state.copy()

                # Filter out internal fields
                excluded_fields = ["tool_types_dict"]
                for field in list(result.keys()):
                    if field.startswith("__") or field in excluded_fields:
                        result.pop(field, None)

                return result

        # If state is neither a StateSchema nor a dict, return empty dict
        logger.warning(f"Cannot extract values from {type(state).__name__}")
        return {}

    def get(self, key: str, default: Any = None) -> Any:
        """
        Safely get a field value with a default.

        Args:
            key: Field name to get
            default: Default value if field doesn't exist

        Returns:
            Field value or default
        """
        if hasattr(self, key):
            return getattr(self, key)
        return default

    def update(self, other: Union[Dict[str, Any], "StateSchema"]) -> "StateSchema":
        """
        Update the state with values from another state or dictionary.

        This method performs a simple update without applying reducers.

        Args:
            other: Dictionary or StateSchema with update values

        Returns:
            Self for chaining
        """
        if isinstance(other, StateSchema):
            data = other.model_dump()
        else:
            data = other

        # Simple update without attempting to apply reducers
        for key, value in data.items():
            setattr(self, key, value)

        return self

    def apply_reducers(
        self, other: Union[Dict[str, Any], "StateSchema"]
    ) -> "StateSchema":
        """
        Update state applying reducer functions where defined.

        This method processes updates with special handling for fields
        that have reducer functions defined.

        Args:
            other: Dictionary or StateSchema with update values

        Returns:
            Self for chaining
        """
        if isinstance(other, StateSchema):
            data = other.model_dump()
        else:
            data = other

        # Get reducer functions
        reducer_fields = getattr(self.__class__, "__reducer_fields__", {})

        # Apply updates with reducers where defined
        for key, value in data.items():
            # Skip if the field doesn't exist in this state
            if not hasattr(self, key):
                # Just add the field with simple assignment
                setattr(self, key, value)
                continue

            # Get current value
            current_value = getattr(self, key)

            # Apply reducer if available for this field
            if key in reducer_fields:
                reducer = reducer_fields[key]
                try:
                    # Apply reducer and set the result
                    reduced_value = reducer(current_value, value)
                    setattr(self, key, reduced_value)
                    logger.debug(f"Applied reducer for field '{key}'")
                    continue  # Skip to next field after successful reduction
                except Exception as e:
                    logger.warning(
                        f"Error applying reducer for {key}: {e}", exc_info=True
                    )
                    # Fall through to special handling or simple assignment

            # Special handling for list values - concat them when both are lists
            if isinstance(current_value, list) and isinstance(value, list):
                merged_list = current_value + value
                setattr(self, key, merged_list)
                logger.debug(f"Merged lists for field '{key}'")
                continue

            # Special handling for dictionary values - merge them instead of replacing
            if isinstance(current_value, dict) and isinstance(value, dict):
                merged_dict = current_value.copy()
                merged_dict.update(value)
                setattr(self, key, merged_dict)
                logger.debug(f"Merged dictionaries for field '{key}'")
                continue

            # Simple assignment (no reducer or reducer failed)
            setattr(self, key, value)
            logger.debug(f"Simple assignment for field '{key}'")

        return self

    def add_message(self, message: BaseMessage) -> "StateSchema":
        """
        Add a single message to the messages field.

        Args:
            message: BaseMessage to add

        Returns:
            Self for chaining
        """
        if not hasattr(self, "messages"):
            # Create messages field if it doesn't exist
            self.messages = [message]
            return self

        # Check if we're using a reducer
        reducer_fields = getattr(self.__class__, "__reducer_fields__", {})
        if "messages" in reducer_fields:
            # Use the reducer with a single-item list
            self.messages = reducer_fields["messages"](self.messages, [message])
        else:
            # Simple append
            if isinstance(self.messages, list):
                self.messages.append(message)
            else:
                self.messages = [message]

        return self

    def add_messages(self, new_messages: List[BaseMessage]) -> "StateSchema":
        """
        Add multiple messages to the messages field.

        Args:
            new_messages: List of messages to add

        Returns:
            Self for chaining
        """
        if not hasattr(self, "messages"):
            # Create messages field if it doesn't exist
            self.messages = list(new_messages)  # Create a copy
            return self

        # Check if we're using a reducer
        reducer_fields = getattr(self.__class__, "__reducer_fields__", {})
        if "messages" in reducer_fields:
            # Use the reducer
            self.messages = reducer_fields["messages"](self.messages, new_messages)
        else:
            # Simple extend
            if isinstance(self.messages, list):
                self.messages.extend(new_messages)
            else:
                self.messages = list(new_messages)

        return self

    def merge_messages(self, new_messages: List[BaseMessage]) -> "StateSchema":
        """
        Merge new messages with existing messages using appropriate reducer.

        Args:
            new_messages: New messages to add

        Returns:
            Self for chaining
        """
        return self.add_messages(new_messages)

    def clear_messages(self) -> "StateSchema":
        """
        Clear all messages in the messages field.

        Returns:
            Self for chaining
        """
        if hasattr(self, "messages"):
            self.messages = []
        return self

    def get_last_message(self) -> Optional[BaseMessage]:
        """
        Get the last message in the messages field.

        Returns:
            Last message or None if no messages exist
        """
        if hasattr(self, "messages") and self.messages:
            return self.messages[-1]
        return None

    def copy(self, **updates) -> "StateSchema":
        """
        Create a copy of this state, optionally with updates.

        Args:
            **updates: Field values to update in the copy

        Returns:
            New StateSchema instance
        """
        # Use Pydantic v2 model_copy
        return self.model_copy(update=updates)

    def deep_copy(self) -> "StateSchema":
        """
        Create a deep copy of this state object.

        Returns:
            New StateSchema instance with deep-copied values
        """
        return copy.deepcopy(self)

    @classmethod
    def _get_reducer_registry(cls) -> Dict[str, Callable]:
        """
        Get a registry of reducer functions mapped to their names.

        Returns:
            Dictionary mapping reducer names to functions
        """
        registry = {}

        # Add standard reducers
        try:
            from langgraph.graph import add_messages

            registry["add_messages"] = add_messages
        except ImportError:
            # Create a simple concat function as fallback
            def concat_lists(a, b):
                return (a or []) + (b or [])

            registry["concat_lists"] = concat_lists

        # Add common reducer functions
        def concat_strings(a, b):
            return (a or "") + (b or "")

        registry["concat_strings"] = concat_strings

        def sum_values(a, b):
            return (a or 0) + (b or 0)

        registry["sum_values"] = sum_values

        # Add common functions
        registry["max"] = max
        registry["min"] = min

        # Add operator module reducers
        import operator

        for op_name in dir(operator):
            if not op_name.startswith("_"):
                op_func = getattr(operator, op_name)
                if callable(op_func):
                    registry[f"operator.{op_name}"] = op_func
                    registry[op_name] = (
                        op_func  # Also store without prefix for backward compatibility
                    )

        # Try to get reducer functions from class if they exist
        if hasattr(cls, "__reducer_fields__"):
            registry.update(cls.__reducer_fields__)

        # Handle lambda functions
        if "<lambda>" in cls.__serializable_reducers__.values():
            # Can't restore lambdas from name, but we can provide a generic reducer
            def generic_lambda_reducer(a, b):
                # Simple fallback implementation
                if isinstance(a, (list, tuple)) and isinstance(b, (list, tuple)):
                    return a + b
                elif isinstance(a, dict) and isinstance(b, dict):
                    result = a.copy()
                    result.update(b)
                    return result
                else:
                    # Default to returning the newer value
                    return b

            registry["<lambda>"] = generic_lambda_reducer

        return registry

    @classmethod
    def shared_fields(cls) -> List[str]:
        """
        Get the list of fields shared with parent graphs.

        Returns:
            List of shared field names
        """
        return cls.__shared_fields__

    @classmethod
    def is_shared(cls, field_name: str) -> bool:
        """
        Check if a field is shared with parent graphs.

        Args:
            field_name: Field name to check

        Returns:
            True if field is shared, False otherwise
        """
        return field_name in cls.__shared_fields__

    @classmethod
    def to_manager(cls, name: Optional[str] = None) -> "StateSchemaManager":
        """
        Convert schema class to a StateSchemaManager for further manipulation.

        Args:
            name: Optional name for the resulting manager

        Returns:
            StateSchemaManager instance
        """
        from haive.core.schema.schema_manager import StateSchemaManager

        return StateSchemaManager(cls, name=name or cls.__name__)

    @classmethod
    def manager(cls) -> "StateSchemaManager":
        """
        Get a manager for this schema (shorthand for to_manager()).

        Returns:
            StateSchemaManager instance
        """
        return cls.to_manager()

    @classmethod
    def derive_input_schema(
        cls, engine_name: Optional[str] = None, name: Optional[str] = None
    ) -> Type[BaseModel]:
        """
        Derive an input schema for the given engine from this state schema.

        This method intelligently selects the appropriate base class for the derived schema,
        using prebuilt states (MessagesState, ToolState) when appropriate instead of
        just creating a generic BaseModel.

        Args:
            engine_name: Optional name of the engine to target (default: all inputs)
            name: Optional name for the schema class

        Returns:
            A BaseModel subclass for input validation, potentially inheriting from
            MessagesState or ToolState for better compatibility
        """
        fields = {}

        # Get input field names
        if engine_name is not None and hasattr(cls, "__engine_io_mappings__"):
            if engine_name in cls.__engine_io_mappings__:
                input_fields = cls.__engine_io_mappings__[engine_name].get("inputs", [])
            else:
                input_fields = []
        elif hasattr(cls, "__input_fields__"):
            # Collect input fields across all engines
            input_fields = []
            for engine_inputs in cls.__input_fields__.values():
                input_fields.extend(engine_inputs)
        else:
            input_fields = []

        # Detect if we should use prebuilt base classes
        has_messages = "messages" in input_fields
        has_tools = "tools" in input_fields

        # Check what the current schema inherits from
        from haive.core.schema.prebuilt.messages_state import MessagesState
        from haive.core.schema.prebuilt.tool_state import ToolState

        current_is_tool_state = issubclass(cls, ToolState)
        current_is_messages_state = issubclass(cls, MessagesState)

        # Determine appropriate base class using same logic as SchemaComposer
        base_class = None
        if has_tools or current_is_tool_state:
            base_class = ToolState
            logger.debug("Using ToolState as base for derived input schema")
        elif has_messages or current_is_messages_state:
            base_class = MessagesState
            logger.debug("Using MessagesState as base for derived input schema")
        else:
            # Fall back to BaseModel for basic schemas
            base_class = BaseModel
            logger.debug("Using BaseModel as base for derived input schema")

        # Add input fields to schema
        for field_name in input_fields:
            if field_name in cls.model_fields:
                field_info = cls.model_fields[field_name]

                # Skip fields that are already defined in the base class
                if (
                    hasattr(base_class, "model_fields")
                    and field_name in base_class.model_fields
                ):
                    logger.debug(
                        f"Skipping field '{field_name}' - already defined in {base_class.__name__}"
                    )
                    continue

                # Create a copy of the field_info to avoid modifying the original
                from pydantic import Field
                from pydantic.fields import FieldInfo

                # Extract the original field configuration
                field_kwargs = {}

                # Check if field is required or optional
                is_required = field_info.is_required()

                if not is_required:
                    # Field is optional - preserve the default value
                    if field_info.default is not ...:
                        field_kwargs["default"] = field_info.default
                    elif field_info.default_factory is not None:
                        field_kwargs["default_factory"] = field_info.default_factory
                    else:
                        # Make it explicitly optional with None default
                        field_kwargs["default"] = None

                # Preserve other field attributes
                if field_info.description:
                    field_kwargs["description"] = field_info.description

                # Create new field info
                new_field_info = Field(**field_kwargs)

                # Add to fields with original type annotation
                fields[field_name] = (field_info.annotation, new_field_info)

        # Create model with appropriate base class
        schema_name = name or f"{cls.__name__}Input"
        if base_class == BaseModel:
            return create_model(schema_name, **fields)
        else:
            return create_model(schema_name, __base__=base_class, **fields)

    @classmethod
    def derive_output_schema(
        cls, engine_name: Optional[str] = None, name: Optional[str] = None
    ) -> Type[BaseModel]:
        """
        Derive an output schema for the given engine from this state schema.

        This method intelligently selects the appropriate base class for the derived schema,
        using prebuilt states (MessagesState, ToolState) when appropriate instead of
        just creating a generic BaseModel.

        Args:
            engine_name: Optional name of the engine to target (default: all outputs)
            name: Optional name for the schema class

        Returns:
            A BaseModel subclass for output validation, potentially inheriting from
            MessagesState or ToolState for better compatibility
        """
        fields = {}

        # Get output field names
        if engine_name is not None and hasattr(cls, "__engine_io_mappings__"):
            if engine_name in cls.__engine_io_mappings__:
                output_fields = cls.__engine_io_mappings__[engine_name].get(
                    "outputs", []
                )
            else:
                output_fields = []
        elif hasattr(cls, "__output_fields__"):
            # Collect output fields across all engines
            output_fields = []
            for engine_outputs in cls.__output_fields__.values():
                output_fields.extend(engine_outputs)
        else:
            output_fields = []

        # Detect if we should use prebuilt base classes
        has_messages = "messages" in output_fields
        has_tools = "tools" in output_fields

        # Check what the current schema inherits from
        from haive.core.schema.prebuilt.messages_state import MessagesState
        from haive.core.schema.prebuilt.tool_state import ToolState

        current_is_tool_state = issubclass(cls, ToolState)
        current_is_messages_state = issubclass(cls, MessagesState)

        # Determine appropriate base class using same logic as SchemaComposer
        base_class = None
        if has_tools or current_is_tool_state:
            base_class = ToolState
            logger.debug("Using ToolState as base for derived output schema")
        elif has_messages or current_is_messages_state:
            base_class = MessagesState
            logger.debug("Using MessagesState as base for derived output schema")
        else:
            # Fall back to BaseModel for basic schemas
            base_class = BaseModel
            logger.debug("Using BaseModel as base for derived output schema")

        # Add output fields to schema
        for field_name in output_fields:
            if field_name in cls.model_fields:
                field_info = cls.model_fields[field_name]

                # Skip fields that are already defined in the base class
                if (
                    hasattr(base_class, "model_fields")
                    and field_name in base_class.model_fields
                ):
                    logger.debug(
                        f"Skipping field '{field_name}' - already defined in {base_class.__name__}"
                    )
                    continue

                # Create a copy of the field_info to avoid modifying the original
                from pydantic import Field
                from pydantic.fields import FieldInfo

                # Extract the original field configuration
                field_kwargs = {}

                # Check if field is required or optional
                is_required = field_info.is_required()

                if not is_required:
                    # Field is optional - preserve the default value
                    if field_info.default is not ...:
                        field_kwargs["default"] = field_info.default
                    elif field_info.default_factory is not None:
                        field_kwargs["default_factory"] = field_info.default_factory
                    else:
                        # Make it explicitly optional with None default
                        field_kwargs["default"] = None

                # Preserve other field attributes
                if field_info.description:
                    field_kwargs["description"] = field_info.description

                # Create new field info
                new_field_info = Field(**field_kwargs)

                # Add to fields with original type annotation
                fields[field_name] = (field_info.annotation, new_field_info)

        # Create model with appropriate base class
        schema_name = name or f"{cls.__name__}Output"
        if base_class == BaseModel:
            return create_model(schema_name, **fields)
        else:
            return create_model(schema_name, __base__=base_class, **fields)

    @classmethod
    def with_shared_fields(cls, fields: List[str]) -> Type[StateSchema]:
        """
        Create a copy of this schema with specified shared fields.

        Args:
            fields: List of field names to be marked as shared

        Returns:
            New StateSchema subclass with updated shared fields
        """
        # Create schema with same fields
        schema = create_model(f"{cls.__name__}WithShared", __base__=cls)

        # Update shared fields
        schema.__shared_fields__ = list(fields)

        return schema

    def patch(
        self, update_data: Dict[str, Any], apply_reducers: bool = True
    ) -> "StateSchema":
        """
        Update specific fields in the state.

        Args:
            update_data: Dictionary of field updates
            apply_reducers: Whether to apply reducer functions

        Returns:
            Self for chaining
        """
        if apply_reducers:
            return self.apply_reducers(update_data)
        else:
            return self.update(update_data)

    def combine_with(
        self, other: Union["StateSchema", Dict[str, Any]]
    ) -> "StateSchema":
        """
        Combine this state with another, applying reducers for shared fields.

        This is more sophisticated than update() or apply_reducers() as it
        properly handles StateSchema-specific metadata and shared fields.

        Args:
            other: Other state to combine with

        Returns:
            New combined state instance
        """
        # Convert to dict if StateSchema
        if isinstance(other, StateSchema):
            other_data = other.model_dump()
        else:
            other_data = other

        # Create a copy of self
        combined = self.model_copy()

        # Apply reducers to the copy
        combined.apply_reducers(other_data)

        return combined

    def differences_from(
        self, other: Union["StateSchema", Dict[str, Any]]
    ) -> Dict[str, Tuple[Any, Any]]:
        """
        Compare this state with another and return differences.

        Args:
            other: Other state to compare with

        Returns:
            Dictionary mapping field names to (self_value, other_value) tuples
        """
        # Convert to dict if StateSchema
        if isinstance(other, StateSchema):
            other_data = other.model_dump()
        else:
            other_data = other

        # Get self data
        self_data = self.model_dump()

        # Find differences
        differences = {}

        # Check fields in self
        for field_name, self_value in self_data.items():
            if field_name in other_data:
                other_value = other_data[field_name]
                if self_value != other_value:
                    differences[field_name] = (self_value, other_value)
            else:
                # Field not in other
                differences[field_name] = (self_value, None)

        # Check fields in other but not in self
        for field_name, other_value in other_data.items():
            if field_name not in self_data:
                differences[field_name] = (None, other_value)

        return differences

    # LangGraph integration methods

    def to_command(
        self, goto: Optional[str] = None, graph: Optional[str] = None
    ) -> Any:
        """
        Convert state to a Command object for LangGraph control flow.

        Args:
            goto: Optional next node to go to
            graph: Optional graph to target (None for current, PARENT for parent)

        Returns:
            Command object with state update
        """
        try:
            from langgraph.types import Command

            # Convert state to dictionary for update
            update = self.model_dump()

            # Create and return command
            return Command(update=update, goto=goto, graph=graph)
        except ImportError:
            logger.warning("LangGraph not available, cannot create Command")
            return {"state": self.model_dump(), "goto": goto, "graph": graph}

    @classmethod
    def from_snapshot(cls, snapshot: Any) -> "StateSchema":
        """
        Create a state from a LangGraph StateSnapshot.

        Args:
            snapshot: StateSnapshot from LangGraph

        Returns:
            New StateSchema instance
        """
        if snapshot is None:
            return cls()

        # Extract values based on object type
        if hasattr(snapshot, "values"):
            # Standard StateSnapshot
            return cls.from_dict(snapshot.values)
        elif hasattr(snapshot, "channel_values") and snapshot.channel_values:
            # Alternative attribute name in some versions
            return cls.from_dict(snapshot.channel_values)
        elif isinstance(snapshot, dict):
            # Dictionary state
            return cls.from_dict(snapshot)

        # Last resort - empty state
        logger.warning(f"Couldn't extract state from snapshot of type {type(snapshot)}")
        return cls()

    # Engine integration methods

    def prepare_for_engine(self, engine_name: str) -> Dict[str, Any]:
        """
        Prepare state data for a specific engine.

        Extracts only fields that are inputs for the specified engine.

        Args:
            engine_name: Name of the engine to prepare for

        Returns:
            Dictionary with engine-specific inputs
        """
        # Extract input field names for this engine
        input_fields = []

        if hasattr(self.__class__, "__engine_io_mappings__"):
            if engine_name in self.__class__.__engine_io_mappings__:
                input_fields = self.__class__.__engine_io_mappings__[engine_name].get(
                    "inputs", []
                )
        elif hasattr(self.__class__, "__input_fields__"):
            if engine_name in self.__class__.__input_fields__:
                input_fields = self.__class__.__input_fields__[engine_name]

        # If no input fields specified, try to use get_engine to find the engine
        if not input_fields:
            engine = self.get_engine(engine_name)
            if engine and hasattr(engine, "input_schema"):
                # If engine has an input schema, use its fields
                if hasattr(engine.input_schema, "model_fields"):
                    input_fields = list(engine.input_schema.model_fields.keys())
                    logger.debug(
                        f"Using input fields from engine {engine_name} input schema: {input_fields}"
                    )

        # If still no input fields, return empty dict
        if not input_fields:
            logger.debug(f"No input fields found for engine {engine_name}")
            return {}

        # Extract values for input fields
        result = {}
        for field_name in input_fields:
            if hasattr(self, field_name):
                result[field_name] = getattr(self, field_name)

        return result

    def merge_engine_output(
        self, engine_name: str, output: Dict[str, Any], apply_reducers: bool = True
    ) -> "StateSchema":
        """
        Merge output from an engine into this state.

        Args:
            engine_name: Name of the engine
            output: Output data from the engine
            apply_reducers: Whether to apply reducers during merge

        Returns:
            Self for chaining
        """
        # Log the merge operation
        logger.debug(f"Merging output from engine '{engine_name}'")

        # Filter output to include only fields that are outputs from this engine
        filtered_output = {}

        if hasattr(self.__class__, "__engine_io_mappings__"):
            if engine_name in self.__class__.__engine_io_mappings__:
                output_fields = self.__class__.__engine_io_mappings__[engine_name].get(
                    "outputs", []
                )
                for field_name in output_fields:
                    if field_name in output:
                        filtered_output[field_name] = output[field_name]
                        logger.debug(
                            f"Including field '{field_name}' from engine output (from mappings)"
                        )
        elif hasattr(self.__class__, "__output_fields__"):
            if engine_name in self.__class__.__output_fields__:
                output_fields = self.__class__.__output_fields__[engine_name]
                for field_name in output_fields:
                    if field_name in output:
                        filtered_output[field_name] = output[field_name]
                        logger.debug(
                            f"Including field '{field_name}' from engine output (from fields)"
                        )

        # If no output fields specified, try to use get_engine to find the engine
        if not filtered_output:
            engine = self.get_engine(engine_name)
            if engine and hasattr(engine, "output_schema"):
                # If engine has an output schema, use all fields from output
                logger.debug(
                    f"Using all output fields from engine '{engine_name}' (has output schema)"
                )
                filtered_output = output
            else:
                # No filtering, use all fields
                logger.debug(
                    f"Using all output fields from engine '{engine_name}' (no filtering)"
                )
                filtered_output = output

        # Apply update with or without reducers
        if apply_reducers:
            logger.debug(
                f"Applying reducers to engine output (fields: {list(filtered_output.keys())})"
            )
            return self.apply_reducers(filtered_output)
        else:
            logger.debug(
                f"Updating with engine output without reducers (fields: {list(filtered_output.keys())})"
            )
            return self.update(filtered_output)

    # Configuration integration

    def to_runnable_config(
        self, thread_id: Optional[str] = None, **kwargs
    ) -> RunnableConfig:
        """
        Convert state to a RunnableConfig.

        Args:
            thread_id: Optional thread ID for the configuration
            **kwargs: Additional configuration parameters

        Returns:
            RunnableConfig containing state data
        """
        # Create base configuration
        config: RunnableConfig = {
            "configurable": {
                "thread_id": thread_id or str(uuid.uuid4()),
                "state": self.model_dump(),
            }
        }

        # Add additional parameters
        for key, value in kwargs.items():
            config["configurable"][key] = value

        return config

    @classmethod
    def from_runnable_config(cls, config: RunnableConfig) -> Optional["StateSchema"]:
        """
        Extract state from a RunnableConfig.

        Args:
            config: RunnableConfig to extract from

        Returns:
            StateSchema instance or None if no state found
        """
        if config and "configurable" in config and "state" in config["configurable"]:
            state_data = config["configurable"]["state"]
            return cls.from_dict(state_data)
        return None

    # Visualization and pretty printing methods

    def pretty_print(self, title: Optional[str] = None) -> None:
        """
        Print state with rich formatting for easy inspection.

        Args:
            title: Optional title for the display
        """
        display_title = title or f"{self.__class__.__name__} Instance"

        # Create tree representation
        tree = Tree(f"[bold blue]{self.__class__.__name__}[/bold blue]")

        # Add fields
        for field_name, field_value in self.model_dump().items():
            # Format field value
            formatted_value = self._format_field_value(field_value)

            # Determine field style based on type
            field_style = "green"
            if isinstance(field_value, list):
                field_style = "yellow"
            elif isinstance(field_value, dict):
                field_style = "cyan"
            elif isinstance(field_value, (int, float)):
                field_style = "magenta"

            # Add to tree with styled field name
            tree.add(
                f"[bold {field_style}]{field_name}[/bold {field_style}]: {formatted_value}"
            )

        # Create panel with tree
        panel = Panel(tree, title=display_title, border_style="blue")

        # Use logger to print
        logger.panel(str(tree), title=display_title, style="blue")

    @staticmethod
    def _format_field_value(value: Any) -> str:
        """
        Format a field value for display.

        Args:
            value: Value to format

        Returns:
            Formatted string representation
        """
        if value is None:
            return "[dim]None[/dim]"
        elif isinstance(value, str):
            if len(value) > 100:
                return f'[green]"{value[:97]}..."[/green]'
            return f'[green]"{value}"[/green]'
        elif isinstance(value, int):
            return f"[magenta]{value}[/magenta]"
        elif isinstance(value, float):
            return f"[magenta]{value:.6g}[/magenta]"
        elif isinstance(value, bool):
            return f"[cyan]{value}[/cyan]"
        elif isinstance(value, list):
            if not value:
                return "[dim][]"
            if len(value) > 5:
                items_str = ", ".join(str(v)[:20] for v in value[:3])
                return f"[yellow][{items_str}, ... ({len(value)} items)][/yellow]"
            return f"[yellow][{', '.join(str(v)[:50] for v in value)}][/yellow]"
        elif isinstance(value, dict):
            if not value:
                return "[dim]{}"
            if len(value) > 3:
                items = list(value.items())[:3]
                items_str = ", ".join(f"{k}: {str(v)[:20]}" for k, v in items)
                return f"[cyan]{{{items_str}, ... ({len(value)} items)}}[/cyan]"
            return f"[cyan]{{{', '.join(f'{k}: {str(v)[:50]}' for k, v in value.items())}}}[/cyan]"
        elif hasattr(value, "__class__"):
            class_name = value.__class__.__name__
            if hasattr(value, "model_dump"):
                return f"[blue]{class_name}(...)[/blue]"
            return f"[blue]<{class_name}>[/blue]"
        return str(value)

        # Add these methods to the StateSchema class

    @classmethod
    def create_input_schema(
        cls, engine_name: Optional[str] = None, name: Optional[str] = None
    ) -> Type[BaseModel]:
        """
        Alias for derive_input_schema for backward compatibility.

        Args:
            engine_name: Optional name of the engine to target
            name: Optional name for the schema class

        Returns:
            A BaseModel subclass for input validation
        """
        return cls.derive_input_schema(engine_name, name)

    @classmethod
    def create_output_schema(
        cls, engine_name: Optional[str] = None, name: Optional[str] = None
    ) -> Type[BaseModel]:
        """
        Alias for derive_output_schema for backward compatibility.

        Args:
            engine_name: Optional name of the engine to target
            name: Optional name for the schema class

        Returns:
            A BaseModel subclass for output validation
        """
        return cls.derive_output_schema(engine_name, name)

    # Enhance the display_schema method to better handle structured output models
    @classmethod
    def display_schema(cls, title: Optional[str] = None) -> None:
        """
        Display schema information in a rich format.

        Args:
            title: Optional title for the display
        """
        schema_name = cls.__name__
        display_title = title or f"{schema_name} Schema"

        # Create main tree
        tree = Tree(
            f"[bold blue]class {schema_name}([/bold blue][italic]{cls.__base__.__name__}[/italic][bold blue])[/bold blue]:"
        )

        # Add fields
        fields_node = tree.add("[bold cyan]Fields:[/bold cyan]")
        for field_name, field_info in cls.model_fields.items():
            # Skip special fields
            if field_name.startswith("__"):
                continue

            # Format field type
            field_type = field_info.annotation
            type_str = str(field_type).replace("typing.", "")

            # Format default value
            if field_info.default_factory is not None:
                factory_name = getattr(
                    field_info.default_factory, "__name__", "factory"
                )
                default_str = f"default_factory={factory_name}"
            else:
                default = field_info.default
                if default is ...:
                    default_str = "[red]required[/red]"
                else:
                    default_str = f"default={repr(default)}"

            # Add description if available
            if field_info.description:
                desc_str = f" [dim]# {field_info.description}[/dim]"
            else:
                desc_str = ""

            # Add to tree with proper styling
            fields_node.add(
                f"[green]{field_name}[/green]: [yellow]{type_str}[/yellow] ({default_str}){desc_str}"
            )

        # Add shared fields
        if cls.__shared_fields__:
            shared_node = tree.add("[bold magenta]Shared Fields:[/bold magenta]")
            for field in cls.__shared_fields__:
                shared_node.add(f"[green]{field}[/green]")

        # Add reducers
        if cls.__serializable_reducers__:
            reducers_node = tree.add("[bold yellow]Reducers:[/bold yellow]")
            for field, reducer in cls.__serializable_reducers__.items():
                reducers_node.add(f"[green]{field}[/green]: [blue]{reducer}[/blue]")

        # Add engine I/O mappings
        if cls.__engine_io_mappings__:
            io_node = tree.add("[bold cyan]Engine I/O Mappings:[/bold cyan]")
            for engine, mapping in cls.__engine_io_mappings__.items():
                engine_node = io_node.add(f"[bold]{engine}[/bold]:")
                if mapping.get("inputs"):
                    engine_node.add(f"[blue]Inputs[/blue]: {mapping['inputs']}")
                if mapping.get("outputs"):
                    engine_node.add(f"[green]Outputs[/green]: {mapping['outputs']}")

        # Add structured output models information
        if hasattr(cls, "__structured_models__") and cls.__structured_models__:
            structured_node = tree.add("[bold green]Structured Models:[/bold green]")
            for model_name, model_path in cls.__structured_models__.items():
                structured_node.add(
                    f"[yellow]{model_name}[/yellow]: [blue]{model_path}[/blue]"
                )

                # Add fields if we have them
                if (
                    hasattr(cls, "__structured_model_fields__")
                    and model_name in cls.__structured_model_fields__
                ):
                    fields = cls.__structured_model_fields__[model_name]
                    fields_str = ", ".join(fields)
                    structured_node.add(f"  [dim]Fields: {fields_str}[/dim]")

        # Use logger to display
        logger.panel(str(tree), title=display_title, style="green")

    @classmethod
    def to_python_code(cls) -> str:
        """
        Convert schema to Python code representation.

        Returns:
            String containing Python code representation
        """
        lines = [f"class {cls.__name__}(StateSchema):"]
        lines.append('    """')
        lines.append(f"    {cls.__name__} schema")
        lines.append('    """')
        lines.append("")

        # Add fields
        for field_name, field_info in cls.model_fields.items():
            # Skip special fields
            if field_name.startswith("__"):
                continue

            # Format field type
            field_type = field_info.annotation
            type_str = str(field_type).replace("typing.", "")

            # Format default value
            if field_info.default_factory is not None:
                factory_name = getattr(
                    field_info.default_factory, "__name__", "factory"
                )
                default_str = f"Field(default_factory={factory_name}"
            else:
                default = field_info.default
                if default is ...:
                    default_str = "Field(..."
                else:
                    default_str = f"Field(default={repr(default)}"

            # Add description if available
            if field_info.description:
                default_str += f', description="{field_info.description}"'

            default_str += ")"

            # Add field line
            lines.append(f"    {field_name}: {type_str} = {default_str}")

        # Add empty line
        lines.append("")

        # Add class variables
        if cls.__shared_fields__:
            lines.append(f"    __shared_fields__ = {cls.__shared_fields__}")

        if cls.__serializable_reducers__:
            lines.append(
                f"    __serializable_reducers__ = {cls.__serializable_reducers__}"
            )

        if cls.__engine_io_mappings__:
            lines.append(f"    __engine_io_mappings__ = {cls.__engine_io_mappings__}")

        # Add structured models if available
        if hasattr(cls, "__structured_models__") and cls.__structured_models__:
            lines.append(f"    __structured_models__ = {cls.__structured_models__}")

        if (
            hasattr(cls, "__structured_model_fields__")
            and cls.__structured_model_fields__
        ):
            lines.append(
                f"    __structured_model_fields__ = {cls.__structured_model_fields__}"
            )

        return "\n".join(lines)

    @classmethod
    def get_structured_model(cls, model_name: str) -> Optional[Type[BaseModel]]:
        """
        Get a structured output model class by name.

        Args:
            model_name: Name of the structured model

        Returns:
            Model class if found, None otherwise
        """
        if (
            not hasattr(cls, "__structured_models__")
            or model_name not in cls.__structured_models__
        ):
            return None

        # Get the model path
        model_path = cls.__structured_models__[model_name]

        # Try to import the model
        try:
            module_path, class_name = model_path.rsplit(".", 1)
            module = __import__(module_path, fromlist=[class_name])
            return getattr(module, class_name)
        except (ImportError, AttributeError, ValueError) as e:
            logger.warning(f"Could not load structured model {model_name}: {e}")
            return None

    @classmethod
    def list_structured_models(cls) -> List[str]:
        """
        List all structured output models in this schema.

        Returns:
            List of structured model names
        """
        if hasattr(cls, "__structured_models__"):
            return list(cls.__structured_models__.keys())
        return []

    @classmethod
    def display_code(cls, title: Optional[str] = None) -> None:
        """
        Display Python code representation of the schema.

        Args:
            title: Optional title for the display
        """
        code = cls.to_python_code()

        # Create syntax highlighted code
        syntax = Syntax(code, "python", theme="monokai", line_numbers=True)

        # Use logger to display
        logger.panel(str(syntax), title=title or f"{cls.__name__} Code", style="yellow")

    @classmethod
    def compare_with(
        cls, other: Type["StateSchema"], title: Optional[str] = None
    ) -> None:
        """
        Compare this schema with another in a side-by-side display.

        Args:
            other: Other schema to compare with
            title: Optional title for the comparison
        """
        table = Table(title=title or "Schema Comparison")

        # Add columns
        table.add_column("Field", style="cyan")
        table.add_column(cls.__name__, style="green")
        table.add_column(other.__name__, style="blue")

        # Get all field names
        all_fields = set(cls.model_fields.keys()) | set(other.model_fields.keys())
        all_fields = {field for field in all_fields if not field.startswith("__")}

        # Add rows for each field
        for field_name in sorted(all_fields):
            cls_field = cls.model_fields.get(field_name)
            other_field = other.model_fields.get(field_name)

            # Format fields
            cls_str = (
                cls._format_field_info(cls_field)
                if cls_field
                else "[dim]Not present[/dim]"
            )
            other_str = (
                cls._format_field_info(other_field)
                if other_field
                else "[dim]Not present[/dim]"
            )

            # Add row
            table.add_row(field_name, cls_str, other_str)

        # Add metadata comparison
        table.add_section()

        # Compare shared fields
        cls_shared = cls.__shared_fields__
        other_shared = other.__shared_fields__
        table.add_row("Shared Fields", str(cls_shared), str(other_shared))

        # Compare reducers
        cls_reducers = cls.__serializable_reducers__
        other_reducers = other.__serializable_reducers__
        table.add_row("Reducers", str(cls_reducers), str(other_reducers))

        # Compare engine I/O mappings
        cls_io = cls.__engine_io_mappings__
        other_io = other.__engine_io_mappings__
        table.add_row("Engine I/O", str(cls_io), str(other_io))

        # Use logger to display table
        logger.table("Schema Comparison", {"Field": "See detailed comparison below"})

        # Create a detailed comparison as a formatted string
        comparison_data = {}
        for field_name in sorted(all_fields):
            cls_field = cls.model_fields.get(field_name)
            other_field = other.model_fields.get(field_name)

            cls_str = cls._format_field_info(cls_field) if cls_field else "Not present"
            other_str = (
                cls._format_field_info(other_field) if other_field else "Not present"
            )

            comparison_data[field_name] = (
                f"{cls.__name__}: {cls_str} | {other.__name__}: {other_str}"
            )

        logger.table("Field Comparison", comparison_data)

    @staticmethod
    def _format_field_info(field_info: Any) -> str:
        """
        Format field info for display.

        Args:
            field_info: Field info to format

        Returns:
            Formatted string representation
        """
        if field_info is None:
            return "None"

        # Extract type
        type_str = str(field_info.annotation).replace("typing.", "")

        # Extract default
        if field_info.default_factory is not None:
            factory_name = getattr(field_info.default_factory, "__name__", "factory")
            default_str = f"default_factory={factory_name}"
        else:
            default = field_info.default
            if default is ...:
                default_str = "[red]required[/red]"
            else:
                default_str = f"default={repr(default)}"

        return f"[yellow]{type_str}[/yellow] ({default_str})"

    @classmethod
    def as_table(cls) -> Table:
        """
        Create a rich table representation of the schema.

        Returns:
            Rich Table object
        """
        table = Table(title=f"{cls.__name__} Schema")

        # Add columns
        table.add_column("Field", style="cyan")
        table.add_column("Type", style="yellow")
        table.add_column("Default", style="green")
        table.add_column("Description", style="blue")
        table.add_column("Annotations", style="magenta")

        # Add rows for each field
        for field_name, field_info in cls.model_fields.items():
            # Skip special fields
            if field_name.startswith("__"):
                continue

            # Format field type
            field_type = field_info.annotation
            type_str = str(field_type).replace("typing.", "")

            # Format default value
            if field_info.default_factory is not None:
                factory_name = getattr(
                    field_info.default_factory, "__name__", "factory"
                )
                default_str = f"default_factory={factory_name}"
            else:
                default = field_info.default
                if default is ...:
                    default_str = "required"
                else:
                    default_str = repr(default)

            # Get description
            description = field_info.description or ""

            # Build annotations string
            annotations = []

            # Check if field is shared
            if field_name in cls.__shared_fields__:
                annotations.append("shared")

            # Check if field has reducer
            if field_name in cls.__serializable_reducers__:
                annotations.append(
                    f"reducer={cls.__serializable_reducers__[field_name]}"
                )

            # Check if field is input/output for any engine
            for engine_name, mapping in cls.__engine_io_mappings__.items():
                if field_name in mapping.get("inputs", []):
                    annotations.append(f"input({engine_name})")
                if field_name in mapping.get("outputs", []):
                    annotations.append(f"output({engine_name})")

            # Add row
            table.add_row(
                field_name, type_str, default_str, description, ", ".join(annotations)
            )

        return table

    @classmethod
    def display_table(cls) -> None:
        """
        Display schema as a table.
        """
        # Build table data
        table_data = {}

        for field_name, field_info in cls.model_fields.items():
            # Skip special fields
            if field_name.startswith("__"):
                continue

            # Format field type
            field_type = field_info.annotation
            type_str = str(field_type).replace("typing.", "")

            # Format default value
            if field_info.default_factory is not None:
                factory_name = getattr(
                    field_info.default_factory, "__name__", "factory"
                )
                default_str = f"default_factory={factory_name}"
            else:
                default = field_info.default
                if default is ...:
                    default_str = "required"
                else:
                    default_str = repr(default)

            # Get description
            description = field_info.description or ""

            # Build annotations
            annotations = []
            if field_name in cls.__shared_fields__:
                annotations.append("shared")
            if field_name in cls.__serializable_reducers__:
                annotations.append(
                    f"reducer={cls.__serializable_reducers__[field_name]}"
                )

            # Format entry
            value = f"Type: {type_str}, Default: {default_str}"
            if description:
                value += f", Description: {description}"
            if annotations:
                value += f", Annotations: {', '.join(annotations)}"

            table_data[field_name] = value

        # Use logger to display
        logger.table(f"{cls.__name__} Schema", table_data)
