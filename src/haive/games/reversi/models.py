"""
Data models for Reversi (Othello) gameplay and analysis.

Includes core types for representing player moves and board position evaluations.
"""

from typing import List, Literal, Optional, Dict
from pydantic import BaseModel, Field
from src.haive.games.framework.base.state import GameState

class Position(BaseModel):
    """
    A coordinate on the Reversi board.

    Attributes:
        row (int): Row index (0-7).
        col (int): Column index (0-7).
    """
    row: int = Field(..., ge=0, lt=8, description="Row index (0-7)")
    col: int = Field(..., ge=0, lt=8, description="Column index (0-7)")

class ReversiMove(BaseModel):
    """
    Represents a single Reversi move.

    Attributes:
        row (int): Row position of the move (0-7).
        col (int): Column position of the move (0-7).
        player (str): The player making the move ('B' or 'W').
    """
    row: int = Field(..., ge=0, lt=8, description="Row index (0-7)")
    col: int = Field(..., ge=0, lt=8, description="Column index (0-7)")
    player: Literal["B", "W"] = Field(..., description="Player making the move (B=Black, W=White)")

    def __str__(self):
        row_letter = chr(ord('A') + self.row)
        col_num = self.col + 1
        return f"{self.player} places at {row_letter}{col_num} ({self.row}, {self.col})"

class ReversiAnalysis(BaseModel):
    """
    Strategy and evaluation report for a Reversi position.

    Attributes:
        mobility (int): Number of legal moves available.
        frontier_discs (int): Count of discs adjacent to at least one empty space.
        corner_discs (int): Number of corners occupied by the player.
        stable_discs (int): Discs that cannot be flipped.
        positional_score (int): Positional heuristic score.
        position_evaluation (str): Assessment of advantage (e.g., 'winning', 'equal').
        recommended_moves (List[Position]): Preferred moves based on analysis.
        danger_zones (List[Position]): High-risk positions to avoid.
        strategy (str): Summary of strategic approach.
        reasoning (str): Detailed explanation of analysis.
    """
    mobility: int = Field(..., description="Number of legal moves available")
    frontier_discs: int = Field(..., description="Number of discs adjacent to empty spaces")
    corner_discs: int = Field(..., description="Number of corner positions captured")
    stable_discs: int = Field(..., description="Number of discs that cannot be flipped")
    positional_score: int = Field(..., description="Score based on strategic position values")
    position_evaluation: Literal["winning", "losing", "equal", "unclear"] = Field(
        ..., description="Overall position evaluation"
    )
    recommended_moves: List[Position] = Field(
        ..., description="List of recommended moves in order of preference"
    )
    danger_zones: List[Position] = Field(
        ..., description="Positions to avoid (may lead to opponent advantage)"
    )
    strategy: str = Field(..., description="Strategic assessment and recommendation")
    reasoning: str = Field(..., description="Detailed reasoning for the analysis")