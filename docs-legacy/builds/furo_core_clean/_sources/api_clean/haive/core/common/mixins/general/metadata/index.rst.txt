
haive.core.common.mixins.general.metadata
=========================================

.. py:module:: haive.core.common.mixins.general.metadata

.. autoapi-nested-parse::

   Metadata mixin for arbitrary key-value storage.

   This module provides a mixin for adding flexible metadata storage to
   Pydantic models. It enables storing arbitrary key-value pairs as additional
   information that may not warrant dedicated model fields.

   Usage:
       ```python
       from pydantic import BaseModel
       from haive.core.common.mixins.general import MetadataMixin

       class Document(MetadataMixin, BaseModel):
           title: str
           content: str

       # Create a document with metadata
       doc = Document(
           title="Example",
           content="Sample content",
           metadata={"author": "John Doe", "tags": ["example", "sample"]}
       )

       # Add additional metadata
       doc.add_metadata("created_at", "2025-06-19")

       # Access metadata
       author = doc.get_metadata("author")  # "John Doe"

       # Check if metadata exists
       if doc.has_metadata("tags"):
           tags = doc.get_metadata("tags")
       ```







Classes
-------

* :py:class:`MetadataMixin` - Mixin for adding flexible metadata storage capabilities.
.. toctree::
   :hidden:
   :maxdepth: 1

   /api_clean/haive/core/common/mixins/general/metadata/MetadataMixin

Package Contents
----------------

