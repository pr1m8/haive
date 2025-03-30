"""Base state management for game agents.

This module provides the foundational state management classes for game agents.
It includes the base GameState class and GameStateManager for handling game state
transitions and move applications.

Example:
    >>> state = GameState(players=["p1", "p2"], current_turn="p1")
    >>> state_manager = GameStateManager()
    >>> new_state = state_manager.apply_move(state, move, "p1")

Typical usage:
    - Inherit from GameState to create game-specific state classes
    - Use GameStateManager to handle state transitions in your game
"""

from pydantic import BaseModel, Field
from typing import List, Tuple, Dict, Optional, Literal, Generic
from src.haive.games.base.models import PlayerState, MoveModel, TMove

class GameState(BaseModel):
    """Generic state representation for any multi-agent game.
    
    This class serves as the base state representation for turn-based games.
    It maintains the core game state including players, turns, move history,
    game status, and player-specific private states.
    
    Attributes:
        players (List[str]): List of player identifiers.
        current_turn (str): ID of the player whose turn it is.
        move_history (List[Tuple[str, str]]): History of (player_id, move) pairs.
        status (Literal["ongoing", "finished"]): Current game status.
        private_states (Dict[str, PlayerState]): Private state information per player.
    
    Example:
        >>> state = GameState(
        ...     players=["player1", "player2"],
        ...     current_turn="player1",
        ...     move_history=[],
        ...     status="ongoing",
        ...     private_states={}
        ... )
    """
    players: List[str] = Field(..., description="List of player identifiers.")
    current_turn: str = Field(..., description="ID of the player whose turn it is.")
    move_history: List[Tuple[str, str]] = Field(default_factory=list, description="History of (player_id, move).")
    status: Literal["ongoing", "finished"] = Field(default="ongoing", description="Current game status.")
    private_states: Dict[str, PlayerState] = Field(default_factory=dict, description="Private state per player.")

    def get_private_state(self, player_id: str) -> Optional[PlayerState]:
        """Retrieves the private state for a specific player.
        
        Args:
            player_id (str): The ID of the player whose private state to retrieve.
            
        Returns:
            Optional[PlayerState]: The player's private state if it exists, None otherwise.
            
        Example:
            >>> state = GameState(players=["p1"], current_turn="p1")
            >>> private_state = state.get_private_state("p1")
        """
        return self.private_states.get(player_id)

class PlayerState(BaseModel):
    """Private state per player, stored separately from GameState."""
    agent_id: str = Field(..., description="Unique identifier for the player.")
    planned_moves: List[str] = Field(default_factory=list, description="List of planned moves.")
    strategic_thoughts: List[str] = Field(default_factory=list, description="List of strategic thoughts.")
    evaluation: Optional[str] = Field(default=None, description="Evaluation of the player's strategic thoughts.")

    
class GameStateManager(Generic[TMove]):
    """Manages game state transitions and move applications.
    
    This class provides the core functionality for managing game state,
    including initialization and move application. It is generic over
    the type of moves (TMove) that can be applied.
    
    Example:
        >>> manager = GameStateManager[ChessMove]()
        >>> initial_state = manager.initialize(["player1", "player2"])
        >>> new_state = manager.apply_move(initial_state, move, "player1")
    """

    @staticmethod
    def initialize(players: List[str]) -> GameState:
        """Creates an initial game state with the given players.
        
        Args:
            players (List[str]): List of player identifiers to initialize the game with.
            
        Returns:
            GameState: A new game state with the specified players, first player's turn.
            
        Example:
            >>> initial_state = GameStateManager.initialize(["p1", "p2"])
        """
        return GameState(players=players, current_turn=players[0])

    @staticmethod
    def apply_move(state: GameState, move_model: MoveModel[TMove], player_id: str) -> GameState:
        """Applies a move to the current game state.
        
        This method creates a new game state reflecting the application of the move.
        It validates the move is being made by the correct player and updates the
        turn order.
        
        Args:
            state (GameState): Current game state.
            move_model (MoveModel[TMove]): The move to apply.
            player_id (str): ID of the player making the move.
            
        Returns:
            GameState: New game state after applying the move.
            
        Raises:
            ValueError: If it's not the specified player's turn.
            
        Example:
            >>> new_state = GameStateManager.apply_move(state, chess_move, "p1")
        """
        if state.current_turn != player_id:
            raise ValueError(f"Not {player_id}'s turn!")

        new_state = GameState(
            players=state.players,
            current_turn=state.players[(state.players.index(player_id) + 1) % len(state.players)],  # Rotate turn
            move_history=state.move_history + [(player_id, str(move_model.move))],
            status="ongoing",
            private_states=state.private_states.copy()
        )
        return new_state
