"""Base state module for game agents.

This module provides the foundational state class for game agents,
defining the core state attributes that all games need to track.

Example:
    >>> state = GameState(
    ...     turn="player1",
    ...     game_status="ongoing",
    ...     move_history=[]
    ... )

Typical usage:
    - Inherit from GameState to create game-specific state classes
    - Use as the state schema in game configurations
    - Track game progress and history
"""

from typing import Any, List, Optional
from pydantic import BaseModel, Field
from abc import ABC, abstractmethod

class GameState(BaseModel, ABC):
    """Base game state that all game states should inherit from.
    
    This class defines the core state attributes that all games need to track,
    including the current turn, game status, move history, and error handling.
    
    Attributes:
        players (List[str]): List of players in the game.
        turn (str): Current player's turn.
        game_status (str): Status of the game (e.g., "ongoing", "finished").
        move_history (List[Any]): History of moves made in the game.
        error_message (Optional[str]): Error message if any error occurred.
    """

    players: List[str] = Field(
        default_factory=list,
        description="List of players"
    )
    
    turn: str = Field(
        default_factory=str,
        description="Current player's turn"
    )
    
    game_status: str = Field(
        default="ongoing",
        description="Status of the game"
    )
    
    move_history: List[Any] = Field(
        default_factory=list,
        description="History of moves"
    )
    
    error_message: Optional[str] = Field(
        default=None,
        description="Error message if any"
    )

    class Config:
        arbitrary_types_allowed = True

    @classmethod
    @abstractmethod
    def initialize(cls, **kwargs) -> "GameState":
        """
        Abstract method that all subclasses must implement to initialize the game state.
        
        Returns:
            GameState: A fully initialized game state object.
        
        Example:
            >>> return Connect4State.initialize(first_player="red")
        """
        pass
