"""Tests for LLM provider base classes and MRO.

This module tests the base provider infrastructure, including:
- Method Resolution Order (MRO) for multiple inheritance
- Base provider functionality
- Rate limiting mixin integration
- Safe import handling
"""

from unittest.mock import Mock, patch

import pytest
from pydantic import Field, SecretStr

from haive.core.common.mixins.secure_config import SecureConfigMixin
from haive.core.models.llm.provider_types import LLMProvider
from haive.core.models.llm.providers.base import BaseLLMProvider, ProviderImportError
from haive.core.models.llm.rate_limiting_mixin import RateLimitingMixin
from haive.core.models.metadata_mixin import ModelMetadataMixin


class TestMRO:
    """Test Method Resolution Order for provider classes."""

    def test_base_provider_mro(self):
        """Test that BaseLLMProvider has correct MRO."""
        mro = BaseLLMProvider.__mro__

        # Check that all expected classes are in MRO
        assert BaseLLMProvider in mro
        assert SecureConfigMixin in mro
        assert ModelMetadataMixin in mro
        assert RateLimitingMixin in mro

        # Check order - BaseLLMProvider should come first
        assert mro[0] == BaseLLMProvider

        # Check that pydantic BaseModel is in MRO
        from pydantic import BaseModel

        assert BaseModel in mro

    def test_no_mro_conflicts(self):
        """Test that there are no MRO conflicts when creating provider."""

        # Create a test provider class
        class TestProvider(BaseLLMProvider):
            provider: LLMProvider = Field(default=LLMProvider.OPENAI)

            def _get_chat_class(self):
                return Mock

            def _get_default_model(self):
                return "test-model"

            def _get_import_package(self):
                return "test-package"

        # Should be able to instantiate without MRO issues
        provider = TestProvider()
        assert provider is not None
        assert isinstance(provider, BaseLLMProvider)
        assert isinstance(provider, SecureConfigMixin)
        assert isinstance(provider, ModelMetadataMixin)
        assert isinstance(provider, RateLimitingMixin)


class TestBaseLLMProvider:
    """Test BaseLLMProvider functionality."""

    def test_abstract_methods(self):
        """Test that abstract methods must be implemented."""
        # Should not be able to instantiate BaseLLMProvider directly
        with pytest.raises(TypeError) as exc_info:
            BaseLLMProvider()

        assert "Can't instantiate abstract class" in str(exc_info.value)

    def test_provider_implementation(self):
        """Test implementing a provider."""

        class TestProvider(BaseLLMProvider):
            provider: LLMProvider = Field(default=LLMProvider.OPENAI)

            def _get_chat_class(self):
                return Mock

            def _get_default_model(self):
                return "test-model"

            def _get_import_package(self):
                return "test-package"

        provider = TestProvider()

        # Test default values
        assert provider.provider == LLMProvider.OPENAI
        assert provider.model == "test-model"  # Should use default
        assert provider.name == "test-model"  # Should match model
        assert provider.cache_enabled is True
        assert provider.debug is False

    def test_api_key_loading(self):
        """Test API key loading from environment."""

        class TestProvider(BaseLLMProvider):
            provider: LLMProvider = Field(default=LLMProvider.OPENAI)

            def _get_chat_class(self):
                return Mock

            def _get_default_model(self):
                return "test-model"

            def _get_import_package(self):
                return "test-package"

        # Test with environment variable
        with patch.dict("os.environ", {"OPENAI_API_KEY": "test-key-123"}):
            provider = TestProvider()
            assert provider.get_api_key() == "test-key-123"

        # Test with explicit API key
        provider = TestProvider(api_key=SecretStr("explicit-key"))
        assert provider.get_api_key() == "explicit-key"

    def test_instantiate_with_import_error(self):
        """Test instantiation with missing dependencies."""

        class TestProvider(BaseLLMProvider):
            provider: LLMProvider = Field(default=LLMProvider.OPENAI)

            def _get_chat_class(self):
                raise ImportError("langchain-openai not installed")

            def _get_default_model(self):
                return "test-model"

            def _get_import_package(self):
                return "langchain-openai"

        provider = TestProvider()

        with pytest.raises(ProviderImportError) as exc_info:
            provider.instantiate()

        assert "OpenAI provider is not available" in str(exc_info.value)
        assert "pip install langchain-openai" in str(exc_info.value)

    def test_instantiate_with_validation_error(self):
        """Test instantiation with validation errors."""

        class TestProvider(BaseLLMProvider):
            provider: LLMProvider = Field(default=LLMProvider.OPENAI)

            def _get_chat_class(self):
                return Mock

            def _get_default_model(self):
                return "test-model"

            def _get_import_package(self):
                return "test-package"

            def _requires_api_key(self):
                return True

        # No API key provided
        provider = TestProvider()

        with pytest.raises(ValueError) as exc_info:
            provider.instantiate()

        assert "API key is required" in str(exc_info.value)

    def test_rate_limiting_integration(self):
        """Test rate limiting mixin integration."""

        class TestProvider(BaseLLMProvider):
            provider: LLMProvider = Field(default=LLMProvider.OPENAI)

            def _get_chat_class(self):
                return Mock

            def _get_default_model(self):
                return "test-model"

            def _get_import_package(self):
                return "test-package"

            def _requires_api_key(self):
                return False

        # Create provider with rate limiting
        provider = TestProvider(requests_per_second=10, tokens_per_minute=100000)

        # Check rate limiting params are set
        assert provider.requests_per_second == 10
        assert provider.tokens_per_minute == 100000

        # Mock the apply_rate_limiting method
        mock_llm = Mock()
        with patch.object(
            provider, "apply_rate_limiting", return_value=mock_llm
        ) as mock_apply:
            result = provider.instantiate()

            # Should have called apply_rate_limiting
            mock_apply.assert_called_once()
            assert result == mock_llm


class TestProviderImportError:
    """Test ProviderImportError exception."""

    def test_default_message(self):
        """Test default error message."""
        error = ProviderImportError("OpenAI", "langchain-openai")
        assert (
            str(error)
            == "OpenAI provider is not available. Please install it with: pip install langchain-openai"
        )

    def test_custom_message(self):
        """Test custom error message."""
        error = ProviderImportError(
            "OpenAI", "langchain-openai", "Custom error message"
        )
        assert str(error) == "Custom error message"

    def test_attributes(self):
        """Test error attributes."""
        error = ProviderImportError("OpenAI", "langchain-openai")
        assert error.provider == "OpenAI"
        assert error.package == "langchain-openai"


class TestProviderMixins:
    """Test mixin functionality in providers."""

    def test_secure_config_mixin(self):
        """Test SecureConfigMixin functionality."""

        class TestProvider(BaseLLMProvider):
            provider: LLMProvider = Field(default=LLMProvider.OPENAI)

            def _get_chat_class(self):
                return Mock

            def _get_default_model(self):
                return "test-model"

            def _get_import_package(self):
                return "test-package"

        provider = TestProvider(api_key=SecretStr("test-key"))

        # Test secure config methods
        assert hasattr(provider, "get_api_key")
        assert provider.get_api_key() == "test-key"

    def test_metadata_mixin(self):
        """Test ModelMetadataMixin functionality."""

        class TestProvider(BaseLLMProvider):
            provider: LLMProvider = Field(default=LLMProvider.OPENAI)

            def _get_chat_class(self):
                return Mock

            def _get_default_model(self):
                return "gpt-4"

            def _get_import_package(self):
                return "test-package"

        provider = TestProvider(model="gpt-4")

        # Test metadata methods exist
        assert hasattr(provider, "get_context_window")
        assert hasattr(provider, "supports_vision")
        assert hasattr(provider, "supports_function_calling")

    def test_rate_limiting_mixin(self):
        """Test RateLimitingMixin functionality."""

        class TestProvider(BaseLLMProvider):
            provider: LLMProvider = Field(default=LLMProvider.OPENAI)

            def _get_chat_class(self):
                return Mock

            def _get_default_model(self):
                return "test-model"

            def _get_import_package(self):
                return "test-package"

        provider = TestProvider()

        # Test rate limiting methods exist
        assert hasattr(provider, "apply_rate_limiting")
        assert hasattr(provider, "get_rate_limit_info")

        # Test rate limit info
        info = provider.get_rate_limit_info()
        assert "requests_per_second" in info
        assert "tokens_per_second" in info
        assert "enabled" in info
        assert info["enabled"] is False  # No limits set
