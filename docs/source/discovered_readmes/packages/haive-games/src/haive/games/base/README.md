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
                ["p", "p", "p", "p", "p", "p", "p", "p"],
                ["r", "n", "b", "q", "k", "b", "n", "r"]]

        return ChessState(
            board=board,
            current_player="white"
        )

    def is_valid_move(self, state: ChessState, move: dict) -> bool:
        # Validate chess move
        # ...
        return True

    def apply_move(self, state: ChessState, move: dict) -> ChessState:
        # Apply move to create new state
        new_state = state.model_copy(deep=True)
        # Update board
        # ...
        return new_state

    def is_game_over(self, state: ChessState) -> bool:
        # Check for checkmate, stalemate, etc.
        # ...
        return False

# Create game agent
class ChessAgent(GameAgent):
    def __init__(self, config: ChessConfig):
        super().__init__(config)
        self.state_manager = ChessStateManager(config)

    def run(self):
        state = self.state_manager.initialize_state()

        while not self.state_manager.is_game_over(state):
            # Get current player's move
            move = self.get_agent_move(state)

            # Validate and apply move
            if self.state_manager.is_valid_move(state, move):
                state = self.state_manager.apply_move(state, move)

        return state

    def get_agent_move(self, state: ChessState) -> dict:
        # Get move from LLM or other source
        # ...
        return {"from": "e2", "to": "e4"}
```

## Components in Detail

### GameAgent

Base class that implements the core game loop and agent management.

```python
from haive.games.base import GameAgent, GameConfig

class MyGameAgent(GameAgent):
    def __init__(self, config: GameConfig):
        super().__init__(config)
        # Initialize game-specific components

    def run(self):
        # Main game loop
        state = self.initialize_game()

        while not self.is_game_over(state):
            state = self.process_turn(state)

        return state

    def get_agent_move(self, state):
        # Generate agent's move based on current state
        prompt = self.create_prompt(state)
        response = self.llm.invoke(prompt)
        return self.parse_response(response)
```

### GameState

Base model for game state representation with common attributes.

```python
from haive.games.base import GameState
from pydantic import Field
from typing import List, Dict

class PokerState(GameState):
    players: List[Dict] = Field(...)
    community_cards: List[str] = Field(default_factory=list)
    pot: int = Field(default=0)
    current_round: str = Field(default="pre-flop")
    dealer_position: int = Field(default=0)
    current_player_idx: int = Field(default=0)
    min_bet: int = Field(default=0)
```

### GameStateManager

Interface for managing game state transitions, rule enforcement, and game progression.

```python
from haive.games.base import GameStateManager

class PokerStateManager(GameStateManager):
    def initialize_state(self):
        # Set up initial game state
        return PokerState(
            players=[{"id": player_id, "chips": self.config.starting_chips, "hand": []}
                    for player_id in self.config.player_ids]
        )

    def deal_cards(self, state):
        # Deal cards to players
        new_state = state.model_copy(deep=True)
        deck = self.create_deck()

        for player in new_state.players:
            player["hand"] = [deck.pop(), deck.pop()]

        return new_state

    def process_betting_round(self, state):
        # Handle a round of betting
        new_state = state.model_copy(deep=True)
        # ...
        return new_state

    def is_round_complete(self, state):
        # Check if current betting round is complete
        return all(player["has_acted"] for player in state.players if player["active"])

    def is_game_over(self, state):
        # Check if the game is over
        return len([p for p in state.players if p["active"]]) <= 1 or state.current_round == "showdown"
```

### GameConfig

Configuration class for game parameters with validation.

```python
from haive.games.base import GameConfig
from pydantic import Field, field_validator
from typing import List

class PokerConfig(GameConfig):
    player_ids: List[str] = Field(...)
    starting_chips: int = Field(default=1000)
    small_blind: int = Field(default=5)
    big_blind: int = Field(default=10)
    max_players: int = Field(default=9)

    @field_validator("player_ids")
    def validate_player_count(cls, v):
        if len(v) < 2:
            raise ValueError("Poker requires at least 2 players")
        if len(v) > cls.max_players:
            raise ValueError(f"Maximum {cls.max_players} players allowed")
        return v

    @field_validator("small_blind", "big_blind")
    def validate_blinds(cls, v):
        if v <= 0:
            raise ValueError("Blinds must be positive")
        return v
```

## Usage Patterns

### Game Initialization and Configuration

```python
from haive.games.base import GameConfig
from haive.games.poker import PokerAgent, PokerConfig

# Create configuration
config = PokerConfig(
    player_ids=["player1", "player2", "player3", "player4"],
    starting_chips=1000,
    small_blind=5,
    big_blind=10,
    max_rounds=10
)

# Create and run the game
agent = PokerAgent(config)
result = agent.run()
```

### Game Template Generation

```python
from haive.games.base import GameTemplateGenerator

# Generate template for a new game implementation
generator = GameTemplateGenerator(
    game_name="Blackjack",
    game_type="card",
    player_count={"min": 1, "max": 7},
    has_rounds=True
)

# Generate template files
generator.generate(output_dir="my_games")
```

## Integration with LLMs

```python
from haive.games.base import GameAgent
from haive.core.engine.aug_llm import AugLLMConfig, compose_runnable

class ChessAgent(GameAgent):
    def __init__(self, config):
        super().__init__(config)

        # Create LLM for move generation
        llm_config = AugLLMConfig(
            system_message="You are playing chess. Analyze the board and suggest the best move.",
            temperature=0.2
        )
        self.llm = compose_runnable(llm_config)

    def get_agent_move(self, state):
        # Format the board state for the LLM
        board_representation = self.format_board(state.board)

        # Get move from LLM
        prompt = f"""
        Current board:
        {board_representation}

        Current player: {state.current_player}

        What is your next move? Respond with the starting square and destination square (e.g., 'e2 to e4').
        """

        response = self.llm.invoke(prompt)

        # Parse the response
        return self.parse_move(response)
```

## Best Practices

- **State Immutability**: Always create new state objects rather than modifying existing ones
- **Clear Validation**: Implement thorough move validation to prevent illegal moves
- **Error Handling**: Include robust error handling for edge cases
- **Agent Interfaces**: Define clear interfaces for agent decisions
- **State Snapshots**: Keep a history of game states for analysis
- **Separation of Concerns**: Keep game logic separate from agent decision logic

## Migration to Framework

For new projects, consider using the more advanced `framework` module instead:

```python
# Old approach (base module)
from haive.games.base import GameAgent, GameConfig, GameState

# New approach (framework module)
from haive.games.framework import GameAgent, GameConfig, GameState
```

The framework module provides additional features and improvements over the base module.

## API Reference

For full API details, see the [documentation](https://docs.haive.ai/games/base).

## Related Modules

- **haive.games.framework**: Advanced framework for game development
- **haive.core.engine**: Engine components used by game agents
- **haive.core.models**: Model definitions used in games
