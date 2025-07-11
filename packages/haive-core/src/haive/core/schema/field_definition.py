"""FieldDefinition for the Haive Schema System.

This module provides the FieldDefinition class, which represents a complete field
definition including type, default value, metadata, and additional properties required
for the Haive Schema System. FieldDefinition serves as the fundamental building block
for dynamic schema composition and manipulation.

A FieldDefinition encapsulates all information needed to create a field in a Pydantic
model, with additional Haive-specific metadata such as:
- Whether the field is shared between parent and child graphs
- Reducer functions for combining field values during state updates
- Input/output relationships with specific engines
- Association with structured output models
- Source component identification

FieldDefinition objects are used extensively by SchemaComposer and StateSchemaManager
when building dynamic schemas at runtime, providing a complete representation of
each field's characteristics and relationships.

Example:
    ```python
    from haive.core.schema import FieldDefinition
    from typing import List
    import operator

    # Create a field definition for a context field
    field_def = FieldDefinition(
        name="context",
        field_type=List[str],
        default_factory=list,
        description="Retrieved document contexts",
        shared=True,
        reducer=operator.add,  # Concatenate lists when combining values
        input_for=["llm_engine"],  # This field is input for the LLM engine
        output_from=["retriever_engine"]  # This field is output from the retriever
    )

    # Get field info for model creation
    field_type, field_info = field_def.to_field_info()

    # Get annotated field with embedded metadata
    field_type, field_info = field_def.to_annotated_field()
    ```
"""

import logging
from typing import Any, Callable, Dict, List, Optional, Tuple, Type

from haive.core.schema.field_utils import create_annotated_field, create_field

logger = logging.getLogger(__name__)


class FieldDefinition:
    """Complete field definition with metadata for the Haive Schema System.

    The FieldDefinition class encapsulates all information about a field, including
    its type, default value, description, and relationships to engines, making it
    the core building block for dynamic schema composition and manipulation.

    This class provides methods to convert between different field representations
    (standard fields, annotated fields, dictionaries) and helps manage field metadata
    that extends beyond what Pydantic directly supports.

    Attributes:
        name (str): Field name used in the schema
        field_type (Type[Any]): Python type annotation for the field
        field_info (Any): Optional existing Pydantic FieldInfo object
        default (Any): Default value for the field
        default_factory (Optional[Callable[[], Any]]): Factory function for default value
        description (Optional[str]): Human-readable description of the field
        shared (bool): Whether this field is shared with parent graphs
        reducer (Optional[Callable]): Function to combine values during state updates
        source (Optional[str]): Component that provided this field
        input_for (List[str]): Engines that use this field as input
        output_from (List[str]): Engines that produce this field as output
        structured_model (Optional[str]): Name of structured model this field belongs to
        metadata (Dict[str, Any]): Additional metadata properties

    Field metadata plays a crucial role in the Haive Schema System, enabling features like:
    - Field sharing for parent-child graph communication
    - Automatic state updates using reducer functions
    - Input/output tracking for engine integration
    - Structured output model association
    """

    def __init__(
        self,
        name: str,
        field_type: type[Any],
        field_info: Any = None,
        default: Any = None,
        default_factory: Callable[[], Any] | None = None,
        description: str | None = None,
        shared: bool = False,
        reducer: Callable | None = None,
        source: str | None = None,
        input_for: list[str] | None = None,
        output_from: list[str] | None = None,
        structured_model: str | None = None,
        **kwargs,
    ):
        """Initialize a field definition with comprehensive metadata.

        Creates a new FieldDefinition object that encapsulates all information about a field,
        including its type, default value, description, and relationships to other components
        in the system.

        Args:
            name (str): Field name that will be used in the schema
            field_type (Type[Any]): Python type annotation for the field (e.g., str, List[int])
            field_info (Any, optional): Existing Pydantic FieldInfo object. If provided,
                some other parameters may be ignored in favor of this object's properties.
            default (Any, optional): Default value for the field. Ignored if default_factory
                is also provided.
            default_factory (Optional[Callable[[], Any]], optional): Factory function that
                creates the default value. Takes precedence over default if both are provided.
            description (Optional[str], optional): Human-readable description of the field's
                purpose and usage.
            shared (bool, optional): Whether this field is shared with parent graphs. Fields
                marked as shared will be synchronized between parent and child graphs. Defaults to False.
            reducer (Optional[Callable], optional): Function that defines how field values
                are combined during state updates. Should accept two arguments (old_value, new_value)
                and return the combined result.
            source (Optional[str], optional): Name of the component that provided this field,
                useful for tracking field origins.
            input_for (Optional[List[str]], optional): List of engine names that use this field
                as input.
            output_from (Optional[List[str]], optional): List of engine names that produce
                this field as output.
            structured_model (Optional[str], optional): Name of structured output model this
                field belongs to, for schema composition.
            **kwargs: Additional metadata to store with the field definition.

        Note:
            The field_type parameter accepts any valid Python type annotation, including:
            - Basic types: str, int, float, bool
            - Container types: List[T], Dict[K, V], Tuple[T, ...]
            - Union types: Union[T1, T2]
            - Optional types: Optional[T] (equivalent to Union[T, None])
            - Custom classes, especially Pydantic models

        Example:
            ```python
            # Create a field for a list of messages with add_messages reducer
            messages_field = FieldDefinition(
                name="messages",
                field_type=List[BaseMessage],
                default_factory=list,
                description="Conversation message history",
                shared=True,
                reducer=add_messages,
                input_for=["llm_engine"],
                output_from=["memory_engine"]
            )
            ```
        """
        self.name = name
        self.field_type = field_type
        self.field_info = field_info
        self.default = default
        self.default_factory = default_factory
        self.description = description
        self.shared = shared
        self.reducer = reducer
        self.source = source
        self.input_for = input_for or []
        self.output_from = output_from or []
        self.structured_model = structured_model
        self.metadata = kwargs

    @classmethod
    def extract_from_model_field(
        cls,
        name: str,
        field_type: type[Any],
        field_info: Any,
        include_annotations: bool = True,
    ) -> "FieldDefinition":
        """Extract a FieldDefinition from an existing Pydantic model field.

        This class method creates a FieldDefinition by extracting information from
        an existing Pydantic model field. It preserves all field properties including
        default values, default factories, and descriptions. If include_annotations
        is True, it also extracts metadata from type annotations.

        Args:
            name (str): Field name to use in the new FieldDefinition
            field_type (Type[Any]): Type annotation from the model field
            field_info (Any): Pydantic FieldInfo object containing field metadata
            include_annotations (bool, optional): Whether to extract metadata from
                Annotated types. When True, metadata from Annotated[Type, ...] will
                be included in the field definition. Defaults to True.

        Returns:
            FieldDefinition: A new FieldDefinition instance containing all the
                extracted information from the model field.

        Example:
            ```python
            # Extract field from an existing model
            from pydantic import BaseModel, Field

            class MyModel(BaseModel):
                items: List[str] = Field(
                    default_factory=list,
                    description="List of items"
                )

            # Get model field info
            field_name = "items"
            field_type = MyModel.model_fields[field_name].annotation
            field_info = MyModel.model_fields[field_name]

            # Extract field definition
            field_def = FieldDefinition.extract_from_model_field(
                field_name, field_type, field_info
            )
            ```
        """
        # Extract basic properties
        default = field_info.default if hasattr(field_info, "default") else None
        default_factory = (
            field_info.default_factory
            if hasattr(field_info, "default_factory")
            else None
        )
        description = (
            field_info.description if hasattr(field_info, "description") else None
        )

        # If no default or factory and field is required (default is ...), set appropriate default
        if default is ... and default_factory is None:
            # Set to None to allow proper state management
            default = None

        # Create field definition
        field_def = cls(
            name=name,
            field_type=field_type,
            field_info=field_info,
            default=default,
            default_factory=default_factory,
            description=description,
        )

        # Extract additional metadata from annotations if available
        if include_annotations and hasattr(field_type, "__metadata__"):
            for annotation in field_type.__metadata__:
                if hasattr(annotation, "__dict__"):
                    for key, value in annotation.__dict__.items():
                        if key.startswith("_") or key in ["__module__", "__doc__"]:
                            continue
                        field_def.metadata[key] = value

        return field_def

    def to_field_info(self) -> tuple[type[Any], Any]:
        """Convert to a field type and info pair for standard model creation.

        This method generates the necessary type and field_info objects needed
        to create a field in a Pydantic model. It produces a standard field
        (not using Python's Annotated type) that can be used in model creation.

        Returns:
            Tuple[Type[Any], Any]: A tuple containing:
                - field_type: The Python type annotation for the field
                - field_info: The Pydantic FieldInfo object with field metadata

        Example:
            ```python
            from pydantic import create_model

            # Create a field definition
            field_def = FieldDefinition(
                name="count",
                field_type=int,
                default=0,
                description="Counter value"
            )

            # Get field info for model creation
            field_type, field_info = field_def.to_field_info()

            # Use in model creation
            MyModel = create_model(
                "MyModel",
                count=(field_type, field_info),
                __module__=__name__
            )
            ```
        """
        logger.debug(
            f"🔍 TO_FIELD_INFO DEBUG {self.name}: default={self.default}, factory={self.default_factory}"
        )

        if self.field_info:
            # Use existing field info if available
            logger.debug(
                f"🔍 TO_FIELD_INFO {self.name}: Using existing field_info, default={self.field_info.default}"
            )
            return self.field_type, self.field_info

        # Create field using utility function
        logger.debug(
            f"🔍 TO_FIELD_INFO {self.name}: Creating new field with default={self.default}, factory={self.default_factory}"
        )
        field_type, field_info = create_field(
            field_type=self.field_type,
            default=self.default,
            default_factory=self.default_factory,
            description=self.description,
            shared=self.shared,
            reducer=self.reducer,
            **self.metadata,
        )
        logger.debug(
            f"🔍 TO_FIELD_INFO {self.name}: Created field_info with default={field_info.default}, required={field_info.default is ...}"
        )

        return field_type, field_info

    def to_annotated_field(self) -> tuple[type[Any], Any]:
        """Convert to an annotated field type and info pair for model creation.

        This method generates a field type and info pair using Python's Annotated type,
        which embeds metadata directly in the type annotation. This approach allows
        the field to carry additional Haive-specific metadata like shared status,
        reducer functions, and engine I/O relationships.

        Annotated fields preserve their metadata when schemas are composed or
        manipulated, making them ideal for complex schema operations.

        Returns:
            Tuple[Type[Any], Any]: A tuple containing:
                - annotated_field_type: Python type wrapped in Annotated with metadata
                - field_info: Pydantic FieldInfo object with standard field properties

        Example:
            ```python
            from pydantic import create_model

            # Create a field definition with reducer
            field_def = FieldDefinition(
                name="items",
                field_type=List[str],
                default_factory=list,
                description="Collection of items",
                reducer=operator.add  # Will be embedded in the annotation
            )

            # Get annotated field
            field_type, field_info = field_def.to_annotated_field()

            # Use in model creation - metadata persists in the type annotation
            MyModel = create_model(
                "MyModel",
                items=(field_type, field_info),
                __module__=__name__
            )
            ```
        """
        # Create annotated field using utility function
        field_type, field_info = create_annotated_field(
            field_type=self.field_type,
            default=self.default,
            default_factory=self.default_factory,
            description=self.description,
            shared=self.shared,
            reducer=self.reducer,
            **self.metadata,
        )

        return field_type, field_info

    def get_reducer_name(self) -> str | None:
        """Get the reducer function name for serialization purposes.

        This method attempts to extract a meaningful, serializable string
        representation of the field's reducer function. It tries several
        approaches, in order:
        1. Use the function's __name__ attribute
        2. Use the function's __qualname__ attribute (includes class name for methods)
        3. Fall back to string representation

        For functions with a __module__ attribute, the module path is included
        to enable proper importing and resolution during deserialization.

        Returns:
            Optional[str]: String representation of the reducer function that can
                be used for serialization, or None if no reducer is defined.

        Example:
            ```python
            import operator

            field_def = FieldDefinition(
                name="count",
                field_type=int,
                default=0,
                reducer=operator.add
            )

            reducer_name = field_def.get_reducer_name()
            # Returns: "operator.add"
            ```
        """
        if not self.reducer:
            return None

        # Try to get a meaningful name
        if hasattr(self.reducer, "__name__"):
            name = self.reducer.__name__
        elif hasattr(self.reducer, "__qualname__"):
            name = self.reducer.__qualname__
        else:
            name = str(self.reducer)

        # Add module path if available
        if hasattr(self.reducer, "__module__"):
            return f"{self.reducer.__module__}.{name}"
        return name

    def to_dict(self) -> dict[str, Any]:
        """Convert the field definition to a serializable dictionary.

        This method creates a complete dictionary representation of the field
        definition, suitable for serialization or debugging. The dictionary
        includes all field properties including type, default values, description,
        and all metadata.

        Special handling is applied to:
        - The field_type, which is converted to a string representation
        - The default_factory, which is converted to a string if present
        - The reducer function, which is converted to a string name via get_reducer_name()

        Returns:
            Dict[str, Any]: Dictionary representation of the field definition with
                all properties and metadata.

        Example:
            ```python
            field_def = FieldDefinition(
                name="items",
                field_type=List[str],
                default_factory=list,
                description="Collection of items",
                shared=True,
                reducer=operator.add
            )

            data = field_def.to_dict()
            # Returns a dictionary with all field properties
            # {
            #   "name": "items",
            #   "field_type": "typing.List[str]",
            #   "default": None,
            #   "default_factory": "<built-in function list>",
            #   "description": "Collection of items",
            #   "shared": True,
            #   "reducer": "operator.add",
            #   "source": None,
            #   "input_for": [],
            #   "output_from": [],
            #   "structured_model": None
            # }
            ```
        """
        result = {
            "name": self.name,
            "field_type": str(self.field_type),
            "default": self.default,
            "description": self.description,
            "shared": self.shared,
            "source": self.source,
            "input_for": self.input_for,
            "output_from": self.output_from,
            "structured_model": self.structured_model,
        }

        if self.default_factory:
            result["default_factory"] = str(self.default_factory)

        if self.reducer:
            result["reducer"] = self.get_reducer_name()

        result.update(self.metadata)

        return result
