# Haive Code Style Guide - Python Documentation Standards

**Version**: 1.0  
**Date**: 2025-01-08  
**Purpose**: Comprehensive guide for writing high-quality Python code with proper type hints and documentation in the Haive framework

## 🎯 Core Principles

1. **Everything Must Be Typed**: No untyped public APIs
2. **Everything Must Be Documented**: Google-style docstrings for all public elements
3. **Examples Required**: Working code examples in all major components
4. **Sphinx-Ready**: All documentation must work with Sphinx autodoc
5. **Pydantic-First**: Use Pydantic models with comprehensive field documentation

## 📝 Documentation Standards

### Module-Level Documentation

```python
"""Module for advanced chess game implementation with LLM-powered players.

This module provides a complete chess game implementation featuring:
    - Professional chess rules with FEN notation support
    - LLM-powered strategic analysis and move generation
    - Rich visualization and game state management
    - Tournament support and performance analysis

The module follows standard chess protocols and integrates seamlessly
with the Haive agent framework for sophisticated gameplay.

Examples:
    Basic chess game setup::

        from haive.games.chess import ChessAgent, ChessConfig
        from haive.core.models.llm.configs import LLMConfig
        
        config = ChessConfig(
            aug_llm_configs={
                "white_player": LLMConfig(model="gpt-4"),
                "black_player": LLMConfig(model="gpt-4")
            }
        )
        agent = ChessAgent(config)
        result = agent.run_game()

    Advanced configuration with analysis::

        config = ChessConfig(
            enable_analysis=True,
            analysis_depth=3,
            time_control=300
        )
        agent = ChessAgent(config)
        analysis = agent.analyze_position("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")

Notes:
    This module requires the python-chess library for game rules
    and FEN notation support. Install with: pip install python-chess

See Also:
    - haive.games.checkers: Similar board game implementation
    - haive.core.agents: Base agent framework
"""
```

### Class Documentation

```python
class ChessAgent(GameAgent[ChessConfig]):
    """AI-powered chess agent with strategic analysis and move generation.
    
    This agent implements a complete chess game using language models for
    move generation, position analysis, and strategic planning. It supports
    various chess formats, time controls, and analysis modes.
    
    The agent uses a state-based approach with LangGraph for managing the
    game workflow and supports both automated play and human interaction.
    
    Attributes:
        config (ChessConfig): Configuration for the chess agent including
            LLM settings, time controls, and analysis options.
        state_manager (ChessStateManager): Manager for game state operations
            including move validation, check detection, and endgame analysis.
        engines (Dict[str, BaseEngine]): LLM engines for different game
            components (white_player, black_player, analyzer, opening_book).
        analysis_cache (Dict[str, ChessAnalysis]): Cached position analyses
            for performance optimization.
    
    Examples:
        Create and run a basic chess game::
        
            config = ChessConfig()
            agent = ChessAgent(config)
            result = agent.run_game(visualize=True)
            print(f"Winner: {result.winner}")
        
        Run with custom time control::
        
            config = ChessConfig(
                time_control=600,  # 10 minutes per side
                increment=5,       # 5 second increment
                enable_analysis=True
            )
            agent = ChessAgent(config)
            result = agent.run_game()
        
        Analyze specific position::
        
            agent = ChessAgent(config)
            fen = "rnbqk2r/pppp1ppp/5n2/2b1p3/2B1P3/3P1N2/PPP2PPP/RNBQK2R w KQkq - 4 4"
            analysis = agent.analyze_position(fen)
            print(f"Best move: {analysis.best_move}")
            print(f"Evaluation: {analysis.evaluation}")
    
    Raises:
        ConfigurationError: If LLM configurations are invalid or missing.
        ChessError: If game rules are violated or invalid moves are attempted.
        TimeoutError: If move generation exceeds configured time limits.
    
    Note:
        The agent automatically handles chess rules including castling,
        en passant, pawn promotion, and draw conditions. All moves are
        validated using the python-chess library.
    
    See Also:
        ChessConfig: Configuration options for the chess agent.
        ChessState: Game state representation and management.
        ChessAnalysis: Position analysis and evaluation results.
    """
    
    def __init__(self, config: ChessConfig) -> None:
        """Initialize the chess agent with configuration.
        
        Sets up the chess agent with the provided configuration, initializes
        the state manager, creates LLM engines, and prepares the game workflow.
        
        Args:
            config (ChessConfig): Configuration object containing LLM settings,
                time controls, analysis options, and other game parameters.
                Must include valid aug_llm_configs for at least white_player
                and black_player engines.
        
        Raises:
            ConfigurationError: If required LLM configurations are missing
                or if time control settings are invalid.
            ValidationError: If config contains invalid parameter values.
        
        Example:
            Initialize with basic configuration::
            
                config = ChessConfig(
                    aug_llm_configs={
                        "white_player": LLMConfig(model="gpt-4"),
                        "black_player": LLMConfig(model="gpt-4")
                    }
                )
                agent = ChessAgent(config)
        """
        super().__init__(config)
        self.state_manager = ChessStateManager()
        self.analysis_cache: Dict[str, ChessAnalysis] = {}
        self._setup_engines()
        self._initialize_workflow()
    
    async def analyze_position(
        self, 
        fen: str, 
        depth: Optional[int] = None,
        include_variations: bool = True
    ) -> ChessAnalysis:
        """Analyze a chess position and return strategic evaluation.
        
        Performs comprehensive analysis of the given position including
        move suggestions, positional evaluation, tactical opportunities,
        and strategic assessments.
        
        Args:
            fen (str): FEN notation string representing the position to analyze.
                Must be a valid FEN string with all required components.
            depth (Optional[int]): Analysis depth level (1-5). If None, uses
                the configured analysis_depth from the agent config.
                Higher depths provide more thorough analysis but take longer.
            include_variations (bool): Whether to include tactical variations
                and alternative move sequences in the analysis. Defaults to True.
        
        Returns:
            ChessAnalysis: Comprehensive analysis results containing:
                - best_move (str): Recommended best move in algebraic notation
                - evaluation (float): Position evaluation (-10.0 to +10.0)
                - principal_variation (List[str]): Best move sequence
                - tactical_themes (List[str]): Identified tactical patterns
                - strategic_notes (str): Human-readable strategic assessment
                - candidate_moves (List[Tuple[str, float]]): Alternative moves with scores
        
        Raises:
            ValueError: If FEN string is invalid or malformed.
            AnalysisError: If position analysis fails due to LLM errors.
            TimeoutError: If analysis exceeds configured timeout limits.
        
        Examples:
            Analyze starting position::
            
                agent = ChessAgent(config)
                fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
                analysis = await agent.analyze_position(fen)
                print(f"Opening recommendation: {analysis.best_move}")
            
            Deep analysis with variations::
            
                analysis = await agent.analyze_position(
                    fen="r2qk2r/ppp2ppp/2n1bn2/2bpp3/3PP3/2N2N2/PPPB1PPP/R2QKB1R w KQkq - 0 7",
                    depth=4,
                    include_variations=True
                )
                for move, score in analysis.candidate_moves:
                    print(f"{move}: {score}")
        
        Note:
            Analysis results are cached based on FEN and depth to improve
            performance. Cache is automatically invalidated when configuration
            changes that might affect analysis quality.
        """
        # Implementation would go here
        pass
```

### Method Documentation

```python
def make_move(
    self, 
    state: ChessState, 
    move: str, 
    validate: bool = True,
    record_time: bool = True
) -> ChessState:
    """Execute a chess move and return the updated game state.
    
    Processes the given move, validates it according to chess rules,
    updates the game state, and checks for special conditions like
    check, checkmate, or draw.
    
    Args:
        state (ChessState): Current game state before the move.
            Must be a valid ChessState with proper board position.
        move (str): Move to execute in algebraic notation (e.g., "e4", "Nf3",
            "O-O", "exd5"). Supports standard algebraic notation including
            castling, en passant, and pawn promotion.
        validate (bool): Whether to validate the move before execution.
            Defaults to True. Set to False only for pre-validated moves
            to improve performance.
        record_time (bool): Whether to record move time for time control.
            Defaults to True. Used for tournament play and analysis.
    
    Returns:
        ChessState: Updated game state after the move execution containing:
            - Updated board position
            - Move history with timestamps
            - Current player turn
            - Game status (ongoing, check, checkmate, draw)
            - Time remaining for both players
    
    Raises:
        InvalidMoveError: If the move is illegal according to chess rules
            or if the move syntax is invalid.
        GameOverError: If attempting to move when the game has already ended.
        TimeControlError: If the player has insufficient time remaining.
    
    Examples:
        Execute a simple pawn move::
        
            new_state = agent.make_move(current_state, "e4")
            assert new_state.last_move == "e4"
        
        Execute castling move::
        
            new_state = agent.make_move(current_state, "O-O", validate=True)
            assert new_state.castling_rights.white_kingside == False
        
        Handle pawn promotion::
        
            new_state = agent.make_move(current_state, "exd8=Q")
            assert "Q" in new_state.board.piece_at(chess.D8).symbol()
    
    Note:
        Move validation includes checking for legal piece movement,
        piece blocking, check conditions, and special moves. All moves
        are recorded in the game history with precise timestamps.
    """
    # Implementation would go here
    pass
```

### Pydantic Model Documentation

```python
class ChessMove(BaseModel):
    """Represents a chess move with validation and metadata.
    
    This model encapsulates all information about a chess move including
    the move notation, timing, analysis, and game context. It provides
    validation for move syntax and integrates with the chess engine
    for rule checking.
    
    Attributes:
        move (str): The move in standard algebraic notation.
        player (str): Player making the move ("white" or "black").
        timestamp (datetime): When the move was made.
        analysis (Optional[ChessMoveAnalysis]): Analysis of the move quality.
        time_taken (Optional[float]): Time in seconds taken to make the move.
        evaluation (Optional[float]): Position evaluation after the move.
    
    Examples:
        Create a basic move::
        
            move = ChessMove(
                move="e4",
                player="white",
                timestamp=datetime.now()
            )
        
        Create move with analysis::
        
            move = ChessMove(
                move="Nf3",
                player="white",
                timestamp=datetime.now(),
                analysis=ChessMoveAnalysis(
                    quality_score=0.85,
                    move_type="development",
                    alternatives=["e4", "d4"]
                ),
                time_taken=2.5,
                evaluation=0.3
            )
    
    Note:
        Move validation is performed on assignment. Invalid moves will
        raise a ValidationError with specific details about the issue.
    """
    
    move: str = Field(
        ...,
        description="Chess move in standard algebraic notation (e.g., 'e4', 'Nf3', 'O-O')",
        regex=r"^[NBRQK]?[a-h]?[1-8]?x?[a-h][1-8](?:=[NBRQ])?[+#]?$|^O-O(?:-O)?[+#]?$",
        examples=["e4", "Nf3", "Bxf7+", "O-O", "exd8=Q#"]
    )
    
    player: Literal["white", "black"] = Field(
        ...,
        description="Player making the move, either 'white' or 'black'",
        examples=["white", "black"]
    )
    
    timestamp: datetime = Field(
        default_factory=datetime.now,
        description="UTC timestamp when the move was made",
        examples=["2024-01-08T15:30:45.123456"]
    )
    
    analysis: Optional[ChessMoveAnalysis] = Field(
        None,
        description="Optional analysis of the move quality and alternatives",
        examples=[{
            "quality_score": 0.85,
            "move_type": "development",
            "alternatives": ["e4", "d4"]
        }]
    )
    
    time_taken: Optional[float] = Field(
        None,
        ge=0.0,
        le=3600.0,
        description="Time in seconds taken to make the move (0-3600)",
        examples=[2.5, 45.2, 120.0]
    )
    
    evaluation: Optional[float] = Field(
        None,
        ge=-10.0,
        le=10.0,
        description="Position evaluation after the move (-10.0 to +10.0, positive favors white)",
        examples=[0.3, -1.2, 2.8]
    )
    
    @field_validator('move')
    @classmethod
    def validate_move_syntax(cls, v: str) -> str:
        """Validate chess move syntax using regex pattern.
        
        Args:
            v (str): Move string to validate.
            
        Returns:
            str: Validated move string.
            
        Raises:
            ValueError: If move syntax is invalid.
            
        Examples:
            Valid moves: "e4", "Nf3", "Bxf7+", "O-O", "exd8=Q#"
            Invalid moves: "e9", "Zh3", "O-O-O-O"
        """
        if not v or len(v) > 10:
            raise ValueError("Move must be 1-10 characters")
        
        # Additional validation logic would go here
        return v.strip()
    
    @computed_field
    @property
    def is_capture(self) -> bool:
        """Check if the move is a capture.
        
        Returns:
            bool: True if the move contains 'x' indicating a capture.
            
        Examples:
            >>> move = ChessMove(move="Bxf7+", player="white")
            >>> move.is_capture
            True
            >>> move = ChessMove(move="Nf3", player="white")
            >>> move.is_capture
            False
        """
        return 'x' in self.move
    
    @computed_field
    @property
    def is_check(self) -> bool:
        """Check if the move gives check.
        
        Returns:
            bool: True if the move ends with '+' or '#'.
            
        Examples:
            >>> move = ChessMove(move="Qh5+", player="white")
            >>> move.is_check
            True
        """
        return self.move.endswith(('+', '#'))

    class Config:
        """Pydantic configuration for ChessMove model."""
        
        json_schema_extra = {
            "examples": [
                {
                    "move": "e4",
                    "player": "white",
                    "timestamp": "2024-01-08T15:30:45.123456",
                    "time_taken": 2.5,
                    "evaluation": 0.3
                },
                {
                    "move": "Nf6", 
                    "player": "black",
                    "timestamp": "2024-01-08T15:30:48.654321",
                    "analysis": {
                        "quality_score": 0.92,
                        "move_type": "development",
                        "alternatives": ["e6", "d6"]
                    },
                    "time_taken": 1.8,
                    "evaluation": -0.1
                }
            ]
        }
```

### Function Documentation

```python
def analyze_chess_position(
    fen: str,
    depth: int = 3,
    engine_config: Optional[EngineConfig] = None,
    include_variations: bool = True
) -> ChessAnalysis:
    """Analyze a chess position and return comprehensive evaluation.
    
    Performs deep analysis of the given position using the configured
    chess engine and LLM for strategic assessment. Returns detailed
    evaluation including best moves, tactical themes, and strategic plans.
    
    Args:
        fen (str): FEN notation string representing the position.
            Must be a complete and valid FEN string.
        depth (int): Analysis depth from 1-10. Higher values provide
            more accurate analysis but take longer. Defaults to 3.
        engine_config (Optional[EngineConfig]): Configuration for the
            analysis engine. If None, uses default configuration.
        include_variations (bool): Whether to include move variations
            in the analysis. Defaults to True.
    
    Returns:
        ChessAnalysis: Comprehensive analysis containing:
            - best_move: Recommended best move
            - evaluation: Numerical position evaluation
            - principal_variation: Best line continuation
            - tactical_themes: Identified patterns
            - strategic_assessment: Long-term evaluation
    
    Raises:
        ValueError: If FEN string is invalid or malformed.
        EngineError: If chess engine analysis fails.
        TimeoutError: If analysis exceeds time limits.
    
    Examples:
        Analyze starting position::
        
            fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
            analysis = analyze_chess_position(fen, depth=2)
            print(f"Best opening move: {analysis.best_move}")
        
        Deep tactical analysis::
        
            tactical_fen = "r2qk2r/ppp2ppp/2n1bn2/2bpp3/3PP3/2N2N2/PPPB1PPP/R2QKB1R w KQkq - 0 7"
            analysis = analyze_chess_position(
                fen=tactical_fen,
                depth=5,
                include_variations=True
            )
            for theme in analysis.tactical_themes:
                print(f"Tactical theme: {theme}")
    
    Note:
        Analysis quality improves significantly with higher depth values,
        but computation time increases exponentially. For interactive use,
        depths 2-4 provide good balance of speed and accuracy.
    """
    # Implementation would go here
    pass
```

## 🔧 Type Hints Standards

### Basic Types

```python
# Primitive types
name: str = "chess_game"
count: int = 64
score: float = 0.5
is_active: bool = True

# Optional types
description: Optional[str] = None
config: Optional[Dict[str, Any]] = None

# Union types (prefer | syntax in Python 3.10+)
result: str | None = None
value: int | float = 42

# Generic types
moves: List[str] = []
positions: Dict[str, Tuple[int, int]] = {}
cache: Dict[str, Any] = {}
```

### Function Signatures

```python
# Simple function
def calculate_score(moves: List[str], weights: Dict[str, float]) -> float:
    """Calculate weighted score from moves."""
    pass

# Async function
async def analyze_position(
    fen: str, 
    depth: int = 3,
    timeout: Optional[float] = None
) -> ChessAnalysis:
    """Analyze position asynchronously."""
    pass

# Generic function
from typing import TypeVar, Generic

T = TypeVar('T')

def process_game_data(data: List[T], processor: Callable[[T], Any]) -> List[Any]:
    """Process game data with custom processor."""
    pass
```

### Class Type Hints

```python
class GameAgent(Generic[TConfig]):
    """Base game agent with generic configuration."""
    
    def __init__(self, config: TConfig) -> None:
        self.config: TConfig = config
        self.state: Optional[GameState] = None
        self.history: List[Move] = []
    
    @property
    def is_active(self) -> bool:
        """Check if agent is actively playing."""
        return self.state is not None
    
    def process_move(self, move: Move) -> GameState:
        """Process a move and return new state."""
        pass
```

### Pydantic Model Type Hints

```python
class ChessConfig(BaseModel):
    """Configuration for chess game."""
    
    # Required fields with types
    player_names: Dict[str, str] = Field(
        ..., 
        description="Mapping of player IDs to display names"
    )
    
    # Optional fields with defaults
    time_control: Optional[int] = Field(
        None,
        ge=1,
        le=3600,
        description="Time control in seconds (1-3600)"
    )
    
    # Complex types
    engine_configs: Dict[str, LLMConfig] = Field(
        default_factory=dict,
        description="LLM configurations for different engines"
    )
    
    # Validators with proper types
    @field_validator('player_names')
    @classmethod
    def validate_player_names(cls, v: Dict[str, str]) -> Dict[str, str]:
        """Validate player names are non-empty."""
        for player_id, name in v.items():
            if not name.strip():
                raise ValueError(f"Empty name for player {player_id}")
        return v
```

## 📊 Quality Checklist

### ✅ Required for Every Module

- [ ] **Module docstring** with examples and purpose
- [ ] **All classes documented** with Google-style docstrings  
- [ ] **All public methods documented** with Args/Returns/Raises
- [ ] **Type hints on everything** - functions, methods, variables
- [ ] **Pydantic fields documented** with descriptions and examples
- [ ] **Working code examples** in docstrings
- [ ] **Validation logic documented** with examples
- [ ] **Error conditions documented** with specific exceptions

### ✅ Sphinx Compatibility

- [ ] **RST formatting** in docstrings where needed
- [ ] **Cross-references** using proper Sphinx syntax
- [ ] **Code blocks** properly formatted with language hints
- [ ] **Examples tested** and verified to work
- [ ] **API references** link correctly

### ✅ Code Quality

- [ ] **No type: ignore** comments (fix the types instead)
- [ ] **No Any types** unless absolutely necessary
- [ ] **Proper error handling** with specific exceptions
- [ ] **Validation on all inputs** with clear error messages
- [ ] **Performance considerations** documented where relevant

## 🎯 Implementation Priority

1. **Start with models.py** - Foundation for everything else
2. **Move to config.py** - Configuration must be perfect
3. **Update agent.py** - Main logic with comprehensive examples
4. **Polish state.py** - State management documentation
5. **Finish with utilities** - Helper functions and utilities

This guide ensures all code in the Haive framework meets professional standards for type safety, documentation, and usability.