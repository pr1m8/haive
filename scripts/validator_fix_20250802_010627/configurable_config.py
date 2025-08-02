"""Configurable Connect4 agent configuration using player agents.

from typing import Any This module provides a Connect4 configuration that supports
configurable player agents instead of hardcoded engine configurations.

"""

from typing import Any

from haive.core.engine.agent.agent import AgentConfig
from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.models.llm import LLMConfig
from haive.games.connect4.generic_engines import (
    create_generic_connect4_config_from_example,
    create_generic_connect4_engines,
    create_generic_connect4_engines_simple,
)
from haive.games.connect4.state import Connect4State
from haive.games.core.agent.player_agent import PlayerAgentConfig
from pydantic import BaseModel, Field, model_validator


class ConfigurableConnect4Config(AgentConfig):
    """Configurable Connect4 agent configuration.

    This configuration supports using different LLM configurations for
    different players without hardcoding them in engines.

    Examples:
        >>> # Simple string-based configuration
        >>> config = ConfigurableConnect4Config(
        ...     red_model="gpt-4",
        ...     yellow_model="claude-3-opus"
        ... )

        >>> # Using player agent configs
        >>> config = ConfigurableConnect4Config(
        ...     player_configs={
        ...         "red_player": PlayerAgentConfig(llm_config="gpt-4"),
        ...         "yellow_player": PlayerAgentConfig(llm_config="claude-3-opus"),
        ...     }
        ... )

        >>> # Using example configuration
        >>> config = ConfigurableConnect4Config(
        ...     example_config="gpt_vs_claude"
        ... )

    """

    # State schema
    state_schema: type[BaseModel] = Field(
        default=Connect4State, description="The state schema for the game"
    )

    # Player names
    red_player_name: str = Field(
        default="Red Player", description="Name of the red player"
    )
    yellow_player_name: str = Field(
        default="Yellow Player", description="Name of the yellow player"
    )

    # Analysis settings
    enable_analysis: bool = Field(
        default=False, description="Whether to enable position analysis during gameplay"
    )

    # Visualization settings
    should_visualize_graph: bool = Field(
        default=False, description="Whether to visualize the game workflow graph"
    )

    # Game settings
    max_moves: int = Field(
        default=42,
        description="Maximum number of moves before forcing a draw (7x6 board)",
    )

    # Player configuration options (multiple ways to configure)

    # Option 1: Simple model strings
    red_model: str | None = Field(
        default=None,
        description="Model string for red player (e.g., 'gpt-4', 'claude-3-opus')",
    )
    yellow_model: str | None = Field(
        default=None, description="Model string for yellow player"
    )

    # Option 2: Player agent configurations
    player_configs: dict[str, PlayerAgentConfig] | None = Field(
        default=None,
        description="Dictionary of role name to player agent configuration",
    )

    # Option 3: Example configuration name
    example_config: str | None = Field(
        default=None,
        description="Name of example configuration (e.g., 'gpt_vs_claude')",
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

    @model_validator(mode="after")
    def configure_engines_and_names(cls) -> Any:
        """Configure engines from the provided player configurations."""
        # Determine which configuration method to use
        if self.example_config:
            # Use example configuration
            self.engines = create_generic_connect4_config_from_example(
                self.example_config
            )
            self._update_player_names_from_engines()

        elif self.player_configs:
            # Use provided player configurations
            self.engines = create_generic_connect4_engines(self.player_configs)
            self._update_player_names_from_configs()

        elif self.red_model or self.yellow_model:
            # Use simple model strings
            red_model = self.red_model or "gpt-4o"
            yellow_model = self.yellow_model or "claude-3-5-sonnet-20240620"

            self.engines = create_generic_connect4_engines_simple(
                red_model=red_model,
                yellow_model=yellow_model,
                temperature=self.temperature,
            )
            self._update_player_names_from_models(red_model, yellow_model)

        else:
            # Use default configuration
            self.engines = create_generic_connect4_config_from_example("gpt_vs_claude")
            self.red_player_name = "GPT-4 (Red)"
            self.yellow_player_name = "Claude (Yellow)"

        return self

    def _update_player_names_from_engines(self):
        """Update player names based on engine configurations."""
        red_engine = self.engines.get("red_player")
        yellow_engine = self.engines.get("yellow_player")

        if red_engine and hasattr(red_engine, "llm_config"):
            self.red_player_name = self._get_player_name_from_config(
                red_engine.llm_config, "Red"
            )

        if yellow_engine and hasattr(yellow_engine, "llm_config"):
            self.yellow_player_name = self._get_player_name_from_config(
                yellow_engine.llm_config, "Yellow"
            )

    def _update_player_names_from_configs(self):
        """Update player names from player agent configurations."""
        if not self.player_configs:
            return

        red_config = self.player_configs.get("red_player")
        yellow_config = self.player_configs.get("yellow_player")

        if red_config and red_config.player_name:
            self.red_player_name = red_config.player_name
        elif red_config:
            llm_config = red_config.create_llm_config()
            self.red_player_name = self._get_player_name_from_config(llm_config, "Red")

        if yellow_config and yellow_config.player_name:
            self.yellow_player_name = yellow_config.player_name
        elif yellow_config:
            llm_config = yellow_config.create_llm_config()
            self.yellow_player_name = self._get_player_name_from_config(
                llm_config, "Yellow"
            )

    def _update_player_names_from_models(self, red_model: str, yellow_model: str):
        """Update player names from model strings."""
        self.red_player_name = f"{self._extract_model_name(red_model)} (Red)"
        self.yellow_player_name = f"{self._extract_model_name(yellow_model)} (Yellow)"

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


def create_connect4_config(
    red_model: str = "gpt-4o",
    yellow_model: str = "claude-3-5-sonnet-20240620",
    temperature: float = 0.7,
    enable_analysis: bool = False,
    **kwargs,
) -> ConfigurableConnect4Config:
    """Create a Connect4 configuration with simple model strings.

    Args:
        red_model: Model for red player
        yellow_model: Model for yellow player
        temperature: Temperature for all engines
        enable_analysis: Whether to enable position analysis
        **kwargs: Additional configuration parameters

    Returns:
        ConfigurableConnect4Config: Configured Connect4 agent

    Example:
        >>> config = create_connect4_config("gpt-4", "claude-3-opus", temperature=0.8)

    """
    return ConfigurableConnect4Config(
        red_model=red_model,
        yellow_model=yellow_model,
        temperature=temperature,
        enable_analysis=enable_analysis,
        **kwargs,
    )


def create_connect4_config_from_example(
    example_name: str, enable_analysis: bool = False, **kwargs
) -> ConfigurableConnect4Config:
    """Create a Connect4 configuration from an example.

    Args:
        example_name: Name of the example configuration
        enable_analysis: Whether to enable position analysis
        **kwargs: Additional configuration parameters

    Returns:
        ConfigurableConnect4Config: Configured Connect4 agent

    Available examples: gpt_vs_claude, gpt_only, claude_only, budget, mixed

    Example:
        >>> config = create_connect4_config_from_example("budget")

    """
    return ConfigurableConnect4Config(
        example_config=example_name, enable_analysis=enable_analysis, **kwargs
    )


def create_connect4_config_from_player_configs(
    player_configs: dict[str, PlayerAgentConfig],
    enable_analysis: bool = False,
    **kwargs,
) -> ConfigurableConnect4Config:
    """Create a Connect4 configuration from player agent configurations.

    Args:
        player_configs: Dictionary of role to player configuration
        enable_analysis: Whether to enable position analysis
        **kwargs: Additional configuration parameters

    Returns:
        ConfigurableConnect4Config: Configured Connect4 agent

    Example:
        >>> configs = {
        ...     "red_player": create_player_config("gpt-4", player_name="Red Master"),
        ...     "yellow_player": create_player_config("claude-3-opus", player_name="Yellow Pro"),
        ... }
        >>> config = create_connect4_config_from_player_configs(configs)

    """
    return ConfigurableConnect4Config(
        player_configs=player_configs, enable_analysis=enable_analysis, **kwargs
    )


# Aliases for backward compatibility
Connect4ConfigV2 = ConfigurableConnect4Config
