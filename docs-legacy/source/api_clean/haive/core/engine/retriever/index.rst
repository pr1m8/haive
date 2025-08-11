
:py:mod:`haive.core.engine.retriever`
========================

.. py:module:: haive.core.engine.retriever

.. autoapi-nested-parse::

   Retriever module for the Haive framework.

   This module provides a comprehensive interface for document retrieval in the Haive
   framework. It includes configuration classes, type definitions, and utilities for
   creating and using various types of document retrievers, with support for different
   retrieval strategies and extensibility mechanisms.

   Key components:
   - BaseRetrieverConfig: Base configuration class for all retrievers
   - VectorStoreRetrieverConfig: Configuration for vector store-based retrievers
   - RetrieverType: Enumeration of supported retriever types
   - Utility functions for creating and using retrievers

   The retriever system is designed to be highly extensible, with a plugin architecture
   that allows new retriever implementations to be added simply by registering them
   with the appropriate type. The system includes built-in support for vector store-based
   retrievers, ensemble retrievers, and various specialized retrieval strategies.

   .. admonition:: Examples

      >>> from haive.core.engine.retriever import BaseRetrieverConfig, RetrieverType
      >>> from haive.core.engine.vectorstore import VectorStoreConfig
      >>>
      >>> # Create a vector store config
      >>> vs_config = VectorStoreConfig(name="document_store")
      >>>
      >>> # Create a retriever config
      >>> retriever_config = BaseRetrieverConfig.from_retriever_type(
      ...     RetrieverType.VECTOR_STORE,
      ...     name="my_retriever",
      ...     vector_store_config=vs_config,
      ...     k=5
      ... )
      >>>
      >>> # Create and use the retriever
      >>> retriever = retriever_config.instantiate()
      >>> documents = retriever.get_relevant_documents("What is machine learning?")




Subpackages
-----------

.. autosummary::
   :nosignatures:
   :template: autosummary/module.rst
   :toctree: .

   haive.core.engine.retriever.providers
.. toctree::
   :maxdepth: 2
   :hidden:

   /api_clean/haive/core/engine/retriever/providers/index

Submodules
----------

.. autosummary::
   :nosignatures:
   :template: autosummary/module.rst
   :toctree: .

   haive.core.engine.retriever.mixins   haive.core.engine.retriever.retriever   haive.core.engine.retriever.types
.. toctree::
   :maxdepth: 1
   :hidden:

   /api_clean/haive/core/engine/retriever/mixins/index   /api_clean/haive/core/engine/retriever/retriever/index   /api_clean/haive/core/engine/retriever/types/index





Package Contents
----------------

.. rubric:: haive.core.engine.retriever.__all__

.. autosummary::
   :nosignatures:

   haive.core.engine.retriever.BaseRetrieverConfig   haive.core.engine.retriever.RetrieverType   haive.core.engine.retriever.VectorStoreRetrieverConfig   haive.core.engine.retriever.create_retriever_config   haive.core.engine.retriever.create_retriever_from_vectorstore

.. automodule:: haive.core.engine.retriever
   :members:
   :undoc-members:
   :show-inheritance: