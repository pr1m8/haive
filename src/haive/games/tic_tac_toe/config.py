"""
Configuration model for the Tic Tac Toe game agent.

This module defines a Pydantic-based configuration used to initialize
and control the behavior of the Tic Tac Toe game agent, including engine
settings, game setup, and display options.
"""

from src.haive.games.framework.base.config import GameConfig
from src.haive.games.tic_tac_toe.state import TicTacToeState
from src.haive.games.tic_tac_toe.engines import tictactoe_engines
from typing import Dict, Type, Literal
from pydantic import Field
from src.haive.core.engine.aug_llm import AugLLMConfig

class TicTacToeConfig(GameConfig):
    """
    Configuration for the Tic Tac Toe game agent.

    Attributes:
        name (str): Name identifier for the game.
        state_schema (Type[TicTacToeState]): State schema class for the game.
        engines (Dict[str, AugLLMConfig]): Engine configurations for move generation and analysis.
        enable_analysis (bool): Whether to perform post-move analysis.
        visualize (bool): Whether to print the board and actions at each step.
        first_player (Literal['X', 'O']): Symbol of the player who starts the game.
        player_X (Literal['player1', 'player2']): Identity of the player using 'X'.
        player_O (Literal['player1', 'player2']): Identity of the player using 'O'.
    """
    name: str = Field(default="tictactoe", description="Name of the game")
    state_schema: Type[TicTacToeState] = Field(default=TicTacToeState, description="State schema for Tic Tac Toe")
    engines: Dict[str, AugLLMConfig] = Field(
        default=tictactoe_engines, 
        description="Configs for the Tic Tac Toe engines"
    )
    enable_analysis: bool = Field(
        default=True, 
        description="Whether to enable position analysis"
    )
    visualize: bool = Field(
        default=True, 
        description="Whether to visualize the game"
    )
    first_player: Literal["X", "O"] = Field(
        default="X",
        description="Which symbol goes first"
    )
    player_X: Literal["player1", "player2"] = Field(
        default="player1",
        description="Which player uses X"
    )
    player_O: Literal["player1", "player2"] = Field(
        default="player2",
        description="Which player uses O"
    )

    @classmethod
    def default_config(cls):
        """
        Create a default configuration for a new Tic Tac Toe game.

        Returns:
            TicTacToeConfig: An instance of the default game configuration.
        """
        return cls(
            name="tictactoe",
            state_schema=TicTacToeState,
            engines=tictactoe_engines,
            enable_analysis=True,
            visualize=True,
            first_player="X",
            player_X="player1",
            player_O="player2"
        )