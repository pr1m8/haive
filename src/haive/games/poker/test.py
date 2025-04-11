#!/usr/bin/env python3
"""
Test script for the Poker agent.

This script tests various components and functionality of the Poker agent
to identify and fix any issues.
"""

import os
import sys
import logging
import time
import traceback
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent))

from haive.games.poker.config import PokerAgentConfig
from haive.games.poker.agent import PokerAgent
from haive.games.poker.state import PokerState
from haive.games.poker.state_manager import PokerStateManager
from haive.games.poker.models import (
    Card, Player, PokerGameState as Game, PlayerAction, GamePhase, 
    Pot, Suit, CardValue, AgentDecision
)
from haive.games.poker.debug import StructuredOutputTester, GameStatePrinter
from haive.core.engine.aug_llm import AugLLMConfig
from haive.games.poker.engines import poker_agent_configs

# Set up logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("poker_test.log", mode="w")
    ]
)

logger = logging.getLogger(__name__)

class PokerAgentTester:
    """Test suite for the Poker agent."""
    
    def __init__(self, use_default_engines=True):
        """Initialize the tester."""
        self.use_default_engines = use_default_engines
        self.successful_tests = 0
        self.failed_tests = 0
        self.issues_found = []
        
        # Create agent with test configuration
        logger.info("Initializing Poker agent tester")
        
        self.agent = self._create_agent()
        self.state_manager = PokerStateManager(debug=True)
    
    def _create_agent(self):
        """Create a Poker agent with test configuration."""
        # Use default agent types or create custom ones
        if self.use_default_engines:
            engines = poker_agent_configs
        else:
            # Create custom LLM configs for different agent types
            conservative_agent = AugLLMConfig(
                model="gpt-4o",
                temperature=0.3,
                request_timeout=60
            )
            
            aggressive_agent = AugLLMConfig(
                model="gpt-4o",
                temperature=0.7,
                request_timeout=60
            )
            
            hand_analyzer = AugLLMConfig(
                model="gpt-4o",
                temperature=0.2,
                request_timeout=60
            )
            
            engines = {
                "conservative_agent": conservative_agent,
                "aggressive_agent": aggressive_agent,
                "hand_analyzer": hand_analyzer
            }
        
        # Create agent config with 2 players
        config = PokerAgentConfig(
            name="poker_test_agent",
            player_names=["Player 1", "Player 2"],
            starting_chips=1000,
            small_blind=10,
            big_blind=20,
            enable_detailed_analysis=True,
            engines=engines
        )
        
        # Create agent
        return PokerAgent(config=config)
    
    def _create_test_state(self):
        """Create a test state for a poker game."""
        # Initialize the game through state manager
        self.state_manager.initialize_game(self.agent.config)
        self.state_manager.start_new_hand()
        
        # Get the state and modify as needed for tests
        state = self.state_manager.state
        
        # Modify state for testing if needed
        # For example, set specific cards or betting amounts
        
        return state
    
    def _create_advanced_test_state(self):
        """Create a more complex test state with predetermined cards."""
        # Initialize basic state
        state = self._create_test_state()
        game = state.game
        
        # Set specific player cards for testing
        player0_cards = [
            Card(value=CardValue.ACE, suit=Suit.SPADES),
            Card(value=CardValue.ACE, suit=Suit.HEARTS)
        ]
        
        player1_cards = [
            Card(value=CardValue.KING, suit=Suit.DIAMONDS),
            Card(value=CardValue.KING, suit=Suit.CLUBS)
        ]
        
        game.players[0].cards = player0_cards
        game.players[1].cards = player1_cards
        
        # Set community cards (flop)
        game.community_cards = [
            Card(value=CardValue.TEN, suit=Suit.HEARTS),
            Card(value=CardValue.JACK, suit=Suit.HEARTS),
            Card(value=CardValue.QUEEN, suit=Suit.HEARTS)
        ]
        
        # Update game phase
        game.phase = GamePhase.FLOP
        
        # Set betting state
        game.pot_size = 40  # Initial blinds
        game.current_bet = 0
        
        # Update state
        state.game = game
        
        return state
    
    def test_initialize_game(self):
        """Test the initialize_game method."""
        logger.info("Testing initialize_game...")
        
        try:
            start_time = time.time()
            result = self.agent.initialize_game(PokerState())
            duration = time.time() - start_time
            
            # Check results
            if not isinstance(result, PokerState):
                raise ValueError(f"Expected PokerState, got {type(result)}")
            
            if not result.game or not result.game.players:
                raise ValueError("Game not properly initialized")
            
            if len(result.game.players) != 2:
                raise ValueError(f"Expected 2 players, got {len(result.game.players)}")
            
            # Log success
            logger.info(f"Game initialization successful in {duration:.2f}s")
            self.successful_tests += 1
            return True
            
        except Exception as e:
            logger.error(f"Game initialization test failed: {e}")
            logger.error(traceback.format_exc())
            self.failed_tests += 1
            self.issues_found.append({
                "test": "initialize_game",
                "error": str(e),
                "traceback": traceback.format_exc()
            })
            return False
    
    def test_setup_hand(self):
        """Test the setup_hand method."""
        logger.info("Testing setup_hand...")
        
        try:
            # Initialize the game first
            initial_state = self.agent.initialize_game(PokerState())
            
            start_time = time.time()
            result = self.agent.setup_hand(initial_state)
            duration = time.time() - start_time
            
            # Check results
            if not isinstance(result, PokerState):
                raise ValueError(f"Expected PokerState, got {type(result)}")
            
            game = result.game
            
            # Check that cards were dealt
            if not all(len(player.cards) == 2 for player in game.players):
                raise ValueError("Players don't have 2 cards each")
            
            # Check that blinds were posted
            if game.pot_size == 0:
                raise ValueError("Blinds were not posted")
            
            # Check that we're in the correct phase
            if game.phase != GamePhase.PRE_FLOP:
                raise ValueError(f"Expected PRE_FLOP phase, got {game.phase}")
            
            # Log success
            logger.info(f"Hand setup successful in {duration:.2f}s")
            self.successful_tests += 1
            return True
            
        except Exception as e:
            logger.error(f"Hand setup test failed: {e}")
            logger.error(traceback.format_exc())
            self.failed_tests += 1
            self.issues_found.append({
                "test": "setup_hand",
                "error": str(e),
                "traceback": traceback.format_exc()
            })
            return False
    
    def test_player_decision(self):
        """Test the handle_player_decision method."""
        logger.info("Testing player_decision...")
        
        try:
            # Get a state with a hand in progress
            state = self._create_test_state()
            
            start_time = time.time()
            result = self.agent.handle_player_decision(state)
            duration = time.time() - start_time
            
            # Check results
            if not isinstance(result, PokerState):
                raise ValueError(f"Expected PokerState, got {type(result)}")
            
            # Check if a decision was made
            game = result.game
            last_action = None
            
            for player in game.players:
                if player.last_action:
                    last_action = player.last_action
                    break
            
            if not last_action:
                raise ValueError("No player decision made")
            
            # Log success
            logger.info(f"Player decision successful in {duration:.2f}s")
            logger.info(f"Decision: {last_action}")
            self.successful_tests += 1
            return True
            
        except Exception as e:
            logger.error(f"Player decision test failed: {e}")
            logger.error(traceback.format_exc())
            self.failed_tests += 1
            self.issues_found.append({
                "test": "player_decision",
                "error": str(e),
                "traceback": traceback.format_exc()
            })
            return False
    
    def test_update_game_phase(self):
        """Test the update_game_phase method."""
        logger.info("Testing update_game_phase...")
        
        try:
            # Create a state where all players have acted
            state = self._create_test_state()
            
            # Manually complete the betting round
            for player in state.game.players:
                player.has_acted = True
                player.last_action = PlayerAction.CALL
            
            start_time = time.time()
            result = self.agent.update_game_phase(state)
            duration = time.time() - start_time
            
            # Check results
            if not isinstance(result, PokerState):
                raise ValueError(f"Expected PokerState, got {type(result)}")
            
            # Check that the phase was updated
            if result.game.phase == GamePhase.PRE_FLOP:
                # Should have advanced to FLOP
                raise ValueError(f"Game phase not updated from {state.game.phase}")
            
            # If phase is FLOP, check that community cards were dealt
            if result.game.phase == GamePhase.FLOP and len(result.game.community_cards) != 3:
                raise ValueError(f"Expected 3 community cards for FLOP, got {len(result.game.community_cards)}")
            
            # Log success
            logger.info(f"Game phase update successful in {duration:.2f}s")
            logger.info(f"New phase: {result.game.phase}")
            self.successful_tests += 1
            return True
            
        except Exception as e:
            logger.error(f"Game phase update test failed: {e}")
            logger.error(traceback.format_exc())
            self.failed_tests += 1
            self.issues_found.append({
                "test": "update_game_phase",
                "error": str(e),
                "traceback": traceback.format_exc()
            })
            return False
    
    def test_structured_output(self):
        """Test the structured output handling with the debug tools."""
        logger.info("Testing structured output handling...")
        
        try:
            # Get a player agent from the agent's configuration
            player_id = "player_0"
            if player_id not in self.agent.player_agents:
                raise ValueError(f"Player agent {player_id} not found")
            
            player_agent = self.agent.player_agents[player_id]
            runnable = player_agent['runnable']
            
            # Create a state for testing
            state = self._create_advanced_test_state()
            
            # Create a test context similar to what the agent would use
            test_context = {
                "player_cards": "Ace of Spades, Ace of Hearts",
                "community_cards": "Ten of Hearts, Jack of Hearts, Queen of Hearts",
                "position": "Button",
                "pot_size": 40,
                "current_bet": 0,
                "player_chips": 1000,
                "opponent_chips": 980,
                "legal_actions": [
                    {"action": "CHECK", "amount": 0},
                    {"action": "BET", "min_amount": 20, "max_amount": 1000}
                ]
            }
            
            # Use the StructuredOutputTester
            tester = StructuredOutputTester(runnable, test_context)
            result = tester.run_test()
            
            # Check results
            if not result.get("success", False):
                raise ValueError(f"Structured output test failed: {result.get('error', 'Unknown error')}")
            
            # Print report
            tester.print_report()
            
            # Log success
            logger.info("Structured output test successful")
            self.successful_tests += 1
            return True
            
        except Exception as e:
            logger.error(f"Structured output test failed: {e}")
            logger.error(traceback.format_exc())
            self.failed_tests += 1
            self.issues_found.append({
                "test": "structured_output",
                "error": str(e),
                "traceback": traceback.format_exc()
            })
            return False
    
    def test_hand_evaluation(self):
        """Test the end_hand method for correct hand evaluation."""
        logger.info("Testing hand evaluation...")
        
        try:
            # Create a state at showdown
            state = self._create_advanced_test_state()
            
            # Set up for showdown
            state.game.phase = GamePhase.SHOWDOWN
            for player in state.game.players:
                player.has_folded = False
            
            # Run the end_hand method
            start_time = time.time()
            result = self.agent.end_hand(state)
            duration = time.time() - start_time
            
            # Check results
            if not isinstance(result, PokerState):
                raise ValueError(f"Expected PokerState, got {type(result)}")
            
            # Check that a winner was determined
            if not any(player.is_winner for player in result.game.players):
                raise ValueError("No winner determined")
            
            # Log success
            logger.info(f"Hand evaluation successful in {duration:.2f}s")
            for player in result.game.players:
                if player.is_winner:
                    logger.info(f"Winner: Player {player.id} with {player.hand_rank}")
            
            self.successful_tests += 1
            return True
            
        except Exception as e:
            logger.error(f"Hand evaluation test failed: {e}")
            logger.error(traceback.format_exc())
            self.failed_tests += 1
            self.issues_found.append({
                "test": "hand_evaluation",
                "error": str(e),
                "traceback": traceback.format_exc()
            })
            return False
    
    def run_all_tests(self):
        """Run all tests and report results."""
        logger.info("Running all Poker agent tests...")
        
        start_time = time.time()
        
        self.test_initialize_game()
        self.test_setup_hand()
        self.test_player_decision()
        self.test_update_game_phase()
        self.test_structured_output()
        self.test_hand_evaluation()
        
        duration = time.time() - start_time
        
        # Report results
        print("\n" + "="*50)
        print("POKER AGENT TEST RESULTS")
        print("="*50)
        print(f"Tests completed in {duration:.2f}s")
        print(f"Successful tests: {self.successful_tests}")
        print(f"Failed tests: {self.failed_tests}")
        
        if self.issues_found:
            print("\nIssues found:")
            for issue in self.issues_found:
                print(f"\n- Test: {issue['test']}")
                print(f"  Error: {issue['error']}")
        
        print("="*50)
        
        return self.successful_tests, self.failed_tests, self.issues_found

def main():
    """Run the Poker agent tests."""
    print("Starting Poker agent tests...")
    
    # Run with default engine configurations
    tester = PokerAgentTester(use_default_engines=True)
    tester.run_all_tests()

if __name__ == "__main__":
    main()
