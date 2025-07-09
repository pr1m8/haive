"""Tests for LLM factory functionality.

This module tests the LLM factory including:
- Provider creation
- Error handling for missing dependencies
- Rate limiting integration
- Provider listing and info
"""

from unittest.mock import Mock, patch

import pytest

from haive.core.models.llm.factory import (
    LLMFactory,
    create_llm,
    get_available_providers,
    get_provider_models,
)
from haive.core.models.llm.provider_types import LLMProvider
from haive.core.models.llm.providers.base import ProviderImportError


class TestLLMFactory:
    """Test LLMFactory class."""

    def test_factory_initialization(self):
        """Test factory can be initialized."""
        factory = LLMFactory()
        assert factory is not None

    @patch("haive.core.models.llm.factory.get_provider")
    def test_create_with_valid_provider(self, mock_get_provider):
        """Test creating LLM with valid provider."""
        # Mock provider class
        mock_provider_class = Mock()
        mock_provider_instance = Mock()
        mock_llm = Mock()

        mock_get_provider.return_value = mock_provider_class
        mock_provider_class.return_value = mock_provider_instance
        mock_provider_instance.instantiate.return_value = mock_llm

        factory = LLMFactory()

        # Create LLM
        result = factory.create(
            provider=LLMProvider.OPENAI, model="gpt-4", temperature=0.7
        )

        # Verify calls
        mock_get_provider.assert_called_once_with(LLMProvider.OPENAI)
        mock_provider_class.assert_called_once_with(model="gpt-4", temperature=0.7)
        mock_provider_instance.instantiate.assert_called_once()
        assert result == mock_llm

    @patch("haive.core.models.llm.factory.get_provider")
    def test_create_with_string_provider(self, mock_get_provider):
        """Test creating LLM with string provider name."""
        # Mock provider
        mock_provider_class = Mock()
        mock_provider_instance = Mock()
        mock_llm = Mock()

        mock_get_provider.return_value = mock_provider_class
        mock_provider_class.return_value = mock_provider_instance
        mock_provider_instance.instantiate.return_value = mock_llm

        factory = LLMFactory()

        # Create with string provider
        result = factory.create(provider="openai", model="gpt-3.5-turbo")

        # Should convert string to enum
        mock_get_provider.assert_called_once_with(LLMProvider.OPENAI)
        assert result == mock_llm

    def test_create_with_invalid_provider_string(self):
        """Test creating LLM with invalid provider string."""
        factory = LLMFactory()

        with pytest.raises(ValueError) as exc_info:
            factory.create(provider="invalid-provider")

        assert "Unknown provider: invalid-provider" in str(exc_info.value)

    @patch("haive.core.models.llm.factory.get_provider")
    def test_create_with_provider_not_available(self, mock_get_provider):
        """Test creating LLM when provider not available."""
        mock_get_provider.side_effect = ValueError("Provider not available")

        factory = LLMFactory()

        with pytest.raises(ValueError) as exc_info:
            factory.create(provider=LLMProvider.OPENAI)

        assert "Provider openai not available" in str(exc_info.value)

    @patch("haive.core.models.llm.factory.get_provider")
    def test_create_with_rate_limiting(self, mock_get_provider):
        """Test creating LLM with rate limiting parameters."""
        # Mock provider
        mock_provider_class = Mock()
        mock_provider_instance = Mock()
        mock_llm = Mock()

        mock_get_provider.return_value = mock_provider_class
        mock_provider_class.return_value = mock_provider_instance
        mock_provider_instance.instantiate.return_value = mock_llm

        factory = LLMFactory()

        # Create with rate limiting
        result = factory.create(
            provider=LLMProvider.OPENAI,
            model="gpt-4",
            requests_per_second=10,
            tokens_per_minute=100000,
            temperature=0.5,
        )

        # Check rate limiting params were passed to provider
        mock_provider_class.assert_called_once_with(
            model="gpt-4",
            temperature=0.5,
            requests_per_second=10,
            tokens_per_minute=100000,
        )
        assert result == mock_llm

    @patch("haive.core.models.llm.factory.get_provider")
    def test_create_with_import_error(self, mock_get_provider):
        """Test handling of import errors."""
        # Mock provider that raises ProviderImportError
        mock_provider_class = Mock()
        mock_provider_instance = Mock()

        mock_get_provider.return_value = mock_provider_class
        mock_provider_class.return_value = mock_provider_instance
        mock_provider_instance.instantiate.side_effect = ProviderImportError(
            "OpenAI", "langchain-openai"
        )

        factory = LLMFactory()

        with pytest.raises(ProviderImportError) as exc_info:
            factory.create(provider=LLMProvider.OPENAI)

        assert "OpenAI provider is not available" in str(exc_info.value)

    @patch("haive.core.models.llm.factory.list_providers")
    def test_get_available_providers(self, mock_list_providers):
        """Test getting available providers."""
        mock_list_providers.return_value = ["openai", "anthropic", "ollama"]

        factory = LLMFactory()
        providers = factory.get_available_providers()

        assert providers == ["openai", "anthropic", "ollama"]
        mock_list_providers.assert_called_once()

    @patch("haive.core.models.llm.factory.get_provider")
    def test_get_provider_info(self, mock_get_provider):
        """Test getting provider information."""
        # Mock provider class
        mock_provider_class = Mock()
        mock_provider_class.__name__ = "OpenAIProvider"
        mock_provider_instance = Mock()
        mock_provider_instance._get_import_package.return_value = "langchain-openai"

        mock_get_provider.return_value = mock_provider_class
        mock_provider_class.return_value = mock_provider_instance

        factory = LLMFactory()
        info = factory.get_provider_info(LLMProvider.OPENAI)

        assert info["name"] == "openai"
        assert info["config_class"] == "OpenAIProvider"
        assert info["import_required"] == "langchain-openai"
        assert info["available"] is True

    @patch("haive.core.models.llm.factory.get_provider")
    def test_get_provider_info_not_available(self, mock_get_provider):
        """Test getting info for unavailable provider."""
        mock_get_provider.side_effect = ImportError("Not available")

        factory = LLMFactory()
        info = factory.get_provider_info(LLMProvider.OPENAI)

        assert info["name"] == "openai"
        assert info["config_class"] == "Not Implemented"
        assert info["available"] is False


class TestFactoryFunctions:
    """Test module-level factory functions."""

    @patch("haive.core.models.llm.factory._factory")
    def test_create_llm(self, mock_factory):
        """Test create_llm convenience function."""
        mock_llm = Mock()
        mock_factory.create.return_value = mock_llm

        result = create_llm("openai", "gpt-4", temperature=0.7)

        mock_factory.create.assert_called_once_with(
            provider="openai", model="gpt-4", temperature=0.7
        )
        assert result == mock_llm

    @patch("haive.core.models.llm.factory.list_providers")
    def test_get_available_providers_function(self, mock_list_providers):
        """Test get_available_providers function."""
        mock_list_providers.return_value = ["openai", "anthropic"]

        result = get_available_providers()

        assert result == ["openai", "anthropic"]
        mock_list_providers.assert_called_once()

    @patch("haive.core.models.llm.factory.get_provider")
    def test_get_provider_models(self, mock_get_provider):
        """Test get_provider_models function."""
        # Mock provider class with get_models method
        mock_provider_class = Mock()
        mock_provider_class.get_models.return_value = ["gpt-4", "gpt-3.5-turbo"]

        mock_get_provider.return_value = mock_provider_class

        result = get_provider_models("openai")

        assert result == ["gpt-4", "gpt-3.5-turbo"]
        mock_get_provider.assert_called_once_with(LLMProvider.OPENAI)
        mock_provider_class.get_models.assert_called_once()

    @patch("haive.core.models.llm.factory.get_provider")
    def test_get_provider_models_not_implemented(self, mock_get_provider):
        """Test get_provider_models when provider doesn't support it."""
        # Mock provider without get_models
        mock_provider_class = Mock(spec=[])  # No methods
        mock_get_provider.return_value = mock_provider_class

        with pytest.raises(NotImplementedError) as exc_info:
            get_provider_models("openai")

        assert "does not support listing models" in str(exc_info.value)
