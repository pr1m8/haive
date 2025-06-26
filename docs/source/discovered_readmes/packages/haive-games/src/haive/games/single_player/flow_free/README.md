# Flow Free Game Module

This module provides a complete implementation of the Flow Free puzzle game for use with the Haive framework. Flow Free is a puzzle game where the player connects pairs of colored dots with pipes, filling the entire board without any overlapping paths.

## Features

- Complete implementation of Flow Free game mechanics
- Customizable board sizes (5x5, 6x6, 7x7)
- Multiple difficulty levels
- Support for LLM-powered gameplay and analysis
- Interactive and auto-play modes
- Rich visualization for terminal display
- Hint system with intelligent suggestions

## Components

### Core Models

- `FlowFreeMove` - Represents a move in the game (extending a flow to a specific position)
- `FlowFreeAnalysis` - Strategic analysis of the board position, including critical paths and recommendations
- `Position` - Represents a position on the board
- `FlowColor` - Enum of available colors for flows
- `PipeDirection` - Direction of pipe segments (up, down, left, right)

### Game State

- `FlowFreeState` - Tracks the complete game state including board, flows, and game progress
- `FlowFreeStateManager` - Manages game mechanics, move validation, and state transitions

### Agent and Configuration

- `FlowFreeAgent` - LLM-based agent for playing Flow Free with strategic reasoning
- `FlowFreeConfig` - Configuration for customizing game parameters and agent behavior
- `flow_free_engines` - Engine configurations for move generation and position analysis

## Usage Example

```python
from haive.games.single_player.flow_free.agent import FlowFreeAgent
from haive.games.single_player.flow_free.config import FlowFreeConfig
from haive.games.single_player.base import GameDifficulty, GameMode, PlayerType

# Create a configuration for an easy 5x5 puzzle
config = FlowFreeConfig(
    difficulty=GameDifficulty.EASY,
    rows=5,
    cols=5,
    player_type=PlayerType.LLM,
    game_mode=GameMode.AUTO
)

# Create and run the agent
agent = FlowFreeAgent(config)
final_state = agent.run_game()

# Check if the puzzle was solved
if final_state.get("game_status") == "victory":
    print("Puzzle solved!")
else:
    print("Puzzle not solved")
```

## Game Rules

Flow Free is played on a grid with the following rules:

1. Connect pairs of same-colored dots with pipes
2. Pipes cannot cross or overlap with other pipes
3. Every cell on the grid must be filled with a pipe
4. Pipes can make 90-degree turns but not diagonal connections

The puzzle is solved when all pairs are connected and all grid cells are filled.

## Interactive Commands

When running in interactive mode, the following commands are available:

- `flow <color>` - Select a flow by color
- `move <row> <col>` - Place a pipe segment at the specified position
- `board` - Display the current board state
- `flows` - List all flows and their status
- `hint` - Get a hint for the next move
- `restart` - Restart the current puzzle
- `quit` - Quit the game

## Running the Example

The module includes an example script that can be run with various options:

```
python example.py --difficulty easy --mode auto --size 5x5
```

Available options:

- `--difficulty`: easy, medium, hard, expert
- `--mode`: auto, interactive, assist
- `--size`: 5x5, 6x6, 7x7
- `--flows`: Number of flows to include
- `--no-visualize`: Disable visualization

## Integration with Haive Framework

This module is designed to work seamlessly with the Haive single-player game framework, providing:

- Standardized state representation
- Engine configurations for agent deployment
- Strategic analysis capabilities
- Full compatibility with LLM-based reasoning
