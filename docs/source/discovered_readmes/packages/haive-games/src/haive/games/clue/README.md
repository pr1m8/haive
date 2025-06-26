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
ui = ClueUI()
ui.display_state(state)
ui.show_thinking("player1")  # Show thinking animation
ui.show_guess(guess, "player1")  # Display a guess
ui.show_response(response, "player1")  # Show response to a guess
ui.show_game_over(state)  # Show game over screen
```

### ClueState

Represents the complete state of a Clue game, including solution, player cards, guess history, and hypotheses.

```python
state = ClueStateManager.initialize()
print(f"Current player: {state.current_player}")
print(f"Turn: {state.current_turn_number}/{state.max_turns}")
```

### ClueStateManager

Manages game state transitions, guess application, and deduction tracking.

```python
state = ClueStateManager.initialize()
guess = ClueGuess(suspect=ValidSuspect.COLONEL_MUSTARD,
                  weapon=ValidWeapon.KNIFE,
                  room=ValidRoom.KITCHEN)
new_state = ClueStateManager.apply_move(state, guess)
```

### Models

- `ClueGuess`: Represents a guess with suspect, weapon, and room
- `ClueResponse`: Response to a guess, indicating if it was correct or refuted
- `ClueSolution`: The correct solution to the mystery
- `ClueHypothesis`: AI-generated hypothesis about the solution
- Various enums (`ValidSuspect`, `ValidWeapon`, `ValidRoom`, `CardType`)

## Customization

You can customize the game behavior through the `ClueConfig` class:

```python
config = ClueConfig(
    max_turns=15,  # Maximum number of turns
    first_player="player2",  # Player who starts the game
    solution={  # Predetermined solution (optional)
        "suspect": ValidSuspect.COLONEL_MUSTARD,
        "weapon": ValidWeapon.KNIFE,
        "room": ValidRoom.KITCHEN,
    },
)
```

## UI Customization

The ClueUI class can be customized by modifying the color scheme:

```python
ui = ClueUI()
ui.colors["suspect"] = "bright_blue"  # Change suspect color
ui.colors["weapon"] = "bright_red"  # Change weapon color
ui.colors["room"] = "bright_green"  # Change room color
ui.colors["player1"] = "bright_cyan"  # Change player1 color
```

## Contributing

When contributing to this module, please maintain the existing code style and ensure all new code has Google-style docstrings for Sphinx documentation.
