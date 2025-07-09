"""StateSchemaManager for creating and manipulating state schemas.

This module provides the StateSchemaManager class, which offers a low-level API for
dynamically creating, modifying, and managing state schemas at runtime. Unlike the
SchemaComposer, which provides a higher-level builder-style API focused on composition,
the StateSchemaManager offers fine-grained control over schema construction and
modification with support for advanced features like computed properties, validators,
and custom methods.

The StateSchemaManager is particularly useful for:
- Programmatically building schemas with complex interdependencies
- Adding validators, properties, and methods to schemas
- Performing schema transformations and modifications at runtime
- Providing a programmatic interface for schema manipulation
- Creating specialized schema variants with custom behaviors

Key capabilities include:
- Field creation and manipulation with comprehensive type handling
- Support for field sharing, reducers, and engine I/O relationships
- Addition of validators, properties, and computed properties
- Dynamic method addition (instance, class, and static methods)
- Schema finalization with proper metadata configuration
- Integration with SchemaComposer for seamless conversion

Example:
    ```python
    from haive.core.schema import StateSchemaManager
    from typing import List
    from langchain_core.messages import BaseMessage

    # Create a manager
    manager = StateSchemaManager(name="ConversationState")

    # Add fields
    manager.add_field(
        "messages",
        List[BaseMessage],
        default_factory=list,
        description="Conversation history",
        shared=True
    )

    # Add a computed property
    def get_last_message(self):
        if not self.messages:
            return None
        return self.messages[-1]

    manager.add_computed_property("last_message", get_last_message)

    # Add a method
    def add_message(self, message):
        self.messages.append(message)

    manager.add_method("add_message", add_message)

    # Build the schema
    ConversationState = manager.build()
    ```

This module is part of the Haive Schema System, providing the lower-level foundation
for schema manipulation that complements the higher-level SchemaComposer.
"""

from __future__ import annotations

import inspect
import logging
from collections import defaultdict
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Dict,
    List,
    Optional,
    Set,
    Tuple,
    Type,
    TypeVar,
    Union,
)

from pydantic import BaseModel, create_model

from haive.core.schema.field_definition import FieldDefinition
from haive.core.schema.field_utils import (
    create_field,
    infer_field_type,
    resolve_reducer,
)
from haive.core.schema.state_schema import StateSchema

if TYPE_CHECKING:
    from haive.core.schema.schema_composer import SchemaComposer

logger = logging.getLogger(__name__)

T = TypeVar("T")


class StateSchemaManager:
    """Manager for dynamically creating and manipulating state schemas.

    The StateSchemaManager provides a comprehensive, low-level API for dynamically
    creating, modifying, and managing state schemas at runtime. It offers granular
    control over schema construction and modification with advanced features like
    computed properties, validators, and custom methods.

    This class serves as a layer over Pydantic's model creation functionality with
    additional features specific to the Haive framework, including field sharing,
    reducer functions, and engine I/O tracking. Unlike SchemaComposer, which provides
    a higher-level builder-style API focused on composition from components,
    StateSchemaManager offers fine-grained control over schema construction.

    Key capabilities include:

    - Field management: Add, modify, and remove fields with comprehensive type handling
    - Field sharing: Configure which fields are shared between parent and child graphs
    - Reducer functions: Set up field-specific reducers for state merging
    - Engine I/O: Track which fields are inputs and outputs for which engines
    - Validators: Add custom validation functions for field values
    - Properties and computed properties: Define dynamic properties with getters/setters
    - Methods: Add instance, class, and static methods to the schema
    - Schema finalization: Build and finalize the schema with proper metadata

    This class is particularly useful for programmatically building schemas with
    complex interdependencies, adding validation logic, and creating specialized
    schema variants with custom behaviors.
    """

    def __init__(
        self,
        data: Optional[
            Union[Dict[str, Any], Type[BaseModel], BaseModel, "SchemaComposer"]
        ] = None,
        name: Optional[str] = None,
        config: Optional[Dict[str, Any]] = None,
    ):
        """
        Initialize a new StateSchemaManager.

        Args:
            data: Source data to initialize from
            name: Custom schema name
            config: Optional configuration dictionary
        """
        self.fields: Dict[str, Tuple[Type, Any]] = {}
        self.field_definitions: Dict[str, FieldDefinition] = (
            {}
        )  # New field definitions store
        self.validators: Dict[str, Callable] = {}
        self.properties: Dict[str, Callable] = {}
        self.computed_properties: Dict[str, Tuple[Callable, Callable]] = {}
        self.field_descriptions: Dict[str, str] = {}
        self.instance_methods: Dict[str, Callable] = {}
        self.class_methods: Dict[str, Callable] = {}
        self.static_methods: Dict[str, Callable] = {}
        self.locked = False
        self.config = config or {}

        # Special field sets for state schema
        self._shared_fields: Set[str] = set()
        self._reducer_names: Dict[str, str] = (
            {}
        )  # Field name -> reducer name (serializable)
        self._reducer_functions: Dict[str, Callable] = (
            {}
        )  # Field name -> reducer function

        # Input/output tracking for engines
        self._input_fields: Dict[str, Set[str]] = defaultdict(
            set
        )  # Engine name -> input fields
        self._output_fields: Dict[str, Set[str]] = defaultdict(
            set
        )  # Engine name -> output fields
        self._engine_io_mappings: Dict[str, Dict[str, List[str]]] = (
            {}
        )  # Engine name -> IO mapping

        # Set default name
        if data is None:
            self.name = name or self.config.get("default_schema_name", "UnnamedSchema")
            return

        # Extract name from data if not provided
        if name is None:
            if hasattr(data, "name"):
                self.name = data.name
            elif isinstance(data, type):
                self.name = data.__name__
            else:
                self.name = "CustomState"
        else:
            self.name = name

        # Load data based on type
        if isinstance(data, dict):
            self._load_from_dict(data)
        elif isinstance(data, type) and issubclass(data, BaseModel):
            self._load_from_model(data)
        elif isinstance(data, BaseModel):
            self._load_from_model(data.__class__)
        elif hasattr(data, "fields") and (
            hasattr(data, "shared_fields") or hasattr(data, "engine_io_mappings")
        ):
            self._load_from_composer(data)
        else:
            raise TypeError(f"Unsupported data type: {type(data)}")

    def _load_from_model(self, model_cls: Type[BaseModel]) -> None:
        """
        Load fields and methods from a Pydantic model.

        Args:
            model_cls: Pydantic model class to load from
        """
        try:
            # Extract fields from model_fields
            if hasattr(model_cls, "model_fields"):
                for field_name, field_info in model_cls.model_fields.items():
                    # Skip special fields
                    if field_name.startswith("__") or field_name == "runnable_config":
                        continue

                    # Create a field definition
                    field_def = FieldDefinition.extract_from_model_field(
                        name=field_name,
                        field_type=field_info.annotation,
                        field_info=field_info,
                    )

                    # Add to field definitions
                    self.field_definitions[field_name] = field_def

                    # Add to fields for backward compatibility
                    self.fields[field_name] = field_def.to_field_info()

                    # Set description if available
                    if field_def.description:
                        self.field_descriptions[field_name] = field_def.description

            # Extract shared fields
            if hasattr(model_cls, "__shared_fields__"):
                self._shared_fields.update(model_cls.__shared_fields__)
                # Update field definition shared flag
                for field_name in model_cls.__shared_fields__:
                    if field_name in self.field_definitions:
                        self.field_definitions[field_name].shared = True

            # Extract reducer information
            if hasattr(model_cls, "__serializable_reducers__"):
                self._reducer_names.update(model_cls.__serializable_reducers__)

            if hasattr(model_cls, "__reducer_fields__"):
                self._reducer_functions.update(model_cls.__reducer_fields__)
                # Update field definition reducers
                for field_name, reducer in model_cls.__reducer_fields__.items():
                    if field_name in self.field_definitions:
                        self.field_definitions[field_name].reducer = reducer

            # Extract engine I/O mappings
            if hasattr(model_cls, "__engine_io_mappings__"):
                for engine_name, mapping in model_cls.__engine_io_mappings__.items():
                    self._engine_io_mappings[engine_name] = mapping.copy()

                    # Extract input fields
                    for field_name in mapping.get("inputs", []):
                        self._input_fields[engine_name].add(field_name)
                        # Update field definition
                        if field_name in self.field_definitions:
                            if (
                                engine_name
                                not in self.field_definitions[field_name].input_for
                            ):
                                self.field_definitions[field_name].input_for.append(
                                    engine_name
                                )

                    # Extract output fields
                    for field_name in mapping.get("outputs", []):
                        self._output_fields[engine_name].add(field_name)
                        # Update field definition
                        if field_name in self.field_definitions:
                            if (
                                engine_name
                                not in self.field_definitions[field_name].output_from
                            ):
                                self.field_definitions[field_name].output_from.append(
                                    engine_name
                                )

            # Extract input/output fields (alternative format)
            if hasattr(model_cls, "__input_fields__"):
                for engine_name, fields_list in model_cls.__input_fields__.items():
                    self._input_fields[engine_name].update(fields_list)
                    # Update field definitions
                    for field_name in fields_list:
                        if field_name in self.field_definitions:
                            if (
                                engine_name
                                not in self.field_definitions[field_name].input_for
                            ):
                                self.field_definitions[field_name].input_for.append(
                                    engine_name
                                )

            if hasattr(model_cls, "__output_fields__"):
                for engine_name, fields_list in model_cls.__output_fields__.items():
                    self._output_fields[engine_name].update(fields_list)
                    # Update field definitions
                    for field_name in fields_list:
                        if field_name in self.field_definitions:
                            if (
                                engine_name
                                not in self.field_definitions[field_name].output_from
                            ):
                                self.field_definitions[field_name].output_from.append(
                                    engine_name
                                )

            # Load methods and validators
            for name, attr in inspect.getmembers(model_cls):
                # Skip private/special methods
                if name.startswith("_") and name != "__validator__":
                    continue

                if isinstance(attr, property):
                    # Handle property
                    getter = attr.fget
                    setter = attr.fset
                    if getter and setter:
                        self.computed_properties[name] = (getter, setter)
                    elif getter:
                        self.properties[name] = getter
                elif inspect.ismethod(attr) or inspect.isfunction(attr):
                    # Handle methods
                    if name.startswith("validate_"):
                        self.validators[name] = attr
                    elif getattr(attr, "__validator__", False):
                        self.validators[name] = attr
        except Exception as e:
            logger.error(f"Error loading from model {model_cls.__name__}: {e}")
            # Add a placeholder field as fallback
            self.fields["placeholder"] = (str, create_field(str, "")[1])
            self.field_definitions["placeholder"] = FieldDefinition(
                name="placeholder", field_type=str, default=""
            )

    def _load_from_composer(self, composer: Any) -> None:
        """
        Load fields and metadata from a SchemaComposer.

        Args:
            composer: SchemaComposer instance
        """
        try:
            # Add field definitions directly
            if hasattr(composer, "fields") and isinstance(composer.fields, dict):
                for field_name, field_def in composer.fields.items():
                    # Add to field definitions
                    self.field_definitions[field_name] = field_def

                    # Add to fields for backward compatibility
                    self.fields[field_name] = field_def.to_field_info()

                    # Set description if available
                    if field_def.description:
                        self.field_descriptions[field_name] = field_def.description

                    # Set shared flag
                    if field_def.shared:
                        self._shared_fields.add(field_name)

                    # Set reducer
                    if field_def.reducer:
                        self._reducer_functions[field_name] = field_def.reducer
                        reducer_name = field_def.get_reducer_name()
                        if reducer_name:
                            self._reducer_names[field_name] = reducer_name

            # Add shared fields
            if hasattr(composer, "shared_fields"):
                self._shared_fields.update(composer.shared_fields)

            # Add engine I/O mappings
            if hasattr(composer, "engine_io_mappings"):
                for engine_name, mapping in composer.engine_io_mappings.items():
                    self._engine_io_mappings[engine_name] = mapping.copy()

            # Add input/output fields
            if hasattr(composer, "input_fields"):
                for engine_name, fields in composer.input_fields.items():
                    self._input_fields[engine_name].update(fields)

            if hasattr(composer, "output_fields"):
                for engine_name, fields in composer.output_fields.items():
                    self._output_fields[engine_name].update(fields)
        except Exception as e:
            logger.error(f"Error loading from composer: {e}")
            # Add a placeholder field as fallback
            self.fields["placeholder"] = (str, create_field(str, "")[1])
            self.field_definitions["placeholder"] = FieldDefinition(
                name="placeholder", field_type=str, default=""
            )

    def _load_from_dict(self, data: Dict[str, Any]) -> None:
        """
        Load fields from a dictionary.

        Args:
            data: Dictionary containing field data
        """
        try:
            # Handle special metadata keys
            if "shared_fields" in data:
                self._shared_fields.update(data["shared_fields"])

            if "reducer_names" in data or "serializable_reducers" in data:
                reducer_names = data.get(
                    "reducer_names", data.get("serializable_reducers", {})
                )
                self._reducer_names.update(reducer_names)

            if "reducer_functions" in data:
                self._reducer_functions.update(data["reducer_functions"])

            if "field_descriptions" in data:
                self.field_descriptions.update(data["field_descriptions"])

            if "engine_io_mappings" in data:
                for engine_name, mapping in data["engine_io_mappings"].items():
                    self._engine_io_mappings[engine_name] = mapping.copy()

            if "input_fields" in data:
                for engine_name, fields in data["input_fields"].items():
                    self._input_fields[engine_name].update(fields)

            if "output_fields" in data:
                for engine_name, fields in data["output_fields"].items():
                    self._output_fields[engine_name].update(fields)

            # Process field definitions
            for key, value in data.items():
                # Skip special metadata keys
                if key in [
                    "shared_fields",
                    "reducer_names",
                    "serializable_reducers",
                    "reducer_functions",
                    "field_descriptions",
                    "engine_io_mappings",
                    "input_fields",
                    "output_fields",
                ]:
                    continue

                # Handle different field formats
                if isinstance(value, tuple) and len(value) >= 2:
                    # Handle (type, default) format
                    field_type, default = value[0:2]

                    # Check for extra metadata
                    extra = {}
                    if len(value) >= 3 and isinstance(value[2], dict):
                        extra = value[2]

                    # Extract metadata
                    description = extra.pop("description", None)
                    shared = extra.pop("shared", False) or key in self._shared_fields
                    reducer = None
                    if "reducer" in extra:
                        reducer_value = extra.pop("reducer")
                        if callable(reducer_value):
                            reducer = reducer_value
                        elif isinstance(reducer_value, str):
                            reducer = resolve_reducer(reducer_value)
                    elif key in self._reducer_functions:
                        reducer = self._reducer_functions[key]

                    # Check if default is a factory function
                    default_factory = None
                    if callable(default) and not isinstance(default, type):
                        default_factory = default
                        default = None

                    # Create field definition
                    field_def = FieldDefinition(
                        name=key,
                        field_type=field_type,
                        default=default,
                        default_factory=default_factory,
                        description=description,
                        shared=shared,
                        reducer=reducer,
                        **extra,
                    )

                    # Add field
                    self.field_definitions[key] = field_def
                    self.fields[key] = field_def.to_field_info()

                    # Set description
                    if description:
                        self.field_descriptions[key] = description
                else:
                    # Field with value only - infer type
                    field_type = infer_field_type(value)

                    # Create field definition
                    field_def = FieldDefinition(
                        name=key,
                        field_type=field_type,
                        default=value,
                        shared=key in self._shared_fields,
                        reducer=self._reducer_functions.get(key),
                    )

                    # Add field
                    self.field_definitions[key] = field_def
                    self.fields[key] = field_def.to_field_info()
        except Exception as e:
            logger.error(f"Error loading from dict: {e}")
            # Add a placeholder field as fallback
            self.fields["placeholder"] = (str, create_field(str, "")[1])
            self.field_definitions["placeholder"] = FieldDefinition(
                name="placeholder", field_type=str, default=""
            )

    def add_field(
        self,
        name: str,
        field_type: Type[T],
        default: Any = None,
        default_factory: Optional[Callable[[], T]] = None,
        description: Optional[str] = None,
        shared: bool = False,
        reducer: Optional[Callable] = None,
        input_for: Optional[List[str]] = None,
        output_from: Optional[List[str]] = None,
        optional: bool = True,
        **kwargs,
    ) -> "StateSchemaManager":
        """
        Add a field to the schema with comprehensive options.

        Args:
            name: Field name
            field_type: Type of the field
            default: Default value for the field
            default_factory: Optional factory function for default value
            description: Optional field description
            shared: Whether field is shared with parent graph
            reducer: Optional reducer function for this field
            input_for: List of engines this field serves as input for
            output_from: List of engines this field is output from
            optional: Whether to make the field optional (default: True)
            **kwargs: Additional field parameters

        Returns:
            Self for chaining
        """
        if self.locked:
            raise ValueError("Schema is locked and cannot be modified.")

        # Create field definition
        field_def = FieldDefinition(
            name=name,
            field_type=field_type,
            default=default,
            default_factory=default_factory,
            description=description,
            shared=shared,
            reducer=reducer,
            input_for=input_for,
            output_from=output_from,
            **kwargs,
        )

        # Store the field definition
        self.field_definitions[name] = field_def

        # Store the field info for backward compatibility
        self.fields[name] = field_def.to_field_info()

        # Track additional metadata
        if description:
            self.field_descriptions[name] = description

        if shared:
            self._shared_fields.add(name)

        if reducer:
            # Store reducer function
            self._reducer_functions[name] = reducer

            # Store serializable reducer name
            reducer_name = field_def.get_reducer_name()
            if reducer_name:
                self._reducer_names[name] = reducer_name

        # Track engine I/O
        if input_for:
            for engine_name in input_for:
                self._input_fields[engine_name].add(name)

                # Update engine I/O mapping
                if engine_name not in self._engine_io_mappings:
                    self._engine_io_mappings[engine_name] = {
                        "inputs": [],
                        "outputs": [],
                    }
                if name not in self._engine_io_mappings[engine_name]["inputs"]:
                    self._engine_io_mappings[engine_name]["inputs"].append(name)

        if output_from:
            for engine_name in output_from:
                self._output_fields[engine_name].add(name)

                # Update engine I/O mapping
                if engine_name not in self._engine_io_mappings:
                    self._engine_io_mappings[engine_name] = {
                        "inputs": [],
                        "outputs": [],
                    }
                if name not in self._engine_io_mappings[engine_name]["outputs"]:
                    self._engine_io_mappings[engine_name]["outputs"].append(name)

        return self

    def remove_field(self, name: str) -> "StateSchemaManager":
        """
        Remove a field from the schema.

        Args:
            name: Name of the field to remove

        Returns:
            Self for chaining
        """
        if self.locked:
            raise ValueError("Schema is locked and cannot be modified.")

        # Remove from fields
        if name in self.fields:
            del self.fields[name]

        # Remove from field definitions
        if name in self.field_definitions:
            del self.field_definitions[name]

        # Remove from metadata
        if name in self.field_descriptions:
            del self.field_descriptions[name]

        if name in self._shared_fields:
            self._shared_fields.remove(name)

        if name in self._reducer_names:
            del self._reducer_names[name]

        if name in self._reducer_functions:
            del self._reducer_functions[name]

        # Remove from engine I/O
        for engine_name, fields in self._input_fields.items():
            if name in fields:
                fields.remove(name)
                # Update mapping
                if (
                    engine_name in self._engine_io_mappings
                    and name in self._engine_io_mappings[engine_name]["inputs"]
                ):
                    self._engine_io_mappings[engine_name]["inputs"].remove(name)

        for engine_name, fields in self._output_fields.items():
            if name in fields:
                fields.remove(name)
                # Update mapping
                if (
                    engine_name in self._engine_io_mappings
                    and name in self._engine_io_mappings[engine_name]["outputs"]
                ):
                    self._engine_io_mappings[engine_name]["outputs"].remove(name)

        return self

    def modify_field(
        self,
        name: str,
        new_type: Optional[Type] = None,
        new_default: Any = None,
        new_default_factory: Optional[Callable] = None,
        new_description: Optional[str] = None,
        new_shared: Optional[bool] = None,
        new_reducer: Optional[Callable] = None,
        add_input_for: Optional[List[str]] = None,
        add_output_from: Optional[List[str]] = None,
        remove_input_for: Optional[List[str]] = None,
        remove_output_from: Optional[List[str]] = None,
        **kwargs,
    ) -> "StateSchemaManager":
        """
        Modify an existing field's properties.

        Args:
            name: Name of the field to modify
            new_type: New type for the field
            new_default: New default value
            new_default_factory: New default factory function
            new_description: New description
            new_shared: Whether field should be shared
            new_reducer: New reducer function
            add_input_for: List of engines to add as input consumers
            add_output_from: List of engines to add as output producers
            remove_input_for: List of engines to remove as input consumers
            remove_output_from: List of engines to remove as output producers
            **kwargs: Additional field parameters

        Returns:
            Self for chaining
        """
        if self.locked:
            raise ValueError("Schema is locked and cannot be modified.")

        # Check if field exists
        if name not in self.field_definitions:
            logger.warning(f"Field {name} does not exist, cannot be modified")
            return self

        # Get current field definition
        field_def = self.field_definitions[name]

        # Update type if provided
        if new_type is not None:
            field_def.field_type = new_type

        # Update default or default_factory if provided
        if new_default_factory is not None:
            field_def = FieldDefinition(
                name=name,
                field_type=field_def.field_type,
                default_factory=new_default_factory,
                description=field_def.description,
                shared=field_def.shared,
                reducer=field_def.reducer,
                input_for=field_def.input_for,
                output_from=field_def.output_from,
            )
        elif new_default is not None:
            field_def = FieldDefinition(
                name=name,
                field_type=field_def.field_type,
                default=new_default,
                description=field_def.description,
                shared=field_def.shared,
                reducer=field_def.reducer,
                input_for=field_def.input_for,
                output_from=field_def.output_from,
            )

        # Update description if provided
        if new_description is not None:
            field_def.description = new_description
            self.field_descriptions[name] = new_description

        # Update shared status if specified
        if new_shared is not None:
            field_def.shared = new_shared
            if new_shared:
                self._shared_fields.add(name)
            elif name in self._shared_fields:
                self._shared_fields.remove(name)

        # Update reducer if provided
        if new_reducer is not None:
            field_def.reducer = new_reducer
            self._reducer_functions[name] = new_reducer

            # Update reducer name
            reducer_name = field_def.get_reducer_name()
            if reducer_name:
                self._reducer_names[name] = reducer_name
            elif name in self._reducer_names:
                del self._reducer_names[name]

        # Update engine I/O
        if add_input_for:
            for engine_name in add_input_for:
                if engine_name not in field_def.input_for:
                    field_def.input_for.append(engine_name)
                    self._input_fields[engine_name].add(name)

                    # Update mapping
                    if engine_name not in self._engine_io_mappings:
                        self._engine_io_mappings[engine_name] = {
                            "inputs": [],
                            "outputs": [],
                        }
                    if name not in self._engine_io_mappings[engine_name]["inputs"]:
                        self._engine_io_mappings[engine_name]["inputs"].append(name)

        if add_output_from:
            for engine_name in add_output_from:
                if engine_name not in field_def.output_from:
                    field_def.output_from.append(engine_name)
                    self._output_fields[engine_name].add(name)

                    # Update mapping
                    if engine_name not in self._engine_io_mappings:
                        self._engine_io_mappings[engine_name] = {
                            "inputs": [],
                            "outputs": [],
                        }
                    if name not in self._engine_io_mappings[engine_name]["outputs"]:
                        self._engine_io_mappings[engine_name]["outputs"].append(name)

        if remove_input_for:
            for engine_name in remove_input_for:
                if engine_name in field_def.input_for:
                    field_def.input_for.remove(engine_name)
                    if name in self._input_fields[engine_name]:
                        self._input_fields[engine_name].remove(name)

                    # Update mapping
                    if (
                        engine_name in self._engine_io_mappings
                        and name in self._engine_io_mappings[engine_name]["inputs"]
                    ):
                        self._engine_io_mappings[engine_name]["inputs"].remove(name)

        if remove_output_from:
            for engine_name in remove_output_from:
                if engine_name in field_def.output_from:
                    field_def.output_from.remove(engine_name)
                    if name in self._output_fields[engine_name]:
                        self._output_fields[engine_name].remove(name)

                    # Update mapping
                    if (
                        engine_name in self._engine_io_mappings
                        and name in self._engine_io_mappings[engine_name]["outputs"]
                    ):
                        self._engine_io_mappings[engine_name]["outputs"].remove(name)

        # Update additional parameters
        if kwargs:
            # Create a new field definition with updated parameters
            field_info_kwargs = field_def._extract_field_kwargs()
            field_info_kwargs.update(kwargs)

            # Create new field definition
            if field_def.default_factory is not None:
                field_def = FieldDefinition(
                    name=name,
                    field_type=field_def.field_type,
                    default_factory=field_def.default_factory,
                    description=field_def.description,
                    shared=field_def.shared,
                    reducer=field_def.reducer,
                    input_for=field_def.input_for,
                    output_from=field_def.output_from,
                    **field_info_kwargs,
                )
            else:
                field_def = FieldDefinition(
                    name=name,
                    field_type=field_def.field_type,
                    default=field_def.default,
                    description=field_def.description,
                    shared=field_def.shared,
                    reducer=field_def.reducer,
                    input_for=field_def.input_for,
                    output_from=field_def.output_from,
                    **field_info_kwargs,
                )

        # Update field definition
        self.field_definitions[name] = field_def

        # Update field for backward compatibility
        self.fields[name] = field_def.to_field_info()

        return self

    def has_field(self, name: str) -> bool:
        """
        Check if the schema has a specific field.

        Args:
            name: Field name to check

        Returns:
            True if field exists, False otherwise
        """
        return name in self.field_definitions

    def get_model(
        self,
        lock: bool = False,
        as_state_schema: bool = True,
        name: Optional[str] = None,
        use_annotated: bool = True,
    ) -> Type[BaseModel]:
        """
        Create a Pydantic model with all configured options.

        Args:
            lock: Whether to lock the schema against further modifications
            as_state_schema: Whether to use StateSchema as the base class
            name: Optional name for the schema class
            use_annotated: Whether to use Annotated types for metadata

        Returns:
            Created model class
        """
        if lock:
            self.locked = True

        # Use provided name or default
        model_name = name or self.name

        # Choose the base class
        base_class = StateSchema if as_state_schema else BaseModel

        # Create field definitions for the model
        field_defs = {}

        for name, field_def in self.field_definitions.items():
            if use_annotated:
                field_type, field_info = field_def.to_annotated_field()
            else:
                field_type, field_info = field_def.to_field_info()

            field_defs[name] = (field_type, field_info)

        # Create the model with fields
        model = create_model(model_name, __base__=base_class, **field_defs)

        # Add shared fields metadata if using StateSchema
        if as_state_schema:
            model.__shared_fields__ = list(self._shared_fields)

            # Add reducer metadata
            model.__serializable_reducers__ = dict(self._reducer_names)

            # Add actual reducer functions
            if not hasattr(model, "__reducer_fields__"):
                model.__reducer_fields__ = {}
            model.__reducer_fields__.update(self._reducer_functions)

            # Add engine I/O mappings metadata if available
            if self._engine_io_mappings:
                model.__engine_io_mappings__ = {
                    k: v.copy() for k, v in self._engine_io_mappings.items()
                }

            # Add input/output field tracking
            if self._input_fields:
                model.__input_fields__ = {
                    k: list(v) for k, v in self._input_fields.items()
                }

            if self._output_fields:
                model.__output_fields__ = {
                    k: list(v) for k, v in self._output_fields.items()
                }

        # Add validators
        for name, validator in self.validators.items():
            setattr(model, name, validator)

        # Add properties
        for prop_name, (getter, setter) in self.computed_properties.items():
            prop = property(getter, setter)
            setattr(model, prop_name, prop)

        # Add regular properties
        for prop_name, getter in self.properties.items():
            prop = property(getter)
            setattr(model, prop_name, prop)

        # Add instance methods
        for name, method in self.instance_methods.items():
            setattr(model, name, method)

        # Add class methods
        for name, method in self.class_methods.items():
            setattr(model, name, classmethod(method))

        # Add static methods
        for name, method in self.static_methods.items():
            setattr(model, name, staticmethod(method))

        return model

    def mark_as_input_field(
        self, field_name: str, engine_name: str
    ) -> "StateSchemaManager":
        """
        Mark a field as an input field for an engine.

        Args:
            field_name: Name of the field
            engine_name: Name of the engine

        Returns:
            Self for chaining
        """
        if field_name in self.field_definitions:
            # Update field definition
            if engine_name not in self.field_definitions[field_name].input_for:
                self.field_definitions[field_name].input_for.append(engine_name)

            # Update input fields tracking
            self._input_fields[engine_name].add(field_name)

            # Update engine I/O mapping
            if engine_name not in self._engine_io_mappings:
                self._engine_io_mappings[engine_name] = {"inputs": [], "outputs": []}

            if field_name not in self._engine_io_mappings[engine_name]["inputs"]:
                self._engine_io_mappings[engine_name]["inputs"].append(field_name)

        return self

    def mark_as_output_field(
        self, field_name: str, engine_name: str
    ) -> "StateSchemaManager":
        """
        Mark a field as an output field for an engine.

        Args:
            field_name: Name of the field
            engine_name: Name of the engine

        Returns:
            Self for chaining
        """
        if field_name in self.field_definitions:
            # Update field definition
            if engine_name not in self.field_definitions[field_name].output_from:
                self.field_definitions[field_name].output_from.append(engine_name)

            # Update output fields tracking
            self._output_fields[engine_name].add(field_name)

            # Update engine I/O mapping
            if engine_name not in self._engine_io_mappings:
                self._engine_io_mappings[engine_name] = {"inputs": [], "outputs": []}

            if field_name not in self._engine_io_mappings[engine_name]["outputs"]:
                self._engine_io_mappings[engine_name]["outputs"].append(field_name)

        return self

    def _update_engine_io_mapping(self, engine_name: str) -> None:
        """
        Update engine I/O mapping for a specific engine.

        Args:
            engine_name: Engine name to update mapping for
        """
        # Create mapping if it doesn't exist
        if engine_name not in self._engine_io_mappings:
            self._engine_io_mappings[engine_name] = {"inputs": [], "outputs": []}

        # Update inputs from tracked fields
        if engine_name in self._input_fields:
            self._engine_io_mappings[engine_name]["inputs"] = list(
                self._input_fields[engine_name]
            )

        # Update outputs from tracked fields
        if engine_name in self._output_fields:
            self._engine_io_mappings[engine_name]["outputs"] = list(
                self._output_fields[engine_name]
            )

    def to_composer(self) -> "SchemaComposer":
        """
        Convert to a SchemaComposer instance.

        Returns:
            SchemaComposer with current fields and metadata
        """
        from haive.core.schema.schema_composer import SchemaComposer

        # Create a new composer
        composer = SchemaComposer(name=self.name)

        # Add field definitions
        for _name, field_def in self.field_definitions.items():
            composer.add_field_definition(field_def)

        return composer

    def merge(
        self,
        other: Union[
            "StateSchemaManager", Type[BaseModel], BaseModel, "SchemaComposer"
        ],
    ) -> "StateSchemaManager":
        """
        Merge with another schema, preserving first occurrences.

        Args:
            other: Another object to merge with

        Returns:
            New merged StateSchemaManager
        """
        # Create a new manager with the same name
        merged = StateSchemaManager(name=f"{self.name}_merged")

        # Copy all fields and metadata from self
        for name, field_def in self.field_definitions.items():
            merged.field_definitions[name] = field_def
            merged.fields[name] = field_def.to_field_info()

            if field_def.description:
                merged.field_descriptions[name] = field_def.description

            if field_def.shared:
                merged._shared_fields.add(name)

            if field_def.reducer:
                merged._reducer_functions[name] = field_def.reducer
                reducer_name = field_def.get_reducer_name()
                if reducer_name:
                    merged._reducer_names[name] = reducer_name

            for engine_name in field_def.input_for:
                merged._input_fields[engine_name].add(name)

            for engine_name in field_def.output_from:
                merged._output_fields[engine_name].add(name)

        # Copy engine I/O mappings
        for engine_name, mapping in self._engine_io_mappings.items():
            merged._engine_io_mappings[engine_name] = mapping.copy()

        # Copy methods
        merged.validators = self.validators.copy()
        merged.properties = self.properties.copy()
        merged.computed_properties = self.computed_properties.copy()
        merged.instance_methods = self.instance_methods.copy()
        merged.class_methods = self.class_methods.copy()
        merged.static_methods = self.static_methods.copy()

        # Convert other to StateSchemaManager if needed
        other_manager = other
        if not isinstance(other, StateSchemaManager):
            other_manager = StateSchemaManager(other)

        # Add fields from other (skip if already exists)
        for name, field_def in other_manager.field_definitions.items():
            if name not in merged.field_definitions:
                merged.field_definitions[name] = field_def
                merged.fields[name] = field_def.to_field_info()

                if field_def.description:
                    merged.field_descriptions[name] = field_def.description

                if field_def.shared:
                    merged._shared_fields.add(name)

                if field_def.reducer:
                    merged._reducer_functions[name] = field_def.reducer
                    reducer_name = field_def.get_reducer_name()
                    if reducer_name:
                        merged._reducer_names[name] = reducer_name

                for engine_name in field_def.input_for:
                    merged._input_fields[engine_name].add(name)

                for engine_name in field_def.output_from:
                    merged._output_fields[engine_name].add(name)

        # Add engine I/O mappings (don't overwrite existing)
        for engine_name, mapping in other_manager._engine_io_mappings.items():
            if engine_name not in merged._engine_io_mappings:
                merged._engine_io_mappings[engine_name] = mapping.copy()

        # Add validators (don't overwrite existing)
        for name, validator in other_manager.validators.items():
            if name not in merged.validators:
                merged.validators[name] = validator

        # Add properties (don't overwrite existing)
        for name, prop in other_manager.properties.items():
            if name not in merged.properties:
                merged.properties[name] = prop

        # Add computed properties (don't overwrite existing)
        for name, (getter, setter) in other_manager.computed_properties.items():
            if name not in merged.computed_properties:
                merged.computed_properties[name] = (getter, setter)

        # Add methods (don't overwrite existing)
        for name, method in other_manager.instance_methods.items():
            if name not in merged.instance_methods:
                merged.instance_methods[name] = method

        for name, method in other_manager.class_methods.items():
            if name not in merged.class_methods:
                merged.class_methods[name] = method

        for name, method in other_manager.static_methods.items():
            if name not in merged.static_methods:
                merged.static_methods[name] = method

        # Update engine I/O mappings for consistency
        for engine_name in merged._input_fields.keys() | merged._output_fields.keys():
            merged._update_engine_io_mapping(engine_name)

        return merged

    def add_method(
        self,
        method: Callable,
        method_name: Optional[str] = None,
        method_type: str = "instance",
    ) -> "StateSchemaManager":
        """
        Add a method to the schema.

        Args:
            method: Method callable to add
            method_name: Optional method name (defaults to method.__name__)
            method_type: Type of method: "instance", "class", or "static"

        Returns:
            Self for chaining
        """
        if self.locked:
            raise ValueError("Schema is locked and cannot be modified.")

        name = method_name or method.__name__

        if method_type == "instance":
            self.instance_methods[name] = method
        elif method_type == "class":
            self.class_methods[name] = method
        elif method_type == "static":
            self.static_methods[name] = method
        else:
            raise ValueError(f"Unknown method type: {method_type}")

        return self

    @classmethod
    def from_components(
        cls,
        components: List[Any],
        name: str = "ComponentSchema",
        include_messages_field: bool = True,
    ) -> "StateSchemaManager":
        """
        Create a schema manager from a list of components.

        Args:
            components: List of components to extract fields from
            name: Name for the resulting schema
            include_messages_field: Whether to ensure a messages field exists

        Returns:
            StateSchemaManager with extracted fields
        """
        from haive.core.schema.schema_composer import SchemaComposer

        # Create a composer and extract fields
        composer = SchemaComposer(name=name)
        composer.add_fields_from_components(
            components, include_messages_field=include_messages_field
        )

        # Convert to manager
        return composer.to_manager()

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
        from haive.core.schema.schema_composer import SchemaComposer

        # Use SchemaComposer to create the schema
        return SchemaComposer.create_message_state(
            additional_fields=additional_fields, name=name
        )
