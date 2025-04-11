"""
Monopoly game state model.

This module provides the state model for the Monopoly game, including:
    - Game state tracking
    - Player and property state
    - Game status updates
"""

from typing import Dict, List, Optional, Tuple, Union, Any
from pydantic import BaseModel, Field, computed_field

from src.haive.games.monopoly.models import (
    PropertyInfo,
    SpecialCardInfo,
    PlayerInfo,
    DiceInfo,
    StrategyAnalysis,
    TurnDecision
)

class MonopolyState(BaseModel):
    """
    Represents the complete state of the Monopoly game.
    This model tracks all the information needed to render and update the game.
    """
    # Core game state
    properties: Dict[str, PropertyInfo] = Field(
        default_factory=dict, 
        description="The properties on the board"
    )
    special_cards: Dict[str, SpecialCardInfo] = Field(
        default_factory=dict, 
        description="The special cards on the board (railroads, utilities)"
    )
    players: List[PlayerInfo] = Field(
        default_factory=list, 
        description="The players in the game"
    )
    current_player_index: int = Field(
        default=0, 
        description="The index of the current player"
    )
    
    # Turn-specific state
    dice: Optional[DiceInfo] = Field(
        None, 
        description="The last rolled dice"
    )
    has_rolled: bool = Field(
        default=False, 
        description="Whether the dice has been rolled this turn"
    )
    
    # Game events
    recent_events: List[str] = Field(
        default_factory=list, 
        description="The recent events in the game"
    )
    
    # Cards drawn
    community_chest_drawn: Optional[str] = Field(
        None, 
        description="The community chest card drawn"
    )
    chance_drawn: Optional[str] = Field(
        None, 
        description="The chance card drawn"
    )
    
    # Decision state
    turn_decision: Optional[TurnDecision] = Field(
        None, 
        description="The current turn decision"
    )
    strategy_analysis: Optional[StrategyAnalysis] = Field(
        None, 
        description="The current strategic analysis"
    )
    
    # Error handling
    error_message: Optional[str] = Field(
        None, 
        description="Error message if any"
    )
    
    @computed_field
    def active_players(self) -> int:
        """Get the number of active (non-bankrupt) players."""
        return sum(1 for p in self.players if not p.bankruptcy_status)
    
    @computed_field
    def game_over(self) -> bool:
        """Check if the game is over."""
        return self.active_players <= 1
    
    @computed_field
    def winner(self) -> Optional[PlayerInfo]:
        """Get the winner if the game is over."""
        if self.game_over and self.active_players == 1:
            # Find the non-bankrupt player
            for player in self.players:
                if not player.bankruptcy_status:
                    return player
        return None
    
    def get_current_player(self) -> PlayerInfo:
        """Get the current player."""
        if not self.players or len(self.players) <= self.current_player_index:
            # Return a default player if missing
            return PlayerInfo(
                name=f"Player {self.current_player_index + 1}", 
                index=self.current_player_index,
                position=0,
                cash=1500,
                total_wealth=1500,
                properties_owned=[]
            )
        return self.players[self.current_player_index]
    
    def get_opponent(self) -> PlayerInfo:
        """Get the opponent player in a two-player game."""
        if not self.players or len(self.players) < 2:
            # Return a default opponent if missing
            opponent_index = 1 if self.current_player_index == 0 else 0
            return PlayerInfo(
                name=f"Player {opponent_index + 1}", 
                index=opponent_index,
                position=0,
                cash=1500,
                total_wealth=1500,
                properties_owned=[]
            )
        
        # In a multi-player game, get the next active player
        next_idx = (self.current_player_index + 1) % len(self.players)
        while next_idx != self.current_player_index:
            if not self.players[next_idx].bankruptcy_status:
                return self.players[next_idx]
            next_idx = (next_idx + 1) % len(self.players)
        
        # Fallback to first player that's not current
        for player in self.players:
            if player.index != self.current_player_index:
                return player
        
        # Last resort fallback
        return PlayerInfo(
            name="Opponent", 
            index=1,
            position=0,
            cash=1500,
            total_wealth=1500,
            properties_owned=[]
        )
    
    def get_property_at_position(self, position: int) -> Optional[Union[PropertyInfo, SpecialCardInfo]]:
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
    
    def get_properties_by_color(self, color: str) -> List[PropertyInfo]:
        """Get all properties belonging to a specific color group."""
        return [prop for prop in self.properties.values() if prop.color == color]
    
    def add_event(self, event: str) -> None:
        """Add a new event to the recent events list (max 10)."""
        self.recent_events.append(event)
        if len(self.recent_events) > 10:
            self.recent_events.pop(0)
    
    def roll_dice(self, dice_values: Tuple[int, int]) -> None:
        """Record a dice roll."""
        self.dice = DiceInfo(
            values=dice_values, 
            sum=sum(dice_values)
        )
        self.has_rolled = True
    
    def player_owns_all_in_color(self, player_index: int, color: str) -> bool:
        """Check if a player owns all properties in a color group."""
        properties = self.get_properties_by_color(color)
        if not properties:
            return False
        return all(prop.owner == player_index for prop in properties)
    
    def can_build_house(self, property_name: str) -> bool:
        """Check if houses can be built on a property."""
        if property_name not in self.properties:
            return False
            
        prop = self.properties[property_name]
        
        # Must be owned
        if prop.owner is None:
            return False
            
        # Must not be mortgaged
        if prop.is_mortgaged:
            return False
            
        # Must not already have 5 houses (hotel)
        if prop.houses >= 5:
            return False
            
        # Must have monopoly on color group
        if not self.player_owns_all_in_color(prop.owner, prop.color):
            return False
            
        # Check even build rule (optional in this implementation)
        return True
    
    def can_mortgage(self, property_name: str) -> bool:
        """Check if a property can be mortgaged."""
        # Check if it's a regular property
        if property_name in self.properties:
            prop = self.properties[property_name]
            
            # Must be owned
            if prop.owner is None:
                return False
                
            # Must not already be mortgaged
            if prop.is_mortgaged:
                return False
                
            # Must not have houses
            if prop.houses > 0:
                return False
                
            return True
            
        # Check if it's a special card
        elif property_name in self.special_cards:
            card = self.special_cards[property_name]
            
            # Must be owned
            if card.owner is None:
                return False
                
            # Must not already be mortgaged
            if card.is_mortgaged:
                return False
                
            return True
            
        return False