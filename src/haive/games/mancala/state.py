from src.haive.games.framework.base.state import GameState          
from src.haive.games.mancala.models import MancalaMove
from typing import List, Literal, Optional
from pydantic import BaseModel, Field

class MancalaState(GameState):
    """State for a Mancala game."""
    # The board has 14 pits:
    # - Indices 0-5: Player 1's pits (bottom row, left to right)
    # - Index 6: Player 1's store (right)
    # - Indices 7-12: Player 2's pits (top row, right to left)
    # - Index 13: Player 2's store (left)
    board: List[int] = Field(..., min_items=14, max_items=14, description="Game board")
    turn: Literal["player1", "player2"] = Field(..., description="Current player's turn")
    game_status: Literal["ongoing", "player1_win", "player2_win", "draw"] = Field(
        default="ongoing", description="Status of the game"
    )
    move_history: List[MancalaMove] = Field(
        default_factory=list, description="History of moves"
    )
    free_turn: bool = Field(default=False, description="Whether player gets an extra turn")
    winner: Optional[str] = Field(
        default=None, description="Winner of the game, if any"
    )
    
    @property
    def player1_score(self) -> int:
        """Get player 1's score (store)."""
        return self.board[6]
    
    @property
    def player2_score(self) -> int:
        """Get player 2's score (store)."""
        return self.board[13]
    
    @property
    def board_string(self) -> str:
        """Get a string representation of the board."""
        result = "    "
        # Player 2's pits (reversed)
        for i in range(12, 6, -1):
            result += f"{self.board[i]:2d} "
        result += "\n"
        
        # Stores
        result += f"{self.board[13]:2d}" + " " * 20 + f"{self.board[6]:2d}\n"
        
        # Player 1's pits
        result += "    "
        for i in range(0, 6):
            result += f"{self.board[i]:2d} "
        result += "\n\n"
        
        result += f"Player 1 (bottom): {self.player1_score}  |  Player 2 (top): {self.player2_score}"
        return result
