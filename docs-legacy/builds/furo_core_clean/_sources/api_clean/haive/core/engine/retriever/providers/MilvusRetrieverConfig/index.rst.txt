
haive.core.engine.retriever.providers.MilvusRetrieverConfig
===========================================================

.. py:module:: haive.core.engine.retriever.providers.MilvusRetrieverConfig

.. autoapi-nested-parse::

   Milvus Retriever implementation for the Haive framework.

   from typing import Any
   This module provides a configuration class for the Milvus retriever,
   which uses Milvus vector database for high-performance similarity search.
   Milvus is an open-source vector database built for scalable similarity search
   and AI applications with support for various indexing algorithms.

   The MilvusRetriever works by:
   1. Connecting to a Milvus server instance
   2. Performing vector similarity search using various metrics
   3. Supporting advanced indexing and search parameters
   4. Providing high-performance retrieval for large-scale datasets

   This retriever is particularly useful when:
   - Working with large-scale vector datasets (millions+ vectors)
   - Need high-performance similarity search
   - Require advanced indexing capabilities (IVF, HNSW, etc.)
   - Building production vector search applications
   - Need distributed and scalable vector storage

   The implementation integrates with LangChain's Milvus retriever while
   providing a consistent Haive configuration interface.







Classes
-------

* :py:class:`MilvusRetrieverConfig` - Configuration for Milvus retriever in the Haive framework.
.. toctree::
   :hidden:
   :maxdepth: 1

   /api_clean/haive/core/engine/retriever/providers/MilvusRetrieverConfig/MilvusRetrieverConfig

Package Contents
----------------

