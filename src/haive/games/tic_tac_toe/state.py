"""
Tic Tac Toe game models, including core state definition for gameplay and logic.

This module defines the `TicTacToeState` class used to represent the board, track players, and capture gameplay data such as history and analysis. 
It includes helper properties to assess the board and enforce its structure.
"""

from typing import List, Optional, Literal, Dict, Tuple
from pydantic import BaseModel, Field, field_validator
from ..framework.base.state import GameState
from ..tic_tac_toe.models import TicTacToeMove
from ..tic_tac_toe.models import TicTacToeAnalysis
class TicTacToeState(GameState):
    """
    Represents the full game state of a Tic Tac Toe match.

    Attributes:
        board (List[List[Optional[str]]]): A 3x3 grid containing 'X', 'O', or None.
        turn (Literal['X', 'O']): Current player's symbol.
        game_status (Literal['ongoing', 'X_win', 'O_win', 'draw']): Status of the game.
        move_history (List[TicTacToeMove]): List of moves made during the game.
        winner (Optional[str]): 'X' or 'O' if someone won, else None.
        player_X (Literal['player1', 'player2']): Which player controls X.
        player_O (Literal['player1', 'player2']): Which player controls O.
        player1_analysis (List[Dict[str, any]]): Analysis performed by player1.
        player2_analysis (List[Dict[str, any]]): Analysis performed by player2.
    """

    board: List[List[Optional[str]]] = Field(
        ..., description="3x3 game board, each cell can be None, 'X', or 'O'"
    )
    turn: Literal["X", "O"] = Field(..., description="Current player's turn")
    game_status: Literal["ongoing", "X_win", "O_win", "draw"] = Field(
        default="ongoing", description="Status of the game"
    )
    move_history: List[TicTacToeMove] = Field(
        default_factory=list, description="History of moves"
    )
    winner: Optional[str] = Field(
        default=None, description="Winner of the game, if any"
    )
    player_X: Literal["player1", "player2"] = Field(
        default="player1", description="Which player is X"
    )
    player_O: Literal["player1", "player2"] = Field(
        default="player2", description="Which player is O"
    )
    player1_analysis: List[TicTacToeAnalysis] = Field(
        default_factory=list, description="Analyses by player1"
    )
    player2_analysis: List[TicTacToeAnalysis] = Field(
        default_factory=list, description="Analyses by player2"
    )

    @field_validator('board')
    def validate_board(cls, board):
        """
        Validate that the board is a 3x3 grid with valid symbols ('X', 'O', or None).

        Args:
            board (List[List[Optional[str]]]): The board to validate.

        Raises:
            ValueError: If the board does not meet shape or value constraints.

        Returns:
            List[List[Optional[str]]]: Validated board.
        """
        if len(board) != 3:
            raise ValueError("Board must have 3 rows")
        for row in board:
            if len(row) != 3:
                raise ValueError("Each row must have 3 columns")
            for cell in row:
                if cell is not None and cell not in ['X', 'O']:
                    raise ValueError(f"Cell values must be None, 'X', or 'O', got {cell}")
        return board

    @property
    def empty_cells(self) -> List[Tuple[int, int]]:
        """Return a list of coordinates for all empty cells on the board."""
        return [(i, j) for i in range(3) for j in range(3) if self.board[i][j] is None]

    @property
    def is_board_full(self) -> bool:
        """Check whether the board is completely filled."""
        return all(self.board[i][j] is not None for i in range(3) for j in range(3))

    @property
    def current_player_name(self) -> str:
        """
        Get the name of the current player (player1 or player2).

        Returns:
            str: The identifier for the player whose turn it is.
        """
        return self.player_X if self.turn == 'X' else self.player_O

    @property
    def board_string(self) -> str:
        """
        Get a pretty-printed string representation of the board.

        Returns:
            str: Multiline string representing the current board state.
        """
        result = []
        result.append("   0 1 2")
        result.append("  -------")
        for i, row in enumerate(self.board):
            row_str = f"{i} |"
            for cell in row:
                if cell is None:
                    row_str += " |"
                else:
                    row_str += f"{cell}|"
            result.append(row_str)
            result.append("  -------")
        return "\n".join(result)
    @classmethod
    def initialize(cls, **kwargs):
        """
        Initialize a new Tic Tac Toe game.
        """
        first_player = kwargs.get('first_player', 'X')
        player_X = kwargs.get('player_X', 'player1')
        player_O = kwargs.get('player_O', 'player2')

        board = [[None for _ in range(3)] for _ in range(3)]

        return cls(
            board=board,
            turn=first_player,
            game_status="ongoing",
            move_history=[],
            player_X=player_X,
            player_O=player_O,
            player1_analysis=[],
            player2_analysis=[],
        )
