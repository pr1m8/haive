
haive.core.engine.retriever.providers.ContextualCompressionRetrieverConfig
==========================================================================

.. py:module:: haive.core.engine.retriever.providers.ContextualCompressionRetrieverConfig

.. autoapi-nested-parse::

   Contextual Compression Retriever implementation for the Haive framework.

   This module provides a configuration class for the Contextual Compression retriever,
   which compresses retrieved documents to extract only the most relevant information
   relative to the query, improving both relevance and efficiency.

   The ContextualCompressionRetriever works by:
   1. Using a base retriever to get initial document candidates
   2. Applying a compressor (LLM or extractive) to compress each document
   3. Extracting only the parts of documents that are relevant to the query
   4. Returning compressed, more focused document content

   This retriever is particularly useful when:
   - Documents are long and contain irrelevant sections
   - Need to reduce token usage in downstream processing
   - Want to improve precision by filtering out noise
   - Building systems with strict context length limits

   The implementation integrates with LangChain's ContextualCompressionRetriever while
   providing a consistent Haive configuration interface with flexible compression options.







Classes
-------

* :py:class:`ContextualCompressionRetrieverConfig` - Configuration for Contextual Compression retriever in the Haive framework.
.. toctree::
   :hidden:
   :maxdepth: 1

   /api_clean/haive/core/engine/retriever/providers/ContextualCompressionRetrieverConfig/ContextualCompressionRetrieverConfig

Package Contents
----------------

