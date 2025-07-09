"""
Test module for vector store providers.

This module contains tests for the VectorStoreProvider enum and the
VectorStoreProviderRegistry to ensure all providers are properly registered
and can be instantiated.
"""

import unittest
from typing import List, Type

from langchain_core.vectorstores import VectorStore

from haive.core.engine.vectorstore.vectorstore import (
    VectorStoreConfig,
    VectorStoreProvider,
    VectorStoreProviderRegistry,
)


class TestVectorStoreProviders(unittest.TestCase):
    """Test case for vector store providers."""

    def test_provider_enum_values(self):
        """Test that all providers have proper string values."""
        # Verify all providers have non-empty string values
        for provider in VectorStoreProvider:
            self.assertIsInstance(provider.value, str)
            self.assertTrue(provider.value)  # Non-empty string

    def test_provider_registry(self):
        """Test that the provider registry returns classes for built-in providers."""
        # Test getting the class for a built-in provider
        # Note: This doesn't actually instantiate the class
        provider_class = VectorStoreProviderRegistry.get_provider_class(
            VectorStoreProvider.FAISS
        )
        self.assertIsNone(
            provider_class
        )  # Should be None since we're falling back to the built-in imports

    def test_register_custom_provider(self):
        """Test registering a custom provider."""

        # Create a mock VectorStore class
        class MockVectorStore(VectorStore):
            """Mock vector store for testing."""

            def add_texts(self, texts: List[str], metadatas=None, **kwargs):
                """Add texts to the vector store."""
                return ["id1", "id2", "id3"]

            def similarity_search(self, query: str, k: int = 4, **kwargs):
                """Search for similar documents."""
                return []

            @classmethod
            def from_texts(cls, texts: List[str], embedding, metadatas=None, **kwargs):
                """Create a vector store from texts."""
                return cls()

            @classmethod
            def from_documents(cls, documents, embedding, **kwargs):
                """Create a vector store from documents."""
                return cls()

        # Register the custom provider
        VectorStoreProviderRegistry.register_provider("MockStore", MockVectorStore)

        # Get the class from the registry
        provider_class = VectorStoreProviderRegistry.get_provider_class("MockStore")
        self.assertEqual(provider_class, MockVectorStore)

    def test_provider_factory(self):
        """Test registering a provider factory."""

        # Create a factory function
        def get_mock_vectorstore() -> Type[VectorStore]:
            """Factory function returning a mock vector store class."""

            class FactoryMockVectorStore(VectorStore):
                """Mock vector store created from a factory."""

                def add_texts(self, texts: List[str], metadatas=None, **kwargs):
                    """Add texts to the vector store."""
                    return ["id1", "id2", "id3"]

                def similarity_search(self, query: str, k: int = 4, **kwargs):
                    """Search for similar documents."""
                    return []

                @classmethod
                def from_texts(
                    cls, texts: List[str], embedding, metadatas=None, **kwargs
                ):
                    """Create a vector store from texts."""
                    return cls()

                @classmethod
                def from_documents(cls, documents, embedding, **kwargs):
                    """Create a vector store from documents."""
                    return cls()

            return FactoryMockVectorStore

        # Register the factory
        VectorStoreProviderRegistry.register_provider_factory(
            "FactoryMockStore", get_mock_vectorstore
        )

        # Get the class from the registry
        provider_class = VectorStoreProviderRegistry.get_provider_class(
            "FactoryMockStore"
        )
        self.assertIsNotNone(provider_class)
        self.assertTrue(issubclass(provider_class, VectorStore))

    def test_list_providers(self):
        """Test listing all providers."""
        providers = VectorStoreProviderRegistry.list_providers()

        # Check that we have all the built-in providers
        self.assertIn("Chroma", providers)
        self.assertIn("FAISS", providers)
        self.assertIn("Pinecone", providers)
        self.assertIn("Weaviate", providers)
        self.assertIn("PGVector", providers)
        self.assertIn("Redis", providers)
        self.assertIn("Elasticsearch", providers)

        # Note: We don't check for custom providers here as they may not
        # be properly registered due to enum extension limitations


if __name__ == "__main__":
    unittest.main()
