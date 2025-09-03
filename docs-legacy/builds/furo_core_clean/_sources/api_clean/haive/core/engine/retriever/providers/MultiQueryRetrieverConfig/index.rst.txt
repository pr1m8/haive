
haive.core.engine.retriever.providers.MultiQueryRetrieverConfig
===============================================================

.. py:module:: haive.core.engine.retriever.providers.MultiQueryRetrieverConfig

.. autoapi-nested-parse::

   Multi-Query Retriever implementation for the Haive framework.

   This module provides a configuration class for the Multi-Query retriever,
   which generates multiple query variations to improve retrieval coverage
   and find more relevant documents for complex or ambiguous queries.

   The MultiQueryRetriever works by:
   1. Using an LLM to generate multiple query variations from the original query
   2. Running each generated query against the base retriever
   3. Collecting and deduplicating all retrieved documents
   4. Returning the combined set of unique documents

   This retriever is particularly useful when:
   - Dealing with complex or ambiguous user queries
   - Need to improve recall by finding documents with different phrasings
   - User queries might miss relevant documents due to vocabulary mismatch
   - Building systems that need comprehensive document coverage

   The implementation integrates with LangChain's MultiQueryRetriever while
   providing a consistent Haive configuration interface with LLM integration.







Classes
-------

* :py:class:`MultiQueryRetrieverConfig` - Configuration for Multi-Query retriever in the Haive framework.
.. toctree::
   :hidden:
   :maxdepth: 1

   /api_clean/haive/core/engine/retriever/providers/MultiQueryRetrieverConfig/MultiQueryRetrieverConfig

Package Contents
----------------

