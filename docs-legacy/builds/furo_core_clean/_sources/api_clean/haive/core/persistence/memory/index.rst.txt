
haive.core.persistence.memory
=============================

.. py:module:: haive.core.persistence.memory

.. autoapi-nested-parse::

   In-memory persistence implementation for the Haive framework.

   This module provides an in-memory checkpointer implementation that stores state
   data temporarily in memory. It's primarily intended for development, testing,
   and demonstration purposes where persistence across application restarts is
   not required.

   The memory checkpointer is the simplest implementation, requiring no external
   dependencies or infrastructure. It supports both synchronous and asynchronous
   operation modes, making it suitable for a wide range of use cases where
   temporary state management is sufficient.







Classes
-------

* :py:class:`MemoryCheckpointerConfig` - Configuration for in-memory checkpoint persistence.
.. toctree::
   :hidden:
   :maxdepth: 1

   /api_clean/haive/core/persistence/memory/MemoryCheckpointerConfig

Package Contents
----------------

