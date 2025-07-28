"""Chess game models module.

This module provides data models for the chess game, including:
    - Move representation
    - Player decisions
    - Position analysis
    - Structured output models for LLMs
"""

import chess
from pydantic import BaseModel, Field, field_validator


class ChessMoveModel(BaseModel):
    """Model for chess moves with validation.

    This class represents a chess move with:
        - UCI notation (e.g., "e2e4")
        - Optional explanation
        - Move validation

    Attributes:
        move (str): Move in UCI notation
        explanation (Optional[str]): Explanation of the move's purpose
    """

    move: str = Field(..., description="Move in UCI notation (e.g., 'e2e4')")

    explanation: str | None = Field(
        default=None, description="Optional explanation of the move's purpose"
    )

    @field_validator("move")
    @classmethod
    def validate_move(cls, v: str) -> str:
        """Validate the move format.

        Args:
            v: The move string to validate

        Returns:
            The validated move string

        Raises:
            ValueError: If move is not a string or too short
        """
        if not isinstance(v, str) or len(v) < 4:
            raise ValueError("Move must be a string of at least 4 characters")
        return v

    def to_move(self) -> chess.Move:
        """Convert to a chess.Move object."""
        return chess.Move.from_uci(self.move)

    @classmethod
    def from_move(
        cls, move: chess.Move, explanation: str | None = None
    ) -> "ChessMoveModel":
        """Create from a chess.Move object."""
        return cls(move=move.uci(), explanation=explanation)


class ChessPlayerDecision(BaseModel):
    """Model for chess player decisions.

    This class represents a player's decision-making process:
        - Move selection
        - Position evaluation
        - Alternative moves considered
        - Reasoning process

    Attributes:
        selected_move (ChessMoveModel): Chosen move with explanation
        position_eval (str): Player's assessment of the position
        alternatives (List[ChessMoveModel]): Alternative moves considered
        reasoning (str): Detailed reasoning for the move choice
    """

    selected_move: ChessMoveModel = Field(
        ..., description="Selected move with explanation"
    )

    position_eval: str = Field(
        ..., description="Player's assessment of the current position"
    )

    alternatives: list[ChessMoveModel] = Field(
        default_factory=list, description="Alternative moves that were considered"
    )

    reasoning: str = Field(..., description="Detailed reasoning for the move choice")


class ChessAnalysis(BaseModel):
    """Model for chess position analysis.

    This class represents a detailed analysis of a chess position:
        - Material evaluation
        - Positional assessment
        - Tactical opportunities
        - Strategic plans

    Attributes:
        material_eval (float): Material evaluation in pawns
        position_eval (str): Qualitative position assessment
        tactics (List[str]): List of tactical opportunities
        strategy (str): Long-term strategic plan
        best_moves (List[str]): Suggested best moves
    """

    material_eval: float = Field(
        default=0.0, description="Material evaluation in pawns (positive favors white)"
    )

    position_eval: str = Field(
        ..., description="Qualitative assessment of the position"
    )

    tactics: list[str] = Field(
        default_factory=list, description="List of tactical opportunities"
    )

    strategy: str = Field(..., description="Long-term strategic plan")

    best_moves: list[str] = Field(
        default_factory=list,
        description="List of suggested best moves in order of preference",
    )


class SegmentedAnalysis(BaseModel):
    """Structured analysis of a chess position in segments.

    This class breaks down position analysis into distinct categories:
        - Numerical position score
        - Attacking chances
        - Defensive needs
        - Strategic plans

    Attributes:
        position_score (float): The score evaluation of the position
        attacking_chances (str): Likelihood of a successful attack
        suggested_plans (List[str]): Recommended next plans
        defensive_needs (Optional[str]): Defensive needs and counterplay ideas
    """

    position_score: float = Field(
        ..., description="The score evaluation of the position"
    )

    attacking_chances: str = Field(..., description="Likelihood of a successful attack")

    suggested_plans: list[str] = Field(..., description="Recommended next plans")

    defensive_needs: str | None = Field(
        default=None, description="Defensive needs and counterplay ideas"
    )


class ChessMoveValidation(BaseModel):
    """Model for chess move validation results.

    This class represents the validation of a chess move:
        - Move legality
        - Error messages
        - Resulting position

    Attributes:
        is_valid (bool): Whether the move is legal
        error_message (Optional[str]): Error message if move is invalid
        resulting_fen (Optional[str]): FEN of position after move
    """

    is_valid: bool = Field(
        ..., description="Whether the move is legal in the current position"
    )

    error_message: str | None = Field(
        default=None, description="Error message if the move is invalid"
    )

    resulting_fen: str | None = Field(
        default=None, description="FEN notation of the position after the move"
    )
