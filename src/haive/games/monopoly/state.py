from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Tuple, Union
from src.haive.games.monopoly.models import (
    PropertyInfo,
    SpecialCardInfo,
    PlayerInfo,
    DiceInfo
)

class MonopolyState(BaseModel):
    """
    Represents the complete state of the Monopoly game.
    This is separate from the state manager to allow for easier testing and serialization.
    """
    properties: Dict[str, PropertyInfo] = Field(default_factory=dict, description="The properties on the board")
    special_cards: Dict[str, SpecialCardInfo] = Field(default_factory=dict, description="The special cards on the board")
    players: List[PlayerInfo] = Field(default_factory=list, description="The players in the game")
    current_player_index: int = Field(default=0, description="The index of the current player")
    dice: Optional[DiceInfo] = Field(None, description="The last rolled dice")
    has_rolled: bool = Field(default=False, description="Whether the dice has been rolled")
    recent_events: List[str] = Field(default_factory=list, description="The recent events in the game")
    community_chest_drawn: Optional[str] = Field(None, description="The community chest card drawn")
    chance_drawn: Optional[str] = Field(None, description="The chance card drawn")
    
    def get_current_player(self) -> PlayerInfo:
        """Get the current player."""
        if not self.players or len(self.players) <= self.current_player_index:
            # Return a default player if missing
            return PlayerInfo(
                name=f"Player {self.current_player_index + 1}", 
                index=self.current_player_index,
                position=(0, 0),
                cash=15000,
                total_wealth=15000
            )
        return self.players[self.current_player_index]
    
    def get_opponent(self) -> PlayerInfo:
        """Get the opponent player (assumes 2 players)."""
        if not self.players or len(self.players) < 2:
            # Return a default opponent if missing
            opponent_index = 1 if self.current_player_index == 0 else 0
            return PlayerInfo(
                name=f"Player {opponent_index + 1}", 
                index=opponent_index,
                position=(0, 0),
                cash=15000,
                total_wealth=15000
            )
        
        opponent_index = 1 if self.current_player_index == 0 else 0
        try:
            return self.players[opponent_index]
        except IndexError:
            # Fallback if player doesn't exist
            return PlayerInfo(
                name=f"Player {opponent_index + 1}", 
                index=opponent_index,
                position=(0, 0),
                cash=15000,
                total_wealth=15000
            )
    
    def get_property_at_position(self, position: Tuple[int, int]) -> Optional[Union[PropertyInfo, SpecialCardInfo]]:
        """Get the property or special card at a specific position."""
        # Check regular properties
        for prop in self.properties.values():
            if prop.position == position:
                return prop
                
        # Check special cards
        for card in self.special_cards.values():
            if card.position == position:
                return card
                
        return None
    
    def get_properties_by_country(self, country: str) -> List[PropertyInfo]:
        """Get all properties belonging to a specific country."""
        return [prop for prop in self.properties.values() if prop.country == country]
    
    def add_event(self, event: str) -> None:
        """Add a new event to the recent events list (max 5)."""
        self.recent_events.append(event)
        if len(self.recent_events) > 5:
            self.recent_events.pop(0)
    
    def roll_dice(self, dice_values: Tuple[int, int]) -> None:
        """Record a dice roll."""
        self.dice = DiceInfo(
            values=dice_values, 
            sum=sum(dice_values),
            is_double=dice_values[0] == dice_values[1]
        )
        self.has_rolled = True