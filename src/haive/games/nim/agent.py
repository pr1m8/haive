"""
Agent for playing Nim.

This module defines the Nim agent, which uses language models
to generate moves and analyze positions in the game.
"""
from src.haive.games.nim.config import NimConfig
from src.haive.games.nim.state import NimState
from src.haive.games.nim.state_manager import NimStateManager
from src.haive.games.framework.base.agent import GameAgent
from src.haive.core.graph.GraphBuilder import DynamicGraph
from typing import Dict, Any, Optional
import time 
from langgraph.types import Command

class NimAgent(GameAgent[NimConfig]):
    """Agent for playing Nim.
    """
    
    def __init__(self, config: NimConfig = NimConfig()):
        """Initialize the Nim agent.

        Args:
            config (NimConfig): The configuration for the game.
        """
      
        self.state_manager = NimStateManager
        super().__init__(config)
    
    def initialize_game(self, state: Dict[str, Any]) -> Command:
        """Initialize a new Nim game with configured pile sizes.

        Args:
            state (Dict[str, Any]): The initial state of the game.

        Returns:
            Command: The command to initialize the game.
        """
        game_state = self.state_manager.initialize(pile_sizes=self.config.pile_sizes)
        # Set misere mode from src.config
        game_state.misere_mode = self.config.misere_mode
        return Command(update=game_state.model_dump() if hasattr(game_state, "model_dump") else game_state.dict())
    
    def prepare_move_context(self, state: NimState, player: str) -> Dict[str, Any]:
        """Prepare context for move generation.

        Args:
            state (NimState): The current game state.
            player (str): The player to prepare the context for.

        Returns:
            Dict[str, Any]: The context for the move generation.
        """
        # Format legal moves for display
        formatted_legal_moves = "\n".join([
            f"Take {move.stones_taken} stones from pile {move.pile_index} (current size: {state.piles[move.pile_index]})" 
            for move in self.state_manager.get_legal_moves(state)
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
    
    def extract_move(self, response: Any) -> Any:
        """Extract move from engine response.

        Args:
            response (Any): The response from the engine.

        Returns:
            Any: The move from the engine.
        """
        # The response should already be a NimMove object
        return response
    
    def make_player1_move(self, state: NimState) -> Command:
        """Make a move for player1.

        Args:
            state (NimState): The current game state.

        Returns:
            Command: The command to make the move.
        """
        return self.make_move(state, "player1")
    
    def make_player2_move(self, state: NimState) -> Command:
        """Make a move for player2.

        Args:
            state (NimState): The current game state.

        Returns:
            Command: The command to make the move.
        """
        return self.make_move(state, "player2")
    
    def make_move(self, state: NimState, player: str) -> Command:
        """Make a move for the specified player.

        Args:
            state (NimState): The current game state.
            player (str): The player to make the move for.

        Returns:
            Command: The command to make the move.
        """
        # Check if it's the player's turn
        
        # Prepare context for the move
        context = self.prepare_move_context(state, player)
        
        # Select the appropriate engine
        engine_key = f"{player}_player"
        engine = self.engines[engine_key]
        
        # Generate move
        move = engine.invoke(context)
        
        # Apply the move
        new_state = self.state_manager.apply_move(state, move)
        
        # Return the updated state
        return Command(update=new_state.model_dump() if hasattr(new_state, "model_dump") else new_state.dict())
    
    def prepare_analysis_context(self, state: NimState, player: str) -> Dict[str, Any]:
        """Prepare context for position analysis.

        Args:
            state (NimState): The current game state.
            player (str): The player to prepare the context for.

        Returns:
            Dict[str, Any]: The context for the position analysis.
        """
        return {
            "board_string": state.board_string,
            "player": player,
            "move_history": [str(move) for move in state.move_history[-5:]],
            "misere_mode": state.misere_mode,
            "nim_sum": state.nim_sum
        }
    
    def analyze_player1(self, state: NimState) -> Command:
        """Analyze position for player1.

        Args:
            state (NimState): The current game state.

        Returns:
            Command: The command to analyze the position.
        """
        return self.analyze_position(state, "player1")
    
    def analyze_player2(self, state: NimState) -> Command:
        """Analyze position for player2.

        Args:
            state (NimState): The current game state.

        Returns:
            Command: The command to analyze the position.
        """
        return self.analyze_position(state, "player2")
    
    def analyze_position(self, state: NimState, player: str) -> Command:
        """Analyze the current position for the specified player.

        Args:
            state (NimState): The current game state.
            player (str): The player to analyze the position for.

        Returns:
            Command: The command to analyze the position.
        """
        if not self.config.enable_analysis:
            return Command(update=state.model_dump() if hasattr(state, "model_dump") else state.dict())
        # Prepare context for analysis
        context = self.prepare_analysis_context(state, player)
        
        # Select the appropriate engine
        engine_key = f"{player}_analyzer"
        engine = self.engines[engine_key]
        
        # Generate analysis
        analysis = engine.invoke(context)
        
        # Update state with analysis
        new_state = self.state_manager.add_analysis(state, player, analysis)
        
        # Return the updated state
        return Command(update=new_state.model_dump() if hasattr(new_state, "model_dump") else new_state.dict())
    def run_game(self, visualize: bool = True) -> Dict[str, Any]:
        """
        Run a complete Nim game with optional visualization.

        Args:
            visualize (bool): Whether to visualize each game state.

        Returns:
            Dict[str, Any]: The final game state.
        """
        # Initialize the game state
        initial_state = self.state_manager.initialize(
            pile_sizes=self.config.pile_sizes,
            misere_mode=self.config.misere_mode
        )

        # Run the game with visualization
        if visualize:
            for step in self.stream(initial_state, stream_mode="values"):
                self.visualize_state(step)
            return step  # final state
        else:
            return super().run(initial_state)

    def visualize_state(self, state: Dict[str, Any]) -> None:
        """Visualize the current game state.

        Args:
            state (Dict[str, Any]): The current game state.
        """
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
            print(f"Position Evaluation: {last_analysis.position_evaluation}")
            print(f"Explanation: {last_analysis.explanation}")
            
        if hasattr(game_state, "player2_analysis") and game_state.player2_analysis and game_state.turn == "player1":
            last_analysis = game_state.player2_analysis[-1]
            print(f"\n🔍 Player 2's Analysis:")
            print(f"Position Evaluation: {last_analysis.position_evaluation}")
            print(f"Explanation: {last_analysis.explanation}")
        
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
        builder.add_node("player1_move", self.make_player1_move)
        builder.add_node("player2_move", self.make_player2_move)
        builder.add_node("analyze_player1", self.analyze_player1)
        builder.add_node("analyze_player2", self.analyze_player2)
        
        # Set up the game flow
        builder.add_edge("initialize", "player1_move")  # Start with player1
        builder.add_edge("player1_move", "analyze_player1")
        builder.add_edge("analyze_player1", "player2_move")
        builder.add_edge("player2_move", "analyze_player2")
        builder.add_edge("analyze_player2", "player1_move")  # Complete the cycle
        
        # Build the graph
        self.graph = builder.build()

#a=NimAgent()
#a.run_game(visualize=True)