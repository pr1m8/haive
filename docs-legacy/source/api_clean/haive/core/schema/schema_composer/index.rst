
haive.core.schema.schema_composer
=================================

.. py:module:: haive.core.schema.schema_composer

.. autoapi-nested-parse::

   SchemaComposer for the Haive Schema System.

   from typing import Any, Optional
   This module provides the SchemaComposer class, which offers a streamlined API for
   building state schemas dynamically from various components. The SchemaComposer is
   designed for schema composition, enabling the creation of complex state schemas by
   combining fields from multiple sources.

   The SchemaComposer is particularly useful for:
   - Building schemas from heterogeneous components (engines, models, dictionaries)
   - Dynamically creating schemas at runtime based on available components
   - Composing schemas with proper field sharing, reducers, and engine I/O mappings
   - Ensuring consistent state handling across complex agent architectures

   Key features include:
   - Automatic field extraction from components
   - Field definition management with comprehensive metadata
   - Support for shared fields between parent and child graphs
   - Tracking of engine input/output relationships
   - Integration with structured output models
   - Rich visualization for debugging and analysis

   .. admonition:: Example

      ```python
      from haive.core.schema import SchemaComposer
      from typing import List
      from langchain_core.messages import BaseMessage
      from pydantic import Field
      import operator
      
      # Create a new composer
      composer = SchemaComposer(name="ConversationState")
      
      # Add fields manually
      composer.add_field(
          name="messages",
          field_type=List[BaseMessage],
          default_factory=list,
          description="Conversation history",
          shared=True,
          reducer="add_messages"
      )
      
      composer.add_field(
          name="context",
          field_type=List[str],
          default_factory=list,
          description="Retrieved document contexts",
          reducer=operator.add
      )
      
      # Extract fields from components
      composer.add_fields_from_components([
          retriever_engine,
          llm_engine,
          memory_component
      ])
      
      # Build the schema
      ConversationState = composer.build()
      
      # Use the schema
      state = ConversationState()
      ```







Classes
-------

* :py:class:`SchemaComposer` - Utility for building state schemas dynamically from component fields.
.. toctree::
   :hidden:
   :maxdepth: 1

   /api_clean/haive/core/schema/schema_composer/SchemaComposer

Package Contents
----------------

