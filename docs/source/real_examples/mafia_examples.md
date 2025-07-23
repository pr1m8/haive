# Mafia Agent Examples

Real examples and outputs from the mafia agent.

## mafia_README

**Source**: `packages/haive-games/src/haive/games/mafia/README.md`

# Mafia Game

This package provides a complete implementation of the Mafia party game for the Haive agent framework.

## Overview

Mafia is a social deduction game where players are assigned secret roles and must work together or against each other to achieve their faction's goals. The game alternates between day and night phases, with different actions available to players based on their roles.

- **Villagers** work to identify and eliminate Mafia members
- **Mafia** members secretly eliminate Villagers while avoiding detection
- **Doctor** can save one player each night from being killed
- **Detective** can investigate one player each night to learn their role
- **Narrator** manages game flow and provides narrative structure

## Features

- Multi-player game agent with role-based gameplay
- Day/Night phase management
- Role-specific actions and abilities
- Hidden information and voting mechanics
- Game state tracking and validation
- LLM-powered player decision making
- Rich terminal visualization

## Usage

```python
from haive.games.mafia import MafiaAgent, MafiaAgentConfig

# Create a default configuration for 7 players (6 players + narrator)
config = MafiaAgentConfig.default_config(
    player_count=7,
    max_days=3
)

# Create and initialize the agent
agent = MafiaAgent(config)

# Generate player names
player_names = [f"Player_{i+1}" for i in range(6)]
player_names.append("Narrator")  # Add narrator as the last player

# Initialize game state
from haive.games.mafia.state_manager import MafiaStateManager
initial_state = MafiaStateManager.initialize(player_names)

# Run the game with visualization
for state in agent.app.stream(initial_state.model_dump(), stream_mode="values"):
    agent.visualize_state(state)

    # Check for game end
    if state.get("game_status") != "ongoing":
        break
```

For a complete example with error handling and additional options, see the `example.py` file.

## Game Structure

The game follows this state machine:

1. **Setup P

... (truncated)


---

