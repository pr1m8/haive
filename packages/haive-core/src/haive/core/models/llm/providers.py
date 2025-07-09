"""
LLM Provider Implementations Module.

This module provides specific implementations for different LLM providers,
including OpenAI, Azure OpenAI, and others. Each provider has its own configuration
and engine class that builds on the base LLM structure while handling provider-specific
requirements and optimizations.

The provider implementations follow a consistent pattern:
1. A configuration class extending LLMEngineConfig
2. An engine class extending LLMEngine
3. Registration with the EngineRegistry

Typical usage example:
    ```python
    from haive.core.models.llm.providers import OpenAIConfig

    # Create a provider-specific configuration
    config = OpenAIConfig(
        name="gpt4",
        model="gpt-4",
        api_key="sk-..."
    )

    # Instantiate the engine
    engine = config.instantiate()

    # Generate text
    response = engine.generate("Explain quantum computing")
    ```
"""

from __future__ import annotations

from typing import Iterator, Optional, TypeVar

from pydantic import Field

from haive.core.models.llm.engine import EngineRegistry, LLMEngine, LLMEngineConfig

# Type variables for provider-specific types
TOpenAIConfig = TypeVar("TOpenAIConfig", bound="OpenAIConfig")
TAzureConfig = TypeVar("TAzureConfig", bound="AzureConfig")


class OpenAIConfig(LLMEngineConfig[TOpenAIConfig]):
    """
    Configuration for OpenAI LLM engines.

    This class provides configuration specific to OpenAI's API,
    including model selection, API credentials, and generation parameters.

    Attributes:
        model: OpenAI model identifier (e.g., "gpt-4", "gpt-3.5-turbo")
        api_key: OpenAI API key for authentication
        organization: Optional OpenAI organization ID for enterprise accounts
    """

    model: str = Field(..., description="OpenAI model identifier")
    api_key: str = Field(..., description="OpenAI API key")
    organization: Optional[str] = Field(None, description="OpenAI organization ID")

    def instantiate(self, **kwargs) -> "OpenAIEngine":
        """
        Create an OpenAI engine instance.

        This method instantiates an OpenAI-specific engine with the current
        configuration.

        Args:
            **kwargs: Additional instantiation parameters to override
                     configuration defaults

        Returns:
            A new OpenAI engine instance ready for text generation
        """
        return OpenAIEngine(self)


class OpenAIEngine(LLMEngine[OpenAIConfig]):
    """
    OpenAI LLM engine implementation.

    This class implements the LLM engine interface for OpenAI's API,
    providing text generation and streaming capabilities with appropriate
    error handling and resource management.

    The engine lazily initializes the underlying LangChain ChatOpenAI model
    when needed and handles prompt formatting and response parsing.
    """

    def __init__(self, config: OpenAIConfig):
        """
        Initialize the OpenAI engine.

        Args:
            config: Configuration for this OpenAI engine containing
                   model, API credentials, and generation parameters
        """
        super().__init__(config)
        self._model = None

    def initialize(self) -> None:
        """
        Initialize the OpenAI model.

        This method creates a LangChain ChatOpenAI instance with the configured
        parameters. It is called automatically on first use but can be called
        manually for pre-initialization.

        Raises:
            ImportError: If the langchain_openai package is not installed
            ValueError: If the API key is invalid or missing
            RuntimeError: If model initialization fails for other reasons
        """
        from langchain_openai import ChatOpenAI

        self._model = ChatOpenAI(
            model=self.config.model,
            openai_api_key=self.config.api_key,
            openai_organization=self.config.organization,
            **self.config.get_generation_config(),
        )

    def cleanup(self) -> None:
        """
        Clean up OpenAI resources.

        This method ensures any resources associated with the OpenAI model
        are properly released. Currently, no specific cleanup is needed
        for OpenAI models beyond releasing the reference.
        """
        self._model = None

    def generate(self, prompt: str, **kwargs) -> str:
        """
        Generate text using OpenAI's API.

        This method sends the prompt to OpenAI and returns the complete
        generated response as a string.

        Args:
            prompt: The input prompt text to send to the model
            **kwargs: Additional generation parameters to override the
                     configuration defaults, such as temperature or max_tokens

        Returns:
            The generated text response

        Raises:
            RuntimeError: If model initialization fails
            ValueError: If the prompt is invalid
        """
        if self._model is None:
            self.initialize()
        response = self._model.invoke(prompt, **kwargs)
        return response.content

    def generate_stream(self, prompt: str, **kwargs) -> Iterator[str]:
        """
        Generate text using OpenAI's API in streaming mode.

        This method returns an iterator that yields text chunks as they
        are generated by the model, enabling real-time display of responses.

        Args:
            prompt: The input prompt text to send to the model
            **kwargs: Additional generation parameters to override the
                     configuration defaults, such as temperature or max_tokens

        Yields:
            Text chunks as they are generated

        Raises:
            RuntimeError: If model initialization fails
            ValueError: If the prompt is invalid or if streaming is not
                       supported by the selected model
        """
        if self._model is None:
            self.initialize()
        for chunk in self._model.stream(prompt, **kwargs):
            yield chunk.content


class AzureConfig(LLMEngineConfig[TAzureConfig]):
    """
    Configuration for Azure OpenAI LLM engines.

    This class provides configuration specific to Azure's OpenAI API,
    including deployment settings, credentials, and API parameters.

    Azure OpenAI requires different parameters than standard OpenAI,
    including deployment names instead of model names, and specific
    endpoints for each Azure resource.

    Attributes:
        deployment_name: Azure deployment name for the model
        api_key: Azure API key for authentication
        api_base: Azure API base URL (endpoint)
        api_version: Azure API version string
    """

    deployment_name: str = Field(..., description="Azure deployment name")
    api_key: str = Field(..., description="Azure API key")
    api_base: str = Field(..., description="Azure API base URL")
    api_version: str = Field(default="2023-05-15", description="Azure API version")

    def instantiate(self, **kwargs) -> "AzureEngine":
        """
        Create an Azure engine instance.

        This method instantiates an Azure-specific engine with the current
        configuration.

        Args:
            **kwargs: Additional instantiation parameters to override
                     configuration defaults

        Returns:
            A new Azure engine instance ready for text generation
        """
        return AzureEngine(self)


class AzureEngine(LLMEngine[AzureConfig]):
    """
    Azure OpenAI LLM engine implementation.

    This class implements the LLM engine interface for Azure's OpenAI API,
    providing text generation and streaming capabilities with appropriate
    error handling and resource management.

    The engine lazily initializes the underlying LangChain AzureChatOpenAI model
    when needed and handles prompt formatting and response parsing.
    """

    def __init__(self, config: AzureConfig):
        """
        Initialize the Azure engine.

        Args:
            config: Configuration for this Azure engine containing
                   deployment name, API credentials, and generation parameters
        """
        super().__init__(config)
        self._model = None

    def initialize(self) -> None:
        """
        Initialize the Azure model.

        This method creates a LangChain AzureChatOpenAI instance with the configured
        parameters. It is called automatically on first use but can be called
        manually for pre-initialization.

        Raises:
            ImportError: If the langchain_openai package is not installed
            ValueError: If API credentials are invalid or missing
            RuntimeError: If model initialization fails for other reasons
        """
        from langchain_openai import AzureChatOpenAI

        self._model = AzureChatOpenAI(
            deployment_name=self.config.deployment_name,
            openai_api_key=self.config.api_key,
            openai_api_base=self.config.api_base,
            openai_api_version=self.config.api_version,
            **self.config.get_generation_config(),
        )

    def cleanup(self) -> None:
        """
        Clean up Azure resources.

        This method ensures any resources associated with the Azure model
        are properly released. Currently, no specific cleanup is needed
        for Azure models beyond releasing the reference.
        """
        self._model = None

    def generate(self, prompt: str, **kwargs) -> str:
        """
        Generate text using Azure's OpenAI API.

        This method sends the prompt to Azure OpenAI and returns the complete
        generated response as a string.

        Args:
            prompt: The input prompt text to send to the model
            **kwargs: Additional generation parameters to override the
                     configuration defaults, such as temperature or max_tokens

        Returns:
            The generated text response

        Raises:
            RuntimeError: If model initialization fails
            ValueError: If the prompt is invalid
        """
        if self._model is None:
            self.initialize()
        response = self._model.invoke(prompt, **kwargs)
        return response.content

    def generate_stream(self, prompt: str, **kwargs) -> Iterator[str]:
        """
        Generate text using Azure's OpenAI API in streaming mode.

        This method returns an iterator that yields text chunks as they
        are generated by the model, enabling real-time display of responses.

        Args:
            prompt: The input prompt text to send to the model
            **kwargs: Additional generation parameters to override the
                     configuration defaults, such as temperature or max_tokens

        Yields:
            Text chunks as they are generated

        Raises:
            RuntimeError: If model initialization fails
            ValueError: If the prompt is invalid or if streaming is not
                       supported by the selected deployment
        """
        if self._model is None:
            self.initialize()
        for chunk in self._model.stream(prompt, **kwargs):
            yield chunk.content


# Register the provider-specific engine types
EngineRegistry.register(OpenAIConfig, OpenAIEngine)
EngineRegistry.register(AzureConfig, AzureEngine)
