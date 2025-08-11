
haive.core.engine.vectorstore.providers.RedisVectorStoreConfig
==============================================================

.. py:module:: haive.core.engine.vectorstore.providers.RedisVectorStoreConfig

.. autoapi-nested-parse::

   Redis Vector Store implementation for the Haive framework.

   This module provides a configuration class for the Redis vector store,
   which combines in-memory caching with vector similarity search capabilities.

   Redis provides:
   1. Ultra-fast in-memory vector operations
   2. Real-time vector search with sub-millisecond latency
   3. Hybrid data structures (vectors + traditional Redis types)
   4. Distributed caching and session storage
   5. Pub/Sub for real-time vector updates
   6. Enterprise clustering and persistence

   This vector store is particularly useful when:
   - You need extremely low-latency vector search
   - Want to cache vector embeddings for performance
   - Building real-time recommendation systems
   - Need to combine vectors with session data
   - Require high-throughput vector operations

   The implementation integrates with LangChain's Redis while providing
   a consistent Haive configuration interface.







Classes
-------

* :py:class:`RedisVectorStoreConfig` - Configuration for Redis vector store in the Haive framework.
.. toctree::
   :hidden:
   :maxdepth: 1

   /api_clean/haive/core/engine/vectorstore/providers/RedisVectorStoreConfig/RedisVectorStoreConfig

Package Contents
----------------

