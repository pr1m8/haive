
haive.core.engine.retriever.providers.PineconeHybridSearchRetrieverConfig
=========================================================================

.. py:module:: haive.core.engine.retriever.providers.PineconeHybridSearchRetrieverConfig

.. autoapi-nested-parse::

   from typing import Any
   Pinecone Hybrid Search Retriever implementation for the Haive framework.

   This module provides a configuration class for the Pinecone Hybrid Search retriever,
   which combines vector similarity search with keyword search using Pinecone's
   hybrid search capabilities.

   The PineconeHybridSearchRetriever works by:
   1. Connecting to a Pinecone index
   2. Performing both vector and keyword search
   3. Combining results using Pinecone's hybrid scoring

   This retriever is particularly useful when:
   - Using Pinecone as the vector database
   - Need both semantic and keyword search
   - Want Pinecone's optimized hybrid search performance
   - Building applications that benefit from combined search approaches

   The implementation integrates with LangChain's PineconeHybridSearchRetriever while
   providing a consistent Haive configuration interface with secure API key management.







Classes
-------

* :py:class:`PineconeHybridSearchRetrieverConfig` - Configuration for Pinecone Hybrid Search retriever in the Haive framework.
.. toctree::
   :hidden:
   :maxdepth: 1

   /api_clean/haive/core/engine/retriever/providers/PineconeHybridSearchRetrieverConfig/PineconeHybridSearchRetrieverConfig

Package Contents
----------------

