import random
import copy
from typing import List, Optional, Tuple, Dict, Any

from src.haive.games.cards.blackjack.models import (
    Card, CardSuit, PlayerHand, PlayerState, 
    BlackjackGameState, PlayerAction
)

class BlackjackStateManager:
    """
    Manages the state and core logic for a Blackjack game.
    """
    
    @classmethod
    def create_deck(cls) -> List[Card]:
        """
        Create a full deck of 52 cards.
        """
        suits = list(CardSuit)
        values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        deck = [Card(value=value, suit=suit) for suit in suits for value in values]
        random.shuffle(deck)
        return deck
    
    @classmethod
    def initialize_game(cls, num_players: int = 1) -> BlackjackGameState:
        """
        Initialize a new Blackjack game.
        
        Args:
            num_players: Number of players in the game
            
        Returns:
            Initialized game state
        """
        # Create deck and players
        deck = cls.create_deck()
        players = [
            PlayerState(name=f"Player_{i+1}") 
            for i in range(num_players)
        ]
        
        # Create game state
        game_state = BlackjackGameState(
            players=players,
            deck=deck,
            game_status="betting"
        )
        
        return game_state
    
    @classmethod
    def place_bet(cls, state: BlackjackGameState, player_index: int, bet_amount: float) -> BlackjackGameState:
        """
        Place a bet for a player.
        
        Args:
            state: Current game state
            player_index: Index of the player placing the bet
            bet_amount: Amount to bet
            
        Returns:
            Updated game state
        """
        new_state = copy.deepcopy(state)
        player = new_state.players[player_index]
        
        # Validate bet
        if bet_amount > player.total_chips:
            raise ValueError("Insufficient chips to place bet")
        
        player.current_bet = bet_amount
        player.total_chips -= bet_amount
        
        # Create initial hand
        initial_hand = PlayerHand(bet=bet_amount)
        player.hands = [initial_hand]
        
        return new_state
    
    @classmethod
    def deal_initial_cards(cls, state: BlackjackGameState) -> BlackjackGameState:
        """
        Deal initial cards to players and dealer.
        
        Args:
            state: Current game state
            
        Returns:
            Updated game state with initial cards dealt
        """
        new_state = copy.deepcopy(state)
        
        # Deal two cards to each player
        for player in new_state.players:
            for _ in range(2):
                card = new_state.deck.pop()
                player.hands[0].cards.append(card)
        
        # Deal two cards to dealer
        for _ in range(2):
            card = new_state.deck.pop()
            new_state.dealer_hand.append(card)
        
        # Update game status
        new_state.game_status = "playing"
        new_state.current_player_index = 0
        new_state.current_hand_index = 0
        
        return new_state
    
    @classmethod
    def get_current_player_and_hand(cls, state: BlackjackGameState) -> Tuple[PlayerState, PlayerHand]:
        """
        Get the current active player and their current hand.
        
        Args:
            state: Current game state
            
        Returns:
            Tuple of current player and current hand
        """
        player = state.players[state.current_player_index]
        current_hand = player.hands[state.current_hand_index]
        return player, current_hand
    
    @classmethod
    def process_player_action(
        cls, 
        state: BlackjackGameState, 
        action: PlayerAction
    ) -> BlackjackGameState:
        """
        Process a player's action during their turn.
        
        Args:
            state: Current game state
            action: Player's chosen action
            
        Returns:
            Updated game state
        """
        new_state = copy.deepcopy(state)
        player, current_hand = cls.get_current_player_and_hand(new_state)
        
        # Handle different actions
        if action.action == "hit":
            # Draw a card
            card = new_state.deck.pop()
            current_hand.cards.append(card)
            
            # Check for bust
            if current_hand.is_bust():
                current_hand.is_active = False
        
        elif action.action == "stand":
            # Mark current hand as inactive
            current_hand.is_active = False
        
        elif action.action == "double_down":
            # Validate player has enough chips
            if player.total_chips < current_hand.bet:
                raise ValueError("Insufficient chips to double down")
            
            # Double the bet
            player.total_chips -= current_hand.bet
            current_hand.bet *= 2
            
            # Draw one card and stand
            card = new_state.deck.pop()
            current_hand.cards.append(card)
            current_hand.is_active = False
        
        elif action.action == "split":
            # Validate split is possible
            if len(current_hand.cards) != 2 or current_hand.cards[0].value != current_hand.cards[1].value:
                raise ValueError("Cannot split this hand")
            
            # Validate player has enough chips
            if player.total_chips < current_hand.bet:
                raise ValueError("Insufficient chips to split")
            
            # Create two new hands
            new_hand1 = PlayerHand(
                cards=[current_hand.cards[0]],
                bet=current_hand.bet,
                is_split=True
            )
            new_hand2 = PlayerHand(
                cards=[current_hand.cards[1]],
                bet=current_hand.bet,
                is_split=True
            )
            
            # Update player's state
            player.hands = [new_hand1, new_hand2]
            player.total_chips -= current_hand.bet
            
            # Ensure hands get their own card
            new_hand1.cards.append(new_state.deck.pop())
            new_hand2.cards.append(new_state.deck.pop())
        
        elif action.action == "surrender":
            # Return half the bet
            player.total_chips += current_hand.bet / 2
            current_hand.is_active = False
        
        # Move to next hand or player if current hand is inactive
        cls._advance_turn(new_state)
        
        return new_state
    
    @classmethod
    def _advance_turn(cls, state: BlackjackGameState):
        """
        Advance to the next active hand or player.
        
        Args:
            state: Current game state
        """
        player = state.players[state.current_player_index]
        
        # Move to next hand for current player
        state.current_hand_index += 1
        
        # If no more hands for this player, move to next player
        while state.current_hand_index >= len(player.hands):
            # Move to next player
            state.current_player_index += 1
            state.current_hand_index = 0
            
            # If we've gone through all players, move to dealer's turn
            if state.current_player_index >= len(state.players):
                state.game_status = "dealer_turn"
                return
            
            # Update player reference
            player = state.players[state.current_player_index]
    
    @classmethod
    def dealer_turn(cls, state: BlackjackGameState) -> BlackjackGameState:
        """
        Execute dealer's turn according to standard Blackjack rules.
        
        Args:
            state: Current game state
            
        Returns:
            Final game state with results
        """
        new_state = copy.deepcopy(state)
        
        # Dealer hits on 16 or less, stands on 17 or more
        dealer_total = sum(card.point_value() for card in new_state.dealer_hand)
        
        while dealer_total < 17:
            card = new_state.deck.pop()
            new_state.dealer_hand.append(card)
            dealer_total = sum(card.point_value() for card in new_state.dealer_hand)
        
        # Determine winners
        new_state = cls._determine_winners(new_state)
        
        return new_state
    
    @classmethod
    def _determine_winners(cls, state: BlackjackGameState) -> BlackjackGameState:
        """
        Determine winners and distribute chips.
        
        Args:
            state: Current game state
            
        Returns:
            Final game state with results
        """
        dealer_total = sum(card.point_value() for card in state.dealer_hand)
        dealer_bust = dealer_total > 21
        
        for player in state.players:
            for hand in player.hands:
                # Skip inactive hands
                if not hand.is_active:
                    continue
                
                hand_total = hand.total_value()
                
                # Determine outcome
                if hand.is_blackjack():
                    # Blackjack pays 3:2
                    player.total_chips += hand.bet * 2.5
                elif hand_bust := hand.is_bust():
                    # Player busts, loses bet
                    pass
                elif dealer_bust:
                    # Dealer busts, player wins
                    player.total_chips += hand.bet * 2
                elif hand_total > dealer_total:
                    # Player wins
                    player.total_chips += hand.bet * 2
                elif hand_total == dealer_total:
                    # Push (tie), return original bet
                    player.total_chips += hand.bet
                # If dealer total is higher and not bust, player loses
        
        # Mark game as over
        state.game_status = "game_over"
        
        return state
    
    @classmethod
    def reset_game(cls, state: BlackjackGameState) -> BlackjackGameState:
        """
        Reset the game for a new round.
        
        Args:
            state: Current game state
            
        Returns:
            Reset game state
        """
        new_state = cls.initialize_game(len(state.players))
        
        # Preserve players' total chips
        for new_player, old_player in zip(new_state.players, state.players):
            new_player.total_chips = old_player.total_chips
        
        return new_state