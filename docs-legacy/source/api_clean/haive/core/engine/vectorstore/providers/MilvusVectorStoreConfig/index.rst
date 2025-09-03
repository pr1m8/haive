
haive.core.engine.vectorstore.providers.MilvusVectorStoreConfig
===============================================================

.. py:module:: haive.core.engine.vectorstore.providers.MilvusVectorStoreConfig

.. autoapi-nested-parse::

   Milvus Vector Store implementation for the Haive framework.

   This module provides a configuration class for the Milvus vector store,
   which is a cloud-native vector database built for scalable similarity search.

   Milvus provides:
   1. Billion-scale vector similarity search
   2. Hybrid search with attribute filtering
   3. Multiple index types for different scenarios
   4. Distributed architecture with high availability
   5. GPU acceleration support
   6. Time Travel for data versioning

   This vector store is particularly useful when:
   - You need to handle billion-scale vector datasets
   - Require high availability and horizontal scaling
   - Need hybrid search with metadata filtering
   - Want GPU acceleration for indexing and search
   - Building large-scale recommendation or search systems

   The implementation integrates with LangChain's Milvus while providing
   a consistent Haive configuration interface.







Classes
-------

* :py:class:`MilvusVectorStoreConfig` - Configuration for Milvus vector store in the Haive framework.
.. toctree::
   :hidden:
   :maxdepth: 1

   /api_clean/haive/core/engine/vectorstore/providers/MilvusVectorStoreConfig/MilvusVectorStoreConfig

Package Contents
----------------

