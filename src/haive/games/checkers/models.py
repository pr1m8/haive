# src/haive/agents/agent_games/checkers/models.py

from typing import List, Dict, Literal, Optional, Tuple, Union
from pydantic import BaseModel, Field, field_validator
from src.haive.games.framework.base import GameState

class CheckersMove(BaseModel):
    """Represents a move in checkers."""
    from_pos: Tuple[int, int] = Field(..., description="Starting position (row, col)")
    to_pos: Tuple[int, int] = Field(..., description="Ending position (row, col)")
    captures: List[Tuple[int, int]] = Field(default_factory=list, description="Positions of captured pieces")
    
    @field_validator("from_pos", "to_pos", mode="after")
    def validate_positions(cls, v):
        row, col = v
        if not (0 <= row < 8 and 0 <= col < 8):
            raise ValueError(f"Position {v} is out of bounds")
        return v
    
    def __str__(self):
        capture_str = f" capturing {self.captures}" if self.captures else ""
        return f"{self.from_pos} → {self.to_pos}{capture_str}"

class CheckersPlayerDecision(BaseModel):
    """Player's decision on the next move."""
    move: CheckersMove = Field(..., description="The chosen move")
    reasoning: Optional[str] = Field(default=None, description="Reasoning behind the move")

class CheckersAnalysis(BaseModel):
    """Analysis of a checkers position."""
    material_advantage: int = Field(..., description="Material advantage in pieces (positive favors red)")
    control_of_center: str = Field(..., description="Assessment of center control")
    king_count: Dict[str, int] = Field(..., description="Number of kings for each player")
    mobility: Dict[str, int] = Field(..., description="Number of legal moves for each player")
    threatened_pieces: List[Tuple[int, int]] = Field(default_factory=list, description="Pieces that can be captured")
    suggested_moves: List[str] = Field(default_factory=list, description="Suggested moves with brief reasoning")

class CheckersPiece(BaseModel):
    """Represents a checkers piece."""
    color: Literal["red", "black"] = Field(..., description="Piece color")
    is_king: bool = Field(default=False, description="Whether the piece is a king")

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