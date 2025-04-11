from typing import List, Optional, Dict, Literal, ClassVar
from pydantic import BaseModel, Field
from src.haive.games.checkers.models import CheckersMove


class CheckersState(BaseModel):
    board: List[List[int]] = Field(default_factory=lambda: CheckersState._default_board(), description="2D grid representation of the board")
    board_string: str = Field(default_factory=lambda: CheckersState._create_board_string(CheckersState._default_board()), description="String representation of the board")
    turn: Literal["red", "black"] = Field(default="red")
    move_history: List[CheckersMove] = Field(default_factory=list)
    game_status: Literal["ongoing", "game_over"] = Field(default="ongoing")
    winner: Optional[Literal["red", "black"]] = None
    red_analysis: List[Dict] = Field(default_factory=list)
    black_analysis: List[Dict] = Field(default_factory=list)
    captured_pieces: Dict[str, List[str]] = Field(default_factory=lambda: {"red": [], "black": []})

    _board_size: ClassVar[int] = 8

    @classmethod
    def _default_board(cls) -> List[List[int]]:
        return [
            [0, 3, 0, 3, 0, 3, 0, 3],
            [3, 0, 3, 0, 3, 0, 3, 0],
            [0, 3, 0, 3, 0, 3, 0, 3],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 1, 0, 1, 0, 1, 0],
            [0, 1, 0, 1, 0, 1, 0, 1],
            [1, 0, 1, 0, 1, 0, 1, 0]
        ]

    @classmethod
    def _create_board_string(cls, board: List[List[int]]) -> str:
        symbols = {0: ".", 1: "r", 2: "R", 3: "b", 4: "B"}
        rows = [
            f"{cls._board_size - i} | " + " ".join(symbols[cell] for cell in row)
            for i, row in enumerate(board)
        ]
        col_labels = "    " + " ".join("abcdefgh")
        return "\n".join(rows) + "\n" + col_labels

    @classmethod
    def initialize(cls) -> "CheckersState":
        board = cls._default_board()
        return cls(
            board=board,
            board_string=cls._create_board_string(board)
        )

    class Config:
        arbitrary_types_allowed = True
