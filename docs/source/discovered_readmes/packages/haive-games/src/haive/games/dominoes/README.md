# Dominoes Game

A complete implementation of the classic Dominoes game with rich terminal UI visualization.

## Features

- Full game logic for Dominoes with standard rules
- Two UI options:
  - Basic UI with clean display of game state
  - Enhanced Rich UI with improved styling and animations
- Support for AI-powered game agents
- Interactive gameplay with move validation
- Automatic calculation of legal moves and scoring
- End-game detection and winner determination
- Game state analysis capabilities

## Game Rules

- Players take turns placing matching dominoes
- The first player to use all their tiles wins
- If the game is locked (no player can make a move), the player with the lowest pip count wins
- Strategic tile placement is key to victory

## Components

### Models

- `DominoTile`: Represents a domino tile with left and right values
- `DominoMove`: Represents a move in the game (tile and location)
- `DominoesPlayerDecision`: Player's decision in a turn (move or pass)
- `DominoesAnalysis`: Analysis of a player's position

### State Management

- `DominoesState`: Immutable game state representation
- `DominoesStateManager`: Handles game state transitions and validation

### User Interface

- `DominoesUI`: Basic UI for game visualization
- `DominoesRichUI`: Enhanced UI with improved styling and animations

### Game Control

- `DominoesAgent`: Manages game flow and player interactions

## Usage

### Running the Example Game

```python
from haive.games.dominoes.agent import DominoesAgent
from haive.games.dominoes.config import DominoesAgentConfig
from haive.games.dominoes.rich_ui import DominoesRichUI

# Create agent config
config = DominoesAgentConfig(name="dominoes_game")

# Create agent
agent = DominoesAgent(config)

# Create UI
ui = DominoesRichUI()

# Run the game
ui.run_game_with_ui(agent, delay=1.2)
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
from haive.games.dominoes.state import DominoesState
from haive.games.dominoes.models import DominoTile

# Initialize a new random game
game_state = DominoesState.initialize()

# Access game properties
player_hands = game_state.hands
current_board = game_state.board
current_player = game_state.turn

# Access open ends of the board
left_value = game_state.left_value
right_value = game_state.right_value
```

### Customizing the UI

The Rich UI can be customized by extending the `DominoesRichUI` class and overriding specific methods:

```python
from haive.games.dominoes.rich_ui import DominoesRichUI
from rich.text import Text

class CustomDominoesUI(DominoesRichUI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Customize colors
        self.colors["player1"] = "bright_green"
        self.colors["player2"] = "bright_purple"

    def create_domino_tile_art(self, tile, open_end=False):
        # Override to create custom tile representation
        # Example: Add emoji indicators for doubles
        if tile.is_double():
            tile_style = self.colors["double_tile"]
            domino_art = [
                "┌───┬───┐",
                f"│ {tile.left} │ {tile.right} │ 🔥",
                "└───┴───┘"
            ]
        else:
            tile_style = self.colors["tile"]
            domino_art = [
                "┌───┬───┐",
                f"│ {tile.left} │ {tile.right} │",
                "└───┴───┘"
            ]

        return Text("\n".join(domino_art), style=tile_style)
```

## Example Game Output

```
🎲 DOMINOES GAME 🎲
┌───────────────────────────────────────────────────────────────────────────┐
│                                Game Board                                  │
│                                                                           │
│              ┌───┬───┐    →    ┌───┬───┐    →    ┌───┬───┐                │
│              │ 6 │ 6 │         │ 6 │ 4 │         │ 4 │ 2 │                │
│              └───┴───┘         └───┴───┘         └───┴───┘                │
│                                                                           │
└───────────────────────────────────────────────────────────────────────────┘
┌───────────────────────────────────┐ ┌───────────────────────────────────┐
│        player1's Hand (Current Turn) │        player2's Hand              │
│                                   │ │                                   │
│    ┌───┬───┐  ┌───┬───┐  ┌───┬───┐  │ │  ┌───┬───┐  ┌───┬───┐  ┌───┬───┐  │
│    │ 0 │ 5 │  │ 1 │ 1 │  │ 2 │ 3 │  │ │  │ 0 │ 1 │  │ 0 │ 3 │  │ 0 │ 4 │  │
│    └───┴───┘  └───┴───┘  └───┴───┘  │ │  └───┴───┘  └───┴───┘  └───┴───┘  │
│                                   │ │                                   │
│        Total Pip Count: 12        │ │        Total Pip Count: 8         │
│                                   │ │                                   │
└───────────────────────────────────┘ └───────────────────────────────────┘
┌───────────────────────────────────────────────────────────────────────────┐
│                               Move History                                │
│                                                                           │
│  #   Player   Move                                                        │
│  1   player1  [6|6] on left end                                           │
│  2   player2  [6|4] on right end                                          │
│  3   player1  [4|2] on right end                                          │
│                                                                           │
└───────────────────────────────────────────────────────────────────────────┘
```

## Integration with LLM Agents

The Dominoes game is designed to work seamlessly with LLM-powered agents. The state representation includes fields for player analysis and strategic thinking, making it ideal for AI research and experimentation.

## Contributing

Contributions to improve the Dominoes game implementation are welcome. Some areas for potential enhancement:

- Additional rule variations (e.g., blocking game, points scoring)
- Network multiplayer support
- Improved AI strategies
- Enhanced visualizations and animations

Please follow the project's coding style and include tests for new features.
