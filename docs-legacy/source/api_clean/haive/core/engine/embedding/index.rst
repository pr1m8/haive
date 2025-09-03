
:py:mod:`haive.core.engine.embedding`
========================

.. py:module:: haive.core.engine.embedding

.. autoapi-nested-parse::

   Embedding engine module for the Haive framework.

   This module provides comprehensive embedding functionality with support for
   multiple providers including OpenAI, Azure OpenAI, HuggingFace, Cohere,
   Google Vertex AI, Ollama, and more.

   The module follows a factory pattern where embedding configurations are created
   through provider-specific config classes, then instantiated to create the actual
   embedding instances. All providers are lazily loaded to minimize startup time.

   .. attribute:: BaseEmbeddingConfig

      Base class for all embedding configurations.

   .. attribute:: EmbeddingConfigFactory

      Factory for creating embedding configurations.

   .. attribute:: EmbeddingType

      Enum of supported embedding providers.

   .. attribute:: create_embedding_config

      Factory function for creating configurations.

   .. attribute:: providers

      Lazily loaded providers module.

   .. admonition:: Examples

      Basic usage with OpenAI embeddings::
      
          from haive.core.engine.embedding import BaseEmbeddingConfig
          from haive.core.engine.embedding.providers import OpenAIEmbeddingConfig
      
          # Create configuration
          config = OpenAIEmbeddingConfig(
              name="my_embeddings",
              model="text-embedding-3-large"
          )
      
          # Instantiate embeddings
          embeddings = config.instantiate()
      
          # Embed text
          vectors = embeddings.embed_documents(["Hello world", "How are you?"])
          query_vector = embeddings.embed_query("Hello")
      
      Configuration discovery and dynamic provider selection::
      
          from haive.core.engine.embedding import BaseEmbeddingConfig
      
          # List all registered providers
          available_providers = BaseEmbeddingConfig.list_registered_types()
          print(f"Available providers: {available_providers}")
      
          # Get specific provider class
          provider_class = BaseEmbeddingConfig.get_config_class("OpenAI")
          config = provider_class(name="dynamic_embeddings")
      
      Using the factory function for simplified creation::
      
          from haive.core.engine.embedding import create_embedding_config
      
          config = create_embedding_config(
              provider="OpenAI",
              model="text-embedding-3-large",
              name="my_embeddings"
          )
      
          embeddings = config.instantiate()

   .. note::

      All provider classes are lazily loaded through the `providers` attribute
      to avoid import overhead during module initialization. This allows the
      framework to start quickly even when many providers are available.




Subpackages
-----------

.. autosummary::
   :nosignatures:
   :template: autosummary/module.rst
   :toctree: .

   haive.core.engine.embedding.providers
.. toctree::
   :maxdepth: 2
   :hidden:

   /api_clean/haive/core/engine/embedding/providers/index

Submodules
----------

.. autosummary::
   :nosignatures:
   :template: autosummary/module.rst
   :toctree: .

   haive.core.engine.embedding.base   haive.core.engine.embedding.config   haive.core.engine.embedding.types
.. toctree::
   :maxdepth: 1
   :hidden:

   /api_clean/haive/core/engine/embedding/base/index   /api_clean/haive/core/engine/embedding/config/index   /api_clean/haive/core/engine/embedding/types/index





Package Contents
----------------

.. rubric:: haive.core.engine.embedding.__all__

.. autosummary::
   :nosignatures:

   haive.core.engine.embedding.BaseEmbeddingConfig   haive.core.engine.embedding.EmbeddingConfigFactory   haive.core.engine.embedding.EmbeddingType   haive.core.engine.embedding.create_embedding_config   haive.core.engine.embedding.providers

.. automodule:: haive.core.engine.embedding
   :members:
   :undoc-members:
   :show-inheritance: