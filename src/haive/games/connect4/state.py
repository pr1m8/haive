
# src/haive/agents/agent_games/connect4/state.py

from typing import List, Optional, Dict, Literal
from pydantic import Field, field_validator
from src.haive.games.framework.base.state import GameState
from src.haive.games.connect4.models import Connect4Move

class Connect4State(GameState):
    """State for a Connect 4 game."""
    board: List[List[Optional[str]]] = Field(
        ..., description="6x7 board representation (rows x columns)"
    )
    turn: Literal["red", "yellow"] = Field(..., description="Current player's turn")
    game_status: Literal["ongoing", "red_win", "yellow_win", "draw"] = Field(
        default="ongoing", description="Status of the game"
    )
    move_history: List[Connect4Move] = Field(
        default_factory=list, description="History of moves"
    )
    red_analysis: List[Dict] = Field(
        default_factory=list, description="Analysis history for red player"
    )
    yellow_analysis: List[Dict] = Field(
        default_factory=list, description="Analysis history for yellow player"
    )
    winner: Optional[str] = Field(
        default=None, description="Winner of the game, if any"
    )
    
    @property
    def board_string(self) -> str:
        """Get a string representation of the board."""
        result = []
        
        # Column headers
        result.append("  0 1 2 3 4 5 6")
        result.append("  -------------")
        
        # Board rows (reversed to show bottom at the bottom)
        for i, row in enumerate(self.board):
            row_str = f"{i}|"
            for cell in row:
                if cell is None:
                    row_str += " |"
                elif cell == "red":
                    row_str += "R|"
                else:  # yellow
                    row_str += "Y|"
            result.append(row_str)
        
        result.append("  -------------")
        result.append("  0 1 2 3 4 5 6")
        
        return "\n".join(result)
    
    def is_column_full(self, column: int) -> bool:
        """Check if a column is full."""
        return self.board[0][column] is not None
    
    def get_next_row(self, column: int) -> Optional[int]:
        """Get the next available row in a column."""
        for row in range(len(self.board) - 1, -1, -1):
            if self.board[row][column] is None:
                return row
        return None
    
    @field_validator('board')
    def validate_board_dimensions(cls, board):
        """Validate board dimensions are 6x7."""
        if len(board) != 6:
            raise ValueError("Board must have 6 rows")
        if any(len(row) != 7 for row in board):
            raise ValueError("Each row must have 7 columns")
        return board
    
    @classmethod
    def initialize(cls):
        """Initialize a new Connect 4 game."""
        board = [[None for _ in range(7)] for _ in range(6)]
        return cls(
            board=board,
            turn="red",
            game_status="ongoing",
            move_history=[]
        )