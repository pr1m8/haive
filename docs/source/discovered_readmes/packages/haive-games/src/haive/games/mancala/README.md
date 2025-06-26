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

```python
from haive.games.mancala.agent import MancalaAgent
from haive.games.mancala.config import MancalaConfig

# Initialize the agent with configuration
config = MancalaConfig(stones_per_pit=4)
agent = MancalaAgent(config)

# Run the game with visualization
final_state = agent.run_game(visualize=True)
```

### Creating a Custom Game

```python
from haive.games.mancala.state import MancalaState
from haive.games.mancala.state_manager import MancalaStateManager
from haive.games.mancala.models import MancalaMove

# Initialize a game state with 5 stones per pit
state = MancalaState.initialize(stones_per_pit=5)

# Print the current board
print(state.board_string)

# Get legal moves for the current player
legal_moves = MancalaStateManager.get_legal_moves(state)
print(f"Legal moves: {legal_moves}")

# Make a move
if legal_moves:
    new_state = MancalaStateManager.apply_move(state, legal_moves[0])
    print(f"New state after move: {new_state}")
```

### Using the Minimal Test Script

You can run the minimal test script to see a demonstration of the game logic:

```bash
python minimal_test.py
```

For an interactive game where you can input moves:

```bash
python minimal_test.py interactive
```

## Technical Implementation

### Board Representation

The board is represented as a list of 14 integers, where each integer is the number of stones in that pit:

```
    12 11 10  9  8  7
13                    6
     0  1  2  3  4  5
```

### Move Representation

Moves are represented by the `MancalaMove` class, which contains:

- `pit_index`: The index of the pit to sow from (0-5)
- `player`: The player making the move ("player1" or "player2")

### Game State

The `MancalaState` class contains:

- `board`: The current board state (list of 14 integers)
- `turn`: The current player's turn ("player1" or "player2")
- `game_status`: Status of the game ("ongoing", "player1_win", "player2_win", "draw")
- `move_history`: History of all moves made
- `free_turn`: Whether the current player gets a free turn
- `winner`: The winner of the game, if any
- Additional fields for analysis and debugging

## Integration with Haive Framework

This module integrates with the Haive framework for agent-based gameplay:

1. The `MancalaAgent` class provides a complete agent for playing the game.
2. LLM engines are configured in `engines.py` for move generation and position analysis.
3. The state management follows the Haive framework patterns for state updates.

## Testing

Run the `minimal_test.py` script to verify that the core game logic is working correctly:

```bash
python minimal_test.py
```

This will run a predetermined sequence of moves and display the game state after each move.
