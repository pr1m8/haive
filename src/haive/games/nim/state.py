from pydantic import BaseModel, Field
from typing import List, Optional, Literal
from src.haive.games.nim.models import NimMove, NimAnalysis

class NimState(BaseModel):
    """Represents the state of a Nim game."""
    piles: List[int] = Field(default=[3, 5, 7], description="Current sizes of the piles")
    turn: Literal["player1", "player2"] = Field(default="player1", description="Current player's turn")
    game_status: Literal["in_progress", "player1_win", "player2_win"] = Field(
        default="in_progress", description="Current status of the game"
    )
    move_history: List[NimMove] = Field(default_factory=list, description="History of moves")
    player1_analysis: List[NimAnalysis] = Field(default_factory=list, description="Analyses by player1")
    player2_analysis: List[NimAnalysis] = Field(default_factory=list, description="Analyses by player2")
    misere_mode: bool = Field(default=False, description="If True, player taking last stone loses")
    
    @property
    def board_string(self) -> str:
        """Return a string representation of the board."""
        result = []
        for i, pile_size in enumerate(self.piles):
            pile_str = "Pile " + str(i) + ": " + "O " * pile_size
            result.append(pile_str)
        return "\n".join(result)
    
    @property
    def is_game_over(self) -> bool:
        """Check if the game is over."""
        return self.game_status != "in_progress"
    
    @property
    def stones_left(self) -> int:
        """Return the total number of stones left."""
        return sum(self.piles)
    
    @property
    def nim_sum(self) -> int:
        """Calculate the nim-sum (XOR sum) of the pile sizes."""
        result = 0
        for pile_size in self.piles:
            result ^= pile_size
        return result