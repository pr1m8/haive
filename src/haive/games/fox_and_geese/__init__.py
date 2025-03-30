from typing import List, Dict, Literal, Optional, Tuple, Union, Set
from pydantic import BaseModel, Field
from src.haive.games.framework.base import GameState, GameStateManager
import copy

class FoxAndGeesePosition(BaseModel):
    """Position on the Fox and Geese board."""
    row: int = Field(..., ge=0, lt=7, description="Row (0-6)")
    col: int = Field(..., ge=0, lt=7, description="Column (0-6)")
    
    def __str__(self):
        return f"({self.row}, {self.col})"
    
    def __eq__(self, other):
        if not isinstance(other, FoxAndGeesePosition):
            return False
        return self.row == other.row and self.col == other.col
    
    def __hash__(self):
        return hash((self.row, self.col))

class FoxAndGeeseMove(BaseModel):
    """Represents a move in Fox and Geese."""
    from_pos: FoxAndGeesePosition = Field(..., description="Starting position")
    to_pos: FoxAndGeesePosition = Field(..., description="Ending position")
    piece_type: Literal["fox", "goose"] = Field(..., description="Type of piece moved")
    capture: Optional[FoxAndGeesePosition] = Field(default=None, description="Position of captured goose, if any")
    
    def __str__(self):
        if self.capture:
            return f"{self.piece_type.capitalize()} moves from {self.from_pos} to {self.to_pos}, capturing at {self.capture}"
        return f"{self.piece_type.capitalize()} moves from {self.from_pos} to {self.to_pos}"



class FoxAndGeeseStateManager(GameStateManager[FoxAndGeeseState]):
    """Manager for Fox and Geese game state."""
    
    @classmethod
    def initialize(cls) -> FoxAndGeeseState:
        """Initialize a new Fox and Geese game."""
        # Fox starts at the center
        fox_position = FoxAndGeesePosition(row=3, col=3)
        
        # Geese start at the top
        geese_positions = set()
        for col in range(7):
            if col % 2 == 0:  # Only on white squares
                geese_positions.add(FoxAndGeesePosition(row=0, col=col))
                geese_positions.add(FoxAndGeesePosition(row=1, col=col))
        
        return FoxAndGeeseState(
            fox_position=fox_position,
            geese_positions=geese_positions,
            turn="fox",  # Fox goes first
            game_status="ongoing",
            move_history=[],
            num_geese=len(geese_positions)
        )
    
    @classmethod
    def apply_move(cls, state: FoxAndGeeseState, move: FoxAndGeeseMove) -> FoxAndGeeseState:
        """Apply a move to the Fox and Geese state."""
        # Create a deep copy of the state
        new_state = copy.deepcopy(state)
        
        # Update the position based on piece type
        if move.piece_type == "fox":
            new_state.fox_position = move.to_pos
            
            # Handle capture if present
            if move.capture:
                new_state.geese_positions.remove(move.capture)
                new_state.num_geese -= 1
        else:  # Goose
            new_state.geese_positions.remove(move.from_pos)
            new_state.geese_positions.add(move.to_pos)
        
        # Add to move history
        new_state.move_history.append(move)
        
        # Switch turns
        new_state.turn = "geese" if state.turn == "fox" else "fox"
        
        # Check for game over
        new_state = cls.check_game_status(new_state)
        
        return new_state
    
    @classmethod
    def get_legal_moves(cls, state: FoxAndGeeseState) -> List[FoxAndGeeseMove]:
        """Get all legal moves for the current state."""
        moves = []
        
        if state.turn == "fox":
            # Fox can move diagonally in any direction
            moves = cls._get_fox_moves(state)
        else:
            # Geese can only move diagonally forward
            moves = cls._get_geese_moves(state)
        
        return moves
    
    @classmethod
    def _get_fox_moves(cls, state: FoxAndGeeseState) -> List[FoxAndGeeseMove]:
        """Get all legal moves for the fox."""
        moves = []
        row, col = state.fox_position.row, state.fox_position.col
        
        # Diagonal directions
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        
        for dr, dc in directions:
            # Regular move
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < 7 and 0 <= new_col < 7:
                # Check if position is empty
                new_pos = FoxAndGeesePosition(row=new_row, col=new_col)
                if new_pos not in state.geese_positions:
                    moves.append(FoxAndGeeseMove(
                        from_pos=state.fox_position,
                        to_pos=new_pos,
                        piece_type="fox"
                    ))
            
            # Capture move - jump over a goose
            capture_row, capture_col = row + dr, col + dc
            land_row, land_col = row + 2*dr, col + 2*dc
            
            if (0 <= capture_row < 7 and 0 <= capture_col < 7 and
                0 <= land_row < 7 and 0 <= land_col < 7):
                
                capture_pos = FoxAndGeesePosition(row=capture_row, col=capture_col)
                land_pos = FoxAndGeesePosition(row=land_row, col=land_col)
                
                # Check if there's a goose to capture and landing spot is empty
                if (capture_pos in state.geese_positions and
                    land_pos not in state.geese_positions):
                    
                    moves.append(FoxAndGeeseMove(
                        from_pos=state.fox_position,
                        to_pos=land_pos,
                        piece_type="fox",
                        capture=capture_pos
                    ))
        
        return moves
    
    @classmethod
    def _get_geese_moves(cls, state: FoxAndGeeseState) -> List[FoxAndGeeseMove]:
        """Get all legal moves for the geese."""
        moves = []
        
        # Geese can only move diagonally forward (downward)
        directions = [(1, -1), (1, 1)]
        
        for goose in state.geese_positions:
            row, col = goose.row, goose.col
            
            for dr, dc in directions:
                new_row, new_col = row + dr, col + dc
                
                if 0 <= new_row < 7 and 0 <= new_col < 7:
                    # Check if position is empty
                    new_pos = FoxAndGeesePosition(row=new_row, col=new_col)
                    if new_pos not in state.geese_positions and new_pos != state.fox_position:
                        moves.append(FoxAndGeeseMove(
                            from_pos=goose,
                            to_pos=new_pos,
                            piece_type="goose"
                        ))
        
        return moves
    
    @classmethod
    def check_game_status(cls, state: FoxAndGeeseState) -> FoxAndGeeseState:
        """Check and update game status."""
        # Fox wins if it captures too many geese
        if state.num_geese < 4:  # Assuming fox wins if fewer than 4 geese remain
            state.game_status = "fox_win"
            state.winner = "fox"
        
        # Geese win if they trap the fox (fox has no legal moves)
        elif state.turn == "fox" and not cls._get_fox_moves(state):
            state.game_status = "geese_win"
            state.winner = "geese"
        
        return state