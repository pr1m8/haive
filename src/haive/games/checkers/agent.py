# src/haive/agents/agent_games/checkers/agent.py

from typing import Dict, Any
from langgraph.types import Command
from langgraph.graph import END
from src.haive.games.framework.base import GameAgent
from src.haive.games.checkers.models import CheckersMove, CheckersPlayerDecision
from src.haive.games.checkers.state import CheckersState
from src.haive.games.checkers.state_manager import CheckersStateManager
from src.haive.games.checkers.config import CheckersAgentConfig
from src.haive.core.engine.agent.agent import register_agent
from src.haive.core.graph.GraphBuilder import DynamicGraph
import time

@register_agent(CheckersAgentConfig)
class CheckersAgent(GameAgent[CheckersAgentConfig]):
    """Agent for playing checkers."""
    
    def __init__(self, config: CheckersAgentConfig):
        self.state_manager = CheckersStateManager
        super().__init__(config)

    def initialize_game(self, state: Dict[str, Any]) -> Command:
        game_state = self.state_manager.initialize()
        return Command(update=game_state, goto="player1_move")

    def prepare_move_context(self, state: CheckersState, player: str) -> Dict[str, Any]:
        legal_moves = self.state_manager.get_legal_moves(state)
        formatted_legal_moves = [str(move) for move in legal_moves]
        player_analysis = None
        if player == "red" and state.red_analysis:
            player_analysis = state.red_analysis[-1]
        elif player == "black" and state.black_analysis:
            player_analysis = state.black_analysis[-1]
        return {
            "board": state.board_string,
            "turn": state.turn,
            "color": player,
            "legal_moves": formatted_legal_moves,
            "captured_red": state.captured_pieces["red"],
            "captured_black": state.captured_pieces["black"],
            "move_history": [str(move) for move in state.move_history[-5:]],
            "player_analysis": player_analysis
        }

    def prepare_analysis_context(self, state: CheckersState, player: str) -> Dict[str, Any]:
        return {
            "board": state.board_string,
            "turn": state.turn,
            "color": player,
            "captured_red": state.captured_pieces["red"],
            "captured_black": state.captured_pieces["black"],
            "move_history": [str(move) for move in state.move_history[-5:]]
        }

    def extract_move(self, response: CheckersPlayerDecision) -> CheckersMove:
        return response.move

    def make_player1_move(self, state: Dict[str, Any]) -> Command:
        state_obj = state if isinstance(state, CheckersState) else CheckersState(**state)
        if state_obj.turn != "red":
            goto = "analyze_player1" if state_obj.turn == "black" else "player2_move"
            return Command(update=state_obj.model_dump(), goto=goto)
        return self.make_move(state_obj, "red")

    def make_player2_move(self, state: Dict[str, Any]) -> Command:
        state_obj = state if isinstance(state, CheckersState) else CheckersState(**state)
        if state_obj.turn != "black":
            goto = "analyze_player2" if state_obj.turn == "red" else "player1_move"
            return Command(update=state_obj.model_dump(), goto=goto)
        return self.make_move(state_obj, "black")

    def make_move(self, state: CheckersState, player: str) -> Command:
        if state.turn != player:
            return Command(update=state.model_dump(), goto=f"analyze_{player}")

        context = self.prepare_move_context(state, player)
        engine = self.engines.get(f"{player}_player")
        if not engine:
            raise ValueError(f"Missing engine for {player}_player")

        try:
            move_decision = engine.invoke(context)
            move = self.extract_move(move_decision)
            legal_moves = self.state_manager.get_legal_moves(state)
            valid_move = next((m for m in legal_moves if str(m) == str(move)), None)

            if valid_move:
                updated_state = self.state_manager.apply_move(state, valid_move)
            else:
                fallback_move = legal_moves[0] if legal_moves else None
                if fallback_move:
                    updated_state = self.state_manager.apply_move(state, fallback_move)
                else:
                    return Command(update={"game_status": "game_over"}, goto=END)
        except Exception as e:
            print(f"Error making move: {e}")
            legal_moves = self.state_manager.get_legal_moves(state)
            fallback_move = legal_moves[0] if legal_moves else None
            if fallback_move:
                updated_state = self.state_manager.apply_move(state, fallback_move)
            else:
                return Command(update={"game_status": "game_over"}, goto=END)

        if updated_state.game_status == 'game_over' or updated_state.winner:
            return Command(update=updated_state.model_dump(), goto=END)

        goto = "analyze_player2" if player == "red" else "analyze_player1"
        return Command(update=updated_state.model_dump(), goto=goto)

    def analyze_player1(self, state: Dict[str, Any]) -> Command:
        state_obj = state if isinstance(state, CheckersState) else CheckersState(**state)
        if state_obj.turn != "red":
            return Command(update=state_obj.model_dump(), goto="player1_move")
        return self.analyze_position(state_obj, "red")

    def analyze_player2(self, state: Dict[str, Any]) -> Command:
        state_obj = state if isinstance(state, CheckersState) else CheckersState(**state)
        if state_obj.turn != "black":
            return Command(update=state_obj.model_dump(), goto="player2_move")
        return self.analyze_position(state_obj, "black")

    def analyze_position(self, state: CheckersState, player: str) -> Command:
        if state.turn != player:
            return Command(update=state.model_dump(), goto=f"{player}_move")

        context = self.prepare_analysis_context(state, player)
        engine = self.engines.get(f"{player}_analyzer")
        if not engine:
            raise ValueError(f"Missing engine for {player}_analyzer")

        try:
            analysis = engine.invoke(context)
            updated_state = self.state_manager.update_analysis(state, analysis, player)
        except Exception as e:
            print(f"Error during analysis: {e}")
            updated_state = state

        return Command(update=updated_state.model_dump(), goto=f"{player}_move")

    def visualize_state(self, state: Dict[str, Any]) -> None:
        checker_state = state if isinstance(state, CheckersState) else CheckersState(**state)
        print("\n" + "=" * 50)
        print(f"🎮 Current Player: {checker_state.turn.upper()}")
        print(f"📌 Game Status: {checker_state.game_status}")
        print("=" * 50)
        print("\n" + checker_state.board_string)
        print(f"\n🔴 Red Captures: {checker_state.captured_pieces.get('red', [])}")
        print(f"⚫ Black Captures: {checker_state.captured_pieces.get('black', [])}")
        if checker_state.move_history:
            print(f"\n📝 Last Move: {checker_state.move_history[-1]}")
        if checker_state.red_analysis and checker_state.turn == 'black':
            a = checker_state.red_analysis[-1]
            print("\n🔍 Red's Analysis:")
            print(f"   - Material Advantage: {a.get('material_advantage', 'N/A')}")
            print(f"   - Center Control: {a.get('control_of_center', 'N/A')}")
            print(f"   - Suggested Moves: {', '.join(a.get('suggested_moves', []))}")
        if checker_state.black_analysis and checker_state.turn == 'red':
            a = checker_state.black_analysis[-1]
            print("\n🔍 Black's Analysis:")
            print(f"   - Material Advantage: {a.get('material_advantage', 'N/A')}")
            print(f"   - Center Control: {a.get('control_of_center', 'N/A')}")
            print(f"   - Suggested Moves: {', '.join(a.get('suggested_moves', []))}")
        time.sleep(0.5)

    def run_game(self, visualize: bool = False) -> Dict[str, Any]:
        if visualize:
            initial_state = self.state_manager.initialize()
            try:
                for step in self.app.stream(initial_state, stream_mode="values", debug=True, config=self.runnable_config):
                    self.visualize_state(step)
                    time.sleep(1)
                return step
            except Exception as e:
                print(f"Error running game: {e}")
                return {}
        else:
            return self.run({})

    def setup_workflow(self) -> None:
        gb = DynamicGraph(components=[self.config], state_schema=self.config.state_schema)
        gb.add_node("initialize", self.initialize_game)
        gb.add_node("player1_move", self.make_player1_move)
        gb.add_node("player2_move", self.make_player2_move)
        gb.add_node("analyze_player1", self.analyze_player1)
        gb.add_node("analyze_player2", self.analyze_player2)
        gb.add_edge("initialize", "player1_move")
        gb.add_edge("player1_move", "analyze_player2")
        gb.add_edge("analyze_player2", "player2_move")
        gb.add_edge("player2_move", "analyze_player1")
        gb.add_edge("analyze_player1", "player1_move")
        self.graph = gb.build()
