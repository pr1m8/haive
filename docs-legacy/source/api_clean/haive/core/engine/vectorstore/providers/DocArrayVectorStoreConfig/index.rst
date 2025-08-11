
haive.core.engine.vectorstore.providers.DocArrayVectorStoreConfig
=================================================================

.. py:module:: haive.core.engine.vectorstore.providers.DocArrayVectorStoreConfig

.. autoapi-nested-parse::

   DocArray Vector Store implementation for the Haive framework.

   This module provides a configuration class for the DocArray vector store,
   which offers multiple storage backends for document-oriented vector operations.

   DocArray provides:
   1. Multiple storage backends (in-memory, HNSW, Weaviate, etc.)
   2. Document-oriented data model with rich metadata
   3. Multi-modal support (text, images, audio, etc.)
   4. High-performance vector operations
   5. Flexible schema definition
   6. Built-in data processing pipelines

   This vector store is particularly useful when:
   - You need document-oriented vector operations
   - Want multi-modal data support
   - Need flexible storage backends
   - Building ML pipelines with rich metadata
   - Require high-performance exact or approximate search

   The implementation integrates with LangChain's DocArray while providing
   a consistent Haive configuration interface.







Classes
-------

* :py:class:`DocArrayVectorStoreConfig` - Configuration for DocArray vector store in the Haive framework.
.. toctree::
   :hidden:
   :maxdepth: 1

   /api_clean/haive/core/engine/vectorstore/providers/DocArrayVectorStoreConfig/DocArrayVectorStoreConfig

Package Contents
----------------

