
haive.core.engine.retriever.providers.ElasticsearchRetrieverConfig
==================================================================

.. py:module:: haive.core.engine.retriever.providers.ElasticsearchRetrieverConfig

.. autoapi-nested-parse::

   Elasticsearch Retriever implementation for the Haive framework.

   from typing import Any
   This module provides a configuration class for the Elasticsearch retriever,
   which performs full-text search and retrieval using Elasticsearch. Elasticsearch
   is a distributed, RESTful search and analytics engine capable of solving complex
   search problems and providing real-time search capabilities.

   The ElasticsearchRetriever works by:
   1. Connecting to an Elasticsearch cluster
   2. Executing search queries with various scoring methods
   3. Supporting both keyword and vector-based search
   4. Returning ranked search results as documents

   This retriever is particularly useful when:
   - Working with large-scale document collections
   - Need advanced search capabilities (faceting, aggregations, etc.)
   - Require real-time search and indexing
   - Building enterprise search applications
   - Need scalable and distributed search infrastructure

   The implementation integrates with LangChain's ElasticsearchRetriever while
   providing a consistent Haive configuration interface with secure connection management.







Classes
-------

* :py:class:`ElasticsearchRetrieverConfig` - Configuration for Elasticsearch retriever in the Haive framework.
.. toctree::
   :hidden:
   :maxdepth: 1

   /api_clean/haive/core/engine/retriever/providers/ElasticsearchRetrieverConfig/ElasticsearchRetrieverConfig

Package Contents
----------------

