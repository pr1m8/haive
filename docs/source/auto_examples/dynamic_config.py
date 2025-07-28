"""Dynamic configuration for chess game.

This module provides a flexible configuration system for chess that supports:
- Legacy hardcoded engines (backward compatibility)
- Simple model string configuration
- Example-based configuration
- Advanced PlayerAgentConfig configuration
"""

from typing import Any, Dict, List, Optional

from pydantic import Field

from haive.games.chess.engines import build_chess_aug_llms
from haive.games.chess.generic_engines import create_generic_chess_engines
from haive.games.chess.state import ChessState
from haive.games.core.agent.player_agent import PlayerAgentConfig
from haive.games.core.config import BaseGameConfig, GamePlayerRole


class ChessConfig(BaseGameConfig):
    """Dynamic configuration for chess game.

    This configuration supports multiple modes:
    1. Legacy: Use hardcoded engines from engines.py
    2. Simple: Specify models as strings (white_model, black_model)
    3. Example: Use predefined configurations (e.g., "gpt_vs_claude")
    4. Advanced: Full PlayerAgentConfig specifications

    Attributes:
        white_model: Model for white player (simple mode)
        black_model: Model for black player (simple mode)
        white_player_name: Display name for white player
        black_player_name: Display name for black player
        max_moves: Maximum moves before draw (default: 200)
        enable_fen_visualization: Show FEN strings in analysis
    """

    # Game-specific fields
    name: str = Field(default="Chess", description="Name of the game")
    state_schema: type[ChessState] = Field(default=ChessState)

    # Simple mode fields (override base class generics)
    white_model: Optional[str] = Field(
        default=None, description="Model for white player"
    )
    black_model: Optional[str] = Field(
        default=None, description="Model for black player"
    )

    # Player names
    white_player_name: Optional[str] = Field(
        default=None, description="Name for white player"
    )
    black_player_name: Optional[str] = Field(
        default=None, description="Name for black player"
    )

    # Chess-specific settings
    max_moves: int = Field(default=200, description="Maximum moves before draw")
    enable_fen_visualization: bool = Field(
        default=True, description="Show FEN in analysis"
    )
    recursion_limit: int = Field(
        default=600, description="Python recursion limit for chess"
    )

    def get_role_definitions(self) -> Dict[str, GamePlayerRole]:
        """Define chess player roles."""
        return {
            "white_player": GamePlayerRole(
                name="white_player",
                display_name=self.white_player_name or "White",
                default_model="gpt-4o",
            ),
            "black_player": GamePlayerRole(
                name="black_player",
                display_name=self.black_player_name or "Black",
                default_model="claude-3-5-sonnet-20240620",
            ),
            "white_analyzer": GamePlayerRole(
                name="white_analyzer",
                display_name="White Analyst",
                is_analyzer=True,
                default_model="gpt-4o",
            ),
            "black_analyzer": GamePlayerRole(
                name="black_analyzer",
                display_name="Black Analyst",
                is_analyzer=True,
                default_model="claude-3-5-sonnet-20240620",
            ),
        }

    def get_example_configs(self) -> Dict[str, Dict[str, Any]]:
        """Define example chess configurations."""
        return {
            "gpt_vs_claude": {
                "white_model": "gpt-4o",
                "black_model": "claude-3-5-sonnet-20240620",
                "white_player_name": "GPT White",
                "black_player_name": "Claude Black",
            },
            "anthropic_vs_openai": {
                "white_model": "claude-3-opus-20240229",
                "black_model": "gpt-4-turbo-preview",
                "white_player_name": "Claude White",
                "black_player_name": "GPT Black",
            },
            "gpt_only": {
                "white_model": "gpt-4o",
                "black_model": "gpt-4o",
                "white_player_name": "GPT White",
                "black_player_name": "GPT Black",
            },
            "claude_only": {
                "white_model": "claude-3-opus-20240229",
                "black_model": "claude-3-opus-20240229",
                "white_player_name": "Claude White",
                "black_player_name": "Claude Black",
            },
            "budget": {
                "white_model": "gpt-3.5-turbo",
                "black_model": "claude-3-haiku-20240307",
                "temperature": 0.5,
                "white_player_name": "Budget White",
                "black_player_name": "Budget Black",
            },
            "mixed": {
                "white_model": "gemini-1.5-pro",
                "black_model": "mistral-large",
                "white_player_name": "Gemini White",
                "black_player_name": "Mistral Black",
            },
        }

    def build_legacy_engines(self) -> List[Any]:
        """Build legacy hardcoded engines."""
        return build_chess_aug_llms()

    def create_simple_player_configs(self) -> Dict[str, PlayerAgentConfig]:
        """Create player configs from simple model strings."""
        # Use white_model/black_model if provided, otherwise use base class defaults
        white_model = self.white_model or self.player1_model or "gpt-4o"
        black_model = (
            self.black_model or self.player2_model or "claude-3-5-sonnet-20240620"
        )

        return {
            "white_player": PlayerAgentConfig(
                llm_config=white_model,
                temperature=self.temperature,
                player_name=self.white_player_name or "White",
            ),
            "black_player": PlayerAgentConfig(
                llm_config=black_model,
                temperature=self.temperature,
                player_name=self.black_player_name or "Black",
            ),
            "white_analyzer": PlayerAgentConfig(
                llm_config=white_model,
                temperature=0.2,  # Lower temperature for analysis
                player_name="White Analyst",
            ),
            "black_analyzer": PlayerAgentConfig(
                llm_config=black_model, temperature=0.2, player_name="Black Analyst"
            ),
        }

    def create_engines_from_player_configs(
        self, player_configs: Dict[str, PlayerAgentConfig]
    ) -> List[Any]:
        """Create engines from player configurations."""
        return create_generic_chess_engines(player_configs)


# Convenience functions for easy configuration


def create_chess_config(
    white_model: str = "gpt-4o",
    black_model: str = "claude-3-5-sonnet-20240620",
    **kwargs
) -> ChessConfig:
    """Create a chess configuration with simple model strings.

    Args:
        white_model: Model for white player
        black_model: Model for black player
        **kwargs: Additional configuration parameters

    Returns:
        ChessConfig instance

    Example:
        >>> config = create_chess_config("gpt-4", "claude-3-opus")
        >>> config = create_chess_config(
        ...     "openai:gpt-4o",
        ...     "anthropic:claude-3-5-sonnet",
        ...     temperature=0.8
        ... )
    """
    return ChessConfig(white_model=white_model, black_model=black_model, **kwargs)


def create_chess_config_from_example(example_name: str, **kwargs) -> ChessConfig:
    """Create a chess configuration from a predefined example.

    Args:
        example_name: Name of the example configuration
        **kwargs: Additional parameters to override

    Returns:
        ChessConfig instance

    Available examples:
        - "gpt_vs_claude": GPT-4 vs Claude
        - "anthropic_vs_openai": Claude vs GPT showdown
        - "gpt_only": GPT-4 for both players
        - "claude_only": Claude for both players
        - "budget": Cost-effective models
        - "mixed": Different providers

    Example:
        >>> config = create_chess_config_from_example("budget")
        >>> config = create_chess_config_from_example("gpt_vs_claude", max_moves=150)
    """
    return ChessConfig(example_config=example_name, **kwargs)


def create_chess_config_with_players(
    player_configs: Dict[str, PlayerAgentConfig], **kwargs
) -> ChessConfig:
    """Create a chess configuration with detailed player configs.

    Args:
        player_configs: Dictionary mapping role names to PlayerAgentConfig
        **kwargs: Additional configuration parameters

    Returns:
        ChessConfig instance

    Expected roles:
        - "white_player": White player configuration
        - "black_player": Black player configuration
        - "white_analyzer": White analyzer configuration (optional)
        - "black_analyzer": Black analyzer configuration (optional)

    Example:
        >>> player_configs = {
        ...     "white_player": PlayerAgentConfig(
        ...         llm_config="gpt-4",
        ...         temperature=0.7,
        ...         player_name="Aggressive White"
        ...     ),
        ...     "black_player": PlayerAgentConfig(
        ...         llm_config="claude-3-opus",
        ...         temperature=0.3,
        ...         player_name="Defensive Black"
        ...     )
        ... }
        >>> config = create_chess_config_with_players(player_configs)
    """
    return ChessConfig(player_configs=player_configs, **kwargs)


def create_legacy_chess_config(**kwargs) -> ChessConfig:
    """Create a chess configuration using legacy hardcoded engines.

    This is for backward compatibility with existing code.

    Args:
        **kwargs: Additional configuration parameters

    Returns:
        ChessConfig instance with hardcoded engines
    """
    return ChessConfig(use_legacy_engines=True, **kwargs)


# Quick access to common configurations


def budget_chess(**kwargs) -> ChessConfig:
    """Create a budget-friendly chess configuration."""
    return create_chess_config_from_example("budget", **kwargs)


def competitive_chess(**kwargs) -> ChessConfig:
    """Create a competitive chess configuration with top models."""
    return create_chess_config("gpt-4o", "claude-3-opus-20240229", **kwargs)


def experimental_chess(**kwargs) -> ChessConfig:
    """Create an experimental chess configuration with mixed providers."""
    return create_chess_config_from_example("mixed", **kwargs)
