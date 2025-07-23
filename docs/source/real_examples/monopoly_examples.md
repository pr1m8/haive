# Monopoly Agent Examples

Real examples and outputs from the monopoly agent.

## monopoly_README

**Source**: `packages/haive-games/src/haive/games/monopoly/README.md`

# Monopoly

A comprehensive implementation of the Monopoly board game with intelligent AI agents powered by Large Language Models (LLMs).

## Overview

The Monopoly game implementation provides sophisticated AI agents that can play the classic board game with strategic decision-making, property management, and adaptive gameplay. The system includes both game orchestration agents and individual player agents that use LLM reasoning to make intelligent decisions.

## Key Features

- **Strategic AI Players**: LLM-powered agents that analyze game state and make strategic decisions
- **Complete Game Implementation**: Full Monopoly board with properties, utilities, railroads, and special spaces
- **Property Management**: Intelligent buying, selling, mortgaging, and building decisions
- **Trade Negotiations**: Support for property trading between players (configurable)
- **Jail Mechanics**: Smart decisions for getting out of jail
- **Event System**: Chance and Community Chest cards with proper game effects
- **Game Orchestration**: Automated game flow with turn management and win conditions

## Quick Start

### Basic Game Setup

```python
from haive.games.monopoly import MonopolyGameAgent, MonopolyGameAgentConfig
from haive.games.monopoly import MonopolyPlayerAgent, MonopolyPlayerAgentConfig

# Create player agent for decision-making
player_config = MonopolyPlayerAgentConfig(
    name="player_agent",
    engine=your_llm_engine,
    temperature=0.7
)
player_agent = MonopolyPlayerAgent(player_config)

# Create game orchestration agent
game_config = MonopolyGameAgentConfig(
    name="monopoly_game",
    player_names=["Alice", "Bob", "Charlie"],
    max_turns=1000,
    enable_trading=True,
    player_agent=player_agent
)

game_agent = MonopolyGameAgent(game_config)

# Run the game
result = await game_agent.arun("Start a new Monopoly game")
```

### Simple Demo

```python
from haive.games.monopoly import MonopolyState
from haive.games.monopoly.utils import create_board, create_p

... (truncated)


---

