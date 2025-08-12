
:py:mod:`base`
==============

.. py:module:: base

User management models and enums.

This module provides data structures and enumerations for representing users
and their roles within the system. It includes the core `User` model and the
`UserRole` enum used to control access and behavior across different parts of
the application.

Modules:
    models: Defines the `User` Pydantic model with validation and serialization.
    enums: Provides the `UserRole` and related enumerations used throughout the app.

.. rubric:: Examples

>>> from myapp.users import User, UserRole
>>> user = User(id=1, name="Alice", email="alice@company.com", role=UserRole.ADMIN)
>>> print(user.name)
Alice


.. autolink-examples:: base
   :collapse:

Classes
-------

.. autoapisummary::

   base.User
   base.UserRole


Module Contents
---------------




.. toggle:: Show Inheritance Diagram

   Inheritance diagram for User:

   .. graphviz::
      :align: center

      digraph inheritance_User {
        node [shape=record];
        "User" [label="User"];
        "pydantic.BaseModel" -> "User";
      }

.. autopydantic_model:: base.User
   :members:
   :undoc-members:
   :show-inheritance:
   :model-show-field-summary:
   :model-show-config-summary:
   :model-show-validator-members:
   :model-show-validator-summary:
   :model-show-json:
   :field-list-validators:
   :field-show-constraints:





.. toggle:: Show Inheritance Diagram

   Inheritance diagram for UserRole:

   .. graphviz::
      :align: center

      digraph inheritance_UserRole {
        node [shape=record];
        "UserRole" [label="UserRole"];
        "str" -> "UserRole";
        "enum.Enum" -> "UserRole";
      }

.. autoclass:: base.UserRole
   :members:
   :undoc-members:
   :show-inheritance:

   .. note::

      **UserRole** is an Enum defined in ``base``.





.. rubric:: Related Links

.. autolink-examples:: base
   :collapse:
   
.. autolink-skip:: next
