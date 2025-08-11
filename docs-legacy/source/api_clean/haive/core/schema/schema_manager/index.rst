
haive.core.schema.schema_manager
================================

.. py:module:: haive.core.schema.schema_manager

.. autoapi-nested-parse::

   StateSchemaManager for creating and manipulating state schemas.

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

   .. admonition:: Example

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







Classes
-------

* :py:class:`StateSchemaManager` - Manager for dynamically creating and manipulating state schemas.
.. toctree::
   :hidden:
   :maxdepth: 1

   /api_clean/haive/core/schema/schema_manager/StateSchemaManager

Package Contents
----------------

