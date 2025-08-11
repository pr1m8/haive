
haive.core.engine.retriever.providers.QdrantSparseVectorRetrieverConfig
=======================================================================

.. py:module:: haive.core.engine.retriever.providers.QdrantSparseVectorRetrieverConfig

.. autoapi-nested-parse::

   Qdrant Sparse Vector Retriever implementation for the Haive framework.

   from typing import Any
   This module provides a configuration class for the Qdrant Sparse Vector retriever,
   which uses Qdrant's sparse vector capabilities for keyword-based and hybrid search.
   Qdrant supports both dense and sparse vectors, enabling efficient text search
   using sparse embeddings like BM25 or TF-IDF representations.

   The QdrantSparseVectorRetriever works by:
   1. Connecting to a Qdrant instance
   2. Using sparse vector representations for text search
   3. Supporting efficient keyword matching and retrieval
   4. Enabling hybrid dense + sparse vector search

   This retriever is particularly useful when:
   - Need efficient keyword-based search with Qdrant
   - Want to combine dense and sparse vector search
   - Building hybrid retrieval systems
   - Using Qdrant for production vector search
   - Need high-performance text matching

   The implementation integrates with LangChain's QdrantSparseVectorRetriever while
   providing a consistent Haive configuration interface with secure API key management.







Classes
-------

* :py:class:`QdrantSparseVectorRetrieverConfig` - Configuration for Qdrant Sparse Vector retriever in the Haive framework.
.. toctree::
   :hidden:
   :maxdepth: 1

   /api_clean/haive/core/engine/retriever/providers/QdrantSparseVectorRetrieverConfig/QdrantSparseVectorRetrieverConfig

Package Contents
----------------

