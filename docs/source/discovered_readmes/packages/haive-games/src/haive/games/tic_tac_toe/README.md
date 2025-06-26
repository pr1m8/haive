# Tic Tac Toe Game Module

The Tic Tac Toe module provides a comprehensive implementation of the classic Tic Tac Toe game for use with the Haive framework. This module enables agents to play Tic Tac Toe using LLM-based strategic reasoning, with support for game state management, move validation, analysis, and an interactive rich UI.

## Features

- Complete implementation of Tic Tac Toe rules
- Support for LLM-based strategic agents
- Detailed position analysis including win detection, blocking moves, and fork opportunities
- Customizable game configuration
- Interactive Rich UI for beautiful terminal-based visualization
- Structured state management with proper concurrency handling
- Comprehensive move validation

## Components

### Core Models

- `TicTacToeMove` - Represents a single move in the game (placing a symbol at a specific position)
- `TicTacToeAnalysis` - Strategic analysis of a board position, including winning moves, blocking moves, fork opportunities, and strategic recommendations

### Game State

- `TicTacToeState` - Tracks the complete game state including board layout, turn tracking, move history, and analysis storage
- `TicTacToeStateManager` - Manages game mechanics, rules enforcement, and win detection

### Agents and Configuration

- `TicTacToeAgent` - LLM-based agent for playing Tic Tac Toe with strategic reasoning
- `TicTacToeConfig` - Configuration for customizing game parameters and player settings
- `tictactoe_engines` - Engine configurations for move generation and position analysis

### User Interface

- `RichTicTacToeRunner` - Beautiful terminal-based UI for Tic Tac Toe games using the Rich library

## Usage Example

```python
from haive.games.tic_tac_toe.agent import TicTacToeAgent
from haive.games.tic_tac_toe.config import TicTacToeConfig

# Create a default Tic Tac Toe agent
agent = TicTacToeAgent()

# Run a complete game with visualization
final_state = agent.run_game(visualize=True)

# Check the game outcome
if final_state.get("game_status", "") == "draw":
    print("Game ended in a draw!")
elif final_state.get("game_status", "").endswith("_win"):
    winner_symbol = final_state["game_status"].split("_")[0]
    winner_player = (
        final_state["player_X"] if winner_symbol == "X" else final_state["player_O"]
    )
    print(f"Winner: {winner_symbol} ({winner_player})")
```

## Rich UI Example

The module includes a beautiful interactive UI using the Rich library:

```python
from haive.games.tic_tac_toe.agent import TicTacToeAgent
from haive.games.tic_tac_toe.config import TicTacToeConfig
from haive.games.tic_tac_toe.ui import RichTicTacToeRunner

# Create configuration
config = TicTacToeConfig(
    enable_analysis=True,
    visualize=False,  # Disable built-in visualization since we're using Rich
    first_player="X",
    player_X="player1",
    player_O="player2",
)

# Create agent
agent = TicTacToeAgent(config)

# Create Rich UI runner
ui_runner = RichTicTacToeRunner(agent)

# Run the game with Rich UI
final_state = ui_runner.run_game(
    show_thinking=True,  # Show AI thinking animations
    step_delay=1.5,  # 1.5 second delay between moves
)

# Show game summary
ui_runner.show_game_summary(final_state)
```

## Game Rules

Tic Tac Toe is played on a 3x3 grid with the following rules:

1. Players take turns placing their symbol (X or O) on the board
2. The first player to get three of their symbols in a row (horizontally, vertically, or diagonally) wins
3. If the board fills up with neither player getting three in a row, the game is a draw

## Strategic Concepts

The module includes support for analyzing positions based on key Tic Tac Toe strategic concepts:

- **Winning Moves**: Completing a line of three symbols
- **Blocking Moves**: Preventing the opponent from completing a line
- **Fork Opportunities**: Creating two winning threats simultaneously
- **Center Control**: The center position (1,1) is strategically valuable
- **Corner Play**: Corner positions are more valuable than edge positions

## Customization

The Tic Tac Toe game can be customized through the `TicTacToeConfig` class, which allows you to adjust:

- Which player goes first (X or O)
- Player assignments (which player controls which symbol)
- Whether to enable position analysis
- Visualization preferences
- LLM engine configurations for move generation and analysis

## Integration with Haive Framework

This module is designed to work seamlessly with the Haive agent framework, providing:

- Standardized state representation
- Engine configurations for agent deployment
- Strategic analysis capabilities
- Full compatibility with LLM-based reasoning
- Langgraph-based workflow management
