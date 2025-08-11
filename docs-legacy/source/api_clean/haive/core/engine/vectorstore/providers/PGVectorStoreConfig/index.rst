
haive.core.engine.vectorstore.providers.PGVectorStoreConfig
===========================================================

.. py:module:: haive.core.engine.vectorstore.providers.PGVectorStoreConfig

.. autoapi-nested-parse::

   PGVector Vector Store implementation for the Haive framework.

   This module provides a configuration class for the PGVector vector store,
   which adds vector similarity search capabilities to PostgreSQL databases.

   PGVector provides:
   1. Native PostgreSQL extension for vector operations
   2. Exact and approximate nearest neighbor search
   3. Multiple distance functions (L2, inner product, cosine)
   4. SQL-compatible vector operations
   5. ACID transactions with vector data
   6. Indexing with IVFFlat and HNSW algorithms

   This vector store is particularly useful when:
   - You want to add vector search to existing PostgreSQL infrastructure
   - Need ACID transactions with vector operations
   - Want to combine relational and vector data in SQL queries
   - Require mature database features (backup, replication, etc.)
   - Building applications that need both structured and vector data

   The implementation integrates with LangChain's PGVector while providing
   a consistent Haive configuration interface.







Classes
-------

* :py:class:`PGVectorStoreConfig` - Configuration for PGVector vector store in the Haive framework.
.. toctree::
   :hidden:
   :maxdepth: 1

   /api_clean/haive/core/engine/vectorstore/providers/PGVectorStoreConfig/PGVectorStoreConfig

Package Contents
----------------

