"""Chess game state models.

This module defines the state schema for chess games, including:
    - Board state representation using FEN notation
    - Move history tracking
    - Game status management
    - Position analysis storage
    - Player turn tracking

The state schema provides a complete representation of a chess game state
that can be used by the agent and state manager.
"""

from typing import Any, Literal

import chess
from haive.core.schema.state_schema import StateSchema
from pydantic import Field, computed_field


class ChessState(StateSchema):
    """State schema for the chess game.

    This class extends StateSchema to provide a comprehensive representation
    of a chess game, including board state, move history, game status, and
    analysis information.

    Attributes:
        board_fens (List[str]): List of FEN board states, with the most recent at the end.
        move_history (List[tuple[str, str]]): List of (player_color, UCI move) tuples.
        current_player (Literal["white", "black"]): Color of the player making the current move.
        turn (Literal["white", "black"]): Current turn color.
        game_status (Literal["ongoing", "check", "checkmate", "stalemate", "draw"]): Current status of the game.
        game_result (Optional[str]): Final game result (white_win, black_win, draw) if game is over.
        white_analysis (List[Dict[str, Any]]): Position analysis from white's perspective.
        black_analysis (List[Dict[str, Any]]): Position analysis from black's perspective.
        captured_pieces (Dict[str, List[str]]): Pieces captured by each player.
        error_message (Optional[str]): Error message if any error occurred.
        legal_moves (Optional[str]): String representation of legal moves in current position.
        recent_moves (Optional[str]): Recent moves formatted for LLM context.

    Examples:
        >>> from haive.games.chess import ChessState
        >>> state = ChessState()
        >>> state.board_fen
        'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
        >>> board = state.get_board()
        >>> board.is_check()
        False
    """

    # Board state
    board_fens: list[str] = Field(
        default_factory=lambda: [chess.Board().fen()],
        description="List of FEN board states, latest at the end",
    )

    # Move tracking
    move_history: list[tuple[str, str]] = Field(
        default_factory=list, description="List of (player_color, UCI move) tuples"
    )

    # Game flow
    current_player: Literal["white", "black"] = Field(
        default="white", description="Current player making a move"
    )

    turn: Literal["white", "black"] = Field(default="white", description="Current turn")

    # Game status
    game_status: Literal["ongoing", "check", "checkmate", "stalemate", "draw"] = Field(
        default="ongoing", description="Status of the game"
    )

    game_result: str | None = Field(
        default=None, description="Final game result (white_win, black_win, draw)"
    )

    # Analysis
    white_analysis: list[dict[str, Any]] = Field(
        default_factory=list, description="White's position analysis"
    )

    black_analysis: list[dict[str, Any]] = Field(
        default_factory=list, description="Black's position analysis"
    )

    # Captured pieces
    captured_pieces: dict[str, list[str]] = Field(
        default_factory=lambda: {"white": [], "black": []},
        description="Captured pieces by each player",
    )

    # Error handling
    error_message: str | None = Field(default=None, description="Error message if any")

    # Additional fields for LLM context
    legal_moves: str | None = Field(
        default=None, description="Legal moves in current position"
    )

    recent_moves: str | None = Field(
        default=None, description="Recent moves formatted for LLM"
    )

    @computed_field
    @property
    def board_fen(self) -> str:
        """Get the current board state as FEN notation.

        Returns:
            str: The FEN representation of the current board position.
        """
        return self.board_fens[-1] if self.board_fens else chess.Board().fen()

    @computed_field
    @property
    def current_board_fen(self) -> str:
        """Alias for board_fen for backwards compatibility.

        Returns:
            str: The FEN representation of the current board position.
        """
        return self.board_fen

    def get_board(self) -> chess.Board:
        """Get a chess.Board object for the current position.

        Creates a Python-chess Board object initialized with the current FEN position.

        Returns:
            chess.Board: Board object representing the current position.

        Raises:
            ValueError: If the FEN string is invalid or cannot be parsed.

        Example:
            >>> state = ChessState()
            >>> board = state.get_board()
            >>> board.is_game_over()
            False
        """
        try:
            return chess.Board(self.board_fen)
        except (ValueError, TypeError) as e:
            raise ValueError(f"Invalid FEN string '{self.board_fen}': {e}") from e
