from src.haive.games.reversi.config import ReversiConfig
from src.haive.games.reversi.state import ReversiState
from src.haive.games.reversi.models import ReversiMove, ReversiAnalysis
from src.haive.games.reversi.state_manager import ReversiStateManager
from src.haive.core.engine.agent.agent import register_agent,Agent
from src.haive.core.graph.GraphBuilder import DynamicGraph
from typing import Dict, Any, List, Optional, Tuple
import time 
from langgraph.types import Command
from src.haive.games.framework.base.agent import GameAgent
@register_agent(ReversiConfig)
class ReversiAgent(GameAgent[ReversiConfig]):
    """Agent for playing Reversi/Othello."""
    
    def __init__(self, config: ReversiConfig = ReversiConfig()):
        """
        Initialize the Reversi agent with game configuration and state manager.

        Args:
            config (ReversiConfig): Configuration object defining player settings,
                engines, first player, visualization preference, and analysis options.
        """
        self.state_manager = ReversiStateManager
        super().__init__(config)
    def initialize_game(self, state: Dict[str, Any]) -> Command:
        """
        Initialize a new Reversi game by constructing the initial game state.

        Args:
            state (Dict[str, Any]): Placeholder for incoming LangGraph state (not used directly).

        Returns:
            Command: Command containing the serialized initial ReversiState.
        """
        game_state = self.state_manager.initialize(
            first_player=self.config.first_player,
            player_B=self.config.player_B,
            player_W=self.config.player_W
        )
        return Command(update=game_state.model_dump() if hasattr(game_state, "model_dump") else game_state.dict())
    
    def prepare_move_context(self, state: ReversiState) -> Dict[str, Any]:
        """
        Prepare the prompt context used by the move generation engine.

        Args:
            state (ReversiState): The current game state.

        Returns:
            Dict[str, Any]: A dictionary containing the board string, legal move list,
                            current player turn, and the player's last analysis (if any).
        """
        # Format legal moves
        legal_moves = self.state_manager.get_legal_moves(state)
        formatted_legal_moves = ", ".join([f"({move.row}, {move.col})" for move in legal_moves])
        
        # Get player's analysis if available
        current_player = "player1" if (state.turn == "B" and state.player_B == "player1") or (state.turn == "W" and state.player_W == "player1") else "player2"
        player_analysis = None
        
        if current_player == "player1" and state.player1_analysis:
            player_analysis = state.player1_analysis[-1]
        elif current_player == "player2" and state.player2_analysis:
            player_analysis = state.player2_analysis[-1]
        
        if not player_analysis:
            player_analysis = "No previous analysis available."
        
        # Prepare the context
        return {
            "board_string": state.board_string,
            "current_player": state.turn,
            "legal_moves": formatted_legal_moves,
            "player_analysis": player_analysis
        }
    
    def prepare_analysis_context(self, state: ReversiState, symbol: str) -> Dict[str, Any]:
        """
        Prepare the prompt context for board analysis by the strategy engine.

        Args:
            state (ReversiState): The current game state.
            symbol (str): Player symbol ('B' or 'W') for whom to analyze the board.

        Returns:
            Dict[str, Any]: A dictionary of analysis context including:
                - board string
                - player/opponent symbols
                - color labels
                - legal moves
                - current disc counts
        """
        # Format legal moves
        legal_moves = self.state_manager.get_legal_moves(state)
        formatted_legal_moves = ", ".join([f"({move.row}, {move.col})" for move in legal_moves])
        
        # Get disc counts
        counts = state.disc_count
        player_color = "Black" if symbol == "B" else "White"
        opponent_color = "White" if symbol == "B" else "Black"

        return {
            "board_string": state.board_string,
            "player_symbol": symbol,
            "opponent_symbol": "W" if symbol == "B" else "B",
            "player_color": player_color,
            "opponent_color": opponent_color,
            "legal_moves": formatted_legal_moves,
            "black_count": counts["B"],
            "white_count": counts["W"]
        }

    
    def extract_move(self, response: Any) -> ReversiMove:
        """
        Extract a ReversiMove object from an engine response.

        Args:
            response (Any): Output returned from the LLM engine. Assumed to already be
                parsed into a ReversiMove object via structured output.

        Returns:
            ReversiMove: The move selected by the engine.
        """

        # The response should already be a ReversiMove object
        return response
    
    def make_B_move(self, state: ReversiState) -> Command:
        """
        Make a move for player B (Black).

        Args:
            state (ReversiState): The current game state.

        Returns:
            Command: Command containing the updated ReversiState.
        """
        if state.turn != "B" or state.game_status != "ongoing":
            return Command(update=state.model_dump() if hasattr(state, "model_dump") else state.dict())
        
        # Check if Black has legal moves
        legal_moves = self.state_manager.get_legal_moves(state)
        if not legal_moves:
            # No legal moves, must skip turn
            new_state = self.state_manager.get_skip_move(state)
            return Command(update=new_state.model_dump() if hasattr(new_state, "model_dump") else new_state.dict())
        
        # Prepare context for the move
        context = self.prepare_move_context(state)
        
        # Get the B player engine
        engine = self.engines["B_player"]
        
        # Generate move
        move = engine.invoke(context)
        
        # Apply the move
        new_state = self.state_manager.apply_move(state, move)
        
        # Return the updated state
        return Command(update=new_state.model_dump() if hasattr(new_state, "model_dump") else new_state.dict())
    
    def make_W_move(self, state: ReversiState) -> Command:
        """
        Make a move for player W (White).

        Args:
            state (ReversiState): The current game state.

        Returns:    
            Command: Command containing the updated ReversiState.
        """
        if state.turn != "W" or state.game_status != "ongoing":
            return Command(update=state.model_dump() if hasattr(state, "model_dump") else state.dict())
        
        # Check if White has legal moves
        legal_moves = self.state_manager.get_legal_moves(state)
        if not legal_moves:
            # No legal moves, must skip turn
            new_state = self.state_manager.get_skip_move(state)
            return Command(update=new_state.model_dump() if hasattr(new_state, "model_dump") else new_state.dict())
        
        # Prepare context for the move
        context = self.prepare_move_context(state)
        
        # Get the W player engine
        engine = self.engines["W_player"]
        
        # Generate move
        move = engine.invoke(context)
        
        # Apply the move
        new_state = self.state_manager.apply_move(state, move)
        
        # Return the updated state
        return Command(update=new_state.model_dump() if hasattr(new_state, "model_dump") else new_state.dict())
    
    def analyze_B(self, state: ReversiState) -> Command:
        """
        Analyze position for player B (Black).

        Args:
            state (ReversiState): The current game state.

        Returns:
            Command: Command containing the updated ReversiState.
        """
        if not self.config.enable_analysis or state.game_status != "ongoing":
            return Command(update=state.model_dump() if hasattr(state, "model_dump") else state.dict())
        # Prepare context for analysis
        context = self.prepare_analysis_context(state, "B")
        
        # Get the B analyzer engine
        engine = self.engines["B_analyzer"]
        
        # Generate analysis
        analysis = engine.invoke(context)
        
        # Determine which player is B
        player = state.player_B
        
        # Update state with analysis
        new_state = self.state_manager.add_analysis(state, player, analysis)
        
        # Return the updated state
        return Command(update=new_state.model_dump() if hasattr(new_state, "model_dump") else new_state.dict())
    
    def analyze_W(self, state: ReversiState) -> Command:
        """
        Analyze position for player W (White).

        Args:
            state (ReversiState): The current game state.

        Returns:
            Command: Command containing the updated ReversiState.
        """
        if not self.config.enable_analysis or state.game_status != "ongoing":
            return Command(update=state.model_dump() if hasattr(state, "model_dump") else state.dict())
        # Prepare context for analysis
        context = self.prepare_analysis_context(state, "W")
        
        # Get the W analyzer engine
        engine = self.engines["W_analyzer"]
        
        # Generate analysis
        analysis = engine.invoke(context)
        
        # Determine which player is W
        player = state.player_W
        
        # Update state with analysis
        new_state = self.state_manager.add_analysis(state, player, analysis)
        
        # Return the updated state
        return Command(update=new_state.model_dump() if hasattr(new_state, "model_dump") else new_state.dict())
    
    def visualize_state(self, state: Dict[str, Any]) -> None:
        """
        Visualize the current game state.

        Args:
            state (Dict[str, Any]): The current game state.

        Returns:
            None
        """
        if not self.config.visualize:
            return
        # Create a ReversiState from the dict
        game_state = ReversiState(**state)
        
        print("\n" + "=" * 50)
        print(f"🎮 Game Status: {game_state.game_status}")
        if game_state.game_status == "ongoing":
            print(f"Current Turn: {game_state.turn} ({'Black' if game_state.turn == 'B' else 'White'} - "
                  f"{game_state.player_B if game_state.turn == 'B' else game_state.player_W})")
        elif game_state.game_status == "draw":
            print("Game ended in a draw!")
        elif game_state.game_status.endswith("_win"):
            winner_symbol = game_state.game_status.split("_")[0]
            winner_player = game_state.player_B if winner_symbol == "B" else game_state.player_W
            print(f"🏆 Winner: {winner_symbol} ({'Black' if winner_symbol == 'B' else 'White'} - {winner_player})")
        
        # Print disc count
        counts = game_state.disc_count
        print(f"Black: {counts['B']} discs, White: {counts['W']} discs")
        print("=" * 50)
        
        # Print the board
        print("\n" + game_state.board_string)
        
        # Print last move if available
        if game_state.move_history:
            last_move = game_state.move_history[-1]
            print(f"\n📝 Last Move: {str(last_move)}")
        
        # Print analyses if available
        current_player = game_state.player_B if game_state.turn == "B" else game_state.player_W
        
        if current_player == "player1" and game_state.player2_analysis:
            # Show player2's last analysis after their move
            last_analysis = game_state.player2_analysis[-1]
            print(f"\n🔍 Previous Player's Analysis:")
            print(f"Position evaluation: {last_analysis['position_evaluation']}")
            print(f"Mobility: {last_analysis['mobility']}, Corner discs: {last_analysis['corner_discs']}")
            print(f"Stable discs: {last_analysis['stable_discs']}, Frontier discs: {last_analysis['frontier_discs']}")
            print(f"Positional score: {last_analysis['positional_score']}")
            print(f"Strategy: {last_analysis['strategy']}")
            if last_analysis['recommended_moves']:
                print(f"Recommended moves: {', '.join([str(m) for m in last_analysis['recommended_moves']])}")
            
        elif current_player == "player2" and game_state.player1_analysis:
            # Show player1's last analysis after their move
            last_analysis = game_state.player1_analysis[-1]
            print(f"\n🔍 Previous Player's Analysis:")
            print(f"Position evaluation: {last_analysis['position_evaluation']}")
            print(f"Mobility: {last_analysis['mobility']}, Corner discs: {last_analysis['corner_discs']}")
            print(f"Stable discs: {last_analysis['stable_discs']}, Frontier discs: {last_analysis['frontier_discs']}")
            print(f"Positional score: {last_analysis['positional_score']}")
            print(f"Strategy: {last_analysis['strategy']}")
            if last_analysis['recommended_moves']:
                print(f"Recommended moves: {', '.join([str(m) for m in last_analysis['recommended_moves']])}")
        
        # Add a short delay for readability
        time.sleep(0.5)
    
    def setup_workflow(self) -> None:
        """Set up the game workflow.

        Returns:
            None
        """
        # Create a graph builder
        builder = DynamicGraph(state_schema=self.state_schema)
        
        # Add nodes for the main game flow
        builder.add_node("initialize", self.initialize_game)
        builder.add_node("make_B_move", self.make_B_move)
        builder.add_node("make_W_move", self.make_W_move)
        builder.add_node("analyze_B", self.analyze_B)
        builder.add_node("analyze_W", self.analyze_W)
        
        # Set up the game flow
        builder.add_edge("initialize", "make_B_move" if self.config.first_player == "B" else "make_W_move")
        
        # B's turn flow
        builder.add_edge("make_B_move", "analyze_B")
        builder.add_edge("analyze_B", "make_W_move")
        
        # W's turn flow
        builder.add_edge("make_W_move", "analyze_W")
        builder.add_edge("analyze_W", "make_B_move")
        
        # Build the graph
        self.graph = builder.build()
        
        # Compile the workflow
        #self.compile()


        
    def run_game(self, visualize: bool = True) -> Dict[str, Any]:
        """
        Run a complete Reversi game with visualization.
        
        Args:
            visualize: Whether to visualize each game state
            
        Returns:
            Final game state
        """
        # Create an empty input state to start the game
        input_state = ReversiStateManager.initialize()
        # Set up visualization if requested
        if visualize:
            # Run the game step by step with visualization
            for step_result in self.stream(input_state, stream_mode="values"):
                # Visualize the current state
                self.visualize_state(step_result)
            
            # Return the final state
            return step_result
        else:
            # Run the game without visualization
            return super().run(input_state)


# Initialize the agent
#a = ReversiAgent()
#a.run_game(visualize=True)
# Run the game with visualization
#final_state = a.run_game(visualize=True)

# Print the winner
#if final_state.get("game_status", "") == "draw":
#     print("\nGame ended in a draw!")
# elif final_state.get("game_status", "").endswith("_win"):
#     winner_symbol = final_state["game_status"].split("_")[0]
#     winner_player = final_state["player_B"] if winner_symbol == "B" else final_state["player_W"]
#     print(f"\nWinner: {winner_symbol} ({'Black' if winner_symbol == 'B' else 'White'} - {winner_player})")