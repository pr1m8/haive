"""
State manager for Reversi (Othello) game logic and mechanics.

Handles legal move validation, disc flipping, game progression,
skipping turns, win detection, and analysis updates.
"""

from typing import List, Dict, Any, Optional, Tuple, Set
from src.haive.games.reversi.state import ReversiState
from src.haive.games.reversi.models import ReversiMove, ReversiAnalysis
from src.haive.games.framework.base.state_manager import GameStateManager

class ReversiStateManager(GameStateManager[ReversiState]):
    """Manager for Reversi/Othello game state."""
    
    # Direction vectors for all 8 directions
    DIRECTIONS = [
        (-1, -1), (-1, 0), (-1, 1),  # NW, N, NE
        (0, -1),           (0, 1),   # W, E
        (1, -1),  (1, 0),  (1, 1)    # SW, S, SE
    ]
    
    @classmethod
    def initialize(cls, **kwargs) -> ReversiState:
        """
        Initialize a new Reversi/Othello game.
        
        Args:
            **kwargs: Keyword arguments for game initialization.
                first_player: Which player goes first ('B' or 'W'). Default is 'B'.
                player_B: Which player is Black ('player1' or 'player2'). Default is 'player1'.
                player_W: Which player is White ('player1' or 'player2'). Default is 'player2'.
                
        Returns:
            ReversiState: A new Reversi game state.
        """
        first_player = kwargs.get('first_player', 'B')
        player_B = kwargs.get('player_B', 'player1')
        player_W = kwargs.get('player_W', 'player2')
        
        # Create an empty 8x8 board
        board = [[None for _ in range(8)] for _ in range(8)]
        
        # Set up initial pieces
        # Standard Reversi setup: 2x2 in the center with alternating colors
        board[3][3] = 'W'
        board[3][4] = 'B'
        board[4][3] = 'B'
        board[4][4] = 'W'
        
        return ReversiState(
            board=board,
            turn=first_player,
            game_status="ongoing",
            move_history=[],
            player_B=player_B,
            player_W=player_W,
            skip_count=0
        )
    
    @classmethod
    def get_legal_moves(cls, state: ReversiState) -> List[ReversiMove]:
        """
        Get all legal moves for the current state.
        
        Args:
            state: The current game state.
            
        Returns:
            List[ReversiMove]: A list of all legal moves.
        """
        legal_moves = []
        player = state.turn
        opponent = 'W' if player == 'B' else 'B'
        
        for row in range(8):
            for col in range(8):
                # Check if the cell is empty
                if state.board[row][col] is not None:
                    continue
                
                # Check if placing a disc here would flip any opponent's discs
                if cls._get_flips(state.board, row, col, player):
                    legal_moves.append(ReversiMove(
                        row=row,
                        col=col,
                        player=player
                    ))
        
        return legal_moves
    
    @classmethod
    def apply_move(cls, state: ReversiState, move: ReversiMove) -> ReversiState:
        """
        Apply a move to the current state and return the new state.
        
        Args:
            state: The current game state.
            move: The move to apply.
            
        Returns:
            ReversiState: A new game state after applying the move.
            
        Raises:
            ValueError: If the move is invalid.
        """
        # Validate player's turn
        if move.player != state.turn:
            raise ValueError(f"Not {move.player}'s turn")
        
        # Get legal moves
        legal_moves = cls.get_legal_moves(state)
        
        # Check if the move is legal
        if not any(m.row == move.row and m.col == move.col for m in legal_moves):
            raise ValueError(f"Illegal move: ({move.row}, {move.col})")
        
        # Create a deep copy of the state
        new_state = state.model_copy(deep=True)
        new_state.skip_count = 0  # Reset skip counter since a move is being made
        
        # Apply the move
        new_state.board[move.row][move.col] = move.player
        
        # Flip opponent's discs
        flips = cls._get_flips(state.board, move.row, move.col, move.player)
        for row, col in flips:
            new_state.board[row][col] = move.player
        
        # Add to move history
        new_state.move_history.append(move)
        
        # Switch turns
        new_state.turn = 'W' if move.player == 'B' else 'B'
        
        # Check if next player has valid moves
        next_player_moves = cls.get_legal_moves(new_state)
        if not next_player_moves:
            # Next player has no valid moves, must skip turn
            new_state.turn = move.player  # Switch back to current player
            new_state.skip_count += 1
            
            # Check if current player also has no moves (game over)
            current_player_moves = cls.get_legal_moves(new_state)
            if not current_player_moves:
                new_state.skip_count += 1  # Both players skipped
        
        # Check game status
        return cls.check_game_status(new_state)
    
    @classmethod
    def check_game_status(cls, state: ReversiState) -> ReversiState:
        """
        Check and update the game status.
        
        Args:
            state: The current game state.
            
        Returns:
            ReversiState: The game state with updated status.
        """
        # If both players have skipped their turns, game is over
        if state.skip_count >= 2:
            # Count discs to determine winner
            counts = state.disc_count
            black_count = counts['B']
            white_count = counts['W']
            
            if black_count > white_count:
                state.game_status = "B_win"
                state.winner = "B"
            elif white_count > black_count:
                state.game_status = "W_win"
                state.winner = "W"
            else:
                state.game_status = "draw"
                state.winner = None
        
        # Check if board is full
        if all(state.board[row][col] is not None for row in range(8) for col in range(8)):
            # Count discs to determine winner
            counts = state.disc_count
            black_count = counts['B']
            white_count = counts['W']
            
            if black_count > white_count:
                state.game_status = "B_win"
                state.winner = "B"
            elif white_count > black_count:
                state.game_status = "W_win"
                state.winner = "W"
            else:
                state.game_status = "draw"
                state.winner = None
        
        return state
    
    @classmethod
    def get_winner(cls, state: ReversiState) -> Optional[str]:
        """
        Get the winner of the game, if any.
        
        Args:
            state: The current game state.
            
        Returns:
            Optional[str]: The winner ('B' or 'W'), or None if the game is ongoing or a draw.
        """
        return state.winner
    
    @classmethod
    def add_analysis(cls, state: ReversiState, player: str, analysis: ReversiAnalysis) -> ReversiState:
        """
        Add an analysis to the state.
        
        Args:
            state: The current game state.
            player: The player who performed the analysis.
            analysis: The analysis to add.
            
        Returns:
            ReversiState: Updated state with the analysis added.
        """
        new_state = state.model_copy()
        
        if player == "player1":
            new_state.player1_analysis.append(analysis)
        else:
            new_state.player2_analysis.append(analysis)
        
        return new_state
    
    @classmethod
    def _get_flips(cls, board: List[List[Optional[str]]], row: int, col: int, player: str) -> Set[Tuple[int, int]]:
        """
        Get the positions of opponent's discs that would be flipped by placing player's disc at (row, col).
        
        Args:
            board: The current board.
            row: Row index of the move.
            col: Column index of the move.
            player: Player making the move ('B' or 'W').
            
        Returns:
            Set[Tuple[int, int]]: Positions of discs that would be flipped.
        """
        # If the cell is not empty, no flips possible
        if board[row][col] is not None:
            return set()
            
        opponent = 'W' if player == 'B' else 'B'
        flips = set()
        
        # Check all 8 directions
        for dx, dy in cls.DIRECTIONS:
            temp_flips = []
            x, y = row + dx, col + dy
            
            # Continue in this direction as long as we find opponent's discs
            while 0 <= x < 8 and 0 <= y < 8 and board[x][y] == opponent:
                temp_flips.append((x, y))
                x += dx
                y += dy
            
            # If we find one of our own discs at the end, these are valid flips
            if 0 <= x < 8 and 0 <= y < 8 and board[x][y] == player and temp_flips:
                flips.update(temp_flips)
        
        return flips
    
    @classmethod
    def is_legal_move(cls, state: ReversiState, row: int, col: int, player: str) -> bool:
        """
        Check if a move is legal.
        
        Args:
            state: The current game state.
            row: Row index of the move.
            col: Column index of the move.
            player: Player making the move ('B' or 'W').
            
        Returns:
            bool: True if the move is legal, False otherwise.
        """
        # Check if the cell is within bounds and empty
        if not (0 <= row < 8 and 0 <= col < 8) or state.board[row][col] is not None:
            return False
        
        # Check if this move would flip any opponent's discs
        return bool(cls._get_flips(state.board, row, col, player))
    
    @classmethod
    def get_skip_move(cls, state: ReversiState) -> ReversiState:
        """
        Apply a skip move when player has no legal moves.
        
        Args:
            state: The current game state.
            
        Returns:
            ReversiState: A new game state after skipping the turn.
        """
        new_state = state.model_copy()
        
        # Increment skip counter
        new_state.skip_count += 1
        
        # Switch turns
        new_state.turn = 'W' if state.turn == 'B' else 'B'
        
        # Check game status
        return cls.check_game_status(new_state)