from typing import Dict, Any, Optional
import time
import random

from langgraph.types import Command
from langgraph.graph import END

from src.haive.core.engine.agent.agent import register_agent
from src.haive.games.framework.base import GameAgent
from src.haive.core.graph.GraphBuilder import DynamicGraph
from src.haive.games.cards.blackjack.config import BlackjackAgentConfig
from src.haive.games.cards.blackjack.state_manager import BlackjackStateManager
from src.haive.games.cards.blackjack.models import (
    BlackjackGameState, 
    PlayerAction, 
    PlayerState
)

@register_agent(BlackjackAgentConfig)
class BlackjackAgent(GameAgent[BlackjackAgentConfig]):
    """Multi-player Blackjack game agent."""
    
    def __init__(self, config: BlackjackAgentConfig=BlackjackAgentConfig()):
        """Initialize the Blackjack agent."""
        self.state_manager = BlackjackStateManager
        super().__init__(config)
        
        # Track game rounds and other metadata
        self.current_round = 0
        self.previous_round_summary = "New game started"
    
    def initialize_game(self, state: Dict[str, Any]) -> Command:
        """
        Initialize a new Blackjack game.
        
        Args:
            state: Initial state dictionary (typically empty)
        
        Returns:
            Command to set up the game
        """
        # Create initial game state
        game_state = self.state_manager.initialize_game(
            num_players=self.config.num_players
        )
        
        # Reset round counter
        self.current_round = 0
        
        return Command(
            update=game_state.model_dump(), 
            goto="betting_phase"
        )
    
    def betting_phase(self, state: Dict[str, Any]) -> Command:
        """
        Manage the betting phase for all players.
        
        Args:
            state: Current game state
        
        Returns:
            Command for next phase
        """
        game_state = BlackjackGameState(**state)
        
        # Use betting engine for each player
        betting_engine = self.engines.get("betting_engine")
        if not betting_engine:
            raise ValueError("Betting engine not configured")
        
        # Process bets for each player
        for i, player in enumerate(game_state.players):
            context = {
                "total_chips": player.total_chips,
                "previous_round_summary": self.previous_round_summary,
                "game_context": f"Round {self.current_round + 1}"
            }
            
            try:
                # Get bet amount from engine
                bet_amount = betting_engine.invoke(context)
                
                # Validate and place bet
                game_state = self.state_manager.place_bet(
                    game_state, 
                    player_index=i, 
                    bet_amount=float(bet_amount)
                )
            except Exception as e:
                # Fallback: random bet between 10-100 or 10% of chips
                fallback_bet = min(
                    max(10, player.total_chips * 0.1), 
                    100
                )
                game_state = self.state_manager.place_bet(
                    game_state, 
                    player_index=i, 
                    bet_amount=fallback_bet
                )
        
        # Move to deal cards
        return Command(
            update=game_state.model_dump(), 
            goto="deal_cards"
        )
    
    def deal_cards(self, state: Dict[str, Any]) -> Command:
        """
        Deal initial cards to all players and dealer.
        
        Args:
            state: Current game state
        
        Returns:
            Command for player turns
        """
        game_state = BlackjackGameState(**state)
        
        # Deal initial cards
        game_state = self.state_manager.deal_initial_cards(game_state)
        
        return Command(
            update=game_state.model_dump(), 
            goto="player_turns"
        )
    
    def player_turns(self, state: Dict[str, Any]) -> Command:
        """
        Manage player turns for decision making.
        
        Args:
            state: Current game state
        
        Returns:
            Command for next phase
        """
        game_state = BlackjackGameState(**state)
        
        # Get current player and hand
        player, current_hand = self.state_manager.get_current_player_and_hand(game_state)
        
        # Prepare context for action decision
        context = {
            "hand_details": " ".join(str(card) for card in current_hand.cards),
            "dealer_card": str(game_state.dealer_hand[0]) if game_state.dealer_hand else "Unknown",
            "current_bet": current_hand.bet,
            "total_chips": player.total_chips
        }
        
        # Use player action engine
        action_engine = self.engines.get("player_action_engine")
        if not action_engine:
            raise ValueError("Player action engine not configured")
        
        try:
            # Get player action
            player_action = action_engine.invoke(context)
        except Exception as e:
            # Fallback action
            player_action = PlayerAction(
                action="hit" if current_hand.total_value() < 17 else "stand",
                reasoning="Default fallback strategy"
            )
        
        # Process the action
        try:
            game_state = self.state_manager.process_player_action(
                game_state, 
                player_action
            )
        except Exception as e:
            # If action is invalid, default to safe action
            fallback_action = PlayerAction(
                action="stand",
                reasoning="Invalid action, defaulting to stand"
            )
            game_state = self.state_manager.process_player_action(
                game_state, 
                fallback_action
            )
        
        # Determine next step based on game status
        if game_state.game_status == "dealer_turn":
            goto = "dealer_turn"
        else:
            goto = "player_turns"
        
        return Command(
            update=game_state.model_dump(), 
            goto=goto
        )
    
    def dealer_turn(self, state: Dict[str, Any]) -> Command:
        """
        Execute dealer's turn.
        
        Args:
            state: Current game state
        
        Returns:
            Command for game conclusion
        """
        game_state = BlackjackGameState(**state)
        
        # Dealer takes their turn
        game_state = self.state_manager.dealer_turn(game_state)
        
        # Increment round counter
        self.current_round += 1
        
        # Update previous round summary
        self.previous_round_summary = (
            f"Round {self.current_round}: "
            f"Dealer hand: {' '.join(str(card) for card in game_state.dealer_hand)}"
        )
        
        # Determine next step
        if self.current_round >= self.config.max_rounds:
            return Command(
                update=game_state.model_dump(), 
                goto=END
            )
        else:
            # Reset for next round
            game_state = self.state_manager.reset_game(game_state)
            
            return Command(
                update=game_state.model_dump(), 
                goto="betting_phase"
            )
    
    def visualize_state(self, state: Dict[str, Any]) -> None:
        """
        Visualize the current game state.
        
        Args:
            state: Current game state
        """
        game_state = BlackjackGameState(**state)
        
        print("\n" + "=" * 50)
        print(f"🎲 Round {self.current_round + 1}")
        print(f"📊 Game Status: {game_state.game_status}")
        print("=" * 50)
        
        # Show dealer's hand
        print("\n🃏 Dealer's Hand:")
        dealer_cards = [str(card) for card in game_state.dealer_hand]
        print(", ".join(dealer_cards))
        print(f"Total: {sum(card.point_value() for card in game_state.dealer_hand)}")
        
        # Show each player's state
        for i, player in enumerate(game_state.players):
            print(f"\n💰 Player {i+1} (Chips: ${player.total_chips:.2f}):")
            for j, hand in enumerate(player.hands):
                hand_cards = [str(card) for card in hand.cards]
                print(f"  Hand {j+1}: {', '.join(hand_cards)}")
                print(f"  Total: {hand.total_value()}")
                print(f"  Bet: ${hand.bet:.2f}")
                print(f"  Status: {'Active' if hand.is_active else 'Inactive'}")
        
        time.sleep(1)  # Add a small delay for readability
    
    def setup_workflow(self) -> None:
        """
        Set up the workflow for the Blackjack game.
        """
        gb = DynamicGraph(
            components=[self.config], 
            state_schema=self.config.state_schema
        )
        
        # Define nodes for the game workflow
        gb.add_node("initialize", self.initialize_game)
        gb.add_node("betting_phase", self.betting_phase)
        gb.add_node("deal_cards", self.deal_cards)
        gb.add_node("player_turns", self.player_turns)
        gb.add_node("dealer_turn", self.dealer_turn)
        
        # Define edges
        gb.add_edge("initialize", "betting_phase")
        gb.add_edge("betting_phase", "deal_cards")
        gb.add_edge("deal_cards", "player_turns")
        
        # Build the graph
        self.graph = gb.build()