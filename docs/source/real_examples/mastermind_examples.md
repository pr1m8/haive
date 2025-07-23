# Mastermind Agent Examples

Real examples and outputs from the mastermind agent.

## mastermind_README

**Source**: `packages/haive-games/src/haive/games/mastermind/README.md`

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


... (truncated)


---

