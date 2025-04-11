"""
Mancala game agent.

This module defines the Mancala game agent, which uses language models
to generate moves and analyze positions in the game.
"""
from src.haive.games.mancala.config import MancalaConfig
from src.haive.games.mancala.models import MancalaMove, MancalaAnalysis
from src.haive.games.mancala.state_manager import MancalaStateManager
from src.haive.games.framework.base.agent import GameAgent
from src.haive.core.graph.GraphBuilder import DynamicGraph
from typing import Dict, Any, List, Optional
import time 
from langgraph.types import Command
from src.haive.core.engine.agent.agent import register_agent
from src.haive.games.mancala.state import MancalaState

@register_agent(MancalaConfig)
class MancalaAgent(GameAgent[MancalaConfig]):
    """Agent for playing Mancala.

    This class implements the Mancala game agent, which uses language models
    to generate moves and analyze positions in the game.
    """
    
    def __init__(self, config: MancalaConfig = MancalaConfig()):
        """Initialize the Mancala agent.

        Args:
            config (MancalaConfig): The configuration for the Mancala game.
        """
        super().__init__(config)
        self.state_manager = MancalaStateManager
        self.engines = config.aug_llm_configs
    
    def initialize_game(self, state: Dict[str, Any]) -> Command:
        """Initialize a new Mancala game with configured stones per pit.

        Args:
            state (Dict[str, Any]): Initial state dictionary (unused here but required for interface).

        Returns:
            Command: Initialization command containing the new game state.
        """
        game_state = self.state_manager.initialize(stones_per_pit=self.config.stones_per_pit)
        return Command(update=game_state.model_dump() if hasattr(game_state, "model_dump") else game_state.dict())
    
    def prepare_move_context(self, state: MancalaState, player: str) -> Dict[str, Any]:
        """Prepare context for move generation.

        Args:
            state (MancalaState): Current game state.
            player (str): The player making the move ('player1' or 'player2').

        Returns:
            Dict[str, Any]: Context dictionary for move generation.
        """
        # Get legal moves
        legal_moves = self.state_manager.get_legal_moves(state)
        
        # Format legal moves for display
        formatted_legal_moves = "\n".join([
            f"Pit {move.pit_index}: {state.board[move.pit_index if player == 'player1' else move.pit_index + 7]} stones" 
            for move in legal_moves
        ])
        
        # Get recent move history
        recent_moves = []
        for move in state.move_history[-5:]:
            recent_moves.append(str(move))
        
        # Get player's analysis if available
        player_analysis = None
        if hasattr(state, f"{player}_analysis") and getattr(state, f"{player}_analysis"):
            player_analysis = getattr(state, f"{player}_analysis")[-1]
        else:
            player_analysis = "No previous analysis available."
        
        # Prepare the context
        return {
            "board_string": state.board_string,
            "turn": state.turn,
            "legal_moves": formatted_legal_moves,
            "move_history": "\n".join(recent_moves),
            "player_analysis": player_analysis
        }
    
    def prepare_analysis_context(self, state: MancalaState, player: str) -> Dict[str, Any]:
        """Prepare context for position analysis.

        Args:
            state (MancalaState): Current game state.
            player (str): The player making the analysis ('player1' or 'player2').

        Returns:
            Dict[str, Any]: Context dictionary for position analysis.
        """
        # Get recent move history
        recent_moves = []
        for move in state.move_history[-5:]:
            recent_moves.append(str(move))
        
        # Get pit stones for each player
        player1_pits = state.board[0:6]
        player2_pits = state.board[7:13]
        
        # Prepare the context
        return {
            "board_string": state.board_string,
            "player": player,
            "player1_score": state.player1_score,
            "player2_score": state.player2_score,
            "player1_pits": player1_pits,
            "player2_pits": player2_pits,
            "move_history": "\n".join(recent_moves)
        }
    
    def extract_move(self, response: Any) -> MancalaMove:
        """Extract move from engine response.

        Args:
            response (Any): Response from the engine.

        Returns:
            MancalaMove: Parsed move object.
        """
        # The response should already be a MancalaMove object
        return response
    
    def make_player1_move(self, state: MancalaState) -> Command:
        """Make a move for player1.

        Args:
            state (MancalaState): Current game state.

        Returns:
            Command: Updated game state after the move.
        """
        return self.make_move(state, "player1")
    
    def make_player2_move(self, state: MancalaState) -> Command:
        """Make a move for player2.

        Args:
            state (MancalaState): Current game state.

        Returns:
            Command: Updated game state after the move.
        """
        return self.make_move(state, "player2")
    
    def make_move(self, state: MancalaState, player: str) -> Command:
        """Make a move for the specified player.

        Args:
            state (MancalaState): Current game state.
            player (str): The player making the move ('player1' or 'player2').

        Returns:
            Command: Updated game state after the move.
        """
        if state.turn != player:
            return Command(update=state.model_dump() if hasattr(state, "model_dump") else state.dict())
        
        # Check if game is over
        if state.game_status != "ongoing":
            return Command(update=state.model_dump() if hasattr(state, "model_dump") else state.dict())
        
        # Prepare context for the move
        context = self.prepare_move_context(state, player)
        
        # Select the appropriate engine
        engine_key = f"{player}_player"
        engine = self.engines[engine_key].create_runnable()
        
        # Generate move
        move = engine.invoke(context)
        
        # Apply the move
        new_state = self.state_manager.apply_move(state, move)
        
        # Return the updated state
        return Command(update=new_state.model_dump() if hasattr(new_state, "model_dump") else new_state.dict())
    
    def analyze_player1(self, state: MancalaState) -> Command:
        """Analyze position for player1.

        Args:
            state (MancalaState): Current game state.

        Returns:
            Command: Updated game state after the analysis.
        """
        return self.analyze_position(state, "player1")
    
    def analyze_player2(self, state: MancalaState) -> Command:
        """Analyze position for player2.

        Args:
            state (MancalaState): Current game state.

        Returns:
            Command: Updated game state after the analysis.
        """
        return self.analyze_position(state, "player2")
    
    def analyze_position(self, state: MancalaState, player: str) -> Command:
        """Analyze the current position for the specified player.

        Args:
            state (MancalaState): Current game state.
            player (str): The player making the analysis ('player1' or 'player2').

        Returns:
            Command: Updated game state after the analysis.
        """
        if not self.config.enable_analysis:
            return Command(update=state.model_dump() if hasattr(state, "model_dump") else state.dict())
        
        # Skip analysis if game is over
        if state.game_status != "ongoing":
            return Command(update=state.model_dump() if hasattr(state, "model_dump") else state.dict())
        
        # Prepare context for analysis
        context = self.prepare_analysis_context(state, player)
        
        # Select the appropriate engine
        engine_key = f"{player}_analyzer"
        engine = self.engines[engine_key].create_runnable()
        
        # Generate analysis
        analysis = engine.invoke(context)
        
        # Update state with analysis
        new_state = self.state_manager.add_analysis(state, player, analysis)
        
        # Return the updated state
        return Command(update=new_state.model_dump() if hasattr(new_state, "model_dump") else new_state.dict())
    
    def visualize_state(self, state: Dict[str, Any]) -> None:
        """Visualize the current game state.

        Args:
            state (Dict[str, Any]): Current game state.
        """
        # Create a MancalaState from the dict
        game_state = MancalaState(**state)
        
        print("\n" + "=" * 50)
        print(f"🎮 Current Player: {game_state.turn}")
        print(f"📌 Game Status: {game_state.game_status}")
        if game_state.free_turn:
            print("🎲 Free Turn: Yes")
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
            print(f"Position Evaluation: {last_analysis.position_evaluation} (Advantage: {last_analysis.advantage_level}/10)")
            print(f"Strategy Focus: {last_analysis.strategy_focus}")
            print(f"Key Tactics: {', '.join(last_analysis.key_tactics)}")
            print(f"Recommended Pits: {', '.join(str(p) for p in last_analysis.pit_recommendations)}")
            
        if hasattr(game_state, "player2_analysis") and game_state.player2_analysis and game_state.turn == "player1":
            last_analysis = game_state.player2_analysis[-1]
            print(f"\n🔍 Player 2's Analysis:")
            print(f"Position Evaluation: {last_analysis.position_evaluation} (Advantage: {last_analysis.advantage_level}/10)")
            print(f"Strategy Focus: {last_analysis.strategy_focus}")
            print(f"Key Tactics: {', '.join(last_analysis.key_tactics)}")
            print(f"Recommended Pits: {', '.join(str(p) for p in last_analysis.pit_recommendations)}")
        
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
        
        # Compile the workflow
    def run_game(self, visualize: bool = True) -> MancalaState:
        """Run a full Mancala game loop with optional visualization.

        Args:
            visualize (bool): Whether to visualize the game state.

        Returns:
            MancalaState: Final game state after completion.
        """
        # Initialize game state
        initial_state = MancalaStateManager.initialize(
            stones_per_pit=self.config.stones_per_pit
        )

        # Run the game
        if visualize:
            for step in self.stream(initial_state, stream_mode="values"):
                self.visualize_state(step)
            return step  # Final state
        else:
            return super().run(initial_state)
agent = MancalaAgent()
agent.run_game(visualize=True)