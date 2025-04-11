"""
Models for Tic Tac Toe gameplay and analysis.

Includes representations for player moves and strategic analysis output.
These models are used for structured outputs and intermediate reasoning steps
by agents or game managers.
"""

from typing import List, Dict, Optional, Literal
from pydantic import BaseModel, Field

class TicTacToeMove(BaseModel):
    """
    Represents a single move in a Tic Tac Toe game.

    Attributes:
        row (int): Row index (0-2) where the player wants to place their symbol.
        col (int): Column index (0-2) where the player wants to place their symbol.
        player (Literal['X', 'O']): The symbol representing the player ('X' or 'O').
    """
    row: int = Field(..., ge=0, lt=3, description="Row index (0-2)")
    col: int = Field(..., ge=0, lt=3, description="Column index (0-2)")
    player: Literal["X", "O"] = Field(..., description="Player making the move")

    def __str__(self):
        return f"{self.player} places at ({self.row}, {self.col})"


class TicTacToeAnalysis(BaseModel):
    """
    Strategic analysis of a Tic Tac Toe board position.

    Attributes:
        winning_moves (List[Dict[str, int]]): List of winning move coordinates for the current player.
        blocking_moves (List[Dict[str, int]]): List of blocking moves to prevent opponent's win.
        fork_opportunities (List[Dict[str, int]]): List of moves that can create a fork.
        center_available (bool): Whether the center cell is empty.
        corner_available (bool): Whether any corner cell is empty.
        position_evaluation (str): Summary of the position's status (winning, losing, drawing, unclear).
        recommended_move (Optional[Dict[str, int]]): Suggested best move based on analysis.
        strategy (str): Strategic recommendation and explanation.
    """
    winning_moves: List[Dict[str, int]] = Field(
        default_factory=list,
        description="List of winning moves (row, col) for the current player, if any"
    )
    blocking_moves: List[Dict[str, int]] = Field(
        default_factory=list,
        description="List of moves (row, col) to block opponent from winning immediately"
    )
    fork_opportunities: List[Dict[str, int]] = Field(
        default_factory=list,
        description="List of moves (row, col) that create multiple simultaneous threats (forks)"
    )
    center_available: bool = Field(
        ..., 
        description="Whether the center square (1,1) is currently unoccupied"
    )
    corner_available: bool = Field(
        ..., 
        description="Whether any corner square is currently unoccupied"
    )
    position_evaluation: Literal["winning", "losing", "drawing", "unclear"] = Field(
        ..., 
        description="High-level evaluation of the board position from the current player's perspective"
    )
    recommended_move: Optional[Dict[str, int]] = Field(
        default=None,
        description="Best move (row, col) to play next, if applicable"
    )
    strategy: str = Field(
        ..., 
        description="Narrative explanation of the best strategy for the current position"
    )