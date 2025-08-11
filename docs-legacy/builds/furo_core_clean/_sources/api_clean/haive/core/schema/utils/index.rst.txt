
haive.core.schema.utils
=======================

.. py:module:: haive.core.schema.utils

.. autoapi-nested-parse::

   Utility functions for schema manipulation in the Haive framework.

   This module provides the SchemaUtils class containing static methods for working with
   schemas in the Haive Schema System. It includes utilities for formatting type
   annotations, extracting field information, creating field definitions, and building
   schemas programmatically.

   The utilities in this module are primarily used by the SchemaComposer and
   StateSchemaManager classes, but they can also be useful for custom schema
   manipulation tasks or when working with schemas directly.

   Key capabilities include:
   - Type annotation formatting for readable representation of complex types
   - Field information extraction from Pydantic field objects
   - Pydantic field creation with proper metadata
   - Support for special types like Optional, Union, and generics
   - Helper functions for schema display and debug visualization

   .. admonition:: Example

      ```python
      from haive.core.schema.utils import SchemaUtils
      from typing import List, Optional
      
      # Format a type annotation
      type_str = SchemaUtils.format_type_annotation(List[Optional[str]])
      print(type_str)  # "List[Optional[str]]"
      
      # Extract field info from a Pydantic model
      from pydantic import BaseModel, Field
      
      class MyModel(BaseModel):
          name: str = Field(default="default", description="User name")
      
      field_info = MyModel.model_fields["name"]
      default, default_repr, desc = SchemaUtils.extract_field_info(field_info)
      # default = "default", desc = "User name"
      ```







Classes
-------

* :py:class:`SchemaUtils` - Utility functions for schema manipulation and formatting.
.. toctree::
   :hidden:
   :maxdepth: 1

   /api_clean/haive/core/schema/utils/SchemaUtils

Package Contents
----------------

