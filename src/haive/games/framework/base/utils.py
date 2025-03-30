"""Utility functions for game agents.

This module provides utility functions for running and managing game agents,
including game execution and state visualization.

Example:
    >>> agent = ChessAgent(config)
    >>> run_game(agent)  # Run a new game
    >>> run_game(agent, initial_state=saved_state)  # Continue from a saved state

Typical usage:
    - Use run_game to execute a complete game with an agent
    - Provide optional initial state to continue from a specific point
    - Monitor game progress through visualization and status updates
"""

from typing import Dict, Any, Optional
#from .agent import GameAgent

def run_game(agent: 'GameAgent', initial_state: Optional[Dict[str, Any]] = None):
    """Run a complete game with the given agent.
    
    This function executes a game from start to finish using the provided agent.
    It handles game initialization, move execution, state visualization, and
    error reporting. The game can optionally start from a provided initial state.
    
    Args:
        agent (GameAgent): The game agent to run the game with.
        initial_state (Optional[Dict[str, Any]], optional): Initial game state.
            If not provided, a new game will be initialized. Defaults to None.
    
    Example:
        >>> agent = ChessAgent(ChessConfig())
        >>> # Start a new game
        >>> run_game(agent)
        >>> 
        >>> # Continue from a saved state
        >>> run_game(agent, saved_state)
    
    Note:
        - The function will print game progress to the console
        - Game visualization depends on the agent's visualize_state method
        - Game history will be saved using the agent's save_state_history method
    """
    # Use provided initial state or create a default one
    game_state = initial_state or {}
    
    # Run the game
    print("\n🎮 Starting Game")
    print("=" * 50)
    
    # Stream through the game steps
    for step in agent.app.stream(
        game_state, 
        config=agent.runnable_config,
        debug=True,
        stream_mode="values"
    ):
        # Visualize the game state
        agent.visualize_state(step)
        
        # Check for errors
        if step.get("error_message"):
            print(f"\n❌ Error: {step['error_message']}")
        
        # Show game status
        if step.get("game_status") != "ongoing":
            print(f"\n🏆 Game Status: {step['game_status'].upper()}")
            if step.get("winner"):
                print(f"🎖️ Winner: {step['winner']}")
    
    # Save game history
    agent.save_state_history()
    print("\n✅ Game Complete!")