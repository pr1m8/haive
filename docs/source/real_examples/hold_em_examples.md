# Hold_Em Agent Examples

Real examples and outputs from the hold_em agent.

## hold_em_README

**Source**: `packages/haive-games/src/haive/games/hold_em/README.md`

# Texas Hold'em Poker Game

A full implementation of Texas Hold'em poker using the Haive framework with LLM-powered players and a rich terminal UI.

## Features

- Complete Texas Hold'em game engine with proper game mechanics
- LLM-powered player agents with distinct playing styles
- Rich terminal UI with card visualization
- Multiple game modes (cash game, tournament, heads-up)
- Hand evaluation and betting logic
- Detailed game state tracking

## Usage

```python
from haive.games.hold_em import HoldemGameAgent, HoldemGameAgentConfig, HoldemRichUI
from haive.games.hold_em.config import create_default_holdem_config

# Create a game configuration
config = create_default_holdem_config(num_players=4, starting_chips=1000)

# Initialize the game agent
agent = HoldemGameAgent(config)

# Start the game with the Rich UI
ui = HoldemRichUI()
ui.run(agent)
```

## Game Modes

The module supports different game modes:

1. **Standard Game**: Regular multi-player game with fixed blinds
2. **Heads-Up**: Two-player format with specialized dynamics
3. **Tournament**: Escalating blinds and elimination format
4. **Cash Game**: Deep stacks and flexible buy-ins

```python
# Create different game configurations
from haive.games.hold_em.config import (
    create_default_holdem_config,
    create_heads_up_config,
    create_tournament_config,
    create_cash_game_config
)

# Standard game
standard_config = create_default_holdem_config(num_players=6)

# Heads-up game
heads_up_config = create_heads_up_config(
    player1_name="Alice",
    player2_name="Bob",
    starting_chips=1000
)

# Tournament
tournament_config = create_tournament_config(
    num_players=8,
    starting_chips=1500
)

# Cash game
cash_config = create_cash_game_config(
    num_players=6,
    big_blind=50,
    max_buy_in=2000
)
```

## Quick Start

The easiest way to start a game is to use the included test script:

```bash
# Run from the root of the package
python -m haive.games.hold_em.test

# Try different game modes
py

... (truncated)


---

