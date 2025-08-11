
:py:mod:`haive.core.engine.embedding.providers`
========================

.. py:module:: haive.core.engine.embedding.providers

.. autoapi-nested-parse::

   Embedding provider configurations.

   This module contains all the embedding provider configurations for the Haive framework.
   Each provider is implemented as a separate class that extends BaseEmbeddingConfig.

   Available Providers:
       - OpenAI: OpenAI embedding models (text-embedding-3-large, etc.)
       - Azure OpenAI: Azure-hosted OpenAI embedding models
       - HuggingFace: HuggingFace Hub and local transformer models
       - Cohere: Cohere embedding models (embed-english-v3.0, etc.)
       - Google Vertex AI: Google Cloud Vertex AI embedding models
       - Ollama: Locally hosted Ollama embedding models
       - Fake: Fake embeddings for testing

   .. admonition:: Examples

      Basic usage::
      
          from haive.core.engine.embedding.providers import OpenAIEmbeddingConfig
      
          config = OpenAIEmbeddingConfig(
              name="my_embeddings",
              model="text-embedding-3-large",
              api_key="sk-..."
          )
      
          embeddings = config.instantiate()
      
      Discovering providers::
      
          from haive.core.engine.embedding.base import BaseEmbeddingConfig
      
          # List all registered providers
          providers = BaseEmbeddingConfig.list_registered_types()
          print(f"Available providers: {list(providers.keys())}")
      
          # Get a specific provider
          provider_class = BaseEmbeddingConfig.get_config_class("OpenAI")





Submodules
----------

.. autosummary::
   :nosignatures:
   :template: autosummary/module.rst
   :toctree: .

   haive.core.engine.embedding.providers.AzureOpenAIEmbeddingConfig   haive.core.engine.embedding.providers.CohereEmbeddingConfig   haive.core.engine.embedding.providers.FakeEmbeddingConfig   haive.core.engine.embedding.providers.GoogleVertexAIEmbeddingConfig   haive.core.engine.embedding.providers.HuggingFaceEmbeddingConfig   haive.core.engine.embedding.providers.OllamaEmbeddingConfig   haive.core.engine.embedding.providers.OpenAIEmbeddingConfig
.. toctree::
   :maxdepth: 1
   :hidden:

   /api_clean/haive/core/engine/embedding/providers/AzureOpenAIEmbeddingConfig/index   /api_clean/haive/core/engine/embedding/providers/CohereEmbeddingConfig/index   /api_clean/haive/core/engine/embedding/providers/FakeEmbeddingConfig/index   /api_clean/haive/core/engine/embedding/providers/GoogleVertexAIEmbeddingConfig/index   /api_clean/haive/core/engine/embedding/providers/HuggingFaceEmbeddingConfig/index   /api_clean/haive/core/engine/embedding/providers/OllamaEmbeddingConfig/index   /api_clean/haive/core/engine/embedding/providers/OpenAIEmbeddingConfig/index





Package Contents
----------------

.. rubric:: haive.core.engine.embedding.providers.__all__

.. autosummary::
   :nosignatures:

   haive.core.engine.embedding.providers.AzureOpenAIEmbeddingConfig   haive.core.engine.embedding.providers.CohereEmbeddingConfig   haive.core.engine.embedding.providers.FakeEmbeddingConfig   haive.core.engine.embedding.providers.GoogleVertexAIEmbeddingConfig   haive.core.engine.embedding.providers.HuggingFaceEmbeddingConfig   haive.core.engine.embedding.providers.OllamaEmbeddingConfig   haive.core.engine.embedding.providers.OpenAIEmbeddingConfig

.. automodule:: haive.core.engine.embedding.providers
   :members:
   :undoc-members:
   :show-inheritance: