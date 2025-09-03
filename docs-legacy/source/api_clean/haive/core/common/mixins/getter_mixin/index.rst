
haive.core.common.mixins.getter_mixin
=====================================

.. py:module:: haive.core.common.mixins.getter_mixin

.. autoapi-nested-parse::

   Collection utility mixin providing flexible query capabilities.

   This module provides a mixin class that adds powerful filtering and lookup
   capabilities to collection classes. It enables attribute-based lookups,
   type filtering, predicate-based searches, and more.

   Usage:
       ```python
       from typing import List
       from haive.core.common.mixins import GetterMixin

       class UserCollection(GetterMixin[User]):
           def __init__(self, users: List[User]):
               self._users = users

           def _get_items(self) -> List[User]:
               return self._users

       # Create collection
       users = UserCollection([
           User(id="1", name="Alice", role="admin"),
           User(id="2", name="Bob", role="user"),
           User(id="3", name="Charlie", role="user")
       ])

       # Find all users with role="user"
       user_role_users = users.get_all_by_attr("role", "user")

       # Find first admin
       admin = users.get_by_attr("role", "admin")

       # Get all usernames
       names = users.field_values("name")
       ```







Classes
-------

* :py:class:`GetterMixin` - A mixin providing rich lookup and filtering capabilities for collections.
.. toctree::
   :hidden:
   :maxdepth: 1

   /api_clean/haive/core/common/mixins/getter_mixin/GetterMixin

Package Contents
----------------

