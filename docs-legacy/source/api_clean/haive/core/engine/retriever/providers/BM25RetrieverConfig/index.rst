
haive.core.engine.retriever.providers.BM25RetrieverConfig
=========================================================

.. py:module:: haive.core.engine.retriever.providers.BM25RetrieverConfig

.. autoapi-nested-parse::

   BM25 Retriever implementation for the Haive framework.

   from typing import Any
   This module provides a configuration class for the BM25 (Best Matching 25) retriever,
   which uses the BM25 ranking function for text retrieval. BM25 is a probabilistic
   ranking function used by search engines to estimate the relevance of documents
   to a given search query.

   The BM25Retriever works by:
   1. Tokenizing and preprocessing documents and queries
   2. Computing BM25 scores for each document-query pair
   3. Ranking documents by their BM25 scores
   4. Returning the top-k most relevant documents

   This retriever is particularly useful when:
   - Working with text-based document collections
   - Need precise keyword matching and term frequency analysis
   - Want interpretable ranking scores
   - Building traditional information retrieval systems
   - Combining with vector search in hybrid approaches

   The implementation integrates with LangChain's BM25Retriever while providing
   a consistent Haive configuration interface.







Classes
-------

* :py:class:`BM25RetrieverConfig` - Configuration for BM25 retriever in the Haive framework.
.. toctree::
   :hidden:
   :maxdepth: 1

   /api_clean/haive/core/engine/retriever/providers/BM25RetrieverConfig/BM25RetrieverConfig

Package Contents
----------------

