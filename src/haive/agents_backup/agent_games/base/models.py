from typing import List, Dict, Tuple, Literal, Optional, TypeVar, Generic
from pydantic import BaseModel, Field, field_validator

TMove = TypeVar("TMove")  # Generic move type

class MoveModel(BaseModel, Generic[TMove]):
    """Represents a structured move in a generic game."""
    move: TMove = Field(..., description="The move representation.")
    game_state: Optional[str] = Field(None, description="Game state at the time of move.")

    @field_validator("move")
    def validate_move(cls, move, info):
        """Override in game-specific models to validate the move."""
        return move

