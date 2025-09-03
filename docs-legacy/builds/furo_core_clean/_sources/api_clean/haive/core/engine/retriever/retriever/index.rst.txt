
haive.core.engine.retriever.retriever
=====================================

.. py:module:: haive.core.engine.retriever.retriever

.. autoapi-nested-parse::

   Retriever engine implementation for the Haive framework.

   from typing import Any
   This module provides a flexible and extensible interface for document retrieval in the Haive framework.
   It includes base classes and implementations for various retriever types, with a focus on vector
   store-based retrieval.

   The module supports different retriever types through a plugin architecture, allowing easy extension
   with new retriever implementations while maintaining a consistent interface.

   Classes:
       RetrieverConfig: Base configuration class for all retrievers
       VectorStoreRetrieverConfig: Configuration for vector store-based retrievers

   Functions:
       create_retriever_config: Factory function for creating retriever configurations
       create_retriever_from_vectorstore: Helper to create a retriever from a vector store

   .. admonition:: Example

      Basic usage of creating a vector store retriever:
      ```python
      from haive.core.engine.retriever import VectorStoreRetrieverConfig
      from haive.core.engine.vectorstore import VectorStoreConfig
      
      # Create vector store config
      vs_config = VectorStoreConfig(...)
      
      # Create retriever config
      retriever_config = VectorStoreRetrieverConfig(
          name="my_retriever",
          vector_store_config=vs_config,
          k=4
      )
      
      # Create and use the retriever
      retriever = retriever_config.instantiate()
      docs = retriever.get_relevant_documents("query")
      ```






Functions
---------

   create_retriever_config   create_retriever_from_vectorstore
.. autofunction:: create_retriever_config
.. autofunction:: create_retriever_from_vectorstore

Classes
-------

* :py:class:`RetrieverInput` - Schema for retriever input.* :py:class:`RetrieverOutput` - Schema for retriever output.* :py:class:`BaseRetrieverConfig` - Base configuration for all retriever engines in the Haive framework.* :py:class:`VectorStoreRetrieverConfig` - Configuration for a vector store-based retriever in the Haive framework.
.. toctree::
   :hidden:
   :maxdepth: 1

   /api_clean/haive/core/engine/retriever/retriever/RetrieverInput   /api_clean/haive/core/engine/retriever/retriever/RetrieverOutput   /api_clean/haive/core/engine/retriever/retriever/BaseRetrieverConfig   /api_clean/haive/core/engine/retriever/retriever/VectorStoreRetrieverConfig

Package Contents
----------------

