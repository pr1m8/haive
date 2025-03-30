from typing import List, Optional, Tuple
import copy
from src.haive.games.connect4.models import Connect4Move
from src.haive.games.connect4.state import Connect4State
from src.haive.games.framework.base.state_manager import GameStateManager

class Connect4StateManager(GameStateManager[Connect4State]):
    """Manager for Connect 4 game state."""
    
    @classmethod
    def initialize(cls) -> Connect4State:
        """Initialize a new Connect 4 game."""
        board = [[None for _ in range(7)] for _ in range(6)]
        return Connect4State(
            board=board,
            turn="red",
            game_status="ongoing",
            move_history=[]
        )
    
    @classmethod
    def apply_move(cls, state: Connect4State, move: Connect4Move) -> Connect4State:
        """Apply a move to the Connect 4 state."""
        new_state = copy.deepcopy(state)
        board = new_state.board
        column = move.column

        # Validate column
        if not (0 <= column < 7):
            raise ValueError(f"Column {column} is out of range (0-6)")

        # Find next available row
        row = new_state.get_next_row(column)
        if row is None:
            raise ValueError(f"Column {column} is full")

        # Place piece
        board[row][column] = new_state.turn
        new_state.move_history.append(move)

        # Check win condition
        if cls._check_win(new_state, row, column):  # <-- FIXED CALL
            new_state.game_status = f"{new_state.turn}_win"
            new_state.winner = new_state.turn
        elif all(cell is not None for row in board for cell in row):
            new_state.game_status = "draw"
        else:
            new_state.turn = "yellow" if new_state.turn == "red" else "red"

        return new_state
    
    @classmethod
    def get_legal_moves(cls, state: Connect4State) -> List[Connect4Move]:
        """Get all legal moves."""
        return [Connect4Move(column=col) for col in range(7) if not state.is_column_full(col)]
    
    @classmethod
    def check_game_over(cls, state: Connect4State) -> bool:
        """Check if the game is over (win or draw)."""
        return state.game_status in ["red_win", "yellow_win", "draw"]

    @classmethod
    def _check_win(cls, state: Connect4State, row: int, col: int) -> bool:
        """Check if there's a win at (row, col)."""
        player = state.turn
        board = state.board

        # Check horizontal
        for c in range(max(0, col - 3), min(4, col + 1)):
            if all(board[row][c + i] == player for i in range(4)):
                return True

        # Check vertical
        if row <= 2:  # Only check if there are enough rows below
            if all(board[row + i][col] == player for i in range(4)):
                return True

        # Check diagonal /
        for offset in range(-3, 1):
            if 0 <= row + offset <= 2 and 0 <= col + offset <= 3:
                if all(board[row + offset + i][col + offset + i] == player for i in range(4)):
                    return True

        # Check diagonal \
        for offset in range(-3, 1):
            if 0 <= row + offset <= 2 and 3 <= col - offset <= 6:
                if all(board[row + offset + i][col - offset - i] == player for i in range(4)):
                    return True

        return False
