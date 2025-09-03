
haive.core.engine.retriever.providers.MergerRetrieverConfig
===========================================================

.. py:module:: haive.core.engine.retriever.providers.MergerRetrieverConfig

.. autoapi-nested-parse::

   Merger Retriever implementation for the Haive framework.

   from typing import Any
   This module provides a configuration class for the Merger retriever,
   which combines and merges results from multiple retrievers to provide
   comprehensive and deduplicated search results.

   The MergerRetriever works by:
   1. Running multiple retrievers in parallel on the same query
   2. Collecting all results from different retrieval strategies
   3. Merging and deduplicating results based on content or metadata
   4. Applying optional ranking and filtering to the merged results

   This retriever is particularly useful when:
   - Need to combine results from different retrieval approaches
   - Want comprehensive coverage across multiple data sources
   - Building systems that need to deduplicate overlapping results
   - Implementing federated search across different backends

   The implementation integrates with LangChain's MergerRetriever while
   providing a consistent Haive configuration interface with flexible merging options.







Classes
-------

* :py:class:`MergerRetrieverConfig` - Configuration for Merger retriever in the Haive framework.
.. toctree::
   :hidden:
   :maxdepth: 1

   /api_clean/haive/core/engine/retriever/providers/MergerRetrieverConfig/MergerRetrieverConfig

Package Contents
----------------

