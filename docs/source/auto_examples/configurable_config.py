"""Configurable chess agent configuration using player agents.

This module provides a chess configuration that supports configurable
player agents instead of hardcoded engine configurations.
"""

from typing import Any

from haive.core.engine.agent.agent import AgentConfig
from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.models.llm import LLMConfig
from pydantic import Field, model_validator

from haive.games.chess.configurable_engines import (
    create_configurable_chess_engines,
    get_example_engines,
)
from haive.games.chess.state import ChessState
from haive.games.core.agent.player_agent import (
    PlayerAgentConfig,
    create_simple_player_configs,
)
from haive.games.utils.recursion_config import RecursionConfig


class ConfigurableChessConfig(AgentConfig):
    """Configurable chess agent configuration.

    This configuration supports using different LLM configurations for
    different players without hardcoding them in engines.

    Examples:
        >>> # Simple string-based configuration
        >>> config = ConfigurableChessConfig(
        ...     white_model="gpt-4",
        ...     black_model="claude-3-opus"
        ... )

        >>> # Using player agent configs
        >>> config = ConfigurableChessConfig(
        ...     player_configs={
        ...         "white_player": PlayerAgentConfig(llm_config="gpt-4"),
        ...         "black_player": PlayerAgentConfig(llm_config="claude-3-opus"),
        ...     }
        ... )

        >>> # Using example configuration
        >>> config = ConfigurableChessConfig(
        ...     example_config="anthropic_vs_openai"
        ... )
    """

    # State schema
    state_schema: type[ChessState] = Field(
        default=ChessState, description="The state schema for the game"
    )

    # Player names
    white_player_name: str = Field(
        default="White Player", description="Name of the white player"
    )
    black_player_name: str = Field(
        default="Black Player", description="Name of the black player"
    )

    # Analysis settings
    enable_analysis: bool = Field(
        default=True, description="Whether to enable position analysis during gameplay"
    )

    # Visualization settings
    should_visualize_graph: bool = Field(
        default=True, description="Whether to visualize the game workflow graph"
    )

    # Game settings
    max_moves: int = Field(
        default=200, description="Maximum number of moves before forcing a draw"
    )

    # Player configuration options (multiple ways to configure)

    # Option 1: Simple model strings
    white_model: str | None = Field(
        default=None,
        description="Model string for white player (e.g., 'gpt-4', 'claude-3-opus')",
    )
    black_model: str | None = Field(
        default=None, description="Model string for black player"
    )

    # Option 2: Player agent configurations
    player_configs: dict[str, PlayerAgentConfig] | None = Field(
        default=None,
        description="Dictionary of role name to player agent configuration",
    )

    # Option 3: Example configuration name
    example_config: str | None = Field(
        default=None,
        description="Name of example configuration (e.g., 'anthropic_vs_openai')",
    )

    # Global settings
    temperature: float | None = Field(
        default=0.7,
        description="Temperature for all engines (can be overridden per player)",
    )

    # Computed engines (set by validator)
    engines: dict[str, AugLLMConfig] = Field(
        default_factory=dict, description="LLM configurations for players and analyzers"
    )

    # Runnable config with proper defaults
    runnable_config: dict[str, Any] = Field(
        default_factory=lambda: RecursionConfig.configure_runnable(
            game_name="chess",
            enable_analysis=True,
        ),
        description="Runtime configuration for the agent",
    )

    @model_validator(mode="after")
    @classmethod
    def configure_engines_and_names(cls) -> Any:
        """Configure engines from the provided player configurations."""
        # Ensure proper recursion configuration
        self.runnable_config = RecursionConfig.configure_runnable(
            runnable_config=self.runnable_config,
            game_name="chess",
            enable_analysis=self.enable_analysis,
        )

        # Determine which configuration method to use
        if self.example_config:
            # Use example configuration
            self.engines = get_example_engines(self.example_config)
            self._update_player_names_from_engines()

        elif self.player_configs:
            # Use provided player configurations
            self.engines = create_configurable_chess_engines(self.player_configs)
            self._update_player_names_from_configs()

        elif self.white_model or self.black_model:
            # Use simple model strings
            white_model = self.white_model or "gpt-4o"
            black_model = self.black_model or "claude-3-5-sonnet-20240620"

            player_configs = create_simple_player_configs(
                white_model=white_model,
                black_model=black_model,
                temperature=self.temperature,
            )
            self.engines = create_configurable_chess_engines(player_configs)
            self._update_player_names_from_models(white_model, black_model)

        else:
            # Use default configuration
            self.engines = get_example_engines("anthropic_vs_openai")
            self.white_player_name = "Claude (White)"
            self.black_player_name = "GPT-4 (Black)"

        return self

    def _update_player_names_from_engines(self):
        """Update player names based on engine configurations."""
        white_engine = self.engines.get("white_player")
        black_engine = self.engines.get("black_player")

        if white_engine and hasattr(white_engine, "llm_config"):
            self.white_player_name = self._get_player_name_from_config(
                white_engine.llm_config, "White"
            )

        if black_engine and hasattr(black_engine, "llm_config"):
            self.black_player_name = self._get_player_name_from_config(
                black_engine.llm_config, "Black"
            )

    def _update_player_names_from_configs(self):
        """Update player names from player agent configurations."""
        if not self.player_configs:
            return

        white_config = self.player_configs.get("white_player")
        black_config = self.player_configs.get("black_player")

        if white_config and white_config.player_name:
            self.white_player_name = white_config.player_name
        elif white_config:
            llm_config = white_config.create_llm_config()
            self.white_player_name = self._get_player_name_from_config(
                llm_config, "White"
            )

        if black_config and black_config.player_name:
            self.black_player_name = black_config.player_name
        elif black_config:
            llm_config = black_config.create_llm_config()
            self.black_player_name = self._get_player_name_from_config(
                llm_config, "Black"
            )

    def _update_player_names_from_models(self, white_model: str, black_model: str):
        """Update player names from model strings."""
        self.white_player_name = f"{self._extract_model_name(white_model)} (White)"
        self.black_player_name = f"{self._extract_model_name(black_model)} (Black)"

    def _get_player_name_from_config(self, llm_config: LLMConfig, color: str) -> str:
        """Extract player name from LLM config."""
        provider = getattr(llm_config, "provider", "unknown")
        model = getattr(llm_config, "model", "unknown")

        if hasattr(provider, "value"):
            provider = provider.value

        return f"{provider}-{model} ({color})"

    def _extract_model_name(self, model_string: str) -> str:
        """Extract a friendly model name from a model string."""
        if ":" in model_string:
            provider, model = model_string.split(":", 1)
            return f"{provider.title()}-{model}"
        return model_string

    class Config:
        """Pydantic configuration."""

        arbitrary_types_allowed = True


# Convenience functions for creating configurations


def create_chess_config(
    white_model: str = "gpt-4o",
    black_model: str = "claude-3-5-sonnet-20240620",
    temperature: float = 0.7,
    enable_analysis: bool = True,
    **kwargs,
) -> ConfigurableChessConfig:
    """Create a chess configuration with simple model strings.

    Args:
        white_model: Model for white player
        black_model: Model for black player
        temperature: Temperature for all engines
        enable_analysis: Whether to enable position analysis
        **kwargs: Additional configuration parameters

    Returns:
        ConfigurableChessConfig: Configured chess agent

    Example:
        >>> config = create_chess_config("gpt-4", "claude-3-opus", temperature=0.8)
    """
    return ConfigurableChessConfig(
        white_model=white_model,
        black_model=black_model,
        temperature=temperature,
        enable_analysis=enable_analysis,
        **kwargs,
    )


def create_chess_config_from_example(
    example_name: str, enable_analysis: bool = True, **kwargs
) -> ConfigurableChessConfig:
    """Create a chess configuration from an example.

    Args:
        example_name: Name of the example configuration
        enable_analysis: Whether to enable position analysis
        **kwargs: Additional configuration parameters

    Returns:
        ConfigurableChessConfig: Configured chess agent

    Available examples: anthropic_vs_openai, gpt4_only, claude_only,
                       mixed_providers, budget_friendly

    Example:
        >>> config = create_chess_config_from_example("budget_friendly")
    """
    return ConfigurableChessConfig(
        example_config=example_name, enable_analysis=enable_analysis, **kwargs
    )


def create_chess_config_from_player_configs(
    player_configs: dict[str, PlayerAgentConfig], enable_analysis: bool = True, **kwargs
) -> ConfigurableChessConfig:
    """Create a chess configuration from player agent configurations.

    Args:
        player_configs: Dictionary of role to player configuration
        enable_analysis: Whether to enable position analysis
        **kwargs: Additional configuration parameters

    Returns:
        ConfigurableChessConfig: Configured chess agent

    Example:
        >>> configs = {
        ...     "white_player": create_player_config("gpt-4", player_name="Deep Blue"),
        ...     "black_player": create_player_config("claude-3-opus", player_name="AlphaZero"),
        ... }
        >>> config = create_chess_config_from_player_configs(configs)
    """
    return ConfigurableChessConfig(
        player_configs=player_configs, enable_analysis=enable_analysis, **kwargs
    )


# Aliases for backward compatibility
ChessConfigV2 = ConfigurableChessConfig
