"""
Monopoly game data models.

This module provides data models for the Monopoly game, including:
    - Property information
    - Player information
    - Decision models for LLM outputs
    - Game state models
"""

from typing import List, Dict, Optional, Tuple, Literal, Union, Any
from pydantic import BaseModel, Field, validator, model_validator

# ==============================================================
# Game State Models - Core data structures
# ==============================================================

class PropertyInfo(BaseModel):
    """Information about a property on the board."""
    name: str = Field(description="The name of the property")
    color: Optional[str] = Field(None, description="The color group of the property")
    position: int = Field(description="The position of the property on the board (0-39)")
    cost: int = Field(description="The purchase cost of the property")
    rent_values: List[int] = Field(description="The rent values based on number of houses/hotels")
    rent: int = Field(description="Current rent value for this property")
    mortgage_value: int = Field(description="The mortgage value of the property")
    owner: Optional[int] = Field(None, description="The player index who owns this property, if any")
    houses: int = Field(description="Number of houses on the property (5 = hotel)")
    is_mortgaged: bool = Field(description="Whether the property is mortgaged")

    @model_validator(mode='after')
    def check_houses(self):
        """Ensure houses is within valid range."""
        if self.houses < 0:
            self.houses = 0
        elif self.houses > 5:
            self.houses = 5
        return self


class SpecialCardInfo(BaseModel):
    """Information about special properties like railroads and utilities."""
    name: str = Field(description="The name of the card")
    card_type: Literal["railroad", "utility"] = Field(description="The type of the card")
    position: int = Field(description="The board position")
    cost: int = Field(description="The purchase cost")
    rent: int = Field(description="Current rent value")
    mortgage_value: int = Field(description="Mortgage value")
    owner: Optional[int] = Field(None, description="The player index who owns this")
    is_mortgaged: bool = Field(default=False, description="Whether the property is mortgaged")


class PlayerInfo(BaseModel):
    """Information about a player."""
    name: str = Field(description="Player's name")
    index: int = Field(description="Player index")
    position: int = Field(description="Current board position (0-39)")
    cash: int = Field(description="Current cash on hand")
    total_wealth: int = Field(description="Net worth including cash and property value")
    properties_owned: List[str] = Field(default_factory=list, description="Names of properties owned")
    is_in_jail: bool = Field(default=False, description="Is the player currently in jail")
    jail_cards: int = Field(default=0, description="Number of Get Out of Jail Free cards")
    railways_owned: int = Field(default=0, description="How many railroads this player owns")
    bankruptcy_status: bool = Field(default=False, description="Whether the player is bankrupt")


class DiceInfo(BaseModel):
    """Information about a dice roll."""
    values: Tuple[int, int] = Field(description="Two dice values")
    sum: int = Field(description="Sum of the dice roll")

    @property
    def is_double(self) -> bool:
        """Check if the roll is a double."""
        return self.values[0] == self.values[1]

    @model_validator(mode='after')
    def check_sum(self):
        """Ensure sum matches the dice values."""
        if self.sum != self.values[0] + self.values[1]:
            self.sum = self.values[0] + self.values[1]
        return self


# ==============================================================
# LLM Decision Models - For Agent Outputs
# ==============================================================

class PropertyAction(BaseModel):
    """Model for property management actions."""
    action_type: Literal["buy", "build", "sell", "mortgage", "unmortgage"] = Field(
        description="Action to take with property"
    )
    property_name: str = Field(description="Name of the property to act on")
    reasoning: str = Field(description="Reasoning behind this action")


class MoveAction(BaseModel):
    """Model for movement actions."""
    action_type: Literal["roll", "pay_to_exit_jail", "roll_for_double"] = Field(
        description="Type of move action"
    )
    reasoning: str = Field(description="Reasoning behind this move")


class TurnDecision(BaseModel):
    """Model for comprehensive turn decisions."""
    move_action: Optional[MoveAction] = Field(
        default=None, 
        description="Movement decision for this turn"
    )
    property_actions: List[PropertyAction] = Field(
        default_factory=list, 
        description="Property management actions for this turn"
    )
    end_turn: bool = Field(
        default=False, 
        description="Whether to end the turn after these actions"
    )
    reasoning: str = Field(
        description="Overall strategy or reasoning for decisions"
    )

    @model_validator(mode='after')
    def validate_decision(self):
        """Ensure decision is valid."""
        # If not ending turn, should have at least one action
        if not self.end_turn and not self.move_action and not self.property_actions:
            raise ValueError("Turn must either end or have at least one action")
        return self


class StrategyAnalysis(BaseModel):
    """Model for strategic game analysis."""
    analysis: str = Field(
        description="Comprehensive analysis of the current game state"
    )
    recommended_properties: List[str] = Field(
        default_factory=list, 
        description="Properties recommended to acquire next"
    )
    risk_assessment: str = Field(
        description="Assessment of risks in the current situation"
    )
    opportunity_assessment: str = Field(
        description="Assessment of opportunities in the current situation"
    )
    cash_recommendation: Optional[str] = Field(
        default=None,
        description="Recommendation for cash management"
    )


# ==============================================================
# Composite Decision Models
# ==============================================================

class AgentDecision(BaseModel):
    """Composite model for all agent decisions."""
    turn_decision: Optional[TurnDecision] = Field(
        default=None,
        description="Main turn decision"
    )
    strategy_analysis: Optional[StrategyAnalysis] = Field(
        default=None,
        description="Strategic analysis of the game"
    )
    move_action: Optional[MoveAction] = Field(
        default=None,
        description="Specific move action"
    )
    property_actions: List[PropertyAction] = Field(
        default_factory=list,
        description="Property actions to take"
    )
    error_message: Optional[str] = Field(
        default=None,
        description="Error message if any"
    )

    def get_next_action(self) -> Optional[Union[MoveAction, PropertyAction]]:
        """Get the next action to take."""
        # First try the turn decision
        if self.turn_decision:
            if self.turn_decision.move_action:
                return self.turn_decision.move_action
            if self.turn_decision.property_actions:
                return self.turn_decision.property_actions[0]
            if self.turn_decision.end_turn:
                return None
                
        # Then try individual actions
        if self.move_action:
            return self.move_action
        if self.property_actions:
            return self.property_actions[0]
            
        # No actions available
        return None


# ==============================================================
# Game Event Models
# ==============================================================

class GameEvent(BaseModel):
    """Model for a game event."""
    event_type: str = Field(description="Type of event")
    player_index: Optional[int] = Field(default=None, description="Player involved")
    description: str = Field(description="Event description")
    timestamp: float = Field(default_factory=lambda: __import__('time').time(), description="Event timestamp")
    
    @property
    def formatted_description(self) -> str:
        """Get a formatted description for display."""
        if self.player_index is not None:
            return f"Player {self.player_index + 1}: {self.description}"
        return self.description