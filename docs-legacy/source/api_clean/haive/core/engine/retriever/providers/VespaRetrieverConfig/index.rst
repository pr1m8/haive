
haive.core.engine.retriever.providers.VespaRetrieverConfig
==========================================================

.. py:module:: haive.core.engine.retriever.providers.VespaRetrieverConfig

.. autoapi-nested-parse::

   Vespa Retriever implementation for the Haive framework.

   from typing import Any
   This module provides a configuration class for the Vespa retriever,
   which uses Vespa search engine for advanced search and retrieval capabilities.
   Vespa is a fully featured search engine and vector database which supports
   vector search, lexical search, and hybrid ranking in a single query.

   The VespaRetriever works by:
   1. Connecting to a Vespa application
   2. Supporting both vector and text search simultaneously
   3. Providing advanced ranking and filtering capabilities
   4. Enabling real-time search and content updates

   This retriever is particularly useful when:
   - Need hybrid search combining vector and text search
   - Require real-time search with continuous updates
   - Want advanced ranking and relevance tuning
   - Building large-scale search applications
   - Need both structured and unstructured data search

   The implementation integrates with LangChain's Vespa retriever while
   providing a consistent Haive configuration interface.







Classes
-------

* :py:class:`VespaRetrieverConfig` - Configuration for Vespa retriever in the Haive framework.
.. toctree::
   :hidden:
   :maxdepth: 1

   /api_clean/haive/core/engine/retriever/providers/VespaRetrieverConfig/VespaRetrieverConfig

Package Contents
----------------

