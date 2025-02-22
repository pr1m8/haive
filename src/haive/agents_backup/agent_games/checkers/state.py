from typing import List, Dict, Literal, Optional, Tuple
from pydantic import BaseModel, Field
from enum import Enum
from src.haive.agents.agent_games.checkers.models import CheckersMove, CheckersPlayerAnalysis
class PieceType(str, Enum):
    MAN = "man"
    KING = "king"

class PieceColor(str, Enum):
    RED = "red"
    BLACK = "black"

class CheckersPiece(BaseModel):
    """Represents a piece on the Checkers board."""
    type: PieceType = Field(..., description="Type of the piece (man or king).")
    color: PieceColor = Field(..., description="Color of the piece (red or black).")

class CheckersGameState(BaseModel):
    """Represents the state of a Checkers game."""
    board: List[List[Optional[CheckersPiece]]] = Field(..., description="8x8 board with pieces.")
    move_history: List[CheckersMove] = Field(default_factory=list, description="History of moves made.")
    current_turn: PieceColor = Field(..., description="The color of the player to move.")
    game_status: Literal["ongoing", "red_wins", "black_wins", "draw"] = Field(default="ongoing", description="Current status of the game.")
    red_analysis: Optional[CheckersPlayerAnalysis] = Field(None, description="Analysis from the red player's perspective.")
    black_analysis: Optional[CheckersPlayerAnalysis] = Field(None, description="Analysis from the black player's perspective.")
    error_message: Optional[str] = Field(None, description="Error message for invalid moves or states.")

    @staticmethod
    def initialize_board() -> List[List[Optional[CheckersPiece]]]:
        """Initializes the Checkers board with pieces in starting positions."""
        board = [[None for _ in range(8)] for _ in range(8)]
        for row in range(3):
            for col in range(8):
                if (row + col) % 2 == 1:
                    board[row][col] = CheckersPiece(type=PieceType.MAN, color=PieceColor.BLACK)
        for row in range(5, 8):
            for col in range(8):
                if (row + col) % 2 == 1:
                    board[row][col] = CheckersPiece(type=PieceType.MAN, color=PieceColor.RED)
        return board

    @classmethod
    def new_game(cls) -> 'CheckersGameState':
        """Creates a new game state with the initial board setup."""
        return cls(
            board=cls.initialize_board(),
            current_turn=PieceColor.RED
        )
