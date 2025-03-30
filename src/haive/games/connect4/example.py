import traceback
import time
import logging
import uuid
from src.haive.games.connect4.agent import Connect4Agent
from src.haive.games.connect4.config import Connect4AgentConfig
from src.haive.games.connect4.state_manager import Connect4StateManager

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run_connect4_game(debug: bool = False):
    """
    Run a Connect 4 game with LangGraph-based streaming.
    
    Args:
        debug: Enable debug mode
    """
    print("\n🔴🟡 Setting up Connect4 Game")
    print("=" * 60)
    print(f"Debug mode: {'Enabled' if debug else 'Disabled'}")
    print("=" * 60)
    
    try:
        # ✅ Create agent config
        config = Connect4AgentConfig()
        config.debug = debug

        # ✅ Create the Connect4 agent
        print("\n🎮 Creating Connect4 agent")
        agent = Connect4Agent(config)
        
        # ✅ Initialize game state using StateManager
        print("\n🎲 Initializing game state")
        initial_state = Connect4StateManager.initialize()
        
        # ✅ Debugging: Show the initialized board
        if debug:
            print("\n📋 Initial Game State:")
            agent.visualize_state(initial_state.model_dump())

        # ✅ Assign a unique thread ID for this session
        thread_id = str(uuid.uuid4())

        # ✅ Stream the game execution using LangGraph
        for step in agent.app.stream(
            initial_state.model_dump(),  # Convert state to dictionary
            config={"configurable": {"thread_id": thread_id}},
            debug=debug,
            stream_mode="values"
        ):
            # 🔄 **Visualize the current game state**
            agent.visualize_state(step)

            # ✅ Check if the game is over
            if step.get("game_status") != "ongoing":
                print(f"\n🏆 Game Over! 🎖️ Winner: {step.get('winner', 'No winner')}")
                break
            
            # ✅ Handle errors
            if step.get("error_message"):
                print(f"\n❌ Error: {step.get('error_message')}")
                break

            # ✅ Add a short delay for readability
            time.sleep(0.3)

        # ✅ Save game history
        print("\n📊 Saving game history")
        agent.save_state_history()

    except Exception as e:
        print(f"\n❌ SETUP ERROR: {str(e)}")
        traceback.print_exc()

    print("\n✅ Game Complete!")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Run a Connect 4 game simulation")
    parser.add_argument("--debug", action="store_true", help="Enable debug logging")
    
    args = parser.parse_args()

    # ✅ Set logging level based on debug flag
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)

    # ✅ Run the game
    run_connect4_game(debug=args.debug)
