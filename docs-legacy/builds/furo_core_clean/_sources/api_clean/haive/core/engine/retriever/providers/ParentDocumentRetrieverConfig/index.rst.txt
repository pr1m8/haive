
haive.core.engine.retriever.providers.ParentDocumentRetrieverConfig
===================================================================

.. py:module:: haive.core.engine.retriever.providers.ParentDocumentRetrieverConfig

.. autoapi-nested-parse::

   Parent Document Retriever implementation for the Haive framework.

   This module provides a configuration class for the Parent Document retriever,
   which retrieves small chunks for embedding similarity but returns larger parent
   documents containing those chunks, providing better context while maintaining
   search precision.

   The ParentDocumentRetriever works by:
   1. Splitting documents into small chunks for embedding and similarity search
   2. Storing these chunks in a vector store with references to parent documents
   3. Storing full parent documents in a separate document store
   4. When querying, finding similar chunks but returning their parent documents

   This retriever is particularly useful when:
   - Need precise similarity search on small chunks
   - Want to return full context from larger parent documents
   - Building systems that balance search precision with context completeness
   - Dealing with long documents that need chunk-level search

   The implementation integrates with LangChain's ParentDocumentRetriever while
   providing a consistent Haive configuration interface with flexible chunking options.







Classes
-------

* :py:class:`ParentDocumentRetrieverConfig` - Configuration for Parent Document retriever in the Haive framework.
.. toctree::
   :hidden:
   :maxdepth: 1

   /api_clean/haive/core/engine/retriever/providers/ParentDocumentRetrieverConfig/ParentDocumentRetrieverConfig

Package Contents
----------------

