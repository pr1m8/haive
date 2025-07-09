"""Anthropic Provider Module.

This module implements the Anthropic language model provider for the Haive framework,
supporting Claude 3 models (Opus, Sonnet, Haiku) and earlier Claude versions.

The provider handles API key management, model configuration, and safe imports of
the langchain-anthropic package dependencies.

Examples:
    Basic usage::

        from haive.core.models.llm.providers.anthropic import AnthropicProvider

        provider = AnthropicProvider(
            model="claude-3-opus-20240229",
            temperature=0.7,
            max_tokens=4096
        )
        llm = provider.instantiate()

    With streaming::

        provider = AnthropicProvider(
            model="claude-3-sonnet-20240229",
            streaming=True
        )

        async for chunk in provider.instantiate().astream("Tell me a story"):
            print(chunk.content, end="")

.. autosummary::
   :toctree: generated/

   AnthropicProvider
"""

import os
from typing import Any, List, Optional, Type

from pydantic import Field

from haive.core.models.llm.provider_types import LLMProvider
from haive.core.models.llm.providers.base import BaseLLMProvider, ProviderImportError


class AnthropicProvider(BaseLLMProvider):
    """Anthropic language model provider configuration.

    This provider supports all Anthropic Claude models including Claude 3
    (Opus, Sonnet, Haiku) and Claude 2 variants. It provides access to
    Anthropic's constitutional AI models with support for large context windows.

    Attributes:
        provider: Always LLMProvider.ANTHROPIC
        model: Model name (default: "claude-3-sonnet-20240229")
        temperature: Sampling temperature (0-1)
        max_tokens: Maximum tokens to generate (up to 4096)
        top_p: Nucleus sampling parameter
        top_k: Top-k sampling parameter
        streaming: Whether to stream responses

    Environment Variables:
        ANTHROPIC_API_KEY: API key for authentication
        ANTHROPIC_MODEL: Default model to use

    Model Variants:
        - claude-3-opus-20240229: Most capable, best for complex tasks
        - claude-3-sonnet-20240229: Balanced performance and speed
        - claude-3-haiku-20240307: Fastest, most cost-effective
        - claude-2.1: Previous generation, 200K context
        - claude-2.0: Previous generation, 100K context

    Examples:
        Using Claude 3 Opus::

            provider = AnthropicProvider(
                model="claude-3-opus-20240229",
                temperature=0.5,
                max_tokens=4096
            )
            llm = provider.instantiate()

        With custom sampling::

            provider = AnthropicProvider(
                model="claude-3-sonnet-20240229",
                temperature=0.8,
                top_p=0.9,
                top_k=40
            )
    """

    provider: LLMProvider = Field(
        default=LLMProvider.ANTHROPIC, const=True, description="Provider identifier"
    )

    # Anthropic specific parameters
    temperature: Optional[float] = Field(
        default=None, ge=0, le=1, description="Sampling temperature"
    )
    max_tokens: Optional[int] = Field(
        default=None, ge=1, le=4096, description="Maximum tokens to generate"
    )
    top_p: Optional[float] = Field(
        default=None, ge=0, le=1, description="Nucleus sampling parameter"
    )
    top_k: Optional[int] = Field(
        default=None, ge=1, description="Top-k sampling parameter"
    )
    streaming: bool = Field(default=False, description="Whether to stream responses")

    def _get_chat_class(self) -> Type[Any]:
        """Get the Anthropic chat class.

        Returns:
            ChatAnthropic class from langchain-anthropic

        Raises:
            ProviderImportError: If langchain-anthropic is not installed
        """
        try:
            from langchain_anthropic import ChatAnthropic

            return ChatAnthropic
        except ImportError as e:
            raise ProviderImportError(
                provider="Anthropic", package="langchain-anthropic"
            ) from e

    def _get_default_model(self) -> str:
        """Get the default model for Anthropic.

        Returns:
            Default model name from environment or Claude 3 Sonnet
        """
        return os.getenv("ANTHROPIC_MODEL", "claude-3-sonnet-20240229")

    def _get_import_package(self) -> str:
        """Get the pip package name.

        Returns:
            Package name for installation
        """
        return "langchain-anthropic"

    def _get_initialization_params(self, **kwargs) -> dict:
        """Get initialization parameters for the LLM.

        Returns:
            Dictionary of initialization parameters
        """
        params = super()._get_initialization_params(**kwargs)

        # Add Anthropic-specific parameters if set
        optional_params = ["temperature", "max_tokens", "top_p", "top_k", "streaming"]

        for param in optional_params:
            value = getattr(self, param)
            if value is not None:
                params[param] = value

        return params

    def _get_api_key_param_name(self) -> Optional[str]:
        """Get the parameter name for API key.

        Returns:
            The parameter name for Anthropic API key
        """
        return "anthropic_api_key"

    @classmethod
    def get_models(cls) -> List[str]:
        """Get available Anthropic models.

        Note: Anthropic doesn't provide a public API to list models,
        so this returns a hardcoded list of known models.

        Returns:
            List of available model names
        """
        return [
            # Claude 3 models
            "claude-3-opus-20240229",
            "claude-3-sonnet-20240229",
            "claude-3-haiku-20240307",
            # Claude 2 models
            "claude-2.1",
            "claude-2.0",
            # Legacy models
            "claude-instant-1.2",
        ]
