# Fox_And_Geese Agent Examples

Real examples and outputs from the fox_and_geese agent.

## fox_and_geese_README

**Source**: `packages/haive-games/src/haive/games/fox_and_geese/README.md`

# Fox and Geese Game

A complete implementation of the classic Fox and Geese board game with rich terminal UI visualization.

## Game Overview

Fox and Geese is a traditional hunt game played on a cross-shaped board where:

- The Fox (🦊) tries to capture enough geese to win
- The Geese (🪿) try to trap the fox so it cannot move
- The fox wins by reducing geese to fewer than 4
- The geese win by trapping the fox with no legal moves

The game is played on a 7x7 board where pieces move along the lines. The fox can move in any direction (diagonal, horizontal, vertical), while geese can only move forward or sideways (not backward). The fox can capture geese by jumping over them into an empty space, similar to checkers.

## Features

- Full game logic for Fox and Geese with standard rules
- Two UI options:
  - Basic UI with clean display of game state
  - Enhanced Rich UI with improved styling and animations
- Support for AI-powered game agents
- Interactive gameplay with move validation
- Automatic detection of legal moves and captures
- End-game detection and winner determination
- Game state analysis capabilities
- Fixed implementation that handles state transitions reliably

## Running the Game

### Fixed Runner (Works with or without API Keys)

Run the game with our fixed state handling that avoids LangGraph streaming issues:

```bash
# Run with default settings
python src/haive/games/fox_and_geese/fixed_runner.py

# Enable debug logging
python src/haive/games/fox_and_geese/fixed_runner.py --debug

# Disable position analysis
python src/haive/games/fox_and_geese/fixed_runner.py --no-analysis

# Adjust speed of moves
python src/haive/games/fox_and_geese/fixed_runner.py --delay 0.5
```

### Standard Runner (Requires LLM API Access)

Run the original game implementation with LangGraph streaming:

```bash
# Run with default settings
python src/haive/games/fox_and_geese/example.py
```

## Components

### Models

- `FoxAndGeesePosition`: Represents a position on the board w

... (truncated)


---

