"""Chess agent configuration module.

from typing import Any
This module provides configuration classes for chess agents, including:
    - Core game parameters
    - LLM engine settings
    - Analysis options
    - Visualization settings
    - State schema definition

The configuration system uses Pydantic for validation and default values,
making it easy to create and customize chess agent instances.
"""

from typing import Any

from pydantic import Field, model_validator

from haive.games.chess.engines import build_chess_aug_llms
from haive.games.chess.generic_engines import create_generic_chess_engines
from haive.games.chess.state import ChessState
from haive.games.core.agent.player_agent import PlayerAgentConfig
from haive.games.core.config import BaseGameConfig, GamePlayerRole
from haive.games.utils.recursion_config import RecursionConfig


class ChessConfig(BaseGameConfig):
    """Configuration class for chess game agents.

    This class defines all configuration parameters for a chess agent,
    including state schema, LLM engines, game settings, and visualization
    options.

    Attributes:
        state_schema (Type[ChessState]): The state schema for the game.
        white_player_name (str): Name of the white player.
        black_player_name (str): Name of the black player.
        enable_analysis (bool): Whether to enable position analysis during gameplay.
        should_visualize_graph (bool): Whether to visualize the game workflow graph.
        max_moves (int): Maximum number of moves before forcing a draw.
        engines (Dict[str, AugLLMConfig]): LLM configurations for players and analyzers.
        runnable_config (Dict[str, Any]): Runtime configuration for the agent.

    Examples:
        >>> # Create a basic configuration
        >>> config = ChessConfig()
        >>>
        >>> # Create a configuration with analysis disabled
        >>> config = ChessConfig(enable_analysis=False)
        >>>
        >>> # Create a configuration with custom LLM engines
        >>> from haive.core.engine.aug_llm import build_aug_llm
        >>> engines = {
        ...     "white_player": build_aug_llm("openai", "gpt-4"),
        ...     "black_player": build_aug_llm("anthropic", "claude-3-opus-20240229"),
        ... }
        >>> config = ChessConfig(engines=engines)
    """

    # State schema
    state_schema: type[ChessState] = Field(
        default=ChessState, description="The state schema for the game"
    )

    # Game name
    name: str = Field(default="Chess", description="Name of the game")

    # Player names
    white_player_name: str | None = Field(
        default=None, description="Name of the white player"
    )
    black_player_name: str | None = Field(
        default=None, description="Name of the black player"
    )

    # Chess-specific model fields (override base class)
    white_model: str | None = Field(default=None, description="Model for white player")
    black_model: str | None = Field(default=None, description="Model for black player")

    # Analysis settings (already in base class)
    # enable_analysis is inherited from BaseGameConfig

    # Visualization settings
    should_visualize_graph: bool = Field(
        default=True, description="Whether to visualize the game workflow graph"
    )

    # Game settings
    max_moves: int = Field(
        default=200, description="Maximum number of moves before forcing a draw"
    )

    # Chess-specific recursion limit
    recursion_limit: int = Field(
        default=600, description="Python recursion limit for chess"
    )

    # LLM engines - no default factory for backward compatibility mode
    engines: list[Any] | None = Field(
        default=None,
        description="LLM configurations for players and analyzers",
    )

    # Runnable config with proper defaults
    runnable_config: dict[str, Any] = Field(
        default_factory=lambda: RecursionConfig.configure_runnable(
            game_name="chess",
            enable_analysis=True,
        ),
        description="Runtime configuration for the agent",
    )

    def get_role_definitions(self) -> dict[str, GamePlayerRole]:
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

    def get_example_configs(self) -> dict[str, dict[str, Any]]:
        """Define example chess configurations."""
        return {
            "gpt_vs_claude": {
                "white_model": "gpt-4o",
                "black_model": "claude-3-5-sonnet-20240620",
                "white_player_name": "GPT White",
                "black_player_name": "Claude Black",
            },
            "budget": {
                "white_model": "gpt-3.5-turbo",
                "black_model": "claude-3-haiku-20240307",
                "temperature": 0.5,
            },
        }

    def build_legacy_engines(self) -> list[Any]:
        """Build legacy hardcoded engines."""
        # Import here to avoid circular imports
        return build_chess_aug_llms()

    def create_simple_player_configs(self) -> dict[str, PlayerAgentConfig]:
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
        self, player_configs: dict[str, PlayerAgentConfig]
    ) -> list[Any]:
        """Create engines from player configurations."""
        return create_generic_chess_engines(player_configs)

    @model_validator(mode="after")
    def finalize_config(self) -> "ChessConfig":
        """Finalize configuration after engine setup."""
        # Call parent validator first
        super().configure_engines()

        # Ensure proper recursion configuration
        self.runnable_config = RecursionConfig.configure_runnable(
            runnable_config=self.runnable_config,
            game_name="chess",
            enable_analysis=self.enable_analysis,
        )

        # Update player names if not set
        if not self.white_player_name and self.engines:
            # Try to extract from engines
            for engine in self.engines:
                if hasattr(engine, "prompt_template") and "white" in str(
                    engine.prompt_template
                ):
                    self.white_player_name = "White"
                    break

        if not self.black_player_name and self.engines:
            for engine in self.engines:
                if hasattr(engine, "prompt_template") and "black" in str(
                    engine.prompt_template
                ):
                    self.black_player_name = "Black"
                    break

        return self

    class Config:
        """Pydantic configuration.

        This inner class configures Pydantic behavior for the ChessAgentConfig.

        Attributes:
            arbitrary_types_allowed (bool): Whether to allow arbitrary types in the model.
        """

        arbitrary_types_allowed = True


# ChessConfig is now the main class (no alias needed)
