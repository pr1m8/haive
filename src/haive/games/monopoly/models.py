from typing import List, Dict, Optional, Tuple, Literal, Union, Any
from pydantic import BaseModel, Field


# ==============================================================
# Game State Models - For LLM Decision Making
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
    property_type: Literal["property"] = Field("property", const=True, description="Type is always 'property'")


class SpecialCardInfo(BaseModel):
    """Information about special properties like railroads and utilities."""
    name: str = Field(description="The name of the card")
    card_type: Literal["railroad", "utility"] = Field(description="The type of the card")
    position: int = Field(description="The board position")
    cost: int = Field(description="The purchase cost")
    rent: int = Field(description="Current rent value")
    mortgage_value: int = Field(description="Mortgage value")
    owner: Optional[int] = Field(None, description="The player index who owns this")


class PlayerInfo(BaseModel):
    """Information about a player."""
    name: str = Field(description="Player's name")
    index: int = Field(description="Player index")
    position: int = Field(description="Current board position (0-39)")
    cash: int = Field(description="Current cash on hand")
    total_wealth: int = Field(description="Net worth including cash and property value")
    properties_owned: List[str] = Field(description="Names of properties owned")
    is_in_jail: bool = Field(description="Is the player currently in jail")
    jail_cards: int = Field(description="Number of Get Out of Jail Free cards")
    railways_owned: int = Field(description="How many railroads this player owns")
    bankruptcy_status: bool = Field(description="Whether the player is bankrupt")


# ==============================================================
# LLM Decision Models - For Agent Outputs
# ==============================================================

class PropertyAction(BaseModel):
    action_type: Literal["buy", "build", "sell", "mortgage", "unmortgage"] = Field(description="Action to take")
    property_name: str = Field(description="Property name")
    reasoning: str = Field(description="Why take this action")


class MoveAction(BaseModel):
    action_type: Literal["roll", "pay_to_exit_jail", "roll_for_double"] = Field(description="Move type")
    reasoning: str = Field(description="Why this move was chosen")


class TurnDecision(BaseModel):
    property_actions: List[PropertyAction] = Field(default_factory=list, description="Property management actions")
    move_action: Optional[MoveAction] = Field(None, description="Movement/jail decision")
    end_turn: bool = Field(False, description="Whether to end the turn")
    reasoning: str = Field(description="Overall strategy or logic behind the turn")


class StrategyAnalysis(BaseModel):
    analysis: str = Field(description="Strategic assessment of the situation")
    recommended_properties: List[str] = Field(default_factory=list, description="Good property buys right now")
    risk_assessment: str = Field(description="How risky the current state is")
    opportunity_assessment: str = Field(description="What opportunity exists to take advantage of")


class DiceInfo(BaseModel):
    values: Tuple[int, int] = Field(description="Two dice values")
    sum: int = Field(description="Sum of the dice roll")
