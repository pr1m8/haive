from typing import Dict, Any, List, Tuple
from langgraph.types import Command
from src.haive.games.framework.base import GameAgent
from .models import ReversiState, ReversiMove
from .state import ReversiStateManager
from src.haive.core.engine.agent.agent import register_agent
from src.haive.core.engine.aug_llm import AugLLMConfig
from src.haive.core.models.llm.base import AzureLLMConfig
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
import time

class ReversiAnalysis(BaseModel):
    """Analysis of a Reversi position."""
    material_advantage: str = Field(..., description="Which player has more pieces")
    positional_evaluation: str = Field(..., description="Evaluation of position quality (corners, edges, mobility)")
    recommended_moves: List[Tuple[int, int]] = Field(..., description="Recommended move coordinates")
    strategic_notes: str = Field(..., description="Strategic considerations for the position")

def generate_move_prompt(player: str) -> ChatPromptTemplate:
    """Generate a prompt for making a move in Reversi."""
    return ChatPromptTemplate.from_messages([
        ('system', 
            f"You are the {player} player in a game of Reversi/Othello. Your goal is to have more pieces than your opponent at the end of the game.\n\n"
            f"Rules:\n"
            f"1. Place a disc on an empty square where it will flank opponent discs.\n"
            f"2. When you flank opponent discs, they are flipped to your color.\n"
            f"3. A valid move must flip at least one opponent disc.\n"
            f"4. If you have no valid moves, your turn is skipped.\n"
            f"5. The game ends when neither player can move, usually when the board is full."
        ),
        ('human', 
            "Current Game State:\n"
            "{board_string}\n\n"
            f"You are playing as {player}. It's your turn.\n\n"
            "Legal Moves Available:\n{legal_moves}\n\n"
            "Recent Moves:\n{move_history}\n\n"
            "Choose one of the available legal moves. Provide your reasoning and return a move object."
        )
    ])

def generate_analysis_prompt(player: str) -> ChatPromptTemplate:
    """Generate a prompt for analyzing a Reversi position."""
    return ChatPromptTemplate.from_messages([
        ('system', 
            f"You are a Reversi/Othello strategy expert. Analyze the position from {player}'s perspective."
        ),
        ('human', 
            "Current Game State:\n"
            "{board_string}\n\n"
            f"Analyze the position for {player}.\n\n"
            "Disc Count:\n"
            f"Black: {black_count}\n"
            f"White: {white_count}\n\n"
            "Recent Moves:\n{move_history}\n\n"
            "Provide a detailed analysis including:\n"
            "1. Material evaluation (disc count advantage)\n"
            "2. Positional evaluation (corners, edges, mobility)\n"
            "3. Recommended moves with coordinates\n"
            "4. Strategic considerations"
        )
    ])

# Define the AugLLM configurations
aug_llm_configs = {
    "black_player": AugLLMConfig(
        name="black_player",
        llm_config=AzureLLMConfig(model="gpt-4o"),
        prompt_template=generate_move_prompt("black"),
        structured_output_model=ReversiMove
    ),
    "white_player": AugLLMConfig(
        name="white_player",
        llm_config=AzureLLMConfig(model="gpt-4o"),
        prompt_template=generate_move_prompt("white"),
        structured_output_model=ReversiMove
    ),
    "black_analyzer": AugLLMConfig(
        name="black_analyzer",
        llm_config=AzureLLMConfig(model="gpt-4o"),
        prompt_template=generate_analysis_prompt("black"),
        structured_output_model=ReversiAnalysis
    ),
    "white_analyzer": AugLLMConfig(
        name="white_analyzer",
        llm_config=AzureLLMConfig(model="gpt-4o"),
        prompt_template=generate_analysis_prompt("white"),
        structured_output_model=ReversiAnalysis
    ),
}

class ReversiConfig(GameConfig):
    """Configuration for the Reversi agent."""
    state_schema: Type[ReversiState] = Field(default=ReversiState)
    aug_llm_configs: Dict[str, AugLLMConfig] = Field(
        default=aug_llm_configs, description="Config for the Reversi agent."
    )
    enable_analysis: bool = Field(
        default=True, description="Whether to enable analysis."
    )
    visualize: bool = Field(
        default=True, description="Whether to visualize the game."
    )

    @classmethod
    def default_config(cls):
        """Create a default configuration."""
        return cls(
            state_schema=ReversiState,
            aug_llm_configs=aug_llm_configs,
            enable_analysis=True,
            visualize=True
        )

@register_agent(ReversiConfig)
class ReversiAgent(GameAgent[ReversiConfig]):
    """Agent for playing Reversi."""
    
    def __init__(self, config: ReversiConfig = ReversiConfig()):
        """Initialize the Reversi agent."""
        super().__init__(config)
        self.state_manager = ReversiStateManager
        self.engines = config.aug_llm_configs
    
    def prepare_move_context(self, state: ReversiState, player: str) -> Dict[str, Any]:
        """Prepare context for move generation."""
        # Get legal moves
        legal_moves = self.state_manager.get_legal_moves(state)
        
        # Format legal moves for display
        formatted_legal_moves = "\n".join([
            f"Place at ({move.row}, {move.col}), flipping {len(move.flipped_positions)} discs" 
            for move in legal_moves if not (move.row == -1 and move.col == -1)  # Exclude "skip" moves
        ])
        
        # Check if this is a "skip" turn (no legal moves)
        if not formatted_legal_moves:
            formatted_legal_moves = "No legal moves available. Your turn will be skipped."
        
        # Get recent move history
        recent_moves = []
        for move in state.move_history[-5:]:
            if move.row == -1 and move.col == -1:
                recent_moves.append(f"{move.color} skipped (no legal moves)")
            else:
                recent_moves.append(str(move))
        
        # Prepare the context
        return {
            "board_string": state.board_string,
            "player": player,
            "legal_moves": formatted_legal_moves,
            "move_history": "\n".join(recent_moves),
            "black_count": state.black_count,
            "white_count": state.white_count
        }
    
    def extract_move(self, response: Any) -> ReversiMove:
        """Extract move from engine response."""
        # For a skip move, create a special move with row=-1, col=-1
        if isinstance(response, dict) and response.get("skip", False):
            return ReversiMove(row=-1, col=-1, color=self.state.turn)
        # The response should already be a ReversiMove object
        return response
    
    def make_player1_move(self, state: ReversiState) -> Command:
        """Make a move for black."""
        return self.make_move(state, "black")
    
    def make_player2_move(self, state: ReversiState) -> Command:
        """Make a move for white."""
        return self.make_move(state, "white")
    
    def prepare_analysis_context(self, state: ReversiState, player: str) -> Dict[str, Any]:
        """Prepare context for position analysis."""
        return {
            "board_string": state.board_string,
            "player": player,
            "move_history": [str(move) for move in state.move_history[-5:]],
            "black_count": state.black_count,
            "white_count": state.white_count
        }
    
    def analyze_player1(self, state: ReversiState) -> Command:
        """Analyze position for black."""
        return self.analyze_position(state, "black")
    
    def analyze_player2(self, state: ReversiState) -> Command:
        """Analyze position for white."""
        return self.analyze_position(state, "white")
    
    def visualize_state(self, state: Dict[str, Any]) -> None:
        """Visualize the current game state."""
        # Create a ReversiState from the dict
        game_state = ReversiState(**state)
        
        print("\n" + "=" * 50)
        print(f"🎮 Current Player: {game_state.turn}")
        print(f"📌 Game Status: {game_state.game_status}")
        print("=" * 50)
        
        # Print the board
        print("\n" + game_state.board_string)
        
        # Print last move if available
        if game_state.move_history:
            last_move = game_state.move_history[-1]
            if last_move.row == -1 and last_move.col == -1:
                print(f"\n📝 Last Move: {last_move.color} skipped (no legal moves)")
            else:
                print(f"\n📝 Last Move: {str(last_move)}")
        
        # Print analyses if available
        if hasattr(game_state, "black_analysis") and game_state.black_analysis and game_state.turn == "white":
            last_analysis = game_state.black_analysis[-1]
            print(f"\n🔍 Black's Analysis:")
            print(f"Material: {last_analysis.get('material_advantage', 'N/A')}")
            print(f"Position: {last_analysis.get('positional_evaluation', 'N/A')}")
            print(f"Strategic Notes: {last_analysis.get('strategic_notes', 'N/A')}")
            
        if hasattr(game_state, "white_analysis") and game_state.white_analysis and game_state.turn == "black":
            last_analysis = game_state.white_analysis[-1]
            print(f"\n🔍 White's Analysis:")
            print(f"Material: {last_analysis.get('material_advantage', 'N/A')}")
            print(f"Position: {last_analysis.get('positional_evaluation', 'N/A')}")
            print(f"Strategic Notes: {last_analysis.get('strategic_notes', 'N/A')}")
        
        # Add a short delay for readability
        time.sleep(0.5)