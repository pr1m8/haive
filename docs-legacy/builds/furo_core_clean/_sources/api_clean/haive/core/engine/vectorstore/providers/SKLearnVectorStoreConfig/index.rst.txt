
haive.core.engine.vectorstore.providers.SKLearnVectorStoreConfig
================================================================

.. py:module:: haive.core.engine.vectorstore.providers.SKLearnVectorStoreConfig

.. autoapi-nested-parse::

   SKLearn Vector Store implementation for the Haive framework.

   This module provides a configuration class for the SKLearn vector store,
   which provides ML-integrated nearest neighbor search using scikit-learn.

   SKLearn provides:
   1. Scikit-learn NearestNeighbors integration
   2. Multiple distance metrics and algorithms
   3. Persistent storage in multiple formats (JSON, BSON, Parquet)
   4. In-memory vector operations
   5. ML-friendly interface and integration
   6. Cross-platform compatibility

   This vector store is particularly useful when:
   - You need ML framework integration
   - Want familiar scikit-learn interface
   - Need persistent storage capabilities
   - Building ML pipelines with vector search
   - Require flexible distance metrics

   The implementation integrates with LangChain's SKLearn while providing
   a consistent Haive configuration interface.







Classes
-------

* :py:class:`SKLearnVectorStoreConfig` - Configuration for SKLearn vector store in the Haive framework.
.. toctree::
   :hidden:
   :maxdepth: 1

   /api_clean/haive/core/engine/vectorstore/providers/SKLearnVectorStoreConfig/SKLearnVectorStoreConfig

Package Contents
----------------

