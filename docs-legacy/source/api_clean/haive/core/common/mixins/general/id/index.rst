
haive.core.common.mixins.general.id
===================================

.. py:module:: haive.core.common.mixins.general.id

.. autoapi-nested-parse::

   ID mixin for basic identification capabilities.

   from typing import Any
   This module provides a simple mixin for adding UUID-based identification
   to Pydantic models. It's a lightweight alternative to the more comprehensive
   IdentifierMixin when only basic ID capabilities are needed.

   Usage:
       ```python
       from pydantic import BaseModel
       from haive.core.common.mixins.general import IdMixin

       class MyComponent(IdMixin, BaseModel):
           name: str

           def __init__(self, **data):
               super().__init__(**data)
               # Now the component has a UUID string ID

       # Create with auto-generated ID
       component = MyComponent(name="Test")
       print(component.id)  # UUID string

       # Create with specific ID
       custom_component = MyComponent.with_id("custom-id-123", name="Custom")
       print(custom_component.id)  # "custom-id-123"
       ```







Classes
-------

* :py:class:`IdMixin` - Mixin for adding basic ID generation and management capabilities.
.. toctree::
   :hidden:
   :maxdepth: 1

   /api_clean/haive/core/common/mixins/general/id/IdMixin

Package Contents
----------------

