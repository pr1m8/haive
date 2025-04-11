from typing import Dict, Any, Optional
import time
import random

from langgraph.types import Command
from langgraph.graph import END
from src.haive.core.engine.agent.agent import register_agent
from src.haive.games.framework.base import GameAgent
from src.haive.core.graph.GraphBuilder import DynamicGraph
from src.haive.games.cards.bs.config import BullshitAgentConfig
from src.haive.games.cards.bs.state_manager import BullshitStateManager
from src.haive.games.cards.bs.models import (
    #BullshitGameState, 
    PlayerClaimAction, 
    ChallengeAction, 
    Card
)
from src.haive.games.cards.bs.state import BullshitGameState

@register_agent(BullshitAgentConfig)
class BullshitAgent(GameAgent[BullshitAgentConfig]):
    """Multi-player Bullshit (BS) card game agent."""
    
    def __init__(self, config: BullshitAgentConfig=BullshitAgentConfig()):
        """Initialize the Bullshit agent."""
        self.state_manager = BullshitStateManager
        super().__init__(config)
        
        # Track game rounds and other metadata
        self.current_round = 0
        self.challenge_probability = 0.3  # Base probability of challenging
    
    def initialize_game(self, state: Dict[str, Any]) -> Command:
        """
        Initialize a new Bullshit game.
        
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
            goto="player_turn"
        )
    
    def prepare_claim_context(self, state: BullshitGameState) -> Dict[str, Any]:
        """
        Prepare context for a player's claim.
        
        Args:
            state: Current game state
        
        Returns:
            Context dictionary for claim decision
        """
        current_player = state.players[state.current_player_index]
        
        # Prepare hand details
        hand_details = ", ".join(str(card) for card in current_player.hand)
        
        # Prepare player hand sizes
        player_hand_sizes = "\n".join(
            f"{player.name}: {len(player.hand)} cards" 
            for player in state.players
        )
        
        return {
            "hand_details": hand_details,
            "current_pile_value": state.current_claimed_value or "None",
            "pile_size": len(state.current_pile),
            "player_hand_sizes": player_hand_sizes
        }
    
    def prepare_challenge_context(self, state: BullshitGameState) -> Dict[str, Any]:
        """
        Prepare context for a challenge decision.
        
        Args:
            state: Current game state
        
        Returns:
            Context dictionary for challenge decision
        """
        current_player = state.players[state.current_player_index]
        
        # Prepare hand details
        hand_details = ", ".join(str(card) for card in current_player.hand)
        
        # Prepare player hand sizes
        player_hand_sizes = "\n".join(
            f"{player.name}: {len(player.hand)} cards" 
            for player in state.players
        )
        
        return {
            "hand_details": hand_details,
            "last_played_value": state.current_claimed_value or "None",
            "last_played_cards_count": len(state.last_played_cards),
            "player_hand_sizes": player_hand_sizes
        }
    
    def player_turn(self, state: Dict[str, Any]) -> Command:
        """
        Manage a player's turn in the Bullshit game.
        
        Args:
            state: Current game state
        
        Returns:
            Command for next phase
        """
        game_state = BullshitGameState(**state)
        
        # Increment round counter
        self.current_round += 1
        
        # Get claim engine
        claim_engine = self.engines.get("claim_engine")
        if not claim_engine:
            raise ValueError("Claim engine not configured")
        
        # Prepare context for claim
        context = self.prepare_claim_context(game_state)
        
        try:
            # Get player's claim
            player_claim = claim_engine.invoke(context)
            
            # Validate claim 
            if not self.state_manager.validate_claim(game_state, player_claim):
                # If claim seems impossible, modify to be more realistic
                current_player = game_state.players[game_state.current_player_index]
                available_values = list(set(card.value for card in current_player.hand))
                player_claim = PlayerClaimAction(
                    claimed_value=random.choice(available_values),
                    number_of_cards=min(
                        len([c for c in current_player.hand if c.value == player_claim.claimed_value]),
                        player_claim.number_of_cards
                    ),
                    is_truth=player_claim.is_truth,
                    reasoning="Adjusted for available cards"
                )
            
            # Process the claim
            game_state = self.state_manager.process_player_claim(
                game_state, 
                player_claim
            )
        except Exception as e:
            # Fallback claim strategy
            print(f"Error in claim: {e}")
            current_player = game_state.players[game_state.current_player_index]
            fallback_claim = PlayerClaimAction(
                claimed_value=random.choice([card.value for card in current_player.hand]),
                number_of_cards=min(3, len(current_player.hand)),
                is_truth=random.random() > 0.5,
                reasoning="Fallback random claim"
            )
            game_state = self.state_manager.process_player_claim(
                game_state, 
                fallback_claim
            )
        
        # Decide whether to challenge based on game state
        goto = self.decide_challenge(game_state)
        
        # Check if game should end
        if self.current_round >= self.config.max_rounds:
            goto = END
        
        return Command(
            update=game_state.model_dump(), 
            goto=goto
        )
    
    def decide_challenge(self, state: BullshitGameState) -> str:
        """
        Decide whether to challenge the previous player's claim.
        
        Args:
            state: Current game state
        
        Returns:
            Next node in the graph
        """
        # If no cards have been played yet, continue to next turn
        if not state.last_played_cards:
            return "player_turn"
        
        # Get challenge engine
        challenge_engine = self.engines.get("challenge_engine")
        if not challenge_engine:
            print("No challenge engine configured, skipping challenge")
            return "player_turn"
        
        try:
            # Prepare context for challenge decision
            context = self.prepare_challenge_context(state)
            
            # Determine challenge probability based on game state
            challenge_threshold = self.calculate_challenge_probability(state)
            
            # Only attempt challenge if random chance succeeds
            if random.random() < challenge_threshold:
                # Get challenge decision
                challenge = challenge_engine.invoke(context)
                
                # Process the challenge
                state_with_challenge = self.state_manager.process_challenge(
                    state, 
                    challenge
                )
                
                # If game is over, end
                if state_with_challenge.game_status == "game_over":
                    return END
                
                # Reset the game if challenge occurred
                return "player_turn"
        except Exception as e:
            print(f"Error in challenge decision: {e}")
        
        # Default to continuing the game
        return "player_turn"
    
    def calculate_challenge_probability(self, state: BullshitGameState) -> float:
        """
        Calculate the probability of challenging based on game state.
        
        Args:
            state: Current game state
        
        Returns:
            Probability of challenging
        """
        # Base challenge probability
        base_prob = self.challenge_probability
        
        # Increase challenge probability if pile is getting large
        pile_size_factor = min(len(state.current_pile) / 10, 0.3)
        
        # Adjust based on how many cards the current player has
        current_player = state.players[state.current_player_index]
        hand_size_factor = min(1 - (len(current_player.hand) / 52), 0.2)
        
        # Combine factors
        challenge_prob = base_prob + pile_size_factor + hand_size_factor
        
        return min(challenge_prob, 0.8)  # Cap at 80%
    
    def visualize_state(self, state: Dict[str, Any]) -> None:
        """
        Visualize the current game state.
        
        Args:
            state: Current game state
        """
        game_state = BullshitGameState(**state)
        
        print("\n" + "=" * 50)
        print(f"🃏 Round {self.current_round}")
        print(f"📊 Game Status: {game_state.game_status}")
        print("=" * 50)
        
        # Show current pile
        print("\n📚 Current Pile:")
        pile_details = [str(card) for card in game_state.current_pile]
        print(f"Size: {len(pile_details)} cards")
        print(f"Claimed Value: {game_state.current_claimed_value or 'N/A'}")
        
        # Show each player's state
        for i, player in enumerate(game_state.players):
            print(f"\n🃏 Player {i+1}:")
            print(f"  Hand Size: {len(player.hand)} cards")
            print(f"  Played Cards: {len(player.cards_played)} cards")
        
        # Show challenge history
        if game_state.challenge_history:
            print("\n🕵️ Recent Challenges:")
            for challenge in game_state.challenge_history[-3:]:
                print(f"  {challenge['challenger']} challenged {challenge['challenged_player']}")
                print(f"  Result: {challenge['result']}")
        
        time.sleep(1)  # Add a small delay for readability
    
    def setup_workflow(self) -> None:
        """
        Set up the workflow for the Bullshit game.
        """
        gb = DynamicGraph(
            components=[self.config], 
            state_schema=self.config.state_schema
        )
        
        # Define nodes for the game workflow
        gb.add_node("initialize", self.initialize_game)
        gb.add_node("player_turn", self.player_turn)
        
        # Define default edge
        gb.add_edge("initialize", "player_turn")
        
        # Build the graph
        self.graph = gb.build()

def create_bullshit_agent(
    num_players: int = 4,
    max_rounds: int = 20,
    visualize: bool = True
) -> BullshitAgent:
    """
    Create a Bullshit agent with customizable parameters.
    
    Args:
        num_players: Number of players in the game
        max_rounds: Maximum number of rounds to play
        visualize: Whether to visualize the game state
    
    Returns:
        Configured BullshitAgent
    """
    # Create configuration
    config = BullshitAgentConfig(
        name="multi_player_bullshit",
        num_players=num_players,
        max_rounds=max_rounds,
        engines=BullshitAgentConfig.build_bullshit_aug_llms()
    )
    
    # Create and return the agent
    agent = config.build_agent()
    
    # Override visualization if needed
    if visualize:
        agent.visualize_state = agent.visualize_state
    
    return agent

def run_game(
    num_players: int = 4,
    max_rounds: int = 20,
    visualize: bool = True
) -> dict:
    """
    Convenience function to create and run a Bullshit game.
    
    Args:
        num_players: Number of players in the game
        max_rounds: Maximum number of rounds to play
        visualize: Whether to visualize the game state during play
    
    Returns:
        Final game state
    """
    # Create the agent
    agent = create_bullshit_agent(
        num_players=num_players,
        max_rounds=max_rounds,
        visualize=visualize
    )
    
    # Run the game with visualization
    if visualize:
        final_state = {}
        try:
            for step in agent.stream(   
                {}, 
                stream_mode="values", 
                debug=True, 
                #config=agent.runnable_config
            ):
                agent.visualize_state(step)
                final_state = step
                time.sleep(1)  # Add a small delay between steps
        except Exception as e:
            print(f"Error running game: {e}")
            return {}
        
        return final_state
    else:
        # Run without visualization
        return agent.run({})

# Example usage
if __name__ == "__main__":
    # Run a game with default settings
    final_state = run_game(
        num_players=4,
        max_rounds=20,
        visualize=True
    )
    
    # Print final game summary
    print("\n=== Game Summary ===")
    from src.haive.games.cards.bs.state import BullshitGameState
    final_game_state = BullshitGameState(**final_state)
    
    print("Players' Hand Sizes:")
    for i, player in enumerate(final_game_state.players):
        print(f"Player {i+1}: {len(player.hand)} cards")
    
    if final_game_state.winner:
        print(f"\nWinner: {final_game_state.winner}")


#a = BullshitAgent()
#a.run_game(visualize=True)