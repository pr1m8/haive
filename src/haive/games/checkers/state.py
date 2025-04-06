
from typing import List, Optional, Dict, Literal
from pydantic import BaseModel, Field
from src.haive.games.checkers.models import CheckersMove


class CheckersState(BaseModel):
    """
    State representation for the checkers game.
    
    Attributes:
        board: 2D grid representation of the board (0=empty, 1=red, 2=red king, 3=black, 4=black king)
        board_string: String representation of the board for display
        turn: Current player's turn
        move_history: History of moves played
        game_status: Status of the game
        winner: Winner of the game (if any)
        red_analysis: Analysis history for red player
        black_analysis: Analysis history for black player
        captured_pieces: Record of captured pieces by each player
    """
    board: List[List[int]] = Field(..., description="2D grid representation of the board")
    board_string: str = Field(..., description="String representation of the board")
    turn: Literal["red", "black"] = Field(default="red", description="Current player's turn")
    move_history: List[CheckersMove] = Field(default_factory=list, description="History of moves")
    game_status: Literal["ongoing", "game_over"] = Field(default="ongoing", description="Status of the game")
    winner: Optional[Literal["red", "black"]] = Field(default=None, description="Winner of the game")
    red_analysis: List[Dict] = Field(default_factory=list, description="Analysis history for red player")
    black_analysis: List[Dict] = Field(default_factory=list, description="Analysis history for black player")
    captured_pieces: Dict[str, List[str]] = Field(
        default_factory=lambda: {"red": [], "black": []},
        description="Record of captured pieces by each player"
    )
    
    def model_dump(self) -> Dict:
        """Convert to dictionary representation."""
        result = super().model_dump()
        return result
    
    def dict(self) -> Dict:
        """Legacy compatibility method."""
        return self.model_dump()
    
    class Config:
        """Pydantic configuration."""
        arbitrary_types_allowed = True