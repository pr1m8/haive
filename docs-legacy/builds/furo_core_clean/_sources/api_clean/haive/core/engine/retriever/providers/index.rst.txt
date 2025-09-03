
:py:mod:`haive.core.engine.retriever.providers`
========================

.. py:module:: haive.core.engine.retriever.providers

.. autoapi-nested-parse::

   Retriever provider implementations for the Haive framework.

   This module provides comprehensive document retrieval functionality with support for
   over 40 different retriever implementations spanning vector-based search, traditional
   sparse retrieval, hybrid approaches, and specialized domain-specific retrievers.
   All providers follow a consistent configuration interface through BaseRetrieverConfig.

   The module uses automatic registration where each retriever configuration class
   extends BaseRetrieverConfig and registers itself with the type system through
   the @BaseRetrieverConfig.register decorator. This enables dynamic discovery
   and instantiation of retrievers for RAG (Retrieval-Augmented Generation) workflows.

   Retriever Categories:
       - **Vector-Based Retrievers**: Dense vector similarity search using embeddings
           * VectorStore, MultiVector, SelfQuery, ParentDocument, TimeWeighted
       - **Sparse/Traditional Retrievers**: Keyword and term-based retrieval
           * BM25, TF-IDF, KNN, SVM for classical information retrieval
       - **Hybrid/Advanced Retrievers**: Combining multiple retrieval strategies
           * Ensemble, ContextualCompression, MultiQuery, Reranking
       - **Cloud Services**: Managed retrieval platforms
           * Amazon Knowledge Bases, Azure AI Search, Google Vertex AI Search
       - **Domain-Specific**: Specialized knowledge source retrievers
           * ArXiv (academic papers), PubMed (medical literature), Wikipedia
       - **Web/Search**: Internet and search engine integration
           * WebResearch, Tavily API, ChatGPT Plugin integration

   Key Features:
       - **Automatic Registration**: Decorators enable dynamic provider discovery
       - **Consistent Interface**: Unified configuration and instantiation patterns
       - **Metadata Filtering**: Advanced filtering capabilities across providers
       - **Reranking Support**: Integration with reranking models for quality
       - **LLM Integration**: Compatible with various language models
       - **Scalable Architecture**: From development to production deployments

   Available Retriever Implementations:

       **Cloud and Managed Services:**
           - **Amazon Knowledge Bases**: AWS managed RAG service
           - **Azure AI Search**: Microsoft cognitive search with semantic capabilities
           - **Google Vertex AI Search**: Google Cloud enterprise search
           - **Google Document AI Warehouse**: Document management and search
           - **Bedrock**: AWS Bedrock knowledge base integration

       **Vector-Based Retrievers:**
           - **VectorStore**: Core vector similarity search
           - **MultiVector**: Multiple vector representations per document
           - **SelfQuery**: Natural language to structured query translation
           - **ParentDocument**: Retrieve parent docs from child embeddings
           - **TimeWeighted**: Time-decay weighted vector retrieval
           - **Contextual Compression**: LLM-based result compression

       **Traditional/Sparse Retrievers:**
           - **BM25**: Best Matching 25 ranking function
           - **TF-IDF**: Term Frequency-Inverse Document Frequency
           - **KNN**: K-Nearest Neighbors classification-based retrieval
           - **SVM**: Support Vector Machine ranking

       **Hybrid and Advanced:**
           - **Ensemble**: Combine multiple retrievers with weights
           - **MultiQuery**: Generate multiple queries for better coverage
           - **Merger**: Merge and deduplicate results from multiple sources
           - **RePhraseQuery**: Automatically rephrase queries for better results

       **Search Engine Integration:**
           - **Elasticsearch**: Enterprise search platform
           - **Pinecone Hybrid**: Combines dense and sparse search
           - **Weaviate Hybrid**: GraphQL-based hybrid search
           - **Qdrant Sparse**: High-performance vector database

       **Domain-Specific Knowledge:**
           - **ArXiv**: Academic paper retrieval from arXiv.org
           - **PubMed**: Medical and life science literature
           - **Wikipedia**: Wikipedia article retrieval
           - **AskNews**: News article search and retrieval

       **Web and External APIs:**
           - **WebResearch**: Automated web research and synthesis
           - **Tavily Search**: AI-optimized search API
           - **ChatGPT Plugin**: Integration with ChatGPT plugins
           - **You.com**: You.com search engine integration

       **Vector Database Specific:**
           - **Milvus**: Open-source vector database retrieval
           - **DocArray**: Document array-based retrieval
           - **Vespa**: Yahoo's big data serving engine
           - **LlamaIndex**: LlamaIndex integration retrievers

       **Memory and Specialized:**
           - **Zep**: Conversational memory platform
           - **ZepCloud**: Cloud-hosted Zep retrieval
           - **Neural DB**: Neural database query interface
           - **Metal**: Managed vector search platform

   .. admonition:: Examples

      Basic vector store retriever setup::
      
          from haive.core.engine.retriever.providers import VectorStoreRetrieverConfig
          from haive.core.engine.vectorstore.providers import ChromaVectorStoreConfig
      
          # Configure vector store
          vectorstore_config = ChromaVectorStoreConfig(
              name="knowledge_base",
              collection_name="documents"
          )
          vectorstore = vectorstore_config.instantiate()
      
          # Configure retriever
          retriever_config = VectorStoreRetrieverConfig(
              name="vector_retriever",
              vectorstore=vectorstore,
              search_type="similarity",
              search_kwargs={"k": 5, "score_threshold": 0.7}
          )
          retriever = retriever_config.instantiate()
      
      Hybrid ensemble retrieval combining vector and BM25::
      
          from haive.core.engine.retriever.providers import (
              EnsembleRetrieverConfig,
              BM25RetrieverConfig,
              VectorStoreRetrieverConfig
          )
      
          # Create individual retrievers
          vector_config = VectorStoreRetrieverConfig(
              name="vector_retriever",
              vectorstore=vectorstore,
              search_kwargs={"k": 10}
          )
      
          bm25_config = BM25RetrieverConfig(
              name="bm25_retriever",
              documents=document_list,
              k=10
          )
      
          # Combine with ensemble
          ensemble_config = EnsembleRetrieverConfig(
              name="hybrid_retriever",
              retrievers=[vector_config.instantiate(), bm25_config.instantiate()],
              weights=[0.7, 0.3]  # Prefer vector search
          )
          ensemble = ensemble_config.instantiate()
      
      Self-query retriever with natural language filtering::
      
          from haive.core.engine.retriever.providers import SelfQueryRetrieverConfig
          from haive.core.engine.aug_llm import AugLLMConfig
      
          llm_config = AugLLMConfig(model="gpt-4")
          llm = llm_config.instantiate()
      
          retriever_config = SelfQueryRetrieverConfig(
              name="smart_retriever",
              vectorstore=vectorstore,
              llm=llm,
              document_content_description="Technical documentation and guides",
              metadata_field_info=[
                  {"name": "category", "type": "string", "description": "Document category"},
                  {"name": "date", "type": "datetime", "description": "Publication date"}
              ]
          )
          retriever = retriever_config.instantiate()
      
          # Query with natural language filters
          docs = retriever.get_relevant_documents(
              "Find recent Python tutorials from the programming category"
          )
      
      Web research retriever for external knowledge::
      
          from haive.core.engine.retriever.providers import WebResearchRetrieverConfig
      
          web_config = WebResearchRetrieverConfig(
              name="web_researcher",
              vectorstore=vectorstore,
              llm=llm,
              search_kwargs={"k": 8},
              num_search_results=6
          )
          web_retriever = web_config.instantiate()
      
      Configuration discovery and provider listing::
      
          from haive.core.engine.retriever import BaseRetrieverConfig
      
          # List all registered retriever types
          available_retrievers = BaseRetrieverConfig.list_registered_types()
          print(f"Available retrievers: {len(available_retrievers)} types")
      
          # Get specific retriever class dynamically
          retriever_class = BaseRetrieverConfig.get_config_class("Ensemble")
          config = retriever_class(name="dynamic_ensemble")

   .. note::

      All retriever configurations are imported at module level to ensure proper
      registration with the BaseRetrieverConfig registry system. This enables
      dynamic discovery and instantiation through the common retriever interface.
      
      Retrievers integrate seamlessly with vector stores, embedding systems, and
      LLMs to provide flexible RAG capabilities for knowledge retrieval, question
      answering, and document analysis workflows throughout the Haive framework.

   .. seealso::

      BaseRetrieverConfig: Base class for all retriever configurations
      RetrieverType: Enumeration of available retriever types
      VectorStore integration: Vector database backend configuration
      Embedding systems: Text embedding and similarity computation





Submodules
----------

.. autosummary::
   :nosignatures:
   :template: autosummary/module.rst
   :toctree: .

   haive.core.engine.retriever.providers.AmazonKnowledgeBasesRetrieverConfig   haive.core.engine.retriever.providers.ArceeRetrieverConfig   haive.core.engine.retriever.providers.ArxivRetrieverConfig   haive.core.engine.retriever.providers.AskNewsRetrieverConfig   haive.core.engine.retriever.providers.AzureAISearchRetrieverConfig   haive.core.engine.retriever.providers.BM25RetrieverConfig   haive.core.engine.retriever.providers.BedrockRetrieverConfig   haive.core.engine.retriever.providers.ChatGPTPluginRetrieverConfig   haive.core.engine.retriever.providers.CohereRagRetrieverConfig   haive.core.engine.retriever.providers.ContextualCompressionRetrieverConfig   haive.core.engine.retriever.providers.DocArrayRetrieverConfig   haive.core.engine.retriever.providers.ElasticsearchRetrieverConfig   haive.core.engine.retriever.providers.EnsembleRetrieverConfig   haive.core.engine.retriever.providers.GoogleDocumentAIWarehouseRetrieverConfig   haive.core.engine.retriever.providers.GoogleVertexAISearchRetrieverConfig   haive.core.engine.retriever.providers.KNNRetrieverConfig   haive.core.engine.retriever.providers.KendraRetrieverConfig   haive.core.engine.retriever.providers.LlamaIndexGraphRetrieverConfig   haive.core.engine.retriever.providers.LlamaIndexRetrieverConfig   haive.core.engine.retriever.providers.MergerRetrieverConfig   haive.core.engine.retriever.providers.MetalRetrieverConfig   haive.core.engine.retriever.providers.MilvusRetrieverConfig   haive.core.engine.retriever.providers.MultiQueryRetrieverConfig   haive.core.engine.retriever.providers.MultiVectorRetrieverConfig   haive.core.engine.retriever.providers.NeuralDBRetrieverConfig   haive.core.engine.retriever.providers.ParentDocumentRetrieverConfig   haive.core.engine.retriever.providers.PineconeHybridSearchRetrieverConfig   haive.core.engine.retriever.providers.PubMedRetrieverConfig   haive.core.engine.retriever.providers.QdrantSparseVectorRetrieverConfig   haive.core.engine.retriever.providers.RePhraseQueryRetrieverConfig   haive.core.engine.retriever.providers.RemoteLangChainRetrieverConfig   haive.core.engine.retriever.providers.SVMRetrieverConfig   haive.core.engine.retriever.providers.SelfQueryRetrieverConfig   haive.core.engine.retriever.providers.TFIDFRetrieverConfig   haive.core.engine.retriever.providers.TavilySearchAPIRetrieverConfig   haive.core.engine.retriever.providers.TimeWeightedVectorStoreRetrieverConfig   haive.core.engine.retriever.providers.VespaRetrieverConfig   haive.core.engine.retriever.providers.WeaviateHybridSearchRetrieverConfig   haive.core.engine.retriever.providers.WebResearchRetrieverConfig   haive.core.engine.retriever.providers.WikipediaRetrieverConfig   haive.core.engine.retriever.providers.YouRetrieverConfig   haive.core.engine.retriever.providers.ZepCloudRetrieverConfig   haive.core.engine.retriever.providers.ZepRetrieverConfig
.. toctree::
   :maxdepth: 1
   :hidden:

   /api_clean/haive/core/engine/retriever/providers/AmazonKnowledgeBasesRetrieverConfig/index   /api_clean/haive/core/engine/retriever/providers/ArceeRetrieverConfig/index   /api_clean/haive/core/engine/retriever/providers/ArxivRetrieverConfig/index   /api_clean/haive/core/engine/retriever/providers/AskNewsRetrieverConfig/index   /api_clean/haive/core/engine/retriever/providers/AzureAISearchRetrieverConfig/index   /api_clean/haive/core/engine/retriever/providers/BM25RetrieverConfig/index   /api_clean/haive/core/engine/retriever/providers/BedrockRetrieverConfig/index   /api_clean/haive/core/engine/retriever/providers/ChatGPTPluginRetrieverConfig/index   /api_clean/haive/core/engine/retriever/providers/CohereRagRetrieverConfig/index   /api_clean/haive/core/engine/retriever/providers/ContextualCompressionRetrieverConfig/index   /api_clean/haive/core/engine/retriever/providers/DocArrayRetrieverConfig/index   /api_clean/haive/core/engine/retriever/providers/ElasticsearchRetrieverConfig/index   /api_clean/haive/core/engine/retriever/providers/EnsembleRetrieverConfig/index   /api_clean/haive/core/engine/retriever/providers/GoogleDocumentAIWarehouseRetrieverConfig/index   /api_clean/haive/core/engine/retriever/providers/GoogleVertexAISearchRetrieverConfig/index   /api_clean/haive/core/engine/retriever/providers/KNNRetrieverConfig/index   /api_clean/haive/core/engine/retriever/providers/KendraRetrieverConfig/index   /api_clean/haive/core/engine/retriever/providers/LlamaIndexGraphRetrieverConfig/index   /api_clean/haive/core/engine/retriever/providers/LlamaIndexRetrieverConfig/index   /api_clean/haive/core/engine/retriever/providers/MergerRetrieverConfig/index   /api_clean/haive/core/engine/retriever/providers/MetalRetrieverConfig/index   /api_clean/haive/core/engine/retriever/providers/MilvusRetrieverConfig/index   /api_clean/haive/core/engine/retriever/providers/MultiQueryRetrieverConfig/index   /api_clean/haive/core/engine/retriever/providers/MultiVectorRetrieverConfig/index   /api_clean/haive/core/engine/retriever/providers/NeuralDBRetrieverConfig/index   /api_clean/haive/core/engine/retriever/providers/ParentDocumentRetrieverConfig/index   /api_clean/haive/core/engine/retriever/providers/PineconeHybridSearchRetrieverConfig/index   /api_clean/haive/core/engine/retriever/providers/PubMedRetrieverConfig/index   /api_clean/haive/core/engine/retriever/providers/QdrantSparseVectorRetrieverConfig/index   /api_clean/haive/core/engine/retriever/providers/RePhraseQueryRetrieverConfig/index   /api_clean/haive/core/engine/retriever/providers/RemoteLangChainRetrieverConfig/index   /api_clean/haive/core/engine/retriever/providers/SVMRetrieverConfig/index   /api_clean/haive/core/engine/retriever/providers/SelfQueryRetrieverConfig/index   /api_clean/haive/core/engine/retriever/providers/TFIDFRetrieverConfig/index   /api_clean/haive/core/engine/retriever/providers/TavilySearchAPIRetrieverConfig/index   /api_clean/haive/core/engine/retriever/providers/TimeWeightedVectorStoreRetrieverConfig/index   /api_clean/haive/core/engine/retriever/providers/VespaRetrieverConfig/index   /api_clean/haive/core/engine/retriever/providers/WeaviateHybridSearchRetrieverConfig/index   /api_clean/haive/core/engine/retriever/providers/WebResearchRetrieverConfig/index   /api_clean/haive/core/engine/retriever/providers/WikipediaRetrieverConfig/index   /api_clean/haive/core/engine/retriever/providers/YouRetrieverConfig/index   /api_clean/haive/core/engine/retriever/providers/ZepCloudRetrieverConfig/index   /api_clean/haive/core/engine/retriever/providers/ZepRetrieverConfig/index





Package Contents
----------------

.. rubric:: haive.core.engine.retriever.providers.__all__

.. autosummary::
   :nosignatures:

   haive.core.engine.retriever.providers.AmazonKnowledgeBasesRetrieverConfig   haive.core.engine.retriever.providers.ArceeRetrieverConfig   haive.core.engine.retriever.providers.ArxivRetrieverConfig   haive.core.engine.retriever.providers.AskNewsRetrieverConfig   haive.core.engine.retriever.providers.AzureAISearchRetrieverConfig   haive.core.engine.retriever.providers.BM25RetrieverConfig   haive.core.engine.retriever.providers.BedrockRetrieverConfig   haive.core.engine.retriever.providers.ChatGPTPluginRetrieverConfig   haive.core.engine.retriever.providers.CohereRagRetrieverConfig   haive.core.engine.retriever.providers.ContextualCompressionRetrieverConfig   haive.core.engine.retriever.providers.DocArrayRetrieverConfig   haive.core.engine.retriever.providers.ElasticsearchRetrieverConfig   haive.core.engine.retriever.providers.EnsembleRetrieverConfig   haive.core.engine.retriever.providers.GoogleDocumentAIWarehouseRetrieverConfig   haive.core.engine.retriever.providers.GoogleVertexAISearchRetrieverConfig   haive.core.engine.retriever.providers.KNNRetrieverConfig   haive.core.engine.retriever.providers.KendraRetrieverConfig   haive.core.engine.retriever.providers.LlamaIndexGraphRetrieverConfig   haive.core.engine.retriever.providers.LlamaIndexRetrieverConfig   haive.core.engine.retriever.providers.MergerRetrieverConfig   haive.core.engine.retriever.providers.MetalRetrieverConfig   haive.core.engine.retriever.providers.MilvusRetrieverConfig   haive.core.engine.retriever.providers.MultiQueryRetrieverConfig   haive.core.engine.retriever.providers.MultiVectorRetrieverConfig   haive.core.engine.retriever.providers.NeuralDBRetrieverConfig   haive.core.engine.retriever.providers.ParentDocumentRetrieverConfig   haive.core.engine.retriever.providers.PineconeHybridSearchRetrieverConfig   haive.core.engine.retriever.providers.PubMedRetrieverConfig   haive.core.engine.retriever.providers.QdrantSparseVectorRetrieverConfig   haive.core.engine.retriever.providers.RePhraseQueryRetrieverConfig   haive.core.engine.retriever.providers.RemoteLangChainRetrieverConfig   haive.core.engine.retriever.providers.SVMRetrieverConfig   haive.core.engine.retriever.providers.SelfQueryRetrieverConfig   haive.core.engine.retriever.providers.TFIDFRetrieverConfig   haive.core.engine.retriever.providers.TavilySearchAPIRetrieverConfig   haive.core.engine.retriever.providers.TimeWeightedVectorStoreRetrieverConfig   haive.core.engine.retriever.providers.VespaRetrieverConfig   haive.core.engine.retriever.providers.WeaviateHybridSearchRetrieverConfig   haive.core.engine.retriever.providers.WebResearchRetrieverConfig   haive.core.engine.retriever.providers.WikipediaRetrieverConfig   haive.core.engine.retriever.providers.YouRetrieverConfig   haive.core.engine.retriever.providers.ZepCloudRetrieverConfig   haive.core.engine.retriever.providers.ZepRetrieverConfig

.. automodule:: haive.core.engine.retriever.providers
   :members:
   :undoc-members:
   :show-inheritance: