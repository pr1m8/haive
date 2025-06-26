# Reversi (Othello) Game Module

The Reversi module provides a comprehensive implementation of the classic Reversi/Othello board game for use with the Haive framework. This module enables agents to play Reversi using LLM-based strategic reasoning, with support for game state management, move validation, and position analysis.

## Features

- Complete implementation of standard Reversi/Othello rules
- Support for LLM-based strategic agents
- Detailed position analysis with multiple evaluation metrics
- Customizable game configuration
- Turn skipping when no legal moves are available
- Game visualization via console output
- Structured state management and move validation

## Components

### Core Models

- `Position` - Represents a position on the 8x8 Reversi board
- `ReversiMove` - Represents a single move in the game (placing a disc at a specific position)
- `ReversiAnalysis` - Comprehensive analysis of a game position including mobility, corner control, stability, and strategic recommendations

### Game State

- `ReversiState` - Tracks the complete game state including board layout, turn tracking, move history, and analysis storage
- `ReversiStateManager` - Manages game mechanics, rules enforcement, legal move determination, and disc flipping

### Agents and Configuration

- `ReversiAgent` - LLM-based agent for playing Reversi with strategic reasoning
- `ReversiConfig` - Configuration for customizing game parameters and player settings
- `reversi_engines` - Engine configurations for move generation and position analysis

## Usage Example

```python
from haive.games.reversi.agent import ReversiAgent
from haive.games.reversi.config import ReversiConfig

# Create a default Reversi agent
agent = ReversiAgent()

# Run a complete game with visualization
final_state = agent.run_game(visualize=True)

# Check the game outcome
if final_state.get("game_status", "") == "draw":
    print("Game ended in a draw!")
elif final_state.get("game_status", "").endswith("_win"):
    winner_symbol = final_state["game_status"].split("_")[0]
    winner_color = "Black" if winner_symbol == "B" else "White"
    print(f"Winner: {winner_color}")
```

## Game Rules

Reversi (also known as Othello) is played on an 8x8 board with the following rules:

1. Players take turns placing discs on the board with their assigned color facing up
2. A valid move must capture at least one opponent's disc by flanking it between the newly placed disc and an existing disc of the player's color
3. All captured discs are flipped to the player's color
4. If a player cannot make a valid move, they must pass their turn
5. The game ends when neither player can make a valid move or the board is full
6. The player with the most discs of their color wins

## Strategic Concepts

The module includes support for analyzing positions based on key Reversi strategic concepts:

- **Mobility**: The number of legal moves available to a player
- **Corner Control**: Corners are strategically valuable as they can never be flipped
- **Edge Control**: Edge discs are harder to flip than center discs
- **Stability**: Stable discs are those that cannot be flipped for the remainder of the game
- **Parity**: Having the last move in a region is advantageous
- **Frontier Discs**: Discs adjacent to empty spaces are vulnerable

## Customization

The Reversi game can be customized through the `ReversiConfig` class, which allows you to adjust:

- Which player goes first (Black or White)
- Player assignments (which player controls which color)
- Whether to enable position analysis
- Visualization preferences
- LLM engine configurations for move generation and analysis

## Integration with Haive Framework

This module is designed to work seamlessly with the Haive agent framework, providing:

- Standardized state representation
- Engine configurations for agent deployment
- Strategic analysis capabilities
- Full compatibility with LLM-based reasoning
