
haive.core.persistence.handlers
===============================

.. py:module:: haive.core.persistence.handlers

.. autoapi-nested-parse::

   High-level persistence handling utilities for the Haive framework.

   This module provides high-level functions for managing persistence operations,
   including checkpointer creation, configuration interpretation, state recovery,
   and thread management. It serves as a convenient interface layer that abstracts
   away the details of specific persistence implementations.

   The utilities in this module are designed to work with both simple configuration
   dictionaries and full CheckpointerConfig objects, automatically handling fallbacks,
   error recovery, and sensible defaults. They provide a robust interface for both
   synchronous and asynchronous usage patterns.

   Key functions:
   - setup_checkpointer: Create appropriate checkpointer based on configuration
   - get_checkpoint: Retrieve state from persistence
   - put_checkpoint: Store state in persistence
   - register_thread: Register a thread for tracking and management

   This module enables a more declarative approach to persistence configuration,
   allowing users to specify what they want rather than how to implement it.






Functions
---------

   setup_checkpointer   setup_async_checkpointer   ensure_pool_open   ensure_async_pool_open   close_async_pool_if_needed   register_async_thread_if_needed   close_pool_if_needed   close_async_pool_if_needed   register_thread_if_needed   register_async_thread_if_needed   prepare_merged_input   get_thread_id_from_config
.. autofunction:: setup_checkpointer
.. autofunction:: setup_async_checkpointer
.. autofunction:: ensure_pool_open
.. autofunction:: ensure_async_pool_open
.. autofunction:: close_async_pool_if_needed
.. autofunction:: register_async_thread_if_needed
.. autofunction:: close_pool_if_needed
.. autofunction:: close_async_pool_if_needed
.. autofunction:: register_thread_if_needed
.. autofunction:: register_async_thread_if_needed
.. autofunction:: prepare_merged_input
.. autofunction:: get_thread_id_from_config



Package Contents
----------------

