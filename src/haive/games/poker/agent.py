"""Enhanced Texas Hold'em Poker agent implementation.

This module implements a robust poker agent with improved:
- Structured output handling with proper schema validation
- Comprehensive logging and debugging
- Error handling and retry policies for invalid moves
- Enhanced prompts for LLM decisions
"""
import os
import logging
import uuid
import time
import traceback
from typing import Dict, List, Any, Optional, Union, Tuple
from datetime import datetime

from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langgraph.graph import END, StateGraph, START

from src.haive.core.engine.agent.agent import Agent, register_agent
from src.haive.core.engine.aug_llm import AugLLMConfig, compose_runnable
from src.haive.games.poker.models import (
    PlayerAction, GamePhase, Player, Card, AgentDecision, 
    PlayerObservation, GameResult, AgentDecisionSchema
)
from src.haive.games.poker.state import PokerState
from src.haive.games.poker.config import PokerAgentConfig
from src.haive.games.poker.prompts import (
    decision_prompt, hand_analysis_prompt, opponent_modeling_prompt,
    game_summary_prompt, get_system_prompt
)
from src.haive.games.poker.state_manager import PokerStateManager

# Set up enhanced logging
logger = logging.getLogger(__name__)
file_handler = logging.FileHandler("poker_debug.log")
file_handler.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.addHandler(console_handler)
logger.setLevel(logging.DEBUG)

class RetryConfiguration:
    """Configuration for retry policies."""
    MAX_RETRIES = 3
    RETRY_DELAY = 1.5  # seconds
    BACKOFF_FACTOR = 1.5  # exponential backoff

@register_agent(PokerAgentConfig)
class PokerAgent(Agent[PokerAgentConfig]):
    """Enhanced agent class for managing a multi-player Texas Hold'em poker game.

    Key improvements:
    - Proper structured output handling
    - Comprehensive debug logging
    - Retry policies for failed operations
    - Enhanced prompts and decision handling
    """
    
    def __init__(self, config: PokerAgentConfig=PokerAgentConfig()):
        """Initialize the enhanced poker agent."""
        logger.info("Initializing Enhanced Poker Agent")
        self.state_manager = PokerStateManager(debug=True)
        super().__init__(config)
        self.hands_played = 0
        self.player_stats = {}
        self.player_agents = {}
        self.hand_analyzer = None
        self.retry_history = {}  # Track retry attempts for debugging
        
        # Compose LLM runnables for players and analyzers
        self._setup_agent_runnables()
        logger.info(f"Agent initialized with {len(self.config.player_names)} players")
        
    def _setup_agent_runnables(self):
        """Set up LLM runnables for all players with improved error handling."""
        logger.debug("Setting up agent runnables")
        
        try:
            # Set up agent for hand analysis
            if 'hand_analyzer' in self.config.engines:
                logger.debug("Configuring hand analyzer")
                analyzer_config = self.config.engines['hand_analyzer']
                analyzer_llm = compose_runnable(analyzer_config)
                self.hand_analyzer = analyzer_config.prompt_template | analyzer_llm
            
            # Set up player agents
            agent_types = ['conservative_agent', 'aggressive_agent', 'balanced_agent', 'loose_agent']
            available_configs = [key for key in self.config.engines.keys() if key in agent_types]
            
            if not available_configs:
                logger.error("No valid agent configurations found!")
                raise ValueError("No valid agent configurations found")
            
            logger.debug(f"Available agent types: {available_configs}")
            
            # Assign agent types to players
            for i, player_name in enumerate(self.config.player_names):
                # Choose an agent type (cycle through available types)
                agent_type = available_configs[i % len(available_configs)]
                agent_config = self.config.engines[agent_type]
                style = agent_type.split('_')[0]
                system_prompt = get_system_prompt(style)
                
                # Create runnable with decision prompt
                agent_llm = compose_runnable(agent_config)
                prompt_template = agent_config.prompt_template
                
                # Store runnable with player ID
                player_id = f"player_{i}"
                self.player_agents[player_id] = {
                    'runnable': agent_llm,
                    'prompt_template': prompt_template,
                    'name': player_name,
                    'style': style,
                    'system_prompt': system_prompt
                }
                
                # Initialize player stats
                self.player_stats[player_id] = {
                    'name': player_name,
                    'hands_played': 0,
                    'hands_won': 0,
                    'chips_won': 0,
                    'chips_lost': 0,
                    'biggest_pot_won': 0,
                    'total_bets': 0,
                    'folds': 0,
                    'checks': 0,
                    'calls': 0,
                    'bets': 0,
                    'raises': 0,
                    'all_ins': 0,
                    'decision_errors': 0,
                    'retries': 0
                }
                
                logger.info(f"Set up {style} agent for player {player_name} (ID: {player_id})")

        except Exception as e:
            logger.error(f"Error setting up agent runnables: {e}")
            logger.error(traceback.format_exc())
            raise

    def setup_workflow(self):
        """Set up the poker game workflow graph with enhanced error handling."""
        logger.info("Setting up poker game workflow")
        
        try:
            # Define nodes
            self.graph.add_node("initialize_game", self.initialize_game)
            self.graph.add_node("setup_hand", self.setup_hand)
            self.graph.add_node("player_decision", self.handle_player_decision)
            self.graph.add_node("update_game_phase", self.update_game_phase)
            self.graph.add_node("end_hand", self.end_hand)
            self.graph.add_node("end_game", self.end_game)
            
            # Define edges
            self.graph.add_edge(START, "initialize_game")
            self.graph.add_edge("initialize_game", "setup_hand")
            self.graph.add_edge("setup_hand", "player_decision")
            
            # Player Decision conditions
            self.graph.add_conditional_edges(
                "player_decision",
                self.should_continue_round,
                {
                    "continue_round": "player_decision",
                    "advance_phase": "update_game_phase",
                    "end_hand": "end_hand"
                }
            )
            
            # Update Game Phase conditions
            self.graph.add_conditional_edges(
                "update_game_phase",
                self.should_continue_to_next_phase,
                {
                    "next_phase": "player_decision",
                    "showdown": "end_hand"
                }
            )
            
            # End Hand conditions
            self.graph.add_conditional_edges(
                "end_hand",
                self.should_play_another_hand,
                {
                    True: "setup_hand",
                    False: "end_game"
                }
            )
            
            # End Game -> END
            self.graph.add_edge("end_game", END)
            
            logger.info("Poker game workflow setup complete")
            
        except Exception as e:
            logger.error(f"Error setting up workflow: {e}")
            logger.error(traceback.format_exc())
            raise
    
    def initialize_game(self, state: PokerState) -> PokerState:
        """Initialize the poker game state with enhanced logging."""
        logger.info("Initializing game state")
        
        try:
            # Reset game state
            state.initialize_game(
                player_names=self.config.player_names, 
                starting_chips=self.config.starting_chips
            )
            
            # Set blinds
            state.game.small_blind = self.config.small_blind
            state.game.big_blind = self.config.big_blind
            
            # Log initialization
            state.log_event(f"Game initialized with {len(state.game.players)} players")
            state.log_event(f"Small blind: ${state.game.small_blind}, Big blind: ${state.game.big_blind}")
            
            # Debug log all player details
            logger.debug("Players initialized:")
            for player in state.game.players:
                logger.debug(f"  {player.id}: {player.name}, ${player.chips}, Position: {player.position}")
            
            # Reset stats
            self.hands_played = 0
            for player_id in self.player_stats:
                self.player_stats[player_id].update({
                    'hands_played': 0,
                    'hands_won': 0,
                    'chips_won': 0,
                    'chips_lost': 0,
                    'decision_errors': 0,
                    'retries': 0
                })
            
            logger.info("Game initialization complete")
            return state
            
        except Exception as e:
            logger.error(f"Error initializing game: {e}")
            logger.error(traceback.format_exc())
            state.error = f"Game initialization error: {str(e)}"
            return state
    
    def setup_hand(self, state: PokerState) -> PokerState:
        """Set up a new poker hand with enhanced error handling and debugging."""
        logger.info(f"Setting up hand #{self.hands_played + 1}")
        
        try:
            # Increment hands played
            self.hands_played += 1
            
            # Start a new hand
            state.start_new_hand()
            
            # Update player stats
            for player in state.game.players:
                if player.id in self.player_stats:
                    self.player_stats[player.id]['hands_played'] += 1
            
            # Log the start of a new hand
            state.log_event(f"Hand #{self.hands_played} started")
            
            # Log the dealer and blinds
            dealer_idx = state.game.dealer_position
            dealer = state.game.players[dealer_idx].name
            sb_idx = (dealer_idx + 1) % len(state.game.players)
            small_blind = state.game.players[sb_idx].name
            bb_idx = (dealer_idx + 2) % len(state.game.players)
            big_blind = state.game.players[bb_idx].name
            
            state.log_event(f"Dealer: {dealer}")
            state.log_event(f"Small Blind: {small_blind} (${state.game.small_blind})")
            state.log_event(f"Big Blind: {big_blind} (${state.game.big_blind})")
            
            # Debug log all player hole cards
            logger.debug("Player hole cards:")
            for player in state.game.players:
                logger.debug(f"  {player.name}: {player.hand}")
            
            # Set waiting_for_player
            current_player = state.game.players[state.game.current_player_idx]
            state.waiting_for_player = current_player.id
            
            logger.info(f"Hand #{self.hands_played} setup complete")
            return state
            
        except Exception as e:
            logger.error(f"Error setting up hand: {e}")
            logger.error(traceback.format_exc())
            state.error = f"Hand setup error: {str(e)}"
            return state
    
    def handle_player_decision(self, state: PokerState) -> PokerState:
        """Enhanced player decision handling with improved error recovery.
        
        This method:
        1. Determines the current player
        2. Calculates legal actions
        3. Gets decision from the player agent
        4. Validates and applies the decision
        5. Updates game state
        """
        game = state.game
        
        # Skip if game is over or in showdown
        if game.phase == GamePhase.GAME_OVER or game.phase == GamePhase.SHOWDOWN:
            logger.info("Game in terminal state, skipping player decision")
            return state
        
        # Get current player
        current_player_idx = game.current_player_idx
        
        # Skip if all players but one have folded (hand is over)
        active_players = [p for p in game.players if not p.has_folded]
        if len(active_players) <= 1:
            logger.info("Only one active player left, skipping player decision")
            game.phase = GamePhase.SHOWDOWN
            return state
        
        current_player = game.players[current_player_idx]
        
        # Skip if player has folded
        if current_player.has_folded:
            logger.debug(f"Player {current_player_idx} has folded, moving to next player")
            game.current_player_idx = self._get_next_player_idx(game)
            return state
        
        # Skip if player is all-in
        if current_player.is_all_in:
            logger.debug(f"Player {current_player_idx} is all-in, moving to next player")
            game.current_player_idx = self._get_next_player_idx(game)
            return state
        
        # Get the agent for this player
        player_id = f"player_{current_player_idx}"
        agent_info = self.player_agents.get(player_id)
        
        if not agent_info:
            logger.error(f"No agent found for player {player_id}")
            # Fallback to basic agent
            agent_info = next(iter(self.player_agents.values()))
        
        # Log player turn
        logger.info(f"Player {current_player_idx} ({current_player.name}) turn - {agent_info['style']} agent")
        
        # Calculate legal actions for this player
        legal_actions = self._get_legal_actions(game, current_player)
        
        # Prepare decision context
        context = self._prepare_decision_context(state, current_player_idx, legal_actions)
        
        # Get decision from agent
        try:
            logger.debug(f"Getting decision for player {current_player_idx}")
            
            # Add system prompt for better guidance
            system_prompt = agent_info.get('system_prompt', '')
            decision_prompt_text = decision_prompt.format(
                player_cards=context["player_cards"],
                community_cards=context["community_cards"] or "None",
                position=context["position"],
                pot_size=context["pot_size"],
                current_bet=context["current_bet"],
                player_chips=context["player_chips"],
                legal_actions=self._format_legal_actions(legal_actions),
                other_players=context["other_players"]
            )
            
            # Create a guided prompt with system message
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=decision_prompt_text)
            ]
            
            # Get decision with retry logic
            decision = self._get_player_decision_with_retry(agent_info['runnable'], messages, context, legal_actions)
            
            # Decision received successfully
            if decision:
                logger.info(f"Player {current_player_idx} decision: {decision.action} {decision.amount if hasattr(decision, 'amount') else ''}")
                
                # Apply the decision
                self._apply_player_decision(game, current_player, decision, legal_actions)
                
                # Update player stats
                self._update_player_stats(player_id, decision.action, decision.amount if hasattr(decision, 'amount') else 0)
                
                # Move to next player
                game.current_player_idx = self._get_next_player_idx(game)
            else:
                # Fallback decision (FOLD or CHECK if possible)
                logger.warning(f"Using fallback decision for player {current_player_idx}")
                fallback_action = self._get_fallback_action(legal_actions)
                self._apply_player_decision(game, current_player, fallback_action, legal_actions)
                game.current_player_idx = self._get_next_player_idx(game)
        
        except Exception as e:
            logger.error(f"Error handling player decision: {e}")
            logger.error(traceback.format_exc())
            
            # Use fallback decision (fold)
            fallback_action = self._get_fallback_action(legal_actions)
            logger.warning(f"Using emergency fallback: {fallback_action}")
            self._apply_player_decision(game, current_player, fallback_action, legal_actions)
            game.current_player_idx = self._get_next_player_idx(game)
            
            # Update error stats
            if player_id in self.player_stats:
                self.player_stats[player_id]["decision_errors"] += 1
        
        return state
    
    def _get_player_decision_with_retry(self, runnable, messages, context, legal_actions, max_retries=3):
        """Get player decision with retry logic for handling invalid outputs."""
        decision = None
        retries = 0
        
        while retries < max_retries and decision is None:
            try:
                raw_decision = runnable.invoke(messages)
                logger.debug(f"Raw decision: {raw_decision}")
                
                # Handle different response formats
                if isinstance(raw_decision, AgentDecision):
                    # Properly structured output
                    decision = raw_decision
                elif isinstance(raw_decision, dict) and "action" in raw_decision:
                    # Dict with action field
                    decision = AgentDecision(
                        action=raw_decision["action"],
                        amount=raw_decision.get("amount", 0),
                        reasoning=raw_decision.get("reasoning", "")
                    )
                elif hasattr(raw_decision, "content"):
                    # Message-like response
                    content = raw_decision.content
                    # Try to parse JSON from content
                    try:
                        # Extract JSON if it exists
                        import re
                        import json
                        
                        # Look for JSON pattern
                        json_match = re.search(r'\{.*\}', content, re.DOTALL)
                        if json_match:
                            json_str = json_match.group(0)
                            decision_dict = json.loads(json_str)
                            
                            if "action" in decision_dict:
                                decision = AgentDecision(
                                    action=decision_dict["action"],
                                    amount=decision_dict.get("amount", 0),
                                    reasoning=decision_dict.get("reasoning", "")
                                )
                        else:
                            # Simple text parsing
                            action_match = re.search(r'action[:\s]+([A-Z]+)', content, re.IGNORECASE)
                            amount_match = re.search(r'amount[:\s]+(\d+)', content, re.IGNORECASE)
                            
                            if action_match:
                                action = action_match.group(1).upper()
                                amount = int(amount_match.group(1)) if amount_match else 0
                                
                                decision = AgentDecision(
                                    action=action,
                                    amount=amount,
                                    reasoning=""
                                )
                    except Exception as e:
                        logger.warning(f"Error parsing decision from content: {e}")
                        # Continue to retry
                
                # Validate decision
                if decision:
                    if not self._is_valid_decision(decision, legal_actions):
                        logger.warning(f"Invalid decision: {decision}, retrying")
                        decision = None
            
            except Exception as e:
                logger.warning(f"Error getting player decision: {e}")
                logger.debug(traceback.format_exc())
                decision = None
            
            retries += 1
            
            if decision is None and retries < max_retries:
                logger.info(f"Retrying decision, attempt {retries+1}/{max_retries}")
                time.sleep(1)  # Brief delay before retry
        
        return decision
    
    def _is_valid_decision(self, decision, legal_actions):
        """Check if a decision is valid given the legal actions."""
        try:
            # Convert decision action to enum if it's a string
            if isinstance(decision.action, str):
                action_str = decision.action.upper()
                # Try to convert to PlayerAction enum
                try:
                    action = PlayerAction[action_str]
                except KeyError:
                    # Handle common variants
                    action_map = {
                        "RAISE": PlayerAction.RAISE,
                        "BET": PlayerAction.BET,
                        "CALL": PlayerAction.CALL,
                        "CHECK": PlayerAction.CHECK,
                        "FOLD": PlayerAction.FOLD,
                        "ALL_IN": PlayerAction.ALL_IN,
                        "ALLIN": PlayerAction.ALL_IN,
                        "ALL-IN": PlayerAction.ALL_IN
                    }
                    action = action_map.get(action_str)
                    if not action:
                        logger.warning(f"Unknown action: {action_str}")
                        return False
            else:
                action = decision.action
            
            # Check if action is in legal actions
            legal_action_types = [la["action"] for la in legal_actions]
            
            if action not in legal_action_types and action.name not in legal_action_types:
                logger.warning(f"Action {action} not in legal actions: {legal_action_types}")
                return False
            
            # For BET/RAISE, check amount constraints
            if action in (PlayerAction.BET, PlayerAction.RAISE):
                for la in legal_actions:
                    if la["action"] == action or la["action"] == action.name:
                        min_amount = la.get("min_amount", 0)
                        max_amount = la.get("max_amount", float("inf"))
                        
                        amount = decision.amount if hasattr(decision, "amount") else 0
                        
                        if amount < min_amount or amount > max_amount:
                            logger.warning(f"Amount {amount} outside range [{min_amount}, {max_amount}]")
                            return False
                        
                        return True
            
            return True
        
        except Exception as e:
            logger.error(f"Error validating decision: {e}")
            return False
    
    def _get_fallback_action(self, legal_actions):
        """Get a fallback action when decision fails."""
        # Prefer CHECK if available
        for la in legal_actions:
            if la["action"] == PlayerAction.CHECK:
                return AgentDecision(action=PlayerAction.CHECK, amount=0, reasoning="Fallback decision")
        
        # Otherwise FOLD
        return AgentDecision(action=PlayerAction.FOLD, amount=0, reasoning="Fallback decision")
    
    def _get_player_name(self, player_id: str) -> str:
        """Get player name from ID, with format 'P1' if not found."""
        for player in self.state_manager.state.game.players:
            if player.id == player_id:
                return player.name
        # If not found, extract player number from ID
        if player_id.startswith("player_"):
            try:
                player_num = int(player_id.split("_")[1]) + 1
                return f"P{player_num}"
            except:
                pass
        return player_id
    
    def _get_legal_actions(self, state: PokerState, player: Player) -> List[Dict[str, Any]]:
        """Get legal actions for a player with enhanced error handling."""
        try:
            if not player.is_active or player.is_all_in:
                return []
                
            legal_actions = []
            
            # Fold is always legal
            legal_actions.append({
                "action": PlayerAction.FOLD,
                "amount": 0
            })
            
            # Check is legal if no bet to call
            call_amount = state.game.current_bet - player.current_bet
            if call_amount <= 0:
                legal_actions.append({
                    "action": PlayerAction.CHECK,
                    "amount": 0
                })
            
            # Call is legal if there's a bet to call and player has chips
            if call_amount > 0 and player.chips >= call_amount:
                legal_actions.append({
                    "action": PlayerAction.CALL,
                    "amount": call_amount
                })
            
            # Bet is legal if no current bet and player has chips
            if state.game.current_bet == 0 and player.chips > 0:
                # Minimum bet is big blind
                min_bet = min(state.game.big_blind, player.chips)
                legal_actions.append({
                    "action": PlayerAction.BET,
                    "amount": min_bet,
                    "min": min_bet,
                    "max": player.chips
                })
            
            # Raise is legal if there's a bet and player has enough chips
            if state.game.current_bet > 0 and player.chips > call_amount:
                min_raise_to = state.game.current_bet + state.game.min_raise
                min_raise = min(min_raise_to, player.current_bet + player.chips)
                legal_actions.append({
                    "action": PlayerAction.RAISE,
                    "amount": min_raise,
                    "min": min_raise,
                    "max": player.current_bet + player.chips
                })
            
            # All-in is always legal if player has chips
            if player.chips > 0:
                legal_actions.append({
                    "action": PlayerAction.ALL_IN,
                    "amount": player.chips
                })
            
            logger.debug(f"Legal actions for {player.name}: {[a['action'] for a in legal_actions]}")
            return legal_actions
            
        except Exception as e:
            logger.error(f"Error getting legal actions: {e}")
            # Return fold as the only legal action in case of error
            return [{
                "action": PlayerAction.FOLD,
                "amount": 0
            }]
        
    def _prepare_decision_context(self, state: PokerState, player_idx: int, legal_actions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Prepare the context for decision-making."""
        game = state.game
        player = game.players[player_idx]
        
        # Extract relevant information
        player_cards = str(player.hand)
        community_cards = [str(card) for card in game.community_cards]
        position = player.position
        pot_size = sum(pot.amount for pot in game.pots)
        current_bet = game.current_bet
        player_chips = player.chips
        other_players = [p for p in game.players if p.id != player.id]
        
        return {
            "player_cards": player_cards,
            "community_cards": community_cards,
            "position": position,
            "pot_size": pot_size,
            "current_bet": current_bet,
            "player_chips": player_chips,
            "other_players": other_players
        }
    
    def _apply_player_decision(self, game: PokerState, player: Player, decision: AgentDecision, legal_actions: List[Dict[str, Any]]):
        """Apply the player's decision to the game state."""
        if decision.action == PlayerAction.FOLD:
            player.has_folded = True
            game.current_player_idx = self._get_next_player_idx(game)
        elif decision.action == PlayerAction.CHECK:
            game.current_player_idx = self._get_next_player_idx(game)
        elif decision.action == PlayerAction.CALL:
            game.current_player_idx = self._get_next_player_idx(game)
        elif decision.action == PlayerAction.BET:
            game.current_player_idx = self._get_next_player_idx(game)
        elif decision.action == PlayerAction.RAISE:
            game.current_player_idx = self._get_next_player_idx(game)
        elif decision.action == PlayerAction.ALL_IN:
            player.is_all_in = True
            game.current_player_idx = self._get_next_player_idx(game)
        else:
            logger.warning(f"Unknown decision action: {decision.action}")
    
    def _get_next_player_idx(self, game: PokerState) -> int:
        """Get the index of the next active player."""
        current_idx = game.current_player_idx
        next_idx = (current_idx + 1) % len(game.players)
        while game.players[next_idx].has_folded:
            next_idx = (next_idx + 1) % len(game.players)
        return next_idx
    
    def _format_legal_actions(self, legal_actions: List[Dict[str, Any]]) -> str:
        """Format legal actions as a readable string."""
        return ", ".join([f"{la['action'].upper()} ${la['amount']}" for la in legal_actions])
    
    def _update_player_stats(self, player_id: str, action: PlayerAction, amount: int):
        """Update player statistics based on their decision."""
        if player_id not in self.player_stats:
            logger.warning(f"Cannot update stats for unknown player: {player_id}")
            return
        
        stats = self.player_stats[player_id]
        player_name = stats['name']
        
        # Update action counts
        if action == PlayerAction.FOLD:
            stats['folds'] += 1
            logger.debug(f"Recorded FOLD for {player_name}")
        elif action == PlayerAction.CHECK:
            stats['checks'] += 1
            logger.debug(f"Recorded CHECK for {player_name}")
        elif action == PlayerAction.CALL:
            stats['calls'] += 1
            stats['total_bets'] += amount
            logger.debug(f"Recorded CALL for {player_name}: ${amount}")
        elif action == PlayerAction.BET:
            stats['bets'] += 1
            stats['total_bets'] += amount
            logger.debug(f"Recorded BET for {player_name}: ${amount}")
        elif action == PlayerAction.RAISE:
            stats['raises'] += 1
            stats['total_bets'] += amount
            logger.debug(f"Recorded RAISE for {player_name}: ${amount}")
        elif action == PlayerAction.ALL_IN:
            stats['all_ins'] += 1
            stats['total_bets'] += amount
            logger.debug(f"Recorded ALL_IN for {player_name}: ${amount}")
    
    def update_game_phase(self, state: PokerState) -> PokerState:
        """Update the game phase and handle phase transitions."""
        logger.info(f"Updating game phase from {state.game.phase.value}")
        
        try:
            # Move to the next phase
            state.advance_game_phase()
            
            # Log the phase transition
            phase_str = state.game.phase.value.upper()
            if state.game.phase not in [GamePhase.PREFLOP, GamePhase.GAME_OVER]:
                community_cards = [str(card) for card in state.game.community_cards]
                logger.info(f"New phase: {phase_str} with cards: {', '.join(community_cards)}")
                state.log_event(f"{phase_str}: {', '.join(community_cards)}")
            else:
                logger.info(f"New phase: {phase_str}")
                state.log_event(f"{phase_str}")
            
            # Debug log current game state after phase change
            logger.debug(f"Current game state after phase change:")
            logger.debug(f"  Phase: {state.game.phase.value}")
            logger.debug(f"  Community cards: {[str(c) for c in state.game.community_cards]}")
            logger.debug(f"  Pot sizes: {[pot.amount for pot in state.game.pots]}")
            logger.debug(f"  Current bet: {state.game.current_bet}")
            logger.debug(f"  Active players: {len(state.game.active_players)}")
            
            return state
            
        except Exception as e:
            logger.error(f"Error updating game phase: {e}")
            logger.error(traceback.format_exc())
            state.error = f"Phase update error: {str(e)}"
            return state

    def end_hand(self, state: PokerState) -> PokerState:
        """Handle the end of a hand - determine winner(s) and update stats."""
        logger.info("Ending current hand")
        
        try:
            # If the game is not in GAME_OVER phase, handle showdown
            if state.game.phase != GamePhase.GAME_OVER:
                logger.info("Processing showdown")
                state.game.phase = GamePhase.SHOWDOWN
                state._handle_showdown()
            
            # Log the end of the hand
            state.log_event(f"Hand #{self.hands_played} completed")
            
            # Debug log all player hands and rankings
            logger.debug("Final hand results:")
            for player in state.game.players:
                hand_str = str(player.hand) if player.hand and player.hand.cards else "Folded"
                ranking = state.game.hand_rankings.get(player.id, None)
                ranking_str = ranking.description if ranking else "N/A"
                logger.debug(f"  {player.name}: {hand_str} - {ranking_str}")
            
            # Update player stats for winners
            logger.info(f"Winners: {[self._get_player_name(w) for w in state.game.winners]}")
            for winner_id in state.game.winners:
                if winner_id in self.player_stats:
                    winner = next((p for p in state.game.players if p.id == winner_id), None)
                    if winner:
                        self.player_stats[winner_id]['hands_won'] += 1
                        
                        # Calculate chips won (current chips - starting chips)
                        initial_chips = self.config.starting_chips
                        chips_diff = winner.chips - initial_chips
                        
                        if chips_diff > 0:
                            self.player_stats[winner_id]['chips_won'] += chips_diff
                            logger.debug(f"{winner.name} won {chips_diff} chips total")
                        elif chips_diff < 0:
                            self.player_stats[winner_id]['chips_lost'] += abs(chips_diff)
                            logger.debug(f"{winner.name} lost {abs(chips_diff)} chips total")
                        
                        # Calculate biggest pot
                        total_pot = sum(pot.amount for pot in state.game.pots)
                        if total_pot > self.player_stats[winner_id]['biggest_pot_won']:
                            self.player_stats[winner_id]['biggest_pot_won'] = total_pot
                            logger.debug(f"New biggest pot for {winner.name}: ${total_pot}")
            
            # Clear waiting_for_player
            state.waiting_for_player = None
            
            # Mark the end of the hand in the log
            state.log_event("-" * 40)
            
            logger.info("Hand completion processed successfully")
            return state
            
        except Exception as e:
            logger.error(f"Error ending hand: {e}")
            logger.error(traceback.format_exc())
            state.error = f"Hand completion error: {str(e)}"
            return state
    
    def end_game(self, state: PokerState) -> PokerState:
        """End the poker game and determine final results."""
        logger.info("Ending game")
        
        try:
            # Determine final standings
            players = sorted(state.game.players, key=lambda p: p.chips, reverse=True)
            winner = players[0]
            state.game.winner = winner.name
            
            # Log final results
            state.log_event("\n=== GAME OVER ===")
            state.log_event(f"Winner: {winner.name} with ${winner.chips}")
            logger.info(f"Game winner: {winner.name} with ${winner.chips}")
            
            # Log final standings
            logger.info("Final Standings:")
            state.log_event("\nFinal Standings:")
            for i, player in enumerate(players, 1):
                state.log_event(f"{i}. {player.name}: ${player.chips}")
                logger.info(f"{i}. {player.name}: ${player.chips}")
            
            # Log player statistics
            state.log_event("\nPlayer Statistics:")
            logger.info("Player Statistics:")
            for player in players:
                stats = self.player_stats[player.id]
                state.log_event(f"\n{player.name}:")
                state.log_event(f"Hands Played: {stats['hands_played']}")
                state.log_event(f"Hands Won: {stats['hands_won']}")
                state.log_event(f"Biggest Pot: ${stats['biggest_pot_won']}")
                state.log_event(f"Total Bets: ${stats['total_bets']}")
                state.log_event(f"Actions: Fold({stats['folds']}) Check({stats['checks']}) "
                              f"Call({stats['calls']}) Bet({stats['bets']}) "
                              f"Raise({stats['raises']}) All-in({stats['all_ins']})")
                state.log_event(f"Decision Errors: {stats['decision_errors']}")
                state.log_event(f"Retries: {stats['retries']}")
                
                # Log to console too
                logger.info(f"{player.name}: {stats['hands_won']}/{stats['hands_played']} hands won")
                logger.info(f"  Actions: Fold({stats['folds']}) Check({stats['checks']}) "
                          f"Call({stats['calls']}) Bet({stats['bets']}) "
                          f"Raise({stats['raises']}) All-in({stats['all_ins']})")
            
            # Log error and retry statistics
            total_errors = sum(stats['decision_errors'] for stats in self.player_stats.values())
            total_retries = sum(stats['retries'] for stats in self.player_stats.values())
            logger.info(f"Total decision errors: {total_errors}")
            logger.info(f"Total retries: {total_retries}")
            
            # Save final game history
            if self.config.save_game_history:
                self._save_game_history(state)
            
            return state
            
        except Exception as e:
            logger.error(f"Error ending game: {e}")
            logger.error(traceback.format_exc())
            state.error = f"Game end error: {str(e)}"
            return state
    
    def _save_game_history(self, state: PokerState):
        """Save the current game state and history to disk."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"poker_game_{timestamp}.log"
        
        try:
            # Create logs directory if it doesn't exist
            if not os.path.exists("logs"):
                os.makedirs("logs")
            
            with open(f"logs/{filename}", "w") as f:
                # Write game configuration
                f.write("=== GAME CONFIGURATION ===\n")
                f.write(f"Players: {len(state.game.players)}\n")
                f.write(f"Starting Chips: ${self.config.starting_chips}\n")
                f.write(f"Small Blind: ${self.config.small_blind}\n")
                f.write(f"Big Blind: ${self.config.big_blind}\n")
                f.write(f"Hands Played: {self.hands_played}\n\n")
                
                # Write game events
                f.write("=== GAME HISTORY ===\n")
                for event in state.game_log:
                    f.write(f"{event}\n")
                
                # Write final statistics
                f.write("\n=== PLAYER STATISTICS ===\n")
                for player_id, stats in self.player_stats.items():
                    f.write(f"\n{stats['name']}:\n")
                    for key, value in stats.items():
                        if key != 'name':
                            f.write(f"{key}: {value}\n")
                
                # Write error statistics
                f.write("\n=== ERROR STATISTICS ===\n")
                total_errors = sum(stats['decision_errors'] for stats in self.player_stats.values())
                total_retries = sum(stats['retries'] for stats in self.player_stats.values())
                f.write(f"Total decision errors: {total_errors}\n")
                f.write(f"Total retries: {total_retries}\n")
                
                # Write retry history
                f.write("\n=== RETRY HISTORY ===\n")
                for key, count in self.retry_history.items():
                    if count > 0:
                        f.write(f"{key}: {count} retries\n")
            
            logger.info(f"Game history saved to logs/{filename}")
            
        except Exception as e:
            logger.error(f"Error saving game history: {e}")
            logger.error(traceback.format_exc())
    
    def should_continue_round(self, state: PokerState) -> str:
        """Determine if we should continue the current betting round."""
        logger.debug("Checking if betting round should continue")
        
        # If an error occurred, log and end the hand
        if state.error:
            logger.error(f"Error state detected: {state.error}")
            return "end_hand"
        
        # If the hand is over (only one player left), end the hand
        if len(state.game.active_players) <= 1:
            logger.info(f"Only one player remains active: {state.game.active_players}")
            return "end_hand"
            
        # If the round is complete, advance to the next phase
        if state.game.round_complete:
            logger.info("Betting round is complete, advancing to next phase")
            return "advance_phase"
            
        # Otherwise, continue the round
        logger.debug("Continuing betting round")
        return "continue_round"
    
    def should_continue_to_next_phase(self, state: PokerState) -> str:
        """Determine if the game should advance to the next phase."""
        logger.debug(f"Checking if game should continue after {state.game.phase.value}")
        
        if state.game.phase == GamePhase.RIVER:
            logger.info("River complete, moving to showdown")
            return "showdown"
            
        logger.info(f"Moving to next phase after {state.game.phase.value}")
        return "next_phase"
    
    def should_play_another_hand(self, state: PokerState) -> bool:
        """Determine if another hand should be played."""
        logger.debug("Checking if another hand should be played")
        
        # Check if we've reached the maximum number of hands
        if self.hands_played >= self.config.max_hands:
            logger.info(f"Reached maximum hands ({self.config.max_hands}), ending game")
            return False
        
        # Check if only one player has chips
        players_with_chips = sum(1 for p in state.game.players if p.chips > 0)
        
        if players_with_chips <= 1:
            logger.info(f"Only {players_with_chips} player(s) have chips remaining, ending game")
            return False
            
        logger.info("Game will continue with another hand")
        return True