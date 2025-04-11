"""
Tic Tac Toe Agent class for coordinating gameplay using LLM-driven decision-making.

This module defines the agent responsible for initializing the game,
coordinating turns, running inference engines, and maintaining the gameplay loop.
"""

from src.haive.games.tic_tac_toe.config import TicTacToeConfig
from src.haive.games.tic_tac_toe.state import TicTacToeState
from src.haive.games.tic_tac_toe.models import TicTacToeMove
from src.haive.games.tic_tac_toe.state_manager import TicTacToeStateManager
from src.haive.games.framework.base.agent import GameAgent
from src.haive.core.graph.GraphBuilder import DynamicGraph
from typing import Dict, Any, List, Optional, Tuple
import time 
from langgraph.types import Command
from src.haive.core.engine.agent.agent import register_agent
from langgraph.graph import END,START

@register_agent(TicTacToeConfig)
class TicTacToeAgent(GameAgent[TicTacToeConfig]):
    """
    Agent for playing Tic Tac Toe using structured game flow and LLM inference.

    Responsibilities:
    - Manage game initialization and state updates
    - Coordinate X and O player engines to make moves
    - Optionally analyze game states between turns
    - Visualize board state and strategies
    """

    def __init__(self, config: TicTacToeConfig = TicTacToeConfig()):
        """
        Initialize the Tic Tac Toe agent.

        Args:
            config (TicTacToeConfig): Configuration object for the agent.
        """
        self.state_manager = TicTacToeStateManager
        super().__init__(config)

    def initialize_game(self, state: Dict[str, Any]) -> Command:
        """
        Initialize a new Tic Tac Toe game.

        Args:
            state (Dict[str, Any]): Initial state input (usually ignored).

        Returns:
            Command: Wrapped initial game state.
        """
        game_state = self.state_manager.initialize(
            first_player=self.config.first_player,
            player_X=self.config.player_X,
            player_O=self.config.player_O
        )
        return Command(update=game_state.model_dump() if hasattr(game_state, "model_dump") else game_state.dict())

    def prepare_move_context(self, state: TicTacToeState) -> Dict[str, Any]:
        """
        Prepare structured context for generating a move.

        Args:
            state (TicTacToeState): Current game state.

        Returns:
            Dict[str, Any]: Context dictionary with board info, legal moves, and last analysis.
        """
        legal_moves = self.state_manager.get_legal_moves(state)
        formatted_legal_moves = ", ".join([f"({move.row}, {move.col})" for move in legal_moves])

        current_player = "player1" if (state.turn == "X" and state.player_X == "player1") or (state.turn == "O" and state.player_O == "player1") else "player2"
        player_analysis = None

        if current_player == "player1" and state.player1_analysis:
            player_analysis = state.player1_analysis[-1]
        elif current_player == "player2" and state.player2_analysis:
            player_analysis = state.player2_analysis[-1]

        if not player_analysis:
            player_analysis = "No previous analysis available."

        return {
            "board_string": state.board_string,
            "current_player": state.turn,
            "legal_moves": formatted_legal_moves,
            "player_analysis": player_analysis
        }

    def prepare_analysis_context(self, state: TicTacToeState, symbol: str) -> Dict[str, Any]:
        """
        Prepare structured context for analyzing the game board.

        Args:
            state (TicTacToeState): Current game state.
            symbol (str): The player symbol ('X' or 'O').

        Returns:
            Dict[str, Any]: Context dictionary for analysis prompt.
        """
        return {
            "board_string": state.board_string,
            "player_symbol": symbol,
            "opponent_symbol": "O" if symbol == "X" else "X"
        }

    def extract_move(self, response: Any) -> TicTacToeMove:
        """
        Extract a TicTacToeMove object from the LLM engine's response.

        Args:
            response (Any): The raw response returned from the engine.

        Returns:
            TicTacToeMove: A move object representing the player's intended action.
        """
        return response

    def make_X_move(self, state: TicTacToeState) -> Command:
        """
        Perform a move as player X, invoking the configured LLM engine.

        Args:
            state (TicTacToeState): The current game state.

        Returns:
            Command: Updated game state after applying X's move.
        """
        if state.turn != "X" or state.game_status != "ongoing":
            return Command(update=state.model_dump() if hasattr(state, "model_dump") else state.dict())

        context = self.prepare_move_context(state)
        engine = self.engines["X_player"]
        move = engine.invoke(context)
        new_state = self.state_manager.apply_move(state, move)
        return Command(update=new_state.model_dump() if hasattr(new_state, "model_dump") else new_state.dict())

    def make_O_move(self, state: TicTacToeState) -> Command:
        """
        Perform a move as player O, invoking the configured LLM engine.

        Args:
            state (TicTacToeState): The current game state.

        Returns:
            Command: Updated game state after applying O's move.
        """
        if state.turn != "O" or state.game_status != "ongoing":
            return Command(update=state.model_dump() if hasattr(state, "model_dump") else state.dict())

        context = self.prepare_move_context(state)
        engine = self.engines["O_player"]
        move = engine.invoke(context)
        new_state = self.state_manager.apply_move(state, move)
        return Command(update=new_state.model_dump() if hasattr(new_state, "model_dump") else new_state.dict())

    def analyze_X(self, state: TicTacToeState) -> Command:
        """
        Perform board analysis for player X using the analysis engine.

        Args:
            state (TicTacToeState): The current game state.

        Returns:
            Command: Updated state containing player X's analysis.
        """
        if not self.config.enable_analysis or state.game_status != "ongoing":
            return Command(update=state.model_dump() if hasattr(state, "model_dump") else state.dict())

        context = self.prepare_analysis_context(state, "X")
        engine = self.engines["X_analyzer"]
        analysis = engine.invoke(context)
        player = state.player_X
        new_state = self.state_manager.add_analysis(state, player, analysis)
        return Command(update=new_state.model_dump() if hasattr(new_state, "model_dump") else new_state.dict())

    def analyze_O(self, state: TicTacToeState) -> Command:
        """
        Perform board analysis for player O using the analysis engine.

        Args:
            state (TicTacToeState): The current game state.

        Returns:
            Command: Updated state containing player O's analysis.
        """
        if not self.config.enable_analysis or state.game_status != "ongoing":
            return Command(update=state.model_dump() if hasattr(state, "model_dump") else state.dict())

        context = self.prepare_analysis_context(state, "O")
        engine = self.engines["O_analyzer"]
        analysis = engine.invoke(context)
        player = state.player_O
        new_state = self.state_manager.add_analysis(state, player, analysis)
        return Command(update=new_state.model_dump() if hasattr(new_state, "model_dump") else new_state.dict())
    def visualize_state(self, state: Dict[str, Any]) -> None:
        """
        Visualize the current game state with board, status, and analysis highlights.

        Args:
            state (Dict[str, Any]): The latest state dictionary to visualize.
        """
        if not self.config.visualize:
            return

        game_state = TicTacToeState(**state)

        print("\n" + "=" * 50)
        print(f"\U0001F3AE Game Status: {game_state.game_status}")
        if game_state.game_status == "ongoing":
            print(f"Current Turn: {game_state.turn} ({game_state.player_X if game_state.turn == 'X' else game_state.player_O})")
        elif game_state.game_status == "draw":
            print("Game ended in a draw!")
        elif game_state.game_status.endswith("_win"):
            winner_symbol = game_state.game_status.split("_")[0]
            winner_player = game_state.player_X if winner_symbol == "X" else game_state.player_O
            print(f"\U0001F3C6 Winner: {winner_symbol} ({winner_player})")
        print("=" * 50)

        print("\n" + game_state.board_string)

        if game_state.move_history:
            last_move = game_state.move_history[-1]
            print(f"\n\U0001F4DD Last Move: {str(last_move)}")

        current_player = game_state.player_X if game_state.turn == "X" else game_state.player_O

        if current_player == "player1" and game_state.player2_analysis:
            last_analysis = game_state.player2_analysis[-1]
            print(f"\n\U0001F50D Previous Player's Analysis:")
            print(f"Position evaluation: {last_analysis['position_evaluation']}")
            if last_analysis['winning_moves']:
                print(f"Winning moves: {', '.join([str(m) for m in last_analysis['winning_moves']])}")
            if last_analysis['blocking_moves']:
                print(f"Blocking moves: {', '.join([str(m) for m in last_analysis['blocking_moves']])}")
            if last_analysis['fork_opportunities']:
                print(f"Fork opportunities: {', '.join([str(m) for m in last_analysis['fork_opportunities']])}")
            if last_analysis['recommended_move']:
                print(f"Recommended move: {last_analysis['recommended_move']}")

        elif current_player == "player2" and game_state.player1_analysis:
            last_analysis = game_state.player1_analysis[-1]
            print(f"\n\U0001F50D Previous Player's Analysis:")
            print(f"Position evaluation: {last_analysis['position_evaluation']}")
            if last_analysis['winning_moves']:
                print(f"Winning moves: {', '.join([str(m) for m in last_analysis['winning_moves']])}")
            if last_analysis['blocking_moves']:
                print(f"Blocking moves: {', '.join([str(m) for m in last_analysis['blocking_moves']])}")
            if last_analysis['fork_opportunities']:
                print(f"Fork opportunities: {', '.join([str(m) for m in last_analysis['fork_opportunities']])}")
            if last_analysis['recommended_move']:
                print(f"Recommended move: {last_analysis['recommended_move']}")

        time.sleep(0.5)

    

    def setup_workflow(self):
        builder = DynamicGraph(state_schema=self.state_schema)

        builder.add_node("initialize", self.initialize_game)
        builder.add_node("make_X_move", self.make_X_move)
        builder.add_node("analyze_X", self.analyze_X)
        builder.add_node("make_O_move", self.make_O_move)
        builder.add_node("analyze_O", self.analyze_O)

        # Regular edges
        builder.add_edge("initialize", "make_X_move" if self.config.first_player == "X" else "make_O_move")

        builder.add_conditional_edges(
            "make_X_move",
            self._check_continue_or_end,  # <- your new branching function
            {
                "analyze_X": "analyze_X",
                "end": END,
            }
        )

        builder.add_conditional_edges(
            "make_O_move",
            self._check_continue_or_end,
            {
                "analyze_X": "analyze_X",
                "end": END,
            }
        )

        #builder.add_edge("analyze_X", "make_O_move")
        #builder.add_edge("analyze_O", "make_X_move")

        self.graph = builder.build()

    def _check_continue_or_end(self, state: TicTacToeState) -> str:
        if state.game_status in ("ongoing",):
            return "analyze_O" if state.turn == "X" else "analyze_X"
        return "end"

    def run_game(self, visualize: bool = True) -> Dict[str, Any]:
        """
        Run the full Tic Tac Toe game loop.

        Args:
            visualize (bool): Whether to print out the game state after each move.

        Returns:
            Dict[str, Any]: Final game state at the end of the session.
        """
        initial_state = TicTacToeStateManager.initialize(
            first_player=self.config.first_player,
            player_X=self.config.player_X,
            player_O=self.config.player_O
        )

        if visualize:
            for step in self.stream(initial_state, stream_mode="values"):
                self.visualize_state(step)
            return step
        else:
            return super().run(initial_state)

#agent = TicTacToeAgent()
#agent.run_game(visualize=True)
