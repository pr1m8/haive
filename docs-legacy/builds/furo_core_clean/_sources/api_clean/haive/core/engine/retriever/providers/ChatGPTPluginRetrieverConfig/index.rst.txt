
haive.core.engine.retriever.providers.ChatGPTPluginRetrieverConfig
==================================================================

.. py:module:: haive.core.engine.retriever.providers.ChatGPTPluginRetrieverConfig

.. autoapi-nested-parse::

   ChatGPT Plugin Retriever implementation for the Haive framework.

   from typing import Any
   This module provides a configuration class for the ChatGPT Plugin retriever,
   which integrates with ChatGPT plugins to retrieve information from external
   services and APIs. This enables access to real-time data and specialized
   knowledge sources through the ChatGPT plugin ecosystem.

   The ChatGPTPluginRetriever works by:
   1. Connecting to ChatGPT plugin APIs
   2. Making requests to plugin endpoints
   3. Processing plugin responses into documents
   4. Supporting various plugin types and formats

   This retriever is particularly useful when:
   - Integrating with existing ChatGPT plugins
   - Need access to real-time external data
   - Want to leverage specialized plugin knowledge
   - Building systems that use plugin ecosystems
   - Accessing services through plugin interfaces

   The implementation integrates with LangChain's ChatGPTPluginRetriever while
   providing a consistent Haive configuration interface.







Classes
-------

* :py:class:`ChatGPTPluginRetrieverConfig` - Configuration for ChatGPT Plugin retriever in the Haive framework.
.. toctree::
   :hidden:
   :maxdepth: 1

   /api_clean/haive/core/engine/retriever/providers/ChatGPTPluginRetrieverConfig/ChatGPTPluginRetrieverConfig

Package Contents
----------------

