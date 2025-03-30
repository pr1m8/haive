"""Poker agent implementation for multi-agent Texas Hold'em games.

This module implements a sophisticated poker agent that manages a multi-player
Texas Hold'em game. Key features include:
    - Multi-agent gameplay with different playing styles
    - LLM-based decision making for each player
    - Hand analysis and opponent modeling
    - Complete game state management
    - Detailed game history and statistics tracking
    - Configurable game parameters

The agent uses language models to generate player decisions, analyze hands,
and create engaging gameplay narratives. Each player can have a different
playing style (conservative, aggressive, balanced, loose) with corresponding
LLM configurations.

Example:
    >>> from poker.agent import PokerAgent
    >>> from poker.config import PokerAgentConfig
    >>> 
    >>> # Create agent with custom config
    >>> config = PokerAgentConfig(
    ...     player_names=["Alice", "Bob", "Charlie"],
    ...     starting_chips=1000,
    ...     small_blind=5,
    ...     big_blind=10
    ... )
    >>> agent = PokerAgent(config)
    >>> 
    >>> # Run a complete game
    >>> result = agent.run()
"""

import logging
import uuid
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
import re

logger = logging.getLogger(__name__)
logging.basicConfig(
    filename="poker.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
@register_agent(PokerAgentConfig)
class PokerAgent(Agent[PokerAgentConfig]):
    """Agent class for managing a multi-player Texas Hold'em poker game.

    This agent coordinates multiple AI players with different playing styles,
    manages game state, and handles all aspects of poker gameplay including
    betting rounds, hand evaluation, and game progression.

    The agent uses LLMs for:
        - Player decision making (bet, call, fold, etc.)
        - Hand strength analysis
        - Opponent modeling and adaptation
        - Game narration and logging

    Attributes:
        state_schema_manager (PokerStateManager): Manages game state transitions.
        hands_played (int): Number of hands completed in current game.
        player_stats (Dict[str, Dict]): Statistics for each player.
        player_agents (Dict[str, Dict]): LLM configurations and prompts for each player.
        hand_analyzer (Optional[Any]): LLM chain for analyzing hand strength.

    Example:
        >>> agent = PokerAgent()
        >>> agent.setup_workflow()
        >>> result = agent.run()
        >>> print(f"Winner: {result.winner}")
    """
    
    def __init__(self, config: PokerAgentConfig=PokerAgentConfig()):
        """Initialize the poker agent.

        Args:
            config (PokerAgentConfig, optional): Configuration for the game.
                Defaults to a new PokerAgentConfig instance.

        The initialization process:
            1. Sets up the state manager
            2. Initializes game statistics
            3. Creates LLM configurations for each player
            4. Sets up the hand analyzer

        Example:
            >>> config = PokerAgentConfig(player_names=["P1", "P2", "P3"])
            >>> agent = PokerAgent(config)
        """
        self.state_schema_manager = PokerStateManager()
        super().__init__(config)
        self.hands_played = 0
        self.player_stats = {}
        self.player_agents = {}
        self.hand_analyzer = None
        
        # Compose LLM runnables for players and analyzers
        self._setup_agent_runnables()
        
    def _setup_agent_runnables(self):
        """Set up LLM runnables for all players and the hand analyzer.

        This method:
            1. Creates the hand analysis LLM chain if configured
            2. Sets up player-specific LLM configurations
            3. Assigns playing styles to players
            4. Initializes player statistics

        The method supports multiple playing styles:
            - Conservative: Tight and risk-averse play
            - Aggressive: Frequent betting and bluffing
            - Balanced: Adaptable strategy
            - Loose: Plays many hands

        Side Effects:
            - Populates self.hand_analyzer
            - Populates self.player_agents
            - Initializes self.player_stats
        """
        # Set up agent for hand analysis
        if 'hand_analyzer' in self.config.engines:
            analyzer_config = self.config.engines['hand_analyzer']
            analyzer_llm = compose_runnable(analyzer_config)
            self.hand_analyzer = analyzer_config.prompt_template | analyzer_llm
        
        # Set up player agents
        agent_types = ['conservative_agent', 'aggressive_agent', 'balanced_agent', 'loose_agent']
        available_configs = [key for key in self.config.engines.keys() if key in agent_types]
        
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
            }
            
            logger.info(f"Set up {style} agent for player {player_name} (ID: {player_id})")

    def setup_workflow(self):
        """Set up the poker game workflow graph.

        Creates a directed graph that manages the game flow, including:
            1. Game initialization
            2. Hand setup and dealing
            3. Player decision cycles
            4. Phase transitions (preflop -> flop -> turn -> river)
            5. Hand resolution and chip distribution
            6. Game termination

        The workflow uses conditional edges to handle:
            - Round completion conditions
            - Phase transitions
            - Hand and game ending conditions

        Side Effects:
            - Adds nodes to self.graph
            - Adds edges to self.graph
            - Sets up conditional transitions
        """
        logger.info("Setting up poker game workflow")
        
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
    
    def initialize_game(self, state: PokerState) -> PokerState:
        """Initialize the poker game state.

        Sets up the initial game state with players, chips, and blinds.
        Resets all game statistics and prepares for the first hand.

        Args:
            state (PokerState): Current game state to initialize.

        Returns:
            PokerState: Initialized game state.

        Side Effects:
            - Resets game statistics
            - Sets up player positions
            - Configures blind amounts
            - Initializes chip stacks
            - Logs game setup

        Example:
            >>> state = PokerState()
            >>> state = agent.initialize_game(state)
            >>> print(f"Players: {len(state.game.players)}")
        """
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
        
        # Reset stats
        self.hands_played = 0
        for player_id in self.player_stats:
            self.player_stats[player_id].update({
                'hands_played': 0,
                'hands_won': 0,
                'chips_won': 0,
                'chips_lost': 0,
            })
        
        return state
    
    def setup_hand(self, state: PokerState) -> PokerState:
        """Set up a new poker hand.

        Prepares the game state for a new hand by:
            1. Dealing hole cards to players
            2. Posting blinds
            3. Setting up the betting round
            4. Updating player statistics
            5. Logging hand information

        Args:
            state (PokerState): Current game state.

        Returns:
            PokerState: Updated game state ready for the new hand.

        Side Effects:
            - Increments hands_played counter
            - Updates player statistics
            - Logs hand setup details
            - Sets waiting_for_player

        Example:
            >>> state = agent.setup_hand(state)
            >>> print(f"Hand #{agent.hands_played} started")
        """
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
        
        # Log player hole cards (privately)
        for player in state.game.players:
            logger.debug(f"Player {player.name}'s hole cards: {player.hand}")
        
        # Set waiting_for_player
        current_player = state.game.players[state.game.current_player_idx]
        state.waiting_for_player = current_player.id
        
        return state
    
    def handle_player_decision(self, state: PokerState) -> PokerState:
        """Process the decision of the current player"""
        # Get the current player
        current_player_idx = state.game.current_player_idx
        current_player = state.game.players[current_player_idx]
        
        # Skip players who are not active or all-in
        if not current_player.is_active or current_player.is_all_in:
            state.log_event(f"Skipping {current_player.name} (inactive or all-in)")
            state._advance_to_next_player()
            
            # Set waiting_for_player to the next player
            next_player_idx = state.game.current_player_idx
            next_player = state.game.players[next_player_idx]
            state.waiting_for_player = next_player.id
            
            return state
        
        # Create observation for the current player
        observation = state.create_player_observation(current_player.id)
        
        # Get the player agent
        player_agent = self.player_agents.get(current_player.id)
        if not player_agent:
            error_msg = f"No agent found for player {current_player.id}"
            state.error = error_msg
            logger.error(error_msg)
            return state
        
        # Get legal moves
        legal_moves_list = self.state_manager.get_legal_actions(current_player.id) if hasattr(self, 'state_manager') else []
        legal_moves_str = ", ".join([f"{move['action']}" for move in legal_moves_list]) if legal_moves_list else "fold, check, call, bet, raise, all-in"
        
        try:
            # Format recent actions
            recent_actions_str = "None" if not observation.recent_actions else "\n".join([
                f"- {a.player_id.split('_')[1]}: {a.action.value.upper()}"
                f"{f' + {str(a.amount)}' if a.amount > 0 else ''}"
                for a in observation.recent_actions
            ])
            
            # Format player states
            player_states_str = "\n".join([
                f"- {p['name']}: ${p['chips']} "
                f"({'folded' if not p['is_active'] else 'all-in' if p['is_all_in'] else 'active'}) "
                f"Current bet: ${p['current_bet']}"
                for p in observation.visible_players
            ])
            
            # Format community cards
            community_cards_str = "None" if not observation.community_cards else ", ".join(
                [str(card) for card in observation.community_cards]
            )
            
            # Total pot size (sum of all pots)
            pot_size = sum(pot for pot in observation.pot_sizes)
            
            # Player's current bet this round
            player_current_bet = current_player.current_bet
            
            # Get the LLM and prompt template
            llm = player_agent['llm'] if 'llm' in player_agent else player_agent['runnable']
            
            # Create input dictionary with all variables the template might need
            input_values = {
                "player_id": current_player.id,
                "position_name": observation.position_name,
                "phase": observation.phase.value,
                "hand": str(observation.hand),
                "community_cards": community_cards_str,
                "chips": observation.chips,
                "current_bet": observation.current_bet - player_current_bet,  # What they need to call
                "pot_size": pot_size,
                "recent_actions": recent_actions_str,
                "player_states": player_states_str,
                "legal_moves": legal_moves_str,
            }
            
            # Get the decision from the agent - this will return an AgentDecisionSchema object
            response = llm.invoke(input_values)
            
            # IMPORTANT: No need to parse the response, it's already structured!
            # If using structured output, the response is already an AgentDecisionSchema object
            if isinstance(response, AgentDecisionSchema):
                # Create a standard AgentDecision from the structured output
                decision = AgentDecision(
                    action=response.action,
                    amount=response.amount,
                    reasoning=response.reasoning
                )
            else:
                # Fallback to parsing text if not structured (though this shouldn't happen)
                decision = self._parse_decision(response.content, current_player, state)
            
            # Log the decision
            state.current_decision = decision
            
            # Apply the decision
            state.handle_player_action(current_player.id, decision)
            
            # Update player stats
            self._update_player_stats(current_player.id, decision)
            
            # Set waiting_for_player to the next player
            next_player_idx = state.game.current_player_idx
            if next_player_idx < len(state.game.players):
                next_player = state.game.players[next_player_idx]
                state.waiting_for_player = next_player.id
            else:
                state.waiting_for_player = None
                
        except Exception as e:
            error_msg = f"Error getting decision from agent for {current_player.name}: {str(e)}"
            state.error = error_msg
            logger.error(error_msg)
        
            return state
    
    def _parse_decision(self, response_text: str, player: Player, state: PokerState) -> AgentDecision:
        """Parse the agent's decision from the response text"""
        # Initialize decision with defaults
        decision = AgentDecision(
            action=PlayerAction.FOLD,  # Default to FOLD
            amount=0,
            reasoning="Default reasoning"
        )
        
        try:
            # Extract key parts of the response
            response_lower = response_text.lower()
            
            # Determine the action
            if "fold" in response_lower:
                decision.action = PlayerAction.FOLD
            elif "check" in response_lower:
                decision.action = PlayerAction.CHECK
            elif "call" in response_lower:
                decision.action = PlayerAction.CALL
            elif "bet" in response_lower:
                decision.action = PlayerAction.BET
            elif "raise" in response_lower:
                decision.action = PlayerAction.RAISE
            elif "all-in" in response_lower or "all in" in response_lower:
                decision.action = PlayerAction.ALL_IN
            
            # Extract amount if applicable
            if decision.action in [PlayerAction.BET, PlayerAction.RAISE]:
                # Look for dollar amounts
                amount_matches = re.findall(r'\$(\d+)', response_lower)
                if amount_matches:
                    decision.amount = int(amount_matches[0])
                else:
                    # Try to find numbers
                    number_matches = re.findall(r'(?:bet|raise)(?:\s+to)?(?:\s+\$)?(\d+)', response_lower)
                    if number_matches:
                        decision.amount = int(number_matches[0])
                    else:
                        # Fallback values
                        if decision.action == PlayerAction.BET:
                            decision.amount = state.game.big_blind
                        elif decision.action == PlayerAction.RAISE:
                            decision.amount = state.game.current_bet + state.game.min_raise
            
            # For calls, set the amount to what needs to be called
            if decision.action == PlayerAction.CALL:
                decision.amount = state.game.current_bet - player.current_bet
            
            # For all-in, use all remaining chips
            if decision.action == PlayerAction.ALL_IN:
                decision.amount = player.chips
            
            # Extract reasoning
            reasoning_match = re.search(r'(?:reasoning|rationale|thinking|analysis):(.*?)(?:\n\n|$)', 
                                    response_lower, re.IGNORECASE | re.DOTALL)
            if reasoning_match:
                decision.reasoning = reasoning_match.group(1).strip()
            else:
                # Just use the last paragraph as reasoning
                paragraphs = response_text.split("\n\n")
                if paragraphs:
                    decision.reasoning = paragraphs[-1].strip()
        
        except Exception as e:
            logger.error(f"Error parsing decision: {str(e)}")
            decision.reasoning = f"Error parsing decision: {str(e)}"
        
        # Validate and adjust decision
        decision = self._validate_and_adjust_decision(decision, player, state)
        
        return decision
        
    def _validate_and_adjust_decision(self, decision: AgentDecision, player: Player, state: PokerState) -> AgentDecision:
        """Validate and adjust the decision to ensure it's legal"""
        
        # Check if CHECK is valid (only if there's no current bet to call)
        if decision.action == PlayerAction.CHECK and state.game.current_bet > player.current_bet:
            logger.warning(f"Invalid CHECK from {player.name}, cannot check when there's a bet to call")
            decision.action = PlayerAction.FOLD
            decision.reasoning += " (Adjusted from CHECK to FOLD because there was a bet to call)"
        
        # Check if BET is valid (only if no one has bet yet)
        if decision.action == PlayerAction.BET and state.game.current_bet > 0:
            logger.warning(f"Invalid BET from {player.name}, cannot bet when there's already a bet")
            
            # Adjust to CALL or RAISE based on the bet amount
            if decision.amount <= state.game.current_bet - player.current_bet:
                decision.action = PlayerAction.CALL
                decision.amount = state.game.current_bet - player.current_bet
                decision.reasoning += " (Adjusted from BET to CALL because there was already a bet)"
            else:
                decision.action = PlayerAction.RAISE
                decision.amount = decision.amount
                decision.reasoning += " (Adjusted from BET to RAISE because there was already a bet)"
        
        # Ensure RAISE is at least min raise
        if decision.action == PlayerAction.RAISE:
            min_raise_to = state.game.current_bet + state.game.min_raise
            if decision.amount < min_raise_to:
                logger.warning(f"Raise amount {decision.amount} less than min raise {min_raise_to}, adjusting")
                decision.amount = min_raise_to
                decision.reasoning += f" (Adjusted raise amount to minimum of {min_raise_to})"
        
        # Ensure BET is at least big blind
        if decision.action == PlayerAction.BET and decision.amount < state.game.big_blind:
            logger.warning(f"Bet amount {decision.amount} less than big blind {state.game.big_blind}, adjusting")
            decision.amount = state.game.big_blind
            decision.reasoning += f" (Adjusted bet amount to minimum of {state.game.big_blind})"
        
        # Ensure player has enough chips for the action
        if decision.action in [PlayerAction.BET, PlayerAction.RAISE, PlayerAction.CALL] and decision.amount > player.chips:
            logger.warning(f"{player.name} doesn't have enough chips for {decision.action}")
            
            if decision.amount >= player.chips:
                # If they're betting almost all chips, make it ALL_IN
                decision.action = PlayerAction.ALL_IN
                decision.amount = player.chips
                decision.reasoning += " (Adjusted to ALL_IN due to insufficient chips)"
        
        return decision
    
    def _update_player_stats(self, player_id: str, decision: AgentDecision):
        """Update player statistics based on their decision"""
        if player_id not in self.player_stats:
            return
        
        stats = self.player_stats[player_id]
        
        # Update action counts
        if decision.action == PlayerAction.FOLD:
            stats['folds'] += 1
        elif decision.action == PlayerAction.CHECK:
            stats['checks'] += 1
        elif decision.action == PlayerAction.CALL:
            stats['calls'] += 1
            stats['total_bets'] += decision.amount
        elif decision.action == PlayerAction.BET:
            stats['bets'] += 1
            stats['total_bets'] += decision.amount
        elif decision.action == PlayerAction.RAISE:
            stats['raises'] += 1
            stats['total_bets'] += decision.amount
        elif decision.action == PlayerAction.ALL_IN:
            stats['all_ins'] += 1
            stats['total_bets'] += decision.amount
    
    def update_game_phase(self, state: PokerState) -> PokerState:
        """Update the game phase and handle phase transitions.

        Manages transitions between game phases (preflop -> flop -> turn -> river),
        including dealing community cards and resetting betting rounds.

        Args:
            state (PokerState): Current game state.

        Returns:
            PokerState: Updated game state in the new phase.

        Side Effects:
            - Deals community cards
            - Resets betting amounts
            - Updates game phase
            - Logs phase transition

        Example:
            >>> state = agent.update_game_phase(state)
            >>> print(f"New phase: {state.game.phase}")
        """
        # Move to the next phase
        state.advance_game_phase()
        
        # Log the phase transition
        phase_str = state.game.phase.value.upper()
        if state.game.phase != GamePhase.PREFLOP:
            community_cards = [str(card) for card in state.game.community_cards]
            state.log_event(f"{phase_str}: {', '.join(community_cards)}")
        else:
            state.log_event(f"{phase_str}")
        
        return state
    
    # Fix for the end_hand method

    def end_hand(self, state: PokerState) -> PokerState:
        """Handle the end of a hand - determine winner(s) and update stats"""
        # If the game is not in GAME_OVER phase, handle showdown
        if state.game.phase != GamePhase.GAME_OVER:
            state.game.phase = GamePhase.SHOWDOWN
            state._handle_showdown()  # This method exists and should work correctly
        
        # Log the end of the hand
        state.log_event(f"Hand #{self.hands_played} completed")
        
        # Update player stats for winners
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
                    elif chips_diff < 0:
                        self.player_stats[winner_id]['chips_lost'] += abs(chips_diff)
                    
                    # Calculate biggest pot
                    total_pot = sum(pot.amount for pot in state.game.pots)
                    if total_pot > self.player_stats[winner_id]['biggest_pot_won']:
                        self.player_stats[winner_id]['biggest_pot_won'] = total_pot
        
        # Clear waiting_for_player
        state.waiting_for_player = None
        
        # Mark the end of the hand in the log
        state.log_event("-" * 40)
        
        return state
    
    def end_game(self, state: PokerState) -> PokerState:
        """End the poker game and determine final results.

        Calculates final standings, generates game summary, and handles
        cleanup tasks like saving game history.

        Args:
            state (PokerState): Current game state.

        Returns:
            PokerState: Final game state with results.

        Side Effects:
            - Calculates final chip counts
            - Determines winner(s)
            - Generates game summary
            - Saves final game history
            - Logs game results

        Example:
            >>> state = agent.end_game(state)
            >>> print(f"Game winner: {state.game.winner}")
            >>> print(f"Final chips: {state.game.chips}")
        """
        # Determine final standings
        players = sorted(state.game.players, key=lambda p: p.chips, reverse=True)
        winner = players[0]
        state.game.winner = winner.name
        
        # Log final results
        state.log_event("\n=== GAME OVER ===")
        state.log_event(f"Winner: {winner.name} with ${winner.chips}")
        
        # Log final standings
        state.log_event("\nFinal Standings:")
        for i, player in enumerate(players, 1):
            state.log_event(f"{i}. {player.name}: ${player.chips}")
        
        # Log player statistics
        state.log_event("\nPlayer Statistics:")
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
        
        # Save final game history
        if self.config.save_game_history:
            self._save_game_history(state)
        
        return state
    
    def _save_game_history(self, state: PokerState):
        """Save the current game state and history to disk.

        Creates a timestamped file containing game state, player actions,
        and statistics for analysis and replay.

        Args:
            state (PokerState): Current game state to save.

        Side Effects:
            - Creates a game history file
            - Writes game state and events
            - Saves player statistics

        Example:
            >>> agent._save_game_history(state)
            >>> print("Game history saved to logs/poker_game_TIMESTAMP.log")
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"poker_game_{timestamp}.log"
        
        try:
            with open(f"logs/{filename}", "w") as f:
                # Write game configuration
                f.write("=== GAME CONFIGURATION ===\n")
                f.write(f"Players: {len(state.game.players)}\n")
                f.write(f"Starting Chips: ${self.config.starting_chips}\n")
                f.write(f"Small Blind: ${self.config.small_blind}\n")
                f.write(f"Big Blind: ${self.config.big_blind}\n\n")
                
                # Write game events
                f.write("=== GAME HISTORY ===\n")
                for event in state.game.event_log:
                    f.write(f"{event}\n")
                
                # Write final statistics
                f.write("\n=== PLAYER STATISTICS ===\n")
                for player_id, stats in self.player_stats.items():
                    f.write(f"\n{stats['name']}:\n")
                    for key, value in stats.items():
                        if key != 'name':
                            f.write(f"{key}: {value}\n")
            
            logger.info(f"Game history saved to logs/{filename}")
            
        except Exception as e:
            logger.error(f"Error saving game history: {str(e)}")
    
    # Fix for the should_continue_round method

    def should_continue_round(self, state: PokerState) -> str:
        """Determine if we should continue the current betting round"""
        # If the hand is over (only one player left), end the hand
        if len(state.game.active_players) <= 1:
            return "end_hand"
        
        # If an error occurred, end the hand
        if state.error:
            logger.error(f"Error occurred: {state.error}")
            return "end_hand"
        
        # If the round is complete, advance to the next phase
        # Instead of calling is_betting_round_complete(), directly check the round_complete flag
        if state.game.round_complete:
            return "advance_phase"
        
        # Otherwise, continue the round
        return "continue_round"
    
    def should_continue_to_next_phase(self, state: PokerState) -> str:
        """Determine if the game should advance to the next phase.

        Checks if the current phase is complete and whether to move to
        showdown or the next betting round.

        Args:
            state (PokerState): Current game state.

        Returns:
            str: Decision string:
                - "next_phase": Advance to next betting round
                - "showdown": Proceed to showdown

        Example:
            >>> decision = agent.should_continue_to_next_phase(state)
            >>> if decision == "showdown":
            ...     print("Time for showdown!")
        """
        if state.game.phase == GamePhase.RIVER:
            return "showdown"
        return "next_phase"
    
    def should_play_another_hand(self, state: PokerState) -> bool:
        """Determine if another hand should be played.

        Checks if the maximum number of hands has been reached or if
        only one player has chips remaining.

        Args:
            state (PokerState): Current game state.

        Returns:
            bool: True if another hand should be played, False otherwise.

        Example:
            >>> if agent.should_play_another_hand(state):
            ...     print("Dealing next hand...")
            ... else:
            ...     print("Game complete!")
        """
        # Check if we've reached the maximum number of hands
        if self.hands_played >= self.config.max_hands:
            return False
        
        # Check if only one player has chips
        players_with_chips = sum(1 for p in state.game.players if p.chips > 0)
        return players_with_chips > 1