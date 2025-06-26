# Haive Game Development Guide

## Table of Contents

1. [Introduction](#introduction)
2. [Game Architecture](#game-architecture)
   - [Framework Overview](#framework-overview)
   - [Core Components](#core-components)
   - [Module Structure](#module-structure)
3. [Designing a New Game](#designing-a-new-game)
   - [Game Specification](#game-specification)
   - [State Design](#state-design)
   - [Agent Interface](#agent-interface)
   - [AI Integration](#ai-integration)
4. [Implementation Process](#implementation-process)
   - [Project Setup](#project-setup)
   - [Core Game Logic](#core-game-logic)
   - [LLM Integration](#llm-integration)
   - [Testing Strategy](#testing-strategy)
5. [Debugging Techniques](#debugging-techniques)
   - [State Visualization](#state-visualization)
   - [Agent Behavior Analysis](#agent-behavior-analysis)
   - [Common Issues](#common-issues)
   - [Debugging Tools](#debugging-tools)
6. [Performance Optimization](#performance-optimization)
   - [State Management](#state-management)
   - [LLM Prompt Optimization](#llm-prompt-optimization)
   - [Caching Strategies](#caching-strategies)
7. [Documentation Standards](#documentation-standards)
   - [Code Documentation](#code-documentation)
   - [Game Documentation](#game-documentation)
   - [Example Usage](#example-usage)
8. [Best Practices](#best-practices)
   - [Design Patterns](#design-patterns)
   - [Code Organization](#code-organization)
   - [Testing Approach](#testing-approach)
9. [Advanced Topics](#advanced-topics)
   - [Multi-Agent Games](#multi-agent-games)
   - [Tournament Systems](#tournament-systems)
   - [Analysis Tools](#analysis-tools)
10. [Game Types Reference](#game-types-reference)
    - [Board Games](#board-games)
    - [Card Games](#card-games)
    - [Social Deduction Games](#social-deduction-games)
    - [Custom Game Types](#custom-game-types)

## Introduction

This guide provides comprehensive instructions for developing, debugging, and optimizing games using the Haive framework. The Haive games module is designed to enable the creation of sophisticated AI agent games with a focus on strategic reasoning, social dynamics, and emergent behaviors.

Our framework supports a wide variety of game types from classic board games like Chess and Go to social deduction games like Among Us and Mafia. By following this guide, you'll learn how to efficiently design, implement, and debug your own games within the Haive ecosystem.

## Game Architecture

### Framework Overview

The Haive games framework is built on several key principles:

- **State-Based Design**: Games are represented as a series of state transitions
- **Immutable States**: Each game state is immutable, with actions creating new states
- **Agent-Centric**: Games are driven by agent decisions and actions
- **LLM Integration**: Agents use Large Language Models for strategic reasoning
- **Composable Components**: Reusable components across different games

The framework follows this general flow:

1. Initialize game state
2. Agents observe the state and make decisions
3. Actions are validated and applied to create a new state
4. Repeat until game completion
5. Determine outcome and provide analysis

### Core Components

Every game in the Haive framework consists of these core components:

- **GameState**: Represents the complete game state at a point in time
- **GameStateManager**: Handles state transitions, rule enforcement, and game flow
- **GameConfig**: Configuration for game parameters and settings
- **GameAgent**: Orchestrates the game execution and agent interactions
- **LLM Integration**: Connects game state to language models for decision-making

### Module Structure

A typical game module follows this structure:

```
haive/games/<game_name>/
├── README.md                # Game documentation
├── __init__.py              # Module exports and version
├── agent.py                 # Game agent implementation
├── config.py                # Game configuration
├── state.py                 # Game state representation
├── state_manager.py         # State transition logic
├── models.py                # Data models and types
├── engines.py               # LLM configurations
├── prompts.py               # Prompt templates
├── ui/                      # Visualization components
│   ├── __init__.py
│   └── visualizer.py
└── analysis/                # Game analysis tools
    ├── __init__.py
    └── analyzer.py
```

## Designing a New Game

### Game Specification

Before implementation, create a comprehensive game specification:

1. **Game Overview**:
   - Basic description and objectives
   - Player count and roles
   - Win conditions

2. **Game Mechanics**:
   - Turn structure
   - Available actions
   - Rules and constraints
   - Special conditions

3. **State Representation**:
   - Core state components
   - Visibility rules (what each agent can observe)
   - State transitions

4. **Agent Interface**:
   - Decision points
   - Information available to agents
   - Action format

### State Design

The game state is the most critical component of your implementation:

1. **Define clear state boundaries**: What is and isn't part of the game state
2. **Use Pydantic models**: Leverage type validation for robustness
3. **Consider partial observability**: What information is available to each agent
4. **Plan for serialization**: Ensure the state can be serialized/deserialized
5. **Keep states immutable**: Never modify a state in-place

Example state design:

```python
from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from haive.games.framework import GameState

class ChessState(GameState):
    board: List[List[str]] = Field(...)
    current_player: str = Field(...)
    move_history: List[str] = Field(default_factory=list)
    castling_rights: Dict[str, bool] = Field(default_factory=dict)
    en_passant_target: Optional[str] = Field(default=None)
    halfmove_clock: int = Field(default=0)
    fullmove_number: int = Field(default=1)

    def get_player_view(self, player_id: str) -> "ChessState":
        """Return the state as viewed by the specified player."""
        # In chess, all information is public
        return self
```

### Agent Interface

Design a clear interface for agent decisions:

1. **Define decision points**: When agents need to make decisions
2. **Specify input format**: What information agents receive
3. **Specify output format**: How agent decisions are represented
4. **Handle invalid decisions**: How to respond when agents make invalid moves

Example agent interface:

```python
def get_agent_move(self, state: ChessState, player_id: str) -> ChessMove:
    """Get a move decision from the agent.

    Args:
        state: Current game state
        player_id: ID of the player making the decision

    Returns:
        A chess move decision
    """
    # Format the observation for the agent
    observation = self.format_observation(state, player_id)

    # Get decision from LLM
    response = self.llm.invoke(observation)

    # Parse the response into a move
    move = self.parse_move(response)

    return move
```

### AI Integration

Plan how your game will integrate with LLMs:

1. **Prompt engineering**: Design prompts that provide necessary context
2. **Output parsing**: Define how to parse LLM outputs into valid moves
3. **Context management**: Handle token limits and relevant information
4. **Temperature control**: Adjust based on desired agent behavior
5. **System messages**: Define appropriate agent personas and instructions

## Implementation Process

### Project Setup

1. **Create the module structure**:

   ```bash
   mkdir -p haive/games/your_game_name
   touch haive/games/your_game_name/__init__.py
   touch haive/games/your_game_name/README.md
   ```

2. **Start with the configuration**:

   ```python
   # config.py
   from pydantic import BaseModel, Field
   from haive.games.framework import GameConfig

   class YourGameConfig(GameConfig):
       # Game-specific configuration parameters
       player_count: int = Field(default=2)
       # More parameters...
   ```

3. **Define the game state**:

   ```python
   # state.py
   from pydantic import BaseModel, Field
   from haive.games.framework import GameState

   class YourGameState(GameState):
       # Game-specific state attributes
       # ...
   ```

4. **Implement the state manager**:

   ```python
   # state_manager.py
   from haive.games.framework import GameStateManager

   class YourGameStateManager(GameStateManager):
       def initialize_state(self):
           # Create initial state

       def is_valid_move(self, state, move):
           # Validate moves

       def apply_move(self, state, move):
           # Apply move to create new state

       def is_game_over(self, state):
           # Check for game completion
   ```

5. **Create the game agent**:

   ```python
   # agent.py
   from haive.games.framework import GameAgent

   class YourGameAgent(GameAgent):
       def __init__(self, config):
           super().__init__(config)
           self.state_manager = YourGameStateManager(config)

       def run(self):
           # Main game loop

       def get_agent_move(self, state, player_id):
           # Get move from agent
   ```

### Core Game Logic

Implement these critical components:

1. **State initialization**: Create the starting game state
2. **Move validation**: Verify that moves follow game rules
3. **State transitions**: Apply moves to create new states
4. **Win conditions**: Determine when the game is over and who won
5. **Player observations**: What each player can see

### LLM Integration

Integrate language models effectively:

1. **Create engine configurations**:

   ```python
   # engines.py
   from haive.core.engine.aug_llm import AugLLMConfig

   game_llm_config = AugLLMConfig(
       system_message="You are playing [game]. [Instructions...]",
       temperature=0.4
   )
   ```

2. **Design prompt templates**:

   ```python
   # prompts.py

   MOVE_PROMPT_TEMPLATE = """
   Current game state:
   {board_representation}

   You are playing as {player}

   Your previous moves: {move_history}

   What is your next move? Respond with a valid move in the format: [move format]
   """
   ```

3. **Implement response parsing**:
   ```python
   def parse_move(self, response: str) -> Move:
       """Parse LLM response into a valid move."""
       # Implementation depends on your game's move format
   ```

### Testing Strategy

Develop a comprehensive testing approach:

1. **Unit tests**: Test individual components (state transitions, validation)
2. **Integration tests**: Test full game execution
3. **Edge case tests**: Verify handling of unusual situations
4. **Self-play tests**: Have agents play against themselves
5. **Regression tests**: Ensure fixes don't break existing functionality

## Debugging Techniques

### State Visualization

Create visualizations to understand game state:

1. **Text representations**: ASCII/Unicode board representations
2. **HTML/SVG output**: Generate visual diagrams
3. **Animation**: Show state transitions over time
4. **Interactive debugging**: Allow stepping through game states

Example state visualizer:

```python
def visualize_board(state: ChessState) -> str:
    """Generate a text representation of the chess board."""
    board_str = ""
    for row in state.board:
        board_str += "|" + "|".join(piece or " " for piece in row) + "|\n"
    return board_str
```

### Agent Behavior Analysis

Analyze agent decision-making:

1. **Capture reasoning**: Store agent explanations
2. **Decision points**: Identify critical decisions
3. **Comparative analysis**: Compare different agent strategies
4. **Pattern recognition**: Identify recurring behaviors

Example agent analysis:

```python
def analyze_agent_decisions(game_result):
    """Analyze key decisions made during the game."""
    critical_moves = []

    for i, state in enumerate(game_result.state_history):
        if is_critical_position(state):
            move = game_result.move_history[i]
            reasoning = game_result.reasoning_history[i]
            critical_moves.append({
                "move_number": i,
                "position": state,
                "move": move,
                "reasoning": reasoning,
                "evaluation": evaluate_move(state, move)
            })

    return critical_moves
```

### Common Issues

Watch for these common game development problems:

1. **State mutation bugs**: Accidentally modifying immutable states
2. **Validation gaps**: Missing validation for certain edge cases
3. **Infinite loops**: Games that never reach completion
4. **Prompt issues**: Unclear or inconsistent agent instructions
5. **Context window overflow**: Too much information for the LLM
6. **Parsing errors**: Failure to correctly parse agent responses
7. **Random seed issues**: Non-deterministic behavior affecting reproducibility

### Debugging Tools

Utilize these debugging approaches:

1. **State history recording**: Save all states for post-game analysis
2. **Detailed logging**: Log key events and decisions
3. **Step-by-step execution**: Run games with pauses between steps
4. **State comparison**: Compare states before and after actions
5. **Prompt inspection**: Examine prompts sent to the LLM
6. **Response analysis**: Analyze raw LLM responses

Example debugging setup:

```python
def debug_game_execution(config, debug_options=None):
    """Run a game with debugging enabled."""
    if debug_options is None:
        debug_options = {
            "save_states": True,
            "save_prompts": True,
            "save_responses": True,
            "step_by_step": False,
            "verbose_logging": True
        }

    agent = YourGameAgent(config)
    agent.enable_debugging(debug_options)
    result = agent.run()

    # Save debug information
    if debug_options["save_states"]:
        with open("debug/states.json", "w") as f:
            json.dump([state.model_dump() for state in result.state_history], f)

    return result
```

## Performance Optimization

### State Management

Optimize state handling:

1. **Minimize state size**: Include only necessary information
2. **Use efficient data structures**: Choose appropriate structures for operations
3. **Lazy evaluation**: Calculate derived properties only when needed
4. **State caching**: Cache derived or computed properties
5. **Avoid deep copying**: Use copy-on-write patterns

### LLM Prompt Optimization

Optimize LLM interactions:

1. **Minimize prompt size**: Include only relevant information
2. **Structured prompts**: Organize information for easy comprehension
3. **Few-shot examples**: Include examples for consistent outputs
4. **Clear instructions**: Specify exact response format expected
5. **Token optimization**: Reduce unnecessary tokens

### Caching Strategies

Implement caching for performance:

1. **Prompt caching**: Cache prompts for similar states
2. **Response caching**: Cache LLM responses for repeated scenarios
3. **State cache**: Cache computed state properties
4. **Evaluation cache**: Cache position evaluations

Example caching implementation:

```python
class CachedStateManager(YourGameStateManager):
    def __init__(self, config):
        super().__init__(config)
        self.state_cache = {}
        self.eval_cache = {}

    def get_legal_moves(self, state):
        """Get legal moves with caching."""
        state_key = self.get_state_key(state)
        if state_key in self.state_cache:
            return self.state_cache[state_key]

        legal_moves = super().get_legal_moves(state)
        self.state_cache[state_key] = legal_moves
        return legal_moves

    def get_state_key(self, state):
        """Generate a unique key for the state."""
        # Implementation depends on your state structure
```

## Documentation Standards

### Code Documentation

Follow these documentation standards:

1. **Use Google-style docstrings**:

   ```python
   def function_name(param1: type, param2: type) -> return_type:
       """Short description of function.

       More detailed description explaining the function,
       its behavior, and any special cases.

       Args:
           param1: Description of param1
           param2: Description of param2

       Returns:
           Description of return value

       Raises:
           ExceptionType: Description of when this exception is raised

       Examples:
           >>> function_name(1, 'test')
           'result'
       """
   ```

2. **Document all public classes and functions**
3. **Include examples in docstrings**
4. **Use type hints consistently**
5. **Add module-level docstrings**

### Game Documentation

Create comprehensive game documentation:

1. **README.md**: Overview, features, installation, quick start
2. **Game rules**: Complete explanation of game mechanics
3. **API reference**: Detailed reference for all components
4. **Configuration options**: All available configuration parameters
5. **Examples**: Clear usage examples

### Example Usage

Provide complete examples:

1. **Basic usage**: Simple game execution
2. **Configuration**: How to customize the game
3. **Agent customization**: How to create custom agents
4. **Analysis**: How to analyze game results
5. **Integration**: How to integrate with other modules

## Best Practices

### Design Patterns

Apply these design patterns:

1. **Factory Pattern**: For creating game components
2. **Strategy Pattern**: For different agent strategies
3. **Observer Pattern**: For game event handling
4. **Command Pattern**: For handling game actions
5. **State Pattern**: For managing game phases

### Code Organization

Organize your code effectively:

1. **Separate concerns**: State, logic, configuration, agent interfaces
2. **Use consistent naming**: Follow framework conventions
3. **Modularize code**: Break down complex functionality
4. **Follow package structure**: Use the standard structure
5. **Keep interfaces clean**: Clear and consistent interfaces

### Testing Approach

Implement a thorough testing strategy:

1. **Test-driven development**: Write tests before implementation
2. **Unit tests for core logic**: State transitions, validations
3. **Integration tests**: Full game execution
4. **Parameterized tests**: Test with different configurations
5. **Regression tests**: Ensure fixes don't break existing functionality

## Advanced Topics

### Multi-Agent Games

Considerations for games with multiple agents:

1. **Agent interaction**: How agents communicate and interact
2. **Information asymmetry**: Different information for different agents
3. **Coordination mechanisms**: How agents coordinate actions
4. **Social dynamics**: Social deduction, cooperation, competition
5. **Team structures**: Teams, alliances, rivalries

### Tournament Systems

Implementing tournament systems:

1. **Tournament formats**: Round-robin, Swiss, knockout
2. **Scoring systems**: Win/loss/draw, points systems
3. **Matchmaking**: How to pair agents
4. **Analysis**: Performance statistics and insights
5. **Leaderboards**: Tracking agent performance

### Analysis Tools

Developing game analysis tools:

1. **Move analysis**: Evaluate individual moves
2. **Strategy identification**: Recognize strategic patterns
3. **Skill measurement**: Assess agent skill levels
4. **Decision point analysis**: Identify critical decisions
5. **Comparative analysis**: Compare different agents or strategies

## Game Types Reference

### Board Games

Considerations for board games:

1. **Board representation**: Grid, graph, coordinate system
2. **Piece movement**: Movement rules and constraints
3. **Capture mechanics**: How pieces interact
4. **Special moves**: Unique movement or action rules
5. **State evaluation**: Position assessment

### Card Games

Considerations for card games:

1. **Deck management**: Shuffling, drawing, discard pile
2. **Hand representation**: Cards held by players
3. **Card visibility**: Face-up, face-down, hidden information
4. **Combinations**: Card combinations and their values
5. **Bidding/betting**: Wagering mechanisms

### Social Deduction Games

Considerations for social deduction games:

1. **Hidden roles**: Secret player assignments
2. **Information revelation**: How information becomes known
3. **Discussion mechanics**: Player communication
4. **Deception mechanics**: Lying, bluffing, misdirection
5. **Voting systems**: Collective decision making

### Custom Game Types

Creating custom game types:

1. **Define core mechanics**: What makes your game unique
2. **Establish state representation**: How to represent game state
3. **Design agent interface**: How agents interact with the game
4. **Create evaluation metrics**: How to assess game outcomes
5. **Develop analysis tools**: How to analyze game dynamics
