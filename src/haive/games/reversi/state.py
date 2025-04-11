"""
Reversi (Othello) game state model.

Defines board layout, current game status, turn tracking, move history,
analysis storage, and rendering utilities for the Reversi agent system.
"""

from typing import List, Optional, Literal, Dict
from pydantic import BaseModel, Field, field_validator
from src.haive.games.framework.base.state import GameState
from src.haive.games.reversi.models import ReversiMove

class ReversiState(GameState):
    """
    State model for a game of Reversi/Othello.

    Attributes:
        board (List[List[Optional[str]]]): 8x8 grid representing the game board.
        turn (str): The current player's turn ('B' or 'W').
        game_status (str): Overall game status (ongoing, draw, B_win, W_win).
        move_history (List[ReversiMove]): History of all moves made.
        winner (Optional[str]): Winner symbol ('B' or 'W'), or None.
        player_B (str): Identifier for the player using black discs.
        player_W (str): Identifier for the player using white discs.
        player1_analysis (List[Dict[str, any]]): Analysis history by player1.
        player2_analysis (List[Dict[str, any]]): Analysis history by player2.
        skip_count (int): Number of consecutive turns skipped (used for endgame).
    """
    board: List[List[Optional[str]]] = Field(
        ..., description="8x8 game board, each cell can be None, 'B', or 'W'"
    )
    turn: Literal["B", "W"] = Field(..., description="Current player's turn (B=Black, W=White)")
    game_status: Literal["ongoing", "B_win", "W_win", "draw"] = Field(
        default="ongoing", description="Status of the game"
    )
    move_history: List[ReversiMove] = Field(
        default_factory=list, description="History of moves"
    )
    winner: Optional[str] = Field(
        default=None, description="Winner of the game, if any"
    )
    player_B: Literal["player1", "player2"] = Field(
        default="player1", description="Which player is Black"
    )
    player_W: Literal["player1", "player2"] = Field(
        default="player2", description="Which player is White"
    )
    player1_analysis: List[Dict[str, any]] = Field(
        default_factory=list, description="Analyses by player1"
    )
    player2_analysis: List[Dict[str, any]] = Field(
        default_factory=list, description="Analyses by player2"
    )
    skip_count: int = Field(
        default=0, description="Number of consecutive skipped turns"
    )

    @field_validator('board')
    def validate_board(cls, board):
        """
        Validate that the board is an 8x8 grid with only valid values.

        Args:
            board (List[List[Optional[str]]]): Input board state.

        Returns:
            List[List[Optional[str]]]: The validated board.

        Raises:
            ValueError: If the board structure or contents are invalid.
        """
        if len(board) != 8:
            raise ValueError("Board must have 8 rows")
        for row in board:
            if len(row) != 8:
                raise ValueError("Each row must have 8 columns")
            for cell in row:
                if cell is not None and cell not in ['B', 'W']:
                    raise ValueError(f"Cell values must be None, 'B', or 'W', got {cell}")
        return board

    @property
    def current_player_name(self) -> str:
        """
        Get the current player's identifier.

        Returns:
            str: Either 'player1' or 'player2'.
        """
        return self.player_B if self.turn == 'B' else self.player_W

    @property
    def disc_count(self) -> Dict[str, int]:
        """
        Count the number of discs of each color on the board.

        Returns:
            Dict[str, int]: Dictionary with counts of 'B' and 'W'.
        """
        black_count = sum(1 for row in self.board for cell in row if cell == 'B')
        white_count = sum(1 for row in self.board for cell in row if cell == 'W')
        return {'B': black_count, 'W': white_count}

    @property
    def board_string(self) -> str:
        """
        Get a human-readable string of the current board layout.

        Returns:
            str: Formatted board as text.
        """
        result = []
        result.append("    1 2 3 4 5 6 7 8")
        result.append("  +-----------------+")
        for i, row in enumerate(self.board):
            row_str = f"{chr(65 + i)} |"
            for cell in row:
                if cell is None:
                    row_str += " |"
                else:
                    row_str += f"{cell}|"
            result.append(row_str)
            result.append("  +-----------------+")
        counts = self.disc_count
        result.append(f"Black: {counts['B']} discs, White: {counts['W']} discs")
        return "\n".join(result)
    
    @classmethod
    def initialize(
        cls,
        first_player: str = 'B',
        player_B: str = 'player1',
        player_W: str = 'player2'
    ) -> "ReversiState":
        """
        Class-level initializer for ReversiState.

        Args:
            first_player (str): 'B' or 'W'. Who plays first.
            player_B (str): Which player controls black.
            player_W (str): Which player controls white.

        Returns:
            ReversiState: Initialized state.
        """
        from src.haive.games.reversi.state_manager import ReversiStateManager
        return ReversiStateManager.initialize(
            first_player=first_player,
            player_B=player_B,
            player_W=player_W
        )
