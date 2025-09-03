
haive.core.engine.vectorstore.providers.InMemoryVectorStoreConfig
=================================================================

.. py:module:: haive.core.engine.vectorstore.providers.InMemoryVectorStoreConfig

.. autoapi-nested-parse::

   InMemory Vector Store implementation for the Haive framework.

   from typing import Any
   This module provides a configuration class for the InMemory vector store,
   which provides simple in-memory vector operations for development and testing.

   InMemory provides:
   1. Simple dictionary-based storage
   2. Cosine similarity search using numpy
   3. No external dependencies beyond langchain-core
   4. Fast development and testing setup
   5. Document filtering capabilities
   6. Maximal marginal relevance search

   This vector store is particularly useful when:
   - You need quick development and testing
   - Want no external dependencies
   - Building prototypes and proofs of concept
   - Need simple vector operations
   - Testing vector search functionality

   The implementation integrates with LangChain's InMemoryVectorStore while providing
   a consistent Haive configuration interface.







Classes
-------

* :py:class:`InMemoryVectorStoreConfig` - Configuration for InMemory vector store in the Haive framework.
.. toctree::
   :hidden:
   :maxdepth: 1

   /api_clean/haive/core/engine/vectorstore/providers/InMemoryVectorStoreConfig/InMemoryVectorStoreConfig

Package Contents
----------------

