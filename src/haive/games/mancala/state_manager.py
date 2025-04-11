"""
State manager for the Mancala game.

This module defines the state manager for the Mancala game,
which manages the state of the game and provides methods for initializing,
updating, and analyzing the game state.
"""
from typing import List, Dict, Any, Optional, Union
from src.haive.games.mancala.state import MancalaState
from src.haive.games.mancala.models import MancalaMove
from src.haive.games.framework.base.state_manager import GameStateManager

class MancalaStateManager(GameStateManager[MancalaState]):
    """Manager for Mancala game state.

    This class provides methods for initializing, updating, and analyzing the game state.
    """
    
    @classmethod
    def initialize(cls, **kwargs) -> MancalaState:
        """
        Initialize a new Mancala game.
        
        Args:
            **kwargs: Keyword arguments for game initialization.
                stones_per_pit: Number of stones per pit initially. Defaults to 4.
                
        Returns:
            MancalaState: A new Mancala game state.
        """
        stones_per_pit = kwargs.get('stones_per_pit', 4)
        
        # Create the initial board
        # - Indices 0-5: Player 1's pits
        # - Index 6: Player 1's store
        # - Indices 7-12: Player 2's pits
        # - Index 13: Player 2's store
        board = [stones_per_pit] * 14
        board[6] = 0  # Player 1's store
        board[13] = 0  # Player 2's store
        
        return MancalaState(
            board=board,
            turn="player1",  # Player 1 starts
            game_status="ongoing",
            move_history=[],
            free_turn=False
        )
    
    @classmethod
    def get_legal_moves(cls, state: MancalaState) -> List[MancalaMove]:
        """
        Get all legal moves for the current state.
        
        Args:
            state: The current game state.
            
        Returns:
            List[MancalaMove]: A list of all legal moves.
        """
        legal_moves = []
        player = state.turn
        
        # Determine which pits to check based on the current player
        start_pit = 0 if player == "player1" else 7
        end_pit = 6 if player == "player1" else 13
        
        # Check each pit
        for i in range(start_pit, end_pit):
            # Skip the store
            if i == 6 or i == 13:
                continue
                
            # If the pit has stones, it's a legal move
            if state.board[i] > 0:
                # Calculate the pit index relative to the player (0-5)
                pit_index = i if player == "player1" else i - 7
                legal_moves.append(MancalaMove(pit_index=pit_index, player=player))
        
        return legal_moves
    
    @classmethod
    def apply_move(cls, state: MancalaState, move: MancalaMove) -> MancalaState:
        """
        Apply a move to the current state and return the new state.
        
        Args:
            state: The current game state.
            move: The move to apply.
            
        Returns:
            MancalaState: A new game state after applying the move.
            
        Raises:
            ValueError: If the move is invalid.
        """
        # Validate player's turn
        if move.player != state.turn:
            raise ValueError(f"Not {move.player}'s turn")
        
        # Convert to actual board index
        start_pit = move.pit_index if move.player == "player1" else move.pit_index + 7
        
        # Validate the move
        if state.board[start_pit] == 0:
            raise ValueError(f"Pit {move.pit_index} is empty")
        
        # Create a new state
        new_state = state.model_copy()
        new_state.free_turn = False  # Reset free turn flag
        
        # Get stones from the starting pit
        stones = new_state.board[start_pit]
        new_state.board[start_pit] = 0
        
        # Sow the stones
        current_pit = start_pit
        player_store = 6 if move.player == "player1" else 13
        opponent_store = 13 if move.player == "player1" else 6
        
        while stones > 0:
            current_pit = (current_pit + 1) % 14
            
            # Skip opponent's store
            if current_pit == opponent_store:
                continue
                
            # Add a stone to the current pit
            new_state.board[current_pit] += 1
            stones -= 1
        
        # Check for capture
        last_pit = current_pit
        if last_pit != player_store and new_state.board[last_pit] == 1:
            # The last stone landed in an empty pit on the player's side
            if (move.player == "player1" and 0 <= last_pit < 6) or (move.player == "player2" and 7 <= last_pit < 13):
                opposite_pit = 12 - last_pit
                
                # If the opposite pit has stones, capture them
                if new_state.board[opposite_pit] > 0:
                    # Add the stones from both pits to the player's store
                    new_state.board[player_store] += new_state.board[last_pit] + new_state.board[opposite_pit]
                    new_state.board[last_pit] = 0
                    new_state.board[opposite_pit] = 0
        
        # Check for free turn
        if last_pit == player_store:
            new_state.free_turn = True
        
        # Add move to history
        new_state.move_history.append(move)
        
        # Switch turns if no free turn
        if not new_state.free_turn:
            new_state.turn = "player2" if move.player == "player1" else "player1"
        
        # Check game status
        return cls.check_game_status(new_state)
    
    @classmethod
    def check_game_status(cls, state: MancalaState) -> MancalaState:
        """
        Check and update the game status.
        
        Args:
            state: The current game state.
            
        Returns:
            MancalaState: The game state with updated status.
        """
        # Check if any player's side is empty
        player1_empty = all(state.board[i] == 0 for i in range(6))
        player2_empty = all(state.board[i] == 0 for i in range(7, 13))
        
        if player1_empty or player2_empty:
            # Game is over, collect remaining stones
            if player1_empty:
                # Add player2's stones to their store
                for i in range(7, 13):
                    state.board[13] += state.board[i]
                    state.board[i] = 0
            else:
                # Add player1's stones to their store
                for i in range(6):
                    state.board[6] += state.board[i]
                    state.board[i] = 0
            
            # Determine the winner
            if state.player1_score > state.player2_score:
                state.game_status = "player1_win"
                state.winner = "player1"
            elif state.player2_score > state.player1_score:
                state.game_status = "player2_win"
                state.winner = "player2"
            else:
                state.game_status = "draw"
                state.winner = None
        
        return state
    
    @classmethod
    def get_winner(cls, state: MancalaState) -> Optional[str]:
        """
        Get the winner of the game, if any.
        
        Args:
            state: The current game state.
            
        Returns:
            Optional[str]: The winner, or None if the game is ongoing or a draw.
        """
        if state.game_status == "player1_win":
            return "player1"
        elif state.game_status == "player2_win":
            return "player2"
        return None
    
    @classmethod
    def add_analysis(cls, state: MancalaState, player: str, analysis: Any) -> MancalaState:
        """
        Add an analysis to the state.
        
        Args:
            state: The current game state.
            player: The player who performed the analysis.
            analysis: The analysis to add.
            
        Returns:
            MancalaState: Updated state with the analysis added.
        """
        new_state = state.model_copy()
        
        # Add analysis field if it doesn't exist
        if not hasattr(new_state, f"{player}_analysis"):
            setattr(new_state, f"{player}_analysis", [])
        
        # Add the analysis
        getattr(new_state, f"{player}_analysis").append(analysis)
        
        return new_state