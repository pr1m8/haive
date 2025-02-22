from src.haive.agents.base import AgentArchitecture, AgentArchitectureConfig
from src.haive.core.aug_llm.base import AugLLMConfig
from langgraph.graph import StateGraph
from langgraph.types import Command
from langgraph.constants import START, END
import sente
from typing import Dict, Literal, Optional
from pydantic import Field
from src.haive.agents.agent_games.go.state import GoGameState,GoGameStateManager
from src.haive.agents.agent_games.go.models import GoPlayerDecision, GoAnalysis
from src.haive.agents.agent_games.go.aug_llms import aug_llm_configs
from src.haive.core.aug_llm.base import compose_runnable


class GoAgentConfig(AgentArchitectureConfig):
    """Configuration for the Go agent with strategic analysis."""
    state_schema: type = Field(default=GoGameState)
    aug_llm_configs: Dict[str, AugLLMConfig] = Field(
        default=aug_llm_configs, description="Config for the Go agent."
    )
    should_visualize_graph: bool = Field(
        default=True, description="Whether to visualize the game graph."
    )
    graph_name: str = Field(
        default="go_game.png", description="The name of the visualization file."
    )
    include_analysis: bool = Field(
        default=True, description="Whether to include analysis in the game."
    )

class GoAgent(AgentArchitecture):
    def __init__(self, config: GoAgentConfig):
        super().__init__(config)

        # ✅ Ensure LLMs are properly composed
        self.llms = {name: compose_runnable(cfg) for name, cfg in config.aug_llm_configs.items()}

        # ✅ Ensure LLMs are not None
        for key, llm in self.llms.items():
            if llm is None:
                raise ValueError(f"Failed to compose LLM for {key}")

    def setup_workflow(self):
        """Defines the Go game workflow, including move execution and optional analysis."""
        self.graph.add_node("initialize_game", self.initialize_game)
        self.graph.add_node("black_move", self.make_black_move)
        self.graph.add_node("white_move", self.make_white_move)
        self.graph.add_node("black_analysis_position", self.analyze_black_position)
        self.graph.add_node("white_analysis_position", self.analyze_white_position)
        self.graph.add_node("check_game_status", self.check_game_status)

        # ✅ Set up initial game state
        self.graph.add_edge(START, "initialize_game")
        self.graph.add_edge("initialize_game", "black_move")

        # ✅ Move Execution with Optional Analysis
        if self.config.include_analysis:
            self.graph.add_edge("black_move", "black_analysis_position")
            self.graph.add_conditional_edges(
                "black_analysis_position", self.should_continue_game, {True: "white_move", False: END}
            )

            self.graph.add_edge("white_move", "white_analysis_position")
            self.graph.add_conditional_edges(
                "white_analysis_position", self.should_continue_game, {True: "black_move", False: END}
            )
        else:
            self.graph.add_conditional_edges(
                "black_move", self.should_continue_game, {True: "white_move", False: END}
            )
            self.graph.add_conditional_edges(
                "white_move", self.should_continue_game, {True: "black_move", False: END}
            )

    def initialize_game(self, state: Optional[GoGameState] = None) -> Command:
        """Initialize a new game of Go."""
        game_state = GoGameStateManager.initialize()
        return Command(update=game_state.dict())

    def make_move(self, state: GoGameState, color: str) -> Command:
        """Executes a move for the given player (black/white)."""
        player = self.llms.get(f"{color}_player")
        if player is None:
            raise ValueError(f"Missing LLM for {color}_player")

        move_response = player.invoke({
            "board_size": state.board_size,
            "move_history": state.move_history[-5:],  # Last 5 moves
            "color": color,
            "captured_stones": state.captured_stones,
            "player_analysis": (
                state.black_analysis[-1] if color == "black" and state.black_analysis else
                state.white_analysis[-1] if color == "white" and state.white_analysis else "N/A"
            )
        })

        move = move_response.move  # Extract move tuple (row, col)
        new_state = GoGameStateManager.apply_move(state, move)

        return Command(update=new_state.dict())

    def analyze_position(self, state: GoGameState, color: str) -> Command:
        """Analyze the position for the given player (black/white)."""
        analyzer = self.llms.get(f"{color}_analyzer")
        if analyzer is None:
            raise ValueError(f"Missing LLM for {color}_analyzer")

        analysis = analyzer.invoke({
            "board_size": state.board_size,
            "move_history": state.move_history[-5:],  # Last 5 moves
            "color": color,
            "captured_stones": state.captured_stones,
        })

        if color == "black":
            return Command(update={"black_analysis": state.black_analysis[-4:] + [analysis.dict()]})
        else:
            return Command(update={"white_analysis": state.white_analysis[-4:] + [analysis.dict()]})

    def check_game_status(self, state: GoGameState) -> Command:
        """Checks and updates the Go game status."""
        game = sente.sgf.loads(state.board_sgf)

        status = "ongoing"
        if game.is_over():
            status = "ended"

        return Command(update={"game_status": status})

    def should_continue_game(self, state: GoGameState) -> bool:
        """Determines if the game should continue."""
        return state.game_status == "ongoing"

    def make_black_move(self, state: GoGameState) -> Command:
        """Handles black's move."""
        return self.make_move(state, "black")

    def make_white_move(self, state: GoGameState) -> Command:
        """Handles white's move."""
        return self.make_move(state, "white")

    def analyze_black_position(self, state: GoGameState) -> Command:
        """Analyzes black's position if analysis is enabled."""
        return self.analyze_position(state, "black")

    def analyze_white_position(self, state: GoGameState) -> Command:
        """Analyzes white's position if analysis is enabled."""
        return self.analyze_position(state, "white")
import sente
from typing import Dict, Any, Optional
from src.haive.agents.agent_games.go.agent import GoAgent, GoAgentConfig


def run_go_game(agent: GoAgent):
    """Run a Go game with visualization and structured output."""

    # ✅ Initialize the game state
    initial_state = {
        "board_size": 19,
        "board_sgf": sente.sgf.dumps(sente.Game(19)),  # Start with an empty board
        "turn": "black",
        "move_history": [],
        "captured_stones": {"black": 0, "white": 0},
        "passes": 0,  # Track consecutive passes
        "game_status": "ongoing",
        "black_analysis": [],
        "white_analysis": [],
        "error_message": None
    }

    # ✅ Stream the game loop
    for step in agent.app.stream(initial_state, config=agent.runnable_config, debug=True, stream_mode="values"):
        print(sente.sgf.loads(step["board_sgf"]))
        game = sente.sgf.loads(step["board_sgf"])

        # 🎯 **Game Board Visualization**
        print("\n🔷 Current Board Position:")
        print(game)

        # 🎯 **Game State Information**
        print(f"\n🎮 Current Player: {step['turn'].capitalize()}")
        print(f"📌 Game Status: {step['game_status']}")
        print("-" * 50)

        # ✅ **Display Last Move**
        if step.get("move_history"):
            last_move = step["move_history"][-1]
            print(f"📝 Last Move: {last_move[0].capitalize()} played at {last_move[1]}")

        # ✅ **Handle Black's Analysis Safely**
        if step.get("black_analysis"):
            last_black_analysis: Dict[str, Any] = step["black_analysis"][-1]  # Extract last analysis dictionary
            print("\n🔍 Black's Analysis:")
            print(f"   - Territory Estimate: {last_black_analysis.get('territory_evaluation', 'N/A')}")
            print(f"   - Strong Positions: {last_black_analysis.get('strong_positions', 'N/A')}")
            print(f"   - Weak Positions: {last_black_analysis.get('weak_positions', 'N/A')}")
            print(f"   - Strategic Advice: {', '.join(last_black_analysis.get('strategic_advice', []))}")

        # ✅ **Handle White's Analysis Safely**
        if step.get("white_analysis"):
            last_white_analysis: Dict[str, Any] = step["white_analysis"][-1]  # Extract last analysis dictionary
            print("\n🔍 White's Analysis:")
            print(f"   - Territory Estimate: {last_white_analysis.get('territory_evaluation', 'N/A')}")
            print(f"   - Strong Positions: {last_white_analysis.get('strong_positions', 'N/A')}")
            print(f"   - Weak Positions: {last_white_analysis.get('weak_positions', 'N/A')}")
            print(f"   - Strategic Advice: {', '.join(last_white_analysis.get('strategic_advice', []))}")

        # ✅ **Captured Stones**
        if step.get("captured_stones"):
            print("\n🔻 Captured Stones:")
            print(f"   - Black Captured: {step['captured_stones']['black']}")
            print(f"   - White Captured: {step['captured_stones']['white']}")

        print("\n" + "-" * 60)  # Divider for clarity


# Run the game
if __name__ == "__main__":
    run_go_game(agent=GoAgent(config=GoAgentConfig()))
