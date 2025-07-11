"""Secure configuration mixin for API credentials.

This module provides a mixin for secure handling of API credentials
with environment variable fallbacks and validation logic. It enables
automatic resolution of API keys from environment variables based on
the provider type, with proper secure storage using Pydantic's SecretStr.

Usage:
    ```python
    from pydantic import BaseModel, Field
    from typing import Optional
    from haive.core.common.mixins import SecureConfigMixin

    class APIConfig(SecureConfigMixin, BaseModel):
        provider: str = Field(default="openai")
        api_key: Optional[SecretStr] = Field(default=None)

        def make_api_call(self):
            # Securely retrieve the API key
            key = self.get_api_key()
            if not key:
                raise ValueError("No API key available")
            # Use key for API call
            # ...

    # Will try to use OPENAI_API_KEY from environment
    config = APIConfig(provider="openai")

    # Will use the explicitly provided key
    config = APIConfig(provider="anthropic", api_key="sk-ant-...")
    ```
"""

import logging
import os
from typing import Optional

from pydantic import SecretStr, field_validator

logger = logging.getLogger(__name__)


class SecureConfigMixin:
    """A mixin to provide secure and flexible configuration for API keys.

    This mixin enables:
    1. Dynamic API key resolution from multiple sources
    2. Secure storage using SecretStr
    3. Environment variable fallbacks based on provider type
    4. Validation and error reporting

    The mixin implements a field validator for the 'api_key' field that
    attempts to resolve the key from environment variables if not explicitly
    provided, based on the 'provider' field. It also provides a safe
    method to retrieve the key value with appropriate error handling.

    Attributes:
        api_key: A SecretStr containing the API key.
        provider: The API provider name (used to determine environment variable).
    """

    @field_validator("api_key", mode="after", check_fields=False)
    @classmethod
    def _validate_api_key(cls, v, values):
        """Dynamically set the API key with robust fallback mechanism.

        This validator implements a priority-based resolution strategy:
        1. Use explicitly provided value
        2. Try environment variable based on provider
        3. Fall back to default/empty

        Args:
            v: The current value of the api_key field.
            values: The values dict containing other fields.

        Returns:
            The resolved SecretStr containing the API key.
        """
        # If a value is already set and not empty, return it
        if v is not None and v != "":
            # If it's not a SecretStr, convert it
            if not isinstance(v, SecretStr):
                return SecretStr(str(v))
            return v

        # Determine the environment variable based on provider
        provider = values.get("provider")
        if not provider:
            return SecretStr("")

        logger.debug(f"Validating API key for provider: {provider}")

        # Create mapping for both enum values and string values
        env_key_map = {
            # Using .value to handle enum objects
            "azure": "AZURE_OPENAI_API_KEY",
            "openai": "OPENAI_API_KEY",
            "anthropic": "ANTHROPIC_API_KEY",
            "gemini": "GEMINI_API_KEY",
            "google": "GOOGLE_API_KEY",
            "deepseek": "DEEPSEEK_API_KEY",
            "mistralai": "MISTRAL_API_KEY",
            "groq": "GROQ_API_KEY",
            "cohere": "COHERE_API_KEY",
            "together_ai": "TOGETHER_AI_API_KEY",
            "fireworks_ai": "FIREWORKS_AI_API_KEY",
            "perplexity": "PERPLEXITY_API_KEY",
            "huggingface": "HUGGING_FACE_API_KEY",
            "ai21": "AI21_API_KEY",
            "aleph_alpha": "ALEPH_ALPHA_API_KEY",
            "gooseai": "GOOSEAI_API_KEY",
            "mosaicml": "MOSAICML_API_KEY",
            "nlp_cloud": "NLP_CLOUD_API_KEY",
            "openlm": "OPENLM_API_KEY",
            "petals": "PETALS_API_KEY",
            "replicate": "REPLICATE_API_KEY",
            "vertex_ai": "VERTEX_AI_API_KEY",
        }

        # Get provider value - handle both enum and string
        provider_value = provider.value if hasattr(provider, "value") else str(provider)

        # Try to get API key from environment variables
        env_key = env_key_map.get(provider_value.lower())

        if env_key:
            logger.debug(f"Looking for environment variable: {env_key}")
            api_key = os.getenv(env_key)
            if api_key and api_key.strip():
                logger.debug(
                    f"Found API key for {provider_value} in {env_key} (length: {len(api_key)})"
                )
                return SecretStr(api_key)
            logger.warning(f"Environment variable {env_key} not found or empty")
        else:
            logger.warning(
                f"No environment mapping found for provider: {provider_value}"
            )

        # If no key found, return an empty SecretStr
        logger.debug(
            f"No API key found for {provider_value}, returning empty SecretStr"
        )
        return SecretStr("")

    def get_api_key(self) -> str | None:
        """Safely retrieve the API key with improved error handling.

        This method attempts to retrieve the API key value from the SecretStr
        field, with comprehensive error handling and helpful log messages for
        troubleshooting. In development environments, it can return fake test
        keys for testing purposes.

        Returns:
            The API key as a string, or None if not available or invalid.
        """
        try:
            # Check if api_key attribute exists and is not None
            if not hasattr(self, "api_key") or self.api_key is None:
                logger.warning(
                    f"No API key attribute found for {getattr(self, 'provider', 'unknown provider')}"
                )
                return None

            # Try to get the secret value
            key_value = self.api_key.get_secret_value()

            # Check if the key is actually empty
            if not key_value or key_value.strip() == "":
                # Enhanced logging for debugging
                provider_value = getattr(self, "provider", "unknown")
                provider_str = (
                    provider_value.value
                    if hasattr(provider_value, "value")
                    else str(provider_value)
                )

                # Get the expected environment variable name for this provider
                env_key_map = {
                    # Using .value to handle enum objects
                    "azure": "AZURE_OPENAI_API_KEY",
                    "openai": "OPENAI_API_KEY",
                    "anthropic": "ANTHROPIC_API_KEY",
                    "gemini": "GEMINI_API_KEY",
                    "google": "GOOGLE_API_KEY",
                }

                env_var = env_key_map.get(
                    provider_str.lower(), f"{provider_str.upper()}_API_KEY"
                )
                logger.warning(
                    f"API key for {provider_str} is empty. Please ensure the {env_var} environment variable is set."
                )

                # For Azure, provide additional helpful info
                if provider_str.lower() == "azure":
                    logger.warning(
                        "For Azure OpenAI, make sure both AZURE_OPENAI_API_KEY and AZURE_OPENAI_ENDPOINT are set."
                    )

                return None

            return key_value
        except Exception as e:
            logger.exception(f"Error retrieving API key: {e}")

            # If we're in a testing environment, use fake keys for development
            if (
                os.getenv("ENVIRONMENT") == "development"
                or os.getenv("TESTING") == "true"
            ):
                provider_value = getattr(self, "provider", "")
                provider_str = (
                    provider_value.value
                    if hasattr(provider_value, "value")
                    else str(provider_value)
                )
                logger.debug(
                    f"Using fake test key for {provider_str} in development environment"
                )
                return f"test_key_{provider_str}"

            return None
