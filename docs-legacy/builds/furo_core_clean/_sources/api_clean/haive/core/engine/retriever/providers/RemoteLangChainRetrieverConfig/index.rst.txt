
haive.core.engine.retriever.providers.RemoteLangChainRetrieverConfig
====================================================================

.. py:module:: haive.core.engine.retriever.providers.RemoteLangChainRetrieverConfig

.. autoapi-nested-parse::

   Remote LangChain Retriever implementation for the Haive framework.

   This module provides a configuration class for the Remote LangChain retriever,
   which enables retrieval from remote LangChain services and endpoints,
   allowing distributed and federated retrieval architectures.

   The RemoteLangChainRetriever works by:
   1. Connecting to remote LangChain retrieval endpoints
   2. Sending queries to distributed retrieval services
   3. Receiving and processing results from remote systems
   4. Providing unified access to distributed retrieval infrastructure

   This retriever is particularly useful when:
   - Building distributed retrieval architectures
   - Need to access remote LangChain services
   - Implementing federated search across multiple systems
   - Building microservice-based retrieval infrastructures

   The implementation integrates with LangChain Community's RemoteLangChainRetriever while
   providing a consistent Haive configuration interface with secure endpoint management.







Classes
-------

* :py:class:`RemoteLangChainRetrieverConfig` - Configuration for Remote LangChain retriever in the Haive framework.
.. toctree::
   :hidden:
   :maxdepth: 1

   /api_clean/haive/core/engine/retriever/providers/RemoteLangChainRetrieverConfig/RemoteLangChainRetrieverConfig

Package Contents
----------------

