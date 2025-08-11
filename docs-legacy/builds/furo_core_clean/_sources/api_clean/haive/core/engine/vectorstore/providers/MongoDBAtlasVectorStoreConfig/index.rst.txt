
haive.core.engine.vectorstore.providers.MongoDBAtlasVectorStoreConfig
=====================================================================

.. py:module:: haive.core.engine.vectorstore.providers.MongoDBAtlasVectorStoreConfig

.. autoapi-nested-parse::

   MongoDB Atlas Vector Store implementation for the Haive framework.

   This module provides a configuration class for the MongoDB Atlas vector store,
   which combines document database capabilities with vector search functionality.

   MongoDB Atlas Vector Search provides:
   1. Unified database for documents and vectors
   2. Rich query capabilities combining vector and metadata
   3. ACID transactions and consistency guarantees
   4. Global clusters with automatic failover
   5. Built-in full-text search alongside vector search
   6. Flexible document model with nested structures

   This vector store is particularly useful when:
   - You need both document storage and vector search
   - Want to leverage existing MongoDB infrastructure
   - Require complex queries combining vectors and metadata
   - Need ACID transactions for your vector data
   - Building applications with rich document structures

   The implementation integrates with LangChain's MongoDB Atlas while providing
   a consistent Haive configuration interface.







Classes
-------

* :py:class:`MongoDBAtlasVectorStoreConfig` - Configuration for MongoDB Atlas vector store in the Haive framework.
.. toctree::
   :hidden:
   :maxdepth: 1

   /api_clean/haive/core/engine/vectorstore/providers/MongoDBAtlasVectorStoreConfig/MongoDBAtlasVectorStoreConfig

Package Contents
----------------

