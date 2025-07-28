"""Chess game utility functions.

This module provides helper functions for the chess game, including:
    - Game status determination
    - Board visualization
    - Move validation

These utilities support the core functionality of the chess module
by providing common operations used across different components.
"""

import chess


def determine_game_status(board: chess.Board) -> str:
    """Determine the current game status based on the board position.

    Analyzes a chess board to determine its current status (checkmate,
    stalemate, check, etc.) based on the rules of chess.

    Args:
        board (chess.Board): Chess board to analyze

    Returns:
        str: Game status as one of: "checkmate", "stalemate", "draw",
            "check", or "ongoing"

    Examples:
        >>> board = chess.Board()
        >>> determine_game_status(board)
        'ongoing'

        >>> # Fool's mate position
        >>> board = chess.Board("rnbqkbnr/pppp1ppp/8/4p3/6P1/5P2/PPPPP2P/RNBQKBNR b KQkq - 0 2")
        >>> board.push_san("Qh4#")
        >>> determine_game_status(board)
        'checkmate'
    """
    if board.is_checkmate():
        return "checkmate"
    if board.is_stalemate():
        return "stalemate"
    if board.is_insufficient_material():
        return "draw"
    if board.is_check():
        return "check"
    return "ongoing"


def generate_ascii_board(fen: str, last_move: str | None = None) -> str:
    r"""Generate an ASCII representation of the chess board.

    Creates a text-based visualization of a chess board from its FEN
    representation, optionally highlighting the last move made.

    Args:
        fen (str): FEN string representation of the board
        last_move (str | None, optional): Last move in UCI notation (e.g., "e2e4")
            to highlight on the board. Defaults to None.

    Returns:
        str: ASCII representation of the board with coordinates and
            optional move highlighting

    Examples:
        >>> # Starting position
        >>> board_ascii = generate_ascii_board("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
        >>> print(board_ascii.split("\\n")[0])
        '8 r n b q k b n r'

        >>> # With last move highlighted
        >>> board_ascii = generate_ascii_board(
        ...     "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1",
        ...     "e2e4"
        ... )
    """
    board = chess.Board(fen)

    # Highlight last move if provided
    highlighted_squares = set()
    if last_move:
        try:
            move = chess.Move.from_uci(last_move)
            highlighted_squares.add(move.from_square)
            highlighted_squares.add(move.to_square)
        except ValueError:
            pass

    # Convert the board to ASCII
    board_str = str(board)

    # Add file coordinates at the bottom
    file_coords = "  a b c d e f g h"

    # Add rank coordinates on the left
    lines = board_str.split("\n")
    for i, line in enumerate(lines):
        lines[i] = f"{8-i} {line}"

    # Join the lines and add the file coordinates
    return "\n".join(lines) + "\n" + file_coords


def validate_move(fen: str, move_uci: str) -> tuple[bool, str | None, str | None]:
    """Validate a chess move and return the resulting position.

    Checks if a move is valid in the given position and returns validation
    results including error messages and the resulting position if valid.

    Args:
        fen (str): FEN string of the current position
        move_uci (str): Move in UCI notation (e.g., "e2e4")

    Returns:
        tuple[bool, str | None, str | None]: A tuple containing:
            - is_valid (bool): Whether the move is legal
            - error_message (str | None): Error message if move is invalid, None otherwise
            - resulting_fen (str | None): FEN of the position after the move if valid, None otherwise

    Examples:
        >>> # Valid move
        >>> is_valid, error, new_fen = validate_move(
        ...     "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
        ...     "e2e4"
        ... )
        >>> is_valid
        True
        >>> error is None
        True
        >>> new_fen.startswith("rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR")
        True

        >>> # Invalid move
        >>> is_valid, error, new_fen = validate_move(
        ...     "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
        ...     "e2e5"
        ... )
        >>> is_valid
        False
        >>> "not legal" in error
        True
        >>> new_fen is None
        True
    """
    board = chess.Board(fen)

    try:
        move = chess.Move.from_uci(move_uci)

        if move not in board.legal_moves:
            return False, f"Move {move_uci} is not legal in the current position", None

        board.push(move)
        resulting_fen = board.fen()

        return True, None, resulting_fen

    except ValueError:
        return False, f"Invalid UCI format: {move_uci}", None
