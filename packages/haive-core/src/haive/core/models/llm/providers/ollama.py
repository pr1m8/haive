"""Ollama Provider Module.

This module implements the Ollama language model provider for the Haive framework,
supporting local LLM deployment through Ollama's model serving infrastructure.

Ollama enables running open-source LLMs locally without requiring API keys or
external services, making it ideal for privacy-sensitive applications and
offline deployments.

Examples:
    Basic usage::

        from haive.core.models.llm.providers.ollama import OllamaProvider

        provider = OllamaProvider(
            model="llama3",
            temperature=0.7
        )
        llm = provider.instantiate()

    With custom server::

        provider = OllamaProvider(
            model="mixtral",
            base_url="http://gpu-server:11434",
            num_gpu=2
        )

.. autosummary::
   :toctree: generated/

   OllamaProvider
"""

import os
from typing import Any

from pydantic import Field

from haive.core.models.llm.provider_types import LLMProvider
from haive.core.models.llm.providers.base import BaseLLMProvider, ProviderImportError


class OllamaProvider(BaseLLMProvider):
    """Ollama local language model provider configuration.

    This provider supports running open-source LLMs locally through Ollama,
    including Llama 3, Mistral, Mixtral, and many other models. It requires
    a running Ollama server but no API keys.

    Attributes:
        provider: Always LLMProvider.OLLAMA
        model: Model name (default: "llama3")
        base_url: Ollama server URL (default: "http://localhost:11434")
        temperature: Sampling temperature (0-1)
        num_predict: Maximum tokens to generate
        top_p: Nucleus sampling parameter
        top_k: Top-k sampling parameter
        repeat_penalty: Repetition penalty
        seed: Random seed for reproducibility
        num_gpu: Number of GPUs to use
        num_thread: Number of CPU threads

    Environment Variables:
        OLLAMA_BASE_URL: Server URL (default: http://localhost:11434)
        OLLAMA_NUM_GPU: Default number of GPUs to use

    Popular Models:
        - llama3: Meta's Llama 3 (8B, 70B)
        - mistral: Mistral 7B
        - mixtral: Mixtral 8x7B MoE
        - codellama: Code-specialized Llama
        - phi3: Microsoft's Phi-3
        - gemma: Google's Gemma
        - qwen: Alibaba's Qwen

    Examples:
        Running Llama 3 locally::

            provider = OllamaProvider(
                model="llama3:70b",
                temperature=0.7,
                num_predict=2048
            )
            llm = provider.instantiate()

        Using a remote Ollama server::

            provider = OllamaProvider(
                model="mixtral:8x7b",
                base_url="http://192.168.1.100:11434",
                num_gpu=2,
                temperature=0.5
            )

        With specific hardware settings::

            provider = OllamaProvider(
                model="codellama:34b",
                num_gpu=1,
                num_thread=8,
                repeat_penalty=1.1
            )
    """

    provider: LLMProvider = Field(
        default=LLMProvider.OLLAMA, const=True, description="Provider identifier"
    )

    # Ollama specific parameters
    base_url: str = Field(
        default_factory=lambda: os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
        description="Ollama server URL",
    )
    temperature: float | None = Field(
        default=None, ge=0, le=1, description="Sampling temperature"
    )
    num_predict: int | None = Field(
        default=None, ge=1, description="Maximum tokens to generate"
    )
    top_p: float | None = Field(
        default=None, ge=0, le=1, description="Nucleus sampling parameter"
    )
    top_k: int | None = Field(
        default=None, ge=1, description="Top-k sampling parameter"
    )
    repeat_penalty: float | None = Field(
        default=None, ge=0, description="Repetition penalty"
    )
    seed: int | None = Field(
        default=None, description="Random seed for reproducibility"
    )
    num_gpu: int | None = Field(
        default_factory=lambda: int(os.getenv("OLLAMA_NUM_GPU", "0")) or None,
        ge=0,
        description="Number of GPUs to use",
    )
    num_thread: int | None = Field(
        default=None, ge=1, description="Number of CPU threads"
    )

    def _get_chat_class(self) -> type[Any]:
        """Get the Ollama chat class.

        Returns:
            ChatOllama class from langchain-ollama

        Raises:
            ProviderImportError: If langchain-ollama is not installed
        """
        try:
            from langchain_ollama import ChatOllama

            return ChatOllama
        except ImportError as e:
            raise ProviderImportError(
                provider="Ollama", package="langchain-ollama"
            ) from e

    def _get_default_model(self) -> str:
        """Get the default model for Ollama.

        Returns:
            Default model name
        """
        return "llama3"

    def _get_import_package(self) -> str:
        """Get the pip package name.

        Returns:
            Package name for installation
        """
        return "langchain-ollama"

    def _requires_api_key(self) -> bool:
        """Check if this provider requires an API key.

        Returns:
            False - Ollama runs locally without API keys
        """
        return False

    def _validate_config(self) -> None:
        """Validate Ollama configuration.

        For Ollama, we just ensure the base URL is set.
        """
        if not self.base_url:
            self.base_url = "http://localhost:11434"

    def _get_initialization_params(self, **kwargs) -> dict:
        """Get initialization parameters for the LLM.

        Returns:
            Dictionary of initialization parameters
        """
        params = super()._get_initialization_params(**kwargs)

        # Remove API key and cache params (not used by Ollama)
        params.pop("api_key", None)
        params.pop("cache", None)

        # Add base URL
        params["base_url"] = self.base_url

        # Add Ollama-specific parameters if set
        optional_params = [
            "temperature",
            "num_predict",
            "top_p",
            "top_k",
            "repeat_penalty",
            "seed",
            "num_gpu",
            "num_thread",
        ]

        for param in optional_params:
            value = getattr(self, param)
            if value is not None:
                params[param] = value

        return params

    @classmethod
    def get_models(cls) -> list[str]:
        """Get available Ollama models.

        This attempts to connect to the local Ollama server and list
        installed models. If the server is not running, returns a
        list of popular models.

        Returns:
            List of available model names
        """
        try:
            import requests

            base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
            response = requests.get(f"{base_url}/api/tags", timeout=5)

            if response.status_code == 200:
                models = response.json().get("models", [])
                return [model["name"] for model in models]
        except Exception:
            pass

        # Return popular models if can't connect to server
        return [
            "llama3",
            "llama3:70b",
            "mistral",
            "mixtral",
            "mixtral:8x7b",
            "codellama",
            "codellama:34b",
            "phi3",
            "gemma",
            "gemma:7b",
            "qwen",
            "qwen:72b",
            "deepseek-coder",
            "starcoder2",
            "neural-chat",
            "starling-lm",
            "openchat",
            "zephyr",
        ]
