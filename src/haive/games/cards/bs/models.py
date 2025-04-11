from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from enum import Enum
import random

class CardSuit(str, Enum):
    HEARTS = "hearts"
    DIAMONDS = "diamonds"
    CLUBS = "clubs"
    SPADES = "spades"

class Card(BaseModel):
    """Represents a playing card."""
    value: str  # 2-10, J, Q, K, A
    suit: CardSuit
    
    def __str__(self) -> str:
        return f"{self.value} of {self.suit.value}"
    
    @classmethod
    def create_deck(cls) -> List['Card']:
        """Create a full deck of 52 cards."""
        suits = list(CardSuit)
        values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        deck = [cls(value=value, suit=suit) for suit in suits for value in values]
        random.shuffle(deck)
        return deck

class PlayerClaimAction(BaseModel):
    """Represents a player's claim during their turn."""
    claimed_value: str = Field(..., description="The value of cards being claimed")
    number_of_cards: int = Field(..., description="Number of cards being played")
    is_truth: bool = Field(..., description="Whether the player is telling the truth")
    reasoning: Optional[str] = Field(default=None, description="Reasoning behind the claim")

class ChallengeAction(BaseModel):
    """Represents a player challenging another player's claim."""
    challenge_type: str = Field(..., description="Type of challenge")
    target_player_index: int = Field(..., description="Index of the player being challenged")
    reasoning: Optional[str] = Field(default=None, description="Reasoning behind the challenge")

class PlayerState(BaseModel):
    """Represents a player's state in the Bullshit game."""
    name: str
    hand: List[Card] = Field(default_factory=list)
    cards_played: List[Card] = Field(default_factory=list)
    
    def play_cards(self, cards: List[Card]) -> None:
        """Remove played cards from hand."""
        for card in cards:
            self.hand.remove(card)
            self.cards_played.append(card)
