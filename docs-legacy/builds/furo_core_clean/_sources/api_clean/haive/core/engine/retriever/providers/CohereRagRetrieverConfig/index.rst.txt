
haive.core.engine.retriever.providers.CohereRagRetrieverConfig
==============================================================

.. py:module:: haive.core.engine.retriever.providers.CohereRagRetrieverConfig

.. autoapi-nested-parse::

   Cohere RAG Retriever implementation for the Haive framework.

   from typing import Any
   This module provides a configuration class for the Cohere RAG retriever,
   which uses Cohere's Retrieval-Augmented Generation API for document retrieval
   and generation. Cohere RAG provides enterprise-grade retrieval with built-in
   re-ranking, citation capabilities, and optimized retrieval performance.

   The CohereRagRetriever works by:
   1. Using Cohere's RAG API for retrieval and generation
   2. Automatically re-ranking results for relevance
   3. Providing citations and source attribution
   4. Supporting various document sources and connectors

   This retriever is particularly useful when:
   - Need enterprise-grade RAG capabilities
   - Want built-in re-ranking and citation features
   - Building production RAG applications
   - Need reliable and optimized retrieval performance
   - Working with large document collections

   The implementation integrates with LangChain's CohereRagRetriever while
   providing a consistent Haive configuration interface with secure API key management.







Classes
-------

* :py:class:`CohereRagRetrieverConfig` - Configuration for Cohere RAG retriever in the Haive framework.
.. toctree::
   :hidden:
   :maxdepth: 1

   /api_clean/haive/core/engine/retriever/providers/CohereRagRetrieverConfig/CohereRagRetrieverConfig

Package Contents
----------------

