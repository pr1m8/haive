from typing import List, Dict, Any, Optional, Tuple
import copy

from .models import (
    ShipPlacement,
    MoveCommand,
    MoveOutcome,
    GamePhase,
    ShipType,
    Coordinates,
    MoveResult
)
from .state import BattleshipState, PlayerState

class BattleshipStateManager:
    """
    Manager for Battleship game state transitions.
    
    This class provides methods for:
        - Initializing a new game
        - Placing ships
        - Making moves
        - Checking game status
    """
    
    @staticmethod
    def initialize() -> BattleshipState:
        """
        Initialize a new Battleship game state.
        
        Returns:
            BattleshipState: Fresh game state with default settings
        """
        return BattleshipState(
            player1_state=PlayerState(),
            player2_state=PlayerState(),
            current_player="player1",
            game_phase=GamePhase.SETUP,
            move_history=[],
            error_message=None
        )
    
    @staticmethod
    def place_ships(state: BattleshipState, player: str, placements: List[ShipPlacement]) -> BattleshipState:
        """
        Place ships for a player.

        Args:
            state: Current game state
            player: Player making the placements ("player1" or "player2")
            placements: List of ship placements

        Returns:
            BattleshipState: Updated game state
        """
        # Create a copy of the state
        new_state = copy.deepcopy(state)
        player_state = new_state.get_player_state(player)

        # If the game is already playing or ended, reject further placements
        if new_state.game_phase != GamePhase.SETUP:
            new_state.error_message = f"Cannot place ships once the game has started"
            return new_state

        # Check if player has already placed ships
        if player_state.has_placed_ships:
            new_state.error_message = f"{player} has already placed ships"
            return new_state

        # Validate ship types (each type should appear exactly once)
        ship_types = [p.ship_type for p in placements]
        all_ship_types = list(ShipType)

        if sorted(ship_types) != sorted(all_ship_types):
            missing_types = set(all_ship_types) - set(ship_types)
            if missing_types:
                new_state.error_message = f"Missing ship types: {', '.join(t.value for t in missing_types)}"
            else:
                duplicates = [t for t in ship_types if ship_types.count(t) > 1]
                new_state.error_message = f"Duplicate ship types: {', '.join(t.value for t in set(duplicates))}"
            return new_state

        # Clear existing ships (just in case)
        player_state.board.ships = []

        # Try to place each ship
        for placement in placements:
            if not player_state.board.place_ship(placement):
                new_state.error_message = f"Invalid placement for {placement.ship_type.value}"
                return new_state

        # Record successful placements
        player_state.ship_placements = placements
        player_state.has_placed_ships = True

        # Debug logging
        print(f"[DEBUG] {player} successfully placed ships.")

        # Check if both players have finished setup
        if new_state.is_setup_complete():
            print("[DEBUG] Both players placed ships. Game starting!")
            new_state.game_phase = GamePhase.PLAYING

        return new_state

    @staticmethod
    def make_move(state: BattleshipState, player: str, move: MoveCommand) -> BattleshipState:
        """
        Make a move for a player.
        
        Args:
            state: Current game state
            player: Player making the move ("player1" or "player2")
            move: Attack command
            
        Returns:
            BattleshipState: Updated game state
        """
        # Create a copy of the state
        new_state = copy.deepcopy(state)
        
        # Check if it's the right game phase
        if new_state.game_phase != GamePhase.PLAYING:
            new_state.error_message = f"Cannot make move in {new_state.game_phase.value} phase"
            return new_state
        
        # Check if it's the player's turn
        if new_state.current_player != player:
            new_state.error_message = f"Not {player}'s turn"
            return new_state
        
        # Get player and opponent states
        player_state = new_state.get_player_state(player)
        opponent = new_state.get_opponent(player)
        opponent_state = new_state.get_player_state(opponent)
        
        # Process the attack
        outcome = opponent_state.board.receive_attack(move.row, move.col)
        
        # Update attack tracking for the player
        coord = Coordinates(row=move.row, col=move.col)
        player_state.board.attacks.append(coord)
        
        if outcome.result in [MoveResult.HIT, MoveResult.SUNK]:
            player_state.board.successful_hits.append(coord)
        elif outcome.result == MoveResult.MISS:
            player_state.board.failed_attacks.append(coord)
        
        # Record the move in history
        new_state.move_history.append((player, outcome))
        
        # Check for game over
        if opponent_state.board.all_ships_sunk():
            new_state.game_phase = GamePhase.ENDED
            new_state.winner = player
        else:
            # Switch player
            new_state.current_player = opponent
        
        return new_state
    
    @staticmethod
    def add_analysis(state: BattleshipState, player: str, analysis: str) -> BattleshipState:
        """
        Add strategic analysis for a player.
        
        Args:
            state: Current game state
            player: Player for whom to add analysis
            analysis: Analysis text
            
        Returns:
            BattleshipState: Updated game state
        """
        # Create a copy of the state
        new_state = copy.deepcopy(state)
        player_state = new_state.get_player_state(player)
        
        # Add analysis
        player_state.strategic_analysis.append(analysis)
        
        # Keep only the most recent analyses (limit to 5)
        if len(player_state.strategic_analysis) > 5:
            player_state.strategic_analysis = player_state.strategic_analysis[-5:]
        
        return new_state