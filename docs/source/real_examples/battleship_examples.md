# Battleship Agent Examples

Real examples and outputs from the battleship agent.

## battleship_README

**Source**: `packages/haive-games/src/haive/games/battleship/README.md`

# Battleship

Classic naval strategy game with LLM-powered AI agents and advanced targeting strategies.

## Overview

The Battleship module provides a complete implementation of the classic naval combat game, featuring AI agents that use sophisticated targeting strategies, pattern recognition, and tactical reasoning. Built on the Haive framework, it supports configurable fleet compositions and multiple difficulty levels.

**Key Features:**

- **Classic Battleship Rules**: Standard 10x10 grid with traditional ship placement and targeting
- **AI-Powered Players**: LLM-based agents with strategic thinking and pattern recognition
- **Advanced Targeting**: Hunt-and-destroy algorithms with probability-based targeting
- **Flexible Fleet Configuration**: Customizable ship types, sizes, and quantities
- **Strategic Analysis**: Board evaluation, probability mapping, and move suggestions
- **Game Visualization**: Rich terminal display with board states and move history
- **Multi-Provider Support**: Works with Azure, OpenAI, and Anthropic LLM providers

**Naval Strategy Elements:**

- **Ship Placement**: Strategic positioning with clustering and spacing considerations
- **Targeting Patterns**: Systematic search patterns and adaptive strategies
- **Probability Analysis**: Statistical targeting based on remaining ship configurations
- **Hunt Mode**: Focused attacks after scoring hits
- **Pattern Recognition**: Learning from opponent behavior and shot patterns

## Architecture

The battleship implementation follows two-player game architecture:

```
BattleshipAgent
├── Configuration (BattleshipAgentConfig)
├── State Management (BattleshipStateManager)
├── Player Boards (ship placement and targeting grids)
├── LLM Engines (placement, targeting, analysis)
├── Strategy System (hunt/target modes)
└── Workflow (LangGraph-based game flow)
```

### Core Components

- **BattleshipAgent**: Main game controller managing flow and player interactions
- **BattleshipState**: Complete game state

... (truncated)


---

