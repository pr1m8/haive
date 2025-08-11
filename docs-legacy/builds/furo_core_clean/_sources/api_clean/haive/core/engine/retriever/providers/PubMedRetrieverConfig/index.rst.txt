
haive.core.engine.retriever.providers.PubMedRetrieverConfig
===========================================================

.. py:module:: haive.core.engine.retriever.providers.PubMedRetrieverConfig

.. autoapi-nested-parse::

   PubMed Retriever implementation for the Haive framework.

   from typing import Any
   This module provides a configuration class for the PubMed retriever,
   which retrieves biomedical and life science literature from the PubMed database.
   PubMed is a free search engine accessing primarily the MEDLINE database of references
   and abstracts on life sciences and biomedical topics.

   The PubMedRetriever works by:
   1. Connecting to the PubMed API (via NCBI E-utilities)
   2. Executing search queries against the PubMed database
   3. Retrieving article abstracts and metadata
   4. Returning formatted documents with biomedical literature

   This retriever is particularly useful when:
   - Building medical or healthcare applications
   - Researching biomedical topics and treatments
   - Creating evidence-based medicine tools
   - Developing clinical decision support systems
   - Building scientific literature review applications

   The implementation integrates with LangChain's PubMedRetriever while providing
   a consistent Haive configuration interface.







Classes
-------

* :py:class:`PubMedRetrieverConfig` - Configuration for PubMed retriever in the Haive framework.
.. toctree::
   :hidden:
   :maxdepth: 1

   /api_clean/haive/core/engine/retriever/providers/PubMedRetrieverConfig/PubMedRetrieverConfig

Package Contents
----------------

