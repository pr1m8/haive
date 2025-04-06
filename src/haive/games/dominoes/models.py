from typing import List, Dict, Set, Optional, Literal, Union
from pydantic import BaseModel, Field
from src.haive.games.framework.base.state import GameState

class DominoTile(BaseModel):
    """A domino tile with two values."""
    left: int = Field(..., ge=0, le=6, description="Left value (0-6)")
    right: int = Field(..., ge=0, le=6, description="Right value (0-6)")
    
    def is_double(self) -> bool:
        """Check if this is a double (same value on both sides)."""
        return self.left == self.right
    
    def sum(self) -> int:
        """Get the sum of both values."""
        return self.left + self.right
    
    def reversed(self) -> 'DominoTile':
        """Get a new tile with left and right values swapped."""
        return DominoTile(left=self.right, right=self.left)
    
    def __str__(self) -> str:
        """String representation of the tile."""
        return f"[{self.left}|{self.right}]"
    
    def __eq__(self, other) -> bool:
        """Check if two tiles are equal (ignoring order)."""
        if not isinstance(other, DominoTile):
            return False
        return (self.left == other.left and self.right == other.right) or \
               (self.left == other.right and self.right == other.left)

class DominoMove(BaseModel):
    """A move in dominoes."""
    tile: DominoTile = Field(..., description="The tile to play")
    location: Literal["left", "right"] = Field(..., description="Where to play the tile")
    
    def __str__(self) -> str:
        """String representation of the move."""
        return f"Play {self.tile} on the {self.location} end"

class DominoesPlayerDecision(BaseModel):
    """A player's decision in dominoes."""
    move: Optional[DominoMove] = Field(default=None, description="The move to make, if any")
    pass_turn: bool = Field(default=False, description="Whether to pass the turn")
    reasoning: str = Field(..., description="Reasoning for the decision")
    
    def __str__(self) -> str:
        """String representation of the decision."""
        if self.pass_turn:
            return f"Pass the turn. Reasoning: {self.reasoning}"
        return f"Make move: {self.move}. Reasoning: {self.reasoning}"

class DominoesAnalysis(BaseModel):
    """Analysis of a dominoes position."""
    hand_strength: int = Field(..., ge=1, le=10, description="Overall hand strength (1-10)")
    pip_count_assessment: str = Field(..., description="Assessment of the pip count")
    open_ends: List[str] = Field(..., description="Analysis of open end values")
    missing_values: List[int] = Field(..., description="Values not in the player's hand")
    suggested_strategy: str = Field(..., description="Strategic recommendations")
    blocking_potential: str = Field(..., description="Potential for blocking opponent")
    reasoning: str = Field(..., description="Detailed reasoning for the analysis")
