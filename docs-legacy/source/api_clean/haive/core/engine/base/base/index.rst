
haive.core.engine.base.base
===========================

.. py:module:: haive.core.engine.base.base

.. autoapi-nested-parse::

   Core engine abstractions for the Haive framework.

   This module provides the base classes and abstractions for all engines in the Haive framework.
   Engines are the core components that provide a consistent interface for creating and using
   AI components like LLMs, retrievers, vector stores, etc.

   The Engine class is a configuration/factory class that produces runnable objects,
   not an invokable itself. It standardizes how engines define their input and output
   field requirements.







Classes
-------

* :py:class:`Engine` - Abstract base class for all engine configurations.* :py:class:`InvokableEngine` - Base class for engines that create invokable runtime objects.* :py:class:`NonInvokableEngine` - Base class for engines that create non-invokable utility objects.
.. toctree::
   :hidden:
   :maxdepth: 1

   /api_clean/haive/core/engine/base/base/Engine   /api_clean/haive/core/engine/base/base/InvokableEngine   /api_clean/haive/core/engine/base/base/NonInvokableEngine

Package Contents
----------------

