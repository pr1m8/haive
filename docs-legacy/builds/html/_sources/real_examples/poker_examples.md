# Poker Agent Examples

Real examples and outputs from the poker agent.

## poker_README

**Source**: `packages/haive-games/src/haive/games/poker/README.md`

# Haive Games: Poker Module

## Overview

The Poker module provides a comprehensive implementation of Texas Hold'em poker for AI agents. It features complete game state management, hand evaluation, betting logic, and strategic decision-making through LLM-based agents. This module enables AI agents to play realistic poker games with reasoning about probabilities, bluffing, and opponent modeling.

## Key Features

- **Complete Texas Hold'em Rules**: Fully implemented poker rules including betting rounds, hand evaluation, and showdown logic
- **Multi-Agent Support**: Designed for multiple players with different strategies
- **State Management**: Comprehensive game state tracking with full history
- **LLM-Based Decision Making**: Sophisticated agent reasoning for poker strategy
- **Betting Logic**: Complete betting system with raises, calls, checks, and folds
- **Hand Evaluation**: Accurate poker hand ranking and comparison
- **Visualization**: Tools for rendering game state and player actions
- **Configurable Parameters**: Adjustable blinds, stack sizes, and game variants

## Installation

This module is part of the `haive-games` package. Install the full package with:

```bash
pip install haive-games
```

## Quick Start

```python
from haive.games.poker import PokerAgent, PokerAgentConfig
from haive.core.engine.aug_llm import AugLLMConfig

# Configure the game
config = PokerAgentConfig(
    player_names=["Alice", "Bob", "Charlie", "Dave"],
    starting_chips=1000,
    small_blind=5,
    big_blind=10,
    llm_config=AugLLMConfig(
        system_message="You are playing Texas Hold'em poker. Make strategic decisions based on your cards, the community cards, and betting patterns.",
        temperature=0.7  # Higher temperature for more varied play styles
    )
)

# Create and run the game
agent = PokerAgent(config)
result = agent.run()

# View results
print(f"Winner: {result.winner}")
print(f"Final chip counts: {result.chip_counts}")
print(f"Hands played: {result.num_hand

... (truncated)


---

```
