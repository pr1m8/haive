# Mastermind Game

A complete implementation of the classic Mastermind code-breaking game within the Haive framework.

## Game Overview

Mastermind is a code-breaking game where:

1. The codemaker creates a secret code of four colored pegs
2. The codebreaker must guess the code within a limited number of turns
3. After each guess, the codemaker provides feedback:
   - Black pegs: correct color and position
   - White pegs: correct color but wrong position

The codebreaker wins if they guess the code correctly within the maximum number of turns. Otherwise, the codemaker wins.

## Features

- Complete game logic with Rich UI visualization
- Support for both human and AI players
- Robust state management and error handling
- Analysis capabilities for AI players

## Components

- **agent.py**: Main game agent handling gameplay and orchestration
- **config.py**: Configuration classes for game settings
- **models.py**: Data models for game entities (guesses, feedback, analysis)
- **state.py**: Game state management and representation
- **state_manager.py**: Logic for manipulating game state and applying moves
- **ui.py**: Rich terminal UI for game visualization
- **engines.py**: LLM engine configurations for AI players
- **example.py**: Example script to run the game

## Usage

To run a basic game:

```python
from haive.games.mastermind.agent import MastermindAgent
from haive.games.mastermind.config import MastermindConfig

# Create a configuration with optional custom settings
config = MastermindConfig(
    codemaker="player1",  # Who creates the secret code
    max_turns=10,         # Maximum number of guesses allowed
    colors=["red", "blue", "green", "yellow", "purple", "orange"],
    # Optional predefined secret code
    secret_code=["red", "blue", "green", "yellow"]
)

# Create and run the agent
agent = MastermindAgent(config=config)
final_state = agent.run_game(visualize=True)
```

## Customization

The game can be customized through the `MastermindConfig` class:

- **codemaker**: Which player creates the code ("player1" or "player2")
- **max_turns**: Maximum number of guesses allowed
- **colors**: List of available colors
- **code_length**: Length of the secret code (default is 4)
- **secret_code**: Optional predefined secret code
- **enable_analysis**: Whether to enable AI analysis of game positions
- **visualize**: Whether to enable visualization

## Implementation Details

### State Management

The game state is represented by the `MastermindState` class, which includes:

- Secret code
- History of guesses and feedback
- Current player's turn
- Game status
- Analysis data

### Agent Flow

1. **Initialization**: Set up the game state with a secret code
2. **Turn Loop**:
   - Codebreaker makes a guess
   - System evaluates the guess and provides feedback
   - System analyzes the current position (if enabled)
   - Repeat until the code is guessed or max turns are reached
3. **Game End**: Determine winner and display results

### Rich UI

The game includes a Rich terminal UI that visualizes:

- The game board with all guesses and feedback
- Game status information
- Analysis data from AI players
- Final results display

## Error Handling

The implementation includes robust error handling:

- State conversion and validation
- Fallback mechanisms for invalid inputs
- Graceful degradation when components are unavailable
- Loop detection to prevent infinite gameplay

## Dependencies

- Rich library for terminal UI
- Pydantic for data validation
- LangGraph for workflow management
