from typing import List, Dict, Literal, Optional, Tuple
from pydantic import BaseModel, Field, field_validator
import sente


class GoMoveModel(BaseModel):
    """Represents a structured Go move as (row, col) coordinates."""
    move: Tuple[int, int] = Field(..., description="Move (row, col) on the board.")
    board_size: int = Field(default=19, description="Board size, default is 19x19.")

    @field_validator("move")
    def validate_move(cls, move: Tuple[int, int], values):
        """Ensures move is within board bounds."""
        row, col = move
        board_size = values.get("board_size", 19)

        if not (0 <= row < board_size and 0 <= col < board_size):
            raise ValueError(f"Move {move} is out of bounds for a {board_size}x{board_size} board.")

        return move

    def to_tuple(self) -> Tuple[int, int]:
        """Converts model to tuple representation."""
        return self.move
class GoPlayerDecision(BaseModel):
    """Player agent's decision on the next move."""
    move: GoMoveModel = Field(..., description="Move decision.")

class GoAnalysis(BaseModel):
    """Stores a Go position's evaluation and strategy analysis."""
    territory_control: Dict[Literal["black", "white"], int] = Field(
        ..., description="Estimated control for each player."
    )
    strong_positions: List[Tuple[int, int]] = Field(default_factory=list, description="Key strong positions.")
    weak_positions: List[Tuple[int, int]] = Field(default_factory=list, description="Vulnerable positions.")
    suggested_strategies: List[str] = Field(default_factory=list, description="Strategic insights.")
