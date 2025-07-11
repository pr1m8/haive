"""Field utilities for the Haive Schema System.

This module provides a comprehensive set of utilities for creating, extracting, and
manipulating Pydantic fields within the Haive Schema System. It ensures consistent
handling of field metadata, types, and defaults across the entire framework.

The utilities in this module serve as the low-level foundation for the Schema System,
handling technical details like:
- Creating fields with standardized metadata
- Working with Annotated types for metadata embedding
- Extracting metadata from type annotations
- Type inference and manipulation
- Resolver functions for reducers

Core functions include:
- create_field: Create a standard Pydantic field with metadata
- create_annotated_field: Create a field using Python's Annotated type for metadata
- extract_type_metadata: Extract base type and metadata from annotations
- infer_field_type: Intelligently determine types from values
- get_common_reducers: Access standard reducer functions
- resolve_reducer: Convert reducer names to functions

These utilities are primarily used by FieldDefinition, SchemaComposer, and
StateSchemaManager to implement higher-level functionality.

Example:
    ```python
    from haive.core.schema.field_utils import (
        create_field, create_annotated_field, get_common_reducers
    )
    from typing import List
    import operator

    # Create a standard field
    field_type, field_info = create_field(
        field_type=List[str],
        default_factory=list,
        description="List of items",
        shared=True,
        reducer=operator.add
    )

    # Create an annotated field with embedded metadata
    field_type, field_info = create_annotated_field(
        field_type=List[str],
        default_factory=list,
        description="List of items",
        shared=True,
        reducer=operator.add
    )

    # Get common reducer functions
    reducers = get_common_reducers()
    add_messages = reducers["add_messages"]  # LangGraph's message list combiner
    ```
"""

import logging
import operator
import re
from typing import (
    Annotated,
    Any,
    Callable,
    Dict,
    ForwardRef,
    List,
    Optional,
    Tuple,
    Type,
    TypeVar,
    get_args,
    get_origin,
)

from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


# ============================================================================
# FIELD NAMING UTILITIES
# ============================================================================


def camel_to_snake_case(name: str) -> str:
    """Convert CamelCase to snake_case.

    Args:
        name: CamelCase string to convert

    Returns:
        snake_case version of the string

    Examples:
        >>> camel_to_snake_case("QueryRefinementResponse")
        'query_refinement_response'
        >>> camel_to_snake_case("UserProfile")
        'user_profile'
        >>> camel_to_snake_case("APIKey")
        'api_key'
    """
    # Handle sequences of uppercase letters (like "APIKey" -> "api_key")
    name = re.sub("([A-Z]+)([A-Z][a-z])", r"\1_\2", name)
    # Handle normal CamelCase (like "QueryRefinement" -> "query_refinement")
    name = re.sub("([a-z0-9])([A-Z])", r"\1_\2", name)
    return name.lower()


def create_field_name_from_model(
    model_class: Type[BaseModel], remove_suffixes: bool = False
) -> str:
    """Create a proper field name from a Pydantic model class.

    Args:
        model_class: The Pydantic model class
        remove_suffixes: Whether to remove common suffixes like "Response", "Result"

    Returns:
        A properly formatted snake_case field name

    Examples:
        >>> class QueryRefinementResponse(BaseModel): pass
        >>> create_field_name_from_model(QueryRefinementResponse)
        'query_refinement_response'
        >>> create_field_name_from_model(QueryRefinementResponse, remove_suffixes=True)
        'query_refinement'
    """
    class_name = model_class.__name__

    # Convert to snake_case
    field_name = camel_to_snake_case(class_name)

    # Remove common suffixes if requested
    if remove_suffixes:
        suffixes_to_remove = ["_response", "_result", "_output", "_data"]
        for suffix in suffixes_to_remove:
            if field_name.endswith(suffix):
                field_name = field_name[: -len(suffix)]
                break

    # Ensure we have a valid field name
    if not field_name or field_name == "_":
        field_name = "parsed_result"

    return field_name


def get_field_info_from_model(model_class: Type[BaseModel]) -> Dict[str, Any]:
    """Get field info from a model class, checking for annotations.

    This function looks for field integration annotations on the model class
    and returns field information for schema integration.

    Args:
        model_class: The Pydantic model class

    Returns:
        Dictionary with field configuration for schema integration
    """
    result = {}

    # Check for custom field name annotation
    field_name = getattr(model_class, "__field_name__", None)
    if field_name:
        result["field_name"] = field_name
    else:
        # Use auto-generated field name
        result["field_name"] = create_field_name_from_model(model_class)

    # Check for field description
    field_description = getattr(model_class, "__field_description__", None)
    if field_description:
        result["description"] = field_description
    else:
        result["description"] = f"Parsed {model_class.__name__}"

    # Check for field type override
    field_type = getattr(model_class, "__field_type__", None)
    if field_type:
        result["field_type"] = field_type
    else:
        result["field_type"] = Optional[model_class]

    # Check for other field configuration
    field_config = getattr(model_class, "__field_config__", {})
    result.update(field_config)

    return result


# Decorators for adding field info to models
def field_name(name: str):
    """Simple decorator to set the field name for schema integration.

    Args:
        name: The field name to use in schema integration

    Examples:
        >>> @field_name("query_refinement")
        ... class QueryRefinementResponse(BaseModel):
        ...     pass
    """

    def decorator(cls):
        cls.__field_name__ = name
        return cls

    return decorator


def field_description(description: str):
    """Decorator to set the field description for schema integration.

    Args:
        description: The field description to use

    Examples:
        >>> @field_description("Refined query results")
        ... class QueryRefinementResponse(BaseModel):
        ...     pass
    """

    def decorator(cls):
        cls.__field_description__ = description
        return cls

    return decorator


def field_config(**config):
    """Decorator to set field configuration for schema integration.

    Args:
        **config: Field configuration options

    Examples:
        >>> @field_config(required=True, default=None)
        ... class QueryRefinementResponse(BaseModel):
        ...     pass
    """

    def decorator(cls):
        cls.__field_config__ = config
        return cls

    return decorator


# Type variables
T = TypeVar("T")
FieldType = TypeVar("FieldType")
DefaultType = TypeVar("DefaultType")
ReducerType = TypeVar("ReducerType", bound=Callable[[Any, Any], Any])


class FieldMetadata:
    """Standardized container for field metadata in the Haive Schema System.

    This class encapsulates all metadata associated with a field, serving as a
    comprehensive representation of field properties beyond what Pydantic directly
    supports. It provides a structured way to manage:

    - Basic field properties (description, title, etc.)
    - Haive-specific properties (shared status, reducer functions, etc.)
    - Engine I/O tracking (input/output relationships with engines)
    - Structured output model associations

    FieldMetadata provides methods for converting between different metadata
    representations, including dictionaries for Field instantiation and annotation
    objects for Annotated types. It also supports merging metadata from different
    sources and serializing reducer functions.

    This class serves as a single source of truth for field metadata throughout
    the Schema System, ensuring consistent handling of field properties across
    schema composition, manipulation, and serialization operations.

    Attributes:
        description (Optional[str]): Human-readable description of the field
        shared (bool): Whether the field is shared with parent graphs
        reducer (Optional[Callable]): Function to combine field values during updates
        source (Optional[str]): Component that provided this field
        input_for (List[str]): Engines this field serves as input for
        output_from (List[str]): Engines this field is output from
        structured_model (Optional[str]): Name of structured model this field belongs to
        title (Optional[str]): Field title (for OpenAPI/Schema generation)
        extra (Dict[str, Any]): Additional metadata properties
    """

    def __init__(
        self,
        description: Optional[str] = None,
        shared: bool = False,
        reducer: Optional[Callable] = None,
        source: Optional[str] = None,
        input_for: Optional[List[str]] = None,
        output_from: Optional[List[str]] = None,
        structured_model: Optional[str] = None,
        title: Optional[str] = None,
        **extra,
    ):
        """
        Initialize field metadata with comprehensive properties.

        Args:
            description: Human-readable description of the field
            shared: Whether field is shared with parent graphs
            reducer: Function to combine field values during state updates
            source: Component that provided this field
            input_for: List of engines this field serves as input for
            output_from: List of engines this field is output from
            structured_model: Name of structured model this field belongs to
            title: Optional field title (for OpenAPI/Schema generation)
            **extra: Additional metadata properties
        """
        self.description = description
        self.shared = shared
        self.reducer = reducer
        self.source = source
        self.input_for = input_for or []
        self.output_from = output_from or []
        self.structured_model = structured_model
        self.title = title
        self.extra = extra

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert metadata to dictionary for Field instantiation.

        Returns:
            Dictionary of metadata suitable for pydantic.Field constructor
        """
        result = {}
        if self.description:
            result["description"] = self.description
        if self.title:
            result["title"] = self.title

        # Add standard Field parameters from extra
        standard_params = {
            "gt",
            "ge",
            "lt",
            "le",
            "multiple_of",
            "min_items",
            "max_items",
            "min_length",
            "max_length",
            "pattern",
            "discriminator",
            "json_schema_extra",
            "validation_alias",
            "serialization_alias",
            "validation_alias_priority",
            "serialization_alias_priority",
            "deprecated",
            "examples",
        }

        for k, v in self.extra.items():
            if k in standard_params:
                result[k] = v

        return result

    def to_annotation_metadata(self) -> List[Any]:
        """
        Convert to a list of metadata objects for Annotated types.

        Returns:
            List of metadata objects for use in Annotated[Type, ...]
        """
        metadata = []

        # Add reducer as first metadata if present
        if self.reducer:
            metadata.append(self.reducer)

        # Create a dictionary for other metadata
        other_meta = {}
        if self.shared:
            other_meta["shared"] = True
        if self.source:
            other_meta["source"] = self.source
        if self.input_for:
            other_meta["input_for"] = self.input_for
        if self.output_from:
            other_meta["output_from"] = self.output_from
        if self.structured_model:
            other_meta["structured_model"] = self.structured_model

        # Add to metadata list if we have any other metadata
        if other_meta:
            metadata.append(other_meta)

        return metadata

    def merge(self, other: "FieldMetadata") -> "FieldMetadata":
        """
        Merge with another FieldMetadata instance.

        Args:
            other: FieldMetadata instance to merge with

        Returns:
            New FieldMetadata instance with merged data
        """
        # Start with a copy of the current metadata
        result = FieldMetadata(
            description=other.description or self.description,
            shared=other.shared or self.shared,
            reducer=other.reducer or self.reducer,
            source=other.source or self.source,
            title=other.title or self.title,
        )

        # Merge lists
        result.input_for = list(set(self.input_for + other.input_for))
        result.output_from = list(set(self.output_from + other.output_from))

        # Structured model takes the newer value
        result.structured_model = other.structured_model or self.structured_model

        # Merge extra attributes, with other taking precedence
        result.extra = self.extra.copy()
        for k, v in other.extra.items():
            result.extra[k] = v

        return result

    def get_reducer_name(self) -> Optional[str]:
        """
        Get serializable name for the reducer function.

        Returns:
            String name of the reducer function or None
        """
        if not self.reducer:
            return None

        # Handle operator module functions
        if hasattr(self.reducer, "__module__") and self.reducer.__module__ in (
            "operator",
            "_operator",
        ):
            return f"operator.{self.reducer.__name__}"

        # Handle lambda functions
        if hasattr(self.reducer, "__name__") and self.reducer.__name__ == "<lambda>":
            return "<lambda>"

        # Handle standard functions
        if hasattr(self.reducer, "__name__"):
            if (
                hasattr(self.reducer, "__module__")
                and self.reducer.__module__ != "__main__"
            ):
                # Use fully qualified name for imported functions
                return f"{self.reducer.__module__}.{self.reducer.__name__}"
            return self.reducer.__name__

        # Last resort: string representation
        return str(self.reducer)

    @classmethod
    def from_annotation(cls, annotation: Type) -> Optional["FieldMetadata"]:
        """
        Extract field metadata from an annotated type.

        Args:
            annotation: Type annotation to extract metadata from

        Returns:
            FieldMetadata if metadata was found, None otherwise
        """
        # Check if this is an Annotated type
        if get_origin(annotation) is not Annotated:
            return None

        # Get args from Annotated[Type, ...]
        args = get_args(annotation)
        if len(args) < 2:
            return None

        # Extract metadata from annotation
        metadata = FieldMetadata()

        # Process each metadata object
        for meta in args[1:]:
            if callable(meta) and not isinstance(meta, type):
                # Found a callable, assume it's a reducer
                metadata.reducer = meta
            elif isinstance(meta, dict):
                # Dictionary of metadata
                if "shared" in meta:
                    metadata.shared = meta["shared"]
                if "source" in meta:
                    metadata.source = meta["source"]
                if "input_for" in meta:
                    metadata.input_for = meta["input_for"]
                if "output_from" in meta:
                    metadata.output_from = meta["output_from"]
                if "structured_model" in meta:
                    metadata.structured_model = meta["structured_model"]
                if "description" in meta:
                    metadata.description = meta["description"]
                if "title" in meta:
                    metadata.title = meta["title"]

                # Add any other keys to extra
                for k, v in meta.items():
                    if k not in {
                        "shared",
                        "source",
                        "input_for",
                        "output_from",
                        "structured_model",
                        "description",
                        "title",
                    }:
                        metadata.extra[k] = v

        return metadata


def create_field(
    field_type: Type[T],
    default: Any = None,
    default_factory: Optional[Callable[[], T]] = None,
    metadata: Optional[FieldMetadata] = None,
    description: Optional[str] = None,
    shared: bool = False,
    reducer: Optional[Callable] = None,
    make_optional: bool = True,
    **kwargs,
) -> Tuple[Type, Field]:
    """
    Create a standardized Pydantic field with consistent metadata handling.

    Args:
        field_type: The type of the field
        default: Default value (used if default_factory is None)
        default_factory: Optional factory function for default value
        metadata: Optional FieldMetadata object for comprehensive metadata
        description: Optional field description (ignored if metadata is provided)
        shared: Whether field is shared with parent (ignored if metadata is provided)
        reducer: Optional reducer function (ignored if metadata is provided)
        make_optional: Whether to make the field Optional if it's not already
        **kwargs: Additional field parameters

    Returns:
        Tuple of (field_type, field_info) ready for Pydantic model creation
    """
    from typing import Optional as OptionalType

    # Process field type
    if (
        make_optional
        and field_type is not type(None)
        and get_origin(field_type) is not OptionalType
    ):
        field_type = OptionalType[field_type]

    # Prepare field metadata
    meta = metadata or FieldMetadata(
        description=description, shared=shared, reducer=reducer, **kwargs
    )

    # Build field parameters
    field_params = meta.to_dict()

    # Handle default value or factory
    if default_factory is not None:
        field_info = Field(default_factory=default_factory, **field_params)
    else:
        field_info = Field(default=default, **field_params)

    # Return the field definition
    return field_type, field_info


def create_annotated_field(
    field_type: Type[T],
    default: Any = None,
    default_factory: Optional[Callable[[], T]] = None,
    metadata: Optional[FieldMetadata] = None,
    description: Optional[str] = None,
    shared: bool = False,
    reducer: Optional[Callable] = None,
    make_optional: bool = True,
    **kwargs,
) -> Tuple[Type, Field]:
    """Create a Pydantic field using Python's Annotated type for embedded metadata.

    This function creates a field for Pydantic models using the Annotated type to embed
    metadata directly in the type annotation. This approach aligns with Pydantic v2's
    design and provides better support for schema composition and manipulation.

    By embedding metadata in the Annotated type, field properties like shared status
    and reducer functions stay attached to the field type itself, which allows them
    to be preserved during operations like schema composition and subclassing.

    The function supports both direct metadata parameters (description, shared, reducer)
    and a comprehensive FieldMetadata object for more complex metadata.

    Args:
        field_type (Type[T]): The Python type of the field (e.g., str, List[int])
        default (Any, optional): Default value for the field. Used if default_factory
            is not provided. Defaults to None.
        default_factory (Optional[Callable[[], T]], optional): Factory function that
            returns the default value. Takes precedence over default if both are
            provided. Defaults to None.
        metadata (Optional[FieldMetadata], optional): Comprehensive field metadata
            object. If provided, other metadata parameters (description, shared,
            reducer) are ignored. Defaults to None.
        description (Optional[str], optional): Human-readable description of the field.
            Ignored if metadata is provided. Defaults to None.
        shared (bool, optional): Whether the field is shared with parent graphs.
            Ignored if metadata is provided. Defaults to False.
        reducer (Optional[Callable], optional): Function to combine field values during
            updates. Ignored if metadata is provided. Defaults to None.
        make_optional (bool, optional): Whether to make the field Optional[T] if it's
            not already. This ensures the field can be None, which is important for
            state management. Defaults to True.
        **kwargs: Additional field parameters passed to FieldMetadata or Field.

    Returns:
        Tuple[Type, Field]: A tuple containing:
            - field_type: The annotated type with embedded metadata
            - field_info: The Pydantic Field object with standard properties

    Example:
        ```python
        from typing import List
        from pydantic import create_model, Field
        import operator

        # Create an annotated field with shared status and reducer
        field_type, field_info = create_annotated_field(
            field_type=List[str],
            default_factory=list,
            description="List of items",
            shared=True,
            reducer=operator.add
        )

        # Create a model using the field
        MyModel = create_model(
            "MyModel",
            items=(field_type, field_info)
        )

        # The model will have "items" as a shared field with an add reducer
        # The metadata stays attached to the field type
        ```
    """
    from typing import Optional as OptionalType

    # Prepare field metadata
    meta = metadata or FieldMetadata(
        description=description, shared=shared, reducer=reducer, **kwargs
    )

    # Get base type (unwrap Optional if needed)
    base_type = field_type
    if get_origin(field_type) is OptionalType:
        base_type = get_args(field_type)[0]

    # Create Annotated type with metadata
    meta_objects = meta.to_annotation_metadata()
    if meta_objects:
        annotated_type = Annotated[(base_type, *meta_objects)]

        # Re-wrap in Optional if needed
        if make_optional or get_origin(field_type) is OptionalType:
            field_type = OptionalType[annotated_type]
        else:
            field_type = annotated_type
    elif make_optional and get_origin(field_type) is not OptionalType:
        field_type = OptionalType[field_type]

    # Build field parameters (only basic ones for Field constructor)
    field_params = {}
    if meta.description:
        field_params["description"] = meta.description
    if meta.title:
        field_params["title"] = meta.title

    # Add standard Field parameters from extra
    standard_params = {
        "gt",
        "ge",
        "lt",
        "le",
        "multiple_of",
        "min_items",
        "max_items",
        "min_length",
        "max_length",
        "pattern",
        "discriminator",
        "json_schema_extra",
        "validation_alias",
        "serialization_alias",
        "validation_alias_priority",
        "serialization_alias_priority",
        "deprecated",
        "examples",
    }

    for k, v in meta.extra.items():
        if k in standard_params:
            field_params[k] = v

    # Handle default value or factory
    if default_factory is not None:
        field_info = Field(default_factory=default_factory, **field_params)
    else:
        field_info = Field(default=default, **field_params)

    # Return the field definition
    return field_type, field_info


def extract_field_info(
    field_info: Field,
) -> Tuple[Any, Optional[Callable], Dict[str, Any]]:
    """
    Extract useful information from a Pydantic Field object.

    Args:
        field_info: Pydantic Field object

    Returns:
        Tuple of (default_value, default_factory, metadata_dict)
    """
    # Extract default or default_factory
    default = getattr(field_info, "default", ...)
    default_factory = getattr(field_info, "default_factory", None)

    # Extract metadata
    metadata = {}
    for key in ["description", "title"]:
        value = getattr(field_info, key, None)
        if value is not None:
            metadata[key] = value

    # Extract extra (varies between Pydantic v1 and v2)
    if hasattr(field_info, "json_schema_extra") and field_info.json_schema_extra:
        metadata.update(field_info.json_schema_extra)
    elif hasattr(field_info, "extra") and field_info.extra:
        metadata.update(field_info.extra)

    return default, default_factory, metadata


def extract_type_metadata(
    type_annotation: Type,
) -> Tuple[Type, Optional[FieldMetadata]]:
    """
    Extract base type and metadata from a type annotation.

    Args:
        type_annotation: Type annotation to extract from

    Returns:
        Tuple of (base_type, field_metadata)
    """
    # For Annotated types, extract metadata
    if get_origin(type_annotation) is Annotated:
        args = get_args(type_annotation)
        base_type = args[0]
        metadata = FieldMetadata.from_annotation(type_annotation)
        return base_type, metadata

    # For Optional[Annotated[...]] types
    from typing import Optional as OptionalType

    if get_origin(type_annotation) is OptionalType:
        inner_type = get_args(type_annotation)[0]
        if get_origin(inner_type) is Annotated:
            base_type, metadata = extract_type_metadata(inner_type)
            return OptionalType[base_type], metadata

    # For other types, return as is with no metadata
    return type_annotation, None


def format_type_annotation(type_annotation: Type) -> str:
    """
    Format a type annotation for display or documentation.

    Args:
        type_annotation: Type annotation to format

    Returns:
        Formatted string representation of the type
    """
    # Handle primitive types
    if type_annotation is str:
        return "str"
    if type_annotation is int:
        return "int"
    if type_annotation is float:
        return "float"
    if type_annotation is bool:
        return "bool"
    if type_annotation is list or type_annotation is List:
        return "List"
    if type_annotation is dict or type_annotation is Dict:
        return "Dict"
    if type_annotation is None or type_annotation is type(None):
        return "None"

    # Get origin and arguments
    origin = get_origin(type_annotation)
    args = get_args(type_annotation)

    # Handle None origin
    if origin is None:
        if isinstance(type_annotation, ForwardRef):
            return f'"{type_annotation.__forward_arg__}"'
        if hasattr(type_annotation, "__name__"):
            if (
                hasattr(type_annotation, "__module__")
                and type_annotation.__module__ != "builtins"
            ):
                return f"{type_annotation.__module__}.{type_annotation.__name__}"
            return type_annotation.__name__
        return str(type_annotation).replace("typing.", "")

    # Extract base type name
    if hasattr(origin, "__name__"):
        origin_name = origin.__name__
    else:
        origin_name = str(origin).replace("typing.", "")

    # Handle special cases
    from typing import Optional as OptionalType

    if origin is OptionalType:
        inner_type = format_type_annotation(args[0])
        return f"Optional[{inner_type}]"
    elif origin is Union:
        # Check if it's Optional (Union with None)
        if len(args) == 2 and (args[1] is None or args[1] is type(None)):
            inner_type = format_type_annotation(args[0])
            return f"Optional[{inner_type}]"
        elif len(args) == 2 and (args[0] is None or args[0] is type(None)):
            inner_type = format_type_annotation(args[1])
            return f"Optional[{inner_type}]"
        else:
            inner_types = [format_type_annotation(arg) for arg in args]
            return f"Union[{', '.join(inner_types)}]"
    elif origin is list or origin is List:
        if args:
            inner_type = format_type_annotation(args[0])
            return f"List[{inner_type}]"
        return "List"
    elif origin is dict or origin is Dict:
        if len(args) == 2:
            key_type = format_type_annotation(args[0])
            value_type = format_type_annotation(args[1])
            return f"Dict[{key_type}, {value_type}]"
        return "Dict"
    elif origin is Annotated:
        # For Annotated types, format the base type but ignore metadata
        return format_type_annotation(args[0])

    # Generic handling
    if args:
        inner_types = [format_type_annotation(arg) for arg in args]
        return f"{origin_name}[{', '.join(inner_types)}]"

    return origin_name


def get_common_reducers() -> Dict[str, Callable]:
    """
    Get a registry of common reducer functions.

    Returns:
        Dictionary of reducer name -> reducer function
    """
    reducers = {}

    # Add operator module reducers
    for name in dir(operator):
        if not name.startswith("_"):
            func = getattr(operator, name)
            if callable(func):
                reducers[f"operator.{name}"] = func
                reducers[name] = (
                    func  # Also store without prefix for backward compatibility
                )

    # Add common list operations
    def add_lists(a, b):
        return (a or []) + (b or [])

    reducers["add_lists"] = add_lists

    def concat_lists(a, b):
        return (a or []) + (b or [])

    reducers["concat_lists"] = concat_lists

    # Try to import langgraph's add_messages if available
    try:
        from langgraph.graph import add_messages

        reducers["add_messages"] = add_messages
    except ImportError:
        # Fallback implementation
        def add_messages(a, b):
            return (a or []) + (b or [])

        reducers["add_messages"] = add_messages

    # Add string operations
    def concat_strings(a, b):
        return (a or "") + (b or "")

    reducers["concat_strings"] = concat_strings

    # Add numeric operations
    def sum_values(a, b):
        return (a or 0) + (b or 0)

    reducers["sum_values"] = sum_values

    # Add other common functions
    reducers["max"] = max
    reducers["min"] = min

    return reducers


def resolve_reducer(reducer_name: str) -> Optional[Callable]:
    """
    Resolve a reducer function from its name.

    Args:
        reducer_name: Name of the reducer to resolve

    Returns:
        Callable reducer function or None if not found
    """
    # Check common reducers first
    common_reducers = get_common_reducers()
    if reducer_name in common_reducers:
        return common_reducers[reducer_name]

    # Handle operator module functions
    if reducer_name.startswith("operator."):
        func_name = reducer_name.split(".", 1)[1]
        if hasattr(operator, func_name):
            return getattr(operator, func_name)

    # Try to import by module.function_name
    if "." in reducer_name:
        try:
            module_name, func_name = reducer_name.rsplit(".", 1)
            module = __import__(module_name, fromlist=[func_name])
            return getattr(module, func_name)
        except (ImportError, AttributeError):
            logger.warning(f"Could not resolve reducer: {reducer_name}")
            pass

    # Special case for lambda
    if reducer_name == "<lambda>":

        def generic_lambda_reducer(a, b):
            # Simple fallback that concatenates lists or dicts, otherwise takes b
            if isinstance(a, (list, tuple)) and isinstance(b, (list, tuple)):
                return a + b
            elif isinstance(a, dict) and isinstance(b, dict):
                result = a.copy()
                result.update(b)
                return result
            return b

        return generic_lambda_reducer

    # Could not resolve
    return None


def infer_field_type(value: Any) -> Type:
    """
    Infer the field type from a value.

    Args:
        value: Value to infer type from

    Returns:
        Inferred type
    """
    from typing import Any as AnyType
    from typing import Dict, List, Optional

    if value is None:
        return Optional[AnyType]
    elif isinstance(value, str):
        return Optional[str]
    elif isinstance(value, int):
        return Optional[int]
    elif isinstance(value, float):
        return Optional[float]
    elif isinstance(value, bool):
        return Optional[bool]
    elif isinstance(value, list):
        if value and all(isinstance(x, type(value[0])) for x in value):
            item_type = infer_field_type(value[0])
            # Strip Optional from item_type
            if get_origin(item_type) is Optional:
                item_type = get_args(item_type)[0]
            return Optional[List[item_type]]
        return Optional[List[AnyType]]
    elif isinstance(value, dict):
        if value and all(isinstance(k, str) for k in value.keys()):
            return Optional[Dict[str, AnyType]]
        return Optional[Dict[AnyType, AnyType]]
    return Optional[AnyType]
