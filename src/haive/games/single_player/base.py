"""Single-player game framework for LLM-powered games.

This module provides a core framework for building single-player games where
an LLM can act as the player, the assistant, or the game engine. The framework
is designed to be flexible, extensible, and independent of any multiplayer
game concepts.

Example:
    >>> from src.haive.agents.single_player import SinglePlayerGameAgent
    >>> class WordleAgent(SinglePlayerGameAgent):
    ...     def __init__(self, config):
    ...         super().__init__(config)
    ...         self.state_manager = WordleStateManager

Typical usage:
    - Inherit from SinglePlayerGameState for game-specific state
    - Inherit from SinglePlayerStateManager for game logic
    - Inherit from SinglePlayerGameConfig for configuration
    - Inherit from SinglePlayerGameAgent for the agent implementation
"""

from typing import Dict, List, Any, Optional, Union, TypeVar, Type, Generic, Tuple
from pydantic import BaseModel, Field, field_validator, create_model
from enum import Enum
import copy
import time
import random
import json
from datetime import datetime
import uuid
import os
import inspect

from langgraph.graph import StateGraph, START, END
from langgraph.types import Command
from langgraph.checkpoint.memory import MemorySaver

from src.haive.core.engine.aug_llm import AugLLMConfig
from src.haive.core.models.llm.base import AzureLLMConfig
from langchain_core.prompts import ChatPromptTemplate

# Type variables for generics
T = TypeVar('T', bound=BaseModel)

class PlayerType(str, Enum):
    """Type of player in a single-player game."""
    HUMAN = "human"  # Human player with interactive interface
    LLM = "llm"      # LLM as the player
    HYBRID = "hybrid"  # Human with LLM assistance

class GameMode(str, Enum):
    """Mode of operation for the game."""
    INTERACTIVE = "interactive"  # Interactive mode with user input
    AUTO = "auto"                # Fully automated mode with LLM
    ASSIST = "assist"            # LLM provides assistance but human makes decisions

class GameDifficulty(str, Enum):
    """Difficulty level for a game."""
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"
    EXPERT = "expert"

class GameSourceType(str, Enum):
    """Source of the game content."""
    INTERNAL = "internal"  # Generated within the system
    EXTERNAL = "external"  # Scraped or imported from external source
    CUSTOM = "custom"      # Custom user-provided content

class SinglePlayerGameState(BaseModel):
    """Base state for single-player games.
    
    This class defines the core state attributes that all single-player games
    need to track, including game status, move history, and analysis.
    
    Attributes:
        player_type (PlayerType): Type of player (human, LLM, hybrid)
        move_count (int): Number of moves made
        hint_count (int): Number of hints used
        difficulty (GameDifficulty): Difficulty level of the game
        game_status (str): Status of the game (ongoing, victory, defeat)
        move_history (List[Dict]): History of moves made
        analysis_history (List[Dict]): History of analyses made
        error_message (Optional[str]): Error message if any
    """
    player_type: PlayerType = Field(
        default=PlayerType.LLM,
        description="Type of player"
    )
    move_count: int = Field(
        default=0,
        description="Number of moves made"
    )
    hint_count: int = Field(
        default=0,
        description="Number of hints used"
    )
    difficulty: GameDifficulty = Field(
        default=GameDifficulty.MEDIUM,
        description="Difficulty level of the game"
    )
    game_status: str = Field(
        default="ongoing",
        description="Status of the game"
    )
    move_history: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="History of moves"
    )
    analysis_history: List[Dict[str, Any]] = Field(
        default_factory=list, 
        description="History of analyses"
    )
    error_message: Optional[str] = Field(
        default=None,
        description="Error message if any"
    )
    
    def is_game_over(self) -> bool:
        """Check if the game is over."""
        return self.game_status != "ongoing"
    
    def is_victory(self) -> bool:
        """Check if the game was won."""
        return self.game_status == "victory"
    
    def is_defeat(self) -> bool:
        """Check if the game was lost."""
        return self.game_status == "defeat"
    
    def increment_move_count(self) -> None:
        """Increment the move count."""
        self.move_count += 1
    
    def use_hint(self) -> None:
        """Use a hint."""
        self.hint_count += 1


class SinglePlayerStateManager(Generic[T]):
    """Base state manager for single-player games.
    
    This class provides the interface for managing game state transitions
    and operations. Each game should extend this with game-specific logic
    by implementing the required methods.
    
    Type Parameters:
        T: The type of the game state, must be a Pydantic BaseModel.
    
    Methods:
        initialize: Initialize a new game state
        apply_move: Apply a move to the game state
        generate_hint: Generate a hint for the current game state
        check_game_status: Check and update the game status
        interactive_input: Process interactive input from the player
    """
    
    @classmethod
    def initialize(cls, difficulty: GameDifficulty = GameDifficulty.MEDIUM, 
                  player_type: PlayerType = PlayerType.LLM, **kwargs) -> T:
        """Initialize a new game state.
        
        Args:
            difficulty: Difficulty level of the game
            player_type: Type of player
            **kwargs: Additional game-specific initialization parameters
            
        Returns:
            A new game state
        """
        raise NotImplementedError("Must be implemented by subclass")
    
    @classmethod
    def apply_move(cls, state: T, move: Any) -> T:
        """Apply a move to the game state.
        
        Args:
            state: Current game state
            move: Move to apply
            
        Returns:
            Updated game state
        """
        raise NotImplementedError("Must be implemented by subclass")
    
    @classmethod
    def generate_hint(cls, state: T) -> Tuple[T, str]:
        """Generate a hint for the current game state.
        
        Args:
            state: Current game state
            
        Returns:
            Tuple of (updated state, hint text)
        """
        # Create a copy of the state
        new_state = copy.deepcopy(state)
        
        # Increment hint count
        new_state.hint_count += 1
        
        # Default hint - should be overridden by subclasses
        hint = "This is a generic hint. Override this method in your game-specific state manager."
        
        return new_state, hint
    
    @classmethod
    def check_game_status(cls, state: T) -> T:
        """Check and update the game status.
        
        Args:
            state: Current game state
            
        Returns:
            Updated game state with status checked
        """
        raise NotImplementedError("Must be implemented by subclass")
    
    @classmethod
    def get_legal_moves(cls, state: T) -> List[Any]:
        """Get all legal moves for the current state.
        
        Args:
            state: Current game state
            
        Returns:
            List of legal moves
        """
        raise NotImplementedError("Must be implemented by subclass")
    
    @classmethod
    def interactive_input(cls, state: T, user_input: str) -> T:
        """Process interactive input from the player.
        
        This method handles general commands like 'hint', 'quit', etc.
        Game-specific commands should be handled by overriding this method.
        
        Args:
            state: Current game state
            user_input: User input string
            
        Returns:
            Updated game state
        """
        # Create a copy of the state
        new_state = copy.deepcopy(state)
        
        # Convert input to lowercase for easier matching
        input_lower = user_input.strip().lower()
        
        # Handle common commands
        if input_lower == "hint":
            new_state, hint_text = cls.generate_hint(new_state)
            new_state.error_message = f"HINT: {hint_text}"
        elif input_lower == "quit":
            new_state.game_status = "defeat"
            new_state.error_message = "Game quit by player"
        elif input_lower == "status":
            moves = new_state.move_count
            hints = new_state.hint_count
            new_state.error_message = f"Game Status: Moves: {moves}, Hints: {hints}"
        else:
            # Unknown command, let subclass handle it
            pass
            
        return new_state


class SinglePlayerGameConfig(BaseModel):
    """Configuration for single-player games.
    
    This class defines the core configuration parameters that all single-player
    games need, including player type, game mode, and difficulty.
    
    Attributes:
        state_schema: The state schema class for the game
        player_type: Type of player (human, LLM, hybrid)
        game_mode: Mode of operation (interactive, auto, assist)
        difficulty: Difficulty level of the game
        max_hints: Maximum number of hints allowed
        auto_analyze: Whether to automatically analyze after each move
        engines: Configurations for game LLMs
    """
    
    name: str = Field(
        default_factory=lambda: f"spgame_{uuid.uuid4().hex[:8]}", 
        description="Name of the game agent"
    )
    state_schema: Type[SinglePlayerGameState] = Field(
        ...,
        description="State schema for the game"
    )
    player_type: PlayerType = Field(
        default=PlayerType.LLM,
        description="Type of player"
    )
    game_mode: GameMode = Field(
        default=GameMode.AUTO,
        description="Mode of operation"
    )
    difficulty: GameDifficulty = Field(
        default=GameDifficulty.MEDIUM,
        description="Difficulty level of the game"
    )
    max_hints: int = Field(
        default=3,
        description="Maximum number of hints allowed"
    )
    auto_analyze: bool = Field(
        default=True,
        description="Whether to automatically analyze after each move"
    )
    game_source: GameSourceType = Field(
        default=GameSourceType.INTERNAL,
        description="Source of the game content"
    )
    engines: Dict[str, AugLLMConfig] = Field(
        default_factory=dict,
        description="Configurations for game LLMs"
    )
    save_history: bool = Field(
        default=True,
        description="Whether to save state history after execution"
    )
    visualize: bool = Field(
        default=True,
        description="Whether to generate graph visualizations"
    )
    output_dir: str = Field(
        default="outputs",
        description="Directory for output files"
    )
    runtime_config: Dict[str, Any] = Field(
        default_factory=lambda: {"configurable": {"thread_id": str(uuid.uuid4())}},
        description="Configuration for graph execution"
    )


class SinglePlayerGameAgent:
    """Base agent for single-player games.
    
    This class provides the core functionality for single-player game agents,
    including state initialization, move handling, analysis, and visualization.
    
    Attributes:
        config: Configuration for the game agent
        state_manager: Manager for game state transitions
        engines: Dictionary of LLM engines for move generation and analysis
        graph: State graph for game flow
        app: Compiled graph application
    """
    
    def __init__(self, config):
        """Initialize the game agent.
        
        Args:
            config: Configuration for the game agent
        """
        self.config = config
        self.state_manager = None  # Must be set by subclass
        self.memory = MemorySaver()
        self.engines = {}
        
        # Set up engines for move generation and analysis
        for key, engine_config in self.config.engines.items():
            self.engines[key] = engine_config.create_runnable()
            
        # Set up runtime configuration
        self.runnable_config = self.config.runtime_config
        
        # Ensure output directory exists
        os.makedirs(self.config.output_dir, exist_ok=True)
        
        # Set up output paths
        self._setup_output_paths()
        
        # Initialize graph
        self.graph = StateGraph(self.config.state_schema)
        
        # Set up workflow
        self.setup_workflow()
        
        # Compile the graph
        self.app = self.graph.compile(checkpointer=self.memory)
        
    def _setup_output_paths(self):
        """Set up paths for output files."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Set up state history directory and file
        self.state_history_dir = os.path.join(self.config.output_dir, "State_History")
        os.makedirs(self.state_history_dir, exist_ok=True)
        self.state_filename = os.path.join(
            self.state_history_dir, 
            f"{self.config.name}_{timestamp}.json"
        )
        
        # Set up graphs directory and file
        self.graphs_dir = os.path.join(self.config.output_dir, "Graphs")
        os.makedirs(self.graphs_dir, exist_ok=True)
        self.graph_image_path = os.path.join(
            self.graphs_dir, 
            f"{self.config.name}_{timestamp}.png"
        )
    
    def initialize_game(self, state: Dict[str, Any]) -> Command:
        """Initialize a new game.
        
        Args:
            state: Initial state (usually empty)
            
        Returns:
            Command with the initialized game state
        """
        # Initialize with configured difficulty and player type
        game_state = self.state_manager.initialize(
            difficulty=self.config.difficulty,
            player_type=self.config.player_type
        )
        
        # Convert to dict for Command
        state_dict = game_state.model_dump() if hasattr(game_state, "model_dump") else game_state.dict()
        return Command(update=state_dict)
    
    def make_player_move(self, state: T) -> Command:
        """Make a move for the player.
        
        In auto mode, this uses the LLM to generate a move.
        In interactive mode, this just returns the state unchanged.
        
        Args:
            state: Current game state
            
        Returns:
            Command with the updated game state
        """
        # For auto mode, use the LLM to make a move
        if self.config.game_mode == GameMode.AUTO:
            engine = self.engines.get("player_move")
            if not engine:
                return Command(update={"error_message": "No player move engine configured"})
            
            try:
                # Get decision from the engine
                move_context = self.prepare_move_context(state)
                response = engine.invoke(move_context)
                
                # Extract and apply move
                move = self.extract_move(response)
                new_state = self.state_manager.apply_move(state, move)
                
                # Save reasoning if available
                if hasattr(response, "reasoning"):
                    new_state.move_history[-1]["reasoning"] = response.reasoning
                
                # Convert to dict for Command
                state_dict = new_state.model_dump() if hasattr(new_state, "model_dump") else new_state.dict()
                return Command(update=state_dict)
            except Exception as e:
                return Command(update={"error_message": f"Error in player's move: {str(e)}"})
        
        # For other modes, just return the state unchanged
        # Interactive commands are handled separately
        return Command(update={})
    
    def analyze_position(self, state: T) -> Command:
        """Analyze the current game state.
        
        Args:
            state: Current game state
            
        Returns:
            Command with the updated game state including analysis
        """
        analyzer = self.engines.get("game_analyzer")
        if not analyzer:
            return Command(update={})
        
        try:
            # Get analysis from the engine
            analysis_context = self.prepare_analysis_context(state)
            analysis = analyzer.invoke(analysis_context)
            
            # Add analysis to state
            analysis_dict = analysis.model_dump() if hasattr(analysis, "model_dump") else analysis.dict()
            
            return Command(update={
                "analysis_history": state.analysis_history[-4:] + [analysis_dict]
            })
        except Exception as e:
            return Command(update={"error_message": f"Error in analysis: {str(e)}"})
    
    def get_hint(self, state: T) -> Command:
        """Get a hint for the current game state.
        
        Args:
            state: Current game state
            
        Returns:
            Command with the updated game state including a hint
        """
        # Check hint limit
        if state.hint_count >= self.config.max_hints:
            return Command(update={"error_message": "No more hints available"})
        
        # Generate hint
        new_state, hint_text = self.state_manager.generate_hint(state)
        
        # Try to use the analyzer for a more sophisticated hint
        analyzer = self.engines.get("game_analyzer")
        if analyzer:
            try:
                analysis_context = self.prepare_analysis_context(state)
                analysis_context["hint_request"] = True
                analysis = analyzer.invoke(analysis_context)
                
                if hasattr(analysis, "hint") and analysis.hint:
                    hint_text = analysis.hint
            except:
                # Fall back to basic hint
                pass
        
        # Convert to dict for Command
        state_dict = new_state.model_dump() if hasattr(new_state, "model_dump") else new_state.dict()
        state_dict["error_message"] = f"HINT: {hint_text}"
        
        return Command(update=state_dict)
    
    def interactive_command(self, state: T, command: str) -> Command:
        """Process an interactive command.
        
        Args:
            state: Current game state
            command: Command string
            
        Returns:
            Command with the updated game state
        """
        # Process the command
        new_state = self.state_manager.interactive_input(state, command)
        
        # Convert to dict for Command
        state_dict = new_state.model_dump() if hasattr(new_state, "model_dump") else new_state.dict()
        return Command(update=state_dict)
    
    def setup_workflow(self):
        """Setup the workflow for the game.
        
        The workflow depends on the game mode:
        - Auto: Initialize -> Analyze -> Move -> Check -> Repeat
        - Interactive: Initialize -> Listen for commands
        - Assist: Initialize -> Analyze -> Listen for commands
        """
        # Core nodes
        self.graph.add_node("initialize_game", self.initialize_game)
        self.graph.add_node("make_player_move", self.make_player_move)
        
        # Start with initialization
        self.graph.add_edge(START, "initialize_game")
        
        # Add analysis if enabled
        if self.config.auto_analyze:
            self.graph.add_node("analyze_position", self.analyze_position)
            self.graph.add_edge("initialize_game", "analyze_position")
            
            if self.config.game_mode == GameMode.AUTO:
                # Auto mode flow with analysis
                self.graph.add_edge("analyze_position", "make_player_move")
                
                self.graph.add_conditional_edges(
                    "make_player_move",
                    self.should_continue_game,
                    {True: "analyze_position", False: END}
                )
            else:
                # Interactive or assist mode flow with analysis
                self.graph.add_edge("analyze_position", END)
        else:
            # Flow without analysis
            if self.config.game_mode == GameMode.AUTO:
                # Auto mode without analysis
                self.graph.add_edge("initialize_game", "make_player_move")
                
                self.graph.add_conditional_edges(
                    "make_player_move",
                    self.should_continue_game,
                    {True: "make_player_move", False: END}
                )
            else:
                # Interactive or assist mode without analysis
                self.graph.add_edge("initialize_game", END)
    
    def should_continue_game(self, state: T) -> bool:
        """Check if the game should continue.
        
        Args:
            state: Current game state
            
        Returns:
            True if the game should continue, False otherwise
        """
        return state.game_status == "ongoing"
    
    def prepare_move_context(self, state: T) -> Dict[str, Any]:
        """Prepare context for move generation.
        
        Args:
            state: Current game state
            
        Returns:
            Context dictionary for the move engine
        """
        raise NotImplementedError("Must be implemented by subclass")
    
    def prepare_analysis_context(self, state: T) -> Dict[str, Any]:
        """Prepare context for analysis.
        
        Args:
            state: Current game state
            
        Returns:
            Context dictionary for the analysis engine
        """
        raise NotImplementedError("Must be implemented by subclass")
    
    def extract_move(self, response: Any) -> Any:
        """Extract move from engine response.
        
        Args:
            response: Response from the engine
            
        Returns:
            Extracted move
        """
        raise NotImplementedError("Must be implemented by subclass")
    
    def visualize_state(self, state: Dict[str, Any]) -> None:
        """Visualize the current game state.
        
        Args:
            state: Current game state
        """
        raise NotImplementedError("Must be implemented by subclass")
    
    def save_state_history(self) -> None:
        """Save the current agent state to a JSON file."""
        if not self.app or not self.memory:
            print("Cannot save state history: Workflow graph not compiled or memory not initialized")
            return

        state_json = self.app.get_state(self.runnable_config)
        if not state_json:
            print("No state history available")
            return

        # Ensure state is JSON serializable
        def _ensure_json_serializable(obj: Any) -> Any:
            """Ensure object is JSON serializable, converting non-serializable objects."""
            try:
                json.dumps(obj)
                return obj
            except (TypeError, OverflowError):
                if hasattr(obj, "model_dump"):
                    return obj.model_dump()
                elif isinstance(obj, dict):
                    return {k: _ensure_json_serializable(v) for k, v in obj.items()}
                elif isinstance(obj, list):
                    return [_ensure_json_serializable(v) for v in obj]
                elif isinstance(obj, tuple):
                    return [_ensure_json_serializable(v) for v in obj]
                elif hasattr(obj, "__dict__"):
                    return _ensure_json_serializable(obj.__dict__)
                elif hasattr(obj, "__str__"):
                    return str(obj)
                else:
                    return "Unserializable Object"
                    
        state_json = _ensure_json_serializable(state_json)

        # Save to file
        try:
            with open(self.state_filename, "w", encoding="utf-8") as f:
                json.dump(state_json, f, indent=4)
            print(f"State history saved to: {self.state_filename}")
        except Exception as e:
            print(f"Error saving state history: {str(e)}")
