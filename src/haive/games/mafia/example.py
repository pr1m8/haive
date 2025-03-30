"""Example implementation and runner for the Mafia game.

This module provides a complete example of how to set up and run a Mafia game,
including:
    - Game configuration and initialization
    - Player setup with role assignment
    - Game execution with visualization
    - Debug logging and error handling
    - Command-line interface for game parameters

Example:
    To run a game from the command line:
    ```bash
    python example.py --players 7 --days 3 --debug
    ```

    To run programmatically:
    ```python
    from mafia.example import run_mafia_game
    run_mafia_game(player_count=7, max_days=3, debug=True)
    ```
"""

import traceback
import time
import logging
from .agent import MafiaAgent
from .config import MafiaAgentConfig, aug_llm_configs
from .models import PlayerRole, GamePhase
from .state import MafiaGameState
from .state_manager import MafiaStateManager

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run_mafia_game(player_count: int = 5, max_days: int = 3, debug: bool = True):
    """Run a complete Mafia game simulation with visualization.
    
    This function sets up and executes a full Mafia game, handling:
        - Player creation and role assignment
        - Game state initialization
        - Turn-based gameplay execution
        - State visualization
        - Game end conditions
    
    Args:
        player_count (int, optional): Total number of players including narrator.
            Must be at least 4 (3 players + narrator). Defaults to 5.
        max_days (int, optional): Maximum number of in-game days before forcing
            game end. Defaults to 3.
        debug (bool, optional): Enable debug mode for detailed logging.
            Defaults to True.
    
    Raises:
        ValueError: If player_count is less than 4.
        Exception: If game setup or execution fails.
    
    Example:
        >>> run_mafia_game(player_count=7, max_days=3)
        🎭 Setting up Mafia Game
        ======================
        Number of players: 7
        Maximum days: 3
        Debug mode: Enabled
        ======================
        ...
    """
    print("\n🎭 Setting up Mafia Game")
    print("=" * 60)
    print(f"Number of players: {player_count}")
    print(f"Maximum days: {max_days}")
    print(f"Debug mode: {'Enabled' if debug else 'Disabled'}")
    print("=" * 60)
    
    try:
        # Print available configs for debugging
        if debug:
            print("\n🔧 Available Engine Configs:")
            for role, engines in aug_llm_configs.items():
                print(f"  {role}: {list(engines.keys())}")
        
        # Create agent config
        config = MafiaAgentConfig.default_config(
            player_count=player_count,
            max_days=max_days
        )
        
        # Set debug mode
        config.debug = debug
        
        # Create the agent
        print("\n🎮 Creating Mafia agent")
        agent = MafiaAgent(config)
        
        # Generate player names
        player_names = [f"Player_{i+1}" for i in range(player_count - 1)]
        player_names.append("Narrator")  # Add narrator as the last player
        
        # Dump engine keys for debugging
        if debug:
            print("\n🔧 Available Engines in Agent:")
            for key, value in agent.engines.items():
                print(f"  {key}: {list(value.keys()) if value else 'None'}")
            
            print("\n🔑 Role to Engine Mapping:")
            for role, engine_key in agent.role_enum_mapping.items():
                print(f"  {role}: {engine_key}")
        
        # Initialize game state
        print("\n🎲 Initializing game state")
        initial_state = MafiaStateManager.initialize(player_names)
        
        if debug:
            print("\n🎲 Game Role Assignment:")
            for player_id, role in initial_state.roles.items():
                print(f"  {player_id}: {role.value}")
        
        # Run the game
        print("\n🎭 Starting Mafia Game")
        print("=" * 60)
        print(f"Players: {', '.join(player_names[:-1])} + Narrator")
        print("=" * 60)
        
        # Track day count to prevent infinite games
        current_day = 0
        
        # Use a try-finally block to ensure proper cleanup
        try:
            # Create a simple thread ID for the session
            import uuid
            thread_id = str(uuid.uuid4())
            
            # Stream the game execution
            for step in agent.app.stream(
                initial_state.dict() if hasattr(initial_state, "dict") else initial_state,
                config={"configurable": {"thread_id": thread_id}},
                debug=debug,
                stream_mode="values"
            ):
                # Visualize the game state
                agent.visualize_state(step)
                
                # Check for game over
                if step.get("game_status") != "ongoing" or step.get("game_phase") == GamePhase.GAME_OVER.value:
                    print(f"\n🏆 Game Status: {step.get('game_status', 'unknown').upper()}")
                    if step.get("winner"):
                        print(f"🎖️ Winner: {step.get('winner').upper()}")
                    break
                
                # Check for errors
                if step.get("error_message"):
                    print(f"\n❌ Error: {step.get('error_message')}")
                    break
                
                # Check day limit to prevent endless games
                if step.get("day_number", 0) > current_day:
                    current_day = step.get("day_number", 0)
                    if current_day > max_days:
                        print(f"\n⏰ Maximum days ({max_days}) reached. Ending game.")
                        break
                
                # Add a slight delay for better readability
                time.sleep(0.3)
        
        finally:
            # Try to save game history
            try:
                print("\n📊 Saving game history")
                agent.save_state_history()
            except Exception as e:
                print(f"Could not save game history: {e}")
    
    except Exception as e:
        print(f"\n❌ SETUP ERROR: {str(e)}")
        traceback.print_exc()  # Print full error traceback
    
    print("\n✅ Game Complete!")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Run a Mafia game simulation")
    parser.add_argument("--players", type=int, default=9, help="Number of players (including narrator)")
    parser.add_argument("--days", type=int, default=3, help="Maximum number of days")
    parser.add_argument("--debug", action="store_true", help="Enable debug logging")
    
    args = parser.parse_args()
    
    # Set logging level based on debug flag
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
    
    # Validate arguments
    if args.players < 4:
        parser.error("Minimum 4 players required (3 players + narrator)")
    
    # Run the game
    run_mafia_game(player_count=args.players, max_days=args.days, debug=args.debug)