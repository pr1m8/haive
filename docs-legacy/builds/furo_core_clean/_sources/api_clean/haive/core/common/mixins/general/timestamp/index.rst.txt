
haive.core.common.mixins.general.timestamp
==========================================

.. py:module:: haive.core.common.mixins.general.timestamp

.. autoapi-nested-parse::

   Timestamp mixin for tracking creation and modification times.

   This module provides a mixin for adding timestamp tracking to Pydantic models.
   It automatically records creation time and provides methods for updating and
   querying timestamps, which is useful for auditing, caching, and expiration logic.

   Usage:
       ```python
       from pydantic import BaseModel
       from haive.core.common.mixins.general import TimestampMixin

       class Document(TimestampMixin, BaseModel):
           title: str
           content: str

       # Create a document (timestamps automatically set)
       doc = Document(title="Example", content="Content")

       # Check how old the document is
       age = doc.age_in_seconds()

       # Update document and its timestamp
       doc.content = "Updated content"
       doc.update_timestamp()

       # Check time since last update
       time_since_update = doc.time_since_update()
       ```







Classes
-------

* :py:class:`TimestampMixin` - Mixin for adding timestamp tracking to Pydantic models.
.. toctree::
   :hidden:
   :maxdepth: 1

   /api_clean/haive/core/common/mixins/general/timestamp/TimestampMixin

Package Contents
----------------

