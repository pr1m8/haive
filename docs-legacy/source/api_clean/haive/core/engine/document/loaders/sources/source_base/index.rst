
haive.core.engine.document.loaders.sources.source_base
======================================================

.. py:module:: haive.core.engine.document.loaders.sources.source_base

.. autoapi-nested-parse::

   Base source classes for document loaders.

   Sources are data models that represent where documents come from.
   They don't load documents themselves - they just hold the configuration
   and metadata needed by loaders.







Classes
-------

* :py:class:`BaseSource` - Abstract base class for all document sources.* :py:class:`LocalSource` - Base class for local file sources.* :py:class:`DirectorySource` - Source for directory of files.* :py:class:`RemoteSource` - Base class for remote sources with credential support.* :py:class:`DatabaseSource` - Base class for database sources.* :py:class:`CloudSource` - Base class for cloud storage sources.
.. toctree::
   :hidden:
   :maxdepth: 1

   /api_clean/haive/core/engine/document/loaders/sources/source_base/BaseSource   /api_clean/haive/core/engine/document/loaders/sources/source_base/LocalSource   /api_clean/haive/core/engine/document/loaders/sources/source_base/DirectorySource   /api_clean/haive/core/engine/document/loaders/sources/source_base/RemoteSource   /api_clean/haive/core/engine/document/loaders/sources/source_base/DatabaseSource   /api_clean/haive/core/engine/document/loaders/sources/source_base/CloudSource

Package Contents
----------------

.. rubric:: haive.core.engine.document.loaders.sources.source_base.__all__

.. autosummary::
   :nosignatures:

   BaseSource   CloudSource   DatabaseSource   DirectorySource   LocalSource   RemoteSource
.. automodule:: haive.core.engine.document.loaders.sources.source_base
   :members:
   :show-inheritance:
