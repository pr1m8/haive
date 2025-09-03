
haive.core.engine.vectorstore.providers.AnnoyVectorStoreConfig
==============================================================

.. py:module:: haive.core.engine.vectorstore.providers.AnnoyVectorStoreConfig

.. autoapi-nested-parse::

   Annoy Vector Store implementation for the Haive framework.

   This module provides a configuration class for the Annoy vector store,
   which provides memory-efficient approximate nearest neighbor search.

   Annoy provides:
   1. Memory-efficient approximate nearest neighbor search
   2. Fast querying with small memory footprint
   3. Multiple distance metrics (angular, euclidean, manhattan, etc.)
   4. Index building with configurable trees for speed/accuracy trade-offs
   5. Read-only after index building (immutable indices)
   6. No dependencies on large external libraries

   This vector store is particularly useful when:
   - You need memory-efficient vector search
   - Want fast approximate nearest neighbor search
   - Have a static dataset that doesn't need frequent updates
   - Building applications with resource constraints
   - Need deterministic search results

   The implementation integrates with LangChain's Annoy while providing
   a consistent Haive configuration interface.

   Note: Annoy indices are immutable after building - no new documents
   can be added once the index is created.







Classes
-------

* :py:class:`AnnoyVectorStoreConfig` - Configuration for Annoy vector store in the Haive framework.
.. toctree::
   :hidden:
   :maxdepth: 1

   /api_clean/haive/core/engine/vectorstore/providers/AnnoyVectorStoreConfig/AnnoyVectorStoreConfig

Package Contents
----------------

