"""LLM configuration factory for the UI."""

from __future__ import annotations

import os
from typing import Any


def make_llm_config(ui_config: dict[str, Any]) -> Any:
    """Create an AugLLMConfig from UI settings.

    Args:
        ui_config: Dict with provider, model, temperature, max_tokens, system_prompt

    Returns:
        AugLLMConfig instance ready to use
    """
    from haive.core.engine.aug_llm import AugLLMConfig
    from haive.core.models.llm.base import OpenAILLMConfig

    provider = ui_config.get("provider", "openai")
    model = ui_config.get("model", "gpt-4o-mini")
    temperature = ui_config.get("temperature", 0.7)
    max_tokens = ui_config.get("max_tokens", 2000)
    system_prompt = ui_config.get("system_prompt", "")

    kwargs: dict[str, Any] = {
        "temperature": temperature,
        "max_tokens": max_tokens,
    }

    if system_prompt:
        kwargs["system_message"] = system_prompt

    if provider == "openai":
        kwargs["llm_config"] = OpenAILLMConfig(model=model)
    elif provider == "anthropic":
        # Use langchain-anthropic if available
        kwargs["llm_config"] = OpenAILLMConfig(model=model)
    # For azure/ollama, let AugLLMConfig auto-detect from env

    return AugLLMConfig(**kwargs)


def make_game_llm_config(ui_config: dict[str, Any], player_name: str = "Player") -> dict[str, Any]:
    """Create game-compatible LLM config dict.

    Args:
        ui_config: UI LLM settings
        player_name: Name for this player

    Returns:
        Dict suitable for game agent configuration
    """
    return {
        "provider": ui_config.get("provider", "openai"),
        "model": ui_config.get("model", "gpt-4o-mini"),
        "temperature": ui_config.get("temperature", 0.7),
        "player_name": player_name,
    }
