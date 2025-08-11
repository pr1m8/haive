# Go Agent Examples

Real examples and outputs from the go agent.

## go_README

**Source**: `packages/haive-games/src/haive/games/go/README.md`

# Go

Advanced Go (Weiqi/Baduk) game implementation with LLM-powered AI players and SGF support.

## Overview

The Go module provides a comprehensive implementation of the ancient strategy game Go, featuring AI players that understand complex territorial concepts, strategic patterns, and traditional Go principles. Built on the Haive framework with SGF (Smart Game Format) support for professional game analysis.

**Key Features:**

- **Complete Go Rules**: Full implementation including ko rule, territory scoring, and game ending
- **Multiple Board Sizes**: Support for 9x9, 13x13, and 19x19 boards
- **AI Players**: LLM-based agents that understand Go strategy, joseki patterns, and territorial concepts
- **SGF Integration**: Import/export games in standard SGF format using the sente library
- **Position Analysis**: Deep evaluation of board positions, territory estimation, and move suggestions
- **Professional Features**: Handicap stones, komi, and tournament-style timing
- **Rich Visualization**: Beautiful terminal display with coordinate systems and move history

**Go Concepts Implemented:**

- **Territory Control**: Area scoring with dead stone removal
- **Capture Mechanics**: Stone capture and liberties calculation
- **Ko Rule**: Prevention of immediate board repetition
- **Life and Death**: Basic tsumego (life and death) analysis
- **Strategic Patterns**: Opening principles, middle game fighting, endgame technique

## Architecture

The Go implementation follows traditional game engine architecture with AI enhancements:

```
GoAgent
├── Configuration (GoAgentConfig)
├── Game Engine (sente library integration)
├── State Management (GoGameStateManager)
├── LLM Players (black_player, white_player, analyzer)
├── SGF Support (game import/export)
└── Workflow (LangGraph-based game flow)
```

### Core Components

- **GoAgent**: Main game controller with LangGraph workflow
- **GoGameState**: Complete board state with move history and scoring
- **GoGameStateManager**: Rule en

... (truncated)

---
