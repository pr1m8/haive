
haive.core.engine.retriever.providers.RePhraseQueryRetrieverConfig
==================================================================

.. py:module:: haive.core.engine.retriever.providers.RePhraseQueryRetrieverConfig

.. autoapi-nested-parse::

   Rephrase Query Retriever implementation for the Haive framework.

   from typing import Any
   This module provides a configuration class for the Rephrase Query retriever,
   which reformulates user queries using an LLM to improve retrieval performance
   by creating more effective search queries.

   The RePhraseQueryRetriever works by:
   1. Taking the user's original query as input
   2. Using an LLM to rephrase the query for better search effectiveness
   3. Running the rephrased query against the base retriever
   4. Returning documents found using the improved query

   This retriever is particularly useful when:
   - User queries are poorly formulated or ambiguous
   - Need to improve search effectiveness through query optimization
   - Building systems that need to handle natural language queries better
   - Want to bridge the gap between user intent and retrieval effectiveness

   The implementation integrates with LangChain's RePhraseQueryRetriever while
   providing a consistent Haive configuration interface with LLM integration.







Classes
-------

* :py:class:`RePhraseQueryRetrieverConfig` - Configuration for Rephrase Query retriever in the Haive framework.
.. toctree::
   :hidden:
   :maxdepth: 1

   /api_clean/haive/core/engine/retriever/providers/RePhraseQueryRetrieverConfig/RePhraseQueryRetrieverConfig

Package Contents
----------------

