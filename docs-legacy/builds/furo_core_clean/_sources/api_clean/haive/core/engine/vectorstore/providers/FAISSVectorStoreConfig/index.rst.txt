
haive.core.engine.vectorstore.providers.FAISSVectorStoreConfig
==============================================================

.. py:module:: haive.core.engine.vectorstore.providers.FAISSVectorStoreConfig

.. autoapi-nested-parse::

   FAISS Vector Store implementation for the Haive framework.

   This module provides a configuration class for the FAISS (Facebook AI Similarity Search)
   vector store, which is a library for efficient similarity search and clustering of dense vectors.

   FAISS provides:
   1. Extremely fast similarity search for large-scale datasets
   2. Multiple index types optimized for different use cases
   3. GPU acceleration support
   4. Efficient memory usage with compression techniques
   5. Support for both exact and approximate nearest neighbor search

   This vector store is particularly useful when:
   - You need blazing-fast similarity search on large datasets
   - Working with millions or billions of vectors
   - Need to balance between search accuracy and speed
   - Want to leverage GPU acceleration for search
   - Building production systems requiring high throughput

   The implementation integrates with LangChain's FAISS while providing
   a consistent Haive configuration interface.







Classes
-------

* :py:class:`FAISSVectorStoreConfig` - Configuration for FAISS vector store in the Haive framework.
.. toctree::
   :hidden:
   :maxdepth: 1

   /api_clean/haive/core/engine/vectorstore/providers/FAISSVectorStoreConfig/FAISSVectorStoreConfig

Package Contents
----------------

