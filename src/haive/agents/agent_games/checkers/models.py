from typing import List, Tuple, Literal, Optional
from pydantic import BaseModel, Field, validator

class CheckersMove(BaseModel):
    """Represents a move in Checkers."""
    start_pos: Tuple[int, int] = Field(..., description="Starting position of the piece (row, col).")
    end_pos: Tuple[int, int] = Field(..., description="Ending position of the piece (row, col).")
    is_jump: bool = Field(..., description="Indicates if the move is a jump over an opponent's piece.")

    @validator('start_pos', 'end_pos')
    def validate_positions(cls, value):
        row, col = value
        if not (0 <= row < 8 and 0 <= col < 8):
            raise ValueError(f"Position {value} is out of bounds for an 8x8 board.")
        return value

class CheckersPlayerAnalysis(BaseModel):
    """Represents a player's analysis in Checkers."""
    piece_count: int = Field(..., description="Number of pieces the player has on the board.")
    king_count: int = Field(..., description="Number of king pieces the player has.")
    possible_moves: List[CheckersMove] = Field(default_factory=list, description="List of possible moves.")
    strategy_notes: Optional[str] = Field(None, description="Player's strategic considerations.")
