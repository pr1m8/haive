"""Go game state manager module.

This module provides state management functionality for Go games, including:
    - Game state initialization
    - Move application and validation
    - Pass move handling
    - Game end detection
    - Capture counting

Example:
    >>> from src.haive.games.go import GoGameStateManager
    >>> 
    >>> # Initialize a new game
    >>> state = GoGameStateManager.initialize(board_size=19)
    >>> 
    >>> # Apply a move
    >>> new_state = GoGameStateManager.apply_move(state, (3, 4))
    """

import sente
from typing import Dict, Any, List, Optional, Tuple

from .state import GoGameState

class GoGameStateManager:
    """Manager class for Go game state operations.
    
    This class provides static methods for initializing and modifying
    Go game states, including:
        - Game initialization
        - Move application and validation
        - Pass move handling
        - Game end detection
    
    Example:
        >>> # Initialize a new game
        >>> state = GoGameStateManager.initialize(board_size=19)
        >>> 
        >>> # Apply a move
        >>> new_state = GoGameStateManager.apply_move(state, (3, 4))
        >>> print(new_state.turn)  # 'white'
    """

    @staticmethod
    def initialize(board_size: int = 19) -> GoGameState:
        """Initialize a new Go game state.
        
        Args:
            board_size (int): Size of the board (default: 19).
        
        Returns:
            GoGameState: Initial game state.
        
        Example:
            >>> state = GoGameStateManager.initialize(board_size=13)
            >>> print(state.board_size)  # 13
            >>> print(state.turn)  # 'black'
        """
        game = sente.Game(board_size)
        return GoGameState(
            board_sgf=sente.sgf.dumps(game),
            turn="black"
        )

    @staticmethod
    def apply_move(state: GoGameState, move: Optional[Tuple[int, int]]) -> GoGameState:
        """Apply a move to the current game state.
        
        This method handles:
            - Move validation and application
            - Pass moves (when move is None)
            - Capture counting
            - Turn alternation
            - Game end detection
        
        Args:
            state (GoGameState): Current game state.
            move (Optional[Tuple[int, int]]): Move coordinates or None for pass.
        
        Returns:
            GoGameState: New game state after applying the move.
        
        Example:
            >>> state = GoGameStateManager.initialize()
            >>> # Play a move at (3, 4)
            >>> new_state = GoGameStateManager.apply_move(state, (3, 4))
            >>> print(new_state.turn)  # 'white'
            >>> 
            >>> # Pass move
            >>> pass_state = GoGameStateManager.apply_move(new_state, None)
            >>> print(pass_state.passes)  # 1
        """
        game = sente.sgf.loads(state.board_sgf)[0]
        player = state.turn  # Current player

        # Handle pass move
        if move is None:
            new_passes = state.passes + 1
            return GoGameState(
                **state.dict(),
                turn="white" if player == "black" else "black",
                passes=new_passes,
                game_status="ended" if new_passes >= 2 else "ongoing",
                game_result="Draw" if new_passes >= 2 else None
            )

        new_passes = 0  # Reset pass count

        try:
            game.play(*move)
        except Exception as e:
            return GoGameState(
                **state.dict(),
                error_message=f"Invalid move: {str(e)}"
            )

        # Capture tracking
        captured_count = game.get_captures(player)

        return GoGameState(
            board_sgf=sente.sgf.dumps(game),
            move_history=state.move_history + [(player, move)],
            captured_stones={
                "black": state.captured_stones["black"] + (captured_count if player == "white" else 0),
                "white": state.captured_stones["white"] + (captured_count if player == "black" else 0),
            },
            turn="white" if player == "black" else "black",
            passes=new_passes,
            game_status="ended" if game.is_over() else "ongoing",
            game_result=game.get_winner() if game.is_over() else None
        )
