"""Chess game models module.

This module provides data models for the chess game implementation, including:
    - Move validation and representation
    - Player decisions and analysis
    - Game state components
    - Structured output models for LLMs

Example:
    >>> from src.haive.games.chess.models import ChessMoveModel
    >>> 
    >>> # Create and validate a move
    >>> move = ChessMoveModel(
    ...     move="e2e4",
    ...     explanation="Opening with king's pawn"
    ... )
"""

from pydantic import BaseModel, Field, field_validator
import chess
from chess import Board
from typing import List, Optional, Dict, Literal

class ChessMoveModel(BaseModel):
    """Model for chess moves with validation.
    
    This class represents a chess move with:
        - UCI notation (e.g., "e2e4")
        - Optional explanation
        - Move validation
    
    Attributes:
        move (str): Move in UCI notation.
        explanation (Optional[str]): Explanation of the move's purpose.
    
    Example:
        >>> move = ChessMoveModel(
        ...     move="e2e4",
        ...     explanation="Control the center with king's pawn"
        ... )
    """
    
    move: str = Field(
        ...,
        description="Move in UCI notation (e.g., 'e2e4')."
    )
    
    explanation: Optional[str] = Field(
        default=None,
        description="Optional explanation of the move's purpose."
    )
    
    @field_validator("move")
    def validate_move(cls, v: str) -> str:
        """Validate the move format.
        
        Args:
            v (str): Move in UCI notation.
        
        Returns:
            str: Validated move.
        
        Raises:
            ValueError: If the move format is invalid.
        """
        if not isinstance(v, str) or len(v) < 4:
            raise ValueError("Move must be a string of at least 4 characters")
        return v

    @field_validator("move")
    def validate_uci(cls, value, info):
        """Ensure the UCI move is valid and legal in the current position."""
        try:
            move = chess.Move.from_uci(value)
            if not move:
                raise ValueError("Invalid UCI format")
            
            # Get the board FEN from the validation context
            board_fen = info.data.get('board_fen')
            if board_fen:
                board = chess.Board(board_fen)
                if move not in board.legal_moves:
                    raise ValueError(f"Move {value} is not legal in current position")
            
        except ValueError as e:
            raise ValueError(f"Invalid move: {str(e)}")
        return value

    @classmethod
    def from_move(cls, move: chess.Move, board_fen: str = None):
        """Creates a ChessMoveModel from a python-chess Move."""
        return cls(move=move.uci(), board_fen=board_fen)

    def to_move(self):
        """Converts the model back to a python-chess move object."""
        return chess.Move.from_uci(self.move)

class ChessPlayerDecision(BaseModel):
    """Model for chess player decisions.
    
    This class represents a player's decision-making process:
        - Move selection
        - Position evaluation
        - Alternative moves considered
        - Reasoning process
    
    Attributes:
        selected_move (ChessMoveModel): Chosen move with explanation.
        position_eval (str): Player's assessment of the position.
        alternatives (List[ChessMoveModel]): Alternative moves considered.
        reasoning (str): Detailed reasoning for the move choice.
    
    Example:
        >>> decision = ChessPlayerDecision(
        ...     selected_move=ChessMoveModel(move="e2e4", explanation="Control center"),
        ...     position_eval="Equal position with attacking chances",
        ...     alternatives=[
        ...         ChessMoveModel(move="d2d4", explanation="Alternative center control")
        ...     ],
        ...     reasoning="Opening with e4 gives good control of central squares"
        ... )
    """
    
    selected_move: ChessMoveModel = Field(
        ...,
        description="Selected move with explanation."
    )
    
    position_eval: str = Field(
        ...,
        description="Player's assessment of the current position."
    )
    
    alternatives: List[ChessMoveModel] = Field(
        default_factory=list,
        description="Alternative moves that were considered."
    )
    
    reasoning: str = Field(
        ...,
        description="Detailed reasoning for the move choice."
    )

class ChessPosition(BaseModel):
    """Represents a chess position with its key characteristics."""
    material_balance: int = Field(..., description="Material balance in centipawns")
    control_of_center: str = Field(..., description="Assessment of center control: strong/weak/equal")
    king_safety: str = Field(..., description="Assessment of king safety for both sides")
    pawn_structure: str = Field(..., description="Description of pawn structure strengths/weaknesses")

class ChessAnalysis(BaseModel):
    """Model for chess position analysis.
    
    This class represents a detailed analysis of a chess position:
        - Material evaluation
        - Positional assessment
        - Tactical opportunities
        - Strategic plans
    
    Attributes:
        material_eval (float): Material evaluation in pawns.
        position_eval (str): Qualitative position assessment.
        tactics (List[str]): List of tactical opportunities.
        strategy (str): Long-term strategic plan.
        best_moves (List[str]): Suggested best moves.
    
    Example:
        >>> analysis = ChessAnalysis(
        ...     material_eval=0.5,
        ...     position_eval="White has a slight edge due to better pawn structure",
        ...     tactics=["Pin on e-file", "Knight fork possibility on d5"],
        ...     strategy="Control central squares and prepare kingside attack",
        ...     best_moves=["e4", "Nf3", "d4"]
        ... )
    """
    
    material_eval: float = Field(
        default=0.0,
        description="Material evaluation in pawns (positive favors white)."
    )
    
    position_eval: str = Field(
        ...,
        description="Qualitative assessment of the position."
    )
    
    tactics: List[str] = Field(
        default_factory=list,
        description="List of tactical opportunities."
    )
    
    strategy: str = Field(
        ...,
        description="Long-term strategic plan."
    )
    
    best_moves: List[str] = Field(
        default_factory=list,
        description="List of suggested best moves in order of preference."
    )

class SegmentedAnalysis(BaseModel):
    position_score: float = Field(..., description="The score evaluation of the position")
    attacking_chances: str = Field(..., description="Likelihood of a successful attack")
    suggested_plans: List[str] = Field(..., description="Recommended next plans")
    defensive_needs: Optional[str] = Field(None, description="Defensive needs and counterplay ideas")

class ChessMoveValidation(BaseModel):
    """Model for chess move validation results.
    
    This class represents the validation of a chess move:
        - Move legality
        - Error messages
        - Resulting position
    
    Attributes:
        is_valid (bool): Whether the move is legal.
        error_message (Optional[str]): Error message if move is invalid.
        resulting_fen (Optional[str]): FEN of position after move.
    
    Example:
        >>> validation = ChessMoveValidation(
        ...     is_valid=True,
        ...     resulting_fen="rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1"
        ... )
    """
    
    is_valid: bool = Field(
        ...,
        description="Whether the move is legal in the current position."
    )
    
    error_message: Optional[str] = Field(
        default=None,
        description="Error message if the move is invalid."
    )
    
    resulting_fen: Optional[str] = Field(
        default=None,
        description="FEN notation of the position after the move."
    )
