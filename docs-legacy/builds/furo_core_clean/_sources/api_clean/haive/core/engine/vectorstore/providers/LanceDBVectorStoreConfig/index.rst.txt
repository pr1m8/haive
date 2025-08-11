
haive.core.engine.vectorstore.providers.LanceDBVectorStoreConfig
================================================================

.. py:module:: haive.core.engine.vectorstore.providers.LanceDBVectorStoreConfig

.. autoapi-nested-parse::

   LanceDB Vector Store implementation for the Haive framework.

   This module provides a configuration class for the LanceDB vector store,
   which is a modern, high-performance vector database built on Lance format.

   LanceDB provides:
   1. Columnar storage format optimized for vector search
   2. ACID transactions and versioning
   3. Efficient disk-based storage with memory mapping
   4. Hybrid search combining vector and full-text search
   5. Automatic indexing and query optimization
   6. Multi-modal data support (vectors, text, images)

   This vector store is particularly useful when:
   - You need high-performance vector search at scale
   - Want persistent storage with ACID guarantees
   - Need to handle large datasets that don't fit in memory
   - Building applications requiring hybrid search capabilities
   - Want modern columnar storage with versioning support

   The implementation integrates with LangChain's LanceDB while providing
   a consistent Haive configuration interface.







Classes
-------

* :py:class:`LanceDBVectorStoreConfig` - Configuration for LanceDB vector store in the Haive framework.
.. toctree::
   :hidden:
   :maxdepth: 1

   /api_clean/haive/core/engine/vectorstore/providers/LanceDBVectorStoreConfig/LanceDBVectorStoreConfig

Package Contents
----------------

