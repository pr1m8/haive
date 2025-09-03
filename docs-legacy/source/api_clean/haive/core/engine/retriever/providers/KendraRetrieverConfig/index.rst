
haive.core.engine.retriever.providers.KendraRetrieverConfig
===========================================================

.. py:module:: haive.core.engine.retriever.providers.KendraRetrieverConfig

.. autoapi-nested-parse::

   Amazon Kendra Retriever implementation for the Haive framework.

   from typing import Any
   This module provides a configuration class for the Amazon Kendra retriever,
   which uses AWS Kendra's intelligent enterprise search service. Kendra provides
   ML-powered search capabilities with natural language understanding and
   enterprise document processing.

   The KendraRetriever works by:
   1. Connecting to an Amazon Kendra index
   2. Executing natural language queries
   3. Using ML to understand intent and context
   4. Returning ranked results with confidence scores

   This retriever is particularly useful when:
   - Building enterprise search applications
   - Need ML-powered query understanding
   - Working with diverse document types (PDFs, Word, etc.)
   - Want confidence scoring and result ranking
   - Building knowledge management systems

   The implementation integrates with LangChain's AmazonKendraRetriever while
   providing a consistent Haive configuration interface with secure AWS credential management.







Classes
-------

* :py:class:`KendraRetrieverConfig` - Configuration for Amazon Kendra retriever in the Haive framework.
.. toctree::
   :hidden:
   :maxdepth: 1

   /api_clean/haive/core/engine/retriever/providers/KendraRetrieverConfig/KendraRetrieverConfig

Package Contents
----------------

