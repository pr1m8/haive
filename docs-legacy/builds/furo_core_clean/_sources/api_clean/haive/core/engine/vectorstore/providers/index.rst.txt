
:py:mod:`haive.core.engine.vectorstore.providers`
========================

.. py:module:: haive.core.engine.vectorstore.providers

.. autoapi-nested-parse::

   Vector store provider implementations for the Haive framework.

   This module provides comprehensive vector store functionality with support for
   over 25 different vector database backends including cloud-managed services,
   open-source databases, and specialized search engines. All providers follow
   a consistent configuration interface through BaseVectorStoreConfig.

   The module uses automatic registration where each provider configuration class
   extends BaseVectorStoreConfig and registers itself with the type system through
   decorators. This enables dynamic discovery and instantiation of vector stores.

   Supported Vector Store Categories:
       - **Cloud/Managed Services**: Pinecone, Weaviate, Qdrant Cloud, Supabase
       - **Open Source Databases**: Chroma, FAISS, Milvus, LanceDB
       - **Search Engines**: Elasticsearch, OpenSearch, TypeSense
       - **Database Extensions**: PostgreSQL (pgvector), Redis, MongoDB Atlas
       - **Graph Databases**: Neo4j with vector support
       - **Development/Testing**: InMemory, Fake stores

   Key Features:
       - Automatic registration through decorators
       - Dynamic loading and discovery
       - Consistent configuration interface
       - Support for metadata filtering and similarity search
       - Integration with various embedding providers
       - Scalable from development to production

   Available Providers:
       - **Amazon OpenSearch**: AWS managed OpenSearch with vector capabilities
       - **Annoy**: Spotify's approximate nearest neighbor library
       - **Azure AI Search**: Microsoft Azure cognitive search with vectors
       - **Cassandra**: Apache Cassandra with vector search extensions
       - **Chroma**: Popular open-source embedding database
       - **ClickHouse**: Analytical database with vector search
       - **DocArray**: Document-oriented vector storage
       - **Elasticsearch**: Enterprise search with dense/sparse vectors
       - **FAISS**: Facebook's efficient similarity search library
       - **InMemory**: Development and testing vector store
       - **LanceDB**: Modern columnar vector database
       - **Marqo**: Tensor-based search and recommendation engine
       - **Milvus**: Open-source vector database for AI applications
       - **MongoDB Atlas**: MongoDB with vector search capabilities
       - **Neo4j**: Graph database with vector similarity search
       - **OpenSearch**: Community-driven search and analytics
       - **Pinecone**: Managed vector database service
       - **PostgreSQL (pgvector)**: SQL database with vector extensions
       - **Qdrant**: Vector similarity search engine
       - **Redis**: In-memory database with vector search modules
       - **Scikit-learn**: ML library integration for vectors
       - **Supabase**: PostgreSQL-based backend with vector support
       - **Typesense**: Modern search engine with vector capabilities
       - **USearch**: High-performance similarity search
       - **Vectara**: Managed vector search platform
       - **Weaviate**: Open-source vector database
       - **Zilliz**: Cloud service for Milvus vector database

   .. admonition:: Examples

      Basic Chroma vector store setup::
      
          from haive.core.engine.vectorstore.providers import ChromaVectorStoreConfig
          from haive.core.engine.embedding.providers import OpenAIEmbeddingConfig
      
          # Configure embeddings
          embeddings_config = OpenAIEmbeddingConfig(
              name="openai_embeddings",
              model="text-embedding-3-large"
          )
      
          # Configure vector store
          vector_config = ChromaVectorStoreConfig(
              name="chroma_store",
              collection_name="documents",
              embedding_config=embeddings_config,
              persist_directory="./chroma_db"
          )
      
          # Instantiate vector store
          vectorstore = vector_config.instantiate()
      
      Pinecone cloud vector store::
      
          from haive.core.engine.vectorstore.providers import PineconeVectorStoreConfig
      
          vector_config = PineconeVectorStoreConfig(
              name="pinecone_store",
              index_name="my-index",
              api_key="your-api-key",
              environment="us-west1-gcp-free"
          )
      
          vectorstore = vector_config.instantiate()
      
      PostgreSQL with pgvector extension::
      
          from haive.core.engine.vectorstore.providers import PGVectorStoreConfig
      
          vector_config = PGVectorStoreConfig(
              name="postgres_vectors",
              connection_string="postgresql://user:pass@localhost:5432/vectordb",
              collection_name="embeddings",
              embedding_config=embeddings_config
          )
      
      Configuration discovery and provider listing::
      
          from haive.core.engine.vectorstore import BaseVectorStoreConfig
      
          # List all registered vector store types
          available_stores = BaseVectorStoreConfig.list_registered_types()
          print(f"Available stores: {list(available_stores.keys())}")
      
          # Get specific provider class dynamically
          store_class = BaseVectorStoreConfig.get_config_class("Chroma")
          config = store_class(name="dynamic_store")

   .. note::

      All provider configurations are imported at module level to ensure proper
      registration with the base configuration system. This allows dynamic
      discovery and instantiation through the common interface.
      
      Vector stores automatically integrate with the embedding system and can
      be used for similarity search, document retrieval, and semantic analysis
      workflows throughout the Haive framework.





Submodules
----------

.. autosummary::
   :nosignatures:
   :template: autosummary/module.rst
   :toctree: .

   haive.core.engine.vectorstore.providers.AmazonOpenSearchVectorStoreConfig   haive.core.engine.vectorstore.providers.AnnoyVectorStoreConfig   haive.core.engine.vectorstore.providers.AzureSearchVectorStoreConfig   haive.core.engine.vectorstore.providers.CassandraVectorStoreConfig   haive.core.engine.vectorstore.providers.ChromaVectorStoreConfig   haive.core.engine.vectorstore.providers.ClickHouseVectorStoreConfig   haive.core.engine.vectorstore.providers.DocArrayVectorStoreConfig   haive.core.engine.vectorstore.providers.ElasticsearchVectorStoreConfig   haive.core.engine.vectorstore.providers.FAISSVectorStoreConfig   haive.core.engine.vectorstore.providers.InMemoryVectorStoreConfig   haive.core.engine.vectorstore.providers.LanceDBVectorStoreConfig   haive.core.engine.vectorstore.providers.MarqoVectorStoreConfig   haive.core.engine.vectorstore.providers.MilvusVectorStoreConfig   haive.core.engine.vectorstore.providers.MongoDBAtlasVectorStoreConfig   haive.core.engine.vectorstore.providers.Neo4jVectorStoreConfig   haive.core.engine.vectorstore.providers.OpenSearchVectorStoreConfig   haive.core.engine.vectorstore.providers.PGVectorStoreConfig   haive.core.engine.vectorstore.providers.PineconeVectorStoreConfig   haive.core.engine.vectorstore.providers.QdrantVectorStoreConfig   haive.core.engine.vectorstore.providers.RedisVectorStoreConfig   haive.core.engine.vectorstore.providers.SKLearnVectorStoreConfig   haive.core.engine.vectorstore.providers.SupabaseVectorStoreConfig   haive.core.engine.vectorstore.providers.TypesenseVectorStoreConfig   haive.core.engine.vectorstore.providers.USearchVectorStoreConfig   haive.core.engine.vectorstore.providers.VectaraVectorStoreConfig   haive.core.engine.vectorstore.providers.WeaviateVectorStoreConfig   haive.core.engine.vectorstore.providers.ZillizVectorStoreConfig
.. toctree::
   :maxdepth: 1
   :hidden:

   /api_clean/haive/core/engine/vectorstore/providers/AmazonOpenSearchVectorStoreConfig/index   /api_clean/haive/core/engine/vectorstore/providers/AnnoyVectorStoreConfig/index   /api_clean/haive/core/engine/vectorstore/providers/AzureSearchVectorStoreConfig/index   /api_clean/haive/core/engine/vectorstore/providers/CassandraVectorStoreConfig/index   /api_clean/haive/core/engine/vectorstore/providers/ChromaVectorStoreConfig/index   /api_clean/haive/core/engine/vectorstore/providers/ClickHouseVectorStoreConfig/index   /api_clean/haive/core/engine/vectorstore/providers/DocArrayVectorStoreConfig/index   /api_clean/haive/core/engine/vectorstore/providers/ElasticsearchVectorStoreConfig/index   /api_clean/haive/core/engine/vectorstore/providers/FAISSVectorStoreConfig/index   /api_clean/haive/core/engine/vectorstore/providers/InMemoryVectorStoreConfig/index   /api_clean/haive/core/engine/vectorstore/providers/LanceDBVectorStoreConfig/index   /api_clean/haive/core/engine/vectorstore/providers/MarqoVectorStoreConfig/index   /api_clean/haive/core/engine/vectorstore/providers/MilvusVectorStoreConfig/index   /api_clean/haive/core/engine/vectorstore/providers/MongoDBAtlasVectorStoreConfig/index   /api_clean/haive/core/engine/vectorstore/providers/Neo4jVectorStoreConfig/index   /api_clean/haive/core/engine/vectorstore/providers/OpenSearchVectorStoreConfig/index   /api_clean/haive/core/engine/vectorstore/providers/PGVectorStoreConfig/index   /api_clean/haive/core/engine/vectorstore/providers/PineconeVectorStoreConfig/index   /api_clean/haive/core/engine/vectorstore/providers/QdrantVectorStoreConfig/index   /api_clean/haive/core/engine/vectorstore/providers/RedisVectorStoreConfig/index   /api_clean/haive/core/engine/vectorstore/providers/SKLearnVectorStoreConfig/index   /api_clean/haive/core/engine/vectorstore/providers/SupabaseVectorStoreConfig/index   /api_clean/haive/core/engine/vectorstore/providers/TypesenseVectorStoreConfig/index   /api_clean/haive/core/engine/vectorstore/providers/USearchVectorStoreConfig/index   /api_clean/haive/core/engine/vectorstore/providers/VectaraVectorStoreConfig/index   /api_clean/haive/core/engine/vectorstore/providers/WeaviateVectorStoreConfig/index   /api_clean/haive/core/engine/vectorstore/providers/ZillizVectorStoreConfig/index





Package Contents
----------------

.. rubric:: haive.core.engine.vectorstore.providers.__all__

.. autosummary::
   :nosignatures:

   haive.core.engine.vectorstore.providers.AmazonOpenSearchVectorStoreConfig   haive.core.engine.vectorstore.providers.AnnoyVectorStoreConfig   haive.core.engine.vectorstore.providers.AzureSearchVectorStoreConfig   haive.core.engine.vectorstore.providers.CassandraVectorStoreConfig   haive.core.engine.vectorstore.providers.ChromaVectorStoreConfig   haive.core.engine.vectorstore.providers.ClickHouseVectorStoreConfig   haive.core.engine.vectorstore.providers.DocArrayVectorStoreConfig   haive.core.engine.vectorstore.providers.ElasticsearchVectorStoreConfig   haive.core.engine.vectorstore.providers.FAISSVectorStoreConfig   haive.core.engine.vectorstore.providers.InMemoryVectorStoreConfig   haive.core.engine.vectorstore.providers.LanceDBVectorStoreConfig   haive.core.engine.vectorstore.providers.MarqoVectorStoreConfig   haive.core.engine.vectorstore.providers.MilvusVectorStoreConfig   haive.core.engine.vectorstore.providers.MongoDBAtlasVectorStoreConfig   haive.core.engine.vectorstore.providers.Neo4jVectorStoreConfig   haive.core.engine.vectorstore.providers.OpenSearchVectorStoreConfig   haive.core.engine.vectorstore.providers.PGVectorStoreConfig   haive.core.engine.vectorstore.providers.PineconeVectorStoreConfig   haive.core.engine.vectorstore.providers.QdrantVectorStoreConfig   haive.core.engine.vectorstore.providers.RedisVectorStoreConfig   haive.core.engine.vectorstore.providers.SKLearnVectorStoreConfig   haive.core.engine.vectorstore.providers.SupabaseVectorStoreConfig   haive.core.engine.vectorstore.providers.TypesenseVectorStoreConfig   haive.core.engine.vectorstore.providers.USearchVectorStoreConfig   haive.core.engine.vectorstore.providers.VectaraVectorStoreConfig   haive.core.engine.vectorstore.providers.WeaviateVectorStoreConfig   haive.core.engine.vectorstore.providers.ZillizVectorStoreConfig

.. automodule:: haive.core.engine.vectorstore.providers
   :members:
   :undoc-members:
   :show-inheritance: