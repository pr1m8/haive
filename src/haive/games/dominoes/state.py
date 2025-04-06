from src.haive.games.dominoes.models import DominoTile, DominoMove, DominoesAnalysis
from src.haive.games.framework.base.state import GameState
from typing import List, Dict, Optional, Union, Literal
from pydantic import Field      

class DominoesState(GameState):
    """State for a dominoes game."""
    players: List[str] = Field(..., description="List of player names")
    hands: Dict[str, List[DominoTile]] = Field(..., description="Tiles in each player's hand")
    board: List[DominoTile] = Field(default_factory=list, description="Tiles on the board")
    boneyard: List[DominoTile] = Field(default_factory=list, description="Tiles in the boneyard (draw pile)")
    turn: str = Field(..., description="Current player's turn")
    game_status: Literal["ongoing", "player1_win", "player2_win", "draw"] = Field(
        default="ongoing", description="Status of the game"
    )
    move_history: List[Union[DominoMove, Literal["pass"]]] = Field(
        default_factory=list, description="History of moves"
    )
    last_passes: int = Field(default=0, description="Number of consecutive passes")
    scores: Dict[str, int] = Field(default_factory=dict, description="Scores for each player")
    winner: Optional[str] = Field(default=None, description="Winner of the game, if any")
    player1_analysis: List[DominoesAnalysis] = Field(
        default_factory=list, description="Analyses by player1"
    )
    player2_analysis: List[DominoesAnalysis] = Field(
        default_factory=list, description="Analyses by player2"
    )
    
    @property
    def left_value(self) -> Optional[int]:
        """Get the value on the left end of the board."""
        if not self.board:
            return None
        return self.board[0].left
    
    @property
    def right_value(self) -> Optional[int]:
        """Get the value on the right end of the board."""
        if not self.board:
            return None
        return self.board[-1].right
    
    @property
    def board_string(self) -> str:
        """Get a string representation of the board."""
        if not self.board:
            return "Empty board"
        
        board_str = ""
        for i, tile in enumerate(self.board):
            if i > 0:
                # Add a connecting character between tiles
                board_str += "-"
            board_str += str(tile)
        
        return board_str