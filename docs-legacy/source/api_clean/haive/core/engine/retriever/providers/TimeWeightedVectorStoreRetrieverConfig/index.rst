
haive.core.engine.retriever.providers.TimeWeightedVectorStoreRetrieverConfig
============================================================================

.. py:module:: haive.core.engine.retriever.providers.TimeWeightedVectorStoreRetrieverConfig

.. autoapi-nested-parse::

   Time-Weighted Vector Store Retriever implementation for the Haive framework.

   This module provides a configuration class for the Time-Weighted Vector Store retriever,
   which combines vector similarity search with time-based scoring to prioritize recent
   documents while still considering semantic relevance.

   The TimeWeightedVectorStoreRetriever works by:
   1. Performing standard vector similarity search on document content
   2. Applying time-based decay factors to prioritize recent documents
   3. Combining similarity scores with recency scores using configurable weights
   4. Returning documents that balance relevance and recency

   This retriever is particularly useful when:
   - Building systems where document freshness matters (news, updates, etc.)
   - Need to balance between relevance and recency
   - Working with time-sensitive information retrieval
   - Building conversational systems that should prefer recent context

   The implementation integrates with LangChain's TimeWeightedVectorStoreRetriever while
   providing a consistent Haive configuration interface with flexible time weighting options.







Classes
-------

* :py:class:`TimeWeightedVectorStoreRetrieverConfig` - Configuration for Time-Weighted Vector Store retriever in the Haive framework.
.. toctree::
   :hidden:
   :maxdepth: 1

   /api_clean/haive/core/engine/retriever/providers/TimeWeightedVectorStoreRetrieverConfig/TimeWeightedVectorStoreRetrieverConfig

Package Contents
----------------

