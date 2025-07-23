# Framework Agent Examples

Real examples and outputs from the framework agent.

## framework_README

**Source**: `packages/haive-games/src/haive/games/framework/README.md`

# Haive Games: Framework Module

## Overview

The Framework module provides the foundation for building AI agent-based games in the Haive ecosystem. It offers a structured, extensible architecture for implementing games with consistent interfaces, state management, and agent integration. This framework handles the common patterns and mechanics shared across different game implementations, allowing developers to focus on game-specific logic.

## Key Features

- **Standardized Architecture**: Consistent design patterns for all game implementations
- **State Management**: Robust handling of game state transitions and validation
- **Agent Integration**: Seamless connection with LLM-based game agents
- **Multi-Player Support**: Specialized components for multi-player interactions
- **Type Safety**: Strong typing with Pydantic models for game state and configuration
- **Extensibility**: Easy extension points for custom game mechanics

## Components

### Core Components

#### GameAgent

The central class that orchestrates the game flow and manages agent interactions.

```python
from haive.games.framework import GameAgent

class ChessAgent(GameAgent):
    def __init__(self, config):
        super().__init__(config)
        self.state_manager = ChessStateManager(config)

    def get_agent_move(self, state, player_id):
        # Implement agent decision logic
        prompt = self.create_move_prompt(state, player_id)
        response = self.llm.invoke(prompt)
        return self.parse_move(response)
```

#### GameState

Base model for game state representation, ensuring consistent state structure.

```python
from haive.games.framework import GameState
from pydantic import Field
from typing import List

class ChessState(GameState):
    board: List[List[str]] = Field(...)
    current_player: str = Field(...)
    move_history: List[str] = Field(default_factory=list)
    captured_pieces: dict = Field(default_factory=dict)
    game_over: bool = Field(default=False)
    winner: str

... (truncated)


---

