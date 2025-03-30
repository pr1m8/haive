# src/haive/agents/agent_games/checkers/agent.py

from typing import Dict, Any, List
from langgraph.types import Command
from src.haive.games.framework.base import GameAgent
from src.haive.games.checkers.models import CheckersState, CheckersMove, CheckersPlayerDecision
from src.haive.games.checkers.state import CheckersStateManager
from src.haive.games.checkers.config import CheckersAgentConfig
from src.haive.core.engine.agent.agent import register_agent
import time

@register_agent(CheckersAgentConfig)
class CheckersAgent(GameAgent[CheckersState]):
    """Agent for playing checkers."""
    
    def __init__(self, config: CheckersAgentConfig):
        super().__init__(config)
        self.state_manager = CheckersStateManager
    
    def prepare_move_context(self, state: CheckersState, player: str) -> Dict[str, Any]:
        """Prepare context for move generation."""
        # Get legal moves for visualization in the prompt
        legal_moves = self.state_manager.get_legal_moves(state)
        formatted_legal_moves = [str(move) for move in legal_moves]
        
        # Get player's analysis if available
        player_analysis = None
        if player == "red" and state.red_analysis:
            player_analysis = state.red_analysis[-1]
        elif player == "black" and state.black_analysis:
            player_analysis = state.black_analysis[-1]
        
        # Prepare the context for the LLM
        return {
            "board": state.board_string,
            "turn": state.turn,
            "color": player,
            "legal_moves": formatted_legal_moves,
            "captured_pieces": state.captured_pieces,
            "move_history": [str(move) for move in state.move_history[-5:]],  # Last 5 moves
            "player_analysis": player_analysis
        }
    
    def prepare_analysis_context(self, state: CheckersState, player: str) -> Dict[str, Any]:
        """Prepare context for position analysis."""
        return {
            "board": state.board_string,
            "turn": state.turn,
            "color": player,
            "captured_pieces": state.captured_pieces,
            "move_history": [str(move) for move in state.move_history[-5:]]  # Last 5 moves
        }
    
    def extract_move(self, response: CheckersPlayerDecision) -> CheckersMove:
        """Extract move from engine response."""
        return response.move
    
    def make_player1_move(self, state: CheckersState) -> Command:
        """Make a move for the red player."""
        return self.make_move(state, "red")
    
    def make_player2_move(self, state: CheckersState) -> Command:
        """Make a move for the black player."""
        return self.make_move(state, "black")
    
    def analyze_player1(self, state: CheckersState) -> Command:
        """Analyze position for the red player."""
        return self.analyze_position(state, "red")
    
    def analyze_player2(self, state: CheckersState) -> Command:
        """Analyze position for the black player."""
        return self.analyze_position(state, "black")
    
    def visualize_state(self, state: Dict[str, Any]) -> None:
        """Visualize the current game state."""
        # Create a CheckersState from the dict to access board_string
        checker_state = CheckersState(**state)
        
        print("\n" + "=" * 50)
        print(f"🎮 Current Player: {checker_state.turn.upper()}")
        print(f"📌 Game Status: {checker_state.game_status}")
        print("=" * 50)
        
        # Print the board
        print("\n" + checker_state.board_string)
        
        # Print captured pieces
        print(f"\n🔴 Red Captures: {checker_state.captured_pieces['red']}")
        print(f"⚫ Black Captures: {checker_state.captured_pieces['black']}")
        
        # Print last move if available
        if checker_state.move_history:
            last_move = checker_state.move_history[-1]
            print(f"\n📝 Last Move: {last_move}")
        
        # Print analyses if available
        if checker_state.red_analysis and state.get('turn') == 'black':  # Show red's analysis after their move
            last_analysis = checker_state.red_analysis[-1]
            print("\n🔍 Red's Analysis:")
            print(f"   - Material Advantage: {last_analysis.get('material_advantage', 'N/A')}")
            print(f"   - Center Control: {last_analysis.get('control_of_center', 'N/A')}")
            print(f"   - Suggested Moves: {', '.join(last_analysis.get('suggested_moves', []))}")
        
        if checker_state.black_analysis and state.get('turn') == 'red':  # Show black's analysis after their move
            last_analysis = checker_state.black_analysis[-1]
            print("\n🔍 Black's Analysis:")
            print(f"   - Material Advantage: {last_analysis.get('material_advantage', 'N/A')}")
            print(f"   - Center Control: {last_analysis.get('control_of_center', 'N/A')}")
            print(f"   - Suggested Moves: {', '.join(last_analysis.get('suggested_moves', []))}")
        
        # Add a short delay for readability
        time.sleep(0.5)