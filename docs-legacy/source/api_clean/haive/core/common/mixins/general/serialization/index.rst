
haive.core.common.mixins.general.serialization
==============================================

.. py:module:: haive.core.common.mixins.general.serialization

.. autoapi-nested-parse::

   Serialization mixin for enhanced data conversion capabilities.

   from typing import Any
   This module provides a mixin for adding enhanced serialization and
   deserialization capabilities to Pydantic models. It offers methods for
   converting models to dictionaries and JSON strings, and for creating models
   from dictionaries and JSON strings.

   Usage:
       ```python
       from pydantic import BaseModel
       from haive.core.common.mixins.general import SerializationMixin

       class User(SerializationMixin, BaseModel):
           id: str
           name: str
           age: int
           _private_data: str = "hidden"

       # Create a user
       user = User(id="123", name="Alice", age=30)

       # Serialize to dict (excludes _private_data by default)
       user_dict = user.to_dict()

       # Serialize to JSON with indentation
       user_json = user.to_json(indent=2)

       # Deserialize from dict
       new_user = User.from_dict(user_dict)

       # Deserialize from JSON
       new_user = User.from_json(user_json)
       ```







Classes
-------

* :py:class:`SerializationMixin` - Mixin for enhanced serialization and deserialization capabilities.
.. toctree::
   :hidden:
   :maxdepth: 1

   /api_clean/haive/core/common/mixins/general/serialization/SerializationMixin

Package Contents
----------------

