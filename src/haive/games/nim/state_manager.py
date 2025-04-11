"""
State manager for the Nim game. 
"""
from typing import List, Dict, Any, Optional, Union
from src.haive.games.nim.state import NimState
from src.haive.games.nim.models import NimMove, NimAnalysis
from src.haive.games.framework.base.state_manager import GameStateManager
from langgraph.types import Command

class NimStateManager(GameStateManager[NimState]):
    """Manager for Nim game state.

    This class provides methods for initializing a new Nim game,
    retrieving legal moves, applying moves, adding analyses,
    and checking game status.
    """
    
    @classmethod
    def initialize(cls, **kwargs) -> NimState:
        """
        Initialize a new Nim game with the given pile sizes.
        
        Args:
            **kwargs: Keyword arguments for game initialization.
                pile_sizes: Optional list of pile sizes. Defaults to [3, 5, 7].
                
        Returns:
            NimState: A new Nim game state.
        """
        pile_sizes = kwargs.get('pile_sizes', [3, 5, 7])
        return NimState(piles=pile_sizes)
    
    @classmethod
    def get_legal_moves(cls, state: NimState) -> List[NimMove]:
        """
        Get all legal moves for the current state.
        
        Args:
            state: The current game state.
            
        Returns:
            List[NimMove]: A list of all legal moves.
        """
        legal_moves = []
        
        for pile_idx, pile_size in enumerate(state.piles):
            if pile_size > 0:
                for stones in range(1, pile_size + 1):
                    legal_moves.append(NimMove(pile_index=pile_idx, stones_taken=stones))
        
        return legal_moves
    
    @classmethod
    def apply_move(cls, state: NimState, move: NimMove) -> NimState:
        """
        Apply a move to the current state and return the new state.
        
        Args:
            state: The current game state.
            move: The move to apply.
            
        Returns:
            NimState: A new game state after applying the move.
            
        Raises:
            ValueError: If the move is invalid.
        """
        # Validate move
        if move.pile_index < 0 or move.pile_index >= len(state.piles):
            raise ValueError(f"Invalid pile index: {move.pile_index}")
        
        if move.stones_taken < 1 or move.stones_taken > state.piles[move.pile_index]:
            raise ValueError(f"Invalid number of stones: {move.stones_taken}")
        
        # Create new state
        new_state = state.model_copy()
        
        # Apply move
        new_state.piles[move.pile_index] -= move.stones_taken
        new_state.move_history.append(move)
        
        # Switch turns
        new_state.turn = "player2" if state.turn == "player1" else "player1"
        
        # Check game status
        return cls.check_game_status(new_state)
    
    @classmethod
    def add_analysis(cls, state: NimState, player: str, analysis: NimAnalysis) -> NimState:
        """
        Add an analysis to the state.
        
        Args:
            state: The current game state.
            player: The player who performed the analysis.
            analysis: The analysis to add.
            
        Returns:
            NimState: Updated state with the analysis added.
        """
        new_state = state.model_copy()
        
        if player == "player1":
            if not hasattr(new_state, "player1_analysis"):
                new_state.player1_analysis = []
            new_state.player1_analysis.append(analysis)
        else:
            if not hasattr(new_state, "player2_analysis"):
                new_state.player2_analysis = []
            new_state.player2_analysis.append(analysis)
        
        return new_state
    
    @classmethod
    def make_move(cls, state: Union[NimState, Dict[str, Any]], player: str, move: NimMove) -> Command:
        """
        Make a move and return a Command with the updated state.
        
        Args:
            state: The current game state.
            player: The player making the move.
            move: The move to make.
            
        Returns:
            Command: Command with the updated state.
            
        Raises:
            ValueError: If it's not the player's turn.
        """
        # Convert dict to NimState if needed
        if isinstance(state, dict):
            state = NimState(**state)
        
        # Validate that it's the correct player's turn
        if state.turn != player:
            raise ValueError(f"Not {player}'s turn")
        
        # Apply the move
        new_state = cls.apply_move(state, move)
        
        # Return as Command for the graph
        return Command(update=new_state.model_dump())
    
    @classmethod
    def get_winner(cls, state: NimState) -> Optional[str]:
        """
        Get the winner of the game, if any.
        
        Args:
            state: The current game state.
            
        Returns:
            Optional[str]: The winner, or None if the game is ongoing.
        """
        if state.game_status == "player1_win":
            return "player1"
        elif state.game_status == "player2_win":
            return "player2"
        return None
    
    @classmethod
    def check_game_status(cls, state: NimState) -> NimState:
        """
        Check and update the game status.
        
        Args:
            state: The current game state.
            
        Returns:
            NimState: The game state with updated status.
        """
        # Create a copy to avoid modifying the original
        new_state = state
        
        # Check for game over
        if sum(new_state.piles) == 0:
            # In standard Nim, the player who takes the last stone wins
            # In misere Nim, the player who takes the last stone loses
            last_player = "player1" if new_state.turn == "player2" else "player2"
            
            if new_state.misere_mode:
                # Last player loses in misere mode
                winner = "player1" if last_player == "player2" else "player2"
            else:
                # Last player wins in standard mode
                winner = last_player
            
            new_state.game_status = f"{winner}_win"
        
        return new_state