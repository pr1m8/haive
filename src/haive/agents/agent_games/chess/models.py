from pydantic import BaseModel, Field, field_validator
import chess
from chess import Board
from typing import List, Optional, Dict, Literal

class ChessMoveModel(BaseModel):
    """Represents a structured chess move in UCI notation."""
    uci: str = Field(..., description="Universal Chess Interface (UCI) move notation, e.g., 'e2e4'.")
    board_fen: str = Field(None, description="The chess board state FEN string for move validation")

    @field_validator("uci")
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
        return cls(uci=move.uci(), board_fen=board_fen)

    def to_move(self):
        """Converts the model back to a python-chess move object."""
        return chess.Move.from_uci(self.uci)

class ChessPlayerDecision(BaseModel):
    """Player agent's decision on the next move. Simple and focused on the move only."""
    move: ChessMoveModel = Field(..., description="The move to make, formatted in UCI notation.")

class ChessPosition(BaseModel):
    """Represents a chess position with its key characteristics."""
    material_balance: int = Field(..., description="Material balance in centipawns")
    control_of_center: str = Field(..., description="Assessment of center control: strong/weak/equal")
    king_safety: str = Field(..., description="Assessment of king safety for both sides")
    pawn_structure: str = Field(..., description="Description of pawn structure strengths/weaknesses")

class ChessAnalysis(BaseModel):
    """Analyzer agent's detailed analysis of the position and moves."""
    position_assessment: ChessPosition = Field(..., description="Analysis of current position")
    strategic_themes: List[str] = Field(..., description="Key strategic themes in the position")
    candidate_moves: List[ChessMoveModel] = Field(..., description="Potential good moves to consider")
    threats: List[str] = Field(default=[], description="Immediate threats in the position")
    long_term_plans: List[str] = Field(default=[], description="Suggested long-term plans")
    previous_move_evaluation: Optional[str] = Field(None, description="Evaluation of the last move played")

class SegmentedAnalysis(BaseModel):
    position_score: float = Field(..., description="The score evaluation of the position")
    attacking_chances: str = Field(..., description="Likelihood of a successful attack")
    suggested_plans: List[str] = Field(..., description="Recommended next plans")
    defensive_needs: Optional[str] = Field(None, description="Defensive needs and counterplay ideas")

class ChessMoveValidation(BaseModel):
    """Validates chess moves and piece ownership."""
    move: str = Field(..., description="Move in UCI notation")
    board_fen: str = Field(..., description="Current board state in FEN notation")
    player_color: Literal["white", "black"] = Field(..., description="Player making the move")

    @field_validator("move")
    def validate_move_and_ownership(cls, move: str, info) -> str:
        board_fen = info.data.get("board_fen")  
        player_color = info.data.get("player_color")

        if not board_fen:
            raise ValueError(f"❌ Missing board_fen during validation for move {move}")

        board = chess.Board(board_fen)
        legal_moves = [m.uci() for m in board.legal_moves]  # Extract legal moves

        # Debug output
        print(f"\n🔍 Validating move: {move} | Current Board FEN: {board_fen}")
        print(f"♟️ Legal Moves Available: {legal_moves}")

        if move not in legal_moves:
            raise ValueError(f"Illegal move: {move}")

        # ✅ Check if the piece belongs to the correct player
        chess_move = chess.Move.from_uci(move)
        piece = board.piece_at(chess_move.from_square)
        
        if not piece:
            raise ValueError(f"❌ No piece at {chess.square_name(chess_move.from_square)}")

        if (piece.color == chess.WHITE and player_color != "white") or (
            piece.color == chess.BLACK and player_color != "black"
        ):
            raise ValueError(f"❌ Move {move} is not allowed for {player_color}, piece belongs to the opponent!")

        return move
