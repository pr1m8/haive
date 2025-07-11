"""Tests for retriever factory."""

from unittest.mock import MagicMock, Mock, patch

import pytest

from haive.core.models.retriever.factory import (
    RetrieverFactory,
    create_provider,
    create_retriever,
    get_provider_info,
    list_available_providers,
)
from haive.core.models.retriever.provider_types import RetrieverProvider
from haive.core.models.retriever.providers.base import BaseRetrieverProvider


class TestRetrieverFactory:
    """Test RetrieverFactory class."""

    def test_create_with_string_provider(
        self, mock_vector_store, mock_vector_store_retriever
    ):
        """Test creating retriever with string provider."""
        with patch(
            "haive.core.models.retriever.providers.get_provider"
        ) as mock_get_provider:
            # Mock provider class
            mock_provider_class = Mock()
            mock_provider_instance = Mock(spec=BaseRetrieverProvider)
            mock_provider_instance.validate_config = Mock()
            mock_provider_instance.instantiate = Mock(return_value=Mock())
            mock_provider_class.return_value = mock_provider_instance
            mock_get_provider.return_value = mock_provider_class

            # Create retriever
            result = RetrieverFactory.create(
                "vector_store", vector_store=mock_vector_store, k=5
            )

            # Verify calls
            mock_get_provider.assert_called_once_with(RetrieverProvider.VECTOR_STORE)
            mock_provider_class.assert_called_once_with(
                vector_store=mock_vector_store, k=5
            )
            mock_provider_instance.validate_config.assert_called_once()
            mock_provider_instance.instantiate.assert_called_once()
            assert result is not None

    def test_create_with_enum_provider(self, mock_vector_store):
        """Test creating retriever with enum provider."""
        with patch(
            "haive.core.models.retriever.providers.get_provider"
        ) as mock_get_provider:
            mock_provider_class = Mock()
            mock_provider_instance = Mock(spec=BaseRetrieverProvider)
            mock_provider_instance.validate_config = Mock()
            mock_provider_instance.instantiate = Mock(return_value=Mock())
            mock_provider_class.return_value = mock_provider_instance
            mock_get_provider.return_value = mock_provider_class

            result = RetrieverFactory.create(
                RetrieverProvider.VECTOR_STORE, vector_store=mock_vector_store
            )

            mock_get_provider.assert_called_once_with(RetrieverProvider.VECTOR_STORE)
            assert result is not None

    def test_create_with_invalid_provider(self):
        """Test creating retriever with invalid provider string."""
        with pytest.raises(ValueError, match="Unknown provider 'invalid_provider'"):
            RetrieverFactory.create("invalid_provider")

    def test_create_with_unavailable_provider(self):
        """Test creating retriever with unavailable provider."""
        with patch(
            "haive.core.models.retriever.providers.get_provider"
        ) as mock_get_provider:
            mock_get_provider.return_value = None

            with pytest.raises(
                ImportError, match="Provider 'vector_store' is not available"
            ):
                RetrieverFactory.create("vector_store")

    def test_create_with_invalid_parameters(self):
        """Test creating retriever with invalid parameters."""
        with patch(
            "haive.core.models.retriever.providers.get_provider"
        ) as mock_get_provider:
            mock_provider_class = Mock()
            mock_provider_class.side_effect = ValueError("Invalid parameter")
            mock_get_provider.return_value = mock_provider_class

            with pytest.raises(
                ValueError, match="Invalid parameters for vector_store provider"
            ):
                RetrieverFactory.create("vector_store", invalid_param="value")

    def test_create_provider_success(self, mock_vector_store):
        """Test creating provider instance successfully."""
        with patch(
            "haive.core.models.retriever.providers.get_provider"
        ) as mock_get_provider:
            mock_provider_class = Mock()
            mock_provider_instance = Mock(spec=BaseRetrieverProvider)
            mock_provider_class.return_value = mock_provider_instance
            mock_get_provider.return_value = mock_provider_class

            result = RetrieverFactory.create_provider(
                "vector_store", vector_store=mock_vector_store
            )

            assert result == mock_provider_instance
            mock_provider_class.assert_called_once_with(vector_store=mock_vector_store)

    def test_get_provider_package_info(self):
        """Test getting package info for providers."""
        info = RetrieverFactory._get_provider_package_info(
            RetrieverProvider.VECTOR_STORE
        )
        assert "langchain-core" in info

        info = RetrieverFactory._get_provider_package_info(RetrieverProvider.BM25)
        assert "langchain-community" in info


class TestConvenienceFunctions:
    """Test convenience functions."""

    def test_create_retriever(self, mock_vector_store):
        """Test create_retriever convenience function."""
        with patch(
            "haive.core.models.retriever.factory.RetrieverFactory.create"
        ) as mock_create:
            mock_retriever = Mock()
            mock_create.return_value = mock_retriever

            result = create_retriever(
                "vector_store", vector_store=mock_vector_store, k=5
            )

            mock_create.assert_called_once_with(
                "vector_store", vector_store=mock_vector_store, k=5
            )
            assert result == mock_retriever

    def test_create_provider(self, mock_vector_store):
        """Test create_provider convenience function."""
        with patch(
            "haive.core.models.retriever.factory.RetrieverFactory.create_provider"
        ) as mock_create:
            mock_provider = Mock()
            mock_create.return_value = mock_provider

            result = create_provider("vector_store", vector_store=mock_vector_store)

            mock_create.assert_called_once_with(
                "vector_store", vector_store=mock_vector_store
            )
            assert result == mock_provider

    def test_list_available_providers(self):
        """Test list_available_providers function."""
        with patch(
            "haive.core.models.retriever.factory.get_available_providers"
        ) as mock_get:
            mock_providers = [RetrieverProvider.VECTOR_STORE, RetrieverProvider.BM25]
            mock_get.return_value = mock_providers

            result = list_available_providers()

            assert result == mock_providers

    def test_get_provider_info_success(self):
        """Test get_provider_info with available provider."""
        with patch(
            "haive.core.models.retriever.providers.get_provider"
        ) as mock_get_provider:
            mock_provider_class = Mock()
            mock_provider_class.__name__ = "VectorStoreProvider"
            mock_provider_class.__doc__ = "Test provider"
            mock_provider_class.model_fields = {
                "vector_store": Mock(
                    annotation="Any", default=None, description="Vector store"
                ),
                "k": Mock(annotation="int", default=4, description="Number of docs"),
            }
            mock_get_provider.return_value = mock_provider_class

            result = get_provider_info("vector_store")

            assert result["provider"] == "vector_store"
            assert result["available"] is True
            assert result["class_name"] == "VectorStoreProvider"
            assert "vector_store" in result["fields"]
            assert "k" in result["fields"]

    def test_get_provider_info_unavailable(self):
        """Test get_provider_info with unavailable provider."""
        with patch(
            "haive.core.models.retriever.providers.get_provider"
        ) as mock_get_provider:
            mock_get_provider.return_value = None

            result = get_provider_info("vector_store")

            assert result["provider"] == "vector_store"
            assert result["available"] is False
            assert "package_info" in result

    def test_get_provider_info_invalid(self):
        """Test get_provider_info with invalid provider."""
        result = get_provider_info("invalid_provider")

        assert "error" in result
        assert "Unknown provider" in result["error"]


class TestErrorHandling:
    """Test error handling scenarios."""

    def test_import_error_handling(self):
        """Test proper handling of import errors."""
        with patch(
            "haive.core.models.retriever.providers.get_provider"
        ) as mock_get_provider:
            mock_provider_class = Mock()
            mock_provider_instance = Mock(spec=BaseRetrieverProvider)
            mock_provider_instance.validate_config = Mock()
            mock_provider_instance.instantiate = Mock(
                side_effect=ImportError("Package not found")
            )
            mock_provider_class.return_value = mock_provider_instance
            mock_get_provider.return_value = mock_provider_class

            with pytest.raises(ImportError):
                RetrieverFactory.create("vector_store")

    def test_runtime_error_handling(self):
        """Test handling of unexpected runtime errors."""
        with patch(
            "haive.core.models.retriever.providers.get_provider"
        ) as mock_get_provider:
            mock_provider_class = Mock()
            mock_provider_instance = Mock(spec=BaseRetrieverProvider)
            mock_provider_instance.validate_config = Mock()
            mock_provider_instance.instantiate = Mock(
                side_effect=Exception("Unexpected error")
            )
            mock_provider_class.return_value = mock_provider_instance
            mock_get_provider.return_value = mock_provider_class

            with pytest.raises(RuntimeError, match="Failed to create retriever"):
                RetrieverFactory.create("vector_store")
