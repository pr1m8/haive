"""Base state management for multi-player games.

This module provides the foundational state model for multi-player games,
supporting features like:
    - Player tracking and turn management
    - Game phase transitions
    - Move history recording
    - Public and private state management
    - Error handling

Example:
    >>> from src.haive.agents.agent_games.framework.multi_player.state import MultiPlayerGameState
    >>> 
    >>> # Create a game state
    >>> state = MultiPlayerGameState(
    ...     players=["player1", "player2", "player3"],
    ...     game_phase=GamePhase.SETUP
    ... )
    >>> 
    >>> # Advance to next player
    >>> next_player = state.advance_player()
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from src.haive.games.framework.multi_player.models import GamePhase

class MultiPlayerGameState(BaseModel):
    """Base game state for multi-player games.
    
    This class provides the foundation for managing game state in multi-player
    games. It handles player turns, game phases, move history, and both public
    and private state information.
    
    Attributes:
        players (List[str]): List of player names/IDs.
        current_player_idx (int): Index of current player in players list.
        game_phase (str): Current phase of the game (see GamePhase enum).
        game_status (str): Status of the game (e.g., "ongoing", "ended").
        move_history (List[Dict[str, Any]]): History of all moves made.
        round_number (int): Current round number.
        player_data (Dict[str, Dict[str, Any]]): Private data for each player.
        public_state (Dict[str, Any]): Public game state visible to all.
        error_message (Optional[str]): Error message if any.
    
    Example:
        >>> state = MultiPlayerGameState(
        ...     players=["player1", "player2"],
        ...     game_phase=GamePhase.SETUP
        ... )
        >>> state.advance_player()
        'player2'
        >>> private_data = state.get_player_private_data("player1")
    """
    
    players: List[str] = Field(..., description="List of player names/IDs")
    current_player_idx: int = Field(default=0, description="Index of current player in players list")
    game_phase: str = Field(default=GamePhase.SETUP, description="Current phase of the game")
    game_status: str = Field(default="ongoing", description="Status of the game")
    move_history: List[Dict[str, Any]] = Field(default_factory=list, description="History of moves")
    round_number: int = Field(default=0, description="Current round number")
    player_data: Dict[str, Dict[str, Any]] = Field(default_factory=dict, description="Player-specific data")
    public_state: Dict[str, Any] = Field(default_factory=dict, description="Public game state visible to all players")
    error_message: Optional[str] = Field(default=None, description="Error message if any")
    
    class Config:
        arbitrary_types_allowed = True

    @property
    def current_player(self) -> str:
        """Get the current player's name/ID.
        
        Returns:
            str: The current player's name/ID, or empty string if invalid index.
        
        Example:
            >>> state = MultiPlayerGameState(players=["p1", "p2"])
            >>> state.current_player
            'p1'
        """
        if 0 <= self.current_player_idx < len(self.players):
            return self.players[self.current_player_idx]
        return ""
    
    def advance_player(self) -> str:
        """Advance to the next player and return their name/ID.
        
        This method updates the current_player_idx to the next player in
        the rotation and returns the new current player's name/ID.
        
        Returns:
            str: The next player's name/ID.
        
        Example:
            >>> state = MultiPlayerGameState(players=["p1", "p2", "p3"])
            >>> state.advance_player()
            'p2'
            >>> state.advance_player()  # Advances to p3
            'p3'
            >>> state.advance_player()  # Wraps back to p1
            'p1'
        """
        self.current_player_idx = (self.current_player_idx + 1) % len(self.players)
        return self.current_player

    def get_player_private_data(self, player_id: str) -> Dict[str, Any]:
        """Get private data for a specific player.
        
        This method safely retrieves the private state data for a given player,
        returning an empty dict if no data exists.
        
        Args:
            player_id (str): The ID of the player whose data to retrieve.
        
        Returns:
            Dict[str, Any]: The player's private data, or empty dict if none exists.
        
        Example:
            >>> state = MultiPlayerGameState(players=["p1", "p2"])
            >>> state.player_data["p1"] = {"secret_info": 42}
            >>> state.get_player_private_data("p1")
            {'secret_info': 42}
            >>> state.get_player_private_data("unknown")
            {}
        """
        return self.player_data.get(player_id, {})
