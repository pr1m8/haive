from pydantic import BaseModel, Field       
from typing import List, Optional, Dict, Any
from .models import Card, PlayerState

class BullshitGameState(BaseModel):
    """Represents the overall state of a Bullshit game."""
    players: List[PlayerState] = Field(default_factory=list)
    current_pile: List[Card] = Field(default_factory=list)
    current_claimed_value: Optional[str] = None
    current_player_index: int = Field(default=0)
    game_status: str = Field(default="ongoing")
    winner: Optional[str] = None
    last_played_cards: List[Card] = Field(default_factory=list)
    challenge_history: List[Dict[str, Any]] = Field(default_factory=list)