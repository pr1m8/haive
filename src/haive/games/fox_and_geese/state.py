"""
State for the Fox and Geese game.

This module defines the state for the Fox and Geese game,
which includes the fox's position, the geese's positions,
the current player's turn, the game status, the move history,
the winner, and the number of geese remaining.
"""
from src.haive.games.framework.base.state import GameState
from pydantic import Field
from typing import Literal, List, Optional, Set
from src.haive.games.fox_and_geese.models import FoxAndGeesePosition, FoxAndGeeseMove   

class FoxAndGeeseState(GameState):
    """State for a Fox and Geese game.

    This class defines the structure of the Fox and Geese game state,
    which includes the fox's position, the geese's positions,
    the current player's turn, the game status, the move history,
    the winner, and the number of geese remaining.
    """
    fox_position: FoxAndGeesePosition = Field(..., description="Position of the fox")
    geese_positions: Set[FoxAndGeesePosition] = Field(..., description="Positions of geese")
    turn: Literal["fox", "geese"] = Field(..., description="Current player's turn")
    game_status: Literal["ongoing", "fox_win", "geese_win"] = Field(
        default="ongoing", description="Status of the game"
    )
    move_history: List[FoxAndGeeseMove] = Field(
        default_factory=list, description="History of moves"
    )
    winner: Optional[str] = Field(
        default=None, description="Winner of the game, if any"
    )
    num_geese: int = Field(default=0, description="Number of geese remaining")
    
    @property
    def board_string(self) -> str:
        """Get a string representation of the board."""
        # Create an empty 7x7 board
        board = [[" " for _ in range(7)] for _ in range(7)]
        
        # Place the fox
        board[self.fox_position.row][self.fox_position.col] = "F"
        
        # Place the geese
        for goose in self.geese_positions:
            board[goose.row][goose.col] = "G"
        
        # Convert to string
        result = "  0 1 2 3 4 5 6\n"
        for i, row in enumerate(board):
            result += f"{i} {' '.join(row)}\n"
        
        return result
    