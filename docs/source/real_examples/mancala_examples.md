# Mancala Agent Examples

Real examples and outputs from the mancala agent.

## mancala_README

**Source**: `packages/haive-games/src/haive/games/mancala/README.md`

# Mancala Game Module

This module implements the classic Mancala (Kalah) board game using the Haive framework.

## Game Overview

Mancala is one of the oldest known board games, with evidence of play dating back to ancient Egypt. The version implemented here is known as Kalah, which is popular in the United States and Europe.

### Board Layout

The game board consists of 14 pits:

- 6 pits for Player 1 (bottom row, indices 0-5)
- Player 1's store (right side, index 6)
- 6 pits for Player 2 (top row, indices 7-12)
- Player 2's store (left side, index 13)

### Rules

1. **Setup**: At the start of the game, each of the 12 playing pits contains a set number of stones (default is 4).
2. **Objective**: The goal is to collect more stones in your store than your opponent by the end of the game.
3. **Turns**:
   - On your turn, select one of your pits that contains stones.
   - All stones from that pit are distributed counterclockwise, one stone per pit.
   - Your opponent's store is skipped during distribution.
4. **Special Rules**:
   - **Free Turn**: If your last stone lands in your store, you get another turn.
   - **Capture**: If your last stone lands in an empty pit on your side, you capture that stone and all stones in the opposite pit.
5. **Game End**: The game ends when all pits on one side are empty. Any remaining stones on the other side go to that player's store.

## Module Structure

- `models.py`: Data models for the game (MancalaMove, MancalaAnalysis)
- `state.py`: Game state representation (MancalaState)
- `state_manager.py`: Logic for applying moves and managing game state (MancalaStateManager)
- `agent.py`: Agent for playing the game with LLMs (MancalaAgent)
- `config.py`: Configuration for the game agent (MancalaConfig)
- `engines.py`: LLM engines for move generation and analysis
- `example.py`: Example script showing how to run a game
- `minimal_test.py`: Standalone test script for the game logic

## Usage Examples

### Running the Example Game

```pytho

... (truncated)


---

```
