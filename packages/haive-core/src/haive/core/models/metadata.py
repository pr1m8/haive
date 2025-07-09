"""
Model metadata utilities for LLM configurations.

This module provides utilities for downloading, caching, and accessing
model metadata from LiteLLM's model_prices_and_context_window.json.
"""

from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class ModelMetadata:
    """A class to store and provide model metadata.

    This class encapsulates metadata about a language model, including
    its pricing, context window limits, and provider information.
    """

    name: str
    provider: Optional[str] = None
    metadata: Dict[str, Any] = None

    def __post_init__(self):
        if self.metadata is None:
            self.metadata = get_model_metadata(self.name, self.provider)

    @property
    def context_window(self) -> int:
        """Get the context window size for this model."""
        return self.metadata.get("context_window", 2048)

    @property
    def pricing(self) -> Dict[str, float]:
        """Get the pricing information for this model."""
        return {
            "input": self.metadata.get("input_cost_per_token", 0.0),
            "output": self.metadata.get("output_cost_per_token", 0.0),
        }


import json
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, Optional

import requests

logger = logging.getLogger(__name__)

# Singleton metadata cache
_MODEL_METADATA_CACHE = {}
_METADATA_LAST_UPDATED = None
_METADATA_CACHE_TTL = timedelta(hours=24)
_METADATA_URL = "https://raw.githubusercontent.com/BerriAI/litellm/main/model_prices_and_context_window.json"
_METADATA_CACHE_FILE = Path.home() / ".haive" / "cache" / "model_metadata.json"


def _ensure_cache_dir():
    """Ensure the cache directory exists."""
    cache_dir = _METADATA_CACHE_FILE.parent
    cache_dir.mkdir(parents=True, exist_ok=True)


def _load_metadata_from_cache() -> Dict[str, Any]:
    """Load metadata from cache file."""
    try:
        if _METADATA_CACHE_FILE.exists():
            with open(_METADATA_CACHE_FILE, "r") as f:
                return json.load(f)
    except Exception as e:
        logger.warning(f"Failed to load metadata from cache: {e}")
    return {}


def _save_metadata_to_cache(metadata: Dict[str, Any]) -> None:
    """Save metadata to cache file."""
    try:
        _ensure_cache_dir()
        with open(_METADATA_CACHE_FILE, "w") as f:
            json.dump(metadata, f, indent=2)
    except Exception as e:
        logger.warning(f"Failed to save metadata to cache: {e}")


def _download_metadata() -> Dict[str, Any]:
    """Download metadata from LiteLLM's repository."""
    try:
        response = requests.get(_METADATA_URL, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data
    except Exception as e:
        logger.warning(f"Failed to download metadata: {e}")
        return {}


def get_model_metadata(
    model_name: str, provider: Optional[str] = None, force_refresh: bool = False
) -> Dict[str, Any]:
    """
    Get metadata for a specific model with improved matching.

    This function tries to find the most relevant model metadata based on the
    model name and provider, with multiple fallback strategies.

    Args:
        model_name: Name of the model (e.g., "gpt-4", "claude-3-opus")
        provider: Optional provider prefix (e.g., "azure", "anthropic")
        force_refresh: Force download fresh metadata

    Returns:
        Model metadata dictionary or empty dict if not found
    """
    global _MODEL_METADATA_CACHE, _METADATA_LAST_UPDATED

    # Check if we need to refresh metadata
    if (
        force_refresh
        or not _MODEL_METADATA_CACHE
        or (
            _METADATA_LAST_UPDATED is None
            or datetime.now() - _METADATA_LAST_UPDATED > _METADATA_CACHE_TTL
        )
    ):
        # Try to load from cache first
        if not force_refresh:
            cache_data = _load_metadata_from_cache()
            if cache_data:
                _MODEL_METADATA_CACHE = cache_data
                _METADATA_LAST_UPDATED = datetime.now()

        # Download if still needed
        if force_refresh or not _MODEL_METADATA_CACHE:
            fresh_data = _download_metadata()
            if fresh_data:
                _MODEL_METADATA_CACHE = fresh_data
                _METADATA_LAST_UPDATED = datetime.now()
                _save_metadata_to_cache(fresh_data)

    # No metadata available
    if not _MODEL_METADATA_CACHE:
        return {}

    # Normalize inputs
    normalized_model = model_name.lower().strip()
    normalized_provider = provider.lower().strip() if provider else None

    # Try different lookup strategies

    # 1. Exact match with provider prefix
    if provider:
        provider_model_name = f"{normalized_provider}/{normalized_model}"
        if provider_model_name in _MODEL_METADATA_CACHE:
            return _MODEL_METADATA_CACHE[provider_model_name]

        # Try with different provider format
        alternative_provider_name = f"{normalized_provider}-{normalized_model}"
        if alternative_provider_name in _MODEL_METADATA_CACHE:
            return _MODEL_METADATA_CACHE[alternative_provider_name]

    # 2. Exact match without provider
    if normalized_model in _MODEL_METADATA_CACHE:
        return _MODEL_METADATA_CACHE[normalized_model]

    # 3. Best match search - check for model name contained within keys
    # Priority: provider+model > model > model base version
    candidates = []
    for key in _MODEL_METADATA_CACHE.keys():
        if key == "sample_spec":
            continue

        # Skip entries with wrong provider
        if provider and key.startswith(f"{normalized_provider}/"):
            # Provider prefix match - higher priority
            if normalized_model in key.lower():
                # Add with high score (exact provider match)
                candidates.append((key, 100 + len(normalized_model)))
        elif provider and "litellm_provider" in _MODEL_METADATA_CACHE[key]:
            # Check internal provider field
            if (
                _MODEL_METADATA_CACHE[key]["litellm_provider"].lower()
                == normalized_provider
            ):
                if normalized_model in key.lower():
                    # Add with high score (internal provider match)
                    candidates.append((key, 90 + len(normalized_model)))
        else:
            # No provider specified, or provider doesn't match prefix
            if normalized_model in key.lower():
                # Add with medium score (model name match)
                candidates.append((key, 50 + len(normalized_model)))
            # Base model check (without version)
            elif any(segment in key.lower() for segment in normalized_model.split("-")):
                # Add with lower score (partial match)
                candidates.append((key, 20))

    # Return best match if we have candidates
    if candidates:
        # Sort by score descending
        candidates.sort(key=lambda x: x[1], reverse=True)
        return _MODEL_METADATA_CACHE[candidates[0][0]]

    # 4. Fallback - return empty dictionary
    logger.warning(f"No metadata found for model {model_name} with provider {provider}")
    return {}
