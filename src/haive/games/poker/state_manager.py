import logging
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime

from src.haive.games.poker.models import (
    Card, Suit, CardValue, PlayerAction, GamePhase, 
    Player, Hand, Pot, PokerGameState, PlayerObservation
)
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.haive.games.poker.config import PokerAgentConfig

from src.haive.games.poker.state import PokerState
#from src.haive.games.poker.config import PokerAgentConfig
logger = logging.getLogger(__name__)

class PokerStateManager:
    """
    Manager for Texas Hold'em Poker game state.
    
    This class provides methods for:
    - Game initialization and lifecycle management
    - Card dealing and deck management
    - Betting and pot management
    - Hand evaluation and winner determination
    - Player action validation and application
    - State observation
    """
    
    def __init__(self, debug: bool = False):
        """Initialize the poker state manager"""
        self.state = PokerState()
        self.debug = debug
        self.history = []
        
    def initialize_game(self, config: 'PokerAgentConfig'):
        """Initialize a new poker game with the given players"""
        # Initialize state
        self.state.initialize_game(config.player_names, config.starting_chips)
        
        # Set blinds
        self.state.game.small_blind = config.small_blind
        self.state.game.big_blind = config.big_blind
        
        # Log initialization
        self._log_event(f"Game initialized with {len(config.player_names)} players")
        self._log_event(f"Small blind: ${config.small_blind}, Big blind: ${config.big_blind}")
        
        return self.state
    
    def start_new_hand(self):
        """Start a new hand - deal cards, post blinds, etc."""
        # Start a new hand in the state
        self.state.start_new_hand()
        
        # Save initial hand state to history
        self._save_state_snapshot("hand_start")
        
        # Return current player ID
        current_player = self.state.game.players[self.state.game.current_player_idx]
        return current_player.id
    
    def get_player_observation(self, player_id: str) -> PlayerObservation:
        """Get the game state from a specific player's perspective"""
        return self.state.create_player_observation(player_id)
    
    def handle_player_action(self, player_id: str, action: PlayerAction, amount: int = 0) -> Tuple[bool, str]:
        """
        Process a player's action
        
        Args:
            player_id: ID of the player making the action
            action: The action to take (fold, check, call, bet, raise, all-in)
            amount: The bet/raise amount (if applicable)
            
        Returns:
            Tuple of (success, message)
        """
        from src.haive.games.poker.models import AgentDecision
        
        # Create decision object
        decision = AgentDecision(
            action=action,
            amount=amount,
            reasoning=""
        )
        
        # Validate player's turn
        current_player = self.state.game.players[self.state.game.current_player_idx]
        if current_player.id != player_id:
            return False, f"Not {player_id}'s turn"
        
        try:
            # Handle the action in the state
            self.state.handle_player_action(player_id, decision)
            
            # Save state snapshot after action
            self._save_state_snapshot(f"action_{action.value}")
            
            # Return current player ID and success
            if len(self.state.game.active_players) <= 1:
                # Game is over - only one player left
                return True, "hand_complete"
            
            if self.state.game.round_complete:
                # Betting round is complete
                self.state.advance_game_phase()
                
                # Check if hand is complete
                if self.state.game.phase == GamePhase.SHOWDOWN or self.state.game.phase == GamePhase.GAME_OVER:
                    return True, "hand_complete"
                
                # Save state snapshot after phase change
                self._save_state_snapshot(f"phase_{self.state.game.phase.value}")
            
            # Get next player
            next_player = self.state.game.players[self.state.game.current_player_idx]
            return True, next_player.id
            
        except Exception as e:
            logger.error(f"Error handling player action: {str(e)}")
            return False, str(e)
    
    def advance_phase(self) -> Tuple[bool, str]:
        """
        Advance to the next game phase
        
        Returns:
            Tuple of (success, message)
        """
        try:
            # Advance phase in state
            self.state.advance_game_phase()
            
            # Save state snapshot
            self._save_state_snapshot(f"phase_{self.state.game.phase.value}")
            
            # Check if hand is complete
            if self.state.game.phase == GamePhase.SHOWDOWN or self.state.game.phase == GamePhase.GAME_OVER:
                return True, "hand_complete"
            
            # Return next player
            next_player = self.state.game.players[self.state.game.current_player_idx]
            return True, next_player.id
            
        except Exception as e:
            logger.error(f"Error advancing phase: {str(e)}")
            return False, str(e)
    
    def complete_hand(self) -> Dict[str, Any]:
        """
        Complete the current hand (showdown or single winner)
        
        Returns:
            Hand result information
        """
        # If not already in game over phase, handle showdown
        if self.state.game.phase != GamePhase.GAME_OVER:
            self.state.game.phase = GamePhase.SHOWDOWN
            self.state._handle_showdown()
        
        # Save final state
        self._save_state_snapshot("hand_complete")
        
        # Return hand results
        return {
            "winners": self.state.game.winners,
            "winning_hands": {
                player_id: self.state.game.hand_rankings.get(player_id, None)
                for player_id in self.state.game.winners
            },
            "community_cards": [str(card) for card in self.state.game.community_cards],
            "pot_sizes": [pot.amount for pot in self.state.game.pots],
            "player_chips": {
                player.id: player.chips for player in self.state.game.players
            }
        }
    
    def get_game_summary(self) -> Dict[str, Any]:
        """Get a summary of the current game state"""
        return {
            "phase": self.state.game.phase.value,
            "active_players": len(self.state.game.active_players),
            "community_cards": [str(card) for card in self.state.game.community_cards],
            "pot_sizes": [pot.amount for pot in self.state.game.pots],
            "current_bet": self.state.game.current_bet,
            "players": [
                {
                    "id": player.id,
                    "name": player.name,
                    "chips": player.chips,
                    "is_active": player.is_active,
                    "is_all_in": player.is_all_in,
                    "current_bet": player.current_bet,
                    "total_bet": player.total_bet,
                    "position": player.position
                }
                for player in self.state.game.players
            ],
            "dealer_position": self.state.game.dealer_position,
            "current_player_idx": self.state.game.current_player_idx,
            "small_blind": self.state.game.small_blind,
            "big_blind": self.state.game.big_blind,
            "min_raise": self.state.game.min_raise
        }
    
    def get_legal_actions(self, player_id: str) -> List[Dict[str, Any]]:
        """Get all legal actions for a player"""
        player = next((p for p in self.state.game.players if p.id == player_id), None)
        if not player:
            logger.warning(f"Player {player_id} not found")
            return []
        
        if not player.is_active or player.is_all_in:
            return []
            
        legal_actions = []
        
        # Fold is always legal
        legal_actions.append({
            "action": PlayerAction.FOLD.value,
            "amount": 0
        })
        
        # Check is legal if no bet to call
        call_amount = self.state.game.current_bet - player.current_bet
        if call_amount <= 0:
            legal_actions.append({
                "action": PlayerAction.CHECK.value,
                "amount": 0
            })
        
        # Call is legal if there's a bet to call and player has chips
        if call_amount > 0 and player.chips >= call_amount:
            legal_actions.append({
                "action": PlayerAction.CALL.value,
                "amount": call_amount
            })
        
        # Bet is legal if no current bet and player has chips
        if self.state.game.current_bet == 0 and player.chips > 0:
            # Minimum bet is big blind
            min_bet = min(self.state.game.big_blind, player.chips)
            legal_actions.append({
                "action": PlayerAction.BET.value,
                "amount": min_bet,
                "min": min_bet,
                "max": player.chips
            })
        
        # Raise is legal if there's a bet and player has enough chips
        if self.state.game.current_bet > 0 and player.chips > call_amount:
            min_raise_to = self.state.game.current_bet + self.state.game.min_raise
            min_raise = min(min_raise_to, player.chips)
            legal_actions.append({
                "action": PlayerAction.RAISE.value,
                "amount": min_raise,
                "min": min_raise,
                "max": player.chips
            })
        
        # All-in is always legal if player has chips
        if player.chips > 0:
            legal_actions.append({
                "action": PlayerAction.ALL_IN.value,
                "amount": player.chips
            })
        
        return legal_actions
    
    def _save_state_snapshot(self, action_type: str):
        """Save a snapshot of the current state"""
        timestamp = datetime.now().strftime("%H:%M:%S.%f")
        
        snapshot = {
            "timestamp": timestamp,
            "action_type": action_type,
            "phase": self.state.game.phase.value,
            "players": [
                {
                    "id": p.id,
                    "name": p.name,
                    "chips": p.chips,
                    "hand": str(p.hand) if p.hand else "None",
                    "is_active": p.is_active,
                    "current_bet": p.current_bet
                }
                for p in self.state.game.players
            ],
            "community_cards": [str(card) for card in self.state.game.community_cards],
            "pots": [pot.amount for pot in self.state.game.pots],
            "current_player": self.state.game.current_player_idx,
            "current_bet": self.state.game.current_bet
        }
        
        self.history.append(snapshot)
        
        if self.debug:
            logger.debug(f"State snapshot: {action_type}")
            logger.debug(f"Phase: {self.state.game.phase.value}")
            logger.debug(f"Community cards: {[str(c) for c in self.state.game.community_cards]}")
            logger.debug(f"Pot sizes: {[pot.amount for pot in self.state.game.pots]}")
            logger.debug(f"Current bet: {self.state.game.current_bet}")
    
    def _log_event(self, message: str):
        """Log an event to the state game log and logger"""
        self.state.log_event(message)
        if self.debug:
            logger.info(message)
    
    def export_history(self) -> List[Dict[str, Any]]:
        """Export the full game history"""
        return self.history
    
    def reset(self):
        """Reset the state manager"""
        self.state = PokerState()
        self.history = []
    def is_game_over(self):
        """Check if the game is over based on phase"""
        return self.state.game.phase == GamePhase.GAME_OVER