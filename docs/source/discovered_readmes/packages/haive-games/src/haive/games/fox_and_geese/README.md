# Fox and Geese Game

A complete implementation of the classic Fox and Geese board game with rich terminal UI visualization.

## Game Overview

Fox and Geese is a traditional hunt game played on a cross-shaped board where:

- The Fox (🦊) tries to capture enough geese to win
- The Geese (🪿) try to trap the fox so it cannot move
- The fox wins by reducing geese to fewer than 4
- The geese win by trapping the fox with no legal moves

The game is played on a 7x7 board where pieces move along the lines. The fox can move in any direction (diagonal, horizontal, vertical), while geese can only move forward or sideways (not backward). The fox can capture geese by jumping over them into an empty space, similar to checkers.

## Features

- Full game logic for Fox and Geese with standard rules
- Two UI options:
  - Basic UI with clean display of game state
  - Enhanced Rich UI with improved styling and animations
- Support for AI-powered game agents
- Interactive gameplay with move validation
- Automatic detection of legal moves and captures
- End-game detection and winner determination
- Game state analysis capabilities
- Fixed implementation that handles state transitions reliably

## Running the Game

### Fixed Runner (Works with or without API Keys)

Run the game with our fixed state handling that avoids LangGraph streaming issues:

```bash
# Run with default settings
python src/haive/games/fox_and_geese/fixed_runner.py

# Enable debug logging
python src/haive/games/fox_and_geese/fixed_runner.py --debug

# Disable position analysis
python src/haive/games/fox_and_geese/fixed_runner.py --no-analysis

# Adjust speed of moves
python src/haive/games/fox_and_geese/fixed_runner.py --delay 0.5
```

### Standard Runner (Requires LLM API Access)

Run the original game implementation with LangGraph streaming:

```bash
# Run with default settings
python src/haive/games/fox_and_geese/example.py
```

## Components

### Models

- `FoxAndGeesePosition`: Represents a position on the board with row and column coordinates
- `FoxAndGeeseMove`: Represents a move in the game (from position, to position, piece type, and optional capture)
- `FoxAndGeeseAnalysis`: Analysis of a player's position with advantage, key features, and recommended strategies

### State Management

- `FoxAndGeeseState`: Immutable game state representation with fox position, geese positions, and game status
- `FoxAndGeeseStateManager`: Handles game state transitions, move validation, and win conditions

### User Interface

- `FoxAndGeeseUI`: Basic UI for game visualization
- `FoxAndGeeseRichUI`: Enhanced UI with improved styling, animations, and more detailed information

### Game Control

- `FoxAndGeeseAgent`: Manages game flow and player interactions using LLM-based agents
- `FixedFoxAndGeeseAgent`: Improved agent implementation that handles state transitions reliably

## Usage

### Running the Example Game

```python
from haive.games.fox_and_geese.fixed_runner import FixedFoxAndGeeseAgent
from haive.games.fox_and_geese.config import FoxAndGeeseConfig

# Create agent config
config = FoxAndGeeseConfig(
    name="fox_and_geese_fixed",
    enable_analysis=True
)

# Create fixed agent
agent = FixedFoxAndGeeseAgent(config)

# Run the game
final_state = agent.run_fixed_game(delay=1.0)
```

### Enhanced Example with UI Options

The enhanced example script (`enhanced_example.py`) provides options for testing different UI modes:

```bash
# Run with enhanced Rich UI (default)
python enhanced_example.py

# Run with basic UI
python enhanced_example.py --basic-ui

# Run a UI feature demonstration
python enhanced_example.py --demo

# Adjust animation speed
python enhanced_example.py --delay 0.8
```

### Creating Custom Game States

```python
from haive.games.fox_and_geese.state import FoxAndGeeseState
from haive.games.fox_and_geese.models import FoxAndGeesePosition

# Initialize a new game
game_state = FoxAndGeeseState.initialize()

# Access game properties
fox_position = game_state.fox_position
geese_positions = game_state.geese_positions
current_player = game_state.turn
```

### Customizing the UI

The Rich UI can be customized by extending the `FoxAndGeeseRichUI` class and overriding specific methods:

```python
from haive.games.fox_and_geese.rich_ui import FoxAndGeeseRichUI
from rich.text import Text

class CustomFoxAndGeeseUI(FoxAndGeeseRichUI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Customize colors
        self.colors["fox"] = "bright_green"
        self.colors["geese"] = "bright_purple"

    def create_board_table(self, game_state, highlight_positions=None, capture_position=None):
        # Create custom board visualization
        # ...

    def show_thinking(self, player, message="Custom thinking..."):
        # Custom thinking animation
        # ...
```

## Example Game Output

The enhanced UI displays the game with rich formatting:

```
🦊 FOX AND GEESE GAME 🪿
┌──────────────────────────────────────────────────────────────────────────┐
│                             Game Board                                    │
│                                                                          │
│   0 1 2 3 4 5 6                                                          │
│  0 🪿 ⬛ 🪿 ⬛ 🪿 ⬛ 🪿                                                      │
│  1 ⬛ 🪿 ⬛ 🪿 ⬛ 🪿 ⬛                                                      │
│  2 ⬜ ⬛ ⬜ ⬛ ⬜ ⬛ ⬜                                                      │
│  3 ⬛ ⬜ ⬛ 🦊 ⬛ ⬜ ⬛                                                      │
│  4 ⬜ ⬛ ⬜ ⬛ ⬜ ⬛ ⬜                                                      │
│  5 ⬛ ⬜ ⬛ ⬜ ⬛ ⬜ ⬛                                                      │
│  6 ⬜ ⬛ ⬜ ⬛ ⬜ ⬛ ⬜                                                      │
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘
┌────────── Move History ───────────┐┌────── Game Information ───────┐
│                                   ││                               │
│  #   Piece    From    To   Capture││ Current Turn  🦊 Fox's Turn    │
│  1   🦊 Fox   (3,3)  (2,2)   No   ││ Game Status   Game in Progress│
│  2   🪿 Goose  (1,1)  (2,0)   No   ││ Fox Position  (2,2)           │
│  3   🦊 Fox   (2,2)  (1,1)   No   ││ Geese Remaining 8 / 8         │
│  4   🪿 Goose  (0,0)  (1,1)   No   ││ Geese Health   ████████ 100.0%│
│  5   🦊 Fox   (1,1)  (0,2)   No   ││ Move Count     5              │
│                                   ││                               │
│                                   ││                               │
│                                   ││ Victory Conditions            │
│                                   ││ Fox Wins       When fewer than│
│                                   ││                4 geese remain │
│                                   ││ Geese Win      When fox has no│
│                                   ││                legal moves    │
└───────────────────────────────────┘└───────────────────────────────┘
┌───────── Legal Moves for Fox ─────────┐┌──────── Game Analysis ────────┐
│                                       ││                               │
│  #   From    To   Capture             ││  No analysis available yet    │
│  1   (0,2)  (1,3)   No                ││                               │
│  2   (0,2)  (2,4)   No                ││                               │
│  3   (0,2)  (2,0)   No                ││                               │
│                                       ││                               │
│                                       ││                               │
│                                       ││                               │
└───────────────────────────────────────┘└───────────────────────────────┘
```

## Game Rules in Detail

### Initial Setup

- The fox starts at the center of the board (position 3,3)
- The geese start at the top of the board (8 geese total)
- The fox moves first

### Movement

- The fox can move in any direction along the lines (diagonal, horizontal, vertical)
- The geese can only move forward or sideways (never backward)
- All pieces move one space at a time
- The fox can capture geese by jumping over them into an empty space

### Win Conditions

- The fox wins by reducing the number of geese to fewer than 4
- The geese win by trapping the fox so it has no legal moves

## Integration with LLM Agents

The Fox and Geese game is designed to work seamlessly with LLM-powered agents. The state representation includes fields for analysis and strategic thinking, making it ideal for AI research and experimentation.

## Contributing

Contributions to improve the Fox and Geese game implementation are welcome. Some areas for potential enhancement:

- Additional rule variations (e.g., different board sizes, alternate starting positions)
- Network multiplayer support
- Improved AI strategies
- Enhanced visualizations and animations
- Performance optimizations
