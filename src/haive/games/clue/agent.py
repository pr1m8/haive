"""
Agent for the Clue game.

This module defines the agent for the Clue game,
which handles game state management and player actions.
"""
from src.haive.games.clue.config import ClueConfig
from src.haive.games.clue.state import ClueState
from src.haive.games.clue.state_manager import ClueStateManager
from src.haive.games.framework.base.agent import GameAgent
from src.haive.core.engine.agent.agent import register_agent
from typing import Dict, Any, List, Optional
import time

@register_agent(ClueConfig)
class ClueAgent(GameAgent[ClueConfig]):
    """Agent for playing Clue.

    This class implements the Clue game agent, which manages the game state
    and player actions in the Clue board game.
    """
    
    def __init__(self, config: ClueConfig = ClueConfig()):
        """Initialize the Clue agent.

        Args:
            config: The configuration for the Clue game.
        """
        self.state_manager = ClueStateManager
        super().__init__(config)
    
    def initialize_game(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Initialize the Clue game.

        Args:
            state: Initial state dictionary (unused here but required for interface).

        Returns:
            Dict[str, Any]: New game state.
        """
        # Initialize the game state
        game_state = self.state_manager.initialize(
            solution=self.config.solution,
            first_player=self.config.first_player,
            max_turns=self.config.max_turns
        )
        
        return game_state.model_dump() if hasattr(game_state, "model_dump") else game_state.dict()
    
    def visualize_state(self, state: Dict[str, Any]) -> None:
        """Visualize the current game state.

        Args:
            state: The state dictionary to visualize.
        """
        if not self.config.visualize:
            return
            
        # Create a ClueState from the dict
        game_state = ClueState(**state)
        
        print("\n" + "=" * 50)
        print(f"🎮 Game: Clue v{self.config.version}")
        print(f"📊 Turn: {game_state.current_turn_number}/{game_state.max_turns}")
        print(f"🎭 Current Player: {game_state.current_player}")
        print(f"📝 Status: {game_state.game_status}")
        
        # Only show solution if game is over
        if game_state.game_status != "ongoing":
            print(f"🔑 Solution: {game_state.solution.suspect}, {game_state.solution.weapon}, {game_state.solution.room}")
        
        print("=" * 50)
        
        # Print the board with all guesses and responses
        if game_state.guesses:
            print("\n" + game_state.board_string)
        else:
            print("\nNo guesses yet.")
        
        # Add a short delay for readability
        time.sleep(0.5)
    
    def run_game(self, visualize: bool = True) -> Dict[str, Any]:
        """Run a complete Clue game with optional visualization.

        Args:
            visualize: Whether to visualize each game state.

        Returns:
            Dict[str, Any]: The final game state.
        """
        # Initialize the game state
        initial_state = self.state_manager.initialize(
            solution=self.config.solution,
            first_player=self.config.first_player,
            max_turns=self.config.max_turns
        )

        # Run the game
        if visualize:
            # Store the last seen state to prevent infinite loops
            last_state = None
            final_state = None
            
            for step in self.stream(initial_state, stream_mode="values", debug=True):
                self.visualize_state(step)
                
                # Create a ClueState to check for game completion
                current_state = ClueState(**step)
                
                # Break the loop if the game is over
                if current_state.game_status != "ongoing":
                    final_state = step
                    break
                
                # Detect if we're stuck in an infinite loop by comparing with last state
                if last_state:
                    # If we've seen the same guesses twice, we might be in a loop
                    if (len(current_state.guesses) == len(last_state.guesses) and 
                        len(current_state.guesses) > 0 and 
                        len(last_state.guesses) > 0):
                        # Check if max turns reached
                        if len(current_state.guesses) >= current_state.max_turns:
                            print("\n⚠️ Maximum turns reached. Ending game.")
                            # Force game to end
                            current_state.game_status = "ongoing_win"
                            final_state = current_state.model_dump()
                            break
                
                # Update last state
                last_state = current_state
            
            return final_state if final_state else step
        else:
            return super().run(initial_state) 