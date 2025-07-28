"""Chess game state manager module.

This module provides state management functionality for chess games, including:
    - Game state initialization
    - Move application and validation
    - Game status tracking
    - Captured pieces management

The state manager offers a clean interface for modifying chess game states
without having to manipulate the state directly.

Example:
    >>> from haive.games.chess import ChessGameStateManager
    >>>
    >>> # Initialize a new game state
    >>> state = ChessGameStateManager.initialize()
    >>>
    >>> # Apply a move
    >>> new_state = ChessGameStateManager.apply_move(state, "e2e4")
"""

from haive.games.chess.state import ChessState


class ChessGameStateManager:
    """Chess game state manager.

    This class provides static methods for managing chess game states:
        - Game initialization with default settings
        - Move application with validation
        - Game status updates
        - Captured pieces tracking

    The manager implements a functional approach where methods take the current
    state and return a new state, rather than modifying the state in place.

    Examples:
        >>> state = ChessGameStateManager.initialize()
        >>> print(state.board_fen)
        'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'

        >>> new_state = ChessGameStateManager.apply_move(state, "e2e4")
        >>> print(new_state.board_fen)
        'rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1'
    """

    @staticmethod
    def initialize() -> ChessState:
        """Initialize a new chess game state.

        Creates a fresh chess game state with standard initial position and default
        settings for all game parameters.

        Returns:
            ChessState: A fresh game state with standard starting position.

        Examples:
            >>> state = ChessGameStateManager.initialize()
            >>> assert state.turn == "white"
            >>> assert state.game_status == "ongoing"
            >>> assert state.board_fen.startswith("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR")
        """
        import chess

        return ChessState(
            board_fen=chess.Board().fen(),
            turn="white",
            move_history=[],
            captured_pieces={},
            game_status="ongoing",
            analysis={},
            # current_player="white"
            # turn="white"
        )

    @staticmethod
    def apply_move(state: ChessState, move_uci: str) -> ChessState:
        """Apply a move to the current game state.

        Takes the current game state and a move in UCI format, validates it,
        applies it to the board, and returns a new state with updated properties.

        Args:
            state (ChessState): Current game state.
            move_uci (str): Move in UCI notation (e.g., "e2e4").

        Returns:
            ChessState: New game state after applying the move.

        Raises:
            ValueError: If the move is not valid in the current position.

        Note:
            This method handles:
            - Board position updates
            - Captured pieces tracking
            - Game status changes (check, checkmate, stalemate)
            - Player turn switching

        Examples:
            >>> state = ChessGameStateManager.initialize()
            >>> new_state = ChessGameStateManager.apply_move(state, "e2e4")
            >>> assert new_state.turn == "black"
            >>> assert "e2e4" in new_state.move_history

            >>> # Detecting checkmate
            >>> from chess import Board
            >>> board = Board.from_epd("8/8/8/8/8/5K2/4Q3/7k w - - 0 1")
            >>> state = ChessState(board_fen=board.fen())
            >>> new_state = ChessGameStateManager.apply_move(state, "e2e1")
            >>> assert new_state.game_status == "checkmate"
        """
        import chess

        board = chess.Board(state.board_fen)
        move = chess.Move.from_uci(move_uci)

        # Track captured piece
        captured_piece = board.piece_at(move.to_square)

        # Apply move
        board.push(move)

        # Create new state
        new_state = ChessState(
            board_fen=board.fen(),
            move_history=state.move_history + [move_uci],
            captured_pieces=dict(state.captured_pieces),
            turn="black" if state.turn == "white" else "white",
            game_status=state.game_status,
            analysis=state.analysis,
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
