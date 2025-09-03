
haive.core.engine.retriever.providers.KNNRetrieverConfig
========================================================

.. py:module:: haive.core.engine.retriever.providers.KNNRetrieverConfig

.. autoapi-nested-parse::

   K-Nearest Neighbors Retriever implementation for the Haive framework.

   from typing import Any
   This module provides a configuration class for the KNN (K-Nearest Neighbors) retriever,
   which uses k-nearest neighbors algorithm for document retrieval based on vector similarity.
   KNN finds the k most similar documents to a query by computing distances in the embedding space.

   The KNNRetriever works by:
   1. Embedding documents and queries using a specified embedding model
   2. Computing similarity/distance metrics between query and document embeddings
   3. Finding the k nearest neighbors based on the distance metric
   4. Returning the k most similar documents

   This retriever is particularly useful when:
   - Working with small to medium-sized document collections
   - Need simple but effective similarity-based retrieval
   - Want interpretable distance-based ranking
   - Building baseline vector retrieval systems
   - Comparing against more complex vector databases

   The implementation integrates with LangChain's KNNRetriever while providing
   a consistent Haive configuration interface.







Classes
-------

* :py:class:`KNNRetrieverConfig` - Configuration for K-Nearest Neighbors retriever in the Haive framework.
.. toctree::
   :hidden:
   :maxdepth: 1

   /api_clean/haive/core/engine/retriever/providers/KNNRetrieverConfig/KNNRetrieverConfig

Package Contents
----------------

