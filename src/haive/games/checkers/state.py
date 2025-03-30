
from typing import List, Optional, Dict, Literal
from pydantic import BaseModel, Field
from src.haive.games.checkers.models import CheckersPiece, CheckersMove
class CheckersState(GameState):
    """State for a checkers game."""
    board: List[List[Optional[CheckersPiece]]] = Field(
        ..., description="8x8 board representation"
    )
    turn: Literal["red", "black"] = Field(..., description="Current player's turn")
    game_status: Literal["ongoing", "red_win", "black_win", "draw"] = Field(
        default="ongoing", description="Status of the game"
    )
    move_history: List[CheckersMove] = Field(
        default_factory=list, description="History of moves"
    )
    captured_pieces: Dict[str, int] = Field(
        default_factory=lambda: {"red": 0, "black": 0},
        description="Count of captured pieces for each player"
    )
    red_analysis: List[Dict] = Field(
        default_factory=list, description="Analysis history for red player"
    )
    black_analysis: List[Dict] = Field(
        default_factory=list, description="Analysis history for black player"
    )
    
    @property
    def active_player(self) -> str:
        """Get the current active player."""
        return self.turn
    
    @property
    def board_string(self) -> str:
        """Get a string representation of the board."""
        result = []
        result.append("    0   1   2   3   4   5   6   7  ")
        result.append("  +---+---+---+---+---+---+---+---+")
        
        for i, row in enumerate(self.board):
            row_str = f"{i} |"
            for j, piece in enumerate(row):
                if piece is None:
                    # Use different background for black squares
                    if (i + j) % 2 == 1:
                        cell = " . "
                    else:
                        cell = "   "
                else:
                    if piece.color == "red":
                        symbol = "R" if piece.is_king else "r"
                    else:
                        symbol = "B" if piece.is_king else "b"
                    cell = f" {symbol} "
                row_str += cell + "|"
            result.append(row_str)
            result.append("  +---+---+---+---+---+---+---+---+")
        
        return "\n".join(result)