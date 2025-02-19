from typing import List, Dict, Literal, Optional, Tuple
from pydantic import BaseModel, Field, field_validator
import sente

class GoMoveModel(BaseModel):
    """Represents a structured Go move as (row, col) coordinates."""
    move: Tuple[int, int] = Field(..., description="The move to make, represented as (row, col) coordinates.")
    board_state: Optional[str] = Field(None, description="The current board state as a string for validation.")

    @field_validator("move")
    def validate_move(cls, value, info):
        """Ensures the move is within a valid range for a standard Go board (19x19 by default)."""
        row, col = value
        board_size = 19  # Modify if supporting smaller boards
        
        if not (0 <= row < board_size and 0 <= col < board_size):
            raise ValueError(f"Move {value} is outside the {board_size}x{board_size} board.")
        
        # Ensure the move is not already occupied (if board state is available)
        board_state = info.data.get("board_state")
        if board_state:
            game = sente.Game(19)
            game.set_board_from_string(board_state)
            if game.get(row, col) != sente.EMPTY:
                raise ValueError(f"Move {value} is invalid: Position already occupied.")
        
        return value

class GoPlayerState(BaseModel):
    """Private state information for each Go player."""
    planned_moves: List[Tuple[int, int]] = Field(default_factory=list, description="List of planned moves.")
    strategic_thoughts: List[str] = Field(default_factory=list, description="Strategic ideas and thoughts.")
    territory_estimation: Optional[str] = Field(None, description="Estimated controlled territory.")
    last_captured_stones: List[Tuple[int, int]] = Field(default_factory=list, description="Stones captured last move.")

class GoGameState(BaseModel):
    """Tracks the overall state of the Go game."""
    board_state: str = Field(..., description="Current board state as a string.")
    move_history: List[Tuple[int, int]] = Field(default_factory=list, description="List of played moves.")
    captured_stones: Dict[Literal["black", "white"], int] = Field(default_factory=lambda: {"black": 0, "white": 0})
    turn: Literal["black", "white"] = Field(..., description="Current player to move.")
    game_status: Literal["ongoing", "end", "resignation", "timeout"] = Field(default="ongoing", description="Game status.")
    analysis: Optional[str] = None

    @field_validator("turn")
    def validate_turn(cls, v, info):
        """Ensures the turn matches the actual board state."""
        board_state = info.data.get("board_state")
        if board_state:
            game = sente.Game(19)
            game.set_board_from_string(board_state)
            expected_turn = "black" if game.turn() == sente.BLACK else "white"
            if v != expected_turn:
                raise ValueError(f"Turn mismatch: Expected {expected_turn}, but state shows {v}.")
        return v

class GoAnalysis(BaseModel):
    """Stores a Go position's evaluation and strategy analysis."""
    territory_evaluation: Dict[Literal["black", "white"], int] = Field(..., description="Estimated territory for each player.")
    strong_positions: List[Tuple[int, int]] = Field(default_factory=list, description="List of key strong positions.")
    weak_positions: List[Tuple[int, int]] = Field(default_factory=list, description="List of weak or vulnerable positions.")
    strategic_advice: List[str] = Field(default_factory=list, description="Strategic insights.")

class GoGameStateManager:
    """Manages Go game state initialization and move application."""

    @staticmethod
    def initialize() -> GoGameState:
        """Creates a new game state for Go."""
        game = sente.Game(19)
        return GoGameState(
            board_state=game.to_string(),
            turn="black"
        )

    @staticmethod
    def apply_move(state: GoGameState, move: Tuple[int, int]) -> GoGameState:
        """Applies a move to the Go game state and returns the new state."""
        game = sente.Game(19)
        game.set_board_from_string(state.board_state)

        if not game.is_legal(move[0], move[1]):
            raise ValueError(f"Move {move} is not legal.")

        game.play(move[0], move[1])

        new_state = GoGameState(
            board_state=game.to_string(),
            move_history=state.move_history + [move],
            captured_stones=state.captured_stones.copy(),
            turn="white" if state.turn == "black" else "black",
            game_status=state.game_status
        )

        return new_state
