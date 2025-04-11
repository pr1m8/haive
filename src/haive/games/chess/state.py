"""
Chess game state models.

This module provides state models for the chess game, including:
    - Game state tracking
    - Move history
    - Board state
    - Player analysis
"""

from typing import List, Dict, Optional, Literal, Tuple, Union, Any
from pydantic import BaseModel, Field, computed_field
import chess

class ChessState(BaseModel):
    """
    State for the chess game.
    
    This class represents the complete game state including:
        - Board positions (current and history)
        - Move history
        - Game status
        - Player analysis
        - Captured pieces
    
    Attributes:
        board_fens (List[str]): List of FEN board states (latest at the end)
        move_history (List[Tuple[str, str]]): List of (player, move) tuples
        current_player (str): Current player ("white" or "black")
        turn (str): Current turn ("white" or "black")
        game_status (str): Status of the game
        game_result (Optional[str]): Final result when game is over
        white_analysis (List[Dict]): White's position analysis
        black_analysis (List[Dict]): Black's position analysis
        captured_pieces (Dict[str, List[str]]): Captured pieces by each player
        error_message (Optional[str]): Error message if any
    """
    
    board_fens: List[str] = Field(
        default_factory=lambda: [chess.Board().fen()],
        description="List of FEN board states, latest at the end"
    )
    
    move_history: List[Tuple[str, str]] = Field(
        default_factory=list,
        description="List of (player_color, UCI move) tuples"
    )
    
    current_player: Literal["white", "black"] = Field(
        default="white",
        description="Current player making a move"
    )
    
    turn: Literal["white", "black"] = Field(
        default="white",
        description="Current turn"
    )
    
    game_status: Literal["ongoing", "check", "checkmate", "stalemate", "draw"] = Field(
        default="ongoing",
        description="Status of the game"
    )
    
    game_result: Optional[str] = Field(
        default=None,
        description="Final game result (white_win, black_win, draw)"
    )
    
    white_analysis: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="White's position analysis"
    )
    
    black_analysis: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="Black's position analysis"
    )
    
    captured_pieces: Dict[str, List[str]] = Field(
        default_factory=lambda: {"white": [], "black": []},
        description="Captured pieces by each player"
    )
    
    error_message: Optional[str] = Field(
        default=None,
        description="Error message if any"
    )
    
    @computed_field
    def board_fen(self) -> str:
        """Get the current board state (latest FEN)."""
        return self.board_fens[-1] if self.board_fens else chess.Board().fen()
    
    def get_board(self) -> chess.Board:
        """Get a chess.Board object for the current position."""
        return chess.Board(self.board_fen)
    
    def model_dump(self) -> Dict[str, Any]:
        """Convert state to a dictionary."""
        # Create a dictionary with all fields
        result = super().model_dump()
        
        # Add computed property
        result["board_fen"] = self.board_fen
        
        return result
    
    def dict(self) -> Dict[str, Any]:
        """Legacy compatibility method."""
        return self.model_dump()
    
    class Config:
        """Pydantic configuration."""
        arbitrary_types_allowed = True