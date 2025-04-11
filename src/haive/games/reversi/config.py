"""
Configuration model for the Reversi (Othello) game agent.

Defines game metadata, initial settings, and engine bindings used to drive
the game loop and decision-making by language models.
"""

from src.haive.games.framework.base.config import GameConfig
from src.haive.games.reversi.state import ReversiState
from src.haive.games.reversi.engines import reversi_engines
from typing import Dict, Type, Literal
from pydantic import Field
from src.haive.core.engine.aug_llm import AugLLMConfig

class ReversiConfig(GameConfig):
    """
    Configuration for the Reversi/Othello game agent.

    Attributes:
        name (str): Name of the game.
        state_schema (Type[ReversiState]): The state model used for gameplay.
        engines (Dict[str, AugLLMConfig]): Mapping of engine names to LLM configurations.
        enable_analysis (bool): Whether to run post-move analysis.
        visualize (bool): Whether to render the board visually in the console.
        first_player (Literal['B', 'W']): Symbol of the player who starts (Black or White).
        player_B (Literal['player1', 'player2']): Who controls the Black pieces.
        player_W (Literal['player1', 'player2']): Who controls the White pieces.
    """
    name: str = Field(default="reversi", description="Name of the game")
    state_schema: Type[ReversiState] = Field(default=ReversiState, description="State schema for Reversi")
    engines: Dict[str, AugLLMConfig] = Field(
        default=reversi_engines,
        description="Configs for the Reversi engines"
    )
    enable_analysis: bool = Field(
        default=True,
        description="Whether to enable position analysis"
    )
    visualize: bool = Field(
        default=True,
        description="Whether to visualize the game"
    )
    first_player: Literal["B", "W"] = Field(
        default="B",
        description="Which symbol goes first (Black is traditional)"
    )
    player_B: Literal["player1", "player2"] = Field(
        default="player1",
        description="Which player uses Black"
    )
    player_W: Literal["player1", "player2"] = Field(
        default="player2",
        description="Which player uses White"
    )

    @classmethod
    def default_config(cls):
        """
        Create a default configuration for Reversi.

        Returns:
            ReversiConfig: An instance with standard engine bindings and player layout.
        """
        return cls(
            name="reversi",
            state_schema=ReversiState,
            engines=reversi_engines,
            enable_analysis=True,
            visualize=True,
            first_player="B",
            player_B="player1",
            player_W="player2"
        )