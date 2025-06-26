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
    winner: str = Field(default=None)
```

#### GameStateManager

Handles game logic, state transitions, and rule enforcement.

```python
from haive.games.framework import GameStateManager

class ChessStateManager(GameStateManager):
    def initialize_state(self):
        # Set up initial board state
        return ChessState(
            board=self.create_initial_board(),
            current_player="white"
        )

    def is_valid_move(self, state, move):
        # Validate move according to chess rules
        piece = state.board[move.from_row][move.from_col]
        # Chess-specific validation logic...
        return is_valid

    def apply_move(self, state, move):
        # Create new state with the move applied
        new_state = state.model_copy(deep=True)
        # Update board with the move...
        return new_state

    def is_game_over(self, state):
        # Check for checkmate, stalemate, etc.
        return is_checkmate or is_stalemate or is_draw
```

#### GameConfig

Configuration class for game parameters and settings.

```python
from haive.games.framework import GameConfig
from pydantic import Field
from typing import List

class ChessConfig(GameConfig):
    time_control: str = Field(default="standard")
    use_opening_book: bool = Field(default=True)
    skill_level: int = Field(default=5, ge=1, le=10)
    player_names: List[str] = Field(default=["White", "Black"])
```

### Multi-Player Extensions

The framework includes specialized components for multi-player games with more complex interactions.

```python
from haive.games.framework.multi_player import MultiPlayerGameState, MultiPlayerGameAgent

class PokerState(MultiPlayerGameState):
    player_hands: dict = Field(default_factory=dict)
    community_cards: list = Field(default_factory=list)
    pot: int = Field(default=0)
    current_phase: str = Field(default="pre-flop")

class PokerAgent(MultiPlayerGameAgent):
    # Specialized logic for multi-player turn management
    def handle_betting_round(self, state):
        # Process each player's betting decisions in order
        for player_id in self.get_active_players(state):
            action = self.get_player_action(state, player_id)
            state = self.state_manager.apply_action(state, action)
        return state
```

## Usage Patterns

### Basic Game Implementation

```python
from haive.games.framework import GameAgent, GameConfig, GameState, GameStateManager
from haive.core.engine.aug_llm import AugLLMConfig, compose_runnable

# 1. Define game-specific models
class TicTacToeState(GameState):
    board: list[list[str]] = Field(default_factory=lambda: [["" for _ in range(3)] for _ in range(3)])
    current_player: str = Field(default="X")

class TicTacToeMove:
    row: int
    col: int

class TicTacToeConfig(GameConfig):
    player_symbols: list[str] = Field(default=["X", "O"])

# 2. Create state manager
class TicTacToeStateManager(GameStateManager):
    def initialize_state(self):
        return TicTacToeState()

    def is_valid_move(self, state, move):
        return (0 <= move.row < 3 and
                0 <= move.col < 3 and
                state.board[move.row][move.col] == "")

    def apply_move(self, state, move):
        new_state = state.model_copy(deep=True)
        new_state.board[move.row][move.col] = state.current_player
        new_state.current_player = "O" if state.current_player == "X" else "X"
        return new_state

    def is_game_over(self, state):
        # Check win conditions...
        return has_winner or is_board_full

# 3. Create game agent
class TicTacToeAgent(GameAgent):
    def __init__(self, config: TicTacToeConfig):
        super().__init__(config)
        self.state_manager = TicTacToeStateManager(config)

        # Create LLM for agent decisions
        llm_config = AugLLMConfig(
            system_message="You are playing Tic Tac Toe. Make the best move.",
            temperature=0.2
        )
        self.llm = compose_runnable(llm_config)

    def run(self):
        state = self.state_manager.initialize_state()

        while not self.state_manager.is_game_over(state):
            move = self.get_agent_move(state)
            if self.state_manager.is_valid_move(state, move):
                state = self.state_manager.apply_move(state, move)

        return state
```

### Turn-Based Game Pattern

```python
from haive.games.framework import GameAgent

class TurnBasedGameAgent(GameAgent):
    def run(self):
        state = self.state_manager.initialize_state()

        while not self.state_manager.is_game_over(state):
            current_player = self.get_current_player(state)

            # Get and validate move
            move = self.get_agent_move(state, current_player)
            if not self.state_manager.is_valid_move(state, move):
                # Handle invalid move (retry, penalize, etc.)
                continue

            # Apply the move
            state = self.state_manager.apply_move(state, move)

            # Log or visualize the turn
            self.log_turn(state, move)

        # Game is over, determine outcome
        result = self.state_manager.get_game_result(state)
        return result
```

### Simultaneous Action Game

```python
from haive.games.framework import GameAgent

class SimultaneousActionAgent(GameAgent):
    def run(self):
        state = self.state_manager.initialize_state()

        while not self.state_manager.is_game_over(state):
            # Collect actions from all players without revealing them
            player_actions = {}
            for player_id in state.players:
                action = self.get_agent_move(state, player_id)
                player_actions[player_id] = action

            # Apply all actions simultaneously
            state = self.state_manager.apply_simultaneous_actions(state, player_actions)

        return state
```

## Integration with Other Modules

### Integration with Engine Module

```python
from haive.games.framework import GameAgent
from haive.core.engine.aug_llm import AugLLMConfig, compose_runnable

class ChessAgent(GameAgent):
    def __init__(self, config):
        super().__init__(config)

        # Create specialized engines for different aspects of gameplay
        self.move_engine = compose_runnable(AugLLMConfig(
            system_message="You are a chess master. Analyze the board and choose the best move.",
            temperature=0.2
        ))

        self.evaluation_engine = compose_runnable(AugLLMConfig(
            system_message="Evaluate the current chess position objectively.",
            temperature=0.1
        ))

    def get_agent_move(self, state, player_id):
        # Use the move engine to generate a move
        board_representation = self.format_board(state.board)

        response = self.move_engine.invoke({
            "board": board_representation,
            "player": player_id,
            "move_history": state.move_history
        })

        return self.parse_move(response)
```

### Integration with Graph Module

```python
from haive.games.framework import GameAgent
from haive.core.graph.state_graph import BaseGraph
from langgraph.graph import START, END

class StrategyGameAgent(GameAgent):
    def __init__(self, config):
        super().__init__(config)

        # Create a graph for complex agent decision making
        self.decision_graph = BaseGraph(name="strategy_decision")

        # Add nodes for the decision process
        self.decision_graph.add_node("analyze_state", self.analyze_state_node)
        self.decision_graph.add_node("generate_options", self.generate_options_node)
        self.decision_graph.add_node("evaluate_options", self.evaluate_options_node)
        self.decision_graph.add_node("select_best_move", self.select_move_node)

        # Connect nodes
        self.decision_graph.add_edge(START, "analyze_state")
        self.decision_graph.add_edge("analyze_state", "generate_options")
        self.decision_graph.add_edge("generate_options", "evaluate_options")
        self.decision_graph.add_edge("evaluate_options", "select_best_move")
        self.decision_graph.add_edge("select_best_move", END)

        # Compile the graph
        self.decision_workflow = self.decision_graph.compile()

    def get_agent_move(self, state, player_id):
        # Use the decision graph to generate a move
        result = self.decision_workflow.invoke({
            "state": state.model_dump(),
            "player_id": player_id
        })

        return result["selected_move"]
```

## Best Practices

- **State Immutability**: Always create new state objects rather than modifying existing ones
- **Validation First**: Validate moves before applying them to prevent invalid states
- **Clean Separation**: Keep game logic (state manager) separate from agent logic
- **Consistent Interfaces**: Maintain consistent interfaces across different game implementations
- **Error Handling**: Implement robust error handling for invalid moves and edge cases
- **Configuration**: Use configuration to control game parameters rather than hardcoding
- **Testing**: Create automated tests for game logic, especially win conditions

## API Reference

For full API details, see the [documentation](https://docs.haive.ai/games/framework).

## Related Modules

- **haive.core.engine**: Provides the LLM engines used by game agents
- **haive.core.graph**: Graph system for complex agent decision workflows
- **haive.games.base**: Legacy framework for backward compatibility
