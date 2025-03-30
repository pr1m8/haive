"""Texas Hold'em Poker game state management.

This module implements the core state management for a Texas Hold'em poker game,
including:
    - Game initialization and progression
    - Player action handling
    - Betting rounds and pot management
    - Hand evaluation and showdown logic
    - Side pot creation for all-in situations

The state management is built on top of LangGraph for AI agent integration,
using Pydantic models for type safety and validation.

Example:
    >>> from poker.state import PokerState
    >>> 
    >>> # Initialize a new game
    >>> state = PokerState()
    >>> state.initialize_game(["Alice", "Bob", "Charlie"], starting_chips=1000)
    >>> state.start_new_hand()
"""

import random
import logging
from typing import List, Dict, Optional, Set, Tuple, Any
from pydantic import BaseModel, Field
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage

from src.haive.games.poker.models import (
    Card, Hand, Player, ActionRecord, HandRanking, Pot,
    PokerGameState, PlayerObservation, AgentDecision, GameResult,
    Suit, CardValue, HandRank, GamePhase, PlayerAction
)
from datetime import datetime
logger = logging.getLogger(__name__)

class PokerState(BaseModel):
    """State manager for Texas Hold'em Poker game.
    
    Manages the complete state of a poker game, including player actions,
    game progression, betting rounds, and hand evaluation. Built on top of
    LangGraph for AI agent integration.

    Attributes:
        messages (List[BaseMessage]): Message history for agent communication
        current_step (int): Current step in the game progression
        max_steps (int): Maximum allowed steps before forced game end
        error (Optional[str]): Current error state, if any
        memory (Dict[str, Any]): Persistent memory for game state
        game (PokerGameState): Current game state
        waiting_for_player (Optional[str]): ID of player we're waiting for
        game_log (List[str]): Timestamped log of game events
        current_decision (Optional[AgentDecision]): Last decision made

    Example:
        >>> state = PokerState()
        >>> state.initialize_game(["Alice", "Bob"], 1000)
        >>> state.start_new_hand()
        >>> obs = state.create_player_observation("player_0")
    """
    # Standard agent state fields
    messages: List[BaseMessage] = Field(default_factory=list)
    current_step: int = 0
    max_steps: int = 1000
    error: Optional[str] = None
    memory: Dict[str, Any] = Field(default_factory=dict)
    
    # Poker-specific state
    game: PokerGameState = Field(default_factory=PokerGameState)
    waiting_for_player: Optional[str] = None
    game_log: List[str] = Field(default_factory=list)
    current_decision: Optional[AgentDecision] = None
    
    def initialize_game(self, player_names: List[str], starting_chips: int = 1000):
        """Initialize a new poker game with the given players.
        
        Creates a new game state with the specified players, assigning
        IDs, positions, and starting chip stacks.

        Args:
            player_names (List[str]): Names of players to add
            starting_chips (int, optional): Initial chips per player. Defaults to 1000.

        Example:
            >>> state.initialize_game(["Alice", "Bob", "Charlie"], 2000)
        """
        self.game = PokerGameState(
            players=[
                Player(id=f"player_{i}", name=name, chips=starting_chips, position=i)
                for i, name in enumerate(player_names)
            ],
            active_players=[f"player_{i}" for i in range(len(player_names))],
            phase=GamePhase.SETUP,
            pots=[Pot(eligible_players=[f"player_{i}" for i in range(len(player_names))])]
        )
        
        self.initialize_deck()
        self.log_event("Game initialized with players: " + ", ".join(player_names))
    
    def initialize_deck(self):
        """Create and shuffle a new deck of cards.
        
        Creates a standard 52-card deck and performs a random shuffle.
        Updates the game state with the new deck.
        """
        deck = []
        for suit in Suit:
            for value in CardValue:
                deck.append(Card(suit=suit, value=value))
        
        random.shuffle(deck)
        self.game.deck = deck
        self.log_event("Deck shuffled")
    
    def deal_hands(self):
        """Deal two cards to each active player.
        
        Deals hole cards to all active players with chips. Skips inactive
        or busted players. Logs an error if there aren't enough cards.
        """
        if len(self.game.deck) < len(self.game.players) * 2:
            self.log_event("Not enough cards in deck to deal hands")
            return
        
        for player in self.game.players:
            if player.is_active and player.chips > 0:
                player.hand = Hand(cards=[
                    self.game.deck.pop(),
                    self.game.deck.pop()
                ])
        
        self.log_event("Hands dealt to all players")
    
    def post_blinds(self):
        """Post small and big blinds.
        
        Forces the two players after the dealer to post the small and big
        blinds. Updates player chips, pot size, and current bet amount.
        Sets minimum raise to the big blind size.

        Raises:
            Sets self.error if there aren't enough players or if blind
            positions can't be determined.
        """
        if len(self.game.players) < 2:
            self.error = "Not enough players to post blinds"
            return
        
        # Find small blind and big blind positions
        sb_pos = (self.game.dealer_position + 1) % len(self.game.players)
        bb_pos = (self.game.dealer_position + 2) % len(self.game.players)
        
        # Get players
        sb_player = next((p for p in self.game.players if p.position == sb_pos), None)
        bb_player = next((p for p in self.game.players if p.position == bb_pos), None)
        
        if not sb_player or not bb_player:
            self.error = "Cannot find small blind or big blind players"
            return
        
        # Post small blind
        sb_amount = min(self.game.small_blind, sb_player.chips)
        self._place_bet(sb_player, sb_amount)
        self.log_event(f"{sb_player.name} posts small blind of ${sb_amount}")
        
        # Post big blind
        bb_amount = min(self.game.big_blind, bb_player.chips)
        self._place_bet(bb_player, bb_amount)
        self.log_event(f"{bb_player.name} posts big blind of ${bb_amount}")
        
        # Set current bet to big blind
        self.game.current_bet = bb_amount
        self.game.min_raise = bb_amount
    
    def deal_community_cards(self, count: int = 3):
        """Deal community cards to the board.
        
        Deals the specified number of cards from the deck to the community
        cards area. Used for flop (3 cards), turn (1 card), and river (1 card).
        Logs the dealt cards with appropriate phase name.

        Args:
            count (int, optional): Number of cards to deal. Defaults to 3 for flop.

        Raises:
            Sets self.error if there aren't enough cards in the deck.
        """
        if len(self.game.deck) < count:
            self.error = "Not enough cards in deck"
            return
        
        for _ in range(count):
            self.game.community_cards.append(self.game.deck.pop())
        
        cards_dealt = self.game.community_cards[-count:]
        cards_str = ", ".join(str(card) for card in cards_dealt)
        
        if count == 3:
            self.log_event(f"Flop: {cards_str}")
        elif count == 1 and len(self.game.community_cards) == 4:
            self.log_event(f"Turn: {cards_str}")
        elif count == 1 and len(self.game.community_cards) == 5:
            self.log_event(f"River: {cards_str}")
    
    def start_new_hand(self):
        """Start a new hand of poker.
        
        Resets all necessary state for a new hand:
            - Rotates dealer position
            - Resets player hands and bets
            - Clears community cards and pots
            - Initializes new deck and deals cards
            - Posts blinds
            - Sets first player to act (UTG)

        The game progresses through these phases:
            1. Setup (reset state)
            2. Deal hole cards
            3. Post blinds
            4. Start preflop betting
        """
        # Rotate dealer position
        self.game.dealer_position = (self.game.dealer_position + 1) % len(self.game.players)
        
        # Reset player states
        for player in self.game.players:
            player.hand = Hand()
            player.is_active = player.chips > 0
            player.is_all_in = False
            player.current_bet = 0
            player.total_bet = 0
        
        # Reset game state
        self.game.active_players = [p.id for p in self.game.players if p.is_active]
        self.game.community_cards = []
        self.game.phase = GamePhase.SETUP
        self.game.pots = [Pot(eligible_players=self.game.active_players)]
        self.game.current_bet = 0
        self.game.action_history = []
        self.game.last_aggressor = None
        self.game.hand_rankings = {}
        self.game.winners = []
        self.game.round_complete = False
        
        # Initialize new hand
        self.initialize_deck()
        self.deal_hands()
        self.post_blinds()
        
        # Set current player to first to act preflop (UTG - under the gun)
        self.game.current_player_idx = (self.game.dealer_position + 3) % len(self.game.players)
        self.game.phase = GamePhase.PREFLOP
        
        self.log_event(f"New hand started. Dealer: Player {self.game.dealer_position}")
    
    def _place_bet(self, player: Player, amount: int) -> int:
        """Place a bet for a player.
        
        Internal helper method to handle bet placement, including:
            - Updating player chips and bet amounts
            - Adding to pot
            - Checking for all-in
            - Creating side pots if needed

        Args:
            player (Player): Player placing the bet
            amount (int): Amount to bet

        Returns:
            int: Actual amount bet (may be less if player can't cover)

        Side Effects:
            - Updates player chips and bet amounts
            - May create side pots if player goes all-in
        """
        actual_amount = min(amount, player.chips)
        player.chips -= actual_amount
        player.current_bet += actual_amount
        player.total_bet += actual_amount
        
        # Update main pot
        self.game.pots[0].amount += actual_amount
        
        # Check if player is all-in
        if player.chips == 0:
            player.is_all_in = True
            self.log_event(f"{player.name} is all-in!")
            self._create_side_pots_if_needed()
        
        return actual_amount
    
    def _create_side_pots_if_needed(self):
        """Create side pots when players are all-in.
        
        Internal helper method to handle side pot creation when one or more
        players are all-in with different amounts. Ensures fair pot distribution
        when players can't match bets.

        Side Effects:
            - Creates new pots based on all-in amounts
            - Updates pot eligibility for each player
            - Redistributes chips between pots
        """
        all_in_players = sorted(
            [p for p in self.game.players if p.is_all_in and p.is_active],
            key=lambda p: p.total_bet
        )
        
        if not all_in_players:
            return
        
        # Reset pots
        current_bets = {p.id: p.total_bet for p in self.game.players if p.is_active}
        total_pot = sum(current_bets.values())
        
        new_pots = []
        remaining_players = [p.id for p in self.game.players if p.is_active]
        
        # Create pots for each all-in amount
        previous_bet = 0
        for all_in_player in all_in_players:
            bet_diff = all_in_player.total_bet - previous_bet
            if bet_diff > 0:
                pot_amount = bet_diff * len(remaining_players)
                new_pots.append(Pot(
                    amount=pot_amount,
                    eligible_players=remaining_players.copy()
                ))
                
                # For the next pot, this player is no longer eligible
                remaining_players.remove(all_in_player.id)
                
                # Update the previous bet level
                previous_bet = all_in_player.total_bet
        
        # Create the main pot for non-all-in players
        if remaining_players:
            remaining_pot = total_pot - sum(pot.amount for pot in new_pots)
            if remaining_pot > 0:
                new_pots.append(Pot(
                    amount=remaining_pot,
                    eligible_players=remaining_players
                ))
        
        # Replace existing pots
        self.game.pots = new_pots
    
    def handle_player_action(self, player_id: str, decision: AgentDecision):
        """Process a player's action in the game.
        
        Handles all possible player actions (fold, check, call, bet, raise, all-in),
        including validation, bet placement, and game state updates.

        Args:
            player_id (str): ID of player taking action
            decision (AgentDecision): Player's chosen action and amount

        Side Effects:
            - Updates player state (chips, active status)
            - Updates game state (pot, current bet, etc.)
            - Advances to next player
            - May complete betting round
            - May end hand if only one player remains

        Raises:
            Sets self.error for invalid actions:
                - Player not found
                - Player not active
                - Invalid action for current state
                - Invalid bet/raise amount
        """
        player = next((p for p in self.game.players if p.id == player_id), None)
        if not player:
            self.error = f"Player {player_id} not found"
            return
        
        if not player.is_active:
            self.error = f"Player {player_id} is not active"
            return
        
        # Record the action
        action_record = ActionRecord(
            player_id=player_id,
            action=decision.action,
            amount=decision.amount,
            phase=self.game.phase
        )
        self.game.action_history.append(action_record)
        
        # Process based on action type
        if decision.action == PlayerAction.FOLD:
            player.is_active = False
            self.game.active_players.remove(player_id)
            self.log_event(f"{player.name} folds")
            
        elif decision.action == PlayerAction.CHECK:
            if self.game.current_bet > player.current_bet:
                self.error = f"Player {player_id} cannot check, must call {self.game.current_bet - player.current_bet}"
                return
            self.log_event(f"{player.name} checks")
            
        elif decision.action == PlayerAction.CALL:
            call_amount = self.game.current_bet - player.current_bet
            if call_amount <= 0:
                self.error = f"Player {player_id} has nothing to call"
                return
                
            actual_bet = self._place_bet(player, call_amount)
            self.log_event(f"{player.name} calls ${actual_bet}")
            
        elif decision.action == PlayerAction.BET:
            if self.game.current_bet > 0:
                self.error = f"Cannot bet when there is already a bet of {self.game.current_bet}"
                return
                
            if decision.amount < self.game.big_blind:
                decision.amount = self.game.big_blind
                
            actual_bet = self._place_bet(player, decision.amount)
            self.game.current_bet = actual_bet
            self.game.min_raise = actual_bet
            self.game.last_aggressor = player_id
            self.log_event(f"{player.name} bets ${actual_bet}")
            
        elif decision.action == PlayerAction.RAISE:
            if self.game.current_bet == 0:
                self.error = f"Cannot raise when there is no bet, use BET instead"
                return
                
            min_raise_to = self.game.current_bet + self.game.min_raise
            if decision.amount < min_raise_to:
                decision.amount = min_raise_to
                
            # Calculate the actual raise amount
            raise_amount = decision.amount - player.current_bet
            actual_bet = self._place_bet(player, raise_amount)
            
            if player.current_bet > self.game.current_bet:
                self.game.min_raise = player.current_bet - self.game.current_bet
                self.game.current_bet = player.current_bet
                self.game.last_aggressor = player_id
                self.log_event(f"{player.name} raises to ${player.current_bet}")
            else:
                # This happens if player doesn't have enough chips to make the min raise
                self.log_event(f"{player.name} calls ${actual_bet} (not enough for min raise)")
                
        elif decision.action == PlayerAction.ALL_IN:
            if player.chips == 0:
                self.error = f"Player {player_id} is already all-in"
                return
                
            all_in_amount = player.chips
            actual_bet = self._place_bet(player, all_in_amount)
            
            # Determine if this is a raise or just a call
            if player.current_bet > self.game.current_bet:
                raise_amount = player.current_bet - self.game.current_bet
                if raise_amount >= self.game.min_raise:
                    self.game.min_raise = raise_amount
                self.game.current_bet = player.current_bet
                self.game.last_aggressor = player_id
                self.log_event(f"{player.name} goes all-in for ${actual_bet}!")
            else:
                self.log_event(f"{player.name} calls all-in for ${actual_bet}")
        
        # Add reasoning to log if provided
        if decision.reasoning:
            self.log_event(f"{player.name}'s reasoning: {decision.reasoning}")
            
        # Move to next player
        self._advance_to_next_player()
        
        # Check if round is complete
        self._check_round_completion()
        
        # Check if hand is over due to only one player remaining
        if len(self.game.active_players) == 1:
            self._handle_single_player_win()
    
    def _advance_to_next_player(self):
        """Move to the next active player in the game.
        
        Internal helper method to advance the current player index to the
        next player who can act (active and not all-in). If no such player
        is found after a full circle, marks the round as complete.

        Side Effects:
            - Updates current_player_idx
            - May mark round as complete
        """
        start_idx = self.game.current_player_idx
        
        while True:
            self.game.current_player_idx = (self.game.current_player_idx + 1) % len(self.game.players)
            
            # Skip inactive players
            current_player = self.game.players[self.game.current_player_idx]
            if current_player.is_active and not current_player.is_all_in:
                break
                
            # If we've gone all the way around without finding an active player
            if self.game.current_player_idx == start_idx:
                self.game.round_complete = True
                break
    
    def _check_round_completion(self) -> bool:
        """Check if the current betting round is complete.
        
        Internal helper method to determine if the current betting round
        should end. A round is complete when:
            - Only one player remains active
            - All active players have bet the same amount
            - All players have acted after the last aggressor

        Returns:
            bool: True if round is complete, False otherwise

        Side Effects:
            - May mark round as complete
        """
        if self.game.round_complete:
            return True
            
        # If only one player remains active, the round is complete
        if len([p for p in self.game.players if p.is_active and not p.is_all_in]) <= 1:
            self.game.round_complete = True
            return True
            
        # If all active players have bet the same amount (or are all-in)
        active_non_allin_players = [p for p in self.game.players if p.is_active and not p.is_all_in]
        if all(p.current_bet == self.game.current_bet for p in active_non_allin_players):
            last_aggressor = self.game.last_aggressor
            
            # If there's no last aggressor, or if the current player index has reached the last aggressor
            if not last_aggressor or self._player_has_acted_after_last_aggressor():
                self.game.round_complete = True
                return True
                
        return False
    
    def _player_has_acted_after_last_aggressor(self) -> bool:
        """Check if all players have acted after the last aggressive action.
        
        Internal helper method to determine if betting can end by checking if
        all players have had a chance to act after the last bet/raise.

        Returns:
            bool: True if all players have acted, False otherwise
        """
        if not self.game.last_aggressor:
            return True
            
        last_aggressor_idx = next(
            (i for i, p in enumerate(self.game.players) if p.id == self.game.last_aggressor), 
            -1
        )
        
        if last_aggressor_idx == -1:
            return True
            
        # The player who would act next
        next_idx = (self.game.current_player_idx + 1) % len(self.game.players)
        
        # If the next player is the one who made the last aggressive action,
        # then all players have had a chance to act
        return next_idx == last_aggressor_idx
    
    def advance_game_phase(self):
        """Move the game to the next phase if current phase is complete.
        
        Handles progression through game phases:
            1. Preflop -> Flop (deal 3 cards)
            2. Flop -> Turn (deal 1 card)
            3. Turn -> River (deal 1 card)
            4. River -> Showdown (evaluate hands)

        For each phase transition:
            - Resets betting amounts
            - Deals appropriate community cards
            - Sets first player to act
            - Updates game phase

        Side Effects:
            - Updates game phase
            - Deals community cards
            - Resets betting state
            - May end the hand
        """
        if not self.game.round_complete:
            return
            
        # Reset for next betting round
        for player in self.game.players:
            player.current_bet = 0
        self.game.current_bet = 0
        self.game.round_complete = False
        self.game.last_aggressor = None
        
        # Set first to act (left of dealer, except preflop)
        self.game.current_player_idx = (self.game.dealer_position + 1) % len(self.game.players)
        while (not self.game.players[self.game.current_player_idx].is_active or 
               self.game.players[self.game.current_player_idx].is_all_in):
            self.game.current_player_idx = (self.game.current_player_idx + 1) % len(self.game.players)
        
        # Advance the game phase
        if self.game.phase == GamePhase.PREFLOP:
            self.game.phase = GamePhase.FLOP
            self.deal_community_cards(3)
            
        elif self.game.phase == GamePhase.FLOP:
            self.game.phase = GamePhase.TURN
            self.deal_community_cards(1)
            
        elif self.game.phase == GamePhase.TURN:
            self.game.phase = GamePhase.RIVER
            self.deal_community_cards(1)
            
        elif self.game.phase == GamePhase.RIVER:
            self.game.phase = GamePhase.SHOWDOWN
            self._handle_showdown()
            
        self.log_event(f"Moving to {self.game.phase.value} phase")
    
    def _handle_single_player_win(self):
        """Handle case where only one player remains active.
        
        Internal helper method to process an early hand completion when all
        other players have folded. Awards all pots to the remaining player
        and ends the hand.

        Side Effects:
            - Awards pots to winner
            - Updates game phase
            - Logs result
        """
        winner_id = self.game.active_players[0]
        winner = next(p for p in self.game.players if p.id == winner_id)
        
        # Award all pots to the winner
        total_winnings = sum(pot.amount for pot in self.game.pots)
        winner.chips += total_winnings
        
        self.game.winners = [winner_id]
        self.game.phase = GamePhase.GAME_OVER
        
        self.log_event(f"{winner.name} wins ${total_winnings} as the last player standing!")
    
    def _handle_showdown(self):
        """Handle the showdown phase of the game.
        
        Internal helper method to process the showdown when multiple players
        remain after all betting rounds. Includes:
            - Evaluating all active players' hands
            - Determining winners for each pot
            - Distributing chips appropriately
            - Handling split pots

        Side Effects:
            - Evaluates hands
            - Awards pots to winners
            - Updates game phase
            - Logs results
        """
        # Evaluate all active hands
        for player in self.game.players:
            if player.is_active:
                # Combine hole cards and community cards
                all_cards = player.hand.cards + self.game.community_cards
                # Evaluate the best 5-card hand
                hand_ranking = self._evaluate_hand(all_cards)
                self.game.hand_rankings[player.id] = HandRanking(
                    player_id=player.id,
                    rank=hand_ranking[0],
                    high_cards=hand_ranking[1],
                    description=hand_ranking[2]
                )
                self.log_event(f"{player.name} shows: {player.hand} - {hand_ranking[2]}")
        
        # Determine winners for each pot
        pot_winners = {}
        
        for pot_idx, pot in enumerate(self.game.pots):
            eligible_rankings = {
                player_id: ranking 
                for player_id, ranking in self.game.hand_rankings.items()
                if player_id in pot.eligible_players
            }
            
            if not eligible_rankings:
                self.log_event(f"No eligible players for pot {pot_idx}")
                continue
            
            # Find the best hand ranking among eligible players
            best_rank = max(ranking.rank.value for ranking in eligible_rankings.values())
            
            # Get all players with the best rank
            best_players = [
                player_id for player_id, ranking in eligible_rankings.items()
                if ranking.rank.value == best_rank
            ]
            
            # If there's a tie, use high cards to break it
            if len(best_players) > 1:
                best_high_cards = None
                tied_winners = []
                
                for player_id in best_players:
                    ranking = eligible_rankings[player_id]
                    if best_high_cards is None:
                        best_high_cards = ranking.high_cards
                        tied_winners = [player_id]
                    else:
                        # Compare high cards from highest to lowest
                        for i in range(min(len(best_high_cards), len(ranking.high_cards))):
                            if ranking.high_cards[i] > best_high_cards[i]:
                                best_high_cards = ranking.high_cards
                                tied_winners = [player_id]
                                break
                            elif ranking.high_cards[i] < best_high_cards[i]:
                                break
                            elif i == min(len(best_high_cards), len(ranking.high_cards)) - 1:
                                # If we get here, it's a true tie
                                tied_winners.append(player_id)
                
                best_players = tied_winners
            
            # Split the pot among winners
            pot_winners[pot_idx] = best_players
            split_amount = pot.amount // len(best_players)
            remainder = pot.amount % len(best_players)
            
            for player_id in best_players:
                player = next(p for p in self.game.players if p.id == player_id)
                # Give this player their share plus any remainder if they're first
                winnings = split_amount + (remainder if player_id == best_players[0] else 0)
                player.chips += winnings
                
                self.log_event(f"{player.name} wins ${winnings} with {eligible_rankings[player_id].description}")
        
        # Record all winners
        all_winners = set()
        for winners in pot_winners.values():
            all_winners.update(winners)
        
        self.game.winners = list(all_winners)
        self.game.phase = GamePhase.GAME_OVER
    
    
    def _evaluate_hand(self, cards: List[Card]) -> Tuple[HandRank, List[int], str]:
        """Evaluate the best 5-card poker hand from given cards.
        
        Internal helper method to determine the best possible poker hand
        from a set of cards (hole cards + community cards). Handles all
        standard poker hand rankings and tiebreakers.

        Args:
            cards (List[Card]): List of cards to evaluate (usually 7 cards)

        Returns:
            Tuple[HandRank, List[int], str]: A tuple containing:
                - HandRank: The type of hand (pair, flush, etc.)
                - List[int]: High card values for tiebreaking
                - str: Human-readable description of the hand

        Example:
            >>> cards = [
            ...     Card(suit=Suit.HEARTS, value=CardValue.ACE),
            ...     Card(suit=Suit.HEARTS, value=CardValue.KING),
            ...     Card(suit=Suit.HEARTS, value=CardValue.QUEEN),
            ...     Card(suit=Suit.HEARTS, value=CardValue.JACK),
            ...     Card(suit=Suit.HEARTS, value=CardValue.TEN)
            ... ]
            >>> rank, high_cards, desc = _evaluate_hand(cards)
            >>> print(desc)  # Shows "Royal Flush"
        """
        # Sort cards by value, highest first
        sorted_cards = sorted(cards, key=lambda card: card.numeric_value, reverse=True)
        
        # Count occurrences of each value
        value_counts = {}
        for card in sorted_cards:
            if card.value in value_counts:
                value_counts[card.value] += 1
            else:
                value_counts[card.value] = 1
        
        # Count occurrences of each suit
        suit_counts = {}
        for card in sorted_cards:
            if card.suit in suit_counts:
                suit_counts[card.suit] += 1
            else:
                suit_counts[card.suit] = 1
        
        # Check for flush (5+ cards of the same suit)
        flush_suit = None
        for suit, count in suit_counts.items():
            if count >= 5:
                flush_suit = suit
                break
        
        # Get flush cards if there's a flush
        flush_cards = None
        if flush_suit:
            flush_cards = [card for card in sorted_cards if card.suit == flush_suit][:5]
        
        # Check for straight (5+ consecutive values)
        straight_high_card = None
        
        # Handle special case: A-5 straight (Ace counts as 1)
        if (any(card.value == CardValue.ACE for card in sorted_cards) and
            any(card.value == CardValue.FIVE for card in sorted_cards) and
            any(card.value == CardValue.FOUR for card in sorted_cards) and
            any(card.value == CardValue.THREE for card in sorted_cards) and
            any(card.value == CardValue.TWO for card in sorted_cards)):
            straight_high_card = 5  # 5-high straight
        else:
            # Check normal straights
            unique_values = sorted(set(card.numeric_value for card in sorted_cards), reverse=True)
            for i in range(len(unique_values) - 4):
                if unique_values[i] - unique_values[i + 4] == 4:  # 5 consecutive values
                    straight_high_card = unique_values[i]
                    break
        
        # 1. Royal Flush: A-K-Q-J-10 of same suit
        if (flush_cards and 
            flush_cards[0].value == CardValue.ACE and
            flush_cards[1].value == CardValue.KING and
            flush_cards[2].value == CardValue.QUEEN and
            flush_cards[3].value == CardValue.JACK and
            flush_cards[4].value == CardValue.TEN):
            return (HandRank.ROYAL_FLUSH, [14], "Royal Flush")
        
        # 2. Straight Flush: 5 consecutive cards of the same suit
        if flush_cards and straight_high_card:
            # Check if the flush includes a straight
            flush_values = sorted(set(card.numeric_value for card in flush_cards), reverse=True)
            
            # Handle A-5 straight flush
            if (any(card.value == CardValue.ACE for card in flush_cards) and
                any(card.value == CardValue.FIVE for card in flush_cards) and
                any(card.value == CardValue.FOUR for card in flush_cards) and
                any(card.value == CardValue.THREE for card in flush_cards) and
                any(card.value == CardValue.TWO for card in flush_cards)):
                return (HandRank.STRAIGHT_FLUSH, [5], "Five-high Straight Flush")
            
            # Check normal straight flush
            for i in range(len(flush_values) - 4):
                if flush_values[i] - flush_values[i + 4] == 4:
                    # Get the name of the high card from its numeric value
                    high_card_name = next(cv.name for cv in CardValue if cv.value == flush_values[i])
                    return (HandRank.STRAIGHT_FLUSH, [flush_values[i]], 
                        f"{high_card_name.capitalize()}-high Straight Flush")
        
        # 3. Four of a Kind: 4 cards of the same value
        quads = [value for value, count in value_counts.items() if count == 4]
        if quads:
            # Get the highest quad value
            quad_value = max(quads, key=lambda v: v.value)
            # Get the highest kicker
            kicker = next(card.numeric_value for card in sorted_cards 
                        if card.value != quad_value)
            return (HandRank.FOUR_OF_A_KIND, [quad_value.value, kicker],
                f"Four of a Kind, {quad_value.name}s")
        
        # 4. Full House: 3 cards of one value, 2 of another
        trips = [value for value, count in value_counts.items() if count == 3]
        pairs = [value for value, count in value_counts.items() if count == 2]
        
        if trips and pairs:
            # Get highest trip and pair
            best_trip = max(trips, key=lambda v: v.value)
            best_pair = max(pairs, key=lambda v: v.value)
            return (HandRank.FULL_HOUSE, 
                [best_trip.value, best_pair.value],
                f"Full House, {best_trip.name}s over {best_pair.name}s")
        elif len(trips) >= 2:  # Two sets of trips = full house with the best two
            # Sort trips by value
            sorted_trips = sorted(trips, key=lambda v: v.value, reverse=True)
            return (HandRank.FULL_HOUSE,
                [sorted_trips[0].value, sorted_trips[1].value],
                f"Full House, {sorted_trips[0].name}s over {sorted_trips[1].name}s")
        
        # 5. Flush: 5 cards of the same suit
        if flush_cards:
            high_cards = [card.numeric_value for card in flush_cards[:5]]
            # Get the name of the high card
            high_card_name = next(cv.name for cv in CardValue if cv.value == high_cards[0])
            return (HandRank.FLUSH, high_cards,
                f"{high_card_name.capitalize()}-high Flush")
        
        # 6. Straight: 5 consecutive values
        if straight_high_card:
            # Get the name of the high card
            high_card_name = next(cv.name for cv in CardValue if cv.value == straight_high_card)
            return (HandRank.STRAIGHT, [straight_high_card],
                f"{high_card_name.capitalize()}-high Straight")
        
        # 7. Three of a Kind: 3 cards of the same value
        if trips:
            best_trip = max(trips, key=lambda v: v.value)
            kickers = [card.numeric_value for card in sorted_cards 
                    if card.value != best_trip][:2]
            return (HandRank.THREE_OF_A_KIND, [best_trip.value] + kickers,
                f"Three of a Kind, {best_trip.name}s")
        
        # 8. Two Pair: 2 cards of one value, 2 of another
        if len(pairs) >= 2:
            # Sort pairs by value
            sorted_pairs = sorted(pairs, key=lambda v: v.value, reverse=True)
            best_pair = sorted_pairs[0]
            second_pair = sorted_pairs[1]
            # Find the highest kicker that isn't part of either pair
            kicker = next(card.numeric_value for card in sorted_cards 
                        if card.value != best_pair and card.value != second_pair)
            return (HandRank.TWO_PAIR, 
                [best_pair.value, second_pair.value, kicker],
                f"Two Pair, {best_pair.name}s and {second_pair.name}s")
        
        # 9. One Pair: 2 cards of the same value
        if pairs:
            best_pair = max(pairs, key=lambda v: v.value)
            kickers = [card.numeric_value for card in sorted_cards 
                    if card.value != best_pair][:3]
            return (HandRank.PAIR, [best_pair.value] + kickers,
                f"Pair of {best_pair.name}s")
        
        # 10. High Card: Highest value card
        high_cards = [card.numeric_value for card in sorted_cards[:5]]
        # Get the name of the high card
        high_card_name = next(cv.name for cv in CardValue if cv.value == high_cards[0])
        return (HandRank.HIGH_CARD, high_cards,
            f"{high_card_name.capitalize()}-high")

    def create_player_observation(self, player_id: str) -> PlayerObservation:
        """Create an observation object for a player.
        
        Generates a view of the game state from a specific player's perspective,
        hiding information they shouldn't have access to (e.g., other players'
        hole cards).

        Args:
            player_id (str): ID of player to create observation for

        Returns:
            PlayerObservation: Object containing all information visible to player

        Raises:
            ValueError: If player_id is not found

        Example:
            >>> obs = state.create_player_observation("player_0")
            >>> print(obs.hand)  # Shows player's hole cards
            >>> print(obs.community_cards)  # Shows shared cards
        """
        player = next((p for p in self.game.players if p.id == player_id), None)
        if not player:
            raise ValueError(f"Player {player_id} not found")
        
        # Position name mapping
        position_names = {
            0: "Dealer",
            1: "Small Blind",
            2: "Big Blind",
        }
        
        # For positions beyond the blinds
        for i in range(3, len(self.game.players)):
            if i == 3:
                position_names[i] = "UTG"  # Under the Gun
            elif i == len(self.game.players) - 1:
                position_names[i] = "Cutoff"
            else:
                position_names[i] = f"Middle Position {i-2}"
        
        position_name = position_names.get(player.position, f"Position {player.position}")
        
        # Create visible players list (excluding hole cards of others)
        visible_players = []
        for p in self.game.players:
            if p.id == player_id:
                continue  # Skip self in the visible players list
                
            visible_players.append({
                "id": p.id,
                "name": p.name,
                "chips": p.chips,
                "position": p.position,
                "position_name": position_names.get(p.position, f"Position {p.position}"),
                "is_active": p.is_active,
                "is_all_in": p.is_all_in,
                "current_bet": p.current_bet,
                "total_bet": p.total_bet,
            })
        
        # Get recent actions (last 10)
        recent_actions = self.game.action_history[-10:] if self.game.action_history else []
        
        return PlayerObservation(
            player_id=player_id,
            hand=player.hand,
            chips=player.chips,
            position=player.position,
            position_name=position_name,
            community_cards=self.game.community_cards,
            visible_players=visible_players,
            phase=self.game.phase,
            current_bet=self.game.current_bet,
            pot_sizes=[pot.amount for pot in self.game.pots],
            recent_actions=recent_actions,
            min_raise=self.game.min_raise,
            is_active=player.is_active,
            is_current_player=(self.game.players[self.game.current_player_idx].id == player_id)
        )
    
    def log_event(self, message: str):
        """Add a timestamped message to the game log.
        
        Records game events with timestamps for history tracking and debugging.
        Events are both added to the game_log list and sent to the logger.

        Args:
            message (str): Event message to log

        Example:
            >>> state.log_event("Alice raises to $100")
            [14:30:45] Alice raises to $100
        """
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}"
        self.game_log.append(log_entry)
        logger.info(log_entry)