"""Base game agent module.

This module provides the foundational GameAgent class that implements common workflow patterns
for game-specific agents. It handles game initialization, move generation, position analysis,
and game flow control.

Example:
    >>> class ChessAgent(GameAgent[ChessConfig]):
    ...     def __init__(self, config: ChessConfig):
    ...         super().__init__(config)
    ...         self.state_manager = ChessStateManager

Typical usage:
    - Inherit from GameAgent to create game-specific agents
    - Override necessary methods like prepare_move_context and extract_move
    - Use the setup_workflow method to customize the game flow
"""

from typing import Generic, Type, TypeVar, Any, Dict
from src.haive.games.framework.base.config import GameConfig
#from src.haive.games.framework.base.state import GameState
from src.haive.core.engine.agent.agent import Agent
from langgraph.types import Command 
from langgraph.graph import START, END
from pydantic import BaseModel
T = TypeVar('T', bound=BaseModel)

class GameAgent(Agent[GameConfig], Generic[T]):
    """Base game agent that implements common workflow patterns.
    
    This class provides a foundation for building game-specific agents by implementing
    common patterns for game initialization, move generation, position analysis, and
    game flow control. Game-specific agents should inherit from this class and
    override the necessary methods.

    Attributes:
        config (GameConfig): Configuration for the game agent.
        state_manager: Manager for handling game state transitions.
        engines (Dict[str, Any]): Dictionary of LLM engines for different functions.
        graph: The workflow graph for the game.

    Example:
        >>> class ChessAgent(GameAgent[ChessConfig]):
        ...     def __init__(self, config: ChessConfig):
        ...         super().__init__(config)
        ...         self.state_manager = ChessStateManager
        ...
        ...     def prepare_move_context(self, state, player):
        ...         legal_moves = self.state_manager.get_legal_moves(state)
        ...         return {"legal_moves": legal_moves}
    """
    
    def __init__(self, config: GameConfig=GameConfig()):
        """Initialize the game agent.

        Args:
            config (GameConfig, optional): Configuration for the game agent.
                Defaults to GameConfig().
        """
        super().__init__(config)
       
    
    def setup_workflow(self):
        """Setup the standard game workflow with configurable analysis.
        
        This method sets up the default game workflow including initialization,
        player moves, and optional position analysis. Override this method to
        implement custom game flows.

        The default workflow includes:
        1. Game initialization
        2. Alternating player moves
        3. Optional position analysis before each move
        4. Game continuation checks between moves

        Example:
            >>> def setup_workflow(self):
            ...     # Add custom nodes
            ...     self.graph.add_node("custom_analysis", self.analyze_position)
            ...     # Modify the workflow
            ...     self.graph.add_edge("initialize_game", "custom_analysis")
        """
        # Core nodes that all games need
        self.graph.add_node("initialize_game", self.initialize_game)
        self.graph.add_node("player1_move", self.make_player1_move)
        self.graph.add_node("player2_move", self.make_player2_move)
        
        # Start the game
        self.graph.add_edge(START, "initialize_game")
        
        # Analysis nodes (optional)
        if self.config.enable_analysis:
            self.graph.add_node("player1_analysis", self.analyze_player1)
            self.graph.add_node("player2_analysis", self.analyze_player2)
            
            # Flow with analysis
            self.graph.add_edge("initialize_game", "player1_analysis")
            self.graph.add_edge("player1_analysis", "player1_move")
            
            self.graph.add_conditional_edges(
                "player1_move",
                self.should_continue_game,
                {True: "player2_analysis", False: END}
            )
            
            self.graph.add_edge("player2_analysis", "player2_move")
            
            self.graph.add_conditional_edges(
                "player2_move",
                self.should_continue_game,
                {True: "player1_analysis", False: END}
            )
        else:
            # Simplified flow without analysis
            self.graph.add_edge("initialize_game", "player1_move")
            
            self.graph.add_conditional_edges(
                "player1_move",
                self.should_continue_game,
                {True: "player2_move", False: END}
            )
            
            self.graph.add_conditional_edges(
                "player2_move",
                self.should_continue_game,
                {True: "player1_move", False: END}
            )
    
    def initialize_game(self, state: Dict[str, Any]) -> Command:
        """Initialize a new game.

        Args:
            state (Dict[str, Any]): The initial state dictionary.

        Returns:
            Command: A command containing the initialized game state.

        Example:
            >>> def initialize_game(self, state):
            ...     game_state = self.state_manager.initialize()
            ...     return Command(update=game_state.dict())
        """
        game_state = self.state_manager.initialize()
        return Command(update=game_state.model_dump() if hasattr(game_state, "model_dump") else game_state.dict())
    
    def make_move(self, state: T, player: str) -> Command:
        """Make a move for the specified player.

        This method handles the complete move generation process including:
        1. Getting the appropriate engine for the player
        2. Preparing the move context
        3. Generating and validating the move
        4. Applying the move to the game state

        Args:
            state (T): The current game state.
            player (str): The player making the move.

        Returns:
            Command: A command containing the updated game state after the move.

        Example:
            >>> def make_move(self, state, player):
            ...     engine = self.engines.get(f"{player}_player")
            ...     move_context = self.prepare_move_context(state, player)
            ...     response = engine.invoke(move_context)
            ...     move = self.extract_move(response)
            ...     new_state = self.state_manager.apply_move(state, move)
            ...     return Command(update=new_state.dict())
        """
        engine = self.engines.get(f"{player}_player")
        if not engine:
            return Command(update={"error_message": f"No engine found for {player}_player"})
        
        try:
            # Get decision from the engine
            move_context = self.prepare_move_context(state, player)
            response = engine.invoke(move_context)
            
            # Apply move to state
            move = self.extract_move(response)
            new_state = self.state_manager.apply_move(state, move)
            
            # Convert to dict for Command
            state_dict = new_state.model_dump() if hasattr(new_state, "model_dump") else new_state.dict()
            return Command(update=state_dict)
        except Exception as e:
            return Command(update={"error_message": f"Error in {player}'s move: {str(e)}"})
    
    def analyze_position(self, state: T, player: str) -> Command:
        """Analyze the position for the specified player.

        This method handles position analysis including:
        1. Getting the appropriate analyzer engine
        2. Preparing the analysis context
        3. Generating and storing the analysis

        Args:
            state (T): The current game state.
            player (str): The player for whom to analyze the position.

        Returns:
            Command: A command containing the updated game state with analysis.

        Example:
            >>> def analyze_position(self, state, player):
            ...     analyzer = self.engines.get(f"{player}_analyzer")
            ...     analysis = analyzer.invoke({"position": state.board})
            ...     return Command(update={f"{player}_analysis": analysis})
        """
        analyzer = self.engines.get(f"{player}_analyzer")
        if not analyzer:
            return Command(update={})
        
        try:
            # Get analysis from the engine
            analysis_context = self.prepare_analysis_context(state, player)
            analysis = analyzer.invoke(analysis_context)
            
            # Add analysis to state
            analysis_dict = analysis.model_dump() if hasattr(analysis, "model_dump") else analysis.dict()
            analysis_key = f"{player}_analysis"
            
            current_analyses = getattr(state, analysis_key, [])
            return Command(update={
                analysis_key: current_analyses[-4:] + [analysis_dict]
            })
        except Exception as e:
            return Command(update={"error_message": f"Error in {player}'s analysis: {str(e)}"})
    
    def should_continue_game(self, state: T) -> bool:
        """Determine if the game should continue.

        Args:
            state (T): The current game state.

        Returns:
            bool: True if the game should continue, False otherwise.

        Example:
            >>> def should_continue_game(self, state):
            ...     return state.moves_remaining > 0 and not state.checkmate
        """
        return state.game_status == "ongoing"
    
    # Methods to be implemented by subclasses
    def prepare_move_context(self, state: T, player: str) -> Dict[str, Any]:
        """Prepare context for move generation.

        This method should be implemented by subclasses to provide the necessary
        context for the LLM to generate a move.

        Args:
            state (T): The current game state.
            player (str): The player for whom to prepare the context.

        Returns:
            Dict[str, Any]: The context dictionary for move generation.

        Raises:
            NotImplementedError: This method must be implemented by subclasses.

        Example:
            >>> def prepare_move_context(self, state, player):
            ...     legal_moves = self.state_manager.get_legal_moves(state)
            ...     return {
            ...         "board": state.board.to_fen(),
            ...         "legal_moves": legal_moves,
            ...         "player": player
            ...     }
        """
        raise NotImplementedError("Must be implemented by subclass")
    
    def prepare_analysis_context(self, state: T, player: str) -> Dict[str, Any]:
        """Prepare context for position analysis.

        This method should be implemented by subclasses to provide the necessary
        context for the LLM to analyze a position.

        Args:
            state (T): The current game state.
            player (str): The player for whom to prepare the analysis context.

        Returns:
            Dict[str, Any]: The context dictionary for position analysis.

        Raises:
            NotImplementedError: This method must be implemented by subclasses.

        Example:
            >>> def prepare_analysis_context(self, state, player):
            ...     return {
            ...         "board": state.board.to_fen(),
            ...         "material_count": state.get_material_count(player),
            ...         "previous_moves": state.move_history[-5:]
            ...     }
        """
        raise NotImplementedError("Must be implemented by subclass")
    
    def extract_move(self, response: Any) -> Any:
        """Extract move from engine response.

        This method should be implemented by subclasses to parse the LLM's
        response and extract a valid move.

        Args:
            response (Any): The raw response from the LLM engine.

        Returns:
            Any: A valid move object for the game.

        Raises:
            NotImplementedError: This method must be implemented by subclasses.

        Example:
            >>> def extract_move(self, response):
            ...     move_text = response.get("move")
            ...     return ChessMove.from_uci(move_text)
        """
        raise NotImplementedError("Must be implemented by subclass")
    
    def make_player1_move(self, state: T) -> Command:
        """Make a move for player 1.

        This method should be implemented by subclasses to handle moves
        specifically for player 1.

        Args:
            state (T): The current game state.

        Returns:
            Command: A command containing the updated game state after the move.

        Raises:
            NotImplementedError: This method must be implemented by subclasses.

        Example:
            >>> def make_player1_move(self, state):
            ...     return self.make_move(state, "player1")
        """
        raise NotImplementedError("Must be implemented by subclass")
    
    def make_player2_move(self, state: T) -> Command:
        """Make a move for player 2.

        This method should be implemented by subclasses to handle moves
        specifically for player 2.

        Args:
            state (T): The current game state.

        Returns:
            Command: A command containing the updated game state after the move.

        Raises:
            NotImplementedError: This method must be implemented by subclasses.

        Example:
            >>> def make_player2_move(self, state):
            ...     return self.make_move(state, "player2")
        """
        raise NotImplementedError("Must be implemented by subclass")
    
    def analyze_player1(self, state: T) -> Command:
        """Analyze position for player 1.

        This method should be implemented by subclasses to handle position
        analysis specifically for player 1.

        Args:
            state (T): The current game state.

        Returns:
            Command: A command containing the updated game state with analysis.

        Raises:
            NotImplementedError: This method must be implemented by subclasses.

        Example:
            >>> def analyze_player1(self, state):
            ...     return self.analyze_position(state, "player1")
        """
        raise NotImplementedError("Must be implemented by subclass")
    
    def analyze_player2(self, state: T) -> Command:
        """Analyze position for player 2.

        This method should be implemented by subclasses to handle position
        analysis specifically for player 2.

        Args:
            state (T): The current game state.

        Returns:
            Command: A command containing the updated game state with analysis.

        Raises:
            NotImplementedError: This method must be implemented by subclasses.

        Example:
            >>> def analyze_player2(self, state):
            ...     return self.analyze_position(state, "player2")
        """
        raise NotImplementedError("Must be implemented by subclass")

"""Utility functions for game agents.

This module provides utility functions for running and managing game agents,
including game execution and state visualization.

Example:
    >>> agent = ChessAgent(config)
    >>> run_game(agent)  # Run a new game
    >>> run_game(agent, initial_state=saved_state)  # Continue from a saved state

Typical usage:
    - Use run_game to execute a complete game with an agent
    - Provide optional initial state to continue from a specific point
    - Monitor game progress through visualization and status updates
"""

from typing import Dict, Any, Optional
#from .agent import GameAgent

def run_game(agent: 'GameAgent', initial_state: Optional[Dict[str, Any]] = None):
    """Run a complete game with the given agent.
    
    This function executes a game from start to finish using the provided agent.
    It handles game initialization, move execution, state visualization, and
    error reporting. The game can optionally start from a provided initial state.
    
    Args:
        agent (GameAgent): The game agent to run the game with.
        initial_state (Optional[Dict[str, Any]], optional): Initial game state.
            If not provided, a new game will be initialized. Defaults to None.
    
    Example:
        >>> agent = ChessAgent(ChessConfig())
        >>> # Start a new game
        >>> run_game(agent)
        >>> 
        >>> # Continue from a saved state
        >>> run_game(agent, saved_state)
    
    Note:
        - The function will print game progress to the console
        - Game visualization depends on the agent's visualize_state method
        - Game history will be saved using the agent's save_state_history method
    """
    # Use provided initial state or create a default one
    game_state = initial_state or {}
    
    # Run the game
    print("\n🎮 Starting Game")
    print("=" * 50)
    
    # Stream through the game steps
    for step in agent.app.stream(
        game_state, 
        config=agent.runnable_config,
        debug=True,
        stream_mode="values"
    ):
        # Visualize the game state
        agent.visualize_state(step)
        
        # Check for errors
        if step.get("error_message"):
            print(f"\n❌ Error: {step['error_message']}")
        
        # Show game status
        if step.get("game_status") != "ongoing":
            print(f"\n🏆 Game Status: {step['game_status'].upper()}")
            if step.get("winner"):
                print(f"🎖️ Winner: {step['winner']}")
    
    # Save game history
    agent.save_state_history()
    print("\n✅ Game Complete!")