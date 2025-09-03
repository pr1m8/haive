# Dominoes Agent Examples

Real examples and outputs from the dominoes agent.

## dominoes_README

**Source**: `packages/haive-games/src/haive/games/dominoes/README.md`

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
# Ru

... (truncated)


---

```
