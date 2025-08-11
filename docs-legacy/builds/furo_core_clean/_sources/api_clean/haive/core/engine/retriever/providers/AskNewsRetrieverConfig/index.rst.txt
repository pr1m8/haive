
haive.core.engine.retriever.providers.AskNewsRetrieverConfig
============================================================

.. py:module:: haive.core.engine.retriever.providers.AskNewsRetrieverConfig

.. autoapi-nested-parse::

   AskNews Retriever implementation for the Haive framework.

   from typing import Any
   This module provides a configuration class for the AskNews retriever,
   which retrieves news articles and current events using AskNews API.
   AskNews provides access to real-time news content from various sources
   with filtering and categorization capabilities.

   The AskNewsRetriever works by:
   1. Connecting to the AskNews API
   2. Executing news search queries with filters
   3. Retrieving relevant news articles and metadata
   4. Returning formatted documents with news content

   This retriever is particularly useful when:
   - Building news aggregation applications
   - Need real-time current events information
   - Creating content monitoring systems
   - Building fact-checking or research tools
   - Want categorized and filtered news content

   The implementation integrates with LangChain's AskNewsRetriever while
   providing a consistent Haive configuration interface with secure API key management.







Classes
-------

* :py:class:`AskNewsRetrieverConfig` - Configuration for AskNews retriever in the Haive framework.
.. toctree::
   :hidden:
   :maxdepth: 1

   /api_clean/haive/core/engine/retriever/providers/AskNewsRetrieverConfig/AskNewsRetrieverConfig

Package Contents
----------------

