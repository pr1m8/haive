"""Field extractor utility for the Haive Schema System.

This module provides the FieldExtractor class, which offers a standardized way to
extract field definitions from various sources including Pydantic models, engines,
and dictionary specifications. It ensures consistent field handling throughout the
Haive Schema System, serving as a key component for dynamic schema composition.

The FieldExtractor enables automatic discovery of fields and their metadata from
existing components, making it possible to build schemas that properly integrate
with those components without manual field specification. This is particularly
valuable when working with complex systems where fields need to be shared across
multiple components or where field specifications are distributed across different
parts of the system.

Key capabilities include:
- Extracting field definitions from Pydantic models (including annotations)
- Discovering input and output fields from engine components
- Identifying shared fields and reducer functions
- Mapping engine I/O relationships for state management
- Handling structured output models

Example:
    ```python
    from haive.core.schema import FieldExtractor

    # Extract fields from a list of components
    field_defs, engine_io_mappings, structured_model_fields, structured_models = (
        FieldExtractor.extract_from_components([
            retriever_engine,
            llm_engine,
            memory_component
        ])
    )

    # Fields are returned as FieldDefinition objects
    for name, field_def in field_defs.items():
        print(f"Field: {name}, Type: {field_def.field_type}")

    # Engine I/O mappings show which fields are used by which engines
    for engine, mapping in engine_io_mappings.items():
        print(f"Engine: {engine}")
        print(f"  Inputs: {mapping['inputs']}")
        print(f"  Outputs: {mapping['outputs']}")
    ```
"""

import logging
from collections import defaultdict
from typing import (
    Any,
    Callable,
    Dict,
    List,
    Optional,
    Sequence,
    Set,
    Tuple,
    Type,
    TypeVar,
)

from pydantic import BaseModel, Field

from haive.core.schema.field_definition import FieldDefinition
from haive.core.schema.field_utils import extract_type_metadata, infer_field_type

logger = logging.getLogger(__name__)

# Type variable for return types
T = TypeVar("T")


class FieldExtractor:
    """Unified utility for extracting field definitions from various sources.

    The FieldExtractor class provides static methods for extracting field definitions,
    shared fields, reducer functions, and engine I/O mappings from various components
    in the Haive ecosystem. It's designed to work with:

    1. Pydantic models and model classes
    2. Engine components with get_input_fields/get_output_fields methods
    3. Components with structured_output_model attributes
    4. Dictionary-based field specifications

    This class is a key component of the Haive Schema System's composition capabilities,
    enabling automatic discovery and integration of fields from different parts of an
    application. By standardizing field extraction, it ensures consistent handling of
    field metadata throughout the framework.

    The extraction methods are designed to be comprehensive, gathering not only basic
    field information like types and defaults, but also Haive-specific metadata such as:
    - Whether fields are shared between parent and child graphs
    - Reducer functions for combining field values during updates
    - Input/output relationships with specific engines
    - Structured output model associations

    All methods are static and don't require instantiation of the class.
    """

    @staticmethod
    def extract_from_model(model_cls: Type[BaseModel]) -> Tuple[
        Dict[str, Tuple[Any, Any]],  # fields
        Dict[str, str],  # descriptions
        Set[str],  # shared_fields
        Dict[str, str],  # reducer_names
        Dict[str, Callable],  # reducer_functions
        Dict[str, Dict[str, List[str]]],  # engine_io_mappings
        Dict[str, Set[str]],  # input_fields
        Dict[str, Set[str]],  # output_fields
    ]:
        """
        Extract all field information from a Pydantic model.

        This method extracts standard field information as well as Haive-specific
        metadata like shared fields, reducers, and engine I/O mappings.

        Args:
            model_cls: Pydantic model class to extract from

        Returns:
            Tuple of (fields, descriptions, shared_fields, reducer_names,
                     reducer_functions, engine_io_mappings, input_fields,
                     output_fields)
        """
        fields = {}
        descriptions = {}
        shared_fields = set()
        reducer_names = {}
        reducer_functions = {}
        engine_io_mappings = {}
        input_fields = defaultdict(set)
        output_fields = defaultdict(set)

        # Check if it's a Pydantic model
        if not (isinstance(model_cls, type) and issubclass(model_cls, BaseModel)):
            logger.warning(f"Not a Pydantic model: {model_cls}")
            return (
                fields,
                descriptions,
                shared_fields,
                reducer_names,
                reducer_functions,
                engine_io_mappings,
                input_fields,
                output_fields,
            )

        # Extract shared fields from class
        if hasattr(model_cls, "__shared_fields__"):
            shared_fields.update(model_cls.__shared_fields__)

        # Extract reducer information from class
        if hasattr(model_cls, "__serializable_reducers__"):
            reducer_names.update(model_cls.__serializable_reducers__)

        if hasattr(model_cls, "__reducer_fields__"):
            reducer_functions.update(model_cls.__reducer_fields__)

        # Extract engine I/O mappings from class
        if hasattr(model_cls, "__engine_io_mappings__"):
            engine_io_mappings = model_cls.__engine_io_mappings__.copy()

        # Extract input/output field mappings
        if hasattr(model_cls, "__input_fields__"):
            for engine, fields_list in model_cls.__input_fields__.items():
                input_fields[engine].update(fields_list)

        if hasattr(model_cls, "__output_fields__"):
            for engine, fields_list in model_cls.__output_fields__.items():
                output_fields[engine].update(fields_list)

        # Get all fields from model_fields (Pydantic v2)
        for field_name, field_info in model_cls.model_fields.items():
            # Skip internal fields
            if field_name.startswith("__") or field_name == "runnable_config":
                continue

            # Get field type and extract any annotations
            field_type = field_info.annotation
            base_type, meta = extract_type_metadata(field_type)

            # Create a field definition
            field_def = FieldDefinition.extract_from_model_field(
                name=field_name, field_type=field_type, field_info=field_info
            )

            # Check if field is shared
            if field_name in shared_fields:
                field_def.shared = True

            # Check if field has a reducer
            if field_name in reducer_functions:
                field_def.reducer = reducer_functions[field_name]

            # Check if field is used in engine I/O
            for engine_name, mapping in engine_io_mappings.items():
                if field_name in mapping.get("inputs", []):
                    field_def.input_for.append(engine_name)
                    input_fields[engine_name].add(field_name)
                if field_name in mapping.get("outputs", []):
                    field_def.output_from.append(engine_name)
                    output_fields[engine_name].add(field_name)

            # Extract field info for return
            fields[field_name] = field_def.to_field_info()
            if field_def.description:
                descriptions[field_name] = field_def.description

            # Store reducer name if available
            if field_def.reducer:
                reducer_name = field_def.get_reducer_name()
                if reducer_name:
                    reducer_names[field_name] = reducer_name
                reducer_functions[field_name] = field_def.reducer

        return (
            fields,
            descriptions,
            shared_fields,
            reducer_names,
            reducer_functions,
            engine_io_mappings,
            input_fields,
            output_fields,
        )

    @staticmethod
    def extract_from_engine(
        engine: Any,
    ) -> Tuple[
        Dict[str, Tuple[Any, Any]],  # fields
        Dict[str, str],  # descriptions
        Dict[str, Dict[str, List[str]]],  # engine_io_mappings
        Dict[str, Set[str]],  # input_fields
        Dict[str, Set[str]],  # output_fields
    ]:
        """
        Extract all field information from an engine.

        This method extracts field information specific to engines, including
        input and output fields, as well as structured output models.

        Args:
            engine: Engine instance to extract from

        Returns:
            Tuple of (fields, descriptions, engine_io_mappings, input_fields, output_fields)
        """

        fields = {}
        descriptions = {}
        engine_io_mappings = {}
        input_fields = defaultdict(set)
        output_fields = defaultdict(set)

        # Extract engine name for tracking
        engine_name = getattr(engine, "name", str(engine))

        # Create an initial empty mapping for this engine
        engine_io_mappings[engine_name] = {"inputs": [], "outputs": []}

        # Try different methods to extract field information

        # Method 1: Check for get_input_fields and get_output_fields methods
        input_fields_dict = {}
        output_fields_dict = {}

        # Extract input fields
        if hasattr(engine, "get_input_fields") and callable(engine.get_input_fields):
            try:
                input_fields_dict = engine.get_input_fields()

                for field_name, (field_type, field_info) in input_fields_dict.items():
                    # Skip internal or special fields
                    if field_name.startswith("__") or field_name == "runnable_config":
                        continue

                    # Create a field definition
                    field_def = FieldDefinition(
                        name=field_name,
                        field_type=field_type,
                        field_info=field_info,
                        source=engine_name,
                        input_for=[engine_name],
                    )

                    # Extract field info for return
                    fields[field_name] = field_def.to_field_info()
                    if field_def.description:
                        descriptions[field_name] = field_def.description

                    # Track as input field
                    input_fields[engine_name].add(field_name)
            except Exception as e:
                logger.warning(f"Error getting input_fields from {engine_name}: {e}")

        # Extract output fields
        if hasattr(engine, "get_output_fields") and callable(engine.get_output_fields):
            try:
                # Only extract output fields if no structured output model
                # This prevents the duplication problem
                if (
                    not hasattr(engine, "structured_output_model")
                    or engine.structured_output_model is None
                ):
                    output_fields_dict = engine.get_output_fields()

                    for field_name, (
                        field_type,
                        field_info,
                    ) in output_fields_dict.items():
                        # Skip if field already exists - keep input fields as priority
                        if field_name in fields:
                            # Just mark as output field
                            output_fields[engine_name].add(field_name)

                            # Update existing field definition
                            field_type, field_info = fields[field_name]
                            field_def = FieldDefinition(
                                name=field_name,
                                field_type=field_type,
                                field_info=field_info,
                            )

                            # Add output_from to field
                            if engine_name not in field_def.output_from:
                                field_def.output_from.append(engine_name)

                            # Update field info
                            fields[field_name] = field_def.to_field_info()
                            continue

                        # Create a field definition
                        field_def = FieldDefinition(
                            name=field_name,
                            field_type=field_type,
                            field_info=field_info,
                            source=engine_name,
                            output_from=[engine_name],
                        )

                        # Extract field info for return
                        fields[field_name] = field_def.to_field_info()
                        if field_def.description:
                            descriptions[field_name] = field_def.description

                        # Track as output field
                        output_fields[engine_name].add(field_name)
            except Exception as e:
                logger.warning(f"Error getting output_fields from {engine_name}: {e}")

        # Method 2: Check for structured_output_model
        if (
            hasattr(engine, "structured_output_model")
            and engine.structured_output_model is not None
        ):
            try:
                model = engine.structured_output_model

                # Use proper field naming utilities
                from haive.core.schema.field_utils import get_field_info_from_model

                field_info_dict = get_field_info_from_model(model)
                model_name = field_info_dict["field_name"]
                field_description = field_info_dict.get(
                    "description", f"Output in {model.__name__} format"
                )
                field_type = field_info_dict.get("field_type", Optional[model])

                print(
                    f"FIELD_EXTRACTOR: Found structured_output_model in {engine_name}: {model.__name__} -> {model_name}"
                )
                logger.info(
                    f"Found structured_output_model in {engine_name}: {model.__name__} -> {model_name}"
                )

                # Add a single field for the entire model
                field_info = Field(default=None, description=field_description)

                # Create a field definition
                field_def = FieldDefinition(
                    name=model_name,
                    field_type=field_type,
                    field_info=field_info,
                    source=engine_name,
                    output_from=[engine_name],
                    structured_model=model.__name__,
                )

                # Extract field info for return
                fields[model_name] = field_def.to_field_info()
                descriptions[model_name] = field_def.description

                # Track as output field
                output_fields[engine_name].add(model_name)
            except Exception as e:
                logger.warning(
                    f"Error extracting structured_output_model from {engine_name}: {e}"
                )

        # Update engine I/O mappings
        engine_io_mappings[engine_name]["inputs"] = list(input_fields[engine_name])
        engine_io_mappings[engine_name]["outputs"] = list(output_fields[engine_name])

        return fields, descriptions, engine_io_mappings, input_fields, output_fields

    @staticmethod
    def extract_from_dict(data: Dict[str, Any]) -> Tuple[
        Dict[str, Tuple[Any, Any]],  # fields
        Dict[str, str],  # descriptions
        Set[str],  # shared_fields
        Dict[str, str],  # reducer_names
        Dict[str, Callable],  # reducer_functions
        Dict[str, Dict[str, List[str]]],  # engine_io_mappings
        Dict[str, Set[str]],  # input_fields
        Dict[str, Set[str]],  # output_fields
    ]:
        """
        Extract fields from a dictionary definition.

        This method extracts field information from a dictionary, which can
        be provided in various formats.

        Args:
            data: Dictionary containing field definitions

        Returns:
            Tuple of (fields, descriptions, shared_fields, reducer_names,
                     reducer_functions, engine_io_mappings, input_fields,
                     output_fields)
        """

        fields = {}
        descriptions = {}
        shared_fields = set()
        reducer_names = {}
        reducer_functions = {}
        engine_io_mappings = {}
        input_fields = defaultdict(set)
        output_fields = defaultdict(set)

        # Process special metadata keys
        for key, value in data.items():
            if key == "shared_fields":
                shared_fields.update(value)
                continue
            elif key == "reducer_names" or key == "serializable_reducers":
                reducer_names.update(value)
                continue
            elif key == "reducer_functions":
                reducer_functions.update(value)
                continue
            elif key == "field_descriptions":
                descriptions.update(value)
                continue
            elif key == "engine_io_mappings":
                engine_io_mappings.update(value)
                continue
            elif key == "input_fields":
                for engine, fields_list in value.items():
                    input_fields[engine].update(fields_list)
                continue
            elif key == "output_fields":
                for engine, fields_list in value.items():
                    output_fields[engine].update(fields_list)
                continue

            # Process field definitions
            if isinstance(value, tuple) and len(value) >= 2:
                # Handle (type, default) format
                field_type, default = value[0:2]

                # Check for extra metadata
                field_metadata = {}
                if len(value) >= 3 and isinstance(value[2], dict):
                    field_metadata = value[2]
                    if "description" in field_metadata:
                        descriptions[key] = field_metadata["description"]

                # Check if default is a factory function
                if callable(default) and not isinstance(default, type):
                    field_info = Field(default_factory=default, **field_metadata)
                else:
                    field_info = Field(default=default, **field_metadata)

                # Create field definition
                field_def = FieldDefinition(
                    name=key,
                    field_type=field_type,
                    field_info=field_info,
                    shared=key in shared_fields,
                    reducer=reducer_functions.get(key),
                )

                # Check engine I/O mappings
                for engine_name, mapping in engine_io_mappings.items():
                    if key in mapping.get("inputs", []):
                        field_def.input_for.append(engine_name)
                    if key in mapping.get("outputs", []):
                        field_def.output_from.append(engine_name)

                # Extract field info
                fields[key] = field_def.to_field_info()

                # Store reducer name if available
                if field_def.reducer:
                    reducer_name = field_def.get_reducer_name()
                    if reducer_name:
                        reducer_names[key] = reducer_name
            else:
                # Field with value only - infer type
                field_type = infer_field_type(value)
                field_info = Field(default=value)

                # Create field definition
                field_def = FieldDefinition(
                    name=key,
                    field_type=field_type,
                    field_info=field_info,
                    shared=key in shared_fields,
                    reducer=reducer_functions.get(key),
                )

                # Extract field info
                fields[key] = field_def.to_field_info()

        # Return all extracted data
        return (
            fields,
            descriptions,
            shared_fields,
            reducer_names,
            reducer_functions,
            engine_io_mappings,
            input_fields,
            output_fields,
        )

    @staticmethod
    def extract_from_components(
        components: List[Any], include_messages_field: bool = True
    ) -> Tuple[
        Dict[str, FieldDefinition],  # All field definitions
        Dict[str, Dict[str, List[str]]],  # Engine I/O mappings
        Dict[str, Set[str]],  # Structured model fields
        Dict[str, Type],  # Structured models
    ]:
        """Extract field definitions from a list of heterogeneous components.

        This is a high-level method that extracts field definitions from various
        component types (engines, models, dictionaries) and returns them in a
        consistent format. It's designed to work with mixed collections of components
        and serves as the primary entry point for schema composition.

        The method processes each component according to its type:
        - Engine components: Uses get_input_fields/get_output_fields and looks for structured_output_model
        - Pydantic models: Extracts fields, shared fields, reducers, and engine mappings
        - Dictionaries: Processes field definitions in dictionary format

        It also handles field conflict resolution by merging field definitions when
        the same field appears in multiple components.

        Args:
            components (List[Any]): List of components to extract fields from. Can include
                engine instances, Pydantic models, model classes, and dictionaries.
            include_messages_field (bool, optional): Whether to automatically add a
                messages field with appropriate reducer if one doesn't exist in the
                components. This is useful for conversation-based agents. Defaults to True.

        Returns:
            Tuple containing:
                - Dict[str, FieldDefinition]: Dictionary mapping field names to their
                  complete FieldDefinition objects
                - Dict[str, Dict[str, List[str]]]: Engine I/O mappings showing which
                  fields are inputs/outputs for which engines
                - Dict[str, Set[str]]: Structured model fields, mapping model names
                  to sets of field names within those models
                - Dict[str, Type]: Structured model types, mapping model names to
                  their actual class types

        Example:
            ```python
            # Create a list of components
            components = [
                retriever_engine,  # Engine with get_input/output_fields
                ConversationMemory(),  # Pydantic model instance
                ResponseGeneratorConfig,  # Pydantic model class
                {  # Dictionary-based field definition
                    "custom_field": (str, "", {"description": "Custom field"}),
                    "shared_fields": ["messages"]
                }
            ]

            # Extract field definitions
            field_defs, io_mappings, model_fields, models = (
                FieldExtractor.extract_from_components(components)
            )

            # Field definitions can be used with SchemaComposer
            composer = SchemaComposer(name="AgentState")
            for name, field_def in field_defs.items():
                composer.add_field_definition(field_def)

            # Build the schema
            AgentState = composer.build()
            ```
        """
        field_definitions = {}
        engine_io_mappings = {}
        structured_model_fields = defaultdict(set)
        structured_models = {}

        # Process each component
        for component in components:
            if component is None:
                continue

            # Process based on type
            if hasattr(component, "engine_type"):
                # Engine component
                fields, descriptions, io_mappings, in_fields, out_fields = (
                    FieldExtractor.extract_from_engine(component)
                )

                # Convert to FieldDefinition objects
                for field_name, (field_type, field_info) in fields.items():
                    # Check if field already exists
                    if field_name in field_definitions:
                        # Merge with existing field
                        existing_field = field_definitions[field_name]

                        # Update input_for and output_from
                        for engine_name, field_set in in_fields.items():
                            if (
                                field_name in field_set
                                and engine_name not in existing_field.input_for
                            ):
                                existing_field.input_for.append(engine_name)

                        for engine_name, field_set in out_fields.items():
                            if (
                                field_name in field_set
                                and engine_name not in existing_field.output_from
                            ):
                                existing_field.output_from.append(engine_name)
                    else:
                        # Create new field definition
                        field_def = FieldDefinition(
                            name=field_name,
                            field_type=field_type,
                            field_info=field_info,
                            source=getattr(component, "name", str(component)),
                        )

                        # Add input_for and output_from
                        for engine_name, field_set in in_fields.items():
                            if field_name in field_set:
                                field_def.input_for.append(engine_name)

                        for engine_name, field_set in out_fields.items():
                            if field_name in field_set:
                                field_def.output_from.append(engine_name)

                        field_definitions[field_name] = field_def

                # Update engine I/O mappings
                for engine_name, mapping in io_mappings.items():
                    engine_io_mappings[engine_name] = mapping

                # Check for structured output model
                if (
                    hasattr(component, "structured_output_model")
                    and component.structured_output_model
                ):
                    model = component.structured_output_model
                    model_name = model.__name__.lower()

                    # Store model reference
                    structured_models[model_name] = model

                    # Extract model fields
                    if hasattr(model, "model_fields"):
                        for field_name in model.model_fields:
                            structured_model_fields[model_name].add(field_name)

            elif isinstance(component, BaseModel):
                # Pydantic model instance
                (
                    fields,
                    descriptions,
                    shared,
                    reducer_names,
                    reducer_funcs,
                    io_mappings,
                    in_fields,
                    out_fields,
                ) = FieldExtractor.extract_from_model(component.__class__)

                # Convert to FieldDefinition objects
                for field_name, (field_type, field_info) in fields.items():
                    # Create field definition
                    field_def = FieldDefinition(
                        name=field_name,
                        field_type=field_type,
                        field_info=field_info,
                        shared=field_name in shared,
                        reducer=reducer_funcs.get(field_name),
                        source=component.__class__.__name__,
                    )

                    # Add to field definitions if not already present
                    if field_name not in field_definitions:
                        field_definitions[field_name] = field_def

                # Update engine I/O mappings
                for engine_name, mapping in io_mappings.items():
                    engine_io_mappings[engine_name] = mapping

            elif isinstance(component, type) and issubclass(component, BaseModel):
                # Pydantic model class
                (
                    fields,
                    descriptions,
                    shared,
                    reducer_names,
                    reducer_funcs,
                    io_mappings,
                    in_fields,
                    out_fields,
                ) = FieldExtractor.extract_from_model(component)

                # Convert to FieldDefinition objects
                for field_name, (field_type, field_info) in fields.items():
                    # Create field definition
                    field_def = FieldDefinition(
                        name=field_name,
                        field_type=field_type,
                        field_info=field_info,
                        shared=field_name in shared,
                        reducer=reducer_funcs.get(field_name),
                        source=component.__name__,
                    )

                    # Add to field definitions if not already present
                    if field_name not in field_definitions:
                        field_definitions[field_name] = field_def

                # Update engine I/O mappings
                for engine_name, mapping in io_mappings.items():
                    engine_io_mappings[engine_name] = mapping

            elif isinstance(component, dict):
                # Dictionary of field definitions
                (
                    fields,
                    descriptions,
                    shared,
                    reducer_names,
                    reducer_funcs,
                    io_mappings,
                    in_fields,
                    out_fields,
                ) = FieldExtractor.extract_from_dict(component)

                # Convert to FieldDefinition objects
                for field_name, (field_type, field_info) in fields.items():
                    # Create field definition
                    field_def = FieldDefinition(
                        name=field_name,
                        field_type=field_type,
                        field_info=field_info,
                        shared=field_name in shared,
                        reducer=reducer_funcs.get(field_name),
                        source="dictionary",
                    )

                    # Add to field definitions if not already present
                    if field_name not in field_definitions:
                        field_definitions[field_name] = field_def

                # Update engine I/O mappings
                for engine_name, mapping in io_mappings.items():
                    engine_io_mappings[engine_name] = mapping

        # Ensure messages field exists if requested
        if include_messages_field and "messages" not in field_definitions:

            from langchain_core.messages import BaseMessage

            # Try to use add_messages reducer if available
            reducer = None
            try:
                from langgraph.graph import add_messages

                reducer = add_messages
            except ImportError:
                # Fallback to a simple list concatenation
                def concat_lists(a, b):
                    return (a or []) + (b or [])

                reducer = concat_lists

            # Create messages field
            field_def = FieldDefinition(
                name="messages",
                field_type=Sequence[BaseMessage],
                # default_factory=list,
                description="Messages for conversation",
                reducer=reducer,
            )

            field_definitions["messages"] = field_def

        return (
            field_definitions,
            engine_io_mappings,
            structured_model_fields,
            structured_models,
        )
