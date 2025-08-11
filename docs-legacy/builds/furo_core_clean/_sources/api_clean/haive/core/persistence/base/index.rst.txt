
haive.core.persistence.base
===========================

.. py:module:: haive.core.persistence.base

.. autoapi-nested-parse::

   Base classes and interfaces for the Haive persistence system.

   This module defines the core abstractions and interfaces for the persistence
   system used throughout the Haive framework. It provides the foundation for
   various persistence implementations, ensuring a consistent interface regardless
   of the underlying storage technology.

   The central component is the CheckpointerConfig abstract base class, which
   defines the configuration interface that all persistence providers must implement.
   This allows different storage backends to be used interchangeably while providing
   a unified API for state persistence.







Classes
-------

* :py:class:`CheckpointerConfig` - Base configuration for checkpoint persistence implementations.
.. toctree::
   :hidden:
   :maxdepth: 1

   /api_clean/haive/core/persistence/base/CheckpointerConfig

Package Contents
----------------

