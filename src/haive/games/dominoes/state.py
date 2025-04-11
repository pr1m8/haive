from src.haive.games.dominoes.models import DominoTile, DominoMove, DominoesAnalysis
from src.haive.games.framework.base.state import GameState
from typing import List, Dict, Optional, Union, Literal
from pydantic import Field      
import random
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
    
    @classmethod
    def initialize(cls, player_names: List[str] = ["player1", "player2"], tiles_per_hand: int = 7):
        """Initialize a new dominoes game."""
        # Create all tiles from 0-0 to 6-6
        all_tiles = []
        for i in range(7):
            for j in range(i + 1):
                all_tiles.append(DominoTile(left=i, right=j))
        
        # Shuffle the tiles
        random.shuffle(all_tiles)
        
        # Deal tiles to players
        hands = {}
        for player in player_names:
            hands[player] = all_tiles[:tiles_per_hand]
            all_tiles = all_tiles[tiles_per_hand:]
        
        # Rest of tiles go to the boneyard
        boneyard = all_tiles
        
        # Determine who goes first
        # Traditional rule: player with highest double goes first
        first_player = player_names[0]  # Default
        highest_double = -1
        
        for player in player_names:
            for tile in hands[player]:
                if tile.is_double() and tile.left > highest_double:
                    highest_double = tile.left
                    first_player = player
        
        # If no doubles, player with highest tile goes first
        if highest_double == -1:
            highest_sum = -1
            for player in player_names:
                for tile in hands[player]:
                    tile_sum = tile.sum()
                    if tile_sum > highest_sum:
                        highest_sum = tile_sum
                        first_player = player
        
        # Create the initial state
        return DominoesState(
            players=player_names,
            hands=hands,
            board=[],
            boneyard=boneyard,
            turn=first_player,
            game_status="ongoing",
            move_history=[],
            last_passes=0,
            scores={player: 0 for player in player_names}
        )