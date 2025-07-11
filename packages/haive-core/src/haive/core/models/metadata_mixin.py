"""Model metadata mixin for LLM configurations.

This module provides a mixin class that adds comprehensive model metadata
access to LLM configuration classes, including context windows, pricing,
and capability information.
"""

import logging
from typing import Any

from haive.core.models.metadata import get_model_metadata

logger = logging.getLogger(__name__)


class ModelMetadataMixin:
    """Mixin to add comprehensive model metadata methods to LLMConfig classes.

    This mixin provides access to model capabilities, context window sizes,
    pricing information, and other metadata from the model catalog.
    """

    def get_context_window(self) -> int:
        """Get the maximum context window size for this model.

        Returns:
            int: Total context window size (input + output tokens)
        """
        metadata = self._get_model_metadata()

        # Return max_tokens if specified
        if "max_tokens" in metadata:
            return metadata.get("max_tokens", 0)

        # Otherwise calculate from input + output tokens
        input_tokens = metadata.get("max_input_tokens", 0)
        output_tokens = metadata.get("max_output_tokens", 0)

        # If both are specified, return their sum
        if input_tokens > 0 and output_tokens > 0:
            return input_tokens + output_tokens

        # If only one is specified, return that
        if input_tokens > 0:
            return input_tokens
        if output_tokens > 0:
            return output_tokens

        # Default fallback based on common models
        getattr(self, "model", "").lower()
        return 0

    def get_max_input_tokens(self) -> int:
        """Get the maximum input tokens for this model.

        Returns:
            int: Maximum input tokens the model can accept
        """
        metadata = self._get_model_metadata()
        return metadata.get("max_input_tokens", self.get_context_window())

    def get_max_output_tokens(self) -> int:
        """Get the maximum output tokens for this model.

        Returns:
            int: Maximum output tokens the model can generate
        """
        metadata = self._get_model_metadata()
        return metadata.get("max_output_tokens", metadata.get("max_tokens", 0))

    def get_token_pricing(self) -> tuple[float, float]:
        """Get the token pricing for this model.

        Returns:
            Tuple[float, float]: (input_cost_per_token, output_cost_per_token)
        """
        metadata = self._get_model_metadata()
        input_cost = metadata.get("input_cost_per_token", 0.0)
        output_cost = metadata.get("output_cost_per_token", 0.0)
        return (input_cost, output_cost)

    def get_batch_token_pricing(self) -> tuple[float, float]:
        """Get the batch token pricing for this model.

        Returns:
            Tuple[float, float]: (input_batch_cost, output_batch_cost)
        """
        metadata = self._get_model_metadata()
        input_cost = metadata.get("input_cost_per_token_batches", 0.0)
        output_cost = metadata.get("output_cost_per_token_batches", 0.0)
        return (input_cost, output_cost)

    def supports_feature(self, feature: str) -> bool:
        """Check if this model supports a specific feature.

        Args:
            feature: Feature name (e.g., "vision", "function_calling")

        Returns:
            bool: True if the model supports the feature, False otherwise
        """
        metadata = self._get_model_metadata()

        # Check for "supports_X" format
        feature_key = f"supports_{feature}"
        if feature_key in metadata:
            return bool(metadata[feature_key])

        # Check for specific features in other formats
        if feature == "web_search" and "search_context_cost_per_query" in metadata:
            return True

        # Check supported modalities
        if (
            feature in ["text", "image", "video", "audio"]
            and "supported_modalities" in metadata
        ):
            return feature in metadata["supported_modalities"]

        return False

    def get_search_context_costs(self) -> dict[str, float]:
        """Get the search context costs for this model.

        Returns:
            Dict[str, float]: Dictionary mapping context sizes to costs
        """
        metadata = self._get_model_metadata()
        search_costs = metadata.get("search_context_cost_per_query", {})
        return search_costs

    def get_supported_endpoints(self) -> list[str]:
        """Get the supported API endpoints for this model.

        Returns:
            List[str]: List of supported endpoints
        """
        metadata = self._get_model_metadata()
        return metadata.get("supported_endpoints", [])

    def get_supported_modalities(self) -> list[str]:
        """Get the supported input modalities for this model.

        Returns:
            List[str]: List of supported modalities (e.g., "text", "image")
        """
        metadata = self._get_model_metadata()
        return metadata.get("supported_modalities", ["text"])

    def get_supported_output_modalities(self) -> list[str]:
        """Get the supported output modalities for this model.

        Returns:
            List[str]: List of supported output modalities
        """
        metadata = self._get_model_metadata()
        return metadata.get("supported_output_modalities", ["text"])

    def get_deprecation_date(self) -> str | None:
        """Get the deprecation date for this model, if available.

        Returns:
            Optional[str]: Deprecation date in YYYY-MM-DD format, or None if not deprecated
        """
        metadata = self._get_model_metadata()
        return metadata.get("deprecation_date")

    def get_model_mode(self) -> str:
        """Get the mode for this model.

        Returns:
            str: Model mode (e.g., "chat", "embedding", "completion")
        """
        metadata = self._get_model_metadata()
        return metadata.get("mode", "chat")

    def _get_model_metadata(self) -> dict[str, Any]:
        """Get metadata for the current model, using alias if available.

        Returns:
            Dictionary of model metadata
        """
        # Use model_alias if available, otherwise use model name
        model_name_for_lookup = getattr(self, "model_alias", None) or self.model

        # Get provider value, handling different formats
        if hasattr(self.provider, "value"):
            provider_value = self.provider.value
        else:
            provider_value = str(self.provider)

        # Use the imported function for actual lookup
        return get_model_metadata(model_name_for_lookup, provider_value)

    # Property getters for common capabilities
    @property
    def supports_vision(self) -> bool:
        """Check if model supports vision/image inputs."""
        return self.supports_feature("vision")

    @property
    def supports_function_calling(self) -> bool:
        """Check if model supports function calling."""
        return self.supports_feature("function_calling")

    @property
    def supports_parallel_function_calling(self) -> bool:
        """Check if model supports parallel function calling."""
        return self.supports_feature("parallel_function_calling")

    @property
    def supports_system_messages(self) -> bool:
        """Check if model supports system messages."""
        return self.supports_feature("system_messages")

    @property
    def supports_tool_choice(self) -> bool:
        """Check if model supports tool choice."""
        return self.supports_feature("tool_choice")

    @property
    def supports_response_schema(self) -> bool:
        """Check if model supports response schema."""
        return self.supports_feature("response_schema")

    @property
    def supports_reasoning(self) -> bool:
        """Check if model supports reasoning."""
        return self.supports_feature("reasoning")

    @property
    def supports_web_search(self) -> bool:
        """Check if model supports web search."""
        return self.supports_feature("web_search")

    @property
    def supports_audio_input(self) -> bool:
        """Check if model supports audio input."""
        return self.supports_feature("audio_input")

    @property
    def supports_audio_output(self) -> bool:
        """Check if model supports audio output."""
        return self.supports_feature("audio_output")

    @property
    def supports_pdf_input(self) -> bool:
        """Check if model supports PDF input."""
        return self.supports_feature("pdf_input")

    @property
    def supports_prompt_caching(self) -> bool:
        """Check if model supports prompt caching."""
        return self.supports_feature("prompt_caching")

    @property
    def supports_native_streaming(self) -> bool:
        """Check if model supports native streaming."""
        return self.supports_feature("native_streaming")

    @property
    def max_tokens(self) -> int:
        """Get maximum total tokens for this model."""
        return self.get_context_window()

    @property
    def max_input_tokens(self) -> int:
        """Get maximum input tokens for this model."""
        return self.get_max_input_tokens()

    @property
    def max_output_tokens(self) -> int:
        """Get maximum output tokens for this model."""
        return self.get_max_output_tokens()
