# src/haive/games/checkers/models.py

from typing import List, Dict, Optional, Union, Literal
from pydantic import BaseModel, Field, computed_field

class CheckersMove(BaseModel):
    """
    Represents a move in checkers.
    
    Attributes:
        from_position: Starting position in algebraic notation (e.g., "a3")
        to_position: Ending position in algebraic notation (e.g., "b4")
        player: The player making the move ("red" or "black")
        is_jump: Whether this is a jump move
        captured_position: Position of the captured piece (if any)
    """
    from_position: str = Field(..., description="Starting position in algebraic notation")
    to_position: str = Field(..., description="Ending position in algebraic notation")
    player: Literal["red", "black"] = Field(..., description="Player making the move")
    is_jump: bool = Field(default=False, description="Whether this is a jump move")
    captured_position: Optional[str] = Field(default=None, description="Position of captured piece if any")
    
    def __str__(self) -> str:
        """String representation of the move."""
        if self.is_jump:
            return f"{self.from_position}x{self.to_position}"
        return f"{self.from_position}-{self.to_position}"

class CheckersPlayerDecision(BaseModel):
    """
    Player's decision for a move in checkers.
    
    Attributes:
        move: The chosen move
        reasoning: Reasoning for the move choice
        evaluation: Position evaluation
        alternatives: Alternative moves considered
    """
    move: CheckersMove = Field(..., description="The chosen move")
    reasoning: str = Field(..., description="Reasoning for the move choice")
    evaluation: str = Field(..., description="Position evaluation")
    alternatives: List[str] = Field(default_factory=list, description="Alternative moves considered")

class CheckersAnalysis(BaseModel):
    """
    Analysis of a checkers position.
    
    Attributes:
        material_advantage: Assessment of material advantage
        control_of_center: Assessment of center control
        suggested_moves: List of suggested moves
        positional_evaluation: Overall position evaluation
    """
    material_advantage: str = Field(..., description="Assessment of material advantage")
    control_of_center: str = Field(..., description="Assessment of center control")
    suggested_moves: List[str] = Field(default_factory=list, description="List of suggested moves")
    positional_evaluation: str = Field(..., description="Overall position evaluation")
