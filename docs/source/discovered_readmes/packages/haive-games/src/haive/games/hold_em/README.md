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
python -m haive.games.hold_em.test heads-up
python -m haive.games.hold_em.test tournament
python -m haive.games.hold_em.test cash

# Custom configuration
python -m haive.games.hold_em.test custom --players 6 --chips 2000 --bb 50
```

## Player Styles

Players can be configured with different playing styles:

- **Tight**: Conservative, plays few hands but aggressively
- **Loose**: Plays many hands, more willing to take risks
- **Aggressive**: Bets and raises frequently
- **Passive**: Prefers calling to raising
- **Balanced**: Adapts strategy based on situation
- **Tricky**: Uses deception and unexpected plays

## Architecture

The module is organized into the following components:

- `game_agent.py`: Main game management agent
- `player_agent.py`: Player decision-making agent
- `state.py`: Game state models and logic
- `models.py`: Data models for game entities
- `config.py`: Configuration utilities
- `engines.py`: LLM engine definitions
- `utils.py`: Poker utilities
- `ui.py`: Rich terminal UI components
- `engine_logging.py`: Enhanced logging utilities

## Customization

You can create fully customized games by modifying:

1. Player count, styles, and characteristics
2. Starting chips and blind levels
3. Engine prompts and models
4. UI elements and visualization

```python
from haive.games.hold_em import (
    HoldemGameAgentConfig,
    HoldemPlayerAgentConfig,
    HoldemGameAgent
)

# Create custom player configs
player_configs = []
for i, (name, style) in enumerate([
    ("Alice", "tight"),
    ("Bob", "loose"),
    ("Charlie", "aggressive"),
    ("Diana", "balanced")
]):
    player_config = HoldemPlayerAgentConfig(
        name=f"player_{name.lower()}",
        player_name=name,
        player_style=style,
        risk_tolerance=0.3 + (i * 0.1),  # Vary risk tolerance
    )
    player_configs.append(player_config)

# Create custom game config
game_config = HoldemGameAgentConfig(
    name="custom_holdem_game",
    max_players=len(player_configs),
    small_blind=10,
    big_blind=20,
    starting_chips=1000,
    max_hands=50,
    player_configs=player_configs,
)

# Create and run the game
agent = HoldemGameAgent(game_config)
```
