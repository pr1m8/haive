# Connect4 Game Module

A complete implementation of the Connect4 game with LLM-powered agents and rich terminal UI visualization.

## Features

- **LLM-powered game agents**: Uses language models to make strategic moves and analyze positions
- **Rich terminal UI**: Colorful board visualization, game status panels, and animations
- **Position analysis**: Strategic evaluation of the board with threat detection
- **Move validation**: Complete move validation and game rules enforcement
- **Game state management**: Immutable state pattern with history tracking

## Quick Start

```python
from haive.games.connect4 import Connect4Agent, Connect4AgentConfig, Connect4UI
from haive.games.connect4.state_manager import Connect4StateManager

# Create and configure a Connect4 agent
config = Connect4AgentConfig(enable_analysis=True)
agent = Connect4Agent(config)

# Create the UI
ui = Connect4UI()

# Initialize game state
initial_state = Connect4StateManager.initialize()

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
        ui.show_game_over(step.get("winner"))
        break
```

## Running from Command Line

You can run a Connect4 game directly from the command line:

```bash
python -m haive.games.connect4.example
```

Command-line options:

- `--debug`: Enable debug mode with detailed logging
- `--analysis`: Enable position analysis during gameplay
- `--delay`: Set delay between moves in seconds (default: 1.0)

## Module Components

### Connect4Agent

The main game agent that manages the Connect4 game flow, using LangGraph for the workflow and LLMs for move generation and analysis.

```python
agent = Connect4Agent(Connect4AgentConfig())
result = agent.run_game()
```

### Connect4UI

Rich terminal UI for visualizing the game board and game information.

```python
ui = Connect4UI()
ui.display_state(state)
ui.show_thinking("red")  # Show thinking animation
ui.show_move(move, "red")  # Display a move
ui.show_game_over("red")  # Show game over screen
```

### Connect4State

Represents the complete state of a Connect4 game, including board representation, game status, and move history.

```python
state = Connect4State.initialize()
print(state.board_string)  # Display text representation of board
```

### Connect4StateManager

Manages game state transitions, move application, and win condition checking.

```python
state = Connect4StateManager.initialize()
move = Connect4Move(column=3)
new_state = Connect4StateManager.apply_move(state, move)
```

### Models

- `Connect4Move`: Represents a move with column selection and optional explanation
- `Connect4PlayerDecision`: Player's move decision with reasoning and alternatives
- `Connect4Analysis`: Position analysis with threat detection and evaluation

## Customization

You can customize the game behavior through the `Connect4AgentConfig` class:

```python
config = Connect4AgentConfig(
    enable_analysis=True,  # Enable position analysis
    max_moves=42,  # Maximum number of moves
    should_visualize_graph=True,  # Visualize the workflow graph
)
```

## UI Customization

The Connect4UI class can be customized by modifying the color scheme:

```python
ui = Connect4UI()
ui.colors["red"]["piece"] = "bright_red"  # Change red piece color
ui.colors["yellow"]["piece"] = "bright_yellow"  # Change yellow piece color
ui.colors["board"] = "blue"  # Change board color
```

## Contributing

When contributing to this module, please maintain the existing code style and ensure all new code has Google-style docstrings for Sphinx documentation.
