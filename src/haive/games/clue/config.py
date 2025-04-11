"""
Configuration for the Clue game agent.

This module defines the configuration for the Clue game agent,
including game state schema, engines, analysis settings, visualization,
and game parameters.
"""
from src.haive.games.framework.base.config import GameConfig
from src.haive.games.clue.state import ClueState
from typing import Dict, Type, List, Optional
from pydantic import Field

# Version information for tracking changes
VERSION = "1.0.0"

class ClueConfig(GameConfig):
    """Configuration for the Clue game agent.

    This class defines the configuration for the Clue game agent,
    including game state schema, engines, analysis settings, visualization,
    and game parameters.
    """
    name: str = Field(default="clue", description="Name of the game")
    version: str = Field(default=VERSION, description="Version of the game implementation")
    state_schema: Type[ClueState] = Field(default=ClueState)
    enable_analysis: bool = Field(
        default=True, 
        description="Whether to enable position analysis"
    )
    visualize: bool = Field(
        default=True, 
        description="Whether to visualize the game"
    )
    max_turns: int = Field(
        default=20, 
        description="Maximum number of turns"
    )
    first_player: str = Field(
        default="player1",
        description="Player who starts the game (player1 or player2)"
    )
    solution: Optional[Dict] = Field(
        default=None,
        description="Predetermined solution (if None, will be generated randomly)"
    ) 