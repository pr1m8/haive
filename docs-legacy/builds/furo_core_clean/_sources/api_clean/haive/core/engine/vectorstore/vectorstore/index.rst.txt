
haive.core.engine.vectorstore.vectorstore
=========================================

.. py:module:: haive.core.engine.vectorstore.vectorstore

.. autoapi-nested-parse::

   Vector store engine implementation for the Haive framework.

   from typing import Any
   This module provides a comprehensive interface for working with vector stores in the Haive framework.
   It includes configuration models and utilities for creating, managing, and interacting with various
   vector store backends.

   .. attribute:: VectorStoreProvider

      Supported vector store providers (Chroma, FAISS, Pinecone, etc.)

      :type: :py:class:`Enum`

   Classes:
       VectorStoreConfig: Main configuration class for vector stores
       VectorStoreProvider: Enumeration of supported vector store providers
       VectorStoreProviderRegistry: Registry for extending supported providers

   .. admonition:: Example

      Basic usage of creating a vector store:
      ```python
      from haive.core.engine.vectorstore import VectorStoreConfig, VectorStoreProvider
      from haive.core.models.embeddings.base import HuggingFaceEmbeddingConfig
      
      # Create a vector store config
      config = VectorStoreConfig(
          name="my_vectorstore",
          documents=[Document(page_content="Hello world")],
          vector_store_provider=VectorStoreProvider.FAISS,
          embedding_model=HuggingFaceEmbeddingConfig(
              model="sentence-transformers/all-MiniLM-L6-v2"
          )
      )
      
      # Create the vector store
      vectorstore = config.create_vectorstore()
      ```
      
      Registering a custom vector store provider:
      ```python
      from haive.core.engine.vectorstore import VectorStoreProviderRegistry
      
      # Direct registration with a class
      class MyVectorStore(VectorStore):
          # Implementation of VectorStore methods
          ...
      
      VectorStoreProviderRegistry.register_provider("MyCustomStore", MyVectorStore)
      
      # Or with a factory function for lazy loading
      def get_my_vectorstore_class():
          from my_package.vectorstore import MyOtherVectorStore
          return MyOtherVectorStore
      
      VectorStoreProviderRegistry.register_provider_factory("MyOtherStore", get_my_vectorstore_class)
      
      # Now you can use these custom providers
      config = VectorStoreConfig(
          name="custom_vectorstore",
          vector_store_provider="MyCustomStore"
      )
      ```
      
      TODO: Need to seperate and implement the registry system, similar to retrievers and add base.






Functions
---------

   create_vectorstore   create_retriever   create_vs_config_from_documents   create_vs_from_documents   create_retriever_from_documents
.. autofunction:: create_vectorstore
.. autofunction:: create_retriever
.. autofunction:: create_vs_config_from_documents
.. autofunction:: create_vs_from_documents
.. autofunction:: create_retriever_from_documents

Classes
-------

* :py:class:`VectorStoreProvider` - Enumeration of supported vector store providers.* :py:class:`VectorStoreConfig` - Configuration model for a vector store engine.* :py:class:`VectorStoreProviderRegistry` - Registry for custom vector store providers.
.. toctree::
   :hidden:
   :maxdepth: 1

   /api_clean/haive/core/engine/vectorstore/vectorstore/VectorStoreProvider   /api_clean/haive/core/engine/vectorstore/vectorstore/VectorStoreConfig   /api_clean/haive/core/engine/vectorstore/vectorstore/VectorStoreProviderRegistry

Package Contents
----------------

