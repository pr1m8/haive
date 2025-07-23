# Base Agent Examples

Real examples and outputs from the base agent.

## base_README

**Source**: `packages/haive-games/src/haive/games/base/README.md`

# Haive Games: Base Module

## Overview

The Base module provides foundational components for building game agents in the Haive ecosystem. This module serves as the original implementation of the game framework, offering core abstractions for game state, agent logic, and state management. While newer games should use the more advanced `framework` module, the base module remains available for backward compatibility and simpler implementations.

## Key Components

- **GameAgent**: Base agent class for game management and execution
- **GameState**: Core state representation with common attributes
- **GameStateManager**: Interface for game state transitions and rule enforcement
- **GameConfig**: Configuration class for game parameters
- **GameAgentFactory**: Factory for creating game agents
- **Template Generator**: Utilities for creating new game implementations

## Installation

This module is included as part of the `haive-games` package:

```bash
pip install haive-games
```

## Quick Start

```python
from haive.games.base import GameAgent, GameConfig, GameState, GameStateManager
from pydantic import Field
from typing import List

# Define game-specific state
class ChessState(GameState):
    board: List[List[str]] = Field(...)
    current_player: str = Field(...)

# Define game-specific config
class ChessConfig(GameConfig):
    player_names: List[str] = Field(default=["Player 1", "Player 2"])
    time_limit: int = Field(default=300)  # 5 minutes per player

# Create state manager
class ChessStateManager(GameStateManager):
    def initialize_state(self) -> ChessState:
        # Initialize the chess board
        board = [["R", "N", "B", "Q", "K", "B", "N", "R"],
                ["P", "P", "P", "P", "P", "P", "P", "P"],
                [" ", " ", " ", " ", " ", " ", " ", " "],
                [" ", " ", " ", " ", " ", " ", " ", " "],
                [" ", " ", " ", " ", " ", " ", " ", " "],
                [" ", " ", " ", " ", " ", " ", " ", " "],
                ["p",

... (truncated)


---

