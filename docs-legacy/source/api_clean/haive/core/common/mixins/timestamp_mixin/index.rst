
haive.core.common.mixins.timestamp_mixin
========================================

.. py:module:: haive.core.common.mixins.timestamp_mixin

.. autoapi-nested-parse::

   mixins.timestamps.
   =================

   Reusable timestamp mixins for Pydantic models.

   This module provides composable mixins for automatic creation and access
   timestamps in Pydantic models, with built-in UTC, field freezing, custom
   serialization, and age calculation (as both seconds and human-readable string).

   Mixins:
       - CreatedTimestampMixin: Adds a frozen `created_at` datetime field.
       - AccessTimestampsMixin: Adds a frozen `last_accessed_at` datetime field,
         internal touch logic, and computed age fields.

   Typical usage example:

       class MyLog(CreatedTimestampMixin):
           event: str

       class MySession(AccessTimestampsMixin):
           user_id: int

       log = MyLog(event="example")
       session = MySession(user_id=42)
       print(log.created_at)          # UTC datetime of creation
       print(session.age_human)       # e.g. '0 minutes, 2 seconds'

   All datetime fields are timezone-aware (UTC).
   All serialization returns integer POSIX timestamps for compatibility.

   Intended for use with Sphinx AutoAPI and Google-style docstrings.






Functions
---------

   utcnow   to_int_timestamp
.. autofunction:: utcnow
.. autofunction:: to_int_timestamp

Classes
-------

* :py:class:`CreatedTimestampMixin` - Mixin to provide a frozen, auto-populated UTC `created_at` timestamp field.* :py:class:`AccessTimestampsMixin` - Mixin to add a frozen `last_accessed_at` timestamp, `touch` logic, and age calculation.
.. toctree::
   :hidden:
   :maxdepth: 1

   /api_clean/haive/core/common/mixins/timestamp_mixin/CreatedTimestampMixin   /api_clean/haive/core/common/mixins/timestamp_mixin/AccessTimestampsMixin

Package Contents
----------------

