
:py:mod:`haive.core.engine`
========================

.. py:module:: haive.core.engine

.. autoapi-nested-parse::

   Engine module for the Haive framework.

   This module provides the core engine system that powers all AI agents and workflows
   in Haive. It includes LLM configurations, retriever systems, vector stores, and
   the base engine infrastructure.

   The engine system is designed to be modular and extensible, allowing for easy
   integration of new AI models, retrieval systems, and vector storage backends.

   Modules:
       aug_llm: Augmented LLM configurations and factories for creating LLM engines
       base: Base engine classes, protocols, and registry system
       retriever: Retriever implementations for RAG (Retrieval-Augmented Generation)
       vectorstore: Vector store integrations for semantic search and storage
       document: Document processing and transformation utilities
       agent: Agent-specific engine components

   Key Classes:
       AugLLMConfig: Configuration for augmented LLM engines with enhanced capabilities
       Engine: Base class for all engine implementations
       EngineRegistry: Registry for managing and discovering engine types
       BaseRetrieverConfig: Configuration for retriever engines
       VectorStoreConfig: Configuration for vector store engines

   Factory Functions:
       create_retriever: Create a retriever engine from configuration
       create_vectorstore: Create a vector store engine from configuration
       create_retriever_from_documents: Create a retriever with pre-loaded documents

   .. admonition:: Examples

      Creating an LLM engine::
      
          from haive.core.engine import AugLLMConfig
      
          config = AugLLMConfig(
              model="gpt-4",
              temperature=0.7,
              max_tokens=1000
          )
      
      Creating a vector store::
      
          from haive.core.engine import create_vectorstore, VectorStoreConfig
      
          config = VectorStoreConfig(
              type="chroma",
              collection_name="knowledge_base"
          )
          vectorstore = create_vectorstore(config)
      
      Creating a retriever::
      
          from haive.core.engine import create_retriever
      
          retriever = create_retriever(
              vectorstore=vectorstore,
              search_kwargs={"k": 5}
          )




Subpackages
-----------

.. autosummary::
   :nosignatures:
   :template: autosummary/module.rst
   :toctree: .

   haive.core.engine.aug_llm   haive.core.engine.base   haive.core.engine.document   haive.core.engine.embedding   haive.core.engine.output_parser   haive.core.engine.prompt_template   haive.core.engine.retriever   haive.core.engine.tool   haive.core.engine.vectorstore
.. toctree::
   :maxdepth: 2
   :hidden:

   /api_clean/haive/core/engine/aug_llm/index   /api_clean/haive/core/engine/base/index   /api_clean/haive/core/engine/document/index   /api_clean/haive/core/engine/embedding/index   /api_clean/haive/core/engine/output_parser/index   /api_clean/haive/core/engine/prompt_template/index   /api_clean/haive/core/engine/retriever/index   /api_clean/haive/core/engine/tool/index   /api_clean/haive/core/engine/vectorstore/index

Submodules
----------

.. autosummary::
   :nosignatures:
   :template: autosummary/module.rst
   :toctree: .

   haive.core.engine.embeddings
.. toctree::
   :maxdepth: 1
   :hidden:

   /api_clean/haive/core/engine/embeddings/index





Package Contents
----------------

.. rubric:: haive.core.engine.__all__

.. autosummary::
   :nosignatures:

   haive.core.engine.AugLLMConfig   haive.core.engine.Engine   haive.core.engine.InvokableEngine   haive.core.engine.EngineType   haive.core.engine.EngineRegistry   haive.core.engine.BaseEmbeddingConfig   haive.core.engine.EmbeddingType   haive.core.engine.create_embedding_config   haive.core.engine.OutputParserEngine   haive.core.engine.OutputParserType

.. automodule:: haive.core.engine
   :members:
   :undoc-members:
   :show-inheritance: