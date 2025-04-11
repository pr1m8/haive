"""
Models for the Fox and Geese game.

This module defines the models for the Fox and Geese game,
including the move and analysis models.
"""
from typing import List, Dict, Literal, Optional, Tuple, Union, Set
from pydantic import BaseModel, Field
from src.haive.games.framework.base import GameState, GameStateManager
import copy

class FoxAndGeesePosition(BaseModel):
    """Position on the Fox and Geese board.

    This class defines the structure of a position on the Fox and Geese board,
    which includes a row and column coordinate.
    """
    row: int = Field(..., ge=0, lt=7, description="Row (0-6)")
    col: int = Field(..., ge=0, lt=7, description="Column (0-6)")
    
    def __str__(self):
        return f"({self.row}, {self.col})"
    
    def __eq__(self, other):
        if not isinstance(other, FoxAndGeesePosition):
            return False
        return self.row == other.row and self.col == other.col
    
    def __hash__(self):
        return hash((self.row, self.col))

class FoxAndGeeseMove(BaseModel):
    """Represents a move in Fox and Geese.

    This class defines the structure of a move in Fox and Geese,
    which includes a starting position, an ending position,
    a piece type, and an optional captured position.
    """
    from_pos: FoxAndGeesePosition = Field(..., description="Starting position")
    to_pos: FoxAndGeesePosition = Field(..., description="Ending position")
    piece_type: Literal["fox", "goose"] = Field(..., description="Type of piece moved")
    capture: Optional[FoxAndGeesePosition] = Field(default=None, description="Position of captured goose, if any")
    
    def __str__(self):
        if self.capture:
            return f"{self.piece_type.capitalize()} moves from {self.from_pos} to {self.to_pos}, capturing at {self.capture}"
        return f"{self.piece_type.capitalize()} moves from {self.from_pos} to {self.to_pos}"
class FoxAndGeeseAnalysis(BaseModel):
    """Analysis of a Fox and Geese position.

    This class defines the structure of an analysis of a Fox and Geese position,
    which includes an advantage, an advantage level,
    key features, fox strategy, geese strategy,
    and critical squares.
    """
    advantage: Literal["fox", "geese", "equal"] = Field(
        ..., description="Which side has the advantage"
    )
    advantage_level: int = Field(
        ..., ge=0, le=10, description="Level of advantage (0-10)"
    )
    key_features: List[str] = Field(
        ..., description="Key strategic features of the position"
    )
    fox_strategy: str = Field(
        ..., description="Recommended strategy for the fox"
    )
    geese_strategy: str = Field(
        ..., description="Recommended strategy for the geese"
    )
    critical_squares: List[str] = Field(
        ..., description="Critical squares or formations in the position"
    )
    explanation: str = Field(
        ..., description="Detailed explanation of the analysis"
    )