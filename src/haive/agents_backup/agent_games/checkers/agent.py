from src.haive.agents.base import AgentArchitecture, AgentArchitectureConfig
from src.haive.core.aug_llm.base import compose_runnable
from langgraph.graph import StateGraph
from langgraph.types import Command
from langgraph.constants import START, END
from src.haive.agents.agent_games.checkers.state import CheckersGameStateManager, CheckersGameState
from src.haive.agents.agent_games.checkers.models import CheckersMove, CheckersPlayerAnalysis
from src.haive.agents.agent_games.checkers.aug_llms import aug_llm_configs
from typing import Dict
from pydantic import Field


class CheckersAgentConfig(AgentArchitectureConfig):
    """Configuration for the Checkers agent."""
    state_schema: type = Field(default=CheckersGameState)
    aug_llm_configs: Dict[str, object] = Field(
        default=aug_llm_configs,
        description="LLM configurations for checkers"
    )
    should_visualize_graph: bool = Field(
        default=True, description="Whether to visualize the agent's decision flow"
    )
    graph_name: str = Field(
        default="checkers_game.png", description="Graph file name"
    )


class CheckersAgent(AgentArchitecture):
    def __init__(self, config: CheckersAgentConfig):
        super().__init__(config)
        
        # ✅ Setup Augmented LLMs
        self.llms = {name: compose_runnable(cfg) for name, cfg in config.aug_llm_configs.items()}

        # ✅ Ensure LLMs are valid
        for key, llm in self.llms.items():
            if llm is None:
                raise ValueError(f"Failed to compose LLM for {key}")

    def setup_workflow(self):
        """Sets up the game flow using a state graph."""
        self.graph.add_node("initialize_game", self.initialize_game)
        self.graph.add_node("red_analysis", self.analyze_red_position)
        self.graph.add_node("red_move", self.make_red_move)
        self.graph.add_node("black_analysis", self.analyze_black_position)
        self.graph.add_node("black_move", self.make_black_move)
        self.graph.add_node("check_game_status", self.check_game_status)

        # ✅ Game Initialization
        self.graph.add_edge(START, "initialize_game")
        self.graph.add_edge("initialize_game", "red_analysis")

        # ✅ Red Player Turn
        self.graph.add_edge("red_analysis", "red_move")
        self.graph.add_conditional_edges(
            "red_move", self.should_continue_game, {True: "black_analysis", False: END}
        )

        # ✅ Black Player Turn
        self.graph.add_edge("black_analysis", "black_move")
        self.graph.add_conditional_edges(
            "black_move", self.should_continue_game, {True: "red_analysis", False: END}
        )

    def initialize_game(self, state: CheckersGameState) -> Command:
        """Initializes a new Checkers game."""
        return Command(update=CheckersGameStateManager.initialize().dict())

    def make_move(self, state: CheckersGameState, color: str) -> Command:
        """Handles move execution for a player (red/black)."""
        player_llm = self.llms.get(f"{color}_player")
        if player_llm is None:
            raise ValueError(f"Missing LLM for {color}_player")

        move_response = player_llm.invoke({
            "board_state": state.board_state,
            "move_history": state.move_history[-5:],
            "color": color,
            "captured_pieces": state.captured_pieces,
        })

        move = move_response.move
        new_state = CheckersGameStateManager.apply_move(state, move)

        return Command(update=new_state.dict())

    def analyze_position(self, state: CheckersGameState, color: str) -> Command:
        """Analyzes the board position for the given player (red/black)."""
        analyzer_key = f"{color}_analyzer"
        if analyzer_key not in self.llms:
            raise ValueError(f"Missing LLM for {analyzer_key}")

        analysis = self.llms[analyzer_key].invoke({
            "board_state": state.board_state,
            "move_history": state.move_history[-5:],
            "captured_pieces": state.captured_pieces,
            "color": color,
        })

        return Command(update={f"{color}_analysis": state.dict().get(f"{color}_analysis", [])[-4:] + [analysis.dict()]})

    def check_game_status(self, state: CheckersGameState) -> Command:
        """Checks if the game has ended."""
        status = CheckersGameStateManager.check_game_end(state)
        return Command(update={"game_status": status})

    def should_continue_game(self, state: CheckersGameState) -> bool:
        """Determines if the game should continue."""
        return state.game_status == "ongoing"

    def make_red_move(self, state: CheckersGameState) -> Command:
        return self.make_move(state, "red")

    def make_black_move(self, state: CheckersGameState) -> Command:
        return self.make_move(state, "black")

    def analyze_red_position(self, state: CheckersGameState) -> Command:
        return self.analyze_position(state, "red")

    def analyze_black_position(self, state: CheckersGameState) -> Command:
        return self.analyze_position(state, "black")
