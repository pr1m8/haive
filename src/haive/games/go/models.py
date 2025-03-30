"""Go game data models.

This module provides Pydantic models for representing Go game concepts:
    - Move coordinates and validation
    - Player decisions
    - Position analysis and evaluation
    - Territory control tracking

Example:
    >>> from src.haive.games.go.models import GoMoveModel, GoAnalysis
    >>> 
    >>> # Create and validate a move
    >>> move = GoMoveModel(move=(3, 4), board_size=19)
    >>> move.to_tuple()
    (3, 4)
    >>> 
    >>> # Create a position analysis
    >>> analysis = GoAnalysis(
    ...     territory_control={"black": 45, "white": 40},
    ...     strong_positions=[(3, 3), (15, 15)],
    ...     weak_positions=[(0, 0)],
    ...     suggested_strategies=["Strengthen the center group"]
    ... )
"""

from typing import List, Dict, Literal, Optional, Tuple
from pydantic import BaseModel, Field, field_validator
import sente


class GoMoveModel(BaseModel):
    """A model representing a move in Go.
    
    This model validates and stores move coordinates, ensuring they are
    within the bounds of the game board.
    
    Attributes:
        move (Tuple[int, int]): The (row, col) coordinates of the move.
        board_size (int): Size of the game board (default 19x19).
    
    Example:
        >>> move = GoMoveModel(move=(3, 4))
        >>> move.validate_move((3, 4), {"board_size": 19})
        (3, 4)
        >>> move.to_tuple()
        (3, 4)
        >>> 
        >>> # Invalid move raises error
        >>> GoMoveModel(move=(19, 19))  # Out of bounds
        ValueError: Move (19, 19) is out of bounds for a 19x19 board.
    """
    
    move: Tuple[int, int] = Field(
        ..., 
        description="Move coordinates as (row, col) tuple."
    )
    board_size: int = Field(
        default=19, 
        description="Size of the game board (NxN)."
    )

    @field_validator("move")
    def validate_move(cls, move: Tuple[int, int], values):
        """Validate that a move is within board bounds.
        
        Args:
            move (Tuple[int, int]): The move coordinates to validate.
            values (dict): Dictionary containing model field values.
        
        Returns:
            Tuple[int, int]: The validated move coordinates.
        
        Raises:
            ValueError: If move coordinates are outside board bounds.
        """
        row, col = move
        board_size = values.get("board_size", 19)

        if not (0 <= row < board_size and 0 <= col < board_size):
            raise ValueError(
                f"Move {move} is out of bounds for a {board_size}x{board_size} board."
            )

        return move

    def to_tuple(self) -> Tuple[int, int]:
        """Convert the move to a simple coordinate tuple.
        
        Returns:
            Tuple[int, int]: The move coordinates as (row, col).
        """
        return self.move


class GoPlayerDecision(BaseModel):
    """A model representing a player's move decision.
    
    This model encapsulates a player's decision about their next move,
    including validation of the move coordinates.
    
    Attributes:
        move (GoMoveModel): The chosen move coordinates and validation.
    
    Example:
        >>> decision = GoPlayerDecision(
        ...     move=GoMoveModel(move=(3, 4))
        ... )
        >>> decision.move.to_tuple()
        (3, 4)
    """
    
    move: GoMoveModel = Field(
        ..., 
        description="The player's chosen move."
    )


class GoAnalysis(BaseModel):
    """A model for storing Go position analysis.
    
    This model captures a comprehensive analysis of a Go position,
    including territory control, key positions, and strategic advice.
    
    Attributes:
        territory_control (Dict[str, int]): Estimated territory for each player.
        strong_positions (List[Tuple[int, int]]): List of strong positions.
        weak_positions (List[Tuple[int, int]]): List of vulnerable positions.
        suggested_strategies (List[str]): List of strategic recommendations.
    
    Example:
        >>> analysis = GoAnalysis(
        ...     territory_control={"black": 45, "white": 40},
        ...     strong_positions=[(3, 3), (15, 15)],
        ...     weak_positions=[(0, 0)],
        ...     suggested_strategies=[
        ...         "Strengthen the center group",
        ...         "Consider invading the top right"
        ...     ]
        ... )
    """
    
    territory_control: Dict[Literal["black", "white"], int] = Field(
        ..., 
        description="Estimated territory control points for each player."
    )
    strong_positions: List[Tuple[int, int]] = Field(
        default_factory=list, 
        description="List of strategically strong positions."
    )
    weak_positions: List[Tuple[int, int]] = Field(
        default_factory=list, 
        description="List of vulnerable positions needing attention."
    )
    suggested_strategies: List[str] = Field(
        default_factory=list, 
        description="List of strategic recommendations for the position."
    )
