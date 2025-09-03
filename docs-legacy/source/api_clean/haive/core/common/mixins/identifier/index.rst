
haive.core.common.mixins.identifier
===================================

.. py:module:: haive.core.common.mixins.identifier

.. autoapi-nested-parse::

   Identifier mixin for unique identification of objects.

   This module provides a mixin class that adds UUID-based identification and
   human-readable naming to Pydantic models. The mixin handles validation,
   generation, and utility methods for working with identifiers.

   Uses Pydantic v2 patterns with field_validator and computed fields.

   Usage:
       ```python
       from haive.core.common.mixins.identifier import IdentifierMixin

       class MyComponent(IdentifierMixin, BaseModel):
           # Other fields
           content: str

           def __init__(self, **data):
               super().__init__(**data)
               # Now the component has an ID and optional name

       # Create with auto-generated ID
       component = MyComponent(content="Hello")
       print(component.id)  # UUID string
       print(component.short_id)  # First 8 chars of UUID

       # Create with custom name
       named_component = MyComponent(content="Hello", name="GreetingComponent")
       print(named_component.display_name)  # "GreetingComponent"
       ```







Classes
-------

* :py:class:`IdentifierMixin` - Mixin that adds unique identification to any Pydantic model.
.. toctree::
   :hidden:
   :maxdepth: 1

   /api_clean/haive/core/common/mixins/identifier/IdentifierMixin

Package Contents
----------------

