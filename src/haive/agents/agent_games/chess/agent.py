from src.haive.agents.base import AgentArchitecture, AgentArchitectureConfig
from src.haive.core.aug_llm.base import AugLLMConfig
from langgraph.graph import StateGraph
from langgraph.types import Command,Send
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
from langgraph.types import RetryPolicy
def check_game_status(self, state: Dict) -> Send:
    """Check and update game status with enhanced validation."""

    if isinstance(state, dict):
        state = EnhancedChessState(**state)

    board = chess.Board(state.board_fen)

    if board.is_checkmate():
        return Send(END, {"game_status": "checkmate"})
    elif board.is_stalemate():
        return Send(END, {"game_status": "stalemate"})
    elif board.is_insufficient_material():
        return Send(END, {"game_status": "draw"})
    
    # ✅ Determine whose turn it is
    next_turn = "black" if board.turn == chess.BLACK else "white"
    
    if next_turn == "white":
        return Send("white_analysis_position", {"game_status": "ongoing"})
    else:
        return Send("black_analysis_position", {"game_status": "ongoing"})

class ChessAgentConfig(AgentArchitectureConfig):
    """Configuration for the chess agent with optional analysis"""
    state_schema: type = Field(default=EnhancedChessState)
    aug_llm_configs: Dict[str, AugLLMConfig] = Field(default=aug_llm_configs, description="Config for the agent")
    enable_analysis: bool = Field(default=True, description="Enable or disable analysis nodes")
    #visualize_graph: bool = Field(default=True, description="Enable or disable graph visualization")
    should_visualize_graph: bool = Field(default=True, description="Enable or disable graph visualization")
    visualize_graph_output_name: str = Field(default="./chess_game_graph.png", description="File name for the graph output")

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
        """Setup the game workflow with retry policy and proper turn switching."""

        move_retry_policy = RetryPolicy(
            initial_interval=1.0,
            backoff_factor=2.0,
            max_interval=8.0,
            max_attempts=3,
            jitter=True
        )

        # ✅ Core game nodes
        self.graph.add_node("initialize_game", self.initialize_game)
        self.graph.add_node("white_move", self.make_white_move, retry=move_retry_policy)
        self.graph.add_node("black_move", self.make_black_move, retry=move_retry_policy)
        self.graph.add_node("check_game_status", self.check_game_status)

        # ✅ Start Game Flow
        self.graph.add_edge(START, "initialize_game")
        self.graph.add_edge("initialize_game", "white_analysis_position")  # ✅ Start with white analysis before first move

        # ✅ Analysis nodes (private per player)
        if self.config.enable_analysis:
            self.graph.add_node("white_analysis_position", self.analyze_white_position)
            self.graph.add_node("black_analysis_position", self.analyze_black_position)

            # ✅ White Move → Check Game Status
            self.graph.add_edge("white_analysis_position", "white_move")
            self.graph.add_edge("white_move", "check_game_status")

            # ✅ Black Move → Check Game Status
            self.graph.add_edge("black_analysis_position", "black_move")
            self.graph.add_edge("black_move", "check_game_status")

            # ✅ Check game status should redirect properly
            self.graph.add_conditional_edges(
                "check_game_status",
                self.check_game_status,  # Function will determine next step
                {
                    "ongoing_white": "white_analysis_position",  # ✅ If ongoing and it's White's turn
                    "ongoing_black": "black_analysis_position",  # ✅ If ongoing and it's Black's turn
                    "checkmate": END,
                    "stalemate": END,
                    "draw": END
                }
            )

        else:
            # ✅ No analysis: moves directly switch turns
            self.graph.add_edge("white_move", "check_game_status")
            self.graph.add_edge("black_move", "check_game_status")

            self.graph.add_conditional_edges(
                "check_game_status",
                self.check_game_status,
                {
                    "ongoing_white": "white_move",
                    "ongoing_black": "black_move",
                    "checkmate": END,
                    "stalemate": END,
                    "draw": END
                }
            )


        
    ### **🌟 `analyze_position()` - Unified Function**
    def analyze_position(self, state: EnhancedChessState) -> Send:
        """
        Analyze the position for the current player before the next move.
        🌟 `analyze_position()` - Unified Function
        """
        
        
        player_color = state["turn"]
        analyzer_key = f"{player_color}_analyzer"
        analysis = self.llms[analyzer_key].invoke({
            "board_fen": state.board_fen,
            "move_history": state.move_history,
            "player_color": player_color,
            "captured_pieces": state.captured_pieces
        })
        
        return Send({f"{player_color}_analysis": analysis})
           

  
    def initialize_game(self, state: EnhancedChessState) -> Command:
        """Initialize new game state"""
        board = chess.Board()
        return Command(update={
            "board_fen": board.fen(),
            "current_player": "white",
            "turn": "white",  # Adding required field from parent class
            "move_history": [],
            "game_status": "ongoing",
            "white_analysis": None,
            "black_analysis": None,
            "captured_pieces": {"white": [], "black": []}
        })
    
    

    from langgraph.types import Send

    from langgraph.types import Send

    def make_move(self, state: ChessGameState, color: str) -> Send:
        """Executes a move for the given player (white/black) with validation and game status checks."""

        player = self.llms.get(f"{color}_player")
        if player is None:
            raise ValueError(f"Missing LLM for {color}_player")

        print(f"\n🎯 {color.capitalize()} Player Move Execution")
        print(f"📜 Board FEN Before Move: {state.board_fen}")

        # 🎯 Step 1: Request move from AI
        try:
            move_response = player.invoke({
                "board_fen": state.board_fen,
                "move_history": state.move_history,
                "analysis": state.white_analysis if color == "white" else state.black_analysis
            })
            move_uci = move_response.move.uci
            move = chess.Move.from_uci(move_uci)
        except Exception as e:
            print(f"🚨 Error during {color} move decision: {e}")
            return Send("invalid_move", {"error": str(e)})  # Retry via LangGraph

        # 🎯 Step 2: Validate move legality
        board = chess.Board(state.board_fen)
        if move not in board.legal_moves:
            print(f"🚨 Illegal Move Suggested: {move.uci()} ❌")
            print(f"♟️ Available Legal Moves: {[m.uci() for m in board.legal_moves]}")
            return Send("invalid_move", {"error": f"Illegal move {move.uci()}"})  # Retry

        # 🎯 Step 3: Apply the move
        board.push(move)
        print(f"✅ Move Applied: {move.uci()}")
        print(f"📜 Updated Board FEN: {board.fen()}")

        # 🎯 Step 4: Send to `check_game_status`
        return Send("check_game_status", {
            "board_fen": board.fen(),
            "move_history": state.move_history + [move.uci()],
            "captured_pieces": state.captured_pieces,
            "turn": "black" if color == "white" else "white",
            "current_player": "black" if color == "white" else "white",
            "last_move_validation": move.uci()
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
        """Analyze position from white's perspective"""
        analyzer_key = "white_analyzer"
        analysis = self.llms[analyzer_key].invoke({
            "board_fen": state.board_fen,
            "move_history": state.move_history,
            "player_color": "white",
            "captured_pieces": state.captured_pieces
        })
        return Command(update={"white_analysis": analysis})

    def analyze_black_position(self, state: EnhancedChessState) -> Command:
        """Analyze position from black's perspective"""
        analyzer_key = "black_analyzer"
        analysis = self.llms[analyzer_key].invoke({
            "board_fen": state.board_fen,
            "move_history": state.move_history,
            "player_color": "black",
            "captured_pieces": state.captured_pieces
        })
        return Command(update={"black_analysis": analysis})
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

def run_chess_game(agent: ChessAgent):
    """Run a chess game with visualization and analysis"""
    # Initialize the game
    #agent.setup_workflow()
    #agent.compile_graph()
    
    # Create initial state with all required fields
    initial_state = {
        "board_fen": chess.Board().fen(),
        "current_player": "white",
        "turn": "white",  # Adding the required field from parent class
        "move_history": [],
        "game_status": "ongoing",
        "white_analysis": None,
        "black_analysis": None,
        "captured_pieces": {"white": [], "black": []},
        "last_move_validation": None
    }

    # Run the game loop
    for step in agent.app.stream(initial_state, config=agent.runnable_config, debug=True, stream_mode="values"):
        print(step)
        
        board = chess.Board(step["board_fen"])
        print("\nCurrent board position:")
        print(board)
        print(f"\nCurrent player: {step['current_player']}")
        print(f"Turn: {step['turn']}")
        
        if step.get("last_move_validation"):
            print(f"Last move: {step['last_move_validation'].move}")
            
        if step.get("white_analysis"):
            print("\nWhite's analysis:")
            print(f"Position score: {step['white_analysis'].position_score}")
            print(f"Attacking chances: {step['white_analysis'].attacking_chances}")
            print(f"Suggested plans: {', '.join(step['white_analysis'].suggested_plans)}")
            
        if step.get("black_analysis"):
            print("\nBlack's analysis:")
            print(f"Position score: {step['black_analysis'].position_score}")
            # ✅ **Fix: Check if 'defensive_needs' exists before accessing**
            defensive_needs = getattr(step["black_analysis"], "defensive_needs", "No specific defensive needs identified.")
            print(f"Defensive needs: {defensive_needs}")
            print(f"Suggested plans: {', '.join(step['black_analysis'].suggested_plans)}")
            
        if step.get("captured_pieces"):
            print("\nCaptured pieces:")
            print(f"White captured: {', '.join(step['captured_pieces']['white'])}")
            print(f"Black captured: {', '.join(step['captured_pieces']['black'])}")
            
        print("\nGame status:", step["game_status"])
        print("-" * 50)

# Run the game
if __name__ == "__main__":
    agent=ChessAgent(config=ChessAgentConfig())
    run_chess_game(agent=agent)
