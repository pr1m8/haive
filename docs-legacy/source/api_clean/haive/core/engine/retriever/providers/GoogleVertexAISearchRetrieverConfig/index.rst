
haive.core.engine.retriever.providers.GoogleVertexAISearchRetrieverConfig
=========================================================================

.. py:module:: haive.core.engine.retriever.providers.GoogleVertexAISearchRetrieverConfig

.. autoapi-nested-parse::

   Google Vertex AI Search Retriever implementation for the Haive framework.

   from typing import Any
   This module provides a configuration class for the Google Vertex AI Search retriever,
   which uses Google Cloud's Vertex AI Search (formerly Enterprise Search) service.
   Vertex AI Search provides ML-powered search capabilities with natural language
   understanding and enterprise-grade security and compliance.

   The GoogleVertexAISearchRetriever works by:
   1. Connecting to a Vertex AI Search data store
   2. Executing search queries with ML understanding
   3. Returning ranked results with relevance scoring
   4. Supporting various data source types and formats

   This retriever is particularly useful when:
   - Building enterprise search on Google Cloud
   - Need ML-powered query understanding
   - Working with Google Cloud data sources
   - Want enterprise security and compliance
   - Building knowledge management systems

   The implementation integrates with LangChain's GoogleVertexAISearchRetriever while
   providing a consistent Haive configuration interface with secure GCP credential management.







Classes
-------

* :py:class:`GoogleVertexAISearchRetrieverConfig` - Configuration for Google Vertex AI Search retriever in the Haive framework.
.. toctree::
   :hidden:
   :maxdepth: 1

   /api_clean/haive/core/engine/retriever/providers/GoogleVertexAISearchRetrieverConfig/GoogleVertexAISearchRetrieverConfig

Package Contents
----------------

