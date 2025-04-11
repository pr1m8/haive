from src.haive.games.chess.agent import ChessAgent
from src.haive.games.chess.config import ChessAgentConfig
from src.haive.core.engine.agent.persistence.postgres_config import PostgresCheckpointerConfig
from typing import Dict, Any
import chess
import json
import uuid

def run_chess_game(agent: ChessAgent, thread_id: str = None):
    """Run a chess game using agent.run() with persistent state tracking."""
    
    # ✅ Generate or use thread_id for persistence continuity
    thread_id = thread_id or f"chess_thread_{uuid.uuid4().hex[:8]}"
    print(f"🧵 Using thread_id: {thread_id}")

    # ✅ Initialize the game state
    initial_state = {
        "board_fens": [chess.Board().fen()],
        "current_player": "white",
        "turn": "white",
        "move_history": [],
        "game_status": "ongoing",
        "white_analysis": [],
        "black_analysis": [],
        "captured_pieces": {"white": [], "black": []},
        "error_message": None
    }

    # 🧠 Run the full agent workflow until END
    final_state = agent.run(initial_state, thread_id=thread_id)

    # 🎯 Display final board and game outcome
    board = chess.Board(final_state["board_fens"][-1])
    print("\n🏁 Final Board:")
    print(board)
    print(f"🧠 Final State: Turn = {final_state['turn'].capitalize()}, Status = {final_state['game_status']}")

    # 📝 Display last few moves
    if final_state.get("move_history"):
        print("\n📜 Move History:")
        for color, move in final_state["move_history"]:
            print(f"   - {color.capitalize()} played {move}")

    # 📊 Display final analyses if any
    if final_state.get("white_analysis"):
        wa: Dict[str, Any] = final_state["white_analysis"][-1]
        print("\n🔍 White's Final Analysis:")
        print(f"   - Score: {wa.get('position_score')}, Attacking: {wa.get('attacking_chances')}, Defense: {wa.get('defensive_needs')}")
        print(f"   - Plans: {', '.join(wa.get('suggested_plans', []))}")

    if final_state.get("black_analysis"):
        ba: Dict[str, Any] = final_state["black_analysis"][-1]
        print("\n🔍 Black's Final Analysis:")
        print(f"   - Score: {ba.get('position_score')}, Attacking: {ba.get('attacking_chances')}, Defense: {ba.get('defensive_needs')}")
        print(f"   - Plans: {', '.join(ba.get('suggested_plans', []))}")

    # ♟️ Show captured pieces
    print("\n🧾 Captured Pieces:")
    print(f"   - White Captured: {', '.join(final_state['captured_pieces']['white']) or 'None'}")
    print(f"   - Black Captured: {', '.join(final_state['captured_pieces']['black']) or 'None'}")

    # 🧬 Save to JSON file if needed
    agent.save_state_history()

# Entry point
if __name__ == "__main__":
    # ✅ Optionally configure PostgreSQL checkpointer
    postgres_config = PostgresCheckpointerConfig(
        db_host="localhost",
        db_port=5432,
        db_name="postgres",
        db_user="postgres",
        db_pass="postgres",  # 🔐 Replace with env var in real code
        ssl_mode="disable",
        setup_needed=True
    )

    # ✅ Create agent config
    config = ChessAgentConfig(
        enable_analysis=True,
        persistence=postgres_config,
        name="postgres_chess_game"
    )

    agent = ChessAgent(config=config)
    run_chess_game(agent)
