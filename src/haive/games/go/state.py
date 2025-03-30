"""Go game state management.

This module provides state tracking and management for Go games, including:
    - Game state representation
    - Move validation and application
    - Board state tracking in SGF format
    - Capture counting
    - Game status management

Example:
    >>> from src.haive.games.go.state import GoGameState, GoGameStateManager
    >>> 
    >>> # Initialize a new game
    >>> state = GoGameStateManager.initialize(board_size=19)
    >>> 
    >>> # Apply moves
    >>> state = GoGameStateManager.apply_move(state, (3, 4))  # Black's move
    >>> state = GoGameStateManager.apply_move(state, (15, 15))  # White's move
    >>> 
    >>> # Check game status
    >>> print(state.game_status)  # 'ongoing'
    >>> print(state.captured_stones)  # {'black': 0, 'white': 0}
"""

from typing import List, Dict, Literal, Optional, Tuple
from pydantic import BaseModel, Field, field_validator
import sente
from src.haive.games.go.models import GoMoveModel

from src.haive.games.framework.base.state import GameState


class GoGameState(BaseModel):
    """A model representing the complete state of a Go game.
    
    This class tracks all aspects of a Go game's state, including:
        - Board configuration and size
        - Move history
        - Captured stones
        - Game status and result
        - Error conditions
    
    Attributes:
        board_size (int): Size of the Go board (default: 19x19).
        board_sgf (str): Current board state in SGF format.
        move_history (List[Tuple[str, int, int]]): List of played moves as
            (color, row, col) tuples.
        captured_stones (Dict[str, int]): Count of stones captured by each player.
        turn (str): Current player to move ("black" or "white").
        game_status (str): Current game status (ongoing/ended/resignation/timeout).
        passes (int): Count of consecutive pass moves.
        error_message (Optional[str]): Error message if any.
        game_result (Optional[str]): Final game result if game is ended.
    
    Example:
        >>> state = GoGameState(
        ...     board_sgf=sente.sgf.dumps(sente.Game(19)),
        ...     turn="black",
        ...     captured_stones={"black": 0, "white": 0}
        ... )
        >>> state.validate_turn("black", {"board_sgf": state.board_sgf})
        'black'
    """
    
    board_size: int = Field(
        default=19,
        description="Size of the Go board (NxN)."
    )
    board_sgf: str = Field(
        ...,
        description="Current board state in SGF format."
    )
    move_history: List[Tuple[str, int, int]] = Field(
        default_factory=list,
        description="List of moves as (color, row, col) tuples."
    )
    captured_stones: Dict[Literal["black", "white"], int] = Field(
        default_factory=lambda: {"black": 0, "white": 0},
        description="Count of stones captured by each player."
    )
    turn: Literal["black", "white"] = Field(
        ...,
        description="Current player to move."
    )
    game_status: Literal["ongoing", "ended", "resignation", "timeout"] = Field(
        default="ongoing",
        description="Current status of the game."
    )
    passes: int = Field(
        default=0,
        description="Count of consecutive pass moves."
    )
    error_message: Optional[str] = Field(
        default=None,
        description="Error message if any invalid moves or states occur."
    )
    game_result: Optional[str] = Field(
        default=None,
        description="Final game result when game is ended."
    )

    @field_validator("turn")
    def validate_turn(cls, v, info):
        """Validate that the turn matches the board state.
        
        This validator ensures the turn field matches the actual board state
        by checking against the SGF representation.
        
        Args:
            v (str): The turn value to validate.
            info (ValidationInfo): Validation context with other field values.
        
        Returns:
            str: The validated turn value.
        
        Raises:
            ValueError: If turn doesn't match the board state.
        """
        board_sgf = info.data.get("board_sgf")
        if board_sgf:
            game = sente.sgf.loads(board_sgf)
            expected_turn = "black" if game.turn() == sente.BLACK else "white"
            if v != expected_turn:
                raise ValueError(
                    f"Turn mismatch: Expected {expected_turn}, but state shows {v}."
                )
        return v

