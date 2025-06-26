# Haive Games

## Overview

The Haive Games module provides a comprehensive framework for creating and running AI agent-based games. It includes implementations of classic games like Chess, Poker, and Monopoly, as well as novel AI-specific games like debate and social deduction games. The framework enables researchers and developers to evaluate AI capabilities, test multi-agent interactions, and explore emergent behaviors in competitive and cooperative environments.

## Key Features

- **Game Framework**: Reusable components for building new games with minimal boilerplate
- **Multi-Agent Support**: Infrastructure for games with 2+ players and complex interaction patterns
- **State Management**: Robust game state tracking, validation, and progression
- **Agent Integration**: Seamless integration with LLM-based agents for decision making
- **Visualization**: Tools for rendering game states and agent interactions
- **Evaluation**: Benchmarking and metrics for comparing agent performance
- **Configurability**: Flexible configuration for customizing game parameters

## Installation

This module is part of the `haive-games` package. Install it with:

```bash
pip install haive-games
```

Or install via Poetry:

```bash
poetry add haive-games
```

## Quick Start

### Playing a Simple Game

```python
from haive.games.tic_tac_toe import TicTacToeAgent, TicTacToeConfig
from haive.core.engine.aug_llm import AugLLMConfig

# Configure the game
config = TicTacToeConfig(
    player_names=["Player 1", "Player 2"],
    llm_config=AugLLMConfig(
        system_message="You are playing Tic Tac Toe. Make strategic moves to win.",
        temperature=0.2
    )
)

# Create and run the game
agent = TicTacToeAgent(config)
result = agent.run()

# View the results
print(f"Winner: {result.winner}")
print(f"Game history: {result.moves}")
```

### Creating a Custom Game

```python
from haive.games.framework import GameAgent, GameConfig, GameState, GameStateManager
from pydantic import Field
from typing import List

# Define game-specific models
class MyGameState(GameState):
    score: int = Field(default=0)
    rounds: int = Field(default=0)

class MyGameConfig(GameConfig):
    max_rounds: int = Field(default=10)
    difficulty: str = Field(default="medium")

# Create state manager for game logic
class MyGameStateManager(GameStateManager):
    def initialize_state(self) -> MyGameState:
        return MyGameState()

    def is_game_over(self, state: MyGameState) -> bool:
        return state.rounds >= self.config.max_rounds

    def process_move(self, state: MyGameState, move: dict) -> MyGameState:
        # Game-specific move processing
        state.rounds += 1
        return state

# Create the game agent
class MyGameAgent(GameAgent):
    def __init__(self, config: MyGameConfig):
        super().__init__(config)
        self.state_manager = MyGameStateManager(config)

    def run(self):
        state = self.state_manager.initialize_state()

        while not self.state_manager.is_game_over(state):
            # Game turn logic
            move = self.get_agent_move(state)
            state = self.state_manager.process_move(state, move)

        return state
```

## Game Catalog

The package includes implementations for the following games:

### Classic Games

- **Chess**: Complete chess implementation with LLM-based reasoning
- **Poker**: Texas Hold'em with betting, hand evaluation, and bluffing
- **Monopoly**: Property management and economic strategy
- **Tic-Tac-Toe**: Simple grid-based game for quick testing
- **Go**: Ancient strategy board game
- **Nim**: Mathematical strategy game
- **Battleship**: Grid-based search game
- **Mancala**: Stone collection strategy game
- **Connect4**: Vertical grid connection game
- **Mastermind**: Code-breaking logic game
- **Reversi/Othello**: Disk flipping territory game

### Novel AI Games

- **Among Us**: Social deduction game with deception and reasoning
- **Debate**: Structured argumentation with judges and rebuttals
- **Mafia/Werewolf**: Social deduction with hidden roles
- **Clue/Cluedo**: Mystery solving with evidence collection

### Single Player Games

- **Wordle**: Word guessing game
- **2048**: Tile sliding puzzle
- **Word Search**: Grid-based word finding

## Framework Architecture

The games framework is organized into several key components:

### Base Classes

- **GameAgent**: Core agent class that manages the game flow
- **GameState**: Data model for the current game state
- **GameStateManager**: Handles state transitions and game logic
- **GameConfig**: Configuration for the game parameters

### Key Modules

- **framework**: Core framework components shared across games
- **base**: Legacy framework for backward compatibility
- **base_v2**: New version of the framework with enhanced features
- **multi_player**: Extensions for games with multiple players
- **single_player**: Simplified framework for single-player games

## Best Practices

### Game Development

1. **Extend Base Classes**: Always extend the framework's base classes rather than starting from scratch
2. **State Immutability**: Treat game states as immutable; create new states for changes
3. **Clear Validation**: Implement thorough move validation to prevent illegal moves
4. **Agent Interfaces**: Design clear, structured interfaces for agent decisions
5. **Progressive Disclosure**: Provide agents only with information they should have access to

### Agent Configuration

1. **Adjust Temperature**: Use lower temperatures (0.1-0.3) for logic/rule-based decisions
2. **Structured Output**: Use structured outputs for moves to ensure valid formatting
3. **Context Management**: Provide relevant game context without overwhelming the agent
4. **Few-Shot Examples**: Include examples of valid moves for better performance

## Advanced Usage

### Game Evaluation and Benchmarking

```python
from haive.games.benchmark import benchmark_agents
from haive.games.chess import ChessAgent, ChessConfig

# Configure different agent variants
configurations = [
    ChessConfig(name="Aggressive", strategy_bias="aggressive", temperature=0.7),
    ChessConfig(name="Defensive", strategy_bias="defensive", temperature=0.3),
    ChessConfig(name="Balanced", strategy_bias="balanced", temperature=0.5),
]

# Run a tournament with multiple games
results = benchmark_agents(
    agent_class=ChessAgent,
    configurations=configurations,
    num_games=50,
    parallel=True
)

# Analyze results
print(results.win_rates)
print(results.average_game_length)
print(results.strategy_analysis)
```

### Custom Visualization

```python
from haive.games.utils.visualization import GameVisualizer
from haive.games.chess import ChessState

class ChessVisualizer(GameVisualizer):
    def render_board(self, state: ChessState) -> str:
        # Create ASCII or Unicode representation of the chess board
        # ...
        return board_representation

    def render_history(self, states: list[ChessState]) -> str:
        # Generate a move-by-move replay
        # ...
        return history_representation

# Use the visualizer
visualizer = ChessVisualizer()
rendered_board = visualizer.render_board(current_state)
print(rendered_board)
```

### Adding Observer Agents

```python
from haive.games.poker import PokerAgent, PokerConfig
from haive.games.utils.observers import GameObserver

class PokerCommentator(GameObserver):
    def observe(self, state, previous_state=None):
        # Generate commentary on the current game state
        if previous_state and state.current_phase != previous_state.current_phase:
            print(f"Moving to {state.current_phase} phase!")

        if state.last_action:
            print(f"Player {state.last_action.player_id} {state.last_action.type} "
                  f"with {state.last_action.amount if hasattr(state.last_action, 'amount') else ''}")

# Add observer to game
config = PokerConfig(player_names=["Alice", "Bob", "Charlie", "Dave"])
game = PokerAgent(config)
game.add_observer(PokerCommentator())
result = game.run()
```

## API Reference

For full API details, see the [documentation](https://docs.haive.ai/games/).

## Related Modules

- **haive-core**: Core framework components used by games
- **haive-agents**: Agent implementations that can play games
- **haive-tools**: Tools used by agents during gameplay
