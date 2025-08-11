# Reversi Agent Examples

Real examples and outputs from the reversi agent.

## reversi_README

**Source**: `packages/haive-games/src/haive/games/reversi/README.md`

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
    win

... (truncated)


---

```
