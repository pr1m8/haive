# Haive Games Documentation

Welcome to the Haive Games package documentation! This package provides a comprehensive collection of game implementations using the Haive agent framework.

## Overview

The Haive Games package includes 22 fully functional games built on top of the Haive agent system. Each game demonstrates different aspects of agent-based game design, from simple turn-based games to complex multi-player scenarios.

## Quick Start

```python
from haive.games.chess import ChessAgent, ChessConfig
from haive.core.models.llm import LLMConfig, LLMProvider

# Configure LLMs for players
white_llm = LLMConfig(provider=LLMProvider.AZURE, model="gpt-4o")
black_llm = LLMConfig(provider=LLMProvider.AZURE, model="claude-3-5-sonnet")

# Create game configuration
config = ChessConfig(
    aug_llm_configs={"white": white_llm, "black": black_llm},
    max_moves=200
)

# Create and run the game
agent = ChessAgent(config)
initial_state = agent.get_initial_state()

for state in agent.app.stream(initial_state):
    print(f"Move: {state.get('last_move')}")
    if state.get('game_over'):
        print(f"Winner: {state.get('winner')}")
        break
```

## Documentation Structure

- **[Games Overview](./GAMES_OVERVIEW.md)** - Complete list of all 22 games with descriptions
- **[Getting Started](./GETTING_STARTED.md)** - Installation and basic usage
- **[Game Categories](./GAME_CATEGORIES.md)** - Games organized by type
- **[Tournament System](./TOURNAMENT_SYSTEM.md)** - Running tournaments between AI players
- **[Architecture Guide](./ARCHITECTURE.md)** - How games are structured
- **[Development Guide](./DEVELOPMENT_GUIDE.md)** - Creating new games

## Available Games

### Classic Board Games

- Chess, Checkers, Reversi (Othello), Mancala, Nim

### Card Games

- Poker, Texas Hold'em, Dominoes

### Strategy Games

- Risk, Monopoly, Battleship

### Social Deduction Games

- Mafia, Among Us, Clue

### Abstract Strategy

- Connect 4, Tic-Tac-Toe, Fox and Geese, Go

### Puzzle Games

- Mastermind

### Other Games

- Debate (structured argumentation)

## Key Features

- **Unified Architecture**: All games follow a consistent pattern
- **LLM Integration**: Easy configuration of different AI models
- **Tournament Support**: Built-in tournament system for AI vs AI games
- **Extensible Design**: Simple to add new games
- **Type Safety**: Full Pydantic model validation
- **State Management**: Robust game state tracking

## Support

For issues or questions:

- Check the [Troubleshooting Guide](./TROUBLESHOOTING.md)
- See [Common Issues](./COMMON_ISSUES.md)
- File issues at the main Haive repository

## License

Part of the Haive project. See main repository for license details.
