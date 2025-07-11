"""Tests for specific provider implementations.

This module tests individual provider implementations including:
- OpenAI provider
- Anthropic provider
- Google providers (Gemini, Vertex AI)
- Ollama provider
- Provider-specific parameters
"""

import os
from unittest.mock import Mock, patch

import pytest
from pydantic import SecretStr

from haive.core.models.llm.provider_types import LLMProvider
from haive.core.models.llm.providers.base import ProviderImportError


class TestOpenAIProvider:
    """Test OpenAI provider implementation."""

    def test_import_and_basic_config(self):
        """Test importing and basic configuration."""
        try:
            from haive.core.models.llm.providers.openai import OpenAIProvider
        except ImportError:
            pytest.skip("OpenAI provider not implemented yet")

        provider = OpenAIProvider()

        assert provider.provider == LLMProvider.OPENAI
        assert provider.model == "gpt-3.5-turbo"
        assert provider._get_import_package() == "langchain-openai"

    def test_openai_specific_params(self):
        """Test OpenAI-specific parameters."""
        try:
            from haive.core.models.llm.providers.openai import OpenAIProvider
        except ImportError:
            pytest.skip("OpenAI provider not implemented yet")

        provider = OpenAIProvider(
            model="gpt-4",
            temperature=0.7,
            max_tokens=2000,
            top_p=0.9,
            frequency_penalty=0.5,
            presence_penalty=0.3,
            n=2,
        )

        assert provider.model == "gpt-4"
        assert provider.temperature == 0.7
        assert provider.max_tokens == 2000
        assert provider.top_p == 0.9
        assert provider.frequency_penalty == 0.5
        assert provider.presence_penalty == 0.3
        assert provider.n == 2

    def test_openai_instantiate(self):
        """Test OpenAI instantiation with mocked LangChain."""
        try:
            from haive.core.models.llm.providers.openai import OpenAIProvider
        except ImportError:
            pytest.skip("OpenAI provider not implemented yet")

        provider = OpenAIProvider(
            model="gpt-4", api_key=SecretStr("test-key"), temperature=0.5
        )

        # Mock the ChatOpenAI class
        with patch.object(provider, "_get_chat_class") as mock_get_class:
            mock_chat_class = Mock()
            mock_get_class.return_value = mock_chat_class

            provider.instantiate()

            # Check correct parameters passed
            mock_chat_class.assert_called_once()
            call_args = mock_chat_class.call_args[1]
            assert call_args["model_name"] == "gpt-4"
            assert call_args["openai_api_key"] == "test-key"
            assert call_args["temperature"] == 0.5


class TestAnthropicProvider:
    """Test Anthropic provider implementation."""

    def test_import_and_basic_config(self):
        """Test importing and basic configuration."""
        try:
            from haive.core.models.llm.providers.anthropic import AnthropicProvider
        except ImportError:
            pytest.skip("Anthropic provider not implemented yet")

        provider = AnthropicProvider()

        assert provider.provider == LLMProvider.ANTHROPIC
        assert provider.model == "claude-3-sonnet-20240229"
        assert provider._get_import_package() == "langchain-anthropic"

    def test_anthropic_specific_params(self):
        """Test Anthropic-specific parameters."""
        try:
            from haive.core.models.llm.providers.anthropic import AnthropicProvider
        except ImportError:
            pytest.skip("Anthropic provider not implemented yet")

        provider = AnthropicProvider(
            model="claude-3-opus-20240229",
            temperature=0.8,
            max_tokens=4096,
            top_p=0.95,
            top_k=40,
            streaming=True,
        )

        assert provider.model == "claude-3-opus-20240229"
        assert provider.temperature == 0.8
        assert provider.max_tokens == 4096
        assert provider.top_p == 0.95
        assert provider.top_k == 40
        assert provider.streaming is True

    def test_anthropic_model_list(self):
        """Test Anthropic model list."""
        try:
            from haive.core.models.llm.providers.anthropic import AnthropicProvider
        except ImportError:
            pytest.skip("Anthropic provider not implemented yet")

        models = AnthropicProvider.get_models()

        # Should include Claude 3 models
        assert "claude-3-opus-20240229" in models
        assert "claude-3-sonnet-20240229" in models
        assert "claude-3-haiku-20240307" in models


class TestGoogleProviders:
    """Test Google provider implementations."""

    def test_gemini_provider(self):
        """Test Gemini provider."""
        try:
            from haive.core.models.llm.providers.google import GeminiProvider
        except ImportError:
            pytest.skip("Google providers not implemented yet")

        provider = GeminiProvider()

        assert provider.provider == LLMProvider.GEMINI
        assert provider.model == "gemini-1.5-pro"
        assert provider._get_import_package() == "langchain-google-genai"
        assert provider._requires_api_key() is True

    def test_vertex_ai_provider(self):
        """Test Vertex AI provider."""
        try:
            from haive.core.models.llm.providers.google import VertexAIProvider
        except ImportError:
            pytest.skip("Google providers not implemented yet")

        provider = VertexAIProvider(project="test-project", location="us-central1")

        assert provider.provider == LLMProvider.VERTEX_AI
        assert provider.model == "gemini-1.5-pro"
        assert provider.project == "test-project"
        assert provider.location == "us-central1"
        assert provider._get_import_package() == "langchain-google-vertexai"
        assert provider._requires_api_key() is False

    def test_vertex_ai_validation(self):
        """Test Vertex AI validation."""
        try:
            from haive.core.models.llm.providers.google import VertexAIProvider
        except ImportError:
            pytest.skip("Google providers not implemented yet")

        # No project ID should raise error
        provider = VertexAIProvider()

        with pytest.raises(ValueError) as exc_info:
            provider._validate_config()

        assert "Google Cloud Project ID is required" in str(exc_info.value)


class TestOllamaProvider:
    """Test Ollama provider implementation."""

    def test_import_and_basic_config(self):
        """Test importing and basic configuration."""
        try:
            from haive.core.models.llm.providers.ollama import OllamaProvider
        except ImportError:
            pytest.skip("Ollama provider not implemented yet")

        provider = OllamaProvider()

        assert provider.provider == LLMProvider.OLLAMA
        assert provider.model == "llama3"
        assert provider.base_url == "http://localhost:11434"
        assert provider._get_import_package() == "langchain-ollama"
        assert provider._requires_api_key() is False

    def test_ollama_specific_params(self):
        """Test Ollama-specific parameters."""
        try:
            from haive.core.models.llm.providers.ollama import OllamaProvider
        except ImportError:
            pytest.skip("Ollama provider not implemented yet")

        provider = OllamaProvider(
            model="mixtral",
            base_url="http://192.168.1.100:11434",
            temperature=0.7,
            num_predict=2048,
            num_gpu=2,
            num_thread=8,
            repeat_penalty=1.1,
            seed=42,
        )

        assert provider.model == "mixtral"
        assert provider.base_url == "http://192.168.1.100:11434"
        assert provider.temperature == 0.7
        assert provider.num_predict == 2048
        assert provider.num_gpu == 2
        assert provider.num_thread == 8
        assert provider.repeat_penalty == 1.1
        assert provider.seed == 42

    @patch("requests.get")
    def test_ollama_get_models_from_server(self, mock_get):
        """Test getting models from Ollama server."""
        try:
            from haive.core.models.llm.providers.ollama import OllamaProvider
        except ImportError:
            pytest.skip("Ollama provider not implemented yet")

        # Mock server response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "models": [{"name": "llama3"}, {"name": "mixtral"}, {"name": "codellama"}]
        }
        mock_get.return_value = mock_response

        models = OllamaProvider.get_models()

        assert "llama3" in models
        assert "mixtral" in models
        assert "codellama" in models

    @patch("requests.get")
    def test_ollama_get_models_fallback(self, mock_get):
        """Test model list fallback when server unavailable."""
        try:
            from haive.core.models.llm.providers.ollama import OllamaProvider
        except ImportError:
            pytest.skip("Ollama provider not implemented yet")

        # Mock server error
        mock_get.side_effect = Exception("Connection error")

        models = OllamaProvider.get_models()

        # Should return predefined list
        assert "llama3" in models
        assert "mistral" in models
        assert "mixtral" in models
