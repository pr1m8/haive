"""Google AI Providers Module.

This module implements both Google Generative AI (Gemini) and Vertex AI providers
for the Haive framework. It supports Gemini models through the standard API and
enterprise Vertex AI deployments.

The providers handle API key management, model configuration, and safe imports of
the langchain-google packages.

Examples:
    Using Gemini::

        from haive.core.models.llm.providers.google import GeminiProvider

        provider = GeminiProvider(
            model="gemini-1.5-pro",
            temperature=0.7
        )
        llm = provider.instantiate()

    Using Vertex AI::

        from haive.core.models.llm.providers.google import VertexAIProvider

        provider = VertexAIProvider(
            model="gemini-1.5-pro",
            project="my-project",
            location="us-central1"
        )
        llm = provider.instantiate()

.. autosummary::
   :toctree: generated/

   GeminiProvider
   VertexAIProvider
"""

import os
from typing import Any

from pydantic import Field

from haive.core.models.llm.provider_types import LLMProvider
from haive.core.models.llm.providers.base import BaseLLMProvider, ProviderImportError


class GeminiProvider(BaseLLMProvider):
    """Google Gemini language model provider configuration.

    This provider supports Google's Gemini models through the Generative AI API.
    It's suitable for general use with API key authentication.

    Attributes:
        provider: Always LLMProvider.GEMINI
        model: Model name (default: "gemini-1.5-pro")
        temperature: Sampling temperature (0-1)
        max_output_tokens: Maximum tokens to generate
        top_p: Nucleus sampling parameter
        top_k: Top-k sampling parameter
        n: Number of responses to generate

    Environment Variables:
        GOOGLE_API_KEY: API key for authentication
        GEMINI_API_KEY: Alternative API key environment variable

    Model Variants:
        - gemini-1.5-pro: Most capable, 1M token context
        - gemini-1.5-flash: Faster, more efficient
        - gemini-pro: Previous generation
        - gemini-pro-vision: Multimodal support

    Examples:
        Basic usage::

            provider = GeminiProvider(
                model="gemini-1.5-pro",
                temperature=0.7,
                max_output_tokens=2048
            )
            llm = provider.instantiate()

        With advanced sampling::

            provider = GeminiProvider(
                model="gemini-1.5-flash",
                temperature=0.9,
                top_p=0.95,
                top_k=40
            )
    """

    provider: LLMProvider = Field(
        default=LLMProvider.GEMINI, const=True, description="Provider identifier"
    )

    # Gemini specific parameters
    temperature: float | None = Field(
        default=None, ge=0, le=1, description="Sampling temperature"
    )
    max_output_tokens: int | None = Field(
        default=None, ge=1, description="Maximum tokens to generate"
    )
    top_p: float | None = Field(
        default=None, ge=0, le=1, description="Nucleus sampling parameter"
    )
    top_k: int | None = Field(
        default=None, ge=1, description="Top-k sampling parameter"
    )
    n: int | None = Field(default=None, ge=1, description="Number of responses")

    def _get_chat_class(self) -> type[Any]:
        """Get the Gemini chat class.

        Returns:
            ChatGoogleGenerativeAI class

        Raises:
            ProviderImportError: If langchain-google-genai is not installed
        """
        try:
            from langchain_google_genai import ChatGoogleGenerativeAI

            return ChatGoogleGenerativeAI
        except ImportError as e:
            raise ProviderImportError(
                provider="Google Gemini", package="langchain-google-genai"
            ) from e

    def _get_default_model(self) -> str:
        """Get the default model for Gemini.

        Returns:
            Default model name
        """
        return "gemini-1.5-pro"

    def _get_import_package(self) -> str:
        """Get the pip package name.

        Returns:
            Package name for installation
        """
        return "langchain-google-genai"

    def _get_env_key_name(self) -> str:
        """Get environment variable name for API key.

        Returns:
            Environment variable name
        """
        # Check both GOOGLE_API_KEY and GEMINI_API_KEY
        if os.getenv("GEMINI_API_KEY"):
            return "GEMINI_API_KEY"
        return "GOOGLE_API_KEY"

    def _get_initialization_params(self, **kwargs) -> dict:
        """Get initialization parameters for the LLM.

        Returns:
            Dictionary of initialization parameters
        """
        params = super()._get_initialization_params(**kwargs)

        # Add Gemini-specific parameters if set
        optional_params = ["temperature", "max_output_tokens", "top_p", "top_k", "n"]

        for param in optional_params:
            value = getattr(self, param)
            if value is not None:
                params[param] = value

        return params

    def _get_api_key_param_name(self) -> str | None:
        """Get the parameter name for API key.

        Returns:
            The parameter name for Google API key
        """
        return "google_api_key"

    @classmethod
    def get_models(cls) -> list[str]:
        """Get available Gemini models.

        Returns:
            List of available model names
        """
        return [
            "gemini-1.5-pro",
            "gemini-1.5-flash",
            "gemini-pro",
            "gemini-pro-vision",
        ]


class VertexAIProvider(BaseLLMProvider):
    """Google Vertex AI language model provider configuration.

    This provider supports Google's models through Vertex AI, suitable for
    enterprise deployments with project-based authentication and regional control.

    Attributes:
        provider: Always LLMProvider.VERTEX_AI
        model: Model name (default: "gemini-1.5-pro")
        project: Google Cloud project ID
        location: Google Cloud region (default: "us-central1")
        temperature: Sampling temperature (0-1)
        max_output_tokens: Maximum tokens to generate
        top_p: Nucleus sampling parameter
        top_k: Top-k sampling parameter

    Environment Variables:
        GOOGLE_CLOUD_PROJECT: Default project ID
        GOOGLE_APPLICATION_CREDENTIALS: Path to service account JSON

    Authentication:
        Vertex AI uses Google Cloud authentication. You can authenticate by:
        1. Setting GOOGLE_APPLICATION_CREDENTIALS to service account key path
        2. Using gcloud auth application-default login
        3. Running on Google Cloud with appropriate IAM roles

    Examples:
        Basic usage::

            provider = VertexAIProvider(
                model="gemini-1.5-pro",
                project="my-project",
                location="us-central1"
            )
            llm = provider.instantiate()

        With custom parameters::

            provider = VertexAIProvider(
                model="gemini-1.5-flash",
                project="my-project",
                location="europe-west1",
                temperature=0.5,
                max_output_tokens=1024
            )
    """

    provider: LLMProvider = Field(
        default=LLMProvider.VERTEX_AI, const=True, description="Provider identifier"
    )

    # Vertex AI specific parameters
    project: str | None = Field(default=None, description="Google Cloud project ID")
    location: str = Field(default="us-central1", description="Google Cloud region")
    temperature: float | None = Field(
        default=None, ge=0, le=1, description="Sampling temperature"
    )
    max_output_tokens: int | None = Field(
        default=None, ge=1, description="Maximum tokens to generate"
    )
    top_p: float | None = Field(
        default=None, ge=0, le=1, description="Nucleus sampling parameter"
    )
    top_k: int | None = Field(
        default=None, ge=1, description="Top-k sampling parameter"
    )

    def _get_chat_class(self) -> type[Any]:
        """Get the Vertex AI chat class.

        Returns:
            ChatVertexAI class

        Raises:
            ProviderImportError: If langchain-google-vertexai is not installed
        """
        try:
            from langchain_google_vertexai import ChatVertexAI

            return ChatVertexAI
        except ImportError as e:
            raise ProviderImportError(
                provider="Google Vertex AI", package="langchain-google-vertexai"
            ) from e

    def _get_default_model(self) -> str:
        """Get the default model for Vertex AI.

        Returns:
            Default model name
        """
        return "gemini-1.5-pro"

    def _get_import_package(self) -> str:
        """Get the pip package name.

        Returns:
            Package name for installation
        """
        return "langchain-google-vertexai"

    def _requires_api_key(self) -> bool:
        """Check if this provider requires an API key.

        Returns:
            False - Vertex AI uses Google Cloud auth, not API keys
        """
        return False

    def _validate_config(self) -> None:
        """Validate Vertex AI configuration.

        Raises:
            ValueError: If project ID is not set
        """
        if not self.project:
            # Try to get from environment
            self.project = os.getenv("GOOGLE_CLOUD_PROJECT")

        if not self.project:
            raise ValueError(
                "Google Cloud Project ID is required. "
                "Set the 'project' parameter or GOOGLE_CLOUD_PROJECT environment variable."
            )

    def _get_initialization_params(self, **kwargs) -> dict:
        """Get initialization parameters for the LLM.

        Returns:
            Dictionary of initialization parameters
        """
        params = super()._get_initialization_params(**kwargs)

        # Remove API key related params
        params.pop("api_key", None)
        params.pop("cache", None)  # Vertex AI doesn't use cache param

        # Add required Vertex AI parameters
        params["project"] = self.project
        params["location"] = self.location

        # Use model_name instead of model
        params["model_name"] = params.pop("model")

        # Add optional parameters if set
        optional_params = ["temperature", "max_output_tokens", "top_p", "top_k"]

        for param in optional_params:
            value = getattr(self, param)
            if value is not None:
                params[param] = value

        return params

    @classmethod
    def get_models(cls) -> list[str]:
        """Get available Vertex AI models.

        Returns:
            List of available model names
        """
        return [
            "gemini-1.5-pro",
            "gemini-1.5-flash",
            "gemini-pro",
            "gemini-pro-vision",
            "text-bison",
            "text-bison-32k",
            "code-bison",
            "code-bison-32k",
        ]
