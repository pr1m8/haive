# Chess Agent Examples

Real examples and outputs from the chess agent.

## chess_README

**Source**: `packages/haive-games/src/haive/games/chess/README.md`

# Haive Games: Chess Module

## Overview

The Chess module provides a comprehensive implementation of chess for AI agents. It features complete game state representation, move validation, algebraic notation parsing, and strategic decision-making through LLM-based agents. This module enables AI agents to play chess with sophisticated reasoning about position evaluation, tactics, and long-term strategy.

## Key Features

- **Complete Chess Rules**: Full implementation of chess rules including special moves (castling, en passant, promotion)
- **Algebraic Notation**: Support for standard chess notation for move input/output
- **Position Evaluation**: Sophisticated position analysis through LLM reasoning
- **State Management**: Comprehensive game state tracking with move history
- **Move Validation**: Thorough legal move validation and generation
- **Visualization**: ASCII and Unicode board representations
- **Game Analysis**: Post-game analysis of critical positions
- **Opening Book**: Optional integration with chess opening theory

## Installation

This module is part of the `haive-games` package. Install the full package with:

```bash
pip install haive-games
```

## Quick Start

```python
from haive.games.chess import ChessAgent, ChessConfig
from haive.core.engine.aug_llm import AugLLMConfig

# Configure the game
config = ChessConfig(
    player_names=["White", "Black"],
    time_control="rapid",  # Options: blitz, rapid, classical
    llm_config=AugLLMConfig(
        system_message="You are playing chess. Analyze the position carefully and make the best move.",
        temperature=0.2  # Lower temperature for more consistent play
    )
)

# Create and run the game
agent = ChessAgent(config)
result = agent.run()

# View results
print(f"Game result: {result.outcome}")
print(f"Move history: {result.move_history}")
```

## Components

### ChessAgent

Main agent class that orchestrates the chess game.

```python
from haive.games.chess import ChessAgent, ChessConfig

# Cr

... (truncated)


---

```
