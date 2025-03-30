"""Game state models for the Mafia game.

This module defines the core state model for the Mafia game, extending the
base MultiPlayerGameState with Mafia-specific functionality.

The state model tracks:
    - Player roles and statuses
    - Game phase and progression
    - Voting and action history
    - Public announcements
    - Night action outcomes

Example:
    >>> from mafia.state import MafiaGameState
    >>> from mafia.models import PlayerRole, GamePhase
    >>> 
    >>> # Create a new game state
    >>> state = MafiaGameState(
    ...     players=["Player_1", "Player_2", "Narrator"],
    ...     roles={"Player_1": PlayerRole.VILLAGER, 
    ...            "Player_2": PlayerRole.MAFIA,
    ...            "Narrator": PlayerRole.NARRATOR},
    ...     game_phase=GamePhase.SETUP
    ... )
"""

from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Union, Any
import copy

# Import the actual MultiPlayerGameState class
from src.haive.games.framework.multi_player.state import MultiPlayerGameState
from .models import (
    PlayerRole,
    GamePhase,
    ActionType,
    MafiaAction,
    NarratorAction,
    PlayerState,
)

class MafiaGameState(MultiPlayerGameState):
    """State model for a Mafia game.
    
    This class extends MultiPlayerGameState to provide Mafia-specific state
    tracking, including roles, votes, and game progression.

    Attributes:
        players (List[str]): List of player names/IDs
        current_player_idx (int): Index of current player in players list
        game_status (str): Status of the game (ongoing, ended)
        move_history (List[Dict[str, Any]]): History of moves
        round_number (int): Current round number
        player_data (Dict[str, Dict[str, Any]]): Player-specific data
        public_state (Dict[str, Any]): Public game state visible to all
        error_message (Optional[str]): Error message if any
        game_phase (GamePhase): Current phase of the game
        roles (Dict[str, PlayerRole]): Mapping of player IDs to roles
        player_states (Dict[str, PlayerState]): Player state information
        votes (Dict[str, str]): Player votes during voting phase
        action_history (List[Dict[str, Any]]): History of all actions
        public_announcements (List[str]): Public game announcements
        alive_mafia_count (int): Number of mafia members alive
        alive_village_count (int): Number of villagers alive
        alive_doctor_count (int): Number of doctors alive
        alive_detective_count (int): Number of detectives alive
        killed_at_night (Optional[str]): Player targeted by mafia
        saved_at_night (Optional[str]): Player saved by doctor
        night_deaths (List[str]): Players who died during the night
        day_number (int): Current day number
        winner (Optional[str]): Winner (village or mafia)

    Example:
        >>> state = MafiaGameState(
        ...     players=["Player_1", "Player_2", "Narrator"],
        ...     roles={"Player_1": PlayerRole.VILLAGER,
        ...            "Player_2": PlayerRole.MAFIA,
        ...            "Narrator": PlayerRole.NARRATOR},
        ...     game_phase=GamePhase.SETUP
        ... )
        >>> print(state.game_phase)  # Shows SETUP
    """

    # Required fields from MultiPlayerGameState - declare them explicitly 
    # to ensure they're properly recognized
    players: List[str] = Field(default_factory=list, description="List of player names/IDs")
    current_player_idx: int = Field(default=0, description="Index of current player in players list")
    game_status: str = Field(default="ongoing", description="Status of the game (ongoing, ended)")
    move_history: List[Dict[str, Any]] = Field(default_factory=list, description="History of moves")
    round_number: int = Field(default=0, description="Current round number")
    player_data: Dict[str, Dict[str, Any]] = Field(default_factory=dict, description="Player-specific data")
    public_state: Dict[str, Any] = Field(default_factory=dict, description="Public game state visible to all players")
    error_message: Optional[str] = Field(default=None, description="Error message if any")
    
    # Override the game_phase field to use our enum
    game_phase: GamePhase = Field(default=GamePhase.SETUP, description="Current phase of the game")
    
    # Mafia-specific fields
    roles: Dict[str, PlayerRole] = Field(default_factory=dict, description="Player roles")
    player_states: Dict[str, PlayerState] = Field(default_factory=dict, description="Player states")
    votes: Dict[str, str] = Field(default_factory=dict, description="Player votes during voting phase")
    action_history: List[Dict[str, Any]] = Field(default_factory=list, description="History of actions")
    public_announcements: List[str] = Field(default_factory=list, description="Public announcements")
    
    # Counters for game status
    alive_mafia_count: int = Field(default=0, description="Number of mafia members alive")
    alive_village_count: int = Field(default=0, description="Number of villagers alive")
    alive_doctor_count: int = Field(default=0, description="Number of doctors alive")
    alive_detective_count: int = Field(default=0, description="Number of detectives alive")
    
    # Night action tracking
    killed_at_night: Optional[str] = Field(default=None, description="Player targeted by mafia")
    saved_at_night: Optional[str] = Field(default=None, description="Player saved by doctor")
    night_deaths: List[str] = Field(default_factory=list, description="Players who died during the night")
    
    # Game progression tracking
    day_number: int = Field(default=0, description="Current day number")
    
    # Winner tracking - declared explicitly even though it's in the parent class
    winner: Optional[str] = Field(default=None, description="Winner (village or mafia)")
    
    class Config:
        arbitrary_types_allowed = True

    def update_alive_counts(self):
        """Update the count of alive players in different roles.
        
        This method recalculates the number of alive players in each role
        category based on the current player states.

        Note:
            This should be called after any change that might affect player
            life status (e.g., night kills, voting execution).
        
        Example:
            >>> state.player_states["Player_1"].is_alive = False
            >>> state.update_alive_counts()
            >>> print(state.alive_village_count)  # Shows updated count
        """
        self.alive_village_count = sum(
            1 for player_id, state in self.player_states.items()
            if state.is_alive and self.roles.get(player_id) in {PlayerRole.VILLAGER, PlayerRole.DETECTIVE, PlayerRole.DOCTOR}
        )
        self.alive_mafia_count = sum(
            1 for player_id, state in self.player_states.items()
            if state.is_alive and self.roles.get(player_id) == PlayerRole.MAFIA
        )
        self.alive_doctor_count = sum(
            1 for player_id, state in self.player_states.items()
            if state.is_alive and self.roles.get(player_id) == PlayerRole.DOCTOR
        )
        self.alive_detective_count = sum(
            1 for player_id, state in self.player_states.items()
            if state.is_alive and self.roles.get(player_id) == PlayerRole.DETECTIVE
        )

    def add_public_announcement(self, announcement: str) -> None:
        """Add an announcement to the public record.
        
        Args:
            announcement (str): The announcement to add

        Example:
            >>> state.add_public_announcement("Night falls on the village.")
            >>> print(state.public_announcements[-1])
        """
        if not hasattr(self, 'public_announcements'):
            self.public_announcements = []
        self.public_announcements.append(announcement)
        
    def log_action(self, action: Union[MafiaAction, NarratorAction]) -> None:
        """Log an action in the game history.
        
        This method records player and narrator actions in both the action_history
        and move_history, ensuring proper serialization of complex objects.

        Args:
            action (Union[MafiaAction, NarratorAction]): Action to log

        Example:
            >>> action = MafiaAction(
            ...     player_id="Player_1",
            ...     action_type=ActionType.VOTE,
            ...     target_id="Player_2",
            ...     phase=GamePhase.DAY_VOTING,
            ...     round_number=1
            ... )
            >>> state.log_action(action)
        """
        if not hasattr(self, 'action_history'):
            self.action_history = []
        
        # Convert MafiaAction or NarratorAction to dictionary for serialization
        if isinstance(action, MafiaAction):
            action_dict = {
                "type": "MafiaAction",
                "player_id": action.player_id,
                "action_type": action.action_type.value if hasattr(action.action_type, 'value') else str(action.action_type),
                "phase": action.phase.value if hasattr(action.phase, 'value') else str(action.phase),
                "round_number": action.round_number,
                "target_id": action.target_id if hasattr(action, 'target_id') else None,
                "message": action.message if hasattr(action, 'message') else None
            }
        elif isinstance(action, NarratorAction):
            action_dict = {
                "type": "NarratorAction",
                "announcement": action.announcement,
                "phase_transition": action.phase_transition,
                "round_number": action.round_number
            }
        else:
            # fallback for other types
            action_dict = {"type": "UnknownAction", "data": str(action)}
            
        self.action_history.append(action_dict)
        
        # Also update move_history for MultiPlayerGameState compatibility
        if not hasattr(self, 'move_history'):
            self.move_history = []
        self.move_history.append(action_dict)

        # Update alive counts after an action is taken
        self.update_alive_counts()

    def model_copy(self, *, deep: bool = False, **kwargs):
        """Create a copy of the model.
        
        Args:
            deep (bool, optional): Whether to create a deep copy. Defaults to False.
            **kwargs: Additional arguments to pass to model_copy

        Returns:
            MafiaGameState: A copy of the current state

        Example:
            >>> new_state = state.model_copy(deep=True)
        """
        if deep:
            return copy.deepcopy(self)
        return super().model_copy(**kwargs)
