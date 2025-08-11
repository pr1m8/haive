
:py:mod:`haive.core.registry`
========================

.. py:module:: haive.core.registry

.. autoapi-nested-parse::

   Registry management module for the Haive framework.

   This module provides a comprehensive registry system for managing and discovering
   components dynamically throughout the Haive framework. It supports multiple
   registry types and provides both static and dynamic registration capabilities.

   The registry system enables loose coupling between components while maintaining
   discoverability and type safety. Components can be registered at runtime and
   discovered by name or type.

   Key Components:
       RegistryManager: Central manager for all registry operations
       AbstractRegistry: Base class for custom registry implementations
       DynamicRegistry: Registry with runtime modification capabilities
       MemoryRegistry: In-memory registry implementation
       RegistryItem: Data structure for registry entries

   Registry Types:
       - Memory Registry: In-memory storage for fast access
       - Dynamic Registry: Supports runtime modification
       - File Registry: Persistent file-based storage (when available)
       - Database Registry: Database-backed registry (when available)

   Features:
       - Component discovery by name or type
       - Type-safe registration and retrieval
       - Multiple registry backend support
       - Runtime component modification
       - Registry federation and merging
       - Metadata and versioning support

   .. admonition:: Examples

      Basic registry usage::
      
          from haive.core.registry import RegistryManager
      
          # Get registry for engines
          engine_registry = RegistryManager.get_registry("engines")
      
          # Register a component
          engine_registry.register(
              name="my_engine",
              component=MyEngineClass,
              metadata={"version": "1.0.0", "type": "llm"}
          )
      
          # Retrieve component
          engine_class = engine_registry.get("my_engine")
      
      Dynamic registry operations::
      
          from haive.core.registry import DynamicRegistry, RegistryItem
      
          # Create dynamic registry
          registry = DynamicRegistry()
      
          # Register with metadata
          item = RegistryItem(
              name="advanced_engine",
              component=AdvancedEngine,
              metadata={"capabilities": ["reasoning", "memory"]},
              version="2.0.0"
          )
          registry.register_item(item)
      
          # Query by metadata
          reasoning_engines = registry.find_by_metadata(
              {"capabilities": "reasoning"}
          )
      
      Registry management::
      
          # Create custom registry type
          RegistryManager.register_registry_type(
              "custom", CustomRegistryClass
          )
      
          # Get typed registry
          custom_registry = RegistryManager.get_registry(
              "custom", registry_type="custom"
          )

   .. seealso::

      - Component architecture documentation
      - Engine registration guides
      - Plugin development guides





Submodules
----------

.. autosummary::
   :nosignatures:
   :template: autosummary/module.rst
   :toctree: .

   haive.core.registry.base   haive.core.registry.decorators   haive.core.registry.dynamic_registry   haive.core.registry.factory   haive.core.registry.manager   haive.core.registry.memory
.. toctree::
   :maxdepth: 1
   :hidden:

   /api_clean/haive/core/registry/base/index   /api_clean/haive/core/registry/decorators/index   /api_clean/haive/core/registry/dynamic_registry/index   /api_clean/haive/core/registry/factory/index   /api_clean/haive/core/registry/manager/index   /api_clean/haive/core/registry/memory/index





Package Contents
----------------

.. rubric:: haive.core.registry.__all__

.. autosummary::
   :nosignatures:

   haive.core.registry.AbstractRegistry   haive.core.registry.ComponentMetadata   haive.core.registry.DynamicRegistry   haive.core.registry.MemoryRegistry   haive.core.registry.RegistryItem   haive.core.registry.RegistryManager   haive.core.registry.register_component

.. automodule:: haive.core.registry
   :members:
   :undoc-members:
   :show-inheritance: