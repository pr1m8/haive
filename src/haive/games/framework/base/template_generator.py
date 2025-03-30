# src/haive/agents/agent_games/framework/template_generator.py

"""Template generator for game agents (EXPERIMENTAL).

This experimental module provides a template generator for creating new game
implementations. It automates the creation of boilerplate code and ensures
consistency across different game implementations.

Warning:
    This module is experimental and its API may change without notice.
    Use with caution in production environments.

Example:
    >>> # Create templates for a new chess game
    >>> generator = GameTemplateGenerator(
    ...     game_name="Chess",
    ...     player1_name="white",
    ...     player2_name="black",
    ...     enable_analysis=True
    ... )
    >>> generator.generate_templates()

Typical usage:
    - Initialize the generator with game details
    - Generate all template files at once
    - Customize the generated code for your specific game
"""

import os
import re
from typing import List, Dict, Any, Optional
from textwrap import dedent
from ..base.config import GameConfig
from ..base.state import GameState
from ..base.agent import GameAgent

class GameTemplateGenerator:
    """Experimental template generator for new board game implementations.
    
    This class automates the creation of boilerplate code for implementing
    new board games within the framework. It generates a complete set of
    files with proper structure, documentation, and type hints.
    
    Warning:
        This class is experimental and its API may change without notice.
        Generated code may need manual adjustments for specific games.
    
    Attributes:
        game_name (str): The name of the game (used for class names).
        player1_name (str): Name for player 1.
        player2_name (str): Name for player 2.
        enable_analysis (bool): Whether to include analysis in templates.
        game_slug (str): Slugified version of the game name for file paths.
        game_class_name (str): CamelCase version of game name for class names.
        base_dir (str): Base directory for generated files.
    
    Example:
        >>> generator = GameTemplateGenerator("Tic Tac Toe")
        >>> generator.generate_templates()
        ✅ Generated template files for Tic Tac Toe in src/haive/agents/agent_games/tic_tac_toe
    """
    
    def __init__(self, 
                 game_name: str,
                 player1_name: str = "player1",
                 player2_name: str = "player2",
                 enable_analysis: bool = True):
        """Initialize the template generator.
        
        Args:
            game_name (str): The name of the game (used for class names).
            player1_name (str, optional): Name for player 1. Defaults to "player1".
            player2_name (str, optional): Name for player 2. Defaults to "player2".
            enable_analysis (bool, optional): Whether to include analysis in templates.
                Defaults to True.
        
        Example:
            >>> generator = GameTemplateGenerator(
            ...     game_name="Chess",
            ...     player1_name="white",
            ...     player2_name="black"
            ... )
        """
        self.game_name = game_name
        self.player1_name = player1_name
        self.player2_name = player2_name
        self.enable_analysis = enable_analysis
        
        # Convert game name to reasonable formats
        self.game_slug = self.game_name.lower().replace(" ", "_")
        self.game_class_name = ''.join(word.capitalize() for word in self.game_name.split())
        
        # Create directory paths
        self.base_dir = f"src/haive/agents/agent_games/{self.game_slug}"
    
    def generate_templates(self, output_dir: str = None) -> None:
        """Generate all template files for the game.
        
        This method creates a complete set of files needed for a new game
        implementation, including models, state management, configuration,
        and example usage.
        
        Args:
            output_dir (str, optional): Optional directory to write files to.
                If not provided, uses the standard package structure.
        
        Example:
            >>> generator = GameTemplateGenerator("Chess")
            >>> # Generate in default location
            >>> generator.generate_templates()
            >>> # Generate in custom location
            >>> generator.generate_templates("my_games/chess")
        """
        if output_dir:
            self.base_dir = output_dir
        
        # Create the directory if it doesn't exist
        os.makedirs(self.base_dir, exist_ok=True)
        
        # Generate each file
        self._generate_models_file()
        self._generate_state_manager_file()
        self._generate_config_file()
        self._generate_agent_file()
        self._generate_example_file()
        
        print(f"✅ Generated template files for {self.game_name} in {self.base_dir}")
    
    def _generate_models_file(self) -> None:
        """Generate the models.py file with game-specific data models.
        
        This method creates a file containing Pydantic models for:
        - Game moves
        - Player decisions
        - Game state
        - Analysis (if enabled)
        
        The generated models include proper type hints, field descriptions,
        and validation rules.
        """
        content = dedent(f'''
        from typing import List, Dict, Literal, Optional, Tuple, Union
        from pydantic import BaseModel, Field, field_validator
        from ...framework.base import GameState

        class {self.game_class_name}Move(BaseModel):
            """Represents a move in {self.game_name}."""
            # Add game-specific move fields here
            # Example:
            # position: Tuple[int, int] = Field(..., description="Position to play (row, col)")
            
            def __str__(self):
                # Provide a string representation of the move
                return f"Move description"
        ''')
        
        # Add analysis model if enabled
        if self.enable_analysis:
            content += dedent(f'''
            
            class {self.game_class_name}Analysis(BaseModel):
                """Analysis of a {self.game_name} position."""
                # Add game-specific analysis fields here
                # Example:
                # position_score: int = Field(..., description="Evaluation of the position (-10 to 10)")
                # recommendations: List[str] = Field(default_factory=list, description="Strategic recommendations")
            ''')
        
        # Add the game state class
        content += dedent(f'''
        
        class {self.game_class_name}State(GameState):
            """State for a {self.game_name} game."""
            # Add game-specific state fields here
            # Example:
            # board: List[List[Optional[str]]] = Field(..., description="Game board")
            turn: Literal["{self.player1_name}", "{self.player2_name}"] = Field(..., description="Current player's turn")
            game_status: Literal["ongoing", "{self.player1_name}_win", "{self.player2_name}_win", "draw"] = Field(
                default="ongoing", description="Status of the game"
            )
            move_history: List[{self.game_class_name}Move] = Field(
                default_factory=list, description="History of moves"
            )
        ''')
        
        # Add analysis fields if enabled
        if self.enable_analysis:
            content += dedent(f'''
            {self.player1_name}_analysis: List[Dict] = Field(
                default_factory=list, description="Analysis history for {self.player1_name}"
            )
            {self.player2_name}_analysis: List[Dict] = Field(
                default_factory=list, description="Analysis history for {self.player2_name}"
            )
            ''')
        
        # Add winner field
        content += dedent(f'''
            winner: Optional[str] = Field(
                default=None, description="Winner of the game, if any"
            )
            
            @property
            def board_string(self) -> str:
                """Get a string representation of the board."""
                # Implement board visualization here
                return "Board visualization"
        ''')
        
        # Write the file
        with open(f"{self.base_dir}/models.py", "w") as f:
            f.write(content.lstrip())
    
    def _generate_state_manager_file(self) -> None:
        """Generate the state.py file with game state management logic.
        
        This method creates a file containing the state manager class with:
        - Game initialization logic
        - Move application logic
        - Legal move generation
        - Game status checking
        
        The generated code includes placeholders for game-specific logic.
        """
        content = dedent(f'''
        from typing import List, Optional, Dict, Tuple
        import copy
        from .models import {self.game_class_name}State, {self.game_class_name}Move
        from ...framework.base import GameStateManager

        class {self.game_class_name}StateManager(GameStateManager[{self.game_class_name}State]):
            """Manager for {self.game_name} game state."""
            
            @classmethod
            def initialize(cls) -> {self.game_class_name}State:
                """Initialize a new {self.game_name} game."""
                # Implement game initialization logic here
                # Example:
                # board = [[None for _ in range(width)] for _ in range(height)]
                
                # Create and return the initial state
                return {self.game_class_name}State(
                    # Add required state fields here
                    turn="{self.player1_name}",
                    game_status="ongoing",
                    move_history=[]
                )
            
            @classmethod
            def apply_move(cls, state: {self.game_class_name}State, move: {self.game_class_name}Move) -> {self.game_class_name}State:
                """Apply a move to the {self.game_name} state."""
                # Create a deep copy of the state to avoid modifying the original
                new_state = copy.deepcopy(state)
                
                # Extract move details and apply to the state
                # ...
                
                # Update move history
                new_state.move_history.append(move)
                
                # Check for win/draw conditions
                # ...
                
                # Switch turns if game continues
                new_state.turn = "{self.player2_name}" if state.turn == "{self.player1_name}" else "{self.player1_name}"
                
                # Update game status if needed
                new_state = cls.check_game_status(new_state)
                
                return new_state
            
            @classmethod
            def get_legal_moves(cls, state: {self.game_class_name}State) -> List[{self.game_class_name}Move]:
                """Get all legal moves for the current state."""
                # Implement move generation logic here
                moves = []
                
                # Logic to determine valid moves
                # ...
                
                return moves
            
            @classmethod
            def check_game_status(cls, state: {self.game_class_name}State) -> {self.game_class_name}State:
                """Check and update game status."""
                # Implement win/loss/draw detection logic
                # ...
                
                return state
        ''')
        
        # Write the file
        with open(f"{self.base_dir}/state.py", "w") as f:
            f.write(content.lstrip())
    
    def _generate_config_file(self) -> None:
        """Generate the config.py file with agent configuration.
        
        This method creates a file containing:
        - LLM prompt templates for moves and analysis
        - AugLLM configurations for players and analyzers
        - Game-specific agent configuration class
        
        The generated code includes default configurations that can be customized.
        """
        content = dedent(f'''
        from ...framework.base import GameConfig
        from .models import {self.game_class_name}State, {self.game_class_name}PlayerDecision
        from ....core.aug_llm.base import AugLLMConfig
        from ....core.models.llm.base import AzureLLMConfig
        from langchain_core.prompts import ChatPromptTemplate
        from pydantic import Field
        from typing import Dict
        ''')
        
        # Add analysis import if enabled
        if self.enable_analysis:
            content += dedent(f'''
            from .models import {self.game_class_name}Analysis
            ''')
        
        content += dedent(f'''

        # Define the prompts for each agent

        def generate_move_prompt(player: str) -> ChatPromptTemplate:
            """Generate a prompt for making a move in {self.game_name}."""
            return ChatPromptTemplate.from_messages([
                ('system', 
                    f"You are the {{player}} player in a game of {self.game_name}. Your goal is to win by [game objective]."
                ),
                ('human', 
                    "Game State:\\n"
                    "{{board}}\\n\\n"
                    f"You are playing as {{player}}. It's your turn.\\n\\n"
                    "Legal Moves Available:\\n{{legal_moves}}\\n\\n"
                    "Recent Moves:\\n{{move_history}}\\n\\n"
                    "Choose the best move. Provide your reasoning."
                )
            ])
        ''')
        
        # Add analysis prompt if enabled
        if self.enable_analysis:
            content += dedent(f'''

            def generate_analysis_prompt(player: str) -> ChatPromptTemplate:
                """Generate a prompt for analyzing a {self.game_name} position."""
                return ChatPromptTemplate.from_messages([
                    ('system', 
                        f"You are a {self.game_name} strategy expert. Analyze the position from {{player}}'s perspective."
                    ),
                    ('human', 
                        "Game State:\\n"
                        "{{board}}\\n\\n"
                        f"Analyze the position for {{player}}.\\n\\n"
                        "Recent Moves:\\n{{move_history}}\\n\\n"
                        "Provide a detailed analysis including:\\n"
                        "1. Position evaluation\\n"
                        "2. Strategic advantages and disadvantages\\n"
                        "3. Recommended moves or plans"
                    )
                ])
            ''')
        
        content += dedent(f'''

        # Define the AugLLM configurations
        aug_llm_configs = {{
            "{self.player1_name}_player": AugLLMConfig(
                name="{self.player1_name}_player",
                llm_config=AzureLLMConfig(model="gpt-4o"),
                prompt_template=generate_move_prompt("{self.player1_name}"),
                structured_output_model={self.game_class_name}PlayerDecision
            ),
            "{self.player2_name}_player": AugLLMConfig(
                name="{self.player2_name}_player",
                llm_config=AzureLLMConfig(model="gpt-4o"),
                prompt_template=generate_move_prompt("{self.player2_name}"),
                structured_output_model={self.game_class_name}PlayerDecision
            ),''')
        
        # Add analyzer configs if enabled
        if self.enable_analysis:
            content += dedent(f'''
            "{self.player1_name}_analyzer": AugLLMConfig(
                name="{self.player1_name}_analyzer",
                llm_config=AzureLLMConfig(model="gpt-4o"),
                prompt_template=generate_analysis_prompt("{self.player1_name}"),
                structured_output_model={self.game_class_name}Analysis
            ),
            "{self.player2_name}_analyzer": AugLLMConfig(
                name="{self.player2_name}_analyzer",
                llm_config=AzureLLMConfig(model="gpt-4o"),
                prompt_template=generate_analysis_prompt("{self.player2_name}"),
                structured_output_model={self.game_class_name}Analysis
            ),''')
        
        content += dedent(f'''
        }}

        class {self.game_class_name}AgentConfig(GameConfig):
            """Configuration for the {self.game_name} agent."""
            state_schema: type = Field(default={self.game_class_name}State)
            aug_llm_configs: Dict[str, AugLLMConfig] = Field(
                default=aug_llm_configs, description="Config for the {self.game_name} agent."
            )
            enable_analysis: bool = Field(
                default={str(self.enable_analysis)}, description="Whether to enable analysis."
            )
            visualize: bool = Field(
                default=True, description="Whether to visualize the game."
            )

            @classmethod
            def default_config(cls):
                """Create a default configuration."""
                return cls(
                    state_schema={self.game_class_name}State,
                    aug_llm_configs=aug_llm_configs,
                    enable_analysis={str(self.enable_analysis)},
                    visualize=True
                )
        ''')
        
        # Write the file
        with open(f"{self.base_dir}/config.py", "w") as f:
            f.write(content.lstrip())
    
    def _generate_agent_file(self) -> None:
        """Generate the agent.py file with the main agent class.
        
        This method creates a file containing the game agent class with:
        - Move generation and extraction
        - Position analysis (if enabled)
        - Game state visualization
        - Integration with the framework
        
        The generated code includes proper error handling and logging.
        """
        content = dedent(f'''
        from typing import Dict, Any, List
        from langgraph.types import Command
        from ...framework.base import GameAgent
        from .models import {self.game_class_name}State, {self.game_class_name}Move, {self.game_class_name}PlayerDecision
        from .state import {self.game_class_name}StateManager
        from .config import {self.game_class_name}AgentConfig
        from ...base import register_agent
        import time
        ''')
        
        # Add analysis retrieval if enabled
        if self.enable_analysis:
            content += dedent(f'''
                if player == "{self.player1_name}" and state.{self.player1_name}_analysis:
                    player_analysis = state.{self.player1_name}_analysis[-1]
                elif player == "{self.player2_name}" and state.{self.player2_name}_analysis:
                    player_analysis = state.{self.player2_name}_analysis[-1]
            ''')
        
        content += dedent(f'''
                # Prepare the context
                return {{
                    "board": state.board_string,
                    "turn": state.turn,
                    "player": player,
                    "legal_moves": formatted_legal_moves,
                    "move_history": [str(move) for move in state.move_history[-5:]],  # Last 5 moves
                    "player_analysis": player_analysis
                }}
            
            def extract_move(self, response: {self.game_class_name}PlayerDecision) -> {self.game_class_name}Move:
                """Extract move from engine response."""
                return response.move
            
            def make_player1_move(self, state: {self.game_class_name}State) -> Command:
                """Make a move for {self.player1_name}."""
                return self.make_move(state, "{self.player1_name}")
            
            def make_player2_move(self, state: {self.game_class_name}State) -> Command:
                """Make a move for {self.player2_name}."""
                return self.make_move(state, "{self.player2_name}")
        ''')
        
        # Add analysis methods if enabled
        if self.enable_analysis:
            content += dedent(f'''
            
            def prepare_analysis_context(self, state: {self.game_class_name}State, player: str) -> Dict[str, Any]:
                """Prepare context for position analysis."""
                return {{
                    "board": state.board_string,
                    "turn": state.turn,
                    "player": player,
                    "move_history": [str(move) for move in state.move_history[-5:]]
                }}
            
            def analyze_player1(self, state: {self.game_class_name}State) -> Command:
                """Analyze position for {self.player1_name}."""
                return self.analyze_position(state, "{self.player1_name}")
            
            def analyze_player2(self, state: {self.game_class_name}State) -> Command:
                """Analyze position for {self.player2_name}."""
                return self.analyze_position(state, "{self.player2_name}")
            ''')
        
        content += dedent(f'''
            
            def visualize_state(self, state: Dict[str, Any]) -> None:
                """Visualize the current game state."""
                # Create a {self.game_class_name}State from the dict
                game_state = {self.game_class_name}State(**state)
                
                print("\\n" + "=" * 50)
                print(f"🎮 Current Player: {{game_state.turn}}")
                print(f"📌 Game Status: {{game_state.game_status}}")
                print("=" * 50)
                
                # Print the board
                print("\\n" + game_state.board_string)
                
                # Print last move if available
                if game_state.move_history:
                    last_move = game_state.move_history[-1]
                    print(f"\\n📝 Last Move: {{last_move}}")
        ''')
        
        # Add analysis visualization if enabled
        if self.enable_analysis:
            content += dedent(f'''
                
                # Print analyses if available
                if game_state.{self.player1_name}_analysis and game_state.turn == "{self.player2_name}":
                    last_analysis = game_state.{self.player1_name}_analysis[-1]
                    print(f"\\n�� {self.player1_name.capitalize()}'s Analysis:")
                    # Print key analysis points here based on your analysis model structure
                    
                if game_state.{self.player2_name}_analysis and game_state.turn == "{self.player1_name}":
                    last_analysis = game_state.{self.player2_name}_analysis[-1]
                    print(f"\\n🔍 {self.player2_name.capitalize()}'s Analysis:")
                    # Print key analysis points here based on your analysis model structure
            ''')
        
        content += dedent(f'''
                
                # Add a short delay for readability
                time.sleep(0.5)
        ''')
        
        # Write the file
        with open(f"{self.base_dir}/agent.py", "w") as f:
            f.write(content.lstrip())
    
    def _generate_example_file(self) -> None:
        """Generate an example.py file to demonstrate agent usage.
        
        This method creates a file containing:
        - Example game setup and configuration
        - Game execution with visualization
        - State history saving
        
        The generated code serves as a starting point for using the agent.
        """
        content = dedent(f'''
        from .agent import {self.game_class_name}Agent
        from .config import {self.game_class_name}AgentConfig
        import time

        def run_{self.game_slug}_game():
            """Run a {self.game_name} game with visualization."""
            # Create agent with default config
            agent = {self.game_class_name}Agent({self.game_class_name}AgentConfig.default_config())
            
            # Initialize game state
            initial_state = {{
                # Add required state fields for initialization
                "turn": "{self.player1_name}",
                "game_status": "ongoing",
                "move_history": [],
        ''')
        
        # Add analysis state fields if enabled
        if self.enable_analysis:
            content += dedent(f'''
                "{self.player1_name}_analysis": [],
                "{self.player2_name}_analysis": [],
            ''')
        
        content += dedent(f'''
            }}
            
            # Run the game
            print("\\n🎮 Starting {self.game_name} Game")
            print("=" * 50)
            
            for step in agent.app.stream(
                initial_state,
                config=agent.runnable_config,
                debug=True,
                stream_mode="values"
            ):
                # Visualize the game state
                agent.visualize_state(step)
                
                # Check for game over
                if step.get("game_status") != "ongoing":
                    print(f"\\n🏆 Game Status: {{step['game_status'].upper()}}")
                    if step.get("winner"):
                        print(f"🎖️ Winner: {{step['winner']}}")
            
            # Save game history
            agent.save_state_history()
            print("\\n✅ Game Complete!")

        if __name__ == "__main__":
            run_{self.game_slug}_game()
        ''')
        
        # Write the file
        with open(f"{self.base_dir}/example.py", "w") as f:
            f.write(content.lstrip())