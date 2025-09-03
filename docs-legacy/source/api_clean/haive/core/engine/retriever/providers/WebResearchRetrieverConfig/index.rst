
haive.core.engine.retriever.providers.WebResearchRetrieverConfig
================================================================

.. py:module:: haive.core.engine.retriever.providers.WebResearchRetrieverConfig

.. autoapi-nested-parse::

   from typing import Any
   Web Research Retriever implementation for the Haive framework.

   This module provides a configuration class for the Web Research retriever,
   which performs advanced web research by combining web search with document
   processing and retrieval. It searches the web, retrieves content from URLs,
   processes the content, and provides comprehensive research results.

   The WebResearchRetriever works by:
   1. Using a web search API to find relevant URLs
   2. Retrieving and processing content from those URLs
   3. Chunking and embedding the retrieved content
   4. Providing retrieval over the processed web content
   5. Combining search results with retrieved document chunks

   This retriever is particularly useful when:
   - Need up-to-date information from the web
   - Building research applications that require current data
   - Combining web search with document retrieval
   - Creating systems that need comprehensive web coverage
   - Building fact-checking or research assistant applications

   The implementation integrates with LangChain's WebResearchRetriever while
   providing a consistent Haive configuration interface with secure API key management.







Classes
-------

* :py:class:`WebResearchRetrieverConfig` - Configuration for Web Research retriever in the Haive framework.
.. toctree::
   :hidden:
   :maxdepth: 1

   /api_clean/haive/core/engine/retriever/providers/WebResearchRetrieverConfig/WebResearchRetrieverConfig

Package Contents
----------------

