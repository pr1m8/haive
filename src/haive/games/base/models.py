"""Base models for game agents.

This module provides the foundational data models used across game agents.
It includes models for game state, player state, moves, and other common
game-related data structures.

Example:
    >>> board = Board(size=(8, 8))
    >>> player = Player(id="p1", name="Player 1")
    >>> state = GameState(board=board, players=[player])

Typical usage:
    - Use these models as base classes for game-specific models
    - Inherit from these models to add game-specific functionality
"""

from typing import List, Dict, Tuple, Literal, Optional, TypeVar, Generic
from pydantic import BaseModel, Field, field_validator
from abc import ABC
import time

TMove = TypeVar("TMove")  # Generic move type

class MoveModel(BaseModel, Generic[TMove], ABC):
    """Generic model for game moves.
    
    This class represents a move in the game, generic over the specific
    type of move (TMove) used in the game.
    
    Attributes:
        move (TMove): The actual move data.
        player_id (str): ID of the player making the move.
        timestamp (float): When the move was made.
        
    Example:
        >>> class ChessMove(BaseModel):
        ...     from_pos: str
        ...     to_pos: str
        >>> move = MoveModel[ChessMove](
        ...     move=ChessMove(from_pos="e2", to_pos="e4"),
        ...     player_id="p1"
        ... )
    """
    move: TMove = Field(..., description="The move data")
    player_id: str = Field(..., description="ID of the player making the move")
    timestamp: float = Field(default_factory=time.time, description="Move timestamp")

    @field_validator("move")
    def validate_move(cls, move, info):
        """Override in game-specific models to validate the move."""
        return move

class Player(BaseModel):
    """Represents a player in the game.
    
    Base player model with essential player information and state.
    
    Attributes:
        id (str): Unique identifier for the player.
        name (str): Display name of the player.
        score (int): Current score or points.
        is_active (bool): Whether the player is still active in the game.
        
    Example:
        >>> player = Player(id="p1", name="Player 1", score=0)
    """
    id: str = Field(..., description="Unique identifier for the player")
    name: str = Field(..., description="Display name of the player")
    score: int = Field(default=0, description="Current score/points")
    is_active: bool = Field(default=True, description="Whether player is active")

class Board(BaseModel):
    """Represents a generic game board.
    
    This class provides a basic representation of a game board with
    dimensions and optional grid-based structure.
    
    Attributes:
        size (Tuple[int, int]): The dimensions of the board (width, height).
        grid (Optional[List[List[str]]]): Optional grid representation.
        
    Example:
        >>> board = Board(size=(8, 8))
        >>> chess_board = Board(size=(8, 8), grid=[["R", "N", "B", ...]])
    """
    size: Tuple[int, int] = Field(..., description="Board dimensions (width, height)")
    grid: Optional[List[List[str]]] = Field(None, description="Optional grid representation")

class Cell(BaseModel):
    """Represents a cell on the board."""
    row: int = Field(..., description="The row of the cell.")
    col: int = Field(..., description="The column of the cell.")
    content: Optional[str] = Field(None, description="The content of the cell.")

class GameState(BaseModel):
    """Represents the state of a generic game.
    
    Core game state model that can be extended for specific games.
    
    Attributes:
        board (Board): The game board.
        players (List[Player]): List of players in the game.
        current_player (Player): The player whose turn it is.
        game_status (Literal["ongoing", "ended"]): Current game status.
        game_result (Optional[str]): Final result when game ends.
        
    Example:
        >>> state = GameState(
        ...     board=Board(size=(8, 8)),
        ...     players=[Player(id="p1", name="Player 1")],
        ...     current_player=player,
        ...     game_status="ongoing"
        ... )
    """
    board: Board = Field(..., description="The board of the game.")
    players: List[Player] = Field(..., description="The players in the game.")
    current_player: Player = Field(..., description="The current player.")
    game_status: Literal["ongoing", "ended"] = Field(..., description="The status of the game.")
    game_result: Optional[str] = Field(None, description="The result of the game.")

class Piece(BaseModel):
    """Represents a piece on the board."""
    player: Player = Field(..., description="The player that owns the piece.")
    type: str = Field(..., description="The type of the piece.")
    position: Cell = Field(..., description="The position of the piece on the board.")
    
