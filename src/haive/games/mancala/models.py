"""
Models for the Mancala game.

This module defines the models for the Mancala game,
including the move and analysis models.
"""
from pydantic import BaseModel, Field, field_validator
from typing import Literal, List

class MancalaMove(BaseModel):
    """Represents a move in Mancala.

    This class defines the structure of a move in Mancala,
    which includes the pit index to sow from and the player making the move.
    """
    pit_index: int = Field(..., ge=0, lt=6, description="Index of the pit to sow from (0-5)")
    player: Literal["player1", "player2"] = Field(..., description="Player making the move")
    
    @field_validator('pit_index')
    def validate_pit_index(cls, v, values):
        """Validate that the pit index is valid for the player.

        Args:
            v: The pit index to validate.
            values: The values of the other fields.

        Returns:
            The validated pit index.
        """
        if 'player' in values.data:
            # Adjust validation based on player
            if values.data['player'] == 'player1' and not (0 <= v < 6):
                raise ValueError(f"Player 1 pit index must be 0-5, got {v}")
            elif values.data['player'] == 'player2' and not (0 <= v < 6):
                raise ValueError(f"Player 2 pit index must be 0-5, got {v}")
        return v
    
    def __str__(self):
        return f"{self.player} sows from pit {self.pit_index}"


class MancalaAnalysis(BaseModel):
    """Analysis of a Mancala position.

    This class defines the structure of an analysis for a Mancala position,
    which includes the overall position evaluation, advantage level,
    stone distribution, pit recommendations, strategic focus, key tactics,
    and reasoning.
    """
    position_evaluation: Literal["winning", "losing", "equal", "unclear"] = Field(
        ..., description="Overall position evaluation"
    )
    advantage_level: int = Field(
        ..., ge=0, le=10, description="Level of advantage (0-10, where 10 is winning)"
    )
    stone_distribution: str = Field(
        ..., description="Analysis of stone distribution"
    )
    pit_recommendations: List[int] = Field(
        ..., description="Recommended pits to play from"
    )
    strategy_focus: Literal["offensive", "defensive", "balanced"] = Field(
        ..., description="Current strategic focus"
    )
    key_tactics: List[str] = Field(
        ..., description="Key tactical considerations"
    )
    reasoning: str = Field(
        ..., description="Detailed reasoning for the analysis"
    )