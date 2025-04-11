from typing import Optional
import time
from src.haive.games.cards.blackjack.agent import BlackjackAgent
from src.haive.games.cards.blackjack.config import BlackjackAgentConfig

def create_blackjack_agent(
    num_players: int = 2,
    max_rounds: int = 10,
    initial_chips: float = 1000.0,
    visualize: bool = True
) -> BlackjackAgent:
    """
    Create a Blackjack agent with customizable parameters.
    
    Args:
        num_players: Number of players in the game
        max_rounds: Maximum number of rounds to play
        initial_chips: Starting chip amount for each player
        visualize: Whether to visualize the game state during play
    
    Returns:
        Configured BlackjackAgent
    """
    # Create configuration
    config = BlackjackAgentConfig(
        name="multi_player_blackjack",
        num_players=num_players,
        max_rounds=max_rounds,
        initial_chips=initial_chips,
        engines=BlackjackAgentConfig.build_blackjack_aug_llms()
    )
    
    # Create and return the agent
    agent = config.build_agent()
    
    # Override visualization if needed
    if visualize:
        agent.visualize_state = agent.visualize_state
    
    return agent

def run_blackjack_game(
    num_players: int = 2,
    max_rounds: int = 10,
    initial_chips: float = 1000.0,
    visualize: bool = True
) -> dict:
    """
    Convenience function to create and run a Blackjack game.
    
    Args:
        num_players: Number of players in the game
        max_rounds: Maximum number of rounds to play
        initial_chips: Starting chip amount for each player
        visualize: Whether to visualize the game state during play
    
    Returns:
        Final game state
    """
    # Create the agent
    agent = create_blackjack_agent(
        num_players=num_players,
        max_rounds=max_rounds,
        initial_chips=initial_chips,
        visualize=visualize
    )
    
    # Run the game with visualization
    if visualize:
        final_state = {}
        try:
            for step in agent.app.stream(
                {}, 
                stream_mode="values", 
                debug=True, 
                config=agent.runnable_config
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
    final_state = run_blackjack_game(
        num_players=2,
        max_rounds=3,
        visualize=True
    )
    
    # Print final game summary
    print("\n=== Game Summary ===")
    from src.haive.games.cards.blackjack.models import BlackjackGameState
    final_game_state = BlackjackGameState(**final_state)
    
    print("Final Chip Stacks:")
    for i, player in enumerate(final_game_state.players):
        print(f"Player {i+1}: ${player.total_chips:.2f}")
    
    print(f"\nDealer's Final Hand: {' '.join(str(card) for card in final_game_state.dealer_hand)}")
    print(f"Dealer Total: {sum(card.point_value() for card in final_game_state.dealer_hand)}")


# Create and run a game with 4 players, 20 rounds, with visualization
final_state = run_blackjack_game(
    num_players=4,
    max_rounds=20,
    visualize=True
)    