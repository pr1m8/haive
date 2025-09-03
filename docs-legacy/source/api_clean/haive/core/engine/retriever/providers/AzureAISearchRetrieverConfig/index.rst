
haive.core.engine.retriever.providers.AzureAISearchRetrieverConfig
==================================================================

.. py:module:: haive.core.engine.retriever.providers.AzureAISearchRetrieverConfig

.. autoapi-nested-parse::

   Azure AI Search Retriever implementation for the Haive framework.

   from typing import Any
   This module provides a configuration class for the Azure AI Search (formerly Azure Cognitive Search)
   retriever, which retrieves documents from Azure's cloud search service.

   The AzureAISearchRetriever works by:
   1. Connecting to an Azure AI Search service
   2. Executing search queries against indexed documents
   3. Returning ranked search results as documents

   This retriever is particularly useful when:
   - Using Azure cloud infrastructure
   - Need enterprise-grade search capabilities
   - Working with large document collections in Azure
   - Combining with other Azure AI services

   The implementation integrates with LangChain's AzureAISearchRetriever while providing
   a consistent Haive configuration interface with secure credential management.







Classes
-------

* :py:class:`AzureAISearchRetrieverConfig` - Configuration for Azure AI Search retriever in the Haive framework.
.. toctree::
   :hidden:
   :maxdepth: 1

   /api_clean/haive/core/engine/retriever/providers/AzureAISearchRetrieverConfig/AzureAISearchRetrieverConfig

Package Contents
----------------

