# Risk Game Module

The Risk game module provides a complete implementation of the classic board game Risk for use with the Haive framework. This module enables agents to play Risk using LLM-based strategic reasoning, with support for game state management, move validation, and analysis.

## Features

- Complete implementation of classic Risk rules
- Support for 2-6 players
- Configurable game rules and parameters
- LLM-based agents for strategic gameplay
- State management and rule enforcement
- Territory control and continent bonuses
- Card collection and trading
- Attack, defense, and fortification mechanics
- Game position analysis and strategic recommendations

## Components

### Core Models

- `Territory` - Represents a territory on the Risk board with owner, armies, and adjacency information
- `Continent` - Represents a continent with territories and bonus value
- `Card` - Represents a Risk card that can be traded for armies
- `Player` - Represents a player with cards, armies, and elimination status
- `RiskMove` - Represents a move in the game (place armies, attack, fortify, trade cards)
- `RiskAnalysis` - Analysis of a Risk position with recommendations

### Game State

- `RiskState` - Tracks the complete game state including territories, players, cards, and game status
- `RiskStateManager` - Manages state transitions, rule enforcement, and game progression

### Agents and Strategy

- `RiskAgent` - LLM-based agent for playing Risk with strategic reasoning
- `RiskConfig` - Configuration for customizing game rules and parameters

## Usage Example

```python
from haive.games.risk import RiskState, RiskStateManager, RiskAgent, RiskConfig

# Initialize game with players
players = ["Player1", "Player2", "Player3"]
config = RiskConfig.classic()
manager = RiskStateManager.initialize(players, config)

# Create agents
agents = {
    name: RiskAgent(name=name, state=manager.state, strategy="balanced")
    for name in players
}

# Game loop
while not manager.state.is_game_over():
    current_player = manager.state.current_player
    agent = agents[current_player]

    # Get move from agent
    move = agent.get_move()

    # Apply move to state
    manager.apply_move(move)
    print(f"Turn {manager.state.turn_number}: {move}")

# Game over
winner = manager.state.get_winner()
print(f"Game over! Winner: {winner}")
```

## Customization

The Risk game can be customized through the `RiskConfig` class, which allows you to adjust rules such as:

- Player count
- Card trading rules
- Fortification rules
- Dice mechanics
- Custom territory maps

## Integration with Haive Framework

This module is designed to work seamlessly with the Haive agent framework, providing:

- Standardized state representation
- Engine configurations for agent deployment
- Strategic analysis capabilities
- Full compatibility with LLM-based reasoning
