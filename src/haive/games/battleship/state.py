from typing import List, Dict, Tuple, Optional, Any, Set
from pydantic import BaseModel, Field, model_validator

from src.haive.games.battleship.models import (
    Board, 
    Ship, 
    Coordinates, 
    BattleshipMoveModel,
    BattleshipPlacement
)

class PlayerPrivateState(BaseModel):
    """Private state information for a player."""
    board: Board = Field(default_factory=Board)
    strategic_thoughts: List[str] = Field(default_factory=list)

class BattleshipGameState(BaseModel):
    """
    Game state for Battleship.
    
    This class tracks the full game state including both players' boards,
    turn information, move history, and game status.
    """
    # Game configuration
    board_size: int = Field(default=10, description="Size of the game board")
    
    # Player states
    player1_private: PlayerPrivateState = Field(default_factory=PlayerPrivateState)
    player2_private: PlayerPrivateState = Field(default_factory=PlayerPrivateState)
    
    # Game state tracking
    turn: str = Field(default="player1", description="Current player's turn")
    move_history: List[Tuple[str, Tuple[int, int], str]] = Field(
        default_factory=list, 
        description="History of moves (player, (row, col), result)"
    )
    game_status: str = Field(default="ongoing", description="Status of the game (ongoing, ended)")
    game_result: Optional[str] = Field(default=None, description="Winner of the game (player1, player2, or None for draw)")
    error_message: Optional[str] = Field(default=None, description="Error message if any")
    
    class Config:
        arbitrary_types_allowed = True
    
    def model_copy(self, **kwargs):
        """Create a deep copy of the state."""
        copied = super().model_copy(**kwargs)
        # Ensure the move_history is properly copied
        copied.move_history = list(self.move_history)
        return copied