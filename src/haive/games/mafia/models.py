"""Models for the Mafia game implementation.

This module defines the core data models and enums used in the Mafia game, including:
    - Game phases (setup, night, day discussion, voting)
    - Player roles (villager, mafia, detective, doctor, narrator)
    - Action types (speak, vote, kill, investigate, save)
    - State tracking for players and game
    - Decision models for LLM output

Example:
    >>> from mafia.models import PlayerRole, GamePhase, MafiaAction
    >>> 
    >>> # Create a player action
    >>> action = MafiaAction(
    ...     player_id="Player_1",
    ...     action_type="vote",
    ...     phase=GamePhase.DAY_VOTING,
    ...     round_number=1,
    ...     target_id="Player_2"
    ... )
"""

from enum import Enum
from typing import Dict, List, Optional, Union, Any
from pydantic import BaseModel, Field, field_serializer

# Game Phase Enum
class GamePhase(str, Enum):
    """Game phase enumeration for the Mafia game.
    
    This enum defines the possible phases of the game, which determine what
    actions players can take and how the game progresses.
    
    Attributes:
        SETUP: Initial game setup phase
        NIGHT: Night phase where special roles act secretly
        DAY_DISCUSSION: Day phase for open discussion
        DAY_VOTING: Voting phase to eliminate a player
        GAME_OVER: Game has ended
    """
    SETUP = "setup"
    NIGHT = "night"
    DAY_DISCUSSION = "day_discussion"
    DAY_VOTING = "day_voting"
    GAME_OVER = "game_over"

# Player Role Enum
class PlayerRole(str, Enum):
    """Player role enumeration for the Mafia game.
    
    This enum defines the possible roles a player can have, each with
    unique abilities and win conditions.
    
    Attributes:
        VILLAGER: Basic role with no special abilities
        MAFIA: Can kill one player each night
        DETECTIVE: Can investigate one player's role each night
        DOCTOR: Can protect one player from death each night
        NARRATOR: Game master role that manages game flow
    """
    VILLAGER = "villager"
    MAFIA = "mafia"
    DETECTIVE = "detective"
    DOCTOR = "doctor"
    NARRATOR = "narrator"

# Action Type Enum
class ActionType(str, Enum):
    """Action type enumeration for the Mafia game.
    
    This enum defines all possible actions that players can take during
    the game, including both general and role-specific actions.
    
    Attributes:
        SPEAK: Make a public statement during discussion
        VOTE: Vote to eliminate a player during day voting
        KILL: Mafia night action to eliminate a player
        INVESTIGATE: Detective night action to learn a player's role
        SAVE: Doctor night action to protect a player
    """
    SPEAK = "speak"      # Make a statement during discussion
    VOTE = "vote"        # Vote during day phase
    KILL = "kill"        # Mafia ability to kill at night
    INVESTIGATE = "investigate"  # Detective ability to investigate at night
    SAVE = "save"        # Doctor ability to save at night

# Player State (using Pydantic model)
class PlayerState(BaseModel):
    """State information for a player in the Mafia game.
    
    This model tracks all information about a player's current state,
    including their role, alive status, and what they know about others.
    
    Attributes:
        player_id (Optional[str]): Unique identifier for the player
        role (PlayerRole): The player's assigned role
        is_alive (bool): Whether the player is still alive
        known_roles (Dict[str, PlayerRole]): Roles known to this player
        investigation_results (Dict[str, bool]): Detective's investigation results
    
    Example:
        >>> state = PlayerState(
        ...     player_id="Player_1",
        ...     role=PlayerRole.DETECTIVE,
        ...     known_roles={"Player_1": PlayerRole.DETECTIVE}
        ... )
    """
    player_id: Optional[str] = None
    role: PlayerRole = PlayerRole.VILLAGER
    is_alive: bool = True
    known_roles: Dict[str, PlayerRole] = Field(default_factory=dict)
    investigation_results: Dict[str, bool] = Field(default_factory=dict)
    
    class Config:
        arbitrary_types_allowed = True

class MafiaAction(BaseModel):
    """An action taken by a player in the Mafia game.
    
    This model represents any action a player can take, including speaking,
    voting, and role-specific night actions.
    
    Attributes:
        player_id (str): ID of the player taking the action
        action_type (ActionType): Type of action being taken
        phase (GamePhase): Game phase when the action occurs
        round_number (int): Current round number
        target_id (Optional[str]): Target player for the action
        message (Optional[str]): Content for speak actions
    
    Example:
        >>> action = MafiaAction(
        ...     player_id="Player_1",
        ...     action_type=ActionType.VOTE,
        ...     phase=GamePhase.DAY_VOTING,
        ...     round_number=1,
        ...     target_id="Player_2"
        ... )
    """
    player_id: str
    action_type: ActionType
    phase: GamePhase
    round_number: int
    target_id: Optional[str] = None
    message: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the action to a dictionary format.
        
        Returns:
            Dict[str, Any]: Dictionary representation of the action
        """
        return self.model_dump()

    def __str__(self) -> str:
        """Get a human-readable string representation of the action.
        
        Returns:
            str: Description of the action
        """
        if self.action_type == ActionType.SPEAK:
            return f"{self.player_id} says: {self.message}"
        elif self.action_type == ActionType.VOTE:
            return f"{self.player_id} voted for {self.target_id}"
        elif self.action_type == ActionType.KILL:
            return f"{self.player_id} chose to kill {self.target_id}"
        elif self.action_type == ActionType.INVESTIGATE:
            return f"{self.player_id} investigated {self.target_id}"
        elif self.action_type == ActionType.SAVE:
            return f"{self.player_id} chose to save {self.target_id}"
        return f"{self.player_id} took action {self.action_type}"


# NarratorAction as a proper Pydantic model
class NarratorAction(BaseModel):
    """An action taken by the narrator in the Mafia game.
    
    This model represents narrator actions that control game flow and
    provide information to players.
    
    Attributes:
        announcement (Optional[str]): Public message to all players
        player_state_updates (Dict[str, Dict[str, Any]]): State changes
        phase_transition (bool): Whether to move to next phase
        next_phase (Optional[GamePhase]): Phase to transition to
        round_number (int): Current round number
    
    Example:
        >>> action = NarratorAction(
        ...     announcement="Night falls on the village.",
        ...     phase_transition=True,
        ...     next_phase=GamePhase.NIGHT,
        ...     round_number=1
        ... )
    """
    announcement: Optional[str] = None
    player_state_updates: Dict[str, Dict[str, Any]] = Field(default_factory=dict)
    phase_transition: bool = False
    next_phase: Optional[GamePhase] = None
    round_number: int = 1
    
    @field_serializer('next_phase')
    def serialize_next_phase(self, next_phase: Optional[GamePhase]) -> Optional[str]:
        """Serialize the next_phase enum to a string.
        
        Args:
            next_phase (Optional[GamePhase]): Phase to serialize
        
        Returns:
            Optional[str]: String value of the phase or None
        """
        return next_phase.value if next_phase else None
    
    class Config:
        arbitrary_types_allowed = True
    
    def __str__(self) -> str:
        """Get a human-readable string representation of the action.
        
        Returns:
            str: Description of the narrator action
        """
        return f"Narrator: {self.announcement}" if self.announcement else "Narrator took an action"

# Decision models for LLM output
class MafiaPlayerDecision(BaseModel):
    """A decision made by a player in the Mafia game.
    
    This model represents the complete decision output from a player's
    LLM, including both the action and reasoning.
    
    Attributes:
        action (MafiaAction): The action the player will take
        reasoning (Optional[str]): Explanation for the decision
    
    Example:
        >>> decision = MafiaPlayerDecision(
        ...     action=MafiaAction(...),
        ...     reasoning="Player seems suspicious based on voting pattern"
        ... )
    """
    action: MafiaAction
    reasoning: Optional[str] = None
    
    class Config:
        arbitrary_types_allowed = True

class NarratorDecision(BaseModel):
    """A decision made by the narrator in the Mafia game.
    
    This model represents the complete decision output from the narrator's
    LLM, including both the action and reasoning.
    
    Attributes:
        action (NarratorAction): The action the narrator will take
        reasoning (Optional[str]): Explanation for the decision
    
    Example:
        >>> decision = NarratorDecision(
        ...     action=NarratorAction(...),
        ...     reasoning="All players have completed their night actions"
        ... )
    """
    action: NarratorAction
    reasoning: Optional[str] = None
    
    class Config:
        arbitrary_types_allowed = True

# Decision models that don't use custom types (for LLM structured output)
class MafiaPlayerDecisionSchema(BaseModel):
    """Schema for LLM to output structured player decisions.
    
    This model provides a simplified schema for LLM output that can be
    converted into a full MafiaPlayerDecision.
    
    Attributes:
        action_type (str): Type of action to take
        target_id (Optional[str]): Target player for the action
        message (Optional[str]): Content for speak actions
        reasoning (Optional[str]): Explanation for the decision
    
    Example:
        >>> schema = MafiaPlayerDecisionSchema(
        ...     action_type="vote",
        ...     target_id="Player_2",
        ...     reasoning="Suspicious behavior during discussion"
        ... )
    """
    action_type: str = Field(..., description="Type of action (speak, vote, kill, investigate, save)")
    target_id: Optional[str] = Field(default=None, description="Target player ID for actions that require a target")
    message: Optional[str] = Field(default=None, description="Message content for speak actions")
    reasoning: Optional[str] = Field(default=None, description="Reasoning behind the decision")
    
    class Config:
        json_schema_extra= {
            "examples": [
                {
                    "action_type": "speak",
                    "message": "I don't think Player_2 is being honest about their role.",
                    "reasoning": "They've been very quiet during discussions."
                },
                {
                    "action_type": "vote",
                    "target_id": "Player_3",
                    "reasoning": "They seem suspicious based on their contradictory statements."
                },
                {
                    "action_type": "kill",
                    "target_id": "Player_1",
                    "reasoning": "They are showing signs of being a detective."
                },
                {
                    "action_type": "save",
                    "target_id": "Player_4",
                    "reasoning": "They seem to be a valuable village member the mafia might target."
                },
                {
                    "action_type": "investigate",
                    "target_id": "Player_2",
                    "reasoning": "Their behavior has been inconsistent."
                }
            ]
        }

class NarratorDecisionSchema(BaseModel):
    """Schema for LLM to output structured narrator decisions.
    
    This model provides a simplified schema for LLM output that can be
    converted into a full NarratorDecision.
    
    Attributes:
        announcement (Optional[str]): Public message to all players
        phase_transition (bool): Whether to move to next phase
        reasoning (Optional[str]): Explanation for the decision
    
    Example:
        >>> schema = NarratorDecisionSchema(
        ...     announcement="The village falls quiet as night approaches.",
        ...     phase_transition=True,
        ...     reasoning="All players have completed their day actions."
        ... )
    """
    announcement: Optional[str] = Field(default=None, description="Public announcement to the village")
    phase_transition: bool = Field(default=False, description="Whether to transition to the next phase")
    reasoning: Optional[str] = Field(default=None, description="Reasoning behind the decision")
    
    class Config:
        json_schema_extra= {
            "examples": [
                {
                    "announcement": "The village falls quiet as night approaches.",
                    "phase_transition": True,
                    "reasoning": "All players have completed their day actions."
                },
                {
                    "announcement": "Player_2 was found dead this morning, with clear signs of foul play.",
                    "phase_transition": False,
                    "reasoning": "Narrating the result of the night's events."
                }
            ]
        }