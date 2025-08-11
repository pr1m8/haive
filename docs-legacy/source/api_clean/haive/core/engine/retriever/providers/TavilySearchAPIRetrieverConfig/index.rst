
haive.core.engine.retriever.providers.TavilySearchAPIRetrieverConfig
====================================================================

.. py:module:: haive.core.engine.retriever.providers.TavilySearchAPIRetrieverConfig

.. autoapi-nested-parse::

   Tavily Search API Retriever implementation for the Haive framework.

   from typing import Any
   This module provides a configuration class for the Tavily Search API retriever, which
   retrieves web search results using the Tavily search API service.

   The TavilySearchAPIRetriever works by:
   1. Taking a search query
   2. Sending it to the Tavily Search API
   3. Returning web search results as documents

   This retriever is particularly useful when:
   - Need access to current web information
   - Building applications that require real-time search
   - Combining web search with other retrieval methods
   - Providing up-to-date information beyond training data

   The implementation integrates with LangChain's TavilySearchAPIRetriever while providing
   a consistent Haive configuration interface with secure API key management.







Classes
-------

* :py:class:`TavilySearchAPIRetrieverConfig` - Configuration for Tavily Search API retriever in the Haive framework.
.. toctree::
   :hidden:
   :maxdepth: 1

   /api_clean/haive/core/engine/retriever/providers/TavilySearchAPIRetrieverConfig/TavilySearchAPIRetrieverConfig

Package Contents
----------------

