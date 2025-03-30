from typing import List, Dict, Literal, Optional
from typing_extensions import Annotated
import operator
from src.haive.games.chess.models import ChessMoveModel,SegmentedAnalysis
from src.haive.games.chess.models import ChessMoveValidation
from pydantic import BaseModel, Field, field_validator
import chess
from typing import Tuple
class PlayerPrivateState(BaseModel):
    """Private state information for each player"""
    planned_moves: List[str] = Field(default_factory=list)
    strategic_thoughts: List[str] = Field(default_factory=list)
    position_evaluation: Optional[str] = None
    candidate_move: Optional[str] = None

class ChessGameState(BaseModel):
    """State for the chess game"""
    board_fen: str = Field(..., description="Current board state in FEN notation")
    move_history: List[str] = Field(default_factory=list)
    captured_pieces: Dict[Literal["white", "black"], List[str]] = Field(
        default_factory=lambda: {"white": [], "black": []}
    )
    turn: Literal["white", "black"] = Field(...)
    game_status: Literal["ongoing", "check", "checkmate", "stalemate", "draw"] = Field(
        default="ongoing"
    )
    analysis: Optional[str] = None

import chess
from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Literal, Tuple
import operator
import chess
from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Literal, Tuple
import operator


class EnhancedChessState(BaseModel):
    """Extended chess game state with structured move history and private analyses."""

    board_fens: List[str] = Field(
        default_factory=lambda: [chess.Board().fen()],
        description="List of past FEN board states, latest at the end."
    )

    move_history: List[Tuple[str, str]] = Field(
        default_factory=list,
        description="List of (player_color, UCI move) tuples (trimmed to last 5 moves)."
    )

    captured_pieces: Dict[str, List[str]] = Field(
        default_factory=lambda: {"white": [], "black": []},
        description="Captured pieces per color."
    )

    turn: Literal["white", "black"] = Field(
        default="white",
        description="Indicates which player’s turn it is."
    )

    current_player: Literal["white", "black"] = Field(
        default="white",
        description="Current player making a move."
    )

    game_status: Literal["ongoing", "ended"] = Field(
        default="ongoing",
        description="Indicates if the game is still being played."
    )

    game_result: Optional[str] = Field(
        default=None,
        description="Final game result: winner or draw status."
    )

    white_analysis: List[Dict] = Field(
        default_factory=list,
        description="White's private analysis (trimmed to last 5 analyses)."
    )

    black_analysis: List[Dict] = Field(
        default_factory=list,
        description="Black's private analysis (trimmed to last 5 analyses)."
    )

    error_message: Optional[str] = Field(
        default=None,
        description="Error message if move validation fails."
    )

    @property
    def board_fen(self) -> str:
        """Returns the current board state (latest FEN)."""
        return self.board_fens[-1] if self.board_fens else chess.Board().fen()

    def trim_history(self):
        """Ensures lists do not exceed 5 items."""
        self.move_history = self.move_history[-5:]
        self.board_fens = self.board_fens[-5:]
        self.white_analysis = self.white_analysis[-5:]
        self.black_analysis = self.black_analysis[-5:]

class ChessGameStateManager:
    @staticmethod
    def initialize() -> ChessGameState:
        import chess
        return ChessGameState(
            board_fen=chess.Board().fen(),
            turn="white"
        )

    @staticmethod
    def apply_move(state: ChessGameState, move_uci: str) -> ChessGameState:
        import chess
        board = chess.Board(state.board_fen)
        move = chess.Move.from_uci(move_uci)
        
        # Track captured piece
        captured_piece = board.piece_at(move.to_square)
        
        # Apply move
        board.push(move)
        
        # Create new state
        new_state = ChessGameState(
            board_fen=board.fen(),
            move_history=state.move_history + [move_uci],
            captured_pieces=dict(state.captured_pieces),
            turn="black" if state.turn == "white" else "white",
            game_status=state.game_status,
            analysis=state.analysis
        )

        # Update game status
        if board.is_checkmate():
            new_state.game_status = "checkmate"
        elif board.is_stalemate():
            new_state.game_status = "stalemate"
        elif board.is_check():
            new_state.game_status = "check"
        
        # Track captured pieces
        if captured_piece:
            piece_symbol = captured_piece.symbol()
            new_state.captured_pieces[state.turn].append(piece_symbol)

        return new_state