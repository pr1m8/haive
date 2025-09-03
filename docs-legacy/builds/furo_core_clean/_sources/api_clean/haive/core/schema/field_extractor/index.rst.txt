
haive.core.schema.field_extractor
=================================

.. py:module:: haive.core.schema.field_extractor

.. autoapi-nested-parse::

   Field extractor utility for the Haive Schema System.

   from typing import Any
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

   .. admonition:: Example

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







Classes
-------

* :py:class:`FieldExtractor` - Unified utility for extracting field definitions from various sources.
.. toctree::
   :hidden:
   :maxdepth: 1

   /api_clean/haive/core/schema/field_extractor/FieldExtractor

Package Contents
----------------

