
haive.core.engine.document.loaders.sources.registry
===================================================

.. py:module:: haive.core.engine.document.loaders.sources.registry

.. autoapi-nested-parse::

   Source registry with decorator-based registration.

   This module provides a registry for document sources that maps:
   - File extensions to source classes
   - URL patterns to source classes
   - Schemes to source classes
   - Source classes to their associated loaders

   The registry enables automatic source detection and loader selection.






Functions
---------

   register_source
.. autofunction:: register_source

Classes
-------

* :py:class:`LoaderMapping` - Mapping of a loader to a source.* :py:class:`SourceRegistration` - Complete registration info for a source.* :py:class:`SourceRegistry` - Registry for document sources and their loaders.
.. toctree::
   :hidden:
   :maxdepth: 1

   /api_clean/haive/core/engine/document/loaders/sources/registry/LoaderMapping   /api_clean/haive/core/engine/document/loaders/sources/registry/SourceRegistration   /api_clean/haive/core/engine/document/loaders/sources/registry/SourceRegistry

Package Contents
----------------

.. rubric:: haive.core.engine.document.loaders.sources.registry.__all__

.. autosummary::
   :nosignatures:

   LoaderMapping   SourceRegistration   SourceRegistry   register_source   source_registry
.. automodule:: haive.core.engine.document.loaders.sources.registry
   :members:
   :show-inheritance:
