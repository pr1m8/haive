
:py:mod:`haive.core.engine.base`
========================

.. py:module:: haive.core.engine.base

.. autoapi-nested-parse::

   Base abstractions for the Haive engine system.

   This package provides the core abstractions and base classes for all engine types
   in the Haive framework. Engines are configurable factory objects that create and
   manage runtime components like LLMs, vector stores, retrievers, and tools.

   The main components include:
   - Engine: The base class for all engine types
   - EngineType: Enumeration of supported engine types
   - EngineRegistry: Centralized registry for engine instances
   - Invokable/AsyncInvokable: Protocols for objects that can be invoked
   - ComponentRef: Reference mechanism for lazy loading of components
   - ComponentFactory: Factory pattern for creating runtime components

   The engine system follows a configuration/factory pattern that separates:
   1. Serializable configuration (Engine and its subclasses)
   2. Runtime components (created by engines with create_runnable)

   This enables configuration management, serialization, and runtime optimization.





Submodules
----------

.. autosummary::
   :nosignatures:
   :template: autosummary/module.rst
   :toctree: .

   haive.core.engine.base.base   haive.core.engine.base.factory   haive.core.engine.base.protocols   haive.core.engine.base.reference   haive.core.engine.base.registry   haive.core.engine.base.types
.. toctree::
   :maxdepth: 1
   :hidden:

   /api_clean/haive/core/engine/base/base/index   /api_clean/haive/core/engine/base/factory/index   /api_clean/haive/core/engine/base/protocols/index   /api_clean/haive/core/engine/base/reference/index   /api_clean/haive/core/engine/base/registry/index   /api_clean/haive/core/engine/base/types/index





Package Contents
----------------

.. rubric:: haive.core.engine.base.__all__

.. autosummary::
   :nosignatures:

   haive.core.engine.base.AsyncInvokable   haive.core.engine.base.ComponentFactory   haive.core.engine.base.ComponentRef   haive.core.engine.base.Engine   haive.core.engine.base.EngineRegistry   haive.core.engine.base.EngineType   haive.core.engine.base.Invokable   haive.core.engine.base.InvokableEngine   haive.core.engine.base.NonInvokableEngine

.. automodule:: haive.core.engine.base
   :members:
   :undoc-members:
   :show-inheritance: