
haive.core.engine.retriever.providers.EnsembleRetrieverConfig
=============================================================

.. py:module:: haive.core.engine.retriever.providers.EnsembleRetrieverConfig

.. autoapi-nested-parse::

   Ensemble Retriever implementation for the Haive framework.

   This module provides a configuration class for the Ensemble retriever,
   which combines multiple retrieval strategies using weighted combination
   to improve overall retrieval performance and coverage.

   The EnsembleRetriever works by:
   1. Running multiple retrievers in parallel on the same query
   2. Combining results using configurable weights for each retriever
   3. Re-ranking and deduplicating the combined results
   4. Returning the most relevant documents from the ensemble

   This retriever is particularly useful when:
   - You want to combine different retrieval strategies (sparse + dense)
   - Need to balance precision and recall across different approaches
   - Building robust systems that work across diverse query types
   - Implementing hybrid search with customizable weights

   The implementation integrates with LangChain's EnsembleRetriever while
   providing a consistent Haive configuration interface.







Classes
-------

* :py:class:`EnsembleRetrieverConfig` - Configuration for Ensemble retriever in the Haive framework.
.. toctree::
   :hidden:
   :maxdepth: 1

   /api_clean/haive/core/engine/retriever/providers/EnsembleRetrieverConfig/EnsembleRetrieverConfig

Package Contents
----------------

