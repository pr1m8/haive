
haive.core.engine.retriever.providers.TFIDFRetrieverConfig
==========================================================

.. py:module:: haive.core.engine.retriever.providers.TFIDFRetrieverConfig

.. autoapi-nested-parse::

   TF-IDF Retriever implementation for the Haive framework.

   from typing import Any
   This module provides a configuration class for the TF-IDF (Term Frequency-Inverse Document Frequency)
   retriever, which uses classical TF-IDF scoring for document retrieval. TF-IDF is a numerical
   statistic that reflects how important a word is to a document in a collection of documents.

   The TFIDFRetriever works by:
   1. Computing term frequency (TF) for each term in each document
   2. Computing inverse document frequency (IDF) for each term across the corpus
   3. Calculating TF-IDF scores as the product of TF and IDF
   4. Ranking documents by their TF-IDF similarity to the query

   This retriever is particularly useful when:
   - Working with text-based document collections
   - Need classical information retrieval approaches
   - Want interpretable term-based ranking
   - Building baseline retrieval systems
   - Comparing against modern neural approaches

   The implementation integrates with LangChain's TFIDFRetriever while providing
   a consistent Haive configuration interface.







Classes
-------

* :py:class:`TFIDFRetrieverConfig` - Configuration for TF-IDF retriever in the Haive framework.
.. toctree::
   :hidden:
   :maxdepth: 1

   /api_clean/haive/core/engine/retriever/providers/TFIDFRetrieverConfig/TFIDFRetrieverConfig

Package Contents
----------------

