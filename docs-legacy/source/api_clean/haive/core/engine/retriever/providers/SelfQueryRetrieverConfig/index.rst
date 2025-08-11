
haive.core.engine.retriever.providers.SelfQueryRetrieverConfig
==============================================================

.. py:module:: haive.core.engine.retriever.providers.SelfQueryRetrieverConfig

.. autoapi-nested-parse::

   Self-Query Retriever implementation for the Haive framework.

   This module provides a configuration class for the Self-Query retriever,
   which enables natural language queries to be converted into structured queries
   that can filter on document metadata and perform semantic similarity search.

   The SelfQueryRetriever works by:
   1. Using an LLM to parse natural language queries into structured components
   2. Extracting filter conditions for metadata (date, category, etc.)
   3. Extracting the semantic search query component
   4. Performing both metadata filtering and vector similarity search
   5. Returning documents that match both criteria

   This retriever is particularly useful when:
   - Documents have rich metadata that should be queryable
   - Need to combine semantic search with structured filtering
   - Users want to query both content and attributes naturally
   - Building systems that need precise control over search scope

   The implementation integrates with LangChain's SelfQueryRetriever while
   providing a consistent Haive configuration interface with metadata schema support.







Classes
-------

* :py:class:`SelfQueryRetrieverConfig` - Configuration for Self-Query retriever in the Haive framework.
.. toctree::
   :hidden:
   :maxdepth: 1

   /api_clean/haive/core/engine/retriever/providers/SelfQueryRetrieverConfig/SelfQueryRetrieverConfig

Package Contents
----------------

