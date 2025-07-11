"""OpenAI Provider Module.

This module implements the OpenAI language model provider for the Haive framework,
supporting GPT-3.5, GPT-4, and other OpenAI models through a clean, consistent interface.

The provider handles API key management, model configuration, and safe imports of
the langchain-openai package dependencies.

Examples:
    Basic usage::

        from haive.core.models.llm.providers.openai import OpenAIProvider

        provider = OpenAIProvider(
            model="gpt-4",
            temperature=0.7,
            max_tokens=1000
        )
        llm = provider.instantiate()

    With rate limiting::

        provider = OpenAIProvider(
            model="gpt-3.5-turbo",
            requests_per_second=10,
            tokens_per_minute=90000
        )
        llm = provider.instantiate()

.. autosummary::
   :toctree: generated/

   OpenAIProvider
"""

import os
from typing import Any

from pydantic import Field

from haive.core.models.llm.provider_types import LLMProvider
from haive.core.models.llm.providers.base import BaseLLMProvider, ProviderImportError


class OpenAIProvider(BaseLLMProvider):
    """OpenAI language model provider configuration.

    This provider supports all OpenAI chat models including GPT-3.5-turbo,
    GPT-4, and GPT-4-turbo variants. It handles API authentication, model
    selection, and advanced parameters like temperature and token limits.

    Attributes:
        provider: Always LLMProvider.OPENAI
        model: Model name (default: "gpt-3.5-turbo")
        temperature: Sampling temperature (0-2)
        max_tokens: Maximum tokens to generate
        top_p: Nucleus sampling parameter
        frequency_penalty: Frequency penalty (-2 to 2)
        presence_penalty: Presence penalty (-2 to 2)
        n: Number of completions to generate

    Environment Variables:
        OPENAI_API_KEY: API key for authentication
        OPENAI_ORG_ID: Optional organization ID

    Examples:
        Creating a GPT-4 instance::

            provider = OpenAIProvider(
                model="gpt-4",
                temperature=0.7,
                max_tokens=2000
            )
            llm = provider.instantiate()

            response = llm.invoke("Explain quantum computing")

        Using with custom parameters::

            provider = OpenAIProvider(
                model="gpt-3.5-turbo-16k",
                temperature=0.2,
                top_p=0.9,
                frequency_penalty=0.5
            )
    """

    provider: LLMProvider = Field(
        default=LLMProvider.OPENAI, const=True, description="Provider identifier"
    )

    # OpenAI specific parameters
    temperature: float | None = Field(
        default=None, ge=0, le=2, description="Sampling temperature"
    )
    max_tokens: int | None = Field(
        default=None, ge=1, description="Maximum tokens to generate"
    )
    top_p: float | None = Field(
        default=None, ge=0, le=1, description="Nucleus sampling parameter"
    )
    frequency_penalty: float | None = Field(
        default=None, ge=-2, le=2, description="Frequency penalty"
    )
    presence_penalty: float | None = Field(
        default=None, ge=-2, le=2, description="Presence penalty"
    )
    n: int | None = Field(default=None, ge=1, description="Number of completions")
    organization: str | None = Field(
        default_factory=lambda: os.getenv("OPENAI_ORG_ID"),
        description="OpenAI organization ID",
    )

    def _get_chat_class(self) -> type[Any]:
        """Get the OpenAI chat class.

        Returns:
            ChatOpenAI class from langchain-openai

        Raises:
            ProviderImportError: If langchain-openai is not installed
        """
        try:
            from langchain_openai import ChatOpenAI

            return ChatOpenAI
        except ImportError as e:
            raise ProviderImportError(
                provider="OpenAI", package="langchain-openai"
            ) from e

    def _get_default_model(self) -> str:
        """Get the default model for OpenAI.

        Returns:
            Default model name
        """
        return "gpt-3.5-turbo"

    def _get_import_package(self) -> str:
        """Get the pip package name.

        Returns:
            Package name for installation
        """
        return "langchain-openai"

    def _get_initialization_params(self, **kwargs) -> dict:
        """Get initialization parameters for the LLM.

        Returns:
            Dictionary of initialization parameters
        """
        params = super()._get_initialization_params(**kwargs)

        # Add OpenAI-specific parameters if set
        optional_params = [
            "temperature",
            "max_tokens",
            "top_p",
            "frequency_penalty",
            "presence_penalty",
            "n",
        ]

        for param in optional_params:
            value = getattr(self, param)
            if value is not None:
                params[param] = value

        # Add organization if set
        if self.organization:
            params["openai_organization"] = self.organization

        # OpenAI uses 'model_name' not 'model'
        params["model_name"] = params.pop("model")

        return params

    def _get_api_key_param_name(self) -> str | None:
        """Get the parameter name for API key.

        Returns:
            The parameter name for OpenAI API key
        """
        return "openai_api_key"

    @classmethod
    def get_models(cls) -> list[str]:
        """Get available OpenAI models.

        Returns:
            List of available model names

        Raises:
            ImportError: If openai package is not installed
            Exception: If API call fails
        """
        try:
            from openai import OpenAI

            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise ValueError("OPENAI_API_KEY environment variable not set")

            client = OpenAI(api_key=api_key)
            models = client.models.list()

            # Filter to chat models only
            chat_models = [
                model.id
                for model in models.data
                if model.id.startswith(("gpt-3.5", "gpt-4"))
            ]

            return sorted(chat_models)
        except ImportError:
            raise ImportError(
                "openai package is required to list models. "
                "Install with: pip install openai"
            )
        except Exception as e:
            raise Exception(f"Failed to retrieve OpenAI models: {e!s}")
