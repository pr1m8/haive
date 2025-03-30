import chess
def determine_game_status(board: chess.Board) -> str:
    """Determines the current game status based on the board position."""
    if board.is_checkmate():
        return "checkmate"
    elif board.is_stalemate():
        return "stalemate"
    elif board.is_insufficient_material():
        return "draw"
    elif board.is_check():
        return "check"
    else:
        return "ongoing"
