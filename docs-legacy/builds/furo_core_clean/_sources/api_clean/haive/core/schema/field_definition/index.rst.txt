
haive.core.schema.field_definition
==================================

.. py:module:: haive.core.schema.field_definition

.. autoapi-nested-parse::

   FieldDefinition for the Haive Schema System.

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

   .. admonition:: Example

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







Classes
-------

* :py:class:`FieldDefinition` - Complete field definition with metadata for the Haive Schema System.
.. toctree::
   :hidden:
   :maxdepth: 1

   /api_clean/haive/core/schema/field_definition/FieldDefinition

Package Contents
----------------

