"""
Test module for embedding providers.

This module contains tests for the embedding providers to ensure
that they are properly registered and can be instantiated.
"""

import unittest
from typing import List, Type

from haive.core.models.embeddings import (  # Base; Cloud providers; Local providers; Factory function
    AnyscaleEmbeddingConfig,
    AzureEmbeddingConfig,
    BaseEmbeddingConfig,
    BedrockEmbeddingConfig,
    CloudflareEmbeddingConfig,
    CohereEmbeddingConfig,
    EmbeddingProvider,
    FastEmbedEmbeddingConfig,
    HuggingFaceEmbeddingConfig,
    JinaEmbeddingConfig,
    LlamaCppEmbeddingConfig,
    OllamaEmbeddingConfig,
    OpenAIEmbeddingConfig,
    SentenceTransformerEmbeddingConfig,
    VertexAIEmbeddingConfig,
    VoyageAIEmbeddingConfig,
    create_embeddings,
)


class TestEmbeddingProviders(unittest.TestCase):
    """Test case for embedding providers."""

    def test_provider_enum_values(self):
        """Test that all providers have proper string values."""
        # Verify all providers have non-empty string values
        for provider in EmbeddingProvider:
            self.assertIsInstance(provider.value, str)
            self.assertTrue(provider.value)  # Non-empty string

    def test_config_classes_exist(self):
        """Test that all config classes exist for each provider."""
        provider_to_config = {
            EmbeddingProvider.AZURE: AzureEmbeddingConfig,
            EmbeddingProvider.HUGGINGFACE: HuggingFaceEmbeddingConfig,
            EmbeddingProvider.OPENAI: OpenAIEmbeddingConfig,
            EmbeddingProvider.COHERE: CohereEmbeddingConfig,
            EmbeddingProvider.OLLAMA: OllamaEmbeddingConfig,
            EmbeddingProvider.SENTENCE_TRANSFORMERS: SentenceTransformerEmbeddingConfig,
            EmbeddingProvider.FASTEMBED: FastEmbedEmbeddingConfig,
            EmbeddingProvider.JINA: JinaEmbeddingConfig,
            EmbeddingProvider.VERTEXAI: VertexAIEmbeddingConfig,
            EmbeddingProvider.BEDROCK: BedrockEmbeddingConfig,
            EmbeddingProvider.CLOUDFLARE: CloudflareEmbeddingConfig,
            EmbeddingProvider.LLAMACPP: LlamaCppEmbeddingConfig,
            EmbeddingProvider.VOYAGEAI: VoyageAIEmbeddingConfig,
            EmbeddingProvider.ANYSCALE: AnyscaleEmbeddingConfig,
            # Skip NOVITA for now as we haven't implemented it yet
        }

        # Default model parameter for each class that requires one
        default_params = {
            AzureEmbeddingConfig: {"model": "text-embedding-ada-002"},
            LlamaCppEmbeddingConfig: {"model_path": "/path/to/model.gguf"},
        }

        # Verify we have a config class for each implemented provider
        for provider, config_class in provider_to_config.items():
            self.assertTrue(issubclass(config_class, BaseEmbeddingConfig))

            # Check that the provider attribute is correctly set
            params = default_params.get(config_class, {})
            config_instance = config_class(**params)
            self.assertEqual(config_instance.provider, provider)

    def test_factory_function(self):
        """Test that the factory function works with all config classes."""
        # Test with a provider that doesn't require external dependencies
        config = HuggingFaceEmbeddingConfig(
            model="all-MiniLM-L6-v2",
            # Use CPU to avoid requiring GPU for tests
            model_kwargs={"device": "cpu"},
            # Disable cache to avoid file system interactions
            use_cache=False,
        )

        try:
            # Import directly to check if it exists
            from langchain_huggingface import HuggingFaceEmbeddings

            # This will fail if the necessary packages aren't installed
            # We catch the exception to make the test pass in environments without all dependencies
            embeddings = create_embeddings(config)
            self.assertIsNotNone(embeddings)
        except (ImportError, ModuleNotFoundError):
            # Skip test if the required packages aren't installed
            self.skipTest("HuggingFace embeddings package not available")


if __name__ == "__main__":
    unittest.main()
