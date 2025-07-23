# Tic_Tac_Toe Agent Examples

Real examples and outputs from the tic_tac_toe agent.

## tic_tac_toe_README

**Source**: `packages/haive-games/src/haive/games/tic_tac_toe/README.md`

# Tic Tac Toe Game Module

**A comprehensive, strategic Tic Tac Toe implementation with AI analysis, beautiful UI, and perfect play algorithms.**

The Tic Tac Toe module provides a sophisticated implementation of the classic game within the Haive framework, featuring LLM-based strategic reasoning, comprehensive position analysis, and an interactive Rich-based terminal UI. This module demonstrates advanced game AI capabilities while maintaining educational value for understanding strategic decision-making.

## 🎯 Features

### Core Game Engine

- **Complete Tic Tac Toe Rules**: Full implementation with move validation and win detection
- **Strategic AI Analysis**: Deep position evaluation including win/block/fork detection
- **LLM-Based Decision Making**: Advanced reasoning using language models
- **Perfect Play Algorithms**: Minimax implementation with game theory insights
- **Rich Terminal UI**: Beautiful, animated interface with real-time game state display

### Advanced Analysis

- **Winning Move Detection**: Immediate win opportunity identification
- **Blocking Move Analysis**: Critical defensive move computation
- **Fork Opportunities**: Advanced tactics for creating multiple threats
- **Positional Evaluation**: Strategic value assessment (center, corners, edges)
- **Game Theory Integration**: Position classification and outcome prediction

### Developer Features

- **Type-Safe Models**: Comprehensive Pydantic data structures
- **Async Support**: Full asynchronous operation for scalability
- **Configuration System**: Flexible game setup and AI personality adjustment
- **Comprehensive Testing**: Unit tests for all game mechanics
- **Documentation**: Detailed API documentation and examples

## 🚀 Quick Start

### Basic Game

```python
from haive.games.tic_tac_toe import TicTacToeAgent

# Create and run a simple game
agent = TicTacToeAgent()
final_state = agent.run_game(visualize=True)
print(f"Game result: {final_state.get('game_status', 'unknown')}")
```

### Rich 

... (truncated)


---

