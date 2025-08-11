
haive.core.engine.retriever.providers.DocArrayRetrieverConfig
=============================================================

.. py:module:: haive.core.engine.retriever.providers.DocArrayRetrieverConfig

.. autoapi-nested-parse::

   DocArray Retriever implementation for the Haive framework.

   from typing import Any
   This module provides a configuration class for the DocArray retriever,
   which uses DocArray's vector search capabilities for document retrieval.
   DocArray is a library for representing, sending, and searching multimodal
   data, providing efficient vector operations and search.

   The DocArrayRetriever works by:
   1. Using DocArray's DocumentArray for document storage
   2. Performing vector similarity search with various metrics
   3. Supporting efficient in-memory and persisted search
   4. Enabling multimodal document processing

   This retriever is particularly useful when:
   - Working with multimodal documents (text, images, etc.)
   - Need efficient in-memory vector search
   - Want lightweight vector operations
   - Building prototypes or smaller datasets
   - Using DocArray for document processing

   The implementation integrates with LangChain's DocArrayRetriever while
   providing a consistent Haive configuration interface.







Classes
-------

* :py:class:`DocArrayRetrieverConfig` - Configuration for DocArray retriever in the Haive framework.
.. toctree::
   :hidden:
   :maxdepth: 1

   /api_clean/haive/core/engine/retriever/providers/DocArrayRetrieverConfig/DocArrayRetrieverConfig

Package Contents
----------------

