"""State management interface for multi-player games.

This module provides the base state manager interface for multi-player games,
defining the core operations that game-specific state managers must implement.
The state manager handles:
    - Game initialization
    - Move application and validation
    - Legal move generation
    - Game status updates
    - Phase transitions
    - Information hiding

Example:
    >>> from typing import List, Dict, Any
    >>> from src.haive.agents.agent_games.framework.multi_player.state_manager import MultiPlayerGameStateManager
    >>> 
    >>> class MyGameStateManager(MultiPlayerGameStateManager[MyGameState]):
    ...     @classmethod
    ...     def initialize(cls, player_names: List[str], **kwargs) -> MyGameState:
    ...         return MyGameState(players=player_names)
"""

from typing import TypeVar, Generic, List, Any, Dict
from pydantic import BaseModel  

# Type variable for generic state
T = TypeVar('T', bound=BaseModel)


class MultiPlayerGameStateManager(Generic[T]):
    """Manager for multi-player game states.
    
    This abstract base class defines the interface for managing game states
    in multi-player games. Game-specific implementations must inherit from
    this class and implement all abstract methods.
    
    Type Parameters:
        T: The game state type, must be a Pydantic BaseModel.
    
    Example:
        >>> class ChessStateManager(MultiPlayerGameStateManager[ChessState]):
        ...     @classmethod
        ...     def initialize(cls, player_names: List[str], **kwargs) -> ChessState:
        ...         return ChessState(
        ...             players=player_names,
        ...             board=cls.create_initial_board()
        ...         )
    """
    
    @classmethod
    def initialize(cls, player_names: List[str], **kwargs) -> T:
        """Initialize a new game state with multiple players.
        
        Args:
            player_names (List[str]): List of player names/IDs.
            **kwargs: Additional game-specific initialization parameters.
        
        Returns:
            T: A new game state instance.
        
        Raises:
            NotImplementedError: Must be implemented by subclass.
        """
        raise NotImplementedError("Must be implemented by subclass")
    
    @classmethod
    def apply_move(cls, state: T, player_id: str, move: Any) -> T:
        """Apply a move by a specific player.
        
        Args:
            state (T): Current game state.
            player_id (str): ID of the player making the move.
            move (Any): The move to apply.
        
        Returns:
            T: New game state after applying the move.
        
        Raises:
            NotImplementedError: Must be implemented by subclass.
        """
        raise NotImplementedError("Must be implemented by subclass")
    
    @classmethod
    def get_legal_moves(cls, state: T, player_id: str) -> List[Any]:
        """Get legal moves for a specific player.
        
        Args:
            state (T): Current game state.
            player_id (str): ID of the player to get moves for.
        
        Returns:
            List[Any]: List of legal moves for the player.
        
        Raises:
            NotImplementedError: Must be implemented by subclass.
        """
        raise NotImplementedError("Must be implemented by subclass")
    
    @classmethod
    def check_game_status(cls, state: T) -> T:
        """Check and update game status.
        
        This method should check for win conditions, draws, or other
        game-ending conditions and update the state accordingly.
        
        Args:
            state (T): Current game state.
        
        Returns:
            T: Updated game state with current status.
        
        Raises:
            NotImplementedError: Must be implemented by subclass.
        """
        raise NotImplementedError("Must be implemented by subclass")
    
    @classmethod
    def advance_phase(cls, state: T) -> T:
        """Advance the game to the next phase.
        
        This method should handle phase transitions, including any
        necessary state updates or cleanup between phases.
        
        Args:
            state (T): Current game state.
        
        Returns:
            T: Updated game state in the new phase.
        
        Raises:
            NotImplementedError: Must be implemented by subclass.
        """
        raise NotImplementedError("Must be implemented by subclass")
    
    @classmethod
    def filter_state_for_player(cls, state: T, player_id: str) -> Dict[str, Any]:
        """Filter the state to include only information visible to a specific player.
        
        This method should implement information hiding, ensuring players
        only see game information they should have access to.
        
        Args:
            state (T): Current game state.
            player_id (str): ID of the player to filter for.
        
        Returns:
            Dict[str, Any]: Filtered game state with only visible information.
        
        Raises:
            NotImplementedError: Must be implemented by subclass.
        """
        raise NotImplementedError("Must be implemented by subclass")
