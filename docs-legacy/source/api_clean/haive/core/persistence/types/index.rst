
haive.core.persistence.types
============================

.. py:module:: haive.core.persistence.types

.. autoapi-nested-parse::

   Type definitions for the Haive persistence system.

   This module provides enumeration types and utility classes for the persistence
   system, defining the available checkpointer types, operational modes, and
   storage strategies. These types are used throughout the persistence system
   for configuration and operation.

   The module includes special handling for Python keyword conflicts (like 'async')
   and backward compatibility mappings for evolving terminology.







Classes
-------

* :py:class:`CheckpointerType` - Types of checkpointer implementations available in the system.* :py:class:`CheckpointerMode` - Operational modes for checkpointers.* :py:class:`CheckpointStorageMode` - Storage strategies for checkpointers.* :py:class:`ConnectionOptions` - Common connection options and utilities for database-backed checkpointers.
.. toctree::
   :hidden:
   :maxdepth: 1

   /api_clean/haive/core/persistence/types/CheckpointerType   /api_clean/haive/core/persistence/types/CheckpointerMode   /api_clean/haive/core/persistence/types/CheckpointStorageMode   /api_clean/haive/core/persistence/types/ConnectionOptions

Package Contents
----------------

