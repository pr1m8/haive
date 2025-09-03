
haive.core.persistence.utils
============================

.. py:module:: haive.core.persistence.utils

.. autoapi-nested-parse::

   Utility functions for the Haive persistence system.

   This module provides helper functions for working with checkpointers and their
   associated resources. It includes utilities for connection pool management,
   serialization/deserialization of metadata, and other common operations needed
   across different persistence implementations.

   The utilities are designed to be used by the persistence system internals and
   generally aren't intended to be used directly by application code. They provide
   consistent behavior across different checkpointer implementations and handle
   edge cases and error conditions gracefully.






Functions
---------

   serialize_metadata   deserialize_metadata   ensure_pool_open   ensure_async_pool_open   register_thread   register_thread_async
.. autofunction:: serialize_metadata
.. autofunction:: deserialize_metadata
.. autofunction:: ensure_pool_open
.. autofunction:: ensure_async_pool_open
.. autofunction:: register_thread
.. autofunction:: register_thread_async



Package Contents
----------------

