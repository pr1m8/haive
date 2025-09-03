
haive.core.engine.retriever.providers.ArxivRetrieverConfig
==========================================================

.. py:module:: haive.core.engine.retriever.providers.ArxivRetrieverConfig

.. autoapi-nested-parse::

   Arxiv Retriever implementation for the Haive framework.

   from typing import Any
   This module provides a configuration class for the Arxiv retriever, which
   retrieves academic papers from the arXiv preprint repository.

   The ArxivRetriever works by:
   1. Taking a search query for academic papers
   2. Searching the arXiv API for matching papers
   3. Returning paper abstracts and metadata as documents

   This retriever is particularly useful when:
   - Working with academic or research content
   - Need access to the latest preprint papers
   - Building research-focused applications
   - Combining with other retrievers in academic contexts

   The implementation integrates with LangChain's ArxivRetriever while providing
   a consistent Haive configuration interface.







Classes
-------

* :py:class:`ArxivRetrieverConfig` - Configuration for Arxiv retriever in the Haive framework.
.. toctree::
   :hidden:
   :maxdepth: 1

   /api_clean/haive/core/engine/retriever/providers/ArxivRetrieverConfig/ArxivRetrieverConfig

Package Contents
----------------

