from typing import List, Dict, Literal, Optional, Tuple
from pydantic import BaseModel, Field
import sente
from src.haive.games.go.models import GoMoveModel
from typing import List, Dict, Literal, Optional, Tuple
from pydantic import BaseModel, Field, field_validator
import sente

class GoGameState(BaseModel):
    """Tracks the overall state of the Go game."""
    board_size: int = Field(default=19, description="Size of the Go board (default: 19x19).")
    board_sgf: str = Field(..., description="Current board state in SGF format.")
    move_history: List[Tuple[str, int, int]] = Field(default_factory=list, description="List of played moves.")
    captured_stones: Dict[Literal["black", "white"], int] = Field(default_factory=lambda: {"black": 0, "white": 0})
    turn: Literal["black", "white"] = Field(..., description="Current player to move.")
    game_status: Literal["ongoing", "ended", "resignation", "timeout"] = Field(default="ongoing", description="Game status.")
    passes: int = Field(default=0, description="Consecutive passes count.")
    error_message: Optional[str] = None
    game_result: Optional[str] = None

    @field_validator("turn")
    def validate_turn(cls, v, info):
        """Ensures the turn matches the actual board state."""
        board_sgf = info.data.get("board_sgf")
        if board_sgf:
            game = sente.sgf.loads(board_sgf)
            expected_turn = "black" if game.turn() == sente.BLACK else "white"
            if v != expected_turn:
                raise ValueError(f"Turn mismatch: Expected {expected_turn}, but state shows {v}.")
        return v


class GoGameStateManager:
    """Manages Go game state and move application."""

    @staticmethod
    def initialize(board_size: int = 19) -> GoGameState:
        """Initialize a new Go game state."""
        game = sente.Game(board_size)
        return GoGameState(
            board_sgf=sente.sgf.dumps(game),
            turn="black"
        )

    @staticmethod
    def apply_move(state: GoGameState, move: Optional[Tuple[int, int]]) -> GoGameState:
        """Apply a move to the Go game state."""
        game = sente.sgf.loads(state.board_sgf)[0]
        player = state.turn  # Current player

        # Handle pass move
        if move is None:
            new_passes = state.passes + 1
            return GoGameState(
                **state.dict(),
                turn="white" if player == "black" else "black",
                passes=new_passes,
                game_status="ended" if new_passes >= 2 else "ongoing",
                game_result="Draw" if new_passes >= 2 else None
            )

        new_passes = 0  # Reset pass count

        try:
            game.play(*move)
        except Exception as e:
            return GoGameState(**state.dict(), error_message=f"Invalid move: {str(e)}")

        # Capture tracking
        captured_count = game.get_captures(player)

        return GoGameState(
            board_sgf=sente.sgf.dumps(game),
            move_history=state.move_history + [(player, move)],
            captured_stones={
                "black": state.captured_stones["black"] + (captured_count if player == "white" else 0),
                "white": state.captured_stones["white"] + (captured_count if player == "black" else 0),
            },
            turn="white" if player == "black" else "black",
            passes=new_passes,
            game_status="ended" if game.is_over() else "ongoing",
            game_result=game.get_winner() if game.is_over() else None
        )
