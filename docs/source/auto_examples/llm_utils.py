"""Chess-specific LLM utilities using the game LLM factory.

This module provides chess-specific utilities for creating and
configuring LLMs for chess gameplay, building on the core LLM factory
system.
"""

from typing import Any, Dict, Optional

from haive.core.engine.aug_llm import AugLLMConfig

from haive.games.chess.aug_llms import (
    generate_analysis_prompt,
    generate_move_prompt,
)
from haive.games.chess.models import ChessAnalysis, ChessPlayerDecision
from haive.games.llm_config_factory import GameLLMFactory


def create_chess_engines_from_config(
    white_config: Dict[str, Any],
    black_config: Dict[str, Any],
    enable_analysis: bool = True,
    analyzer_configs: Optional[Dict[str, Dict[str, Any]]] = None,
) -> Dict[str, AugLLMConfig]:
    """Create chess engines from simple configuration dictionaries.

    Args:
        white_config: Config for white player with 'provider', 'model', etc.
        black_config: Config for black player with 'provider', 'model', etc.
        enable_analysis: Whether to create analyzer engines
        analyzer_configs: Optional separate configs for analyzers

    Returns:
        Dictionary of AugLLMConfig objects for all chess roles

    Examples:
        >>> # Simple provider-only config
        >>> engines = create_chess_engines_from_config(
        ...     white_config={"provider": "anthropic"},
        ...     black_config={"provider": "openai"}
        ... )

        >>> # With custom models
        >>> engines = create_chess_engines_from_config(
        ...     white_config={
        ...         "provider": "anthropic",
        ...         "model": "claude-3-opus-20240229"
        ...     },
        ...     black_config={
        ...         "provider": "azure",
        ...         "model": "gpt-4-turbo"
        ...     }
        ... )

        >>> # Separate analyzer configs
        >>> engines = create_chess_engines_from_config(
        ...     white_config={"provider": "anthropic"},
        ...     black_config={"provider": "openai"},
        ...     analyzer_configs={
        ...         "white": {"provider": "azure"},
        ...         "black": {"provider": "azure"}
        ...     }
        ... )
    """
    # Create player LLM configs using the factory
    white_llm = GameLLMFactory.create_llm_config(
        game_type="strategic", **white_config  # Chess is strategic
    )

    black_llm = GameLLMFactory.create_llm_config(game_type="strategic", **black_config)

    # Create engine configs
    engines = {
        "white_player": AugLLMConfig(
            llm_config=white_llm,
            prompt_template=generate_move_prompt("white"),
            structured_output_model=ChessPlayerDecision,
            description="White player move generation",
        ),
        "black_player": AugLLMConfig(
            llm_config=black_llm,
            prompt_template=generate_move_prompt("black"),
            structured_output_model=ChessPlayerDecision,
            description="Black player move generation",
        ),
    }

    # Add analyzers if enabled
    if enable_analysis:
        # Use separate analyzer configs if provided, otherwise use player configs
        white_analyzer_config = white_config
        black_analyzer_config = black_config

        if analyzer_configs:
            white_analyzer_config = analyzer_configs.get("white", white_config)
            black_analyzer_config = analyzer_configs.get("black", black_config)

        # Create analyzer LLMs
        white_analyzer_llm = GameLLMFactory.create_llm_config(
            game_type="strategic", **white_analyzer_config
        )

        black_analyzer_llm = GameLLMFactory.create_llm_config(
            game_type="strategic", **black_analyzer_config
        )

        # Add analyzer engines
        engines.update(
            {
                "white_analyzer": AugLLMConfig(
                    llm_config=white_analyzer_llm,
                    prompt_template=generate_analysis_prompt("white"),
                    structured_output_model=ChessAnalysis,
                    description="White position analysis",
                ),
                "black_analyzer": AugLLMConfig(
                    llm_config=black_analyzer_llm,
                    prompt_template=generate_analysis_prompt("black"),
                    structured_output_model=ChessAnalysis,
                    description="Black position analysis",
                ),
            }
        )

    return engines


def create_chess_engines_simple(
    white_provider: str = "anthropic",
    white_model: Optional[str] = None,
    black_provider: str = "anthropic",
    black_model: Optional[str] = None,
    temperature: Optional[float] = None,
    enable_analysis: bool = True,
) -> Dict[str, AugLLMConfig]:
    """Create chess engines with simple provider/model specification.

    Args:
        white_provider: Provider for white (e.g., "anthropic", "openai")
        white_model: Model for white (uses default if None)
        black_provider: Provider for black
        black_model: Model for black (uses default if None)
        temperature: Temperature for all engines
        enable_analysis: Whether to create analyzer engines

    Returns:
        Dictionary of AugLLMConfig objects

    Examples:
        >>> # Use defaults
        >>> engines = create_chess_engines_simple()

        >>> # Different providers
        >>> engines = create_chess_engines_simple(
        ...     white_provider="anthropic",
        ...     black_provider="openai"
        ... )

        >>> # Custom models
        >>> engines = create_chess_engines_simple(
        ...     white_provider="anthropic",
        ...     white_model="claude-3-opus-20240229",
        ...     black_provider="openai",
        ...     black_model="gpt-4-turbo"
        ... )
    """
    white_config = {"provider": white_provider}
    if white_model:
        white_config["model"] = white_model
    if temperature is not None:
        white_config["temperature"] = temperature

    black_config = {"provider": black_provider}
    if black_model:
        black_config["model"] = black_model
    if temperature is not None:
        black_config["temperature"] = temperature

    return create_chess_engines_from_config(
        white_config=white_config,
        black_config=black_config,
        enable_analysis=enable_analysis,
    )


def get_available_chess_providers() -> list[str]:
    """Get list of available LLM providers for chess.

    Returns:
        List of provider names
    """
    return GameLLMFactory.get_available_providers()


def get_recommended_chess_models() -> Dict[str, str]:
    """Get recommended models for chess gameplay.

    Returns:
        Dictionary mapping providers to recommended models
    """
    recommendations = {
        "anthropic": "claude-3-5-sonnet-20240620",  # Fast and strategic
        "openai": "gpt-4o",  # Optimized for performance
        "azure": "gpt-4o",  # Same as OpenAI
        "google": "gemini-1.5-pro",  # Good for analysis
        "groq": "llama-3.1-70b-versatile",  # Fast inference
        "deepseek": "deepseek-chat",  # Cost-effective
    }

    return recommendations
