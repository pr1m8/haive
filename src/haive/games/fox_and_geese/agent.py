"""
Fox and Geese game agent.

This module defines the Fox and Geese game agent, which uses language models
to generate moves and analyze positions in the game.
"""
from src.haive.games.framework.base.agent import GameAgent
from src.haive.games.fox_and_geese.config import FoxAndGeeseConfig
from src.haive.games.fox_and_geese.models import FoxAndGeeseMove,FoxAndGeesePosition
from src.haive.games.fox_and_geese.state import FoxAndGeeseState
from src.haive.games.fox_and_geese.state_manager import FoxAndGeeseStateManager
from src.haive.core.graph.GraphBuilder import DynamicGraph
from typing import Dict, Any, List, Optional
from langgraph.graph import Command
import time
from src.haive.core.engine.agent.agent import register_agent

@register_agent(FoxAndGeeseConfig)
class FoxAndGeeseAgent(GameAgent[FoxAndGeeseConfig]):
    """Agent for playing Fox and Geese.

    This class implements the Fox and Geese game agent, which uses language models
    to generate moves and analyze positions in the game.
    """
    
    def __init__(self, config: FoxAndGeeseConfig = FoxAndGeeseConfig()):
        """Initialize the Fox and Geese agent.

        Args:
            config (FoxAndGeeseConfig): The configuration for the Fox and Geese game.
        """
        super().__init__(config)
        self.state_manager = FoxAndGeeseStateManager
        self.engines = config.aug_llm_configs
    
    def initialize_game(self, state: Dict[str, Any]) -> Command:
        """Initialize a new Fox and Geese game.

        Args:
            state (Dict[str, Any]): Initial state dictionary (unused here but required for interface).

        Returns:
            Command: Initialization command containing the new game state.
        """
        game_state = self.state_manager.initialize()
        return Command(update=game_state.model_dump() if hasattr(game_state, "model_dump") else game_state.dict())
    
    def prepare_move_context(self, state: FoxAndGeeseState, player: str) -> Dict[str, Any]:
        """Prepare context for move generation.

        Args:
            state (FoxAndGeeseState): Current game state.
            player (str): The player making the move ('fox' or 'geese').

        Returns:
            Dict[str, Any]: Context dictionary for move generation.
        """
        # Format legal moves for display
        formatted_legal_moves = "\n".join([str(move) for move in self.state_manager.get_legal_moves(state)])
        
        # Get recent move history
        recent_moves = []
        for move in state.move_history[-5:]:
            recent_moves.append(str(move))
        
        # Prepare the context
        return {
            "board_string": state.board_string,
            "legal_moves": formatted_legal_moves,
            "move_history": "\n".join(recent_moves),
            "num_geese": state.num_geese
        }
    
    def extract_move(self, response: Any) -> FoxAndGeeseMove:
        """Extract move from engine response.

        Args:
            response (Any): Response from the engine.

        Returns:
            FoxAndGeeseMove: Parsed move object.
        """
        # The response should already be a FoxAndGeeseMove object
        return response
    
    def make_fox_move(self, state: FoxAndGeeseState) -> Command:
        """Make a move for the fox.

        Args:
            state (FoxAndGeeseState): Current game state.

        Returns:
            Command: Updated game state after the move.
        """
        # Ensure it's the fox's turn
        if state.turn != "fox":
            return Command(update=state.model_dump() if hasattr(state, "model_dump") else state.dict())
        
        # Prepare context for the fox player
        context = self.prepare_move_context(state, "fox")
        
        # Call the fox player engine
        fox_player = self.engines["fox_player"].create_runnable()
        response = fox_player.invoke(context)
        
        # Extract the move
        move = self.extract_move(response)
        
        # Apply the move
        new_state = self.state_manager.apply_move(state, move)
        
        # Return the updated state
        return Command(update=new_state.model_dump() if hasattr(new_state, "model_dump") else new_state.dict())
    
    def make_geese_move(self, state: FoxAndGeeseState) -> Command:
        """Make a move for the geese.

        Args:
            state (FoxAndGeeseState): Current game state.

        Returns:
            Command: Updated game state after the move.
        """
        # Ensure it's the geese's turn
        if state.turn != "geese":
            return Command(update=state.model_dump() if hasattr(state, "model_dump") else state.dict())
        
        # Prepare context for the geese player
        context = self.prepare_move_context(state, "geese")
        
        # Call the geese player engine
        geese_player = self.engines["geese_player"].create_runnable()
        response = geese_player.invoke(context)
        
        # Extract the move
        move = self.extract_move(response)
        
        # Apply the move
        new_state = self.state_manager.apply_move(state, move)
        
        # Return the updated state
        return Command(update=new_state.model_dump() if hasattr(new_state, "model_dump") else new_state.dict())
    
    def analyze_fox_position(self, state: FoxAndGeeseState) -> Command:
        """Analyze the current position from the Fox's perspective.

        Args:
            state (FoxAndGeeseState): Current game state.

        Returns:
            Command: Updated game state after the analysis.
        """
        context = {
            "board_string": state.board_string,
            "turn": state.turn,
            "num_geese": state.num_geese,
            "move_history": "\n".join([str(move) for move in state.move_history[-5:]])
        }
        
        fox_analyzer = self.engines["fox_analysis"].create_runnable()
        analysis = fox_analyzer.invoke(context)
        
        new_state = state.model_copy() if hasattr(state, "model_copy") else state.copy()
        if not hasattr(new_state, "fox_analysis"):
            new_state.fox_analysis = []
        new_state.fox_analysis.append(analysis)
        
        return Command(update=new_state.model_dump() if hasattr(new_state, "model_dump") else new_state.dict())
    
    def analyze_geese_position(self, state: FoxAndGeeseState) -> Command:
        """Analyze the current position from the Geese's perspective.

        Args:
            state (FoxAndGeeseState): Current game state.

        Returns:
            Command: Updated game state after the analysis.
        """
        context = {
            "board_string": state.board_string,
            "turn": state.turn,
            "num_geese": state.num_geese,
            "move_history": "\n".join([str(move) for move in state.move_history[-5:]])
        }
        
        geese_analyzer = self.engines["geese_analysis"].create_runnable()
        analysis = geese_analyzer.invoke(context)
        
        new_state = state.model_copy() if hasattr(state, "model_copy") else state.copy()
        if not hasattr(new_state, "geese_analysis"):
            new_state.geese_analysis = []
        new_state.geese_analysis.append(analysis)
        
        return Command(update=new_state.model_dump() if hasattr(new_state, "model_dump") else new_state.dict())
    
    def visualize_state(self, state: Dict[str, Any]) -> None:
        """Visualize the current game state.

        Args:
            state (Dict[str, Any]): Current game state.
        """
        if not self.config.visualize:
            return
            
        # Create a FoxAndGeeseState from the dict
        game_state = FoxAndGeeseState(**state)
        
        print("\n" + "=" * 50)
        print(f"🎮 Current Player: {game_state.turn}")
        print(f"📌 Game Status: {game_state.game_status}")
        print(f"🦊 Fox position: {game_state.fox_position}")
        print(f"🐺 Geese remaining: {game_state.num_geese}")
        print("=" * 50)
        
        # Print the board
        print("\n" + game_state.board_string)
        
        # Print last move if available
        if game_state.move_history:
            last_move = game_state.move_history[-1]
            print(f"\n📝 Last Move: {str(last_move)}")
        
        # Print analysis if available
        if hasattr(game_state, "analysis") and game_state.analysis:
            print(f"\n🔍 Latest Analysis:")
            print(game_state.analysis[-1])
        
        # Add a short delay for readability
        time.sleep(0.5)
    
    def setup_workflow(self) -> None:
        """Set up the game workflow.

        Creates a dynamic graph with nodes for game initialization, move making,
        and analysis. Adds edges between nodes based on the current player's turn.
        """
        # Create a graph builder
        builder = DynamicGraph(state_schema=self.state_schema)
        
        # Add nodes for the main game flow
        builder.add_node("initialize", self.initialize_game)
        builder.add_node("fox_move", self.make_fox_move)
        builder.add_node("geese_move", self.make_geese_move)
        builder.add_node("analyze", self.analyze_position)
        
        # Set up the game flow
        builder.add_edge("initialize", "fox_move")  # Start with fox (as per rules)
        builder.add_edge("fox_move", "analyze")
        builder.add_edge("analyze", "geese_move")
        builder.add_edge("geese_move", "analyze")
        builder.add_edge("analyze", "fox_move")  # Complete the cycle
        
        # Build the graph
        self.graph = builder.build()
        
        # Compile the workflow
    def run_game(self, visualize: bool = True) -> Dict[str, Any]:
        """Run the full Fox and Geese game, optionally visualizing each step.

        Args:
            visualize (bool): Whether to visualize the game state.

        Returns:
            Dict[str, Any]: Final game state after completion.
        """
        # Initialize game state
        initial_state = self.state_manager.initialize()
        
        # Run the game
        game_state = self.stream(initial_state, stream_mode="values")
        
        # Visualize the game if requested
        if visualize:
            for state in game_state:
                self.visualize_state(state)
            return state  # Final state
        else:
            return super().run(initial_state)

agent = FoxAndGeeseAgent()
agent.run_game(visualize=True)  