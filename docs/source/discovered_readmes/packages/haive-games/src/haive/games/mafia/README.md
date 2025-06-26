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

1. **Setup Phase**: Players are assigned roles, and the game initializes
2. **Night Phase**: Special roles perform their actions (Mafia kill, Doctor saves, Detective investigates)
3. **Day Discussion**: Players discuss and share information to identify Mafia
4. **Day Voting**: Players vote to eliminate a suspected Mafia member
5. Repeat 2-4 until win conditions are met

The game ends when either:

- All Mafia members are eliminated (Village wins)
- Mafia members equal or outnumber Villagers (Mafia wins)

## Components

- **agent.py**: Main game agent implementation
- **config.py**: Game configuration
- **engines.py**: LLM engine configurations for different roles
- **models.py**: Data models and schemas
- **state.py**: Game state representation
- **state_manager.py**: Game state transitions and logic
- **example.py**: Complete example implementation

## Customization

The game can be customized by modifying the configuration:

```python
# Customize player count and game length
config = MafiaAgentConfig(
    name="custom_mafia",
    max_days=5,
    day_discussion_rounds=2,
    engines=custom_engines,  # Use custom LLM configurations
    initial_player_count=9
)
```

You can also create custom roles or modify game rules by extending the appropriate classes.
