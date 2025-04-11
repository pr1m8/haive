"""
Example usage of the Monopoly agent.

To use the agent in your Monopoly game:
1. Import the setup_monopoly_agent function
2. Call it with the player index you want the agent to control
3. Run the game normally

The agent will automatically make decisions when it's that player's turn.
"""

import logging
import uuid
from typing import Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import the agent setup function
from src.haive.games.monopoly.integration import setup_monopoly_agent

def main():
    """Run the example Monopoly game with AI agent."""
    logger.info("Setting up Monopoly game with AI agent")
    
    # Set up the agent to control player 1
    agent = setup_monopoly_agent(
        player_index=1,  # 0-based index, so this is player 2
        model="gpt-4o",
        temperature=0.7,
        debug=True
    )
    
    # The agent is now integrated with the game
    # When it's player 1's turn, the agent will automatically make decisions
    logger.info("Agent setup complete. Run the game normally.")
    logger.info("The agent will automatically make decisions when it's player 1's turn.")
    
    # Example of manually running a turn (normally not needed as the integration handles this)
    # This is just for demonstration purposes
    def run_manual_turn():
        """Run a manual turn with the agent."""
        # Get current game state (this would normally be handled by the integration)
        game_state = {}  # You would need to extract this from your game
        
        # Analyze strategy
        state = agent.analyze_strategy(game_state)
        
        # Decide actions
        decision_result = agent.decide_turn_actions(state)
        
        # Extract decision
        if hasattr(decision_result, 'update'):
            decision = decision_result.update.get('turn_decision', {})
            logger.info(f"Agent decision: {decision}")
        
        # The integration module would normally handle executing this decision
    
    # Explain how to use the agent
    print("\n" + "="*50)
    print("MONOPOLY AGENT INTEGRATION")
    print("="*50)
    print("\nThe AI agent has been set up to control Player 2.")
    print("When it's Player 2's turn, the agent will automatically:")
    print("1. Analyze the game state")
    print("2. Decide what actions to take")
    print("3. Execute those actions in the game")
    print("\nYou can see the agent's decisions in the log output.")
    print("Just play the game normally, and the agent will handle Player 2's turns.")
    print("="*50 + "\n")

if __name__ == "__main__":
    main()