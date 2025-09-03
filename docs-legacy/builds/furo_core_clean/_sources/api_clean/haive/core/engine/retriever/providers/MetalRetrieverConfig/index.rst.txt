
haive.core.engine.retriever.providers.MetalRetrieverConfig
==========================================================

.. py:module:: haive.core.engine.retriever.providers.MetalRetrieverConfig

.. autoapi-nested-parse::

   Metal Retriever implementation for the Haive framework.

   from typing import Any
   This module provides a configuration class for the Metal retriever,
   which uses Metal's vector search infrastructure for high-performance
   similarity search. Metal provides a managed vector database service
   optimized for production use cases.

   The MetalRetriever works by:
   1. Connecting to a Metal index
   2. Performing vector similarity search
   3. Supporting metadata filtering and search
   4. Providing production-ready vector infrastructure

   This retriever is particularly useful when:
   - Need managed vector search infrastructure
   - Building production vector search applications
   - Want optimized performance and scaling
   - Need reliable vector database service
   - Building recommendation or search systems

   The implementation integrates with LangChain's MetalRetriever while
   providing a consistent Haive configuration interface with secure API key management.







Classes
-------

* :py:class:`MetalRetrieverConfig` - Configuration for Metal retriever in the Haive framework.
.. toctree::
   :hidden:
   :maxdepth: 1

   /api_clean/haive/core/engine/retriever/providers/MetalRetrieverConfig/MetalRetrieverConfig

Package Contents
----------------

