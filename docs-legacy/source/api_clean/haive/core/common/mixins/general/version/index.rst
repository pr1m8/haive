
haive.core.common.mixins.general.version
========================================

.. py:module:: haive.core.common.mixins.general.version

.. autoapi-nested-parse::

   Version mixin for tracking object versions.

   This module provides a mixin for adding version tracking to Pydantic models.
   It tracks the current version and maintains a history of previous versions,
   which is useful for auditing, compatibility checking, and change tracking.

   Usage:
       ```python
       from pydantic import BaseModel
       from haive.core.common.mixins.general import VersionMixin

       class Document(VersionMixin, BaseModel):
           title: str
           content: str

       # Create a document with default version 1.0.0
       doc = Document(title="Example", content="Content")

       # Make changes and bump version
       doc.content = "Updated content"
       doc.bump_version("1.1.0")

       # Check version history
       history = doc.get_version_history()  # ['1.0.0', '1.1.0']
       ```







Classes
-------

* :py:class:`VersionMixin` - Mixin for adding version tracking to Pydantic models.
.. toctree::
   :hidden:
   :maxdepth: 1

   /api_clean/haive/core/common/mixins/general/version/VersionMixin

Package Contents
----------------

