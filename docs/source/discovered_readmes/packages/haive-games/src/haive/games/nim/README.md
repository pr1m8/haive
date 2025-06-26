# Nim Game

A Nim game implementation using the Haive framework with Rich UI support.

## Overview

Nim is a mathematical strategy game where players take turns removing objects from distinct piles. On each turn, a player must remove at least one object, and may remove any number of objects provided they all come from the same pile. The player who takes the last object wins in standard mode, or loses in misère mode.

## Features

- Standard and misère mode gameplay
- Rich terminal UI for visualization
- LLM-based AI players for gameplay
- Position analysis with nim-sum calculation
- Customizable pile sizes and game configuration
- Robust error handling and state management

## Components

### Models

- `NimMove`: Represents a move in the game (pile index and stones taken)
- `NimAnalysis`: Analysis of a Nim position with strategy recommendation
- `NimState`: Complete game state representation

### State Management

The `NimStateManager` class handles:

- Game initialization with custom pile sizes
- Legal move generation
- Move application and validation
- Game status checking
- Analysis tracking

### Agent

The `NimAgent` class:

- Controls game flow using LangGraph
- Manages player turns
- Generates moves using LLMs
- Performs position analysis
- Handles visualization

### Rich UI

The `NimUI` class provides:

- Visual representation of piles
- Game status display
- Move history tracking
- Analysis visualization
- User interaction for moves

## Usage

### Basic Usage

```python
from haive.games.nim.agent import NimAgent
from haive.games.nim.config import NimConfig

# Create agent with default config
agent = NimAgent()

# Run game with visualization
agent.run_game(visualize=True)

# Run game with Rich UI
agent.run_game_with_ui(show_analysis=True)
```

### Custom Configuration

```python
from haive.games.nim.agent import NimAgent
from haive.games.nim.config import NimConfig

# Custom configuration
config = NimConfig(
    pile_sizes=[4, 6, 8],    # Custom pile sizes
    misere_mode=True,        # Last player to take stone loses
    enable_analysis=True,    # Enable position analysis
    visualize=True           # Enable visualization
)

# Create agent with custom config
agent = NimAgent(config=config)

# Run game
agent.run_game_with_ui()
```

## Implementation Details

### Nim-Sum Strategy

The implementation includes the nim-sum calculation, which is the XOR of all pile sizes. This is a key strategic element in Nim:

- In standard Nim, a position is winning if and only if the nim-sum is non-zero
- In misère Nim, the same applies except when the position has only piles of size 1

### State Handling

The game uses Pydantic models for state validation and robust error handling. The `ensure_game_state` helper function ensures proper state conversion regardless of input type.

### Error Handling

The implementation includes robust error handling:

- Move validation to prevent illegal moves
- Fallbacks for unexpected inputs
- Graceful handling of missing dependencies

## Testing

A standalone test script is provided to verify the functionality of the core components without requiring the full Haive framework:

```bash
python standalone_test.py
```

## Dependencies

- Core Haive framework
- LangGraph for workflow management
- Rich (optional) for terminal UI
- Pydantic for data validation

## License

Same as the Haive framework license.
