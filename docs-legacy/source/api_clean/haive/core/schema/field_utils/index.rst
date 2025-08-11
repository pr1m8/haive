
haive.core.schema.field_utils
=============================

.. py:module:: haive.core.schema.field_utils

.. autoapi-nested-parse::

   Field utilities for the Haive Schema System.

   from typing import Any
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

   .. admonition:: Example

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






Functions
---------

   camel_to_snake_case   create_field_name_from_model   get_field_info_from_model   field_name   field_description   field_config   create_field   create_annotated_field   extract_field_info   extract_type_metadata   format_type_annotation   get_common_reducers   resolve_reducer   infer_field_type
.. autofunction:: camel_to_snake_case
.. autofunction:: create_field_name_from_model
.. autofunction:: get_field_info_from_model
.. autofunction:: field_name
.. autofunction:: field_description
.. autofunction:: field_config
.. autofunction:: create_field
.. autofunction:: create_annotated_field
.. autofunction:: extract_field_info
.. autofunction:: extract_type_metadata
.. autofunction:: format_type_annotation
.. autofunction:: get_common_reducers
.. autofunction:: resolve_reducer
.. autofunction:: infer_field_type

Classes
-------

* :py:class:`FieldMetadata` - Standardized container for field metadata in the Haive Schema System.
.. toctree::
   :hidden:
   :maxdepth: 1

   /api_clean/haive/core/schema/field_utils/FieldMetadata

Package Contents
----------------

