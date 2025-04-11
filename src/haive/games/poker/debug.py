"""Debugging utilities for the poker agent.

This module provides tools for debugging, testing and analyzing the poker agent's
performance, including:
- Test harnesses for structured output validation
- Decision validation and verification
- Error analysis and reporting
- Game state visualization
"""

import json
import logging
import time
from typing import Dict, List, Any, Optional, Union, Tuple
import traceback
from datetime import datetime

from src.haive.games.poker.models import (
    PlayerAction, GamePhase, Player, Card, AgentDecision, 
    PlayerObservation, GameResult, AgentDecisionSchema, Suit, CardValue
)

logger = logging.getLogger(__name__)

class StructuredOutputTester:
    """Test harness for validating LLM structured output handling."""
    
    def __init__(self, llm_runnable, input_values: Dict[str, Any]):
        """Initialize the tester with an LLM runnable and test inputs."""
        self.llm = llm_runnable
        self.input_values = input_values
        self.results = []
    
    def run_test(self, retries: int = 3) -> Dict[str, Any]:
        """Run a single test of the LLM runnable with retries."""
        errors = []
        start_time = time.time()
        
        for attempt in range(retries):
            try:
                # Invoke the LLM
                response = self.llm.invoke(self.input_values)
                end_time = time.time()
                
                # Check response type
                result = {
                    "attempt": attempt + 1,
                    "duration": end_time - start_time,
                    "success": False,
                    "response_type": str(type(response)),
                    "raw_response": response
                }
                
                # Check if it's a structured output
                if isinstance(response, AgentDecisionSchema):
                    result["success"] = True
                    result["structured"] = True
                    result["action"] = response.action
                    result["amount"] = response.amount
                    result["has_reasoning"] = bool(response.reasoning)
                elif isinstance(response, dict) and "action" in response:
                    result["success"] = True
                    result["structured"] = False
                    result["action"] = response.get("action")
                    result["amount"] = response.get("amount", 0)
                    result["has_reasoning"] = bool(response.get("reasoning", ""))
                else:
                    result["success"] = False
                    result["error"] = "Unexpected response format"
                    errors.append(f"Unexpected response format: {type(response)}")
                
                # If successful, no need for more retries
                if result["success"]:
                    break
                    
            except Exception as e:
                end_time = time.time()
                errors.append(str(e))
                result = {
                    "attempt": attempt + 1,
                    "duration": end_time - start_time,
                    "success": False,
                    "error": str(e),
                    "traceback": traceback.format_exc()
                }
            
            # Wait before retrying
            if attempt < retries - 1:
                time.sleep(1)
        
        # Store the result
        self.results.append(result)
        
        return result
    
    def run_batch_test(self, iterations: int = 10) -> Dict[str, Any]:
        """Run multiple tests and collect statistics."""
        for i in range(iterations):
            logger.info(f"Running test iteration {i+1}/{iterations}")
            self.run_test()
        
        # Compile statistics
        successes = sum(1 for r in self.results if r["success"])
        structured_outputs = sum(1 for r in self.results if r.get("structured", False))
        avg_duration = sum(r["duration"] for r in self.results) / len(self.results)
        
        action_counts = {}
        for r in self.results:
            if r["success"]:
                action = r.get("action")
                if action:
                    action_counts[action] = action_counts.get(action, 0) + 1
        
        stats = {
            "total_tests": len(self.results),
            "success_rate": successes / len(self.results) if self.results else 0,
            "structured_rate": structured_outputs / len(self.results) if self.results else 0,
            "avg_duration": avg_duration,
            "action_distribution": action_counts
        }
        
        return stats
    
    def print_report(self):
        """Print a detailed report of the test results."""
        if not self.results:
            print("No test results available.")
            return
        
        stats = self.run_batch_test(iterations=0)  # Just compile stats without running more tests
        
        print("="*60)
        print("STRUCTURED OUTPUT TEST REPORT")
        print("="*60)
        print(f"Total tests: {stats['total_tests']}")
        print(f"Success rate: {stats['success_rate']*100:.2f}%")
        print(f"Structured output rate: {stats['structured_rate']*100:.2f}%")
        print(f"Average duration: {stats['avg_duration']:.2f}s")
        print("\nAction distribution:")
        for action, count in stats['action_distribution'].items():
            print(f"  {action}: {count} ({count/stats['total_tests']*100:.2f}%)")
        
        print("\nDetailed results:")
        for i, result in enumerate(self.results):
            print(f"\nTest #{i+1}:")
            print(f"  Success: {result['success']}")
            if result['success']:
                print(f"  Structured: {result.get('structured', False)}")
                print(f"  Action: {result.get('action')}")
                print(f"  Amount: {result.get('amount')}")
                print(f"  Has reasoning: {result.get('has_reasoning', False)}")
            else:
                print(f"  Error: {result.get('error', 'Unknown error')}")
            print(f"  Duration: {result['duration']:.2f}s")


class GameStatePrinter:
    """Utility for visualizing poker game state during debugging."""
    
    @staticmethod
    def print_game_state(state):
        """Print a human-readable version of the current game state."""
        game = state.game
        
        print("\n" + "="*80)
        print(f"GAME STATE: {game.phase.value.upper()}")
        print("="*80)
        
        # Print community cards
        print("\nCommunity Cards:")
        if game.community_cards:
            for card in game.community_cards:
                print(f"  {GameStatePrinter._format_card(card)}", end=" ")
            print()
        else:
            print("  None")
        
        # Print pot information
        print("\nPot:")
        total_pot = sum(pot.amount for pot in game.pots)
        print(f"  Total: ${total_pot}")
        if len(game.pots) > 1:
            for i, pot in enumerate(game.pots):
                pot_name = "Main Pot" if i == 0 else f"Side Pot {i}"
                print(f"  {pot_name}: ${pot.amount}")
        
        # Print current bet
        print(f"  Current Bet: ${game.current_bet}")
        print(f"  Min Raise: ${game.min_raise}")
        
        # Print players
        print("\nPlayers:")
        current_player_idx = game.current_player_idx
        dealer_position = game.dealer_position
        
        for i, player in enumerate(game.players):
            # Position indicators
            position_indicator = ""
            if player.position == dealer_position:
                position_indicator += "D "
            if i == current_player_idx:
                position_indicator += "* "
                
            # Status
            status = "Active"
            if not player.is_active:
                status = "Folded"
            elif player.is_all_in:
                status = "All-In"
                
            # Print player info
            print(f"  {position_indicator}{player.name}: ${player.chips} ({status})")
            
            # Print player's current bet
            if player.current_bet > 0:
                print(f"    Current Bet: ${player.current_bet}")
                
            # Print player's hand if active
            if player.is_active and player.hand and player.hand.cards:
                print(f"    Hand: ", end="")
                for card in player.hand.cards:
                    print(f"{GameStatePrinter._format_card(card)}", end=" ")
                print()
        
        # Print recent actions
        print("\nRecent Actions:")
        if not game.action_history:
            print("  None")
        else:
            # Get the last 5 actions
            recent_actions = game.action_history[-min(5, len(game.action_history)):]
            for action in recent_actions:
                player_name = next((p.name for p in game.players if p.id == action.player_id), action.player_id)
                action_str = action.action.value.upper()
                amount_str = f" ${action.amount}" if action.amount > 0 else ""
                print(f"  {player_name}: {action_str}{amount_str}")
                
        print("\n" + "-"*80)
    
    @staticmethod
    def _format_card(card: Card) -> str:
        """Format a card for display."""
        # Map card values to string representations
        value_map = {
            CardValue.TWO: "2",
            CardValue.THREE: "3",
            CardValue.FOUR: "4",
            CardValue.FIVE: "5",
            CardValue.SIX: "6",
            CardValue.SEVEN: "7",
            CardValue.EIGHT: "8",
            CardValue.NINE: "9",
            CardValue.TEN: "10",
            CardValue.JACK: "J",
            CardValue.QUEEN: "Q",
            CardValue.KING: "K",
            CardValue.ACE: "A"
        }
        
        # Map suits to unicode symbols
        suit_map = {
            Suit.HEARTS: "♥",
            Suit.DIAMONDS: "♦",
            Suit.CLUBS: "♣",
            Suit.SPADES: "♠"
        }
        
        value_str = value_map.get(card.value, str(card.value.value))
        suit_str = suit_map.get(card.suit, card.suit.value[0].upper())
        
        return f"{value_str}{suit_str}"


class DecisionAnalyzer:
    """Analyze and validate player decisions for correctness."""
    
    @staticmethod
    def validate_decision(decision: AgentDecision, player: Player, game_state) -> Dict[str, Any]:
        """Validate if a decision is legal and reasonable."""
        # Start with a clean validation result
        validation = {
            "legal": True,
            "optimal": True,
            "warnings": [],
            "suggestions": [],
            "reasoning_quality": "good"
        }
        
        # Check if action is a valid enum value
        if not isinstance(decision.action, PlayerAction):
            try:
                # Try to convert string to enum
                action = PlayerAction(decision.action.lower())
                validation["warnings"].append(f"Decision action was a string '{decision.action}', not an enum")
                decision.action = action
            except (ValueError, AttributeError):
                validation["legal"] = False
                validation["warnings"].append(f"Invalid action: {decision.action}")
                return validation
        
        # Check if amount is a valid number
        if not isinstance(decision.amount, (int, float)):
            validation["warnings"].append(f"Amount is not a number: {decision.amount}")
            try:
                decision.amount = int(decision.amount)
            except (ValueError, TypeError):
                validation["legal"] = False
                validation["warnings"].append("Invalid amount: cannot be converted to a number")
                return validation
        
        # Ensure amount is non-negative
        if decision.amount < 0:
            validation["legal"] = False
            validation["warnings"].append(f"Negative amount: {decision.amount}")
            return validation
        
        # Check action-specific legality
        current_bet = game_state.current_bet
        player_bet = player.current_bet
        
        # CHECK validation
        if decision.action == PlayerAction.CHECK:
            if current_bet > player_bet:
                validation["legal"] = False
                validation["warnings"].append(f"Cannot check when there's a bet to call (${current_bet - player_bet})")
            if decision.amount != 0:
                validation["warnings"].append(f"Check should have amount 0, not {decision.amount}")
                decision.amount = 0
        
        # CALL validation
        elif decision.action == PlayerAction.CALL:
            call_amount = current_bet - player_bet
            if call_amount <= 0:
                validation["legal"] = False
                validation["warnings"].append("Cannot call when there's no bet to call")
            elif decision.amount != call_amount:
                validation["warnings"].append(f"Call amount should be {call_amount}, not {decision.amount}")
            if player.chips < call_amount:
                validation["legal"] = False
                validation["warnings"].append(f"Not enough chips to call (need {call_amount}, have {player.chips})")
        
        # BET validation
        elif decision.action == PlayerAction.BET:
            if current_bet > 0:
                validation["legal"] = False
                validation["warnings"].append("Cannot bet when there's already a bet")
            elif decision.amount > player.chips:
                validation["legal"] = False
                validation["warnings"].append(f"Bet amount ({decision.amount}) exceeds available chips ({player.chips})")
            elif decision.amount < game_state.big_blind:
                validation["warnings"].append(f"Bet less than big blind (${decision.amount} < ${game_state.big_blind})")
                validation["suggestions"].append(f"Minimum bet should be at least the big blind (${game_state.big_blind})")
        
        # RAISE validation
        elif decision.action == PlayerAction.RAISE:
            if current_bet == 0:
                validation["legal"] = False
                validation["warnings"].append("Cannot raise when there's no bet (use BET instead)")
            else:
                min_raise = current_bet + game_state.min_raise - player_bet
                if decision.amount < min_raise:
                    validation["warnings"].append(f"Raise amount less than minimum ({decision.amount} < {min_raise})")
                    validation["suggestions"].append(f"Minimum raise should be {min_raise}")
                if decision.amount > player.chips:
                    validation["legal"] = False
                    validation["warnings"].append(f"Raise amount exceeds available chips ({decision.amount} > {player.chips})")
        
        # ALL_IN validation
        elif decision.action == PlayerAction.ALL_IN:
            if player.chips == 0:
                validation["legal"] = False
                validation["warnings"].append("Player already all-in")
            elif decision.amount != player.chips:
                validation["warnings"].append(f"All-in amount should be {player.chips}, not {decision.amount}")
                decision.amount = player.chips
        
        # Check reasoning quality
        if not decision.reasoning:
            validation["reasoning_quality"] = "missing"
            validation["warnings"].append("No reasoning provided")
        elif len(decision.reasoning) < 20:
            validation["reasoning_quality"] = "poor"
            validation["warnings"].append("Reasoning is too brief")
        
        return validation