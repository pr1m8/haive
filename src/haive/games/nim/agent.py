from src.haive.games.nim.config import NimConfig
from src.haive.games.nim.state import NimState
from src.haive.games.nim.state_manager import NimStateManager
from src.haive.games.framework.base.agent import GameAgent
from src.haive.core.graph.GraphBuilder import DynamicGraph
from typing import Dict, Any, Optional
import time 
from langgraph.graph import Command
from src.haive.core.graph.GraphBuilder import DynamicGraph
from src.haive.core.graph.GraphBuilder import register_agent
from src.haive.games.nim.models import NimMove, NimAnalysis
@register_agent(NimConfig)
class NimAgent(GameAgent[NimConfig]):
    """Agent for playing Nim."""
    
    def __init__(self, config: NimConfig = NimConfig()):
        """Initialize the Nim agent."""
        super().__init__(config)
        self.state_manager = NimStateManager
        self.engines = config.aug_llm_configs
    
    def initialize_game(self, state: Dict[str, Any]) -> Command:
        """Initialize a new Nim game with configured pile sizes."""
        game_state = self.state_manager.initialize(pile_sizes=self.config.pile_sizes)
        # Set misere mode from config
        game_state.misere_mode = self.config.misere_mode
        return Command(update=game_state.model_dump() if hasattr(game_state, "model_dump") else game_state.dict())
    
    def prepare_move_context(self, state: NimState, player: str) -> Dict[str, Any]:
        """Prepare context for move generation."""
        # Get legal moves
        legal_moves = self.state_manager.get_legal_moves(state)
        
        # Format legal moves for display
        formatted_legal_moves = "\n".join([
            f"Take {move.stones_taken} stones from pile {move.pile_index} (current size: {state.piles[move.pile_index]})" 
            for move in legal_moves
        ])
        
        # Get recent move history
        recent_moves = []
        for move in state.move_history[-5:]:
            recent_moves.append(str(move))
        
        # Prepare the context
        return {
            "board_string": state.board_string,
            "player": player,
            "legal_moves": formatted_legal_moves,
            "move_history": "\n".join(recent_moves),
            "misere_mode": state.misere_mode
        }
    
    def extract_move(self, response: Any) -> NimMove:
        """Extract move from engine response."""
        # The response should already be a NimMove object
        return response
    
    def make_player1_move(self, state: NimState) -> Command:
        """Make a move for player1."""
        return self.make_move(state, "player1")
    
    def make_player2_move(self, state: NimState) -> Command:
        """Make a move for player2."""
        return self.make_move(state, "player2")
    
    def prepare_analysis_context(self, state: NimState, player: str) -> Dict[str, Any]:
        """Prepare context for position analysis."""
        return {
            "board_string": state.board_string,
            "player": player,
            "move_history": [str(move) for move in state.move_history[-5:]],
            "misere_mode": state.misere_mode
        }
    
    def analyze_player1(self, state: NimState) -> Command:
        """Analyze position for player1."""
        return self.analyze_position(state, "player1")
    
    def analyze_player2(self, state: NimState) -> Command:
        """Analyze position for player2."""
        return self.analyze_position(state, "player2")
    
    def visualize_state(self, state: Dict[str, Any]) -> None:
        """Visualize the current game state."""
        # Create a NimState from the dict
        game_state = NimState(**state)
        
        print("\n" + "=" * 50)
        print(f"🎮 Current Player: {game_state.turn}")
        print(f"📌 Game Status: {game_state.game_status}")
        print(f"🎲 Game Mode: {'Misere (last takes loses)' if game_state.misere_mode else 'Standard (last takes wins)'}")
        print("=" * 50)
        
        # Print the board
        print("\n" + game_state.board_string)
        
        # Print last move if available
        if game_state.move_history:
            last_move = game_state.move_history[-1]
            print(f"\n📝 Last Move: {str(last_move)}")
        
        # Print analyses if available
        if hasattr(game_state, "player1_analysis") and game_state.player1_analysis and game_state.turn == "player2":
            last_analysis = game_state.player1_analysis[-1]
            print(f"\n🔍 Player 1's Analysis:")
            print(f"Nim-sum: {last_analysis.get('nim_sum', 'N/A')}")
            print(f"Evaluation: {last_analysis.get('position_evaluation', 'N/A')}")
            print(f"Explanation: {last_analysis.get('explanation', 'N/A')}")
            
        if hasattr(game_state, "player2_analysis") and game_state.player2_analysis and game_state.turn == "player1":
            last_analysis = game_state.player2_analysis[-1]
            print(f"\n🔍 Player 2's Analysis:")
            print(f"Nim-sum: {last_analysis.get('nim_sum', 'N/A')}")
            print(f"Evaluation: {last_analysis.get('position_evaluation', 'N/A')}")
            print(f"Explanation: {last_analysis.get('explanation', 'N/A')}")
        
        # Add a short delay for readability
        time.sleep(0.5)