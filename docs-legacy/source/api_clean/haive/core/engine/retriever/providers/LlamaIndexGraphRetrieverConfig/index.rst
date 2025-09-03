
haive.core.engine.retriever.providers.LlamaIndexGraphRetrieverConfig
====================================================================

.. py:module:: haive.core.engine.retriever.providers.LlamaIndexGraphRetrieverConfig

.. autoapi-nested-parse::

   LlamaIndex Graph Retriever implementation for the Haive framework.

   This module provides a configuration class for the LlamaIndex Graph retriever,
   which performs graph-based retrieval using knowledge graphs and graph databases
   like Neo4j, providing semantic relationships and graph traversal capabilities.

   The LlamaIndexGraphRetriever works by:
   1. Using a graph index (knowledge graph, Neo4j, etc.) as the underlying storage
   2. Performing graph traversal queries to find related nodes and relationships
   3. Converting graph nodes and edges into retrievable documents
   4. Supporting both entity-based and relationship-based retrieval

   This retriever is particularly useful when:
   - Working with knowledge graphs and structured data
   - Need to understand relationships between entities
   - Building systems that require graph traversal and exploration
   - Integrating with Neo4j or other graph databases
   - Performing semantic retrieval over connected data

   The implementation integrates with LangChain Community's LlamaIndexGraphRetriever while
   providing a consistent Haive configuration interface with graph database support.







Classes
-------

* :py:class:`LlamaIndexGraphRetrieverConfig` - Configuration for LlamaIndex Graph retriever in the Haive framework.
.. toctree::
   :hidden:
   :maxdepth: 1

   /api_clean/haive/core/engine/retriever/providers/LlamaIndexGraphRetrieverConfig/LlamaIndexGraphRetrieverConfig

Package Contents
----------------

