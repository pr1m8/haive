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

## Best Practices

- **Position Representation**: Use standard FEN notation for position serialization
- **Move Validation**: Implement thorough validation for all chess rules
- **Special Moves**: Handle all special chess moves correctly (castling, en passant, promotion)
- **Analysis Depth**: Balance analysis depth with performance considerations
- **Opening Knowledge**: Use opening books for early game moves
- **Evaluation Consistency**: Ensure consistent position evaluation methodology
- **Game Visualization**: Provide clear visual representations of the board state

## API Reference

For full API details, see the [documentation](https://docs.haive.ai/games/chess).

## Related Modules

- **haive.games.framework**: Core framework used by the chess implementation
- **haive.games.board**: Board game utilities shared across board games
- **haive.core.engine**: Engine components used by chess agents
