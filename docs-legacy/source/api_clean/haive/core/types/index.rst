
:py:mod:`haive.core.types`
========================

.. py:module:: haive.core.types

.. autoapi-nested-parse::

   Advanced type system module for the Haive framework.

   This module provides specialized type definitions and utilities that enhance
   Python's type system for use within the Haive framework. It includes dynamic
   enumerations, serializable callables, advanced registries, and other type-related
   utilities for flexible, extensible, and type-safe code.

   The types system enables runtime extensibility while maintaining type safety,
   allowing components to be registered, discovered, and validated dynamically
   throughout the framework lifecycle.

   Key Components:
       DynamicEnum: Runtime-extensible enumeration types
       DynamicLiteral: Dynamic type literals for improved type hinting
       SerializableCallable: Type-safe serialization of function references
       AdvancedRegistry: Enhanced registries for component management
       TreeLeaf: Tree structure utilities for type organization

   Features:
       - Runtime enum extension with validation
       - Serializable function references
       - Dynamic type literal creation
       - Advanced component registries
       - Type-safe tree structures
       - Domain-specific type definitions

   .. admonition:: Examples

      Dynamic enumeration usage::
      
          from haive.core.types import DynamicEnum
      
          class ModelProvider(DynamicEnum):
              START_VALUES = ["openai", "anthropic", "google"]
      
          # Use initial values
          provider = "openai"
          assert provider in ModelProvider._values
      
          # Register new values at runtime
          ModelProvider.register("cohere", "mistral")
          assert "mistral" in ModelProvider._values
      
      Serializable callable::
      
          from haive.core.types import SerializableCallable
      
          def process_data(data: dict) -> dict:
              return {"processed": data}
      
          # Serialize function reference
          serializable_func = SerializableCallable(
              module="__main__",
              name="process_data"
          )
      
          # Deserialize and call
          func = serializable_func.get_callable()
          result = func({"key": "value"})
      
      Dynamic literals::
      
          from haive.core.types import DynamicLiteral
      
          # Create dynamic type literal
          SupportedModels = DynamicLiteral([
              "gpt-4", "gpt-3.5-turbo", "claude-3"
          ])
      
          # Extend at runtime
          SupportedModels.add_values(["llama-2", "mistral-7b"])

   .. seealso::

      - Python typing module documentation
      - Component registry system
      - Dynamic configuration guides




Subpackages
-----------

.. autosummary::
   :nosignatures:
   :template: autosummary/module.rst
   :toctree: .

   haive.core.types.general
.. toctree::
   :maxdepth: 2
   :hidden:

   /api_clean/haive/core/types/general/index

Submodules
----------

.. autosummary::
   :nosignatures:
   :template: autosummary/module.rst
   :toctree: .

   haive.core.types.advanced_registry   haive.core.types.dynamic_enum   haive.core.types.dynamic_literal   haive.core.types.serializable_callable   haive.core.types.tree_leaf
.. toctree::
   :maxdepth: 1
   :hidden:

   /api_clean/haive/core/types/advanced_registry/index   /api_clean/haive/core/types/dynamic_enum/index   /api_clean/haive/core/types/dynamic_literal/index   /api_clean/haive/core/types/serializable_callable/index   /api_clean/haive/core/types/tree_leaf/index





Package Contents
----------------

.. rubric:: haive.core.types.__all__

.. autosummary::
   :nosignatures:

   haive.core.types.AdvancedRegistry   haive.core.types.DynamicEnum   haive.core.types.DynamicLiteral   haive.core.types.FileTypes   haive.core.types.ProgrammingLanguages   haive.core.types.SerializableCallable

.. automodule:: haive.core.types
   :members:
   :undoc-members:
   :show-inheritance: