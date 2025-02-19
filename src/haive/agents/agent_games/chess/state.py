from typing import List, Dict, Literal, Optional
from typing_extensions import Annotated
import operator
from src.haive.agents.agent_games.chess.models import ChessMoveModel,SegmentedAnalysis
from src.haive.agents.agent_games.chess.models import ChessMoveValidation
from pydantic import BaseModel, Field, field_validator
import chess

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
class EnhancedChessState(ChessGameState):
    """Enhanced state tracking for chess game"""
    current_player: Literal["white", "black"] = Field(..., description="Current player to move")
    white_analysis: Optional[SegmentedAnalysis] = None
    black_analysis: Optional[SegmentedAnalysis] = None
    last_move_validation: Optional[ChessMoveValidation] = None
    captured_pieces: Dict[str, List[str]] = Field(default_factory=lambda: {"white": [], "black": []})
    
    @field_validator("current_player")
    def validate_turn(cls, v, info):
        # Get the data from the ValidationInfo object
        data = info.data
        
        if hasattr(data, "get"):
            board_fen = data.get("board_fen")
            if board_fen:
                board = chess.Board(board_fen)
                expected_turn = "white" if board.turn == chess.WHITE else "black"
                if v != expected_turn:
                    raise ValueError(f"Turn mismatch. Board shows {expected_turn}'s turn, but state shows {v}'s turn")
        return v
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
