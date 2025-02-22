from src.haive.agents.base import AgentArchitecture, AgentArchitectureConfig
from src.haive.core.aug_llm.base import AugLLMConfig
from langgraph.graph import StateGraph
from langgraph.types import Command
from langgraph.constants import START, END
import chess
from typing import Dict, Literal, Optional, List
from pydantic import BaseModel, Field, field_validator
from src.haive.agents.agent_games.chess.state import ChessGameState
from src.haive.agents.agent_games.chess.models import ChessPlayerDecision, ChessAnalysis
from langchain_core.prompts import ChatPromptTemplate
from src.haive.agents.agent_games.chess.models import ChessMoveValidation
from src.haive.agents.agent_games.chess.aug_llms import aug_llm_configs
from src.haive.agents.agent_games.chess.state import EnhancedChessState
from src.haive.core.aug_llm.base import compose_runnable
class ChessAgentConfig(AgentArchitectureConfig):
    """Configuration for the chess agent with segmented analysis"""
    state_schema: type = Field(default=EnhancedChessState)
    aug_llm_configs: Dict[str,AugLLMConfig] = Field(default=aug_llm_configs,description="Config for the agent")
    should_visualize_graph: bool = Field(default=True,description="Whether to visualize the graph")
    graph_name: str = Field(default="chess_game.png",description="The name of the graph")
    enable_analysis: bool = Field(default=True,description="Whether to enable analysis")

    
class ChessAgent(AgentArchitecture):
    def __init__(self, config: ChessAgentConfig):
        super().__init__(config)
        
        # ✅ Make sure LLMs are properly composed
        self.llms = {name: compose_runnable(cfg) for name, cfg in config.aug_llm_configs.items()}

        # ✅ Ensure LLMs are not None
        for key, llm in self.llms.items():
            if llm is None:
                raise ValueError(f"Failed to compose LLM for {key}")

        

    def setup_workflow(self):
        """Setup the chess agent's game workflow ensuring optional analysis and proper status checks."""
        
        # ✅ Core Nodes
        self.graph.add_node("initialize_game", self.initialize_game)
        self.graph.add_node("white_move", self.make_white_move)
        self.graph.add_node("black_move", self.make_black_move)
        #self.graph.add_node("check_game_status", self.check_game_status)

        # ✅ Start -> Initialize Game
        self.graph.add_edge(START, "initialize_game")

        # ✅ Handle optional analysis before moves
        if self.config.enable_analysis:
            self.graph.add_node("white_analysis_position", self.analyze_white_position)
            self.graph.add_node("black_analysis_position", self.analyze_black_position)

            # ✅ Initialize Game → White Analysis → White Move
            self.graph.add_edge("initialize_game", "white_analysis_position")
            self.graph.add_edge("white_analysis_position", "white_move")

            # ✅ White Move → Check Game Status → (If ongoing) → Black Analysis → Black Move
            self.graph.add_conditional_edges(
                "white_move",
                self.should_continue_game,
                {
                    True: "black_analysis_position",
                    False: END
                }
            )
            self.graph.add_edge("black_analysis_position", "black_move")

            # ✅ Black Move → Check Game Status → (If ongoing) → White Analysis
            self.graph.add_conditional_edges(
                "black_move",
                self.should_continue_game,
                {
                    True: "white_analysis_position",
                    False: END
                }
            )
        
        else:
            # 🚀 Skip analysis → Directly move between turns
            self.graph.add_edge("initialize_game", "white_move")

            # ✅ White Move → Check Game Status → (If ongoing) → Black Move
            self.graph.add_conditional_edges(
                "white_move",
                self.should_continue_game,
                {
                    True: "black_move",
                    False: END
                }
            )

            # ✅ Black Move → Check Game Status → (If ongoing) → White Move
            self.graph.add_conditional_edges(
                "black_move",
                self.should_continue_game,
                {
                    True: "white_move",
                    False: END
                }
            )


        def filter_game_messages(self, state: EnhancedChessState, color: str) -> Dict:
            """Prepares filtered game data for LLM prompts, ensuring expected keys match the prompt template."""

            return {
                "color": color,  # ✅ Pass 'white' or 'black'
                "current_board_fen": state.board_fen,  # ✅ Latest board state
                "previous_board_fen": state.board_fens[-2] if len(state.board_fens) > 1 else "N/A",  # ✅ Second-to-last board state
                "recent_moves": state.move_history[-5:],  # ✅ Last 5 moves
                "captured_pieces": state.captured_pieces,  # ✅ Captured pieces
                "player_analysis": (
                    state.white_analysis[-1] if color == "white" and state.white_analysis else
                    state.black_analysis[-1] if color == "black" and state.black_analysis else "N/A"
                ),  # ✅ Latest analysis for the current player
            }

    def initialize_game(self, state: EnhancedChessState) -> Command:
        """Initialize new game state"""
        board = chess.Board()
        return Command(update={
            "board_fens": [board.fen()],
            "current_player": "white",
            "turn": "white",  # Adding required field from parent class
            "move_history": [],
            "game_status": "ongoing",
            "white_analysis": [],
            "black_analysis": [],
            "captured_pieces": {"white": [], "black": []}
        })
    def make_move(self, state: EnhancedChessState, color: str) -> Command:
        """Executes a move for the given player (white/black)."""

        player = self.llms.get(f"{color}_player")
        if player is None:
            raise ValueError(f"Missing LLM for {color}_player")

        print(f"\n🎯 {color.capitalize()} Player Move Execution")
        print(f"📜 Board FEN Before Move: {state.board_fen}")  # ✅ Fix: Use `board_fen` property
        prompt_inputs = {
            "board_fen": state.board_fen,  # ✅ Latest board state
            "move_history": state.move_history[-5:],  # ✅ Last 5 moves
            "color": color,
            "captured_pieces": state.captured_pieces,
            "player_analysis": (
                state.white_analysis[-1] if color == "white" and state.white_analysis else
                state.black_analysis[-1] if color == "black" and state.black_analysis else "N/A"
            ),
            'current_board_fen':state.board_fen,
            "previous_board_fen": state.board_fens[-2] if len(state.board_fens) > 1 else "N/A",
            "recent_moves": state.move_history[-5:],
            "game_status": state.game_status,
        }
        #print(prompt)
        # 🎯 Step 1: Ask the AI for a move
        move_response = player.invoke({
            "board_fen": state.board_fen,  # ✅ Latest board state
            "move_history": state.move_history[-5:],  # ✅ Last 5 moves
            "color": color,
            "captured_pieces": state.captured_pieces,
            "player_analysis": (
                state.white_analysis[-1] if color == "white" and state.white_analysis else
                state.black_analysis[-1] if color == "black" and state.black_analysis else "N/A"
            ),
            'current_board_fen':state.board_fen,
            "previous_board_fen": state.board_fens[-2] if len(state.board_fens) > 1 else "N/A",
            "recent_moves": state.move_history[-5:],
            "game_status": state.game_status,
        })

        move_uci = move_response.move.uci  # Extract the UCI move string
        move = chess.Move.from_uci(move_uci)  # Convert to python-chess move object

        # 🎯 Step 2: Validate the move
        board = chess.Board(state.board_fen)  # ✅ Fix: Use latest board state
        if move not in board.legal_moves:
            print(f"🚨 Suggested Move {move.uci()} is NOT legal!")
            print(f"♟️ Legal Moves Available: {[m.uci() for m in board.legal_moves]}")
            return Command(update={"error_message": f"Illegal move suggested by {color}: {move.uci()}"})

        # 🎯 Step 3: Apply the move
        board.push(move)

        print(f"✅ Move Applied: {move.uci()}")
        print(f"📜 Board FEN After Move: {board.fen()}")

        # 🎯 Step 4: Update game state
        next_turn = "black" if color == "white" else "white"

        return Command(update={
            "board_fens": state.board_fens[-4:] + [board.fen()],  # ✅ Fix: Maintain history up to last 5 states
            "move_history": state.move_history[-4:] + [(color, move.uci())],  # ✅ Append to history correctly
            "captured_pieces": state.captured_pieces,  # ✅ Keep existing captured pieces
            "turn": next_turn,
            "current_player": next_turn,
            "game_status": (
                "checkmate" if board.is_checkmate() else
                "stalemate" if board.is_stalemate() else
                "check" if board.is_check() else
                "ongoing"
            ),
            "white_analysis": state.white_analysis[-5:],  # ✅ Trim analysis history
            "black_analysis": state.black_analysis[-5:],
            "error_message": None  # ✅ Clear errors
        })



            

    def analyze_white_position(self, state: EnhancedChessState) -> Command:
        """Analyze position from white's perspective"""
        analysis = self.white_analyzer.invoke({
            "board_fen": state.board_fen,
            "move_history": state.move_history,
            "player_color": "white",
            "captured_pieces": state.captured_pieces
        })
        return Command(update={"white_analysis": analysis})

    def analyze_black_position(self, state: EnhancedChessState) -> Command:
        """Analyze position from black's perspective"""
        analysis = self.black_analyzer.invoke({
            "board_fen": state.board_fen,
            "move_history": state.move_history,
            "player_color": "black",
            "captured_pieces": state.captured_pieces
        })
        return Command(update={"black_analysis": analysis})
    def make_white_move(self, state: EnhancedChessState) -> Command:
        """Make a move for white"""
        return self.make_move(state, "white")

    def make_black_move(self, state: EnhancedChessState) -> Command:
        """Make a move for black"""
        return self.make_move(state, "black")

    def analyze_white_position(self, state: EnhancedChessState) -> Command:
        """Analyze position from white's perspective and pass the correct prompt inputs."""

        analyzer_key = "white_analyzer"
        if analyzer_key not in self.llms:
            raise ValueError(f"Missing LLM for {analyzer_key}")

        # ✅ Fix: Pass ALL required variables to the prompt
        analysis = self.llms[analyzer_key].invoke({
            "current_board_fen": state.board_fen,  # ✅ Latest board state
            "previous_board_fen": state.board_fens[-2] if len(state.board_fens) > 1 else "N/A",  # ✅ Previous board
            "recent_moves": state.move_history[-5:],  # ✅ Last 5 moves
            "captured_pieces": state.captured_pieces,  # ✅ Captured pieces
            "color": "white",  # ✅ Ensure player color is passed
        })

        # ✅ Convert `SegmentedAnalysis` to a dictionary
        return Command(update={"white_analysis": state.white_analysis[-4:] + [analysis.dict()]})

    def analyze_black_position(self, state: EnhancedChessState) -> Command:
        """Analyze position from black's perspective and pass the correct prompt inputs."""

        analyzer_key = "black_analyzer"
        if analyzer_key not in self.llms:
            raise ValueError(f"Missing LLM for {analyzer_key}")

        # ✅ Fix: Pass ALL required variables to the prompt
        analysis = self.llms[analyzer_key].invoke({
            "current_board_fen": state.board_fen,  # ✅ Latest board state
            "previous_board_fen": state.board_fens[-2] if len(state.board_fens) > 1 else "N/A",  # ✅ Previous board
            "recent_moves": state.move_history[-5:],  # ✅ Last 5 moves
            "captured_pieces": state.captured_pieces,  # ✅ Captured pieces
            "color": "black",  # ✅ Ensure player color is passed
        })

        # ✅ Convert `SegmentedAnalysis` to a dictionary
        return Command(update={"black_analysis": state.black_analysis[-4:] + [analysis.dict()]})

    def check_game_status(self, state: EnhancedChessState) -> Command:
        """Check and update game status with enhanced validation"""
        board = chess.Board(state.board_fen)
        
        status = "ongoing"
        if board.is_checkmate():
            status = "checkmate"
        elif board.is_stalemate():
            status = "stalemate"
        elif board.is_insufficient_material():
            status = "draw"
        elif board.is_check():
            status = "check"
            
        return Command(update={"game_status": status})

    def should_continue_game(self, state: EnhancedChessState) -> bool:
        """Determine if the game should continue"""
        return state.game_status in ["ongoing", "check"]
import chess
from typing import Dict, Any
from src.haive.agents.agent_games.chess.agent import ChessAgent, ChessAgentConfig

def run_chess_game(agent: ChessAgent):
    """Run a chess game with visualization and structured output."""

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
    for step in agent.app.stream(initial_state, config=agent.runnable_config, debug=False, stream_mode="values"):
        board = chess.Board(step["board_fens"][-1])

        # 🎯 **Game Board Visualization**
        print("\n🔷 Current Board Position:")
        print(board)

        # 🎯 **Game State Information**
        print(f"\n🎮 Current Player: {step['current_player'].capitalize()}")
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
