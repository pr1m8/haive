# Risk Agent Examples

Real examples and outputs from the risk agent.

## risk_README

**Source**: `packages/haive-games/src/haive/games/risk/README.md`

# Risk

A complete implementation of the classic board game Risk with sophisticated AI agents that use Large Language Models for strategic decision-making.

## Overview

The Risk game module provides a full implementation of the classic world domination strategy game, featuring intelligent AI agents that can analyze territorial positions, plan attacks, manage reinforcements, and execute complex strategic maneuvers. The system supports customizable game rules, multiple player counts, and advanced strategic analysis.

## Key Features

- **Complete Risk Implementation**: Full classic Risk rules with territories, continents, armies, and cards
- **Strategic AI Agents**: LLM-powered agents with sophisticated strategic reasoning
- **Flexible Game Configuration**: Customizable rules, player counts, and game variants
- **Territory Management**: Complete world map with adjacency relationships and continent bonuses
- **Combat System**: Dice-based combat with proper attack/defense mechanics
- **Card Trading**: Risk card collection and trading for reinforcement armies
- **Phase Management**: Proper game phase progression (reinforce, attack, fortify)
- **Strategic Analysis**: Deep position analysis and move recommendations

## Quick Start

### Basic Game Setup

```python
from haive.games.risk import RiskStateManager, RiskAgent, RiskConfig

# Initialize a 3-player game
players = ["Napoleon", "Caesar", "Alexander"]
config = RiskConfig.classic()
manager = RiskStateManager.initialize(players, config)

# Create AI agents for each player
agents = {
    name: RiskAgent(name=name, state=manager.state, strategy="balanced")
    for name in players
}

# Game loop
while not manager.state.is_game_over():
    current_player = manager.state.current_player
    agent = agents[current_player]

    # Get strategic move from agent
    move = agent.get_move()

    # Apply move to game state
    manager.apply_move(move)
    print(f"Turn {manager.state.turn_number}: {current_player} - {move}")

# Deter

... (truncated)


---

