from pydantic import BaseModel, Field, field_validator
from typing import Literal

class MancalaMove(BaseModel):
    """Represents a move in Mancala."""
    pit_index: int = Field(..., ge=0, lt=6, description="Index of the pit to sow from (0-5)")
    player: Literal["player1", "player2"] = Field(..., description="Player making the move")
    
    @field_validator('pit_index')
    def validate_pit_index(cls, v, values):
        """Validate that the pit index is valid for the player."""
        if 'player' in values.data:
            # Adjust validation based on player
            if values.data['player'] == 'player1' and not (0 <= v < 6):
                raise ValueError(f"Player 1 pit index must be 0-5, got {v}")
            elif values.data['player'] == 'player2' and not (0 <= v < 6):
                raise ValueError(f"Player 2 pit index must be 0-5, got {v}")
        return v
    
    def __str__(self):
        return f"{self.player} sows from pit {self.pit_index}"
