# Configurable Games System Documentation

## Overview

The configurable games system provides a unified framework for managing game configurations with dynamic LLM selection across all games in haive-games. This system replaces hardcoded LLM configurations with a flexible, runtime-configurable approach.

## Architecture

### Core Components

1. **BaseGameConfig** (`/haive/games/core/config/base.py`)
   - Abstract base class for all game configurations
   - Supports multiple configuration modes
   - Handles engine creation and LLM configuration

2. **PlayerAgentConfig** (`/haive/games/core/agent/player_agent.py`)
   - Configuration for individual player agents
   - Supports LLM specification via strings or config objects
   - Includes temperature, system messages, and player names

3. **Generic Player System** (`/haive/games/core/agent/generic_player_agent.py`)
   - Type-safe player identification system
   - Generic prompt generators
   - Factory pattern for engine creation

4. **LLM Factory** (`/haive/core/models/llm/factory.py`)
   - Creates LLM configurations from canonical strings
   - Supports formats: "gpt-4", "openai:gpt-4", "anthropic:claude-3-opus"
   - Model registry with metadata and aliases

## Configuration Modes

### 1. Legacy Mode

- Uses existing hardcoded engines from `engines.py`
- Backward compatibility for existing code
- Activated with `use_legacy_engines=True`

### 2. Simple Mode (Default)

- Specify models as strings
- Game-specific fields (e.g., `white_model`, `black_model`)
- Automatic engine creation

### 3. Example Mode

- Predefined configurations (e.g., "budget", "gpt_vs_claude")
- Easy switching between common setups
- Activated with `example_config="name"`

### 4. Advanced Mode

- Full PlayerAgentConfig specifications
- Custom prompts and parameters
- Maximum flexibility

## Implementation Pattern

Each game follows this pattern:

1. **Config Class** extends `BaseGameConfig`
2. **Implements Required Methods**:
   - `get_role_definitions()` - Define player roles
   - `get_example_configs()` - Predefined examples
   - `build_legacy_engines()` - Legacy support
   - `create_engines_from_player_configs()` - Engine creation

3. **Game-Specific Fields**:
   - Model fields (e.g., `white_model`, `red_model`)
   - Player names
   - Game settings (e.g., `max_moves`)

## API Integration

The system integrates with haive-dataflow's GameAPI:

1. **Agent Creation**: GameAPI calls `agent_class.get_config_class()`
2. **Configuration**: Passes `config_overrides` to config constructor
3. **State Management**: Uses standard state schemas
4. **WebSocket Support**: Real-time game updates

## File Structure

```
/haive/games/
├── core/
│   ├── config/
│   │   ├── __init__.py
│   │   └── base.py          # BaseGameConfig
│   └── agent/
│       ├── player_agent.py   # PlayerAgentConfig
│       └── generic_player_agent.py  # Generic system
├── chess/
│   ├── config.py            # Unified configuration
│   ├── dynamic_config.py    # Additional helpers
│   └── generic_engines.py   # Generic engine creation
└── [other games...]
```

## Key Benefits

1. **No Hardcoded LLMs** - All models configurable at runtime
2. **Backward Compatible** - Existing code continues to work
3. **Type Safety** - Strong typing with generics
4. **API Ready** - Seamless integration with GameAPI
5. **Flexible** - Multiple configuration modes

## Usage Examples

### Simple Configuration

```python
config = ChessAgentConfig(
    white_model="gpt-4",
    black_model="claude-3-opus"
)
```

### Example Configuration

```python
config = ChessAgentConfig(
    example_config="budget",
    enable_analysis=False
)
```

### Advanced Configuration

```python
player_configs = {
    "white_player": PlayerAgentConfig(
        llm_config="gpt-4",
        temperature=0.7,
        player_name="Aggressive White",
        system_message="Play aggressively..."
    )
}
config = ChessAgentConfig(player_configs=player_configs)
```

## Games Status

### Fully Implemented

- Chess - white/black players
- Connect4 - red/yellow players
- Tic-Tac-Toe - X/O players

### Generic Engines Only

- Battleship, Clue, Debate, Dominoes, Fox and Geese
- Mafia, Mancala, Mastermind, Nim, Poker
- Reversi, Risk

### Not Implemented

- Go (package conflict)
- Among Us (incomplete)
- Hold'em (covered by Poker)
- Monopoly (complex setup)

## Testing

Comprehensive tests in:

- `/haive/games/tests/test_games_functionality.py`
- `/haive/games/tests/test_all_games_end_to_end.py`

Tests verify:

- Import functionality
- Configuration creation
- Engine instantiation
- API compatibility

## Migration Guide

See `MIGRATION_GUIDE.md` for detailed migration instructions from the old system.

## Next Steps

1. Complete configurations for remaining games
2. Add more example configurations
3. Create game-specific documentation
4. Build tournament system
5. Add performance benchmarks
