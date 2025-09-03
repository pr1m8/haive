
:py:mod:`haive.core.engine.vectorstore`
========================

.. py:module:: haive.core.engine.vectorstore

.. autoapi-nested-parse::

   Vector store module for the Haive framework.

   This module provides a comprehensive interface for working with vector databases
   in the Haive framework. It includes configuration models, utility functions, and
   abstractions for creating and interacting with vector stores through a unified API.

   Key components:
   - VectorStoreConfig: Main configuration class for vector stores
   - VectorStoreProvider: Enumeration of supported vector store providers
   - Utility functions for creating vector stores and retrievers

   The vector store system supports various backends (FAISS, Chroma, Pinecone, etc.)
   and provides a consistent interface for embedding, storing, and retrieving documents
   using vector similarity.

   .. admonition:: Examples

      >>> from haive.core.engine.vectorstore import (
      ...     VectorStoreConfig,
      ...     VectorStoreProvider,
      ...     create_vs_from_documents
      ... )
      >>> from langchain_core.documents import Document
      >>>
      >>> # Create documents
      >>> documents = [
      ...     Document(page_content="Apple iPhone 13 with A15 Bionic chip"),
      ...     Document(page_content="Samsung Galaxy S21 with Exynos processor")
      ... ]
      >>>
      >>> # Create a vector store directly
      >>> vectorstore = create_vs_from_documents(
      ...     documents,
      ...     vector_store_provider=VectorStoreProvider.FAISS
      ... )
      >>>
      >>> # Search for similar documents
      >>> results = vectorstore.similarity_search("smartphone with fast processor")




Subpackages
-----------

.. autosummary::
   :nosignatures:
   :template: autosummary/module.rst
   :toctree: .

   haive.core.engine.vectorstore.providers
.. toctree::
   :maxdepth: 2
   :hidden:

   /api_clean/haive/core/engine/vectorstore/providers/index

Submodules
----------

.. autosummary::
   :nosignatures:
   :template: autosummary/module.rst
   :toctree: .

   haive.core.engine.vectorstore.base   haive.core.engine.vectorstore.discovery   haive.core.engine.vectorstore.types   haive.core.engine.vectorstore.vectorstore
.. toctree::
   :maxdepth: 1
   :hidden:

   /api_clean/haive/core/engine/vectorstore/base/index   /api_clean/haive/core/engine/vectorstore/discovery/index   /api_clean/haive/core/engine/vectorstore/types/index   /api_clean/haive/core/engine/vectorstore/vectorstore/index





Package Contents
----------------

.. rubric:: haive.core.engine.vectorstore.__all__

.. autosummary::
   :nosignatures:

   haive.core.engine.vectorstore.VectorStoreConfig   haive.core.engine.vectorstore.VectorStoreProvider   haive.core.engine.vectorstore.VectorStoreProviderRegistry   haive.core.engine.vectorstore.create_retriever   haive.core.engine.vectorstore.create_retriever_from_documents   haive.core.engine.vectorstore.create_vectorstore   haive.core.engine.vectorstore.create_vs_config_from_documents   haive.core.engine.vectorstore.create_vs_from_documents

.. automodule:: haive.core.engine.vectorstore
   :members:
   :undoc-members:
   :show-inheritance: