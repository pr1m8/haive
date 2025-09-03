
haive.core.engine.retriever.providers.MultiVectorRetrieverConfig
================================================================

.. py:module:: haive.core.engine.retriever.providers.MultiVectorRetrieverConfig

.. autoapi-nested-parse::

   Multi-Vector Retriever implementation for the Haive framework.

   This module provides a configuration class for the Multi-Vector retriever,
   which stores multiple vectors per document to enable more nuanced and accurate
   retrieval by representing different aspects or summaries of each document.

   The MultiVectorRetriever works by:
   1. Storing multiple vector representations for each document (summaries, chunks, etc.)
   2. Retrieving documents based on these multiple vector representations
   3. Supporting different indexing strategies (by summary, by chunks, by hypothetical docs)
   4. Providing flexible mapping between vectors and source documents

   This retriever is particularly useful when:
   - Documents have multiple aspects that should be searchable separately
   - Need to index both summaries and full content
   - Want to improve retrieval precision with multi-faceted representations
   - Building systems that need granular document understanding

   The implementation integrates with LangChain's MultiVectorRetriever while
   providing a consistent Haive configuration interface with flexible vector storage.







Classes
-------

* :py:class:`MultiVectorRetrieverConfig` - Configuration for Multi-Vector retriever in the Haive framework.
.. toctree::
   :hidden:
   :maxdepth: 1

   /api_clean/haive/core/engine/retriever/providers/MultiVectorRetrieverConfig/MultiVectorRetrieverConfig

Package Contents
----------------

