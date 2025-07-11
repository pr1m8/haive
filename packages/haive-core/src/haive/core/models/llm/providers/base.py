"""Base provider module for LLM configurations.

This module provides the base classes and utilities for all LLM provider implementations
in the Haive framework. It includes the base configuration class with metadata support,
rate limiting capabilities, and common functionality shared across all providers.

The module structure ensures consistent interfaces, proper error handling for optional
dependencies, and clean separation of concerns between different LLM providers.

Classes:
    BaseLLMProvider: Abstract base class for all LLM provider configurations
    ProviderImportError: Custom exception for provider import failures

Examples:
    Creating a custom provider::

        from haive.core.models.llm.providers.base import BaseLLMProvider
        from haive.core.models.llm.provider_types import LLMProvider

        class CustomLLMProvider(BaseLLMProvider):
            provider = LLMProvider.CUSTOM

            def _get_chat_class(self):
                from langchain_custom import ChatCustom
                return ChatCustom

            def _get_default_model(self):
                return "custom-model-v1"

.. autosummary::
   :toctree: generated/

   BaseLLMProvider
   ProviderImportError
"""

import logging
import os
from abc import ABC, abstractmethod
from typing import Any, Dict

from pydantic import BaseModel, Field, SecretStr, field_validator, model_validator

from haive.core.common.mixins.secure_config import SecureConfigMixin
from haive.core.models.llm.provider_types import LLMProvider
from haive.core.models.llm.rate_limiting_mixin import RateLimitingMixin
from haive.core.models.metadata_mixin import ModelMetadataMixin

logger = logging.getLogger(__name__)


class ProviderImportError(ImportError):
    """Custom exception for provider-specific import failures.

    This exception provides clearer error messages when LLM provider
    dependencies are not installed, including the package name needed
    for installation.

    Attributes:
        provider: The provider that failed to import
        package: The package name to install
        message: Custom error message
    """

    def __init__(self, provider: str, package: str, message: str | None = None):
        """Initialize the provider import error.

        Args:
            provider: Name of the provider
            package: Package name for pip install
            message: Optional custom message
        """
        self.provider = provider
        self.package = package

        if message is None:
            message = (
                f"{provider} provider is not available. "
                f"Please install it with: pip install {package}"
            )

        super().__init__(message)


class BaseLLMProvider(
    SecureConfigMixin, ModelMetadataMixin, RateLimitingMixin, BaseModel, ABC
):
    """Abstract base class for all LLM provider configurations.

    This class provides the common functionality and interface that all
    LLM provider implementations must follow. It includes:

    - Secure API key management with environment variable fallbacks
    - Model metadata access (context windows, capabilities, pricing)
    - Rate limiting configuration
    - Common configuration parameters
    - Safe import handling for optional dependencies

    Subclasses must implement:
        - _get_chat_class(): Return the LangChain chat class
        - _get_default_model(): Return the default model name
        - _get_import_package(): Return the pip package name

    Attributes:
        provider: The LLM provider enum value
        model: The specific model identifier
        name: Optional friendly name for the model
        api_key: Secure storage of API key with env fallback
        cache_enabled: Whether to enable response caching
        cache_ttl: Time-to-live for cached responses
        extra_params: Additional provider-specific parameters
        debug: Enable detailed debug output

    Examples:
        Creating a provider configuration::

            from haive.core.models.llm.providers.openai import OpenAIProvider

            provider = OpenAIProvider(
                model="gpt-4",
                temperature=0.7,
                max_tokens=1000
            )

            llm = provider.instantiate()
    """

    provider: LLMProvider = Field(..., description="The LLM provider identifier")
    model: str | None = Field(None, description="The model to use")
    name: str | None = Field(None, description="Friendly display name")
    api_key: SecretStr = Field(
        default_factory=lambda: SecretStr(""), description="API key for the provider"
    )
    cache_enabled: bool = Field(default=True, description="Enable response caching")
    cache_ttl: int | None = Field(
        default=300, description="Cache time-to-live in seconds"
    )
    extra_params: dict[str, Any] | None = Field(
        default_factory=dict, description="Additional provider-specific parameters"
    )
    debug: bool = Field(default=False, description="Enable debug output")

    # Rate limiting fields (from RateLimitingMixin)
    requests_per_second: float | None = Field(
        default=None,
        description="Maximum number of requests per second. None means no limit.",
        ge=0,
    )
    tokens_per_second: int | None = Field(
        default=None,
        description="Maximum number of tokens per second. None means no limit.",
        ge=0,
    )
    tokens_per_minute: int | None = Field(
        default=None,
        description="Maximum number of tokens per minute. None means no limit.",
        ge=0,
    )
    max_retries: int = Field(
        default=3,
        description="Maximum number of retries for rate-limited requests.",
        ge=0,
    )
    retry_delay: float = Field(
        default=1.0, description="Base delay between retries in seconds.", ge=0
    )
    check_every_n_seconds: float | None = Field(
        default=None,
        description="How often to check rate limits. None uses default.",
        ge=0,
    )
    burst_size: int | None = Field(
        default=None,
        description="Maximum burst size for rate limiting. None uses default.",
        ge=1,
    )

    model_config = {"arbitrary_types_allowed": True}

    @model_validator(mode="after")
    def set_defaults(self) -> "BaseLLMProvider":
        """Set default values after initialization.

        This validator ensures that model and name have appropriate
        default values if not provided during initialization.

        Returns:
            The validated instance
        """
        # Set default model if not provided
        if self.model is None:
            self.model = self._get_default_model()

        # Set default name if not provided
        if self.name is None:
            self.name = self.model

        return self

    @abstractmethod
    def _get_chat_class(self) -> type[Any]:
        """Get the LangChain chat class for this provider.

        This method must be implemented by each provider to return
        the appropriate LangChain chat class. It should handle imports
        and raise ProviderImportError if dependencies are missing.

        Returns:
            The LangChain chat class

        Raises:
            ProviderImportError: If required dependencies are not installed
        """

    @abstractmethod
    def _get_default_model(self) -> str:
        """Get the default model name for this provider.

        Returns:
            The default model identifier
        """

    @abstractmethod
    def _get_import_package(self) -> str:
        """Get the pip package name for this provider.

        Returns:
            The package name for pip install
        """

    def _get_env_key_name(self) -> str:
        """Get the environment variable name for API key.

        Returns:
            The environment variable name (e.g., OPENAI_API_KEY)
        """
        provider_upper = self.provider.value.upper()
        # Handle special cases
        if provider_upper == "TOGETHER_AI":
            return "TOGETHER_AI_API_KEY"
        if provider_upper == "FIREWORKS_AI":
            return "FIREWORKS_AI_API_KEY"
        return f"{provider_upper}_API_KEY"

    @field_validator("api_key")
    @classmethod
    def load_api_key(cls, v: SecretStr, info) -> SecretStr:
        """Load API key from environment if not provided.

        Args:
            v: The provided API key value
            info: Validation info containing the instance

        Returns:
            The API key (from input or environment)
        """
        if v.get_secret_value() == "" and hasattr(info, "data"):
            # Get provider from instance data
            provider = info.data.get("provider")
            if provider:
                # Construct env var name
                env_key = f"{provider.value.upper()}_API_KEY"
                env_value = os.getenv(env_key, "")
                return SecretStr(env_value)
        return v

    def _get_initialization_params(self, **kwargs) -> dict[str, Any]:
        """Get parameters for initializing the LLM.

        This method prepares all parameters needed to instantiate
        the LangChain chat model, including model name, API key,
        and any provider-specific parameters.

        Args:
            **kwargs: Additional parameters to include

        Returns:
            Dictionary of initialization parameters
        """
        params = {
            "model": self.model,
            "cache": self.cache_enabled,
            **(self.extra_params or {}),
            **kwargs,
        }

        # Add API key if available
        api_key = self.get_api_key()
        if api_key:
            # Most providers use 'api_key' but some have specific names
            api_key_param = self._get_api_key_param_name()
            if api_key_param:
                params[api_key_param] = api_key

        return params

    def _get_api_key_param_name(self) -> str | None:
        """Get the parameter name for API key.

        Different providers use different parameter names for API keys.
        This method returns the appropriate parameter name.

        Returns:
            The parameter name for API key, or None if no key needed
        """
        # Default for most providers
        return "api_key"

    def instantiate(self, **kwargs) -> Any:
        """Instantiate the LLM with rate limiting if configured.

        This method creates an instance of the LLM using the provider's
        chat class and configuration. It also applies rate limiting
        if any rate limit parameters are configured.

        Args:
            **kwargs: Additional parameters to pass to the LLM

        Returns:
            The instantiated LLM, potentially wrapped with rate limiting

        Raises:
            ProviderImportError: If provider dependencies are not installed
            ValueError: If required configuration is missing
            RuntimeError: If instantiation fails
        """
        # Get the chat class
        try:
            chat_class = self._get_chat_class()
        except ImportError as e:
            raise ProviderImportError(
                provider=self.provider.value, package=self._get_import_package()
            ) from e

        # Validate required configuration
        self._validate_config()

        # Get initialization parameters
        params = self._get_initialization_params(**kwargs)

        # Create LLM instance
        try:
            llm = chat_class(**params)
        except Exception as e:
            logger.exception(
                f"Failed to instantiate {self.provider.value} model: {e!s}"
            )
            raise RuntimeError(
                f"Failed to instantiate {self.provider.value} model: {e!s}"
            ) from e

        # Apply rate limiting if configured
        llm = self.apply_rate_limiting(llm)

        return llm

    def _validate_config(self) -> None:
        """Validate the configuration before instantiation.

        This method checks that all required configuration is present
        and valid. Subclasses can override to add provider-specific
        validation.

        Raises:
            ValueError: If configuration is invalid
        """
        # Most providers require an API key
        if self._requires_api_key() and not self.get_api_key():
            env_key = self._get_env_key_name()
            raise ValueError(
                f"{self.provider.value} API key is required. "
                f"Please set {env_key} environment variable or provide an API key."
            )

    def _requires_api_key(self) -> bool:
        """Check if this provider requires an API key.

        Returns:
            True if API key is required (default), False otherwise
        """
        # Most providers require API keys
        # Subclasses can override for local models
        return True

    @classmethod
    def get_models(cls) -> list[str]:
        """Get available models for this provider.

        This method attempts to retrieve the list of available models
        from the provider's API. Not all providers support this.

        Returns:
            List of available model names

        Raises:
            NotImplementedError: If provider doesn't support listing models
        """
        raise NotImplementedError(
            f"Provider {cls.__name__} does not support listing models"
        )

    def create_graph_transformer(self) -> Any:
        """Create an LLMGraphTransformer using this LLM.

        Returns:
            LLMGraphTransformer instance
        """
        from langchain_experimental.graph_transformers import LLMGraphTransformer

        llm = self.instantiate()
        return LLMGraphTransformer(llm=llm)
