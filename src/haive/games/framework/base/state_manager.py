"""Base state manager module for game agents.

This module provides the foundational state manager class that handles
game state transitions and operations. It defines the interface that all
game-specific state managers should implement.

Example:
    >>> class ChessStateManager(GameStateManager[ChessMove]):
    ...     @classmethod
    ...     def initialize(cls) -> ChessState:
    ...         return ChessState.new_game()
    ...
    ...     @classmethod
    ...     def apply_move(cls, state: ChessState, move: ChessMove) -> ChessState:
    ...         return state.apply_move(move)

Typical usage:
    - Inherit from GameStateManager to create game-specific state managers
    - Implement the required methods for state initialization and transitions
    - Use in conjunction with game agents to manage game flow
"""

from typing import TypeVar, Generic, Any, List
from pydantic import BaseModel

# Type variable for generic state
T = TypeVar('T', bound=BaseModel)

class GameStateManager(Generic[T]):
    """Base state manager that implements common game state operations.
    
    This class provides the interface for managing game state transitions
    and operations. Each game should extend this with game-specific logic
    by implementing the required methods.
    
    Type Parameters:
        T: The type of the game state, must be a Pydantic BaseModel.
    
    Example:
        >>> class ChessStateManager(GameStateManager[ChessState]):
        ...     @classmethod
        ...     def initialize(cls) -> ChessState:
        ...         return ChessState.new_game()
        ...
        ...     @classmethod
        ...     def apply_move(cls, state: ChessState, move: ChessMove) -> ChessState:
        ...         return state.apply_move(move)
    """
    
    @classmethod
    def initialize(cls, **kwargs) -> T:
        """Initialize a new game state.
        
        This method should create and return a new instance of the game state
        with initial values set appropriately for the start of a game.
        
        Args:
            **kwargs: Additional keyword arguments for game-specific initialization.
        
        Returns:
            T: A new instance of the game state.
            
        Raises:
            NotImplementedError: This method must be implemented by subclasses.
            
        Example:
            >>> @classmethod
            ... def initialize(cls) -> ChessState:
            ...     return ChessState(
            ...         board=Board.initial_setup(),
            ...         turn="white",
            ...         game_status="ongoing"
            ...     )
        """
        raise NotImplementedError("Must be implemented by subclass")
    
    @classmethod
    def apply_move(cls, state: T, move: Any) -> T:
        """Apply a move to the game state.
        
        This method should create and return a new game state that reflects
        the application of the given move to the current state.
        
        Args:
            state (T): The current game state.
            move (Any): The move to apply.
            
        Returns:
            T: A new game state after applying the move.
            
        Raises:
            NotImplementedError: This method must be implemented by subclasses.
            
        Example:
            >>> @classmethod
            ... def apply_move(cls, state: ChessState, move: ChessMove) -> ChessState:
            ...     new_board = state.board.make_move(move)
            ...     return ChessState(
            ...         board=new_board,
            ...         turn="black" if state.turn == "white" else "white",
            ...         move_history=state.move_history + [move]
            ...     )
        """
        raise NotImplementedError("Must be implemented by subclass")
    
    @classmethod
    def get_legal_moves(cls, state: T) -> List[Any]:
        """Get all legal moves for the current state.
        
        This method should return a list of all valid moves that can be made
        from the current game state.
        
        Args:
            state (T): The current game state.
            
        Returns:
            List[Any]: A list of legal moves.
            
        Raises:
            NotImplementedError: This method must be implemented by subclasses.
            
        Example:
            >>> @classmethod
            ... def get_legal_moves(cls, state: ChessState) -> List[ChessMove]:
            ...     return state.board.get_legal_moves(state.turn)
        """
        raise NotImplementedError("Must be implemented by subclass")
    
    @classmethod
    def check_game_status(cls, state: T) -> T:
        """Check and update the game status.
        
        This method should examine the current game state and determine if
        the game status needs to be updated (e.g., if someone has won or
        if the game is a draw).
        
        Args:
            state (T): The current game state.
            
        Returns:
            T: The game state with updated status.
            
        Raises:
            NotImplementedError: This method must be implemented by subclasses.
            
        Example:
            >>> @classmethod
            ... def check_game_status(cls, state: ChessState) -> ChessState:
            ...     if state.board.is_checkmate():
            ...         state.game_status = "checkmate"
            ...     elif state.board.is_stalemate():
            ...         state.game_status = "stalemate"
            ...     return state
        """
        raise NotImplementedError("Must be implemented by subclass")
