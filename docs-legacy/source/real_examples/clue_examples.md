# Clue Agent Examples

Real examples and outputs from the clue agent.

## clue_README

**Source**: `packages/haive-games/src/haive/games/clue/README.md`

# Clue Game Module

A complete implementation of the Clue (Cluedo) detective game with LLM-powered agents and rich terminal UI visualization.

## Features

- **LLM-powered deduction**: Uses language models to make guesses and analyze evidence
- **Rich terminal UI**: Colorful game visualization, player cards, guess history, and animations
- **Deduction tracking**: Maintains hypotheses and confidence levels as the game progresses
- **Game state management**: Immutable state pattern with complete history tracking
- **Multiple player support**: Play with any number of human or AI players

## Quick Start

```python
from haive.games.clue import ClueAgent, ClueConfig, ClueUI
from haive.games.clue.state_manager import ClueStateManager

# Create and configure a Clue agent
config = ClueConfig(max_turns=15)
agent = ClueAgent(config)

# Create the UI
ui = ClueUI()

# Initialize game state
initial_state = ClueStateManager.initialize()

# Display initial state
ui.display_state(initial_state)

# Run a game
for step in agent.app.stream(
    initial_state.model_dump(),
    debug=False,
    stream_mode="values",
):
    # Display the current state
    ui.display_state(step)

    # Check for game over
    if step.get("game_status") != "ongoing":
        ui.show_game_over(ClueState(**step))
        break
```

## Running from Command Line

You can run a Clue game directly from the command line:

```bash
python -m haive.games.clue.example
```

Command-line options:

- `--debug`: Enable debug mode with detailed logging
- `--turns`: Set maximum number of turns (default: 10)
- `--delay`: Set delay between moves in seconds (default: 1.0)

## Module Components

### ClueAgent

The main game agent that manages the Clue game flow, using LangGraph for the workflow and LLMs for guesses and analysis.

```python
agent = ClueAgent(ClueConfig())
result = agent.run_game()
```

### ClueUI

Rich terminal UI for visualizing the game board, player cards, guess history, and deductions.

```python
ui = ClueUI

... (truncated)


---

```
