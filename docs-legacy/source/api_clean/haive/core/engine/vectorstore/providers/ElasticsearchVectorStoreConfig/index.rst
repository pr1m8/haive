
haive.core.engine.vectorstore.providers.ElasticsearchVectorStoreConfig
======================================================================

.. py:module:: haive.core.engine.vectorstore.providers.ElasticsearchVectorStoreConfig

.. autoapi-nested-parse::

   Elasticsearch Vector Store implementation for the Haive framework.

   This module provides a configuration class for the Elasticsearch vector store,
   which combines traditional text search with vector similarity search capabilities.

   Elasticsearch provides:
   1. Hybrid search combining BM25 and vector similarity
   2. Distributed search across multiple nodes
   3. Real-time indexing and search
   4. Rich query DSL with vector operations
   5. Aggregations and analytics on vector data
   6. Enterprise security and monitoring

   This vector store is particularly useful when:
   - You need both text search and vector similarity
   - Want to leverage existing Elasticsearch infrastructure
   - Need distributed search at scale
   - Require complex queries combining multiple search types
   - Building applications with rich search analytics

   The implementation integrates with LangChain's Elasticsearch while providing
   a consistent Haive configuration interface.







Classes
-------

* :py:class:`ElasticsearchVectorStoreConfig` - Configuration for Elasticsearch vector store in the Haive framework.
.. toctree::
   :hidden:
   :maxdepth: 1

   /api_clean/haive/core/engine/vectorstore/providers/ElasticsearchVectorStoreConfig/ElasticsearchVectorStoreConfig

Package Contents
----------------

