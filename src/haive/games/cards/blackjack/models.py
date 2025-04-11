from typing import List, Optional, Literal, Dict, Any
from pydantic import BaseModel, Field
from enum import Enum

class CardSuit(str, Enum):
    HEARTS = "hearts"
    DIAMONDS = "diamonds"
    CLUBS = "clubs"
    SPADES = "spades"

class Card(BaseModel):
    """Represents a playing card."""
    value: str
    suit: CardSuit
    
    def __str__(self) -> str:
        return f"{self.value} of {self.suit.value}"
    
    def point_value(self) -> int:
        """Calculate point value of the card."""
        if self.value in ['J', 'Q', 'K']:
            return 10
        elif self.value == 'A':
            return 11
        else:
            return int(self.value)

class PlayerAction(BaseModel):
    """Represents a player's action in Blackjack."""
    action: Literal["hit", "stand", "double_down", "split", "surrender"] = Field(
        ..., 
        description="Player's chosen action"
    )
    reasoning: Optional[str] = Field(
        default=None, 
        description="Reasoning behind the action"
    )

class PlayerHand(BaseModel):
    """Represents a player's hand in Blackjack."""
    cards: List[Card] = Field(default_factory=list)
    is_split: bool = Field(default=False)
    is_active: bool = Field(default=True)
    bet: float = Field(default=0.0)
    
    def total_value(self) -> int:
        """Calculate the total value of the hand."""
        total = sum(card.point_value() for card in self.cards)
        
        # Adjust for Aces
        num_aces = sum(1 for card in self.cards if card.value == 'A')
        while total > 21 and num_aces:
            total -= 10
            num_aces -= 1
        
        return total
    
    def is_bust(self) -> bool:
        """Check if the hand is bust."""
        return self.total_value() > 21
    
    def is_blackjack(self) -> bool:
        """Check if the hand is a blackjack."""
        return len(self.cards) == 2 and self.total_value() == 21

class PlayerState(BaseModel):
    """Represents a player's state in the game."""
    name: str
    hands: List[PlayerHand] = Field(default_factory=list)
    total_chips: float = Field(default=1000.0)
    current_bet: float = Field(default=0.0)
    is_active: bool = Field(default=True)
    
    def add_hand(self, hand: PlayerHand):
        """Add a hand to the player's state."""
        self.hands.append(hand)

class BlackjackGameState(BaseModel):
    """Represents the overall state of a Blackjack game."""
    players: List[PlayerState] = Field(default_factory=list)
    dealer_hand: List[Card] = Field(default_factory=list)
    current_player_index: int = Field(default=0)
    current_hand_index: int = Field(default=0)
    deck: List[Card] = Field(default_factory=list)
    game_status: Literal["betting", "playing", "dealer_turn", "game_over"] = Field(default="betting")
    round_winner: Optional[str] = Field(default=None)