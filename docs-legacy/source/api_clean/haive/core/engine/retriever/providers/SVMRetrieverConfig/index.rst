
haive.core.engine.retriever.providers.SVMRetrieverConfig
========================================================

.. py:module:: haive.core.engine.retriever.providers.SVMRetrieverConfig

.. autoapi-nested-parse::

   Support Vector Machine Retriever implementation for the Haive framework.

   from typing import Any
   This module provides a configuration class for the SVM (Support Vector Machine) retriever,
   which uses Support Vector Machine algorithm for document retrieval. SVM retriever treats
   document retrieval as a binary classification problem where the query represents the
   positive class and retrieves documents most similar to this positive class.

   The SVMRetriever works by:
   1. Training an SVM classifier using the query as positive examples
   2. Using the SVM decision function to score documents
   3. Ranking documents by their SVM scores
   4. Returning the top-k highest scoring documents

   This retriever is particularly useful when:
   - Working with text classification-style retrieval
   - Need margin-based similarity scoring
   - Want robust retrieval with outlier resistance
   - Building retrieval systems with limited training data
   - Combining with other ML-based retrieval approaches

   The implementation integrates with LangChain's SVMRetriever while providing
   a consistent Haive configuration interface.







Classes
-------

* :py:class:`SVMRetrieverConfig` - Configuration for Support Vector Machine retriever in the Haive framework.
.. toctree::
   :hidden:
   :maxdepth: 1

   /api_clean/haive/core/engine/retriever/providers/SVMRetrieverConfig/SVMRetrieverConfig

Package Contents
----------------

