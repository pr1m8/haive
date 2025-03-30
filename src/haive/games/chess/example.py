from src.haive.games.chess.agent import ChessAgent
from src.haive.games.chess.config import ChessAgentConfig
from typing import Dict, Any
import chess

def run_chess_game(agent: ChessAgent):
    """Run a chess game with visualization and structured output.
    
    This function manages the game loop and provides rich visualization
    of the game state, including:
        - Board visualization using ASCII art
        - Move history tracking
        - Position analysis display
        - Captured pieces tracking
        - Game status updates
    
    Args:
        agent (ChessAgent): The chess agent to run the game with.
    
    Example:
        >>> agent = ChessAgent(ChessAgentConfig(enable_analysis=True))
        >>> run_chess_game(agent)
        
        Current Board Position:
        r n b q k b n r
        p p p p p p p p
        . . . . . . . .
        . . . . . . . .
        . . . . . . . .
        . . . . . . . .
        P P P P P P P P
        R N B Q K B N R
        
        Current Player: White
        Game Status: ongoing
        --------------------------------------------------
    """
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

    # ✅ Stream the game loop
    for step in agent.app.stream(initial_state, config=agent.runnable_config, debug=True, stream_mode="values"):
        board = chess.Board(step["board_fens"][-1])

        # 🎯 **Game Board Visualization**
        print("\n🔷 Current Board Position:")
        print(board)

        # 🎯 **Game State Information**
       # print(f"\n🎮 Current Player: {step['current_player'].capitalize()}")
        print(f"♟️ Turn: {step['turn'].capitalize()}")
        print(f"📌 Game Status: {step['game_status']}")
        print("-" * 50)

        # ✅ **Display Last Move**
        if step.get("move_history"):
            last_move = step["move_history"][-1]
            print(f"📝 Last Move: {last_move[0].capitalize()} played {last_move[1]}")

        # ✅ **Handle White's Analysis Safely**
        if step.get("white_analysis"):
            last_white_analysis: Dict[str, Any] = step["white_analysis"][-1]  # Extract last analysis dictionary
            print("\n🔍 White's Analysis:")
            print(f"   - Position Score: {last_white_analysis.get('position_score', 'N/A')}")
            print(f"   - Attacking Chances: {last_white_analysis.get('attacking_chances', 'N/A')}")
            print(f"   - Defensive Needs: {last_white_analysis.get('defensive_needs', 'N/A')}")
            print(f"   - Suggested Plans: {', '.join(last_white_analysis.get('suggested_plans', []))}")

        # ✅ **Handle Black's Analysis Safely**
        if step.get("black_analysis"):
            last_black_analysis: Dict[str, Any] = step["black_analysis"][-1]  # Extract last analysis dictionary
            print("\n🔍 Black's Analysis:")
            print(f"   - Position Score: {last_black_analysis.get('position_score', 'N/A')}")
            print(f"   - Attacking Chances: {last_black_analysis.get('attacking_chances', 'N/A')}")
            print(f"   - Defensive Needs: {last_black_analysis.get('defensive_needs', 'N/A')}")
            print(f"   - Suggested Plans: {', '.join(last_black_analysis.get('suggested_plans', []))}")

        # ✅ **Captured Pieces**
        if step.get("captured_pieces"):
            print("\n🔻 Captured Pieces:")
            print(f"   - White Captured: {', '.join(step['captured_pieces']['white']) or 'None'}")
            print(f"   - Black Captured: {', '.join(step['captured_pieces']['black']) or 'None'}")

        print("\n" + "-" * 60)  # Divider for clarity
    agent.save_state_history()

# Run the game
if __name__ == "__main__":
    run_chess_game(agent=ChessAgent(config=ChessAgentConfig()))
