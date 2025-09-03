
haive.core.engine.retriever.providers.ZepRetrieverConfig
========================================================

.. py:module:: haive.core.engine.retriever.providers.ZepRetrieverConfig

.. autoapi-nested-parse::

   Zep Retriever implementation for the Haive framework.

   from typing import Any
   This module provides a configuration class for the Zep retriever,
   which retrieves conversation history and memory from Zep's long-term memory store.
   Zep is designed for storing, searching, and enriching conversational AI chat histories
   with metadata, summaries, and semantic search capabilities.

   The ZepRetriever works by:
   1. Connecting to a Zep memory store
   2. Searching conversation history using semantic similarity
   3. Retrieving relevant chat messages and context
   4. Providing conversation memory for AI applications

   This retriever is particularly useful when:
   - Building conversational AI applications with long-term memory
   - Need to retrieve relevant conversation history
   - Want to maintain context across multiple chat sessions
   - Building customer support or chatbot applications
   - Creating personalized AI assistants with memory

   The implementation integrates with LangChain's ZepRetriever while providing
   a consistent Haive configuration interface with secure API key management.







Classes
-------

* :py:class:`ZepRetrieverConfig` - Configuration for Zep retriever in the Haive framework.
.. toctree::
   :hidden:
   :maxdepth: 1

   /api_clean/haive/core/engine/retriever/providers/ZepRetrieverConfig/ZepRetrieverConfig

Package Contents
----------------

