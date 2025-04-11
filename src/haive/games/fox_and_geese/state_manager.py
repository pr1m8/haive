"""
State manager for the Fox and Geese game.

This module defines the state manager for the Fox and Geese game,
which manages the state of the game and provides methods for initializing,
applying moves, checking game status, and getting legal moves for the Fox and Geese game.
"""
import copy
from typing import List
from src.haive.games.fox_and_geese.models import FoxAndGeesePosition, FoxAndGeeseMove
from src.haive.games.fox_and_geese.state import FoxAndGeeseState
from src.haive.games.framework.base.state_manager import GameStateManager


class FoxAndGeeseStateManager(GameStateManager[FoxAndGeeseState]):
    """Manager for Fox and Geese game state.

    This class provides methods for initializing, applying moves,
    checking game status, and getting legal moves for the Fox and Geese game.
    """
    
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
        """Apply a move to the Fox and Geese state.

        This method updates the state of the game based on the move made by the current player.
        It handles both regular moves and capture moves, updating the position of the fox and geese
        accordingly. It also updates the move history and switches turns between fox and geese.
        """
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
        """Get all legal moves for the current state.

        This method returns a list of all legal moves for the current player in the given game state.
        It checks the current player's turn and calls the appropriate method to get the legal moves
        for the fox or geese.
        """
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
        """Get all legal moves for the fox.

        This method returns a list of all legal moves for the fox in the given game state.
        It checks all possible diagonal directions from the fox's current position and
        creates moves for each valid direction.
        """
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
        """Get all legal moves for the geese.

        This method returns a list of all legal moves for the geese in the given game state.
        It checks all possible diagonal directions from the geese's current position and
        creates moves for each valid direction.
        """
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
        """Check and update game status.

        This method checks the current game status and updates the state accordingly.
        It determines if the fox has won by capturing too many geese or if the geese
        have won by trapping the fox. It also updates the game status and winner.
        """
        # Fox wins if it captures too many geese
        if state.num_geese < 4:  # Assuming fox wins if fewer than 4 geese remain
            state.game_status = "fox_win"
            state.winner = "fox"
        
        # Geese win if they trap the fox (fox has no legal moves)
        elif state.turn == "fox" and not cls._get_fox_moves(state):
            state.game_status = "geese_win"
            state.winner = "geese"
        
        return state