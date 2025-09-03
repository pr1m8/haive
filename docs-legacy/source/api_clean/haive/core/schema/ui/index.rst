
haive.core.schema.ui
====================

.. py:module:: haive.core.schema.ui

.. autoapi-nested-parse::

   UI utilities for displaying and visualizing schemas in a user-friendly way.

   This module provides the SchemaUI class, which offers rich-formatted visualization
   of schemas in the Haive Schema System. It allows for displaying schema structures,
   generating equivalent Python code representations, and comparing schemas side by side
   to identify differences.

   The SchemaUI is designed to work with the Rich library to provide colorized,
   structured terminal output for both schema classes and instances. This makes
   it invaluable for debugging, development, and educational purposes when working
   with the Haive Schema System.

   Key features include:
   - Rich terminal visualization of schema structure
   - Python code generation for schema definitions
   - Side-by-side schema comparison
   - Specialized handling for StateSchema features
   - Support for both class and instance visualization
   - Highlight of important schema features like shared fields and reducers

   .. admonition:: Example

      ```python
      from haive.core.schema import SchemaUI
      from haive.core.schema import SchemaComposer
      from typing import List
      
      # Create a schema
      composer = SchemaComposer(name="MyState")
      composer.add_field(
          name="messages",
          field_type=List[str],
          default_factory=list
      )
      MyState = composer.build()
      
      # Display schema structure
      SchemaUI.display_schema(MyState)
      
      # Generate Python code representation
      code = SchemaUI.schema_to_code(MyState)
      print(code)
      
      # Create an instance and display it
      state = MyState(messages=["Hello"])
      SchemaUI.display_schema(state, title="State Instance")
      ```






Functions
---------

   display_schema
.. autofunction:: display_schema

Classes
-------

* :py:class:`SchemaUI` - UI utilities for visualizing and working with schemas.
.. toctree::
   :hidden:
   :maxdepth: 1

   /api_clean/haive/core/schema/ui/SchemaUI

Package Contents
----------------

