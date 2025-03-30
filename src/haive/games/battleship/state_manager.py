from src.haive.games.battleship.state import BattleshipGameState
from src.haive.games.battleship.models import Coordinates, Board

class BattleshipGameStateManager:
    """
    Manages state transitions and validation for a Battleship game.
    
    This class provides utility methods for initializing, updating, and
    validating game states, ensuring consistent state transitions.
    """
    
    @staticmethod
    def initialize() -> BattleshipGameState:
        """
        Creates a new game state with initialized boards and player setups.
        
        Returns:
            BattleshipGameState: A fresh game state ready for play
        """
        # Create initial state with default values
        state = BattleshipGameState()
        
        # Initialize player boards
        state.player1_private.board = Board()
        state.player2_private.board = Board()
        
        # Set initial turn
        state.turn = "player1"
        
        # Clear any move history
        state.move_history = []
        
        return state
    
    @staticmethod
    def apply_move(state: BattleshipGameState, player: str, row: int, col: int) -> BattleshipGameState:
        """
        Validates and applies a move, updating the game state accordingly.
        
        Args:
            state: Current game state
            player: Player making the move ("player1" or "player2")
            row: Row coordinate (0-9)
            col: Column coordinate (0-9)
            
        Returns:
            Updated game state after the move
        """
        # Create a copy of the state
        updated_state = state.model_copy()
        
        # Determine opponent
        opponent = "player2" if player == "player1" else "player1"
        
        # Validate it's the player's turn
        if updated_state.turn != player:
            updated_state.error_message = f"Not {player}'s turn."
            return updated_state
        
        # Convert to Coordinates
        coords = Coordinates(row=row, col=col)
        
        # Get player and opponent states
        player_state = getattr(updated_state, f"{player}_private")
        opponent_state = getattr(updated_state, f"{opponent}_private")
        
        # Check if the move has already been made
        if coords.to_tuple() in [g.to_tuple() for g in player_state.board.guesses]:
            updated_state.error_message = f"Invalid move: {coords.to_tuple()} has already been guessed."
            return updated_state
        
        # Apply the move
        result = opponent_state.board.receive_attack(row, col)
        
        # Update player's tracking
        player_state.board.guesses.append(coords)
        
        if result.result == "hit" or result.result == "sunk":
            player_state.board.hits.append(coords)
        elif result.result == "miss":
            player_state.board.misses.append(coords)
        
        # Record the move in history
        updated_state.move_history.append((player, coords.to_tuple(), result.result))
        
        # Check for game end
        if BattleshipGameStateManager.check_game_over(updated_state):
            return updated_state
        
        # Switch turn
        updated_state.turn = opponent
        
        return updated_state
    
    @staticmethod
    def check_game_over(state: BattleshipGameState) -> bool:
        """
        Checks if the game is over and updates game_status and game_result.
        
        Args:
            state: Current game state
            
        Returns:
            True if game is over, False otherwise
        """
        # Check if all ships are sunk for either player
        player1_all_sunk = state.player1_private.board.all_ships_sunk()
        player2_all_sunk = state.player2_private.board.all_ships_sunk()
        
        if player1_all_sunk or player2_all_sunk:
            state.game_status = "ended"
            
            if player1_all_sunk and player2_all_sunk:
                # Both players lost their ships - draw
                state.game_result = "draw"
            elif player1_all_sunk:
                # Player 2 wins
                state.game_result = "player2"
            else:
                # Player 1 wins
                state.game_result = "player1"
                
            return True
            
        return False
    
    @staticmethod
    def check_game_status(state: BattleshipGameState) -> BattleshipGameState:
        """
        Checks and updates the game status, returning the updated state.
        
        Args:
            state: Current game state
            
        Returns:
            Updated game state with correct status
        """
        # Create a copy of the state
        updated_state = state.model_copy()
        
        # Check if game is over
        BattleshipGameStateManager.check_game_over(updated_state)
        
        return updated_state