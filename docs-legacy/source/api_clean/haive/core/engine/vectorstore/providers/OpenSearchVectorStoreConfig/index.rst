
haive.core.engine.vectorstore.providers.OpenSearchVectorStoreConfig
===================================================================

.. py:module:: haive.core.engine.vectorstore.providers.OpenSearchVectorStoreConfig

.. autoapi-nested-parse::

   OpenSearch Vector Store implementation for the Haive framework.

   This module provides a configuration class for the OpenSearch vector store,
   which provides scalable vector search capabilities with Amazon OpenSearch.

   OpenSearch provides:
   1. Scalable vector search with approximate nearest neighbor (ANN) algorithms
   2. Multiple engine support (nmslib, faiss, lucene)
   3. Hybrid search combining keyword and vector search
   4. AOSS (Amazon OpenSearch Service Serverless) support
   5. Advanced filtering and metadata search
   6. Both synchronous and asynchronous operations

   This vector store is particularly useful when:
   - You need scalable vector search with enterprise features
   - Want hybrid search capabilities (keyword + vector)
   - Building applications with OpenSearch/Elasticsearch expertise
   - Need integration with AWS OpenSearch Service
   - Require advanced filtering and search features

   The implementation integrates with LangChain's OpenSearch while providing
   a consistent Haive configuration interface.







Classes
-------

* :py:class:`OpenSearchVectorStoreConfig` - Configuration for OpenSearch vector store in the Haive framework.
.. toctree::
   :hidden:
   :maxdepth: 1

   /api_clean/haive/core/engine/vectorstore/providers/OpenSearchVectorStoreConfig/OpenSearchVectorStoreConfig

Package Contents
----------------

