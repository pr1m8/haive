:orphan:

# Haive Games: Chess Module

## Overview

The Chess module provides a comprehensive implementation of chess for AI agents. It features complete game state representation, move validation, algebraic notation parsing, and strategic decision-making through LLM-based agents. This module enables AI agents to play chess with sophisticated reasoning about position evaluation, tactics, and long-term strategy.

## Key Features

- **Complete Chess Rules**: Full implementation of chess rules including special moves (castling, en passant, promotion)
- **Algebraic Notation**: Support for standard chess notation for move input/output
- **Position Evaluation**: Sophisticated position analysis through LLM reasoning
- **State Management**: Comprehensive game state tracking with move history
- **Move Validation**: Thorough legal move validation and generation
- **Visualization**: ASCII and Unicode board representations
- **Game Analysis**: Post-game analysis of critical positions
- **Opening Book**: Optional integration with chess opening theory

## Installation

This module is part of the `haive-games` package. Install the full package with:

```bash
pip install haive-games
```

## Quick Start

```python
from haive.games.chess import ChessAgent, ChessConfig
from haive.core.engine.aug_llm import AugLLMConfig

# Configure the game
config = ChessConfig(
    player_names=["White", "Black"],
    time_control="rapid",  # Options: blitz, rapid, classical
    llm_config=AugLLMConfig(
        system_message="You are playing chess. Analyze the position carefully and make the best move.",
        temperature=0.2  # Lower temperature for more consistent play
    )
)

# Create and run the game
agent = ChessAgent(config)
result = agent.run()

# View results
print(f"Game result: {result.outcome}")
print(f"Move history: {result.move_history}")
```

## Components

### ChessAgent

Main agent class that orchestrates the chess game.

```python
from haive.games.chess import ChessAgent, ChessConfig

# Create a custom configuration
config = ChessConfig(
    player_names=["Magnus", "Hikaru"],
    time_control="classical",
    use_opening_book=True,
    skill_level=8  # 1-10 scale
)

# Create the agent
agent = ChessAgent(config)

# Run a full game
result = agent.run()
```

### ChessState

Game state representation for chess.

```python
from haive.games.chess import ChessState, Piece, Square

# Create a chess state from FEN notation
state = ChessState.from_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")

# Get a piece at a square
piece = state.get_piece_at("e4")
if piece:
    print(f"Piece at e4: {piece.symbol}")
else:
    print("No piece at e4")

# Check if a move is legal
is_legal = state.is_legal_move("e2", "e4")
```

### ChessStateManager

Handles game logic, state transitions, and rule enforcement.

```python
from haive.games.chess import ChessStateManager, ChessConfig, ChessMove

# Create a state manager
config = ChessConfig(player_names=["White", "Black"])
state_manager = ChessStateManager(config)

# Initialize a new game
state = state_manager.initialize_state()

# Process a move in algebraic notation
move = ChessMove.from_algebraic("e4")
new_state = state_manager.apply_move(state, move)

# Check for check, checkmate, stalemate
is_check = state_manager.is_in_check(new_state)
is_checkmate = state_manager.is_checkmate(new_state)
is_stalemate = state_manager.is_stalemate(new_state)
```

## Game Structure

A chess game follows this structure:

1. **Setup**: Initialize the board with pieces in their starting positions
2. **Gameplay Loop**:
   - Current player selects a legal move
   - Apply the move to create a new game state
   - Check for game-ending conditions (checkmate, stalemate, draw)
   - Switch to the other player
3. **Game End**: Determine the outcome (white win, black win, draw)

Special rules handled:

- Castling (kingside and queenside)
- En passant captures
- Pawn promotion
- Threefold repetition
- Fifty-move rule
- Insufficient material

## Usage Patterns

### Custom Position Evaluation

```python
from haive.games.chess import ChessAgent, ChessState
from haive.core.engine.aug_llm import AugLLMConfig, compose_runnable

class PositionalChessAgent(ChessAgent):
    def __init__(self, config):
        super().__init__(config)

        # Create specialized evaluation engine
        self.eval_engine = compose_runnable(AugLLMConfig(
            system_message="""
            You are a chess position evaluator. Analyze positions for:
            1. Material balance
            2. Piece activity and coordination
            3. King safety
            4. Pawn structure
            5. Control of key squares and diagonals
            6. Development and initiative

            Provide a numerical evaluation between -2.0 (clear advantage for black)
            and +2.0 (clear advantage for white).
            """,
            temperature=0.1
        ))

    def evaluate_position(self, state):
        # Convert state to FEN notation
        fen = state.to_fen()

        # Get board representation
        board_repr = self.get_board_representation(state)

        # Get evaluation from LLM
        prompt = f"""
        Current position:

        {board_repr}

        FEN: {fen}

        Last move: {state.last_move}

        Evaluate this position numerically between -2.0 and +2.0.
        """

        response = self.eval_engine.invoke(prompt)

        # Parse numerical evaluation
        try:
            # Extract numerical value from response
            import re
            match = re.search(r'([+-]?\d+\.\d+)', response)
            if match:
                return float(match.group(1))
            return 0.0
        except:
            return 0.0
```

### Opening Book Integration

```python
from haive.games.chess import ChessAgent, ChessState
import json

class OpeningBookChessAgent(ChessAgent):
    def __init__(self, config):
        super().__init__(config)
        self.opening_book = self.load_opening_book()

    def load_opening_book(self):
        """Load chess opening book from JSON file."""
        with open("chess_openings.json", "r") as f:
            return json.load(f)

    def get_opening_move(self, state):
        """Get move from opening book if available."""
        # Convert move history to string key
        moves_key = " ".join(state.move_history)

        # Check if position is in opening book
        if moves_key in self.opening_book:
            # Get possible moves and their weights
            moves = self.opening_book[moves_key]["moves"]

            # Select move based on weights
            import random
            total_weight = sum(move["weight"] for move in moves)
            r = random.uniform(0, total_weight)

            running_sum = 0
            for move in moves:
                running_sum += move["weight"]
                if r <= running_sum:
                    return move["move"]

        # Not in opening book, use regular move generation
        return None

    def get_agent_move(self, state):
        # Try opening book first
        opening_move = self.get_opening_move(state)
        if opening_move:
            return opening_move

        # Fall back to LLM-based move selection
        return super().get_agent_move(state)
```

### Game Analysis and Visualization

```python
from haive.games.chess import ChessAgent, ChessConfig
from haive.games.chess.ui import ChessVisualizer

# Run a game
config = ChessConfig(player_names=["Player 1", "Player 2"])
agent = ChessAgent(config)
result = agent.run()

# Create a visualizer
visualizer = ChessVisualizer()

# Generate game summary
summary = visualizer.generate_game_summary(result)
print(summary)

# Visualize a specific position
position_viz = visualizer.visualize_position(result.state_history[15])
print(position_viz)

# Generate PGN notation
pgn = visualizer.generate_pgn(result)
with open("game.pgn", "w") as f:
    f.write(pgn)

# Identify critical positions
critical_positions = visualizer.find_critical_positions(result)
for i, position in enumerate(critical_positions):
    print(f"Critical position {i+1}:")
    print(visualizer.visualize_position(position))
    print(visualizer.analyze_position(position))
```

## Integration with Other Modules

### Integration with Tournament System

```python
from haive.games.chess import ChessAgent, ChessConfig
from haive.games.tournament import TournamentManager

# Create tournament configuration
tournament_config = {
    "num_players": 8,
    "format": "round_robin",  # Options: round_robin, swiss, knockout
    "rounds": 7,
    "time_control": "rapid",
    "scoring": {"win": 1, "draw": 0.5, "loss": 0}
}

# Create tournament manager
tournament = TournamentManager(
    game_class=ChessAgent,
    game_config_class=ChessConfig,
    tournament_config=tournament_config
)

# Run tournament
results = tournament.run()
```

### Integration with Engine Evaluation

```python
from haive.games.chess import ChessState
from haive.games.chess.analysis import StockfishAnalyzer

# Create a state
state = ChessState.from_fen("r1bqkbnr/pppp1ppp/2n5/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq - 2 3")

# Create analyzer
analyzer = StockfishAnalyzer(depth=20)

# Get position evaluation
eval_result = analyzer.evaluate_position(state)
print(f"Evaluation: {eval_result.score}")

# Get top 3 moves
top_moves = analyzer.get_top_moves(state, n=3)
for i, move_info in enumerate(top_moves):
    print(f"{i+1}. {move_info['move']} - Eval: {move_info['score']}")
```

## Google-Style Docstrings

Here are examples of Google-style docstrings used in the module:

```python
def is_legal_move(self, from_square: str, to_square: str) -> bool:
    """Checks if a move from one square to another is legal.

    This method validates whether a chess piece can legally move from the
    source square to the destination square according to chess rules. It
    checks piece movement rules, board boundaries, and special conditions
    like check.

    Args:
        from_square: The source square in algebraic notation (e.g., "e2").
        to_square: The destination square in algebraic notation (e.g., "e4").

    Returns:
        True if the move is legal, False otherwise.

    Examples:
        >>> state = ChessState.from_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
        >>> state.is_legal_move("e2", "e4")
        True
        >>> state.is_legal_move("e2", "e5")
        False
    """
    # Implementation...
```

```python
class ChessMove:
    """Represents a chess move with source and destination squares.

    This class encapsulates a chess move, including source and destination squares,
    and handles special moves like castling and promotion. It provides methods
    for parsing and generating algebraic notation.

    Attributes:
        from_square: The source square in algebraic notation.
        to_square: The destination square in algebraic notation.
        promotion_piece: The piece to promote to, if applicable.
        is_castling: Whether this move is a castling move.
        is_en_passant: Whether this move is an en passant capture.

    Examples:
        >>> move = ChessMove("e2", "e4")
        >>> str(move)
        'e2-e4'
        >>> move = ChessMove.from_algebraic("Nf3")
        >>> move.from_square
        'g1'
        >>> move.to_square
        'f3'
    """

    def __init__(self, from_square: str, to_square: str, promotion_piece: str = None):
        """Initializes a ChessMove.

        Args:
            from_square: The source square in algebraic notation.
            to_square: The destination square in algebraic notation.
            promotion_piece: The piece to promote to, if applicable.
        """
        # Implementation...
```

## Advanced Patterns

### Time Control Implementation

```python
from haive.games.chess import ChessAgent, ChessConfig
import time

class TimedChessAgent(ChessAgent):
    """Chess agent with time control enforcement."""

    def __init__(self, config):
        super().__init__(config)
        self.time_remaining = {
            "white": config.initial_time,
            "black": config.initial_time
        }
        self.increment = config.increment

    def get_agent_move(self, state):
        """Get move with time tracking."""
        color = state.turn
        start_time = time.time()

        # Set time limit for decision
        time_for_move = min(
            self.time_remaining[color] * 0.1,  # Use 10% of remaining
            30  # Max 30 seconds per move
        )

        # Get move with timeout
        move = self.get_move_with_timeout(state, time_for_move)

        # Update clock
        elapsed = time.time() - start_time
        self.time_remaining[color] -= elapsed
        self.time_remaining[color] += self.increment

        # Check for time forfeit
        if self.time_remaining[color] <= 0:
            return self.handle_time_forfeit(color)

        return move
```

### Multi-Engine Consultation

```python
class ConsultationChessAgent(ChessAgent):
    """Chess agent that consults multiple engines."""

    def __init__(self, config):
        super().__init__(config)
        self.engines = [
            self.create_tactical_engine(),
            self.create_positional_engine(),
            self.create_endgame_engine()
        ]

    def get_agent_move(self, state):
        """Get move by consulting multiple engines."""
        # Get candidate moves from each engine
        candidates = []
        for engine in self.engines:
            move = engine.suggest_move(state)
            eval = engine.evaluate_move(state, move)
            candidates.append((move, eval, engine.name))

        # Weight moves by engine expertise
        if self.is_endgame(state):
            # Prioritize endgame engine
            weights = [0.2, 0.2, 0.6]
        elif self.has_tactical_opportunity(state):
            # Prioritize tactical engine
            weights = [0.6, 0.3, 0.1]
        else:
            # Balanced weights
            weights = [0.33, 0.34, 0.33]

        # Select best weighted move
        best_move = self.select_weighted_move(candidates, weights)
        return best_move
```

### Learning from Games

```python
from haive.games.chess import ChessAgent
import json

class LearningChessAgent(ChessAgent):
    """Chess agent that learns from past games."""

    def __init__(self, config):
        super().__init__(config)
        self.game_database = self.load_game_database()
        self.position_evaluations = {}

    def post_game_analysis(self, game_result):
        """Analyze completed game for learning."""
        # Identify critical positions
        critical_positions = self.find_critical_positions(game_result)

        # Store evaluations
        for position in critical_positions:
            fen = position.to_fen()
            evaluation = {
                "move_played": position.last_move,
                "result": game_result.outcome,
                "engine_eval": self.evaluate_position(position),
                "better_moves": self.find_better_moves(position)
            }
            self.position_evaluations[fen] = evaluation

        # Update database
        self.save_to_database(game_result, self.position_evaluations)

    def get_agent_move(self, state):
        """Get move using learned knowledge."""
        fen = state.to_fen()

        # Check if we've seen this position
        if fen in self.position_evaluations:
            learned = self.position_evaluations[fen]
            if learned["result"] == "win" and learned["move_played"]:
                return learned["move_played"]
            elif learned["better_moves"]:
                return learned["better_moves"][0]

        # Fall back to regular play
        return super().get_agent_move(state)
```

## Performance Optimization

### Move Generation Caching

```python
from functools import lru_cache

class OptimizedChessStateManager(ChessStateManager):
    """Optimized state manager with caching."""

    @lru_cache(maxsize=10000)
    def get_legal_moves_cached(self, fen: str) -> List[str]:
        """Get legal moves with caching."""
        state = ChessState.from_fen(fen)
        return self.get_legal_moves(state)

    def get_legal_moves(self, state: ChessState) -> List[str]:
        """Wrapper that uses cache."""
        return self.get_legal_moves_cached(state.to_fen())
```

### Parallel Position Analysis

```python
import asyncio
from concurrent.futures import ThreadPoolExecutor

class ParallelChessAnalyzer:
    """Analyze multiple positions in parallel."""

    def __init__(self, num_workers=4):
        self.executor = ThreadPoolExecutor(max_workers=num_workers)

    async def analyze_positions(self, positions: List[ChessState]):
        """Analyze multiple positions concurrently."""
        tasks = []
        for position in positions:
            task = asyncio.create_task(
                self.analyze_single_position(position)
            )
            tasks.append(task)

        results = await asyncio.gather(*tasks)
        return dict(zip(positions, results))

    async def analyze_single_position(self, state: ChessState):
        """Analyze one position."""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            self.executor,
            self._analyze_position_sync,
            state
        )
```

## Testing Strategies

### Position Testing

```python
import pytest
from haive.games.chess import ChessState, ChessStateManager

class TestChessPositions:
    """Test specific chess positions."""

    @pytest.fixture
    def positions(self):
        """Famous chess positions for testing."""
        return {
            "fool_mate": "rnbqkbnr/pppp1ppp/8/4p3/6P1/5P2/PPPPP2P/RNBQKBNR b KQkq - 0 2",
            "scholar_mate": "r1bqkb1r/pppp1ppp/2n2n2/4p2Q/2B1P3/8/PPPP1PPP/RNB1K1NR w KQkq - 4 4",
            "back_rank": "6k1/5ppp/8/8/8/8/5PPP/R5K1 w - - 0 1"
        }

    def test_checkmate_detection(self, positions):
        """Test checkmate in specific positions."""
        manager = ChessStateManager()

        # Fool's mate position
        state = ChessState.from_fen(positions["fool_mate"])
        assert not manager.is_checkmate(state)  # Not mate yet

        # Play Qh4#
        state = manager.apply_move(state, "Qh4")
        assert manager.is_checkmate(state)  # Checkmate!
```

### Integration Testing

```python
from haive.games.chess import ChessAgent, ChessConfig
from haive.games.utils.test_helpers import create_test_engines

async def test_full_game_flow():
    """Test complete game flow."""
    # Create deterministic test engines
    engines = create_test_engines([
        ["e4", "Nf3", "Bc4", "O-O"],  # White moves
        ["e5", "Nc6", "Nf6", "O-O"]   # Black moves
    ])

    config = ChessConfig(
        white_engine=engines[0],
        black_engine=engines[1]
    )

    agent = ChessAgent(config)
    result = await agent.arun()

    # Verify game progression
    assert len(result.move_history) >= 8
    assert result.state_history[0].to_fen() == ChessState().to_fen()
    assert all(move in result.move_history for move in ["e4", "e5", "Nf3", "Nc6"])
```

## Common Patterns

### Pattern 1: Themed Tournaments

```python
from haive.games.chess import ChessConfig
from haive.games.tournament import Tournament

def create_themed_tournament(theme: str):
    """Create tournament with specific opening theme."""
    openings = {
        "sicilian": "1.e4 c5",
        "french": "1.e4 e6",
        "caro_kann": "1.e4 c6",
        "kings_indian": "1.d4 Nf6 2.c4 g6"
    }

    config = ChessConfig(
        starting_position=openings.get(theme, ""),
        theme_name=theme
    )

    return Tournament(
        game_config=config,
        num_players=8,
        format="swiss"
    )
```

### Pattern 2: Analysis Pipeline

```python
class ChessAnalysisPipeline:
    """Complete analysis pipeline for chess games."""

    def analyze_game(self, pgn_file: str):
        """Full game analysis pipeline."""
        # Load game
        game = self.load_pgn(pgn_file)

        # Phase 1: Opening analysis
        opening_report = self.analyze_opening(game)

        # Phase 2: Middle game analysis
        middlegame_report = self.analyze_middlegame(game)

        # Phase 3: Endgame analysis
        endgame_report = self.analyze_endgame(game)

        # Phase 4: Blunder detection
        blunders = self.find_blunders(game)

        # Phase 5: Alternative lines
        alternatives = self.generate_alternatives(game)

        return {
            "opening": opening_report,
            "middlegame": middlegame_report,
            "endgame": endgame_report,
            "blunders": blunders,
            "alternatives": alternatives
        }
```

## Best Practices

### 1. Position Representation

- Use FEN for serialization and storage
- Cache position evaluations
- Implement efficient board representations (bitboards)
- Handle special positions correctly

### 2. Move Validation

- Validate all moves before applying
- Check for pins and discovered checks
- Handle special moves explicitly
- Provide clear error messages

### 3. Engine Integration

- Use appropriate temperatures for different game phases
- Implement timeout handling
- Cache engine evaluations
- Handle engine failures gracefully

### 4. Game Analysis

- Store games in standard formats (PGN)
- Track critical positions
- Implement post-game analysis
- Generate insightful commentary

### 5. Performance

- Use move ordering for faster search
- Implement transposition tables
- Cache legal move generation
- Profile critical paths

## Troubleshooting

### Invalid Move Generation

**Problem**: Agent generates invalid moves.

**Solution**:

```python
config = ChessConfig(
    move_validation="strict",
    retry_invalid_moves=True,
    max_retries=3,
    provide_legal_moves=True  # Include legal moves in prompt
)
```

### Slow Move Generation

**Problem**: Moves take too long to generate.

**Solution**:

```python
# Reduce analysis depth
config.analysis_depth = 10  # Instead of 20

# Use caching
config.enable_position_cache = True

# Limit candidate moves
config.max_candidate_moves = 5
```

### Memory Issues

**Problem**: Game uses too much memory.

**Solution**:

```python
# Limit history
config.max_history_length = 50

# Clear caches periodically
if len(game.position_cache) > 10000:
    game.position_cache.clear()
```

## Examples

For comprehensive examples, see the [example.py](example.py) file which demonstrates:

- Basic game setup
- Advanced configurations
- Tournament play
- Position analysis
- Custom agents
- Integration patterns

## API Reference

### Core Classes

| Class               | Description                        |
| ------------------- | ---------------------------------- |
| `ChessAgent`        | Main agent orchestrating gameplay  |
| `ChessState`        | Complete game state representation |
| `ChessStateManager` | Game logic and rules engine        |
| `ChessConfig`       | Configuration parameters           |
| `ChessMove`         | Move representation and parsing    |
| `ChessVisualizer`   | Board and game visualization       |

### Key Methods

| Method                      | Description             |
| --------------------------- | ----------------------- |
| `state.to_fen()`            | Convert to FEN notation |
| `state.is_legal_move()`     | Check move legality     |
| `manager.apply_move()`      | Apply move to state     |
| `manager.get_legal_moves()` | Get all legal moves     |
| `agent.run()`               | Run complete game       |

For detailed API documentation, see the [API Reference](../../../../../docs/source/api/haive/games/chess/index.rst).

## Related Modules

- [Game Framework](../framework/README.md) - Core framework components
- [Board Games](../board/README.md) - Shared board game utilities
- [Chess Engines](engines.py) - Engine implementations
- [Chess Models](models.py) - Data models and types



.. raw:: html

    <div class="sphx-glr-thumbnails">

.. thumbnail-parent-div-open

.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="This script prints the validation models and field requirements for better debugging of validation errors.">

.. only:: html

  .. image:: /auto_examples/images/thumb/sphx_glr_debug_schema_thumb.png
    :alt:

  :ref:`sphx_glr_auto_examples_debug_schema.py`

.. raw:: html

      <div class="sphx-glr-thumbnail-title">Debug script for chess game validation models.</div>
    </div>


.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="This module provides an example of how to run a complete chess game using the Haive chess module, demonstrating:     - Agent configuration     - State initialization     - Game streaming     - Event monitoring">

.. only:: html

  .. image:: /auto_examples/images/thumb/sphx_glr_example_thumb.png
    :alt:

  :ref:`sphx_glr_auto_examples_example.py`

.. raw:: html

      <div class="sphx-glr-thumbnail-title">Example chess game runner.</div>
    </div>


.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="This module provides state management functionality for chess games, including:     - Game state initialization     - Move application and validation     - Game status tracking     - Captured pieces management">

.. only:: html

  .. image:: /auto_examples/images/thumb/sphx_glr_state_manager_thumb.png
    :alt:

  :ref:`sphx_glr_auto_examples_state_manager.py`

.. raw:: html

      <div class="sphx-glr-thumbnail-title">Chess game state manager module.</div>
    </div>


.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="This module provides helper functions for the chess game, including:     - Game status determination     - Board visualization     - Move validation">

.. only:: html

  .. image:: /auto_examples/images/thumb/sphx_glr_utils_thumb.png
    :alt:

  :ref:`sphx_glr_auto_examples_utils.py`

.. raw:: html

      <div class="sphx-glr-thumbnail-title">Chess game utility functions.</div>
    </div>


.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="This shows how to interact with the chess API to create and play games.">

.. only:: html

  .. image:: /auto_examples/images/thumb/sphx_glr_api_client_example_thumb.png
    :alt:

  :ref:`sphx_glr_auto_examples_api_client_example.py`

.. raw:: html

      <div class="sphx-glr-thumbnail-title">Example client for the Chess API.</div>
    </div>


.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="This module defines the state schema for chess games, including:     - Board state representation using FEN notation     - Move history tracking     - Game status management     - Position analysis storage     - Player turn tracking">

.. only:: html

  .. image:: /auto_examples/images/thumb/sphx_glr_state_thumb.png
    :alt:

  :ref:`sphx_glr_auto_examples_state.py`

.. raw:: html

      <div class="sphx-glr-thumbnail-title">Chess game state models.</div>
    </div>


.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="This module provides data models for the chess game, including:     - Move representation     - Player decisions     - Position analysis     - Structured output models for LLMs">

.. only:: html

  .. image:: /auto_examples/images/thumb/sphx_glr_models_thumb.png
    :alt:

  :ref:`sphx_glr_auto_examples_models.py`

.. raw:: html

      <div class="sphx-glr-thumbnail-title">Chess game models module.</div>
    </div>


.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="This example demonstrates how to run chess games with different LLM providers and models, showing the flexibility of the new configuration system.">

.. only:: html

  .. image:: /auto_examples/images/thumb/sphx_glr_example_configurable_thumb.png
    :alt:

  :ref:`sphx_glr_auto_examples_example_configurable.py`

.. raw:: html

      <div class="sphx-glr-thumbnail-title">Example of running chess with configurable LLMs.</div>
    </div>


.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="This example demonstrates how to create chess games with different LLM configurations for players without hardcoding them.">

.. only:: html

  .. image:: /auto_examples/images/thumb/sphx_glr_example_configurable_players_thumb.png
    :alt:

  :ref:`sphx_glr_auto_examples_example_configurable_players.py`

.. raw:: html

      <div class="sphx-glr-thumbnail-title">Example of using configurable chess players.</div>
    </div>


.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="This module provides augmented LLM configurations for the chess game, including:     - Move generation prompts for white and black players     - Position analysis prompts for both sides     - Structured output models for moves and analysis     - Pre-configured LLM configurations for easy agent setup">

.. only:: html

  .. image:: /auto_examples/images/thumb/sphx_glr_aug_llms_thumb.png
    :alt:

  :ref:`sphx_glr_auto_examples_aug_llms.py`

.. raw:: html

      <div class="sphx-glr-thumbnail-title">Chess game augmented LLM configurations module.</div>
    </div>


.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="This module provides chess-specific utilities for creating and configuring LLMs for chess gameplay, building on the core LLM factory system.">

.. only:: html

  .. image:: /auto_examples/images/thumb/sphx_glr_llm_utils_thumb.png
    :alt:

  :ref:`sphx_glr_auto_examples_llm_utils.py`

.. raw:: html

      <div class="sphx-glr-thumbnail-title">Chess-specific LLM utilities using the game LLM factory.</div>
    </div>


.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="from typing import Any This module provides configuration classes for chess agents, including:     - Core game parameters     - LLM engine settings     - Analysis options     - Visualization settings     - State schema definition">

.. only:: html

  .. image:: /auto_examples/images/thumb/sphx_glr_config_thumb.png
    :alt:

  :ref:`sphx_glr_auto_examples_config.py`

.. raw:: html

      <div class="sphx-glr-thumbnail-title">Chess agent configuration module.</div>
    </div>


.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="This module demonstrates how to create API endpoints for chess games with configurable LLM providers and models.">

.. only:: html

  .. image:: /auto_examples/images/thumb/sphx_glr_api_example_thumb.png
    :alt:

  :ref:`sphx_glr_auto_examples_api_example.py`

.. raw:: html

      <div class="sphx-glr-thumbnail-title">FastAPI example for chess game with configurable LLMs.</div>
    </div>


.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="This module provides chess engine configurations that use configurable player agents instead of hardcoded LLM configurations, making it easy to switch LLMs for different players.">

.. only:: html

  .. image:: /auto_examples/images/thumb/sphx_glr_configurable_engines_thumb.png
    :alt:

  :ref:`sphx_glr_auto_examples_configurable_engines.py`

.. raw:: html

      <div class="sphx-glr-thumbnail-title">Configurable chess engines using the new player agent system.</div>
    </div>


.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="This module provides LLM engine configurations for chess game agents, including:     - Player engines for white and black     - Analyzer engines for position evaluation     - Prompt templates with chess-specific instructions     - Structured output models for moves and analysis">

.. only:: html

  .. image:: /auto_examples/images/thumb/sphx_glr_engines_thumb.png
    :alt:

  :ref:`sphx_glr_auto_examples_engines.py`

.. raw:: html

      <div class="sphx-glr-thumbnail-title">Chess game engines using AugLLMConfig.</div>
    </div>


.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="This module provides a flexible configuration system for chess that supports: - Legacy hardcoded engines (backward compatibility) - Simple model string configuration - Example-based configuration - Advanced PlayerAgentConfig configuration">

.. only:: html

  .. image:: /auto_examples/images/thumb/sphx_glr_dynamic_config_thumb.png
    :alt:

  :ref:`sphx_glr_auto_examples_dynamic_config.py`

.. raw:: html

      <div class="sphx-glr-thumbnail-title">Dynamic configuration for chess game.</div>
    </div>


.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="This module provides a chess configuration that supports configurable player agents instead of hardcoded engine configurations.">

.. only:: html

  .. image:: /auto_examples/images/thumb/sphx_glr_configurable_config_thumb.png
    :alt:

  :ref:`sphx_glr_auto_examples_configurable_config.py`

.. raw:: html

      <div class="sphx-glr-thumbnail-title">Configurable chess agent configuration using player agents.</div>
    </div>


.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="This module demonstrates how to use the generic player agent system for chess, providing a clean, type-safe implementation that eliminates hardcoded LLM configurations.">

.. only:: html

  .. image:: /auto_examples/images/thumb/sphx_glr_generic_engines_thumb.png
    :alt:

  :ref:`sphx_glr_auto_examples_generic_engines.py`

.. raw:: html

      <div class="sphx-glr-thumbnail-title">Generic chess engines using the new generic player agent system.</div>
    </div>


.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="Chess game UI using Rich for beautiful terminal display.">

.. only:: html

  .. image:: /auto_examples/images/thumb/sphx_glr_ui_thumb.png
    :alt:

  :ref:`sphx_glr_auto_examples_ui.py`

.. raw:: html

      <div class="sphx-glr-thumbnail-title">Chess game UI using Rich for beautiful terminal display.</div>
    </div>


.. raw:: html

    <div class="sphx-glr-thumbcontainer" tooltip="This module provides a chess agent implementation using LangGraph, featuring:     - LLM-powered chess players     - Position analysis     - Game state management     - Workflow graph for turn-based gameplay     - Error handling and retry logic">

.. only:: html

  .. image:: /auto_examples/images/thumb/sphx_glr_agent_thumb.png
    :alt:

  :ref:`sphx_glr_auto_examples_agent.py`

.. raw:: html

      <div class="sphx-glr-thumbnail-title">Chess agent implementation using LangGraph.</div>
    </div>


.. thumbnail-parent-div-close

.. raw:: html

    </div>


.. toctree::
   :hidden:

   /auto_examples/debug_schema
   /auto_examples/example
   /auto_examples/state_manager
   /auto_examples/utils
   /auto_examples/api_client_example
   /auto_examples/state
   /auto_examples/models
   /auto_examples/example_configurable
   /auto_examples/example_configurable_players
   /auto_examples/aug_llms
   /auto_examples/llm_utils
   /auto_examples/config
   /auto_examples/api_example
   /auto_examples/configurable_engines
   /auto_examples/engines
   /auto_examples/dynamic_config
   /auto_examples/configurable_config
   /auto_examples/generic_engines
   /auto_examples/ui
   /auto_examples/agent


.. only:: html

  .. container:: sphx-glr-footer sphx-glr-footer-gallery

    .. container:: sphx-glr-download sphx-glr-download-python

      :download:`Download all examples in Python source code: auto_examples_python.zip </auto_examples/auto_examples_python.zip>`

    .. container:: sphx-glr-download sphx-glr-download-jupyter

      :download:`Download all examples in Jupyter notebooks: auto_examples_jupyter.zip </auto_examples/auto_examples_jupyter.zip>`


.. only:: html

 .. rst-class:: sphx-glr-signature

    `Gallery generated by Sphinx-Gallery <https://sphinx-gallery.github.io>`_
