
haive.core.engine.document.loaders.strategy
===========================================

.. py:module:: haive.core.engine.document.loaders.strategy

.. autoapi-nested-parse::

   Loader Strategy System for Document Engine.

   This module implements the loader strategy system for intelligent loader selection
   based on source type, performance requirements, and capabilities.






Functions
---------

   create_loader
.. autofunction:: create_loader

Classes
-------

* :py:class:`LoaderPriority` - Priority levels for loader selection.* :py:class:`LoaderCapability` - Capabilities that loaders may support.* :py:class:`LoaderStrategy` - Information about a document loader strategy.* :py:class:`LoaderStrategyRegistry` - Registry for managing loader strategies.
.. toctree::
   :hidden:
   :maxdepth: 1

   /api_clean/haive/core/engine/document/loaders/strategy/LoaderPriority   /api_clean/haive/core/engine/document/loaders/strategy/LoaderCapability   /api_clean/haive/core/engine/document/loaders/strategy/LoaderStrategy   /api_clean/haive/core/engine/document/loaders/strategy/LoaderStrategyRegistry

Package Contents
----------------

.. rubric:: haive.core.engine.document.loaders.strategy.__all__

.. autosummary::
   :nosignatures:

   LoaderCapability   LoaderPriority   LoaderStrategy   LoaderStrategyRegistry   create_loader   strategy_registry
.. automodule:: haive.core.engine.document.loaders.strategy
   :members:
   :show-inheritance:
