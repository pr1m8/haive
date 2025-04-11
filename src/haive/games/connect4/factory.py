from src.haive.games.connect4.agent import Connect4Agent
from src.haive.games.connect4.config import Connect4AgentConfig
from src.haive.core.engine.agent.persistence.postgres_config import PostgresCheckpointerConfig
from src.haive.games.connect4.state import Connect4State
import uuid
import time

def run_connect4_game():
    """Run a Connect 4 game using agent.run() with Postgres persistence."""
    
    thread_id = f"connect4_match_{uuid.uuid4().hex[:8]}"
    print(f"🧵 Thread ID: {thread_id}")

    # ✅ Set up persistence
    postgres_config = PostgresCheckpointerConfig(
        db_host="localhost",
        db_port=5432,
        db_name="postgres",
        db_user="postgres",
        db_pass="postgres",
        ssl_mode="disable",
        setup_needed=True,
    )

    # ✅ Agent config
    config = Connect4AgentConfig(
        name="postgres_connect4_game",
        persistence=postgres_config,
        enable_analysis=True,
        runnable_config={
            "configurable": {"thread_id": thread_id},
            "recursion_limit": 100
        }
    )

    # ✅ Instantiate agent
    agent = Connect4Agent(config=config)

    # ✅ Initial game state
    input_state = {
        "board": [[None for _ in range(7)] for _ in range(6)],
        "turn": "red",
        "move_history": [],
        "red_analysis": [],
        "yellow_analysis": [],
        "game_status": "ongoing",
        "winner": None,
        "captured": None,
        "error_message": None
    }

    # ✅ Run the game for a few turns
    state = agent.run(input_state)
    agent.visualize_state(state)
    time.sleep(1)

    while state.get("game_status") == "ongoing":
        state = agent.run({}, thread_id=thread_id)
        agent.visualize_state(state)
        time.sleep(1)

    print("🏁 Game Over!")
    print(f"🎉 Winner: {state.get('winner', 'None')}")

# Run game
if __name__ == "__main__":
    run_connect4_game()
