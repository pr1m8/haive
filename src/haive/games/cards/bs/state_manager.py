import random
import copy
from typing import List, Dict, Any, Optional
from src.haive.games.cards.bs.models import (
    Card, 
    PlayerState, 
    #BullshitGameState, 
    PlayerClaimAction, 
    ChallengeAction
)
from src.haive.games.cards.bs.state import BullshitGameState
class BullshitStateManager:
    """
    Manages the state and core logic for a Bullshit (BS) card game.
    """
    
    @classmethod
    def initialize_game(cls, num_players: int = 4) -> BullshitGameState:
        """
        Initialize a new Bullshit game.
        
        Args:
            num_players: Number of players in the game
            
        Returns:
            Initialized game state
        """
        # Create full deck
        deck = Card.create_deck()
        
        # Distribute cards to players
        players = []
        for i in range(num_players):
            # Calculate how many cards each player should get
            cards_per_player = len(deck) // num_players
            start_index = i * cards_per_player
            end_index = start_index + cards_per_player
            
            # Add any remaining cards to the last player
            if i == num_players - 1:
                player_cards = deck[start_index:]
            else:
                player_cards = deck[start_index:end_index]
            
            players.append(PlayerState(
                name=f"Player_{i+1}",
                hand=player_cards
            ))
        
        # Create game state
        game_state = BullshitGameState(
            players=players,
            game_status="ongoing"
        )
        
        return game_state
    
    @classmethod
    def validate_claim(cls, state: BullshitGameState, claim: PlayerClaimAction) -> bool:
        """
        Validate if a player's claim is potentially true.
        
        Args:
            state: Current game state
            claim: Player's claim about played cards
            
        Returns:
            Whether the claim could be true
        """
        current_player = state.players[state.current_player_index]
        
        # Check if player has enough cards of the claimed value
        cards_of_value = [
            card for card in current_player.hand 
            if card.value == claim.claimed_value
        ]
        
        # If claim matches actual cards, it's potentially true
        return len(cards_of_value) >= claim.number_of_cards
    
    @classmethod
    def process_player_claim(
        cls, 
        state: BullshitGameState, 
        claim: PlayerClaimAction
    ) -> BullshitGameState:
        """
        Process a player's claim and card play.
        
        Args:
            state: Current game state
            claim: Player's claim about played cards
            
        Returns:
            Updated game state
        """
        new_state = copy.deepcopy(state)
        current_player = new_state.players[new_state.current_player_index]
        
        # Select cards to play
        if claim.is_truth:
            # Truthful play: use actual cards of the claimed value
            play_cards = [
                card for card in current_player.hand 
                if card.value == claim.claimed_value
            ][:claim.number_of_cards]
        else:
            # Bluffing: randomly select cards
            play_cards = random.sample(
                current_player.hand, 
                claim.number_of_cards
            )
        
        # Play the cards
        current_player.play_cards(play_cards)
        
        # Update game state
        new_state.last_played_cards = play_cards
        new_state.current_pile.extend(play_cards)
        new_state.current_claimed_value = claim.claimed_value
        
        # Move to next player
        new_state.current_player_index = (new_state.current_player_index + 1) % len(new_state.players)
        
        return new_state
    
    @classmethod
    def process_challenge(
        cls, 
        state: BullshitGameState, 
        challenge: ChallengeAction
    ) -> BullshitGameState:
        """
        Process a challenge to a player's claim.
        
        Args:
            state: Current game state
            challenge: Challenge action
            
        Returns:
            Updated game state
        """
        new_state = copy.deepcopy(state)
        
        # Identify the challenger and the challenged player
        challenger_index = new_state.current_player_index
        challenged_player = new_state.players[challenge.target_player_index]
        
        # Check if the last played cards match the claim
        is_bluff = not all(
            card.value == new_state.current_claimed_value 
            for card in new_state.last_played_cards
        )
        
        # Resolve challenge
        if is_bluff:
            # Bluff detected - challenged player takes the pile
            challenged_player.hand.extend(new_state.current_pile)
            challenge_result = "successful_challenge"
        else:
            # Challenge failed - challenger takes the pile
            new_state.players[challenger_index].hand.extend(new_state.current_pile)
            challenge_result = "failed_challenge"
        
        # Clear the current pile
        new_state.current_pile.clear()
        
        # Record challenge in history
        new_state.challenge_history.append({
            "challenger": new_state.players[challenger_index].name,
            "challenged_player": challenged_player.name,
            "result": challenge_result
        })
        
        # Check for game end
        new_state = cls.check_game_status(new_state)
        
        return new_state
    
    @classmethod
    def check_game_status(cls, state: BullshitGameState) -> BullshitGameState:
        """
        Check if the game has ended.
        
        Args:
            state: Current game state
            
        Returns:
            Updated game state
        """
        new_state = copy.deepcopy(state)
        
        # Check if any player has run out of cards
        for player in new_state.players:
            if len(player.hand) == 0:
                new_state.game_status = "game_over"
                new_state.winner = player.name
                break
        
        return new_state
    
    @classmethod
    def reset_game(cls, state: BullshitGameState) -> BullshitGameState:
        """
        Reset the game for a new round.
        
        Args:
            state: Current game state
            
        Returns:
            Reset game state
        """
        return cls.initialize_game(len(state.players))