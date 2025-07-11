"""Base LLM configuration with model metadata support.

This module provides base classes and implementations for LLM providers
with support for model metadata, context windows, and capabilities.

.. deprecated:: 0.2.0
   This module is deprecated. Use :mod:`haive.core.models.llm.providers` instead.
   The individual provider configurations have been moved to separate modules
   for better organization and maintainability.
"""

import logging
import os
from collections.abc import Sequence
from typing import Any, Dict, List, Optional, Union

from langchain.chat_models.base import BaseChatModel
from langchain_core.messages import AnyMessage
from pydantic import BaseModel, Field, SecretStr, field_validator, model_validator

# Import the mixins
from haive.core.common.mixins.secure_config import SecureConfigMixin
from haive.core.models.llm.provider_types import LLMProvider
from haive.core.models.llm.rate_limiting_mixin import RateLimitingMixin
from haive.core.models.metadata_mixin import ModelMetadataMixin

logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)
# Try to import rich for enhanced debugging
try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.tree import Tree

    RICH_AVAILABLE = True
    console = Console()
except ImportError:
    RICH_AVAILABLE = False
    console = None

# Load environment variables from .env file if present
try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    logger.debug("dotenv module not available, skipping .env file loading")

# Set up LangChain cache if needed
try:
    # Define a relative cache path
    from pathlib import Path

    from langchain.globals import set_llm_cache
    from langchain_community.cache import SQLiteCache

    BASE_DIR = Path(__file__).resolve().parent.parent.parent
    CACHE_DIR = BASE_DIR / "lc_cache"
    CACHE_FILE = CACHE_DIR / ".langchain_cache.db"

    # Ensure cache directory exists
    CACHE_DIR.mkdir(parents=True, exist_ok=True)

    # Set cache
    set_llm_cache(SQLiteCache(database_path=str(CACHE_FILE)))
except ImportError:
    logger.debug("LangChain cache modules not available, skipping cache setup")


class LLMConfig(SecureConfigMixin, ModelMetadataMixin, RateLimitingMixin, BaseModel):
    """Base configuration for Language Model providers with security and metadata support.

    This class provides:
    1. Secure API key handling with environment variable fallbacks
    2. Model metadata access (context windows, capabilities, pricing)
    3. Common configuration parameters
    4. Graph transformation utilities
    5. Rate limiting capabilities via RateLimitingMixin

    All LLM configurations inherit from this base class, providing a consistent
    interface for configuration, instantiation, and management of language models
    from various providers.

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
        Direct instantiation (not recommended)::

            config = LLMConfig(
                provider=LLMProvider.OPENAI,
                model="gpt-4",
                api_key=SecretStr("your-key")
            )

        Using provider-specific config (recommended)::

            config = OpenAILLMConfig(
                model="gpt-4",
                temperature=0.7
            )
            llm = config.instantiate()
    """

    provider: LLMProvider = Field(description="The provider of the LLM.")
    model: str = Field(..., description="The model to be used, e.g., gpt-4.")
    name: str | None = Field(
        default=None, description="Friendly display name for this model."
    )
    api_key: SecretStr = Field(
        default_factory=lambda: SecretStr(""), description="API key for LLM provider."
    )
    cache_enabled: bool = Field(
        default=True, description="Enable or disable response caching."
    )
    cache_ttl: int | None = Field(
        default=300, description="Time-to-live for cache (in seconds)."
    )
    extra_params: dict[str, Any] | None = Field(
        default_factory=dict, description="Optional extra parameters."
    )
    debug: bool = Field(default=False, description="Enable detailed debug output.")

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
    model_alias: str | None = Field(default=None, description="Alias for the model.")

    @model_validator(mode="after")
    def set_default_name(self) -> "LLMConfig":
        """Set a default name for the model if not provided."""
        if self.name is None:
            # Default to model ID if no name provided
            self.name = self.model
        return self

    @model_validator(mode="after")
    def load_model_metadata(self) -> "LLMConfig":
        """Load and validate model metadata after initialization."""
        logger.debug(f"Loading metadata for {self.model} from {self.provider}")

        # Check model capabilities after initialization
        try:
            # Get metadata for validation and logging
            context_window = self.get_context_window()
            logger.debug(f"Model {self.model} context window: {context_window}")

            pricing = self.get_token_pricing()
            logger.debug(f"Model {self.model} pricing: {pricing}")

            # Display rich debug info if enabled
            if self.debug and RICH_AVAILABLE:
                self._display_debug_info()

        except Exception as e:
            logger.warning(f"Error loading model metadata: {e}")

        return self

    def _display_debug_info(self) -> None:
        """Display rich debug information about the model metadata."""
        if not RICH_AVAILABLE:
            logger.debug("Rich library not available for enhanced debugging")
            return

        raw_metadata = self._get_model_metadata()

        # Display metadata tree
        tree = Tree(f"[bold cyan]{self.model} Metadata[/bold cyan]")

        def _add_dict_to_tree(tree_node, data):
            if isinstance(data, dict):
                for key, value in sorted(data.items()):
                    if isinstance(value, dict):
                        branch = tree_node.add(f"[yellow]{key}[/yellow]")
                        _add_dict_to_tree(branch, value)
                    elif isinstance(value, list):
                        branch = tree_node.add(
                            f"[yellow]{key}[/yellow] (list, {len(value)} items)"
                        )
                        for i, item in enumerate(value):
                            if isinstance(item, dict | list):
                                sub_branch = branch.add(f"[blue]Item {i}[/blue]")
                                _add_dict_to_tree(sub_branch, item)
                            else:
                                branch.add(f"[blue]Item {i}:[/blue] {item}")
                    else:
                        tree_node.add(f"[green]{key}[/green]: {value}")

        _add_dict_to_tree(tree, raw_metadata)
        console.print(tree)

        # Display capabilities panel
        capabilities = {
            "vision": self.supports_vision,
            "function_calling": self.supports_function_calling,
            "parallel_function_calling": self.supports_parallel_function_calling,
            "system_messages": self.supports_system_messages,
            "tool_choice": self.supports_tool_choice,
            "response_schema": self.supports_response_schema,
            "web_search": self.supports_web_search,
            "pdf_input": self.supports_pdf_input,
            "audio_input": self.supports_audio_input,
            "audio_output": self.supports_audio_output,
            "prompt_caching": self.supports_prompt_caching,
            "native_streaming": self.supports_native_streaming,
            "reasoning": self.supports_reasoning,
        }

        capability_text = "\n".join(
            [
                f"  {'✓' if supported else '✗'} {capability.replace('_', ' ').title()}"
                for capability, supported in capabilities.items()
            ]
        )

        context_window = self.get_context_window()
        max_input = self.get_max_input_tokens()
        max_output = self.get_max_output_tokens()
        input_cost, output_cost = self.get_token_pricing()

        info_text = (
            f"Context Window: {context_window} tokens\n"
            f"Max Input: {max_input} tokens\n"
            f"Max Output: {max_output} tokens\n"
            f"Input cost per token: ${input_cost}\n"
            f"Output cost per token: ${output_cost}\n\n"
            f"Capabilities:\n{capability_text}"
        )

        # Check for deprecation
        deprecation_date = self.get_deprecation_date()
        if deprecation_date:
            info_text += f"\n\n⚠️ Model will be deprecated on: {deprecation_date}"

        console.print(Panel(info_text, title=f"[bold]{self.model} Summary[/bold]"))

    def format_metadata_for_display(self) -> dict[str, Any]:
        """Format metadata for structured display or comparison.

        Returns:
            Dictionary with formatted metadata
        """
        raw_metadata = self._get_model_metadata()
        context_window = self.get_context_window()
        max_input = self.get_max_input_tokens()
        max_output = self.get_max_output_tokens()
        input_cost, output_cost = self.get_token_pricing()
        deprecation_date = self.get_deprecation_date()

        capabilities = {
            "vision": self.supports_vision,
            "function_calling": self.supports_function_calling,
            "parallel_function_calling": self.supports_parallel_function_calling,
            "system_messages": self.supports_system_messages,
            "tool_choice": self.supports_tool_choice,
            "response_schema": self.supports_response_schema,
            "web_search": self.supports_web_search,
            "pdf_input": self.supports_pdf_input,
            "audio_input": self.supports_audio_input,
            "audio_output": self.supports_audio_output,
            "prompt_caching": self.supports_prompt_caching,
            "native_streaming": self.supports_native_streaming,
            "reasoning": self.supports_reasoning,
        }

        return {
            "name": self.name,
            "provider": (
                self.provider.value
                if hasattr(self.provider, "value")
                else str(self.provider)
            ),
            "model": self.model,
            "context_window": context_window,
            "max_input": max_input,
            "max_output": max_output,
            "input_cost": input_cost,
            "output_cost": output_cost,
            "capabilities": capabilities,
            "raw_metadata": raw_metadata,
            "deprecation_date": deprecation_date,
        }

    def instantiate(self, **kwargs) -> BaseChatModel:
        """Abstract method to instantiate the configured LLM.

        This method must be implemented by all provider-specific subclasses
        to handle the actual creation of the LLM instance.

        Args:
            **kwargs: Additional parameters to pass to the LLM constructor

        Returns:
            Instantiated LLM object ready for use

        Raises:
            NotImplementedError: If not overridden by a subclass
        """
        raise NotImplementedError("This method should be overridden in subclasses.")

    def create_graph_transformer(self) -> Any:
        """Creates an LLMGraphTransformer instance using the LLM."""
        from langchain_experimental.graph_transformers import LLMGraphTransformer

        llm = self.instantiate()
        return LLMGraphTransformer(llm=llm)

    def get_num_tokens_from_messages(
        self,
        messages: Sequence[AnyMessage],
        tools: Sequence[dict[str, Any]] | None = None,
    ) -> int:
        """Count tokens in a sequence of messages.

        This method instantiates the model temporarily to count tokens,
        preserving the serializability of the configuration object.

        Args:
            messages: Sequence of chat messages (HumanMessage, AIMessage, etc.)
            tools: Optional sequence of function schemas for tool calls

        Returns:
            Integer count of tokens across all messages

        Example:
            ```python
            from langchain_core.messages import HumanMessage, AIMessage

            config = OpenAILLMConfig(model="gpt-3.5-turbo")
            messages = [
                HumanMessage(content="Translate 'Hello' to French."),
                AIMessage(content="Bonjour"),
            ]

            token_count = config.get_num_tokens_from_messages(messages)
            print(f"Total tokens: {token_count}")
            ```
        """
        try:
            llm = self.instantiate()
            if hasattr(llm, "get_num_tokens_from_messages"):
                return llm.get_num_tokens_from_messages(messages, tools=tools)
            # Fallback: estimate based on string length if method not available
            total_content = ""
            for msg in messages:
                if hasattr(msg, "content"):
                    total_content += str(msg.content) + " "

            # Rough estimation: ~4 characters per token
            return len(total_content) // 4
        except Exception as e:
            logger.warning(f"Error counting tokens from messages: {e}")
            # Fallback estimation
            total_content = ""
            for msg in messages:
                if hasattr(msg, "content"):
                    total_content += str(msg.content) + " "
            return len(total_content) // 4

    def get_num_tokens(self, text: str) -> int:
        """Count tokens in a single text string.

        This method instantiates the model temporarily to count tokens,
        preserving the serializability of the configuration object.

        Args:
            text: Raw text string to count tokens for

        Returns:
            Integer count of tokens in the text

        Example:
            ```python
            config = OpenAILLMConfig(model="gpt-3.5-turbo")
            text = "Hello, world!"
            token_count = config.get_num_tokens(text)
            print(f"Tokens in text: {token_count}")
            ```
        """
        try:
            llm = self.instantiate()
            if hasattr(llm, "get_num_tokens"):
                return llm.get_num_tokens(text)
            # Fallback: rough estimation based on string length
            return len(text) // 4
        except Exception as e:
            logger.warning(f"Error counting tokens from text: {e}")
            # Fallback estimation: ~4 characters per token
            return len(text) // 4

    def estimate_cost_from_messages(
        self,
        messages: Sequence[AnyMessage],
        tools: Sequence[dict[str, Any]] | None = None,
        include_output_estimate: bool = True,
        estimated_output_tokens: int | None = None,
    ) -> dict[str, float]:
        """Estimate the cost of processing messages with this model.

        This method combines token counting with pricing metadata to estimate costs
        before making API calls, helping with budget management and cost optimization.

        Args:
            messages: Sequence of chat messages
            tools: Optional sequence of function schemas for tool calls
            include_output_estimate: Whether to include estimated output costs
            estimated_output_tokens: Manual override for output token estimation

        Returns:
            Dictionary with cost breakdown:
            {
                "input_tokens": int,
                "input_cost": float,
                "estimated_output_tokens": int,
                "estimated_output_cost": float,
                "total_estimated_cost": float
            }

        Example:
            ```python
            from langchain_core.messages import HumanMessage

            config = OpenAILLMConfig(model="gpt-4")
            messages = [HumanMessage(content="Write a short story about AI.")]

            cost_estimate = config.estimate_cost_from_messages(messages)
            print(f"Estimated total cost: ${cost_estimate['total_estimated_cost']:.6f}")
            ```
        """
        try:
            # Count input tokens
            input_tokens = self.get_num_tokens_from_messages(messages, tools=tools)

            # Get pricing information
            input_cost_per_token, output_cost_per_token = self.get_token_pricing()

            # Calculate input cost
            input_cost = input_tokens * input_cost_per_token

            # Estimate output tokens and cost
            estimated_output_tokens = estimated_output_tokens or (
                max(100, input_tokens // 4) if include_output_estimate else 0
            )
            estimated_output_cost = estimated_output_tokens * output_cost_per_token

            total_estimated_cost = input_cost + estimated_output_cost

            return {
                "input_tokens": input_tokens,
                "input_cost": input_cost,
                "estimated_output_tokens": estimated_output_tokens,
                "estimated_output_cost": estimated_output_cost,
                "total_estimated_cost": total_estimated_cost,
            }

        except Exception as e:
            logger.warning(f"Error estimating cost from messages: {e}")
            return {
                "input_tokens": 0,
                "input_cost": 0.0,
                "estimated_output_tokens": 0,
                "estimated_output_cost": 0.0,
                "total_estimated_cost": 0.0,
            }

    def estimate_cost_from_text(
        self,
        text: str,
        include_output_estimate: bool = True,
        estimated_output_tokens: int | None = None,
    ) -> dict[str, float]:
        """Estimate the cost of processing a single text string.

        Args:
            text: Raw text string to estimate cost for
            include_output_estimate: Whether to include estimated output costs
            estimated_output_tokens: Manual override for output token estimation

        Returns:
            Dictionary with cost breakdown (same format as estimate_cost_from_messages)

        Example:
            ```python
            config = AnthropicLLMConfig(model="claude-3-opus-20240229")
            text = "Explain quantum computing in simple terms."

            cost_estimate = config.estimate_cost_from_text(text)
            print(f"Input cost: ${cost_estimate['input_cost']:.6f}")
            ```
        """
        try:
            # Count input tokens
            input_tokens = self.get_num_tokens(text)

            # Get pricing information
            input_cost_per_token, output_cost_per_token = self.get_token_pricing()

            # Calculate input cost
            input_cost = input_tokens * input_cost_per_token

            # Estimate output tokens and cost
            estimated_output_tokens = estimated_output_tokens or (
                max(100, input_tokens // 4) if include_output_estimate else 0
            )
            estimated_output_cost = estimated_output_tokens * output_cost_per_token

            total_estimated_cost = input_cost + estimated_output_cost

            return {
                "input_tokens": input_tokens,
                "input_cost": input_cost,
                "estimated_output_tokens": estimated_output_tokens,
                "estimated_output_cost": estimated_output_cost,
                "total_estimated_cost": total_estimated_cost,
            }

        except Exception as e:
            logger.warning(f"Error estimating cost from text: {e}")
            return {
                "input_tokens": 0,
                "input_cost": 0.0,
                "estimated_output_tokens": 0,
                "estimated_output_cost": 0.0,
                "total_estimated_cost": 0.0,
            }

    def check_context_window_fit(
        self,
        messages: Sequence[AnyMessage],
        tools: Sequence[dict[str, Any]] | None = None,
        reserve_output_tokens: int = 1000,
    ) -> dict[str, bool | int]:
        """Check if messages fit within the model's context window.

        This method helps prevent "context length exceeded" errors by validating
        message length before making API calls.

        Args:
            messages: Sequence of chat messages to check
            tools: Optional sequence of function schemas for tool calls
            reserve_output_tokens: Number of tokens to reserve for output

        Returns:
            Dictionary with fit analysis:
            {
                "fits": bool,
                "input_tokens": int,
                "context_window": int,
                "available_tokens": int,
                "tokens_over_limit": int  # 0 if fits, positive if over
            }

        Example:
            ```python
            config = OpenAILLMConfig(model="gpt-3.5-turbo")

            # Check if messages fit
            fit_check = config.check_context_window_fit(messages)
            if not fit_check["fits"]:
                print(f"Messages exceed context window by {fit_check['tokens_over_limit']} tokens")
            ```
        """
        try:
            input_tokens = self.get_num_tokens_from_messages(messages, tools=tools)
            context_window = self.get_context_window()
            available_tokens = context_window - reserve_output_tokens

            fits = input_tokens <= available_tokens
            tokens_over_limit = max(0, input_tokens - available_tokens)

            return {
                "fits": fits,
                "input_tokens": input_tokens,
                "context_window": context_window,
                "available_tokens": available_tokens,
                "tokens_over_limit": tokens_over_limit,
            }

        except Exception as e:
            logger.warning(f"Error checking context window fit: {e}")
            return {
                "fits": False,
                "input_tokens": 0,
                "context_window": 0,
                "available_tokens": 0,
                "tokens_over_limit": 0,
            }


class AzureLLMConfig(LLMConfig):
    """Configuration specific to Azure OpenAI."""

    provider: LLMProvider = LLMProvider.AZURE
    model: str = Field(default="gpt-4o", description="Azure deployment name (model).")
    api_version: str = Field(
        default_factory=lambda: os.getenv(
            "AZURE_OPENAI_API_VERSION", "2024-02-15-preview"
        ),
        description="Azure API version.",
    )
    api_base: str = Field(
        default_factory=lambda: os.getenv("AZURE_OPENAI_ENDPOINT", ""),
        description="Azure API base URL.",
    )
    api_type: str = Field(
        default_factory=lambda: os.getenv("OPENAI_API_TYPE", "azure"),
        description="API type for Azure.",
    )
    # Direct loading of API key from environment
    api_key: SecretStr = Field(
        default_factory=lambda: SecretStr(os.getenv("AZURE_OPENAI_API_KEY", "")),
        description="API key for Azure OpenAI.",
    )

    @field_validator("api_version")
    @classmethod
    def load_api_version(cls, v: str) -> str:
        """Load API version from environment if not provided."""
        if not v:
            env_value = os.getenv("AZURE_OPENAI_API_VERSION")
            if env_value:
                return env_value
        return v

    @field_validator("api_base")
    @classmethod
    def load_api_base(cls, v: str) -> str:
        """Load API base from environment if not provided."""
        if not v:
            env_value = os.getenv("AZURE_OPENAI_ENDPOINT")
            if env_value:
                return env_value
        return v

    @field_validator("api_type")
    @classmethod
    def load_api_type(cls, v: str) -> str:
        """Load API type from environment if not provided."""
        if not v:
            env_value = os.getenv("OPENAI_API_TYPE")
            if env_value:
                return env_value
        return v

    @field_validator("api_key")
    @classmethod
    def load_api_key(cls, v: SecretStr) -> SecretStr:
        """Load API key from environment if not provided."""
        if v.get_secret_value() == "":
            env_value = os.getenv("AZURE_OPENAI_API_KEY", "")
            return SecretStr(env_value)
        return v

    def instantiate(self, **kwargs) -> Any:
        """Instantiate Azure OpenAI Chat model with robust error handling."""
        from langchain_openai import AzureChatOpenAI

        # Debug output
        logger.debug("Attempting to instantiate Azure OpenAI model:")
        logger.debug(f"- Model/deployment: {self.model}")
        logger.debug(f"- API version: {self.api_version}")
        logger.debug(f"- API base: {self.api_base}")
        logger.debug(f"- API type: {self.api_type}")
        logger.debug(f"- API key available: {'Yes' if self.get_api_key() else 'No'}")

        # Validate required parameters
        if not self.get_api_key():
            raise ValueError(
                "Azure OpenAI API key is required. "
                "Please set AZURE_OPENAI_API_KEY environment variable or provide an API key."
            )

        if not self.api_base:
            raise ValueError(
                "Azure OpenAI endpoint is required. "
                "Please set AZURE_OPENAI_ENDPOINT environment variable."
            )

        try:
            # Use the new parameter names
            return AzureChatOpenAI(
                deployment_name=self.model,
                api_key=self.get_api_key(),  # Changed from openai_api_key
                api_version=self.api_version,  # Changed from openai_api_version
                azure_endpoint=self.api_base,  # Changed from openai_api_base
                cache=self.cache_enabled,
                **(self.extra_params or {}),
                **kwargs,
            )
        except Exception as e:
            logger.exception(f"Failed to instantiate Azure OpenAI model: {e!s}")
            raise RuntimeError(
                f"Failed to instantiate Azure OpenAI model: {e!s}"
            ) from e


class OpenAILLMConfig(LLMConfig):
    """Configuration for OpenAI models."""

    provider: LLMProvider = LLMProvider.OPENAI
    api_key: SecretStr = Field(
        default_factory=lambda: SecretStr(os.getenv("OPENAI_API_KEY", "")),
        description="API key for OpenAI.",
    )

    @field_validator("api_key")
    @classmethod
    def load_api_key(cls, v: SecretStr) -> SecretStr:
        """Load API key from environment if not provided."""
        if v.get_secret_value() == "":
            env_value = os.getenv("OPENAI_API_KEY", "")
            return SecretStr(env_value)
        return v

    @classmethod
    def get_models(cls) -> list[str]:
        """Get all available OpenAI models."""
        from openai import OpenAI

        client = OpenAI()
        return client.models.list().data

    def instantiate(self, **kwargs) -> Any:
        """Instantiate OpenAI Chat model."""
        from langchain_openai import OpenAIChat

        # Validate API key
        if not self.get_api_key():
            raise ValueError(
                "OpenAI API key is required. "
                "Please set OPENAI_API_KEY environment variable or provide an API key."
            )

        try:
            return OpenAIChat(
                model_name=self.model,
                openai_api_key=self.get_api_key(),
                cache=self.cache_enabled,
                **(self.extra_params or {}),
                **kwargs,
            )
        except Exception as e:
            raise RuntimeError(f"Failed to instantiate OpenAI model: {e!s}") from e


class AnthropicLLMConfig(LLMConfig):
    """Configuration for Anthropic models."""

    provider: LLMProvider = LLMProvider.ANTHROPIC
    model: str = Field(
        default_factory=lambda: os.getenv("ANTHROPIC_MODEL", "claude-3-opus-20240229"),
        description="Anthropic model name.",
    )
    api_key: SecretStr = Field(
        default_factory=lambda: SecretStr(os.getenv("ANTHROPIC_API_KEY", "")),
        description="API key for Anthropic.",
    )

    @field_validator("model")
    @classmethod
    def load_model(cls, v: str) -> str:
        """Load model from environment if not provided."""
        if not v:
            env_value = os.getenv("ANTHROPIC_MODEL")
            if env_value:
                return env_value
        return v

    @field_validator("api_key")
    @classmethod
    def load_api_key(cls, v: SecretStr) -> SecretStr:
        """Load API key from environment if not provided."""
        if v.get_secret_value() == "":
            env_value = os.getenv("ANTHROPIC_API_KEY", "")
            return SecretStr(env_value)
        return v

    @classmethod
    def get_models(cls) -> list[str]:
        """Get all available Anthropic models."""
        from anthropic import Anthropic

        client = Anthropic()
        return client.models.list().data

    def instantiate(self, **kwargs) -> Any:
        """Instantiate Anthropic Chat model."""
        from langchain_anthropic import ChatAnthropic

        # Validate API key
        if not self.get_api_key():
            raise ValueError(
                "Anthropic API key is required. "
                "Please set ANTHROPIC_API_KEY environment variable or provide an API key."
            )

        try:
            return ChatAnthropic(
                model=self.model,
                api_key=self.get_api_key(),
                cache=self.cache_enabled,
                **(self.extra_params or {}),
                **kwargs,
            )
        except Exception as e:
            raise RuntimeError(f"Failed to instantiate Anthropic model: {e!s}") from e


class GeminiLLMConfig(LLMConfig):
    """Configuration for Google Gemini models."""

    provider: LLMProvider = LLMProvider.GEMINI
    model: str = Field(default="gemini-1.5-pro", description="Gemini model name.")
    api_key: SecretStr = Field(
        default_factory=lambda: SecretStr(os.getenv("GEMINI_API_KEY", "")),
        description="API key for Google Gemini.",
    )

    @field_validator("api_key")
    @classmethod
    def load_api_key(cls, v: SecretStr) -> SecretStr:
        """Load API key from environment if not provided."""
        if v.get_secret_value() == "":
            env_value = os.getenv("GEMINI_API_KEY", "")
            return SecretStr(env_value)
        return v

    def instantiate(self, **kwargs) -> Any:
        """Instantiate Google Gemini Chat model."""
        from langchain_google_genai import ChatGoogleGenerativeAI

        # Validate API key
        if not self.get_api_key():
            raise ValueError(
                "Google Gemini API key is required. "
                "Please set GEMINI_API_KEY environment variable or provide an API key."
            )

        try:
            return ChatGoogleGenerativeAI(
                model=self.model,
                api_key=self.get_api_key(),
                cache=self.cache_enabled,
                **(self.extra_params or {}),
                **kwargs,
            )
        except Exception as e:
            raise RuntimeError(f"Failed to instantiate Gemini model: {e!s}") from e


class DeepSeekLLMConfig(LLMConfig):
    """Configuration for DeepSeek models."""

    provider: LLMProvider = LLMProvider.DEEPSEEK
    model: str = Field(default="deepseek-chat", description="DeepSeek model name.")
    api_key: SecretStr = Field(
        default_factory=lambda: SecretStr(os.getenv("DEEPSEEK_API_KEY", "")),
        description="API key for DeepSeek.",
    )

    @classmethod
    def get_models(cls) -> list[str]:
        """Get all available DeepSeek models."""
        from deepseek import DeepSeekAPI

        client = DeepSeekAPI(api_key=os.getenv("DEEPSEEK_API_KEY", ""))
        return client.get_models()

    def instantiate(self, **kwargs) -> Any:
        """Instantiate DeepSeek Chat model."""
        from langchain_deepseek import ChatDeepSeek

        # Validate API key
        if not self.get_api_key():
            raise ValueError(
                "DeepSeek API key is required. "
                "Please set DEEPSEEK_API_KEY environment variable or provide an API key."
            )

        try:
            return ChatDeepSeek(
                model=self.model,
                api_key=self.get_api_key(),
                cache=self.cache_enabled,
                **(self.extra_params or {}),
                **kwargs,
            )
        except Exception as e:
            raise RuntimeError(f"Failed to instantiate DeepSeek model: {e!s}") from e


class MistralLLMConfig(LLMConfig):
    """Configuration for Mistral models."""

    provider: LLMProvider = LLMProvider.MISTRALAI
    model: str = Field(
        default="mistral-large-latest", description="Mistral model name."
    )
    api_key: SecretStr = Field(
        default_factory=lambda: SecretStr(os.getenv("MISTRAL_API_KEY", "")),
        description="API key for Mistral.",
    )

    @field_validator("api_key")
    @classmethod
    def load_api_key(cls, v: SecretStr) -> SecretStr:
        """Load API key from environment if not provided."""
        if v.get_secret_value() == "":
            env_value = os.getenv("MISTRAL_API_KEY", "")
            return SecretStr(env_value)
        return v

    @classmethod
    def get_models(cls) -> list[str]:
        """Get all available Mistral models."""
        from mistralai import Mistral

        client = Mistral(api_key=os.getenv("MISTRAL_API_KEY", ""))
        return client.models.list()

    def instantiate(self, **kwargs) -> Any:
        """Instantiate Mistral Chat model."""
        from langchain_mistralai import ChatMistralAI

        # Validate API key
        if not self.get_api_key():
            raise ValueError(
                "Mistral API key is required. "
                "Please set MISTRAL_API_KEY environment variable or provide an API key."
            )

        try:
            return ChatMistralAI(
                model=self.model,
                api_key=self.get_api_key(),
                cache=self.cache_enabled,
                **(self.extra_params or {}),
                **kwargs,
            )
        except Exception as e:
            raise RuntimeError(f"Failed to instantiate Mistral model: {e!s}") from e


class GroqLLMConfig(LLMConfig):
    """Configuration for Groq models."""

    provider: LLMProvider = LLMProvider.GROQ
    model: str = Field(default="llama3-70b-8192", description="Groq model name.")
    api_key: SecretStr = Field(
        default_factory=lambda: SecretStr(os.getenv("GROQ_API_KEY", "")),
        description="API key for Groq.",
    )

    @field_validator("api_key")
    @classmethod
    def load_api_key(cls, v: SecretStr) -> SecretStr:
        """Load API key from environment if not provided."""
        if v.get_secret_value() == "":
            env_value = os.getenv("GROQ_API_KEY", "")
            return SecretStr(env_value)
        return v

    def instantiate(self, **kwargs) -> Any:
        """Instantiate Groq Chat model."""
        from langchain_groq import ChatGroq

        # Validate API key
        if not self.get_api_key():
            raise ValueError(
                "Groq API key is required. "
                "Please set GROQ_API_KEY environment variable or provide an API key."
            )

        try:
            return ChatGroq(
                model=self.model,
                api_key=self.get_api_key(),
                cache=self.cache_enabled,
                **(self.extra_params or {}),
                **kwargs,
            )
        except Exception as e:
            raise RuntimeError(f"Failed to instantiate Groq model: {e!s}") from e


class CohereLLMConfig(LLMConfig):
    """Configuration for Cohere models."""

    provider: LLMProvider = LLMProvider.COHERE
    model: str = Field(default="command", description="Cohere model name.")
    api_key: SecretStr = Field(
        default_factory=lambda: SecretStr(os.getenv("COHERE_API_KEY", "")),
        description="API key for Cohere.",
    )

    @field_validator("api_key")
    @classmethod
    def load_api_key(cls, v: SecretStr) -> SecretStr:
        """Load API key from environment if not provided."""
        if v.get_secret_value() == "":
            env_value = os.getenv("COHERE_API_KEY", "")
            return SecretStr(env_value)
        return v

    def instantiate(self, **kwargs) -> Any:
        """Instantiate Cohere Chat model."""
        from langchain_cohere import ChatCohere

        # Validate API key
        if not self.get_api_key():
            raise ValueError(
                "Cohere API key is required. "
                "Please set COHERE_API_KEY environment variable or provide an API key."
            )

        try:
            return ChatCohere(
                model=self.model,
                api_key=self.get_api_key(),
                cache=self.cache_enabled,
                **(self.extra_params or {}),
                **kwargs,
            )
        except Exception as e:
            raise RuntimeError(f"Failed to instantiate Cohere model: {e!s}") from e


class TogetherAILLMConfig(LLMConfig):
    """Configuration for Together AI models."""

    provider: LLMProvider = LLMProvider.TOGETHER_AI
    model: str = Field(
        default="meta-llama/Llama-3-70b-chat-hf", description="Together AI model name."
    )
    api_key: SecretStr = Field(
        default_factory=lambda: SecretStr(os.getenv("TOGETHER_AI_API_KEY", "")),
        description="API key for Together AI.",
    )

    @field_validator("api_key")
    @classmethod
    def load_api_key(cls, v: SecretStr) -> SecretStr:
        """Load API key from environment if not provided."""
        if v.get_secret_value() == "":
            env_value = os.getenv("TOGETHER_AI_API_KEY", "")
            return SecretStr(env_value)
        return v

    def instantiate(self, **kwargs) -> Any:
        """Instantiate Together AI Chat model."""
        from langchain_together import ChatTogether

        # Validate API key
        if not self.get_api_key():
            raise ValueError(
                "Together AI API key is required. "
                "Please set TOGETHER_AI_API_KEY environment variable or provide an API key."
            )

        try:
            return ChatTogether(
                model=self.model,
                api_key=self.get_api_key(),
                cache=self.cache_enabled,
                **(self.extra_params or {}),
                **kwargs,
            )
        except Exception as e:
            raise RuntimeError(f"Failed to instantiate Together AI model: {e!s}") from e


class FireworksAILLMConfig(LLMConfig):
    """Configuration for Fireworks AI models."""

    provider: LLMProvider = LLMProvider.FIREWORKS_AI
    model: str = Field(
        default="fireworks/llama-v3-70b-chat", description="Fireworks AI model name."
    )
    api_key: SecretStr = Field(
        default_factory=lambda: SecretStr(os.getenv("FIREWORKS_AI_API_KEY", "")),
        description="API key for Fireworks AI.",
    )

    @field_validator("api_key")
    @classmethod
    def load_api_key(cls, v: SecretStr) -> SecretStr:
        """Load API key from environment if not provided."""
        if v.get_secret_value() == "":
            env_value = os.getenv("FIREWORKS_AI_API_KEY", "")
            return SecretStr(env_value)
        return v

    def instantiate(self, **kwargs) -> Any:
        """Instantiate Fireworks AI Chat model."""
        from langchain_fireworks import ChatFireworks

        # Validate API key
        if not self.get_api_key():
            raise ValueError(
                "Fireworks AI API key is required. "
                "Please set FIREWORKS_AI_API_KEY environment variable or provide an API key."
            )

        try:
            return ChatFireworks(
                model=self.model,
                api_key=self.get_api_key(),
                cache=self.cache_enabled,
                **(self.extra_params or {}),
                **kwargs,
            )
        except Exception as e:
            raise RuntimeError(
                f"Failed to instantiate Fireworks AI model: {e!s}"
            ) from e


class PerplexityLLMConfig(LLMConfig):
    """Configuration for Perplexity AI models."""

    provider: LLMProvider = LLMProvider.PERPLEXITY
    model: str = Field(
        default="sonar-medium-online", description="Perplexity model name."
    )
    api_key: SecretStr = Field(
        default_factory=lambda: SecretStr(os.getenv("PERPLEXITY_API_KEY", "")),
        description="API key for Perplexity AI.",
    )

    @field_validator("api_key")
    @classmethod
    def load_api_key(cls, v: SecretStr) -> SecretStr:
        """Load API key from environment if not provided."""
        if v.get_secret_value() == "":
            env_value = os.getenv("PERPLEXITY_API_KEY", "")
            return SecretStr(env_value)
        return v

    def instantiate(self, **kwargs) -> Any:
        """Instantiate Perplexity AI Chat model."""
        from langchain_community.chat_models import ChatPerplexity

        # Validate API key
        if not self.get_api_key():
            raise ValueError(
                "Perplexity API key is required. "
                "Please set PERPLEXITY_API_KEY environment variable or provide an API key."
            )

        try:
            return ChatPerplexity(
                model=self.model,
                api_key=self.get_api_key(),
                cache=self.cache_enabled,
                **(self.extra_params or {}),
                **kwargs,
            )
        except Exception as e:
            raise RuntimeError(f"Failed to instantiate Perplexity model: {e!s}") from e


class HuggingFaceLLMConfig(LLMConfig):
    """Configuration for Hugging Face models."""

    provider: LLMProvider = LLMProvider.HUGGINGFACE
    model: str = Field(..., description="Model ID on Hugging Face Hub.")
    api_key: SecretStr = Field(
        default_factory=lambda: SecretStr(os.getenv("HUGGING_FACE_API_KEY", "")),
        description="API key for Hugging Face.",
    )
    endpoint_url: str | None = Field(
        default=None, description="Optional Hugging Face Inference Endpoint URL"
    )

    @field_validator("api_key")
    @classmethod
    def load_api_key(cls, v: SecretStr) -> SecretStr:
        """Load API key from environment if not provided."""
        if v.get_secret_value() == "":
            env_value = os.getenv("HUGGING_FACE_API_KEY", "")
            return SecretStr(env_value)
        return v

    def instantiate(self, **kwargs) -> Any:
        """Instantiate Hugging Face model."""
        try:
            from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
        except ImportError:
            raise RuntimeError(
                "langchain-huggingface is not installed. "
                "Please install it with 'pip install langchain-huggingface'"
            )
        # Validate API key
        if not self.get_api_key():
            raise ValueError(
                "Hugging Face API key is required. "
                "Please set HUGGING_FACE_API_KEY environment variable or provide an API key."
            )

        try:
            # Use HuggingFace Hub directly or Inference endpoint based on configuration
            if self.endpoint_url:
                from langchain_huggingface import ChatHuggingFace

                return ChatHuggingFace(
                    model=self.model,
                    api_key=self.get_api_key(),
                    endpoint_url=self.endpoint_url,
                    cache=self.cache_enabled,
                    **(self.extra_params or {}),
                    **kwargs,
                )
            from langchain_huggingface import HuggingFaceEndpoint

            return HuggingFaceEndpoint(
                repo_id=self.model,
                huggingfacehub_api_token=self.get_api_key(),
                cache=self.cache_enabled,
                **(self.extra_params or {}),
                **kwargs,
            )
        except Exception as e:
            raise RuntimeError(
                f"Failed to instantiate Hugging Face model: {e!s}"
            ) from e


class AI21LLMConfig(LLMConfig):
    """Configuration for AI21 models."""

    provider: LLMProvider = LLMProvider.AI21
    model: str = Field(default="j2-ultra", description="AI21 model name.")
    api_key: SecretStr = Field(
        default_factory=lambda: SecretStr(os.getenv("AI21_API_KEY", "")),
        description="API key for AI21.",
    )

    @field_validator("api_key")
    @classmethod
    def load_api_key(cls, v: SecretStr) -> SecretStr:
        """Load API key from environment if not provided."""
        if v.get_secret_value() == "":
            env_value = os.getenv("AI21_API_KEY", "")
            return SecretStr(env_value)
        return v

    def instantiate(self, **kwargs) -> Any:
        """Instantiate AI21 Chat model."""
        try:
            from langchain_ai21 import ChatAI21
        except ImportError:
            raise RuntimeError(
                "langchain-ai21 is not installed. "
                "Please install it with 'pip install langchain-ai21'"
            )

        # Validate API key
        if not self.get_api_key():
            raise ValueError(
                "AI21 API key is required. "
                "Please set AI21_API_KEY environment variable or provide an API key."
            )

        try:
            return ChatAI21(
                model=self.model,
                api_key=self.get_api_key(),
                cache=self.cache_enabled,
                **(self.extra_params or {}),
                **kwargs,
            )
        except Exception as e:
            raise RuntimeError(f"Failed to instantiate AI21 model: {e!s}") from e


class AlephAlphaLLMConfig(LLMConfig):
    """Configuration for Aleph Alpha models."""

    provider: LLMProvider = LLMProvider.ALEPH_ALPHA
    model: str = Field(default="luminous-base", description="Aleph Alpha model name.")
    api_key: SecretStr = Field(
        default_factory=lambda: SecretStr(os.getenv("ALEPH_ALPHA_API_KEY", "")),
        description="API key for Aleph Alpha.",
    )

    @field_validator("api_key")
    @classmethod
    def load_api_key(cls, v: SecretStr) -> SecretStr:
        """Load API key from environment if not provided."""
        if v.get_secret_value() == "":
            env_value = os.getenv("ALEPH_ALPHA_API_KEY", "")
            return SecretStr(env_value)
        return v

    def instantiate(self, **kwargs) -> Any:
        """Instantiate Aleph Alpha Chat model."""
        from langchain_community.chat_models import ChatAlephAlpha

        # Validate API key
        if not self.get_api_key():
            raise ValueError(
                "Aleph Alpha API key is required. "
                "Please set ALEPH_ALPHA_API_KEY environment variable or provide an API key."
            )

        try:
            return ChatAlephAlpha(
                model=self.model,
                aleph_alpha_api_key=self.get_api_key(),
                cache=self.cache_enabled,
                **(self.extra_params or {}),
                **kwargs,
            )
        except Exception as e:
            raise RuntimeError(f"Failed to instantiate Aleph Alpha model: {e!s}") from e


class GooseAILLMConfig(LLMConfig):
    """Configuration for GooseAI models."""

    provider: LLMProvider = LLMProvider.GOOSEAI
    model: str = Field(default="gpt-neo-20b", description="GooseAI model name.")
    api_key: SecretStr = Field(
        default_factory=lambda: SecretStr(os.getenv("GOOSEAI_API_KEY", "")),
        description="API key for GooseAI.",
    )

    @field_validator("api_key")
    @classmethod
    def load_api_key(cls, v: SecretStr) -> SecretStr:
        """Load API key from environment if not provided."""
        if v.get_secret_value() == "":
            env_value = os.getenv("GOOSEAI_API_KEY", "")
            return SecretStr(env_value)
        return v

    def instantiate(self, **kwargs) -> Any:
        """Instantiate GooseAI Chat model."""
        try:
            from langchain_community.chat_models import ChatGooseAI
        except ImportError:
            raise RuntimeError(
                "langchain-community is not installed. "
                "Please install it with 'pip install langchain-community'"
            )

        # Validate API key
        if not self.get_api_key():
            raise ValueError(
                "GooseAI API key is required. "
                "Please set GOOSEAI_API_KEY environment variable or provide an API key."
            )

        try:
            return ChatGooseAI(
                model=self.model,
                gooseai_api_key=self.get_api_key(),
                cache=self.cache_enabled,
                **(self.extra_params or {}),
                **kwargs,
            )
        except Exception as e:
            raise RuntimeError(f"Failed to instantiate GooseAI model: {e!s}") from e


class MosaicMLLLMConfig(LLMConfig):
    """Configuration for MosaicML models."""

    provider: LLMProvider = LLMProvider.MOSAICML
    model: str = Field(default="mpt-7b", description="MosaicML model name.")
    api_key: SecretStr = Field(
        default_factory=lambda: SecretStr(os.getenv("MOSAICML_API_KEY", "")),
        description="API key for MosaicML.",
    )

    @field_validator("api_key")
    @classmethod
    def load_api_key(cls, v: SecretStr) -> SecretStr:
        """Load API key from environment if not provided."""
        if v.get_secret_value() == "":
            env_value = os.getenv("MOSAICML_API_KEY", "")
            return SecretStr(env_value)
        return v

    def instantiate(self, **kwargs) -> Any:
        """Instantiate MosaicML Chat model."""
        from langchain_community.chat_models import ChatMosaicML

        # Validate API key
        if not self.get_api_key():
            raise ValueError(
                "MosaicML API key is required. "
                "Please set MOSAICML_API_KEY environment variable or provide an API key."
            )

        try:
            return ChatMosaicML(
                model=self.model,
                mosaicml_api_key=self.get_api_key(),
                cache=self.cache_enabled,
                **(self.extra_params or {}),
                **kwargs,
            )
        except Exception as e:
            raise RuntimeError(f"Failed to instantiate MosaicML model: {e!s}") from e


class NLPCloudLLMConfig(LLMConfig):
    """Configuration for NLP Cloud models."""

    provider: LLMProvider = LLMProvider.NLP_CLOUD
    model: str = Field(
        default="finetuned-gpt-neox-20b", description="NLP Cloud model name."
    )
    api_key: SecretStr = Field(
        default_factory=lambda: SecretStr(os.getenv("NLP_CLOUD_API_KEY", "")),
        description="API key for NLP Cloud.",
    )

    @field_validator("api_key")
    @classmethod
    def load_api_key(cls, v: SecretStr) -> SecretStr:
        """Load API key from environment if not provided."""
        if v.get_secret_value() == "":
            env_value = os.getenv("NLP_CLOUD_API_KEY", "")
            return SecretStr(env_value)
        return v

    def instantiate(self, **kwargs) -> Any:
        """Instantiate NLP Cloud Chat model."""
        try:
            from langchain_community.llms import ChatNLPCloud
        except ImportError:
            raise RuntimeError(
                "langchain-nlpcloud is not installed. "
                "Please install it with 'pip install langchain-nlpcloud'"
            )

        # Validate API key
        if not self.get_api_key():
            raise ValueError(
                "NLP Cloud API key is required. "
                "Please set NLP_CLOUD_API_KEY environment variable or provide an API key."
            )

        try:
            return ChatNLPCloud(
                model=self.model,
                api_key=self.get_api_key(),
                cache=self.cache_enabled,
                **(self.extra_params or {}),
                **kwargs,
            )
        except Exception as e:
            raise RuntimeError(f"Failed to instantiate NLP Cloud model: {e!s}") from e


class OpenLMLLMConfig(LLMConfig):
    """Configuration for OpenLM models."""

    provider: LLMProvider = LLMProvider.OPENLM
    model: str = Field(default="open-llama-3b", description="OpenLM model name.")
    api_key: SecretStr = Field(
        default_factory=lambda: SecretStr(os.getenv("OPENLM_API_KEY", "")),
        description="API key for OpenLM.",
    )

    @field_validator("api_key")
    @classmethod
    def load_api_key(cls, v: SecretStr) -> SecretStr:
        """Load API key from environment if not provided."""
        if v.get_secret_value() == "":
            env_value = os.getenv("OPENLM_API_KEY", "")
            return SecretStr(env_value)
        return v

    def instantiate(self, **kwargs) -> Any:
        """Instantiate OpenLM Chat model."""
        from langchain_community.chat_models import ChatOpenLM

        # Validate API key
        if not self.get_api_key():
            raise ValueError(
                "OpenLM API key is required. "
                "Please set OPENLM_API_KEY environment variable or provide an API key."
            )

        try:
            return ChatOpenLM(
                model=self.model,
                openlm_api_key=self.get_api_key(),
                cache=self.cache_enabled,
                **(self.extra_params or {}),
                **kwargs,
            )
        except Exception as e:
            raise RuntimeError(f"Failed to instantiate OpenLM model: {e!s}") from e


class PetalsLLMConfig(LLMConfig):
    """Configuration for Petals distributed models."""

    provider: LLMProvider = LLMProvider.PETALS
    model: str = Field(default="bigscience/bloom", description="Petals model name.")
    # No API key needed for Petals distributed inference

    def instantiate(self, **kwargs) -> Any:
        """Instantiate Petals Chat model."""
        from langchain_community.chat_models import ChatPetals

        try:
            return ChatPetals(
                model=self.model,
                cache=self.cache_enabled,
                **(self.extra_params or {}),
                **kwargs,
            )
        except Exception as e:
            raise RuntimeError(f"Failed to instantiate Petals model: {e!s}") from e


class ReplicateLLMConfig(LLMConfig):
    """Configuration for Replicate models."""

    provider: LLMProvider = LLMProvider.REPLICATE
    model: str = Field(
        default="meta/llama-2-70b-chat",
        description="Replicate model name (org/model:version).",
    )
    api_key: SecretStr = Field(
        default=SecretStr(""),
        description="API key for Replicate.",
    )

    @field_validator("api_key")
    @classmethod
    def load_api_key(cls, v: SecretStr) -> SecretStr:
        """Load API key from environment if not provided."""
        if v.get_secret_value() == "":
            env_value = os.getenv("REPLICATE_API_KEY", "")
            return SecretStr(env_value)
        return v

    def instantiate(self, **kwargs) -> Any:
        """Instantiate Replicate Chat model."""
        from langchain_community.chat_models import ChatReplicate

        # Validate API key
        if not self.get_api_key():
            raise ValueError(
                "Replicate API key is required. "
                "Please set REPLICATE_API_KEY environment variable or provide an API key."
            )

        try:
            return ChatReplicate(
                model=self.model,
                replicate_api_token=self.get_api_key(),
                cache=self.cache_enabled,
                **(self.extra_params or {}),
                **kwargs,
            )
        except Exception as e:
            raise RuntimeError(f"Failed to instantiate Replicate model: {e!s}") from e


class VertexAILLMConfig(LLMConfig):
    """Configuration for Google Vertex AI models."""

    provider: LLMProvider = LLMProvider.VERTEX_AI
    model: str = Field(default="gemini-1.5-pro", description="Vertex AI model name.")
    project: str | None = Field(default="", description="Google Cloud Project ID.")
    location: str = Field(
        default="us-central1", description="Google Cloud region/location."
    )
    # No direct API key for Vertex AI - uses Google Cloud auth

    @field_validator("project")
    @classmethod
    def load_project(cls, v: str) -> str:
        """Load project from environment if not provided."""
        if not v:
            env_value = os.getenv("GOOGLE_CLOUD_PROJECT", "")
            return env_value
        return v

    def instantiate(self, **kwargs) -> Any:
        """Instantiate Google Vertex AI Chat model."""
        try:
            from langchain_google_vertexai import ChatVertexAI
        except ImportError:
            raise RuntimeError(
                "langchain-google-vertexai is not installed. "
                "Please install it with 'pip install langchain-google-vertexai'"
            )

        # Validate project
        if not self.project:
            raise ValueError(
                "Google Cloud Project ID is required. "
                "Please set GOOGLE_CLOUD_PROJECT environment variable or provide a project ID."
            )

        try:
            return ChatVertexAI(
                model_name=self.model,
                project=self.project,
                location=self.location,
                cache=self.cache_enabled,
                **(self.extra_params or {}),
                **kwargs,
            )
        except Exception as e:
            raise RuntimeError(f"Failed to instantiate Vertex AI model: {e!s}") from e


class BedrockLLMConfig(LLMConfig):
    """Configuration for AWS Bedrock models.

    AWS Bedrock provides access to foundation models from various providers
    including Anthropic, AI21, Cohere, and Amazon's own models.

    Attributes:
        model_id: The Bedrock model ID (e.g., 'anthropic.claude-v2')
        region_name: AWS region for Bedrock service
        aws_access_key_id: AWS access key (optional, uses AWS credentials chain)
        aws_secret_access_key: AWS secret key (optional, uses AWS credentials chain)
    """

    provider: LLMProvider = LLMProvider.BEDROCK
    model: str = Field(
        default="anthropic.claude-v2", description="Bedrock model ID.", alias="model_id"
    )
    region_name: str = Field(
        default_factory=lambda: os.getenv("AWS_DEFAULT_REGION", "us-east-1"),
        description="AWS region name.",
    )
    aws_access_key_id: SecretStr | None = Field(
        default_factory=lambda: SecretStr(os.getenv("AWS_ACCESS_KEY_ID", "")),
        description="AWS access key ID.",
    )
    aws_secret_access_key: SecretStr | None = Field(
        default_factory=lambda: SecretStr(os.getenv("AWS_SECRET_ACCESS_KEY", "")),
        description="AWS secret access key.",
    )

    def instantiate(self, **kwargs) -> Any:
        """Instantiate AWS Bedrock Chat model."""
        try:
            from langchain_aws import ChatBedrock
        except ImportError:
            raise RuntimeError(
                "langchain-aws is not installed. "
                "Please install it with 'pip install langchain-aws'"
            )

        try:
            params = {
                "model_id": self.model,
                "region_name": self.region_name,
                **(self.extra_params or {}),
                **kwargs,
            }

            # Only add credentials if explicitly provided
            if self.aws_access_key_id and self.aws_access_key_id.get_secret_value():
                params["aws_access_key_id"] = self.aws_access_key_id.get_secret_value()
            if (
                self.aws_secret_access_key
                and self.aws_secret_access_key.get_secret_value()
            ):
                params["aws_secret_access_key"] = (
                    self.aws_secret_access_key.get_secret_value()
                )

            return ChatBedrock(**params)
        except Exception as e:
            raise RuntimeError(f"Failed to instantiate Bedrock model: {e!s}") from e


class NVIDIALLMConfig(LLMConfig):
    """Configuration for NVIDIA AI Endpoints models."""

    provider: LLMProvider = LLMProvider.NVIDIA
    model: str = Field(
        default="meta/llama3-70b-instruct", description="NVIDIA model name."
    )
    api_key: SecretStr = Field(
        default_factory=lambda: SecretStr(os.getenv("NVIDIA_API_KEY", "")),
        description="API key for NVIDIA AI Endpoints.",
    )
    base_url: str | None = Field(
        default="https://api.nvcf.nvidia.com/v2/nvcf/pexec/functions",
        description="NVIDIA API base URL.",
    )

    def instantiate(self, **kwargs) -> Any:
        """Instantiate NVIDIA Chat model."""
        try:
            from langchain_nvidia_ai_endpoints import ChatNVIDIA
        except ImportError:
            raise RuntimeError(
                "langchain-nvidia-ai-endpoints is not installed. "
                "Please install it with 'pip install langchain-nvidia-ai-endpoints'"
            )

        if not self.get_api_key():
            raise ValueError(
                "NVIDIA API key is required. "
                "Please set NVIDIA_API_KEY environment variable or provide an API key."
            )

        try:
            return ChatNVIDIA(
                model=self.model,
                api_key=self.get_api_key(),
                base_url=self.base_url,
                **(self.extra_params or {}),
                **kwargs,
            )
        except Exception as e:
            raise RuntimeError(f"Failed to instantiate NVIDIA model: {e!s}") from e


class OllamaLLMConfig(LLMConfig):
    """Configuration for Ollama local models."""

    provider: LLMProvider = LLMProvider.OLLAMA
    model: str = Field(default="llama3", description="Ollama model name.")
    base_url: str = Field(
        default_factory=lambda: os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
        description="Ollama server URL.",
    )
    # No API key needed for local Ollama

    def instantiate(self, **kwargs) -> Any:
        """Instantiate Ollama Chat model."""
        try:
            from langchain_ollama import ChatOllama
        except ImportError:
            raise RuntimeError(
                "langchain-ollama is not installed. "
                "Please install it with 'pip install langchain-ollama'"
            )

        try:
            return ChatOllama(
                model=self.model,
                base_url=self.base_url,
                **(self.extra_params or {}),
                **kwargs,
            )
        except Exception as e:
            raise RuntimeError(f"Failed to instantiate Ollama model: {e!s}") from e


class LlamaCppLLMConfig(LLMConfig):
    """Configuration for Llama.cpp local models."""

    provider: LLMProvider = LLMProvider.LLAMACPP
    model: str = Field(description="Path to the GGUF model file.", alias="model_path")
    n_ctx: int = Field(default=2048, description="Context window size.")
    n_threads: int | None = Field(default=None, description="Number of threads to use.")
    n_gpu_layers: int = Field(
        default=0, description="Number of layers to offload to GPU."
    )

    def instantiate(self, **kwargs) -> Any:
        """Instantiate Llama.cpp Chat model."""
        try:
            from langchain_community.chat_models import ChatLlamaCpp
        except ImportError:
            raise RuntimeError(
                "langchain-community is not installed. "
                "Please install it with 'pip install langchain-community'"
            )

        try:
            params = {
                "model_path": self.model,
                "n_ctx": self.n_ctx,
                "n_gpu_layers": self.n_gpu_layers,
                **(self.extra_params or {}),
                **kwargs,
            }

            if self.n_threads is not None:
                params["n_threads"] = self.n_threads

            return ChatLlamaCpp(**params)
        except Exception as e:
            raise RuntimeError(f"Failed to instantiate Llama.cpp model: {e!s}") from e


class UpstageLLMConfig(LLMConfig):
    """Configuration for Upstage models."""

    provider: LLMProvider = LLMProvider.UPSTAGE
    model: str = Field(default="solar-1-mini-chat", description="Upstage model name.")
    api_key: SecretStr = Field(
        default_factory=lambda: SecretStr(os.getenv("UPSTAGE_API_KEY", "")),
        description="API key for Upstage.",
    )

    def instantiate(self, **kwargs) -> Any:
        """Instantiate Upstage Chat model."""
        try:
            from langchain_upstage import ChatUpstage
        except ImportError:
            raise RuntimeError(
                "langchain-upstage is not installed. "
                "Please install it with 'pip install langchain-upstage'"
            )

        if not self.get_api_key():
            raise ValueError(
                "Upstage API key is required. "
                "Please set UPSTAGE_API_KEY environment variable or provide an API key."
            )

        try:
            return ChatUpstage(
                model=self.model,
                api_key=self.get_api_key(),
                **(self.extra_params or {}),
                **kwargs,
            )
        except Exception as e:
            raise RuntimeError(f"Failed to instantiate Upstage model: {e!s}") from e


class DatabricksLLMConfig(LLMConfig):
    """Configuration for Databricks models."""

    provider: LLMProvider = LLMProvider.DATABRICKS
    model: str = Field(
        default="databricks-dbrx-instruct",
        description="Databricks model name or endpoint.",
    )
    api_key: SecretStr = Field(
        default_factory=lambda: SecretStr(os.getenv("DATABRICKS_API_KEY", "")),
        description="Databricks API key.",
        alias="databricks_api_key",
    )
    host: str = Field(
        default_factory=lambda: os.getenv("DATABRICKS_HOST", ""),
        description="Databricks workspace URL.",
    )

    def instantiate(self, **kwargs) -> Any:
        """Instantiate Databricks Chat model."""
        try:
            from langchain_databricks import ChatDatabricks
        except ImportError:
            raise RuntimeError(
                "langchain-databricks is not installed. "
                "Please install it with 'pip install langchain-databricks'"
            )

        if not self.get_api_key():
            raise ValueError(
                "Databricks API key is required. "
                "Please set DATABRICKS_API_KEY environment variable or provide an API key."
            )

        try:
            return ChatDatabricks(
                endpoint=self.model,
                databricks_api_key=self.get_api_key(),
                host=self.host if self.host else None,
                **(self.extra_params or {}),
                **kwargs,
            )
        except Exception as e:
            raise RuntimeError(f"Failed to instantiate Databricks model: {e!s}") from e


class WatsonxLLMConfig(LLMConfig):
    """Configuration for IBM Watson.x models."""

    provider: LLMProvider = LLMProvider.WATSONX
    model: str = Field(
        default="ibm/granite-13b-chat-v2", description="Watson.x model ID."
    )
    api_key: SecretStr = Field(
        default_factory=lambda: SecretStr(os.getenv("WATSONX_API_KEY", "")),
        description="IBM Cloud API key.",
    )
    project_id: str = Field(
        default_factory=lambda: os.getenv("WATSONX_PROJECT_ID", ""),
        description="Watson.x project ID.",
    )
    url: str = Field(
        default_factory=lambda: os.getenv(
            "WATSONX_URL", "https://us-south.ml.cloud.ibm.com"
        ),
        description="Watson.x API URL.",
    )

    def instantiate(self, **kwargs) -> Any:
        """Instantiate Watson.x Chat model."""
        try:
            from langchain_ibm import ChatWatsonx
        except ImportError:
            raise RuntimeError(
                "langchain-ibm is not installed. "
                "Please install it with 'pip install langchain-ibm'"
            )

        if not self.get_api_key():
            raise ValueError(
                "Watson.x API key is required. "
                "Please set WATSONX_API_KEY environment variable or provide an API key."
            )

        if not self.project_id:
            raise ValueError(
                "Watson.x project ID is required. "
                "Please set WATSONX_PROJECT_ID environment variable or provide a project ID."
            )

        try:
            return ChatWatsonx(
                model_id=self.model,
                api_key=self.get_api_key(),
                project_id=self.project_id,
                url=self.url,
                **(self.extra_params or {}),
                **kwargs,
            )
        except Exception as e:
            raise RuntimeError(f"Failed to instantiate Watson.x model: {e!s}") from e


class XAILLMConfig(LLMConfig):
    """Configuration for xAI models."""

    provider: LLMProvider = LLMProvider.XAI
    model: str = Field(default="grok-beta", description="xAI model name.")
    api_key: SecretStr = Field(
        default_factory=lambda: SecretStr(os.getenv("XAI_API_KEY", "")),
        description="API key for xAI.",
    )
    base_url: str = Field(
        default="https://api.x.ai/v1", description="xAI API base URL."
    )

    def instantiate(self, **kwargs) -> Any:
        """Instantiate xAI Chat model."""
        try:
            from langchain_xai import ChatXAI
        except ImportError:
            raise RuntimeError(
                "langchain-xai is not installed. "
                "Please install it with 'pip install langchain-xai'"
            )

        if not self.get_api_key():
            raise ValueError(
                "xAI API key is required. "
                "Please set XAI_API_KEY environment variable or provide an API key."
            )

        try:
            return ChatXAI(
                model=self.model,
                api_key=self.get_api_key(),
                base_url=self.base_url,
                **(self.extra_params or {}),
                **kwargs,
            )
        except Exception as e:
            raise RuntimeError(f"Failed to instantiate xAI model: {e!s}") from e


# TODO: CONVERT OT LIST AND ADD SUPP FOR GEMINI
"""
To convert a ModelList object from the Mistral AI Python client into a list of model names like ['mistral-ocr-2505'], use this code:

python
# Assuming `model_list` is your ModelList instance
model_names = [model.id for model in model_list.data]
This works because:

ModelList objects have a data attribute containing model entries

Each model entry has an id field with the model name string

List comprehension efficiently extracts these IDs

Example with full context:

python
from mistralai import Mistral

client = Mistral(api_key="your_api_key")
model_list = client.models.list()  # Returns ModelList object

# Convert to list of model names
model_names = [model.id for model in model_list.data]
print(model_names)  # Output: ['mistral-ocr-2505', 'mistral-small-2503', ...]
"""
# print(DeepSeekLLMConfig.get_models()) -> deepseek-chat,deepseek-reasoner
