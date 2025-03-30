"""
Example usage of the Monopoly agent.

To use the agent in the Monopoly game:
1. Import the setup_monopoly_agent function
2. Call it with the player index you want the agent to control
3. Run the game normally

The agent will automatically make decisions when it's that player's turn.
"""

import pygame
import logging

# Import game modules
from monopoly import player
from monopoly import functions
from monopoly import firstpage
from monopoly import mainboard

# Import agent
from src.haive.games.monopoly.integration import setup_monopoly_agent

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    """Main function for running the Monopoly game with an AI agent."""
    print("Starting Monopoly game with AI agent...")
    
    # Initialize pygame
    pygame.init()
    
    # Setup the display
    display_width = 1430
    display_height = 800
    gameDisplay = pygame.display.set_mode((display_width, display_height))
    pygame.display.set_caption("Monopoly with AI Agent")
    
    # Setup the agent (for player 1)
    agent_integration = setup_monopoly_agent(player_index=1)
    
    # Run the game (mainscreen from mainboard)
    mainboard.mainscreen()
    
    # Quit pygame on exit
    pygame.quit()
    print("Game ended")

if __name__ == "__main__":
    main()