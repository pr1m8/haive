# src/haive/agents/agent_games/connect4/models.py

"""Connect4 game models module.

This module provides data models for the Connect4 game implementation, including:
    - Move validation and representation
    - Player decisions and analysis
    - Game state components
    - Structured output models for LLMs

Example:
    >>> from src.haive.games.connect4.models import Connect4Move
    >>> 
    >>> # Create and validate a move
    >>> move = Connect4Move(
    ...     column=3,
    ...     explanation="Control the center column"
    ... )
"""

# Standard library imports
from typing import List, Dict, Literal, Optional, Tuple

# Third-party imports
from pydantic import BaseModel, Field, field_validator


class Connect4Move(BaseModel):
    """Model for Connect4 moves with validation.
    
    This class represents a Connect4 move with:
        - Column number (0-6)
        - Optional explanation
        - Move validation
    
    Attributes:
        column (int): Column number (0-6).
        explanation (Optional[str]): Explanation of the move's purpose.
    
    Example:
        >>> move = Connect4Move(
        ...     column=3,
        ...     explanation="Control the center column"
        ... )
    """
    
    column: int = Field(
        ...,
        description="Column number (0-6) where the piece will be dropped."
    )
    
    explanation: Optional[str] = Field(
        default=None,
        description="Optional explanation of the move's purpose."
    )
    
    @field_validator("column")
    def validate_column(cls, v: int) -> int:
        """Validate the column number.
        
        Args:
            v (int): Column number to validate.
        
        Returns:
            int: Validated column number.
        
        Raises:
            ValueError: If the column number is not between 0 and 6.
        """
        if not isinstance(v, int) or v < 0 or v > 6:
            raise ValueError("Column must be an integer between 0 and 6")
        return v

    def __str__(self):
        return f"Drop in column {self.column}"

class Connect4PlayerDecision(BaseModel):
    """Model for Connect4 player decisions.
    
    This class represents a player's decision-making process:
        - Move selection
        - Position evaluation
        - Alternative moves considered
        - Reasoning process
    
    Attributes:
        move (Connect4Move): Chosen move with explanation.
        position_eval (str): Player's assessment of the position.
        alternatives (List[Connect4Move]): Alternative moves considered.
        reasoning (str): Detailed reasoning for the move choice.
    
    Example:
        >>> decision = Connect4PlayerDecision(
        ...     move=Connect4Move(column=3, explanation="Control center"),
        ...     position_eval="Strong position with center control",
        ...     alternatives=[
        ...         Connect4Move(column=2, explanation="Alternative center approach")
        ...     ],
        ...     reasoning="Playing in column 3 maintains center control"
        ... )
    """
    
    move: Connect4Move = Field(
        ...,
        description="Selected move with explanation."
    )
    
    position_eval: str = Field(
        ...,
        description="Player's assessment of the current position."
    )
    
    alternatives: List[Connect4Move] = Field(
        default_factory=list,
        description="Alternative moves that were considered."
    )
    
    reasoning: str = Field(
        ...,
        description="Detailed reasoning for the move choice."
    )

class Connect4Analysis(BaseModel):
    """Model for Connect4 position analysis.
    
    This class represents a detailed analysis of a Connect4 position:
        - Position evaluation
        - Center control assessment
        - Threat detection
        - Strategic plans
    
    Attributes:
        position_score (float): Position evaluation (-1.0 to 1.0).
        center_control (int): Center control rating (0-10).
        threats (Dict[str, List[int]]): Detected threats and opportunities.
        suggested_columns (List[int]): Recommended columns to play.
        winning_chances (int): Estimated winning chances (0-100).
    
    Example:
        >>> analysis = Connect4Analysis(
        ...     position_score=0.5,
        ...     center_control=8,
        ...     threats={
        ...         "winning_moves": [3],
        ...         "blocking_moves": [4]
        ...     },
        ...     suggested_columns=[3, 2, 4],
        ...     winning_chances=75
        ... )
    """
    
    position_score: float = Field(
        default=0.0,
        description="Position evaluation (-1.0 to 1.0, positive favors current player)."
    )
    
    center_control: int = Field(
        default=5,
        description="Rating of center column control (0-10)."
    )
    
    threats: Dict[str, List[int]] = Field(
        default_factory=lambda: {"winning_moves": [], "blocking_moves": []},
        description="Detected threats and opportunities."
    )
    
    suggested_columns: List[int] = Field(
        default_factory=list,
        description="List of recommended columns to play."
    )
    
    winning_chances: int = Field(
        default=50,
        description="Estimated winning chances (0-100)."
    )
    
    @field_validator("center_control")
    def validate_center_control(cls, v: int) -> int:
        """Validate the center control rating.
        
        Args:
            v (int): Center control rating to validate.
        
        Returns:
            int: Validated center control rating.
        
        Raises:
            ValueError: If the rating is not between 0 and 10.
        """
        if not isinstance(v, int) or v < 0 or v > 10:
            raise ValueError("Center control must be an integer between 0 and 10")
        return v
    
    @field_validator("winning_chances")
    def validate_winning_chances(cls, v: int) -> int:
        """Validate the winning chances percentage.
        
        Args:
            v (int): Winning chances percentage to validate.
        
        Returns:
            int: Validated winning chances percentage.
        
        Raises:
            ValueError: If the percentage is not between 0 and 100.
        """
        if not isinstance(v, int) or v < 0 or v > 100:
            raise ValueError("Winning chances must be an integer between 0 and 100")
        return v

