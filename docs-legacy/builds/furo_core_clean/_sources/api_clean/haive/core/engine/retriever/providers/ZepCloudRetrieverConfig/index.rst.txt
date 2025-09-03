
haive.core.engine.retriever.providers.ZepCloudRetrieverConfig
=============================================================

.. py:module:: haive.core.engine.retriever.providers.ZepCloudRetrieverConfig

.. autoapi-nested-parse::

   Zep Cloud Retriever implementation for the Haive framework.

   from typing import Any
   This module provides a configuration class for the Zep Cloud retriever,
   which retrieves conversation history and memory from Zep's cloud-hosted
   memory service. Zep Cloud provides managed long-term memory storage
   for conversational AI applications with enhanced features and reliability.

   The ZepCloudRetriever works by:
   1. Connecting to Zep Cloud service
   2. Searching conversation history using semantic similarity
   3. Retrieving relevant chat messages and context
   4. Providing managed conversation memory

   This retriever is particularly useful when:
   - Building conversational AI with cloud-hosted memory
   - Need reliable managed memory infrastructure
   - Want enhanced Zep features and performance
   - Building scalable chatbot applications
   - Need conversation history across sessions

   The implementation integrates with LangChain's ZepCloudRetriever while
   providing a consistent Haive configuration interface with secure API key management.







Classes
-------

* :py:class:`ZepCloudRetrieverConfig` - Configuration for Zep Cloud retriever in the Haive framework.
.. toctree::
   :hidden:
   :maxdepth: 1

   /api_clean/haive/core/engine/retriever/providers/ZepCloudRetrieverConfig/ZepCloudRetrieverConfig

Package Contents
----------------

