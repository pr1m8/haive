
haive.core.engine.retriever.providers.WeaviateHybridSearchRetrieverConfig
=========================================================================

.. py:module:: haive.core.engine.retriever.providers.WeaviateHybridSearchRetrieverConfig

.. autoapi-nested-parse::

   from typing import Any
   Weaviate Hybrid Search Retriever implementation for the Haive framework.

   This module provides a configuration class for the Weaviate Hybrid Search retriever,
   which combines vector similarity search with keyword search using Weaviate's
   hybrid search capabilities. Weaviate is an open-source vector database that
   supports both vector and keyword search in a single query.

   The WeaviateHybridSearchRetriever works by:
   1. Connecting to a Weaviate instance
   2. Performing both vector and keyword search simultaneously
   3. Combining results using Weaviate's hybrid ranking algorithm
   4. Supporting advanced filtering and where clauses

   This retriever is particularly useful when:
   - Need both semantic and keyword search
   - Want optimized hybrid search performance
   - Building applications with diverse query types
   - Using Weaviate as the vector database
   - Need flexible filtering capabilities

   The implementation integrates with LangChain's WeaviateHybridSearchRetriever while
   providing a consistent Haive configuration interface with secure API key management.







Classes
-------

* :py:class:`WeaviateHybridSearchRetrieverConfig` - Configuration for Weaviate Hybrid Search retriever in the Haive framework.
.. toctree::
   :hidden:
   :maxdepth: 1

   /api_clean/haive/core/engine/retriever/providers/WeaviateHybridSearchRetrieverConfig/WeaviateHybridSearchRetrieverConfig

Package Contents
----------------

