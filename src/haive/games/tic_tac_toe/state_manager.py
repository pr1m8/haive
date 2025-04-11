"""
State manager for Tic Tac Toe game logic and mechanics.

Handles core operations like initializing the board, validating and applying moves,
evaluating win conditions, and updating the state with engine analyses.
"""

from typing import List, Dict, Any, Optional, Tuple
from src.haive.games.tic_tac_toe.state import TicTacToeState
from src.haive.games.tic_tac_toe.models import TicTacToeMove, TicTacToeAnalysis
from src.haive.games.framework.base.state_manager import GameStateManager

class TicTacToeStateManager(GameStateManager[TicTacToeState]):
    """Manager for Tic Tac Toe game state."""
    
    @classmethod
    def initialize(cls, **kwargs) -> TicTacToeState:
        """
        Initialize a new Tic Tac Toe game.
        
        Args:
            **kwargs: Keyword arguments for game initialization.
                first_player: Which player goes first ('X' or 'O'). Default is 'X'.
                player_X: Which player is X ('player1' or 'player2'). Default is 'player1'.
                player_O: Which player is O ('player1' or 'player2'). Default is 'player2'.
                
        Returns:
            TicTacToeState: A new Tic Tac Toe game state.
        """
        first_player = kwargs.get('first_player', 'X')
        player_X = kwargs.get('player_X', 'player1')
        player_O = kwargs.get('player_O', 'player2')
        
        # Create an empty 3x3 board
        board = [[None for _ in range(3)] for _ in range(3)]
        
        return TicTacToeState(
            board=board,
            turn=first_player,
            game_status="ongoing",
            move_history=[],
            player_X=player_X,
            player_O=player_O
        )
    
    @classmethod
    def get_legal_moves(cls, state: TicTacToeState) -> List[TicTacToeMove]:
        """
        Get all legal moves for the current state.
        
        Args:
            state: The current game state.
            
        Returns:
            List[TicTacToeMove]: A list of all legal moves.
        """
        legal_moves = []
        
        # If game is over, no legal moves
        if state.game_status != "ongoing":
            return []
            
        # Check each empty cell
        for row in range(3):
            for col in range(3):
                if state.board[row][col] is None:
                    legal_moves.append(TicTacToeMove(
                        row=row,
                        col=col,
                        player=state.turn
                    ))
        
        return legal_moves
    
    @classmethod
    def apply_move(cls, state: TicTacToeState, move: TicTacToeMove) -> TicTacToeState:
        """
        Apply a move to the current state and return the new state.
        
        Args:
            state: The current game state.
            move: The move to apply.
            
        Returns:
            TicTacToeState: A new game state after applying the move.
            
        Raises:
            ValueError: If the move is invalid.
        """
        # Validate player's turn
        if move.player != state.turn:
            raise ValueError(f"Not {move.player}'s turn")
        
        # Validate move is to an empty cell
        if state.board[move.row][move.col] is not None:
            raise ValueError(f"Cell ({move.row}, {move.col}) is already occupied")
        
        # Create a deep copy of the state
        new_state = state.model_copy(deep=True)
        
        # Apply the move
        new_state.board[move.row][move.col] = move.player
        new_state.move_history.append(move)
        
        # Switch turns
        new_state.turn = 'O' if move.player == 'X' else 'X'
        
        # Check game status
        return cls.check_game_status(new_state)
    
    @classmethod
    def check_game_status(cls, state: TicTacToeState) -> TicTacToeState:
        """
        Check and update the game status.
        
        Args:
            state: The current game state.
            
        Returns:
            TicTacToeState: The game state with updated status.
        """
        # Check rows for a win
        for row in range(3):
            if state.board[row][0] is not None and state.board[row][0] == state.board[row][1] == state.board[row][2]:
                winner = state.board[row][0]
                state.game_status = f"{winner}_win"
                state.winner = winner
                return state
        
        # Check columns for a win
        for col in range(3):
            if state.board[0][col] is not None and state.board[0][col] == state.board[1][col] == state.board[2][col]:
                winner = state.board[0][col]
                state.game_status = f"{winner}_win"
                state.winner = winner
                return state
        
        # Check diagonals for a win
        if state.board[0][0] is not None and state.board[0][0] == state.board[1][1] == state.board[2][2]:
            winner = state.board[0][0]
            state.game_status = f"{winner}_win"
            state.winner = winner
            return state
            
        if state.board[0][2] is not None and state.board[0][2] == state.board[1][1] == state.board[2][0]:
            winner = state.board[0][2]
            state.game_status = f"{winner}_win"
            state.winner = winner
            return state
        
        # Check for a draw
        if state.is_board_full:
            state.game_status = "draw"
            state.winner = None
            return state
        
        # Game is still ongoing
        return state
    
    @classmethod
    def get_winner(cls, state: TicTacToeState) -> Optional[str]:
        """
        Get the winner of the game, if any.
        
        Args:
            state: The current game state.
            
        Returns:
            Optional[str]: The winner ('X' or 'O'), or None if the game is ongoing or a draw.
        """
        return state.winner
    
    @classmethod
    def add_analysis(cls, state: TicTacToeState, player: str, analysis: TicTacToeAnalysis) -> TicTacToeState:
        """
        Add an analysis to the state.
        
        Args:
            state: The current game state.
            player: The player who performed the analysis.
            analysis: The analysis to add.
            
        Returns:
            TicTacToeState: Updated state with the analysis added.
        """
        new_state = state.model_copy()
        
        if player == "player1":
            new_state.player1_analysis.append(analysis)
        else:
            new_state.player2_analysis.append(analysis)
        
        return new_state
    
    @classmethod
    def find_winning_move(cls, state: TicTacToeState, player: str) -> List[Tuple[int, int]]:
        """
        Find a winning move for the specified player, if any.
        
        Args:
            state: The current game state.
            player: The player to find a winning move for ('X' or 'O').
            
        Returns:
            List[Tuple[int, int]]: List of winning move coordinates (row, col), or empty list if none.
        """
        winning_moves = []
        
        # Try each empty cell
        for row, col in state.empty_cells:
            # Create a temporary board with the move
            temp_board = [row[:] for row in state.board]
            temp_board[row][col] = player
            
            # Check if this move would win
            if cls._is_winning_board(temp_board, player):
                winning_moves.append((row, col))
        
        return winning_moves
    
    @classmethod
    def _is_winning_board(cls, board: List[List[Optional[str]]], player: str) -> bool:
        """
        Check if the board is a win for the specified player.
        
        Args:
            board: The board to check.
            player: The player to check for ('X' or 'O').
            
        Returns:
            bool: True if the player has won, False otherwise.
        """
        # Check rows
        for row in range(3):
            if board[row][0] == board[row][1] == board[row][2] == player:
                return True
        
        # Check columns
        for col in range(3):
            if board[0][col] == board[1][col] == board[2][col] == player:
                return True
        
        # Check diagonals
        if board[0][0] == board[1][1] == board[2][2] == player:
            return True
            
        if board[0][2] == board[1][1] == board[2][0] == player:
            return True
        
        return False