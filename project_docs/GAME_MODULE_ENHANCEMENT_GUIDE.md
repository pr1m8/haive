# Game Module Enhancement Guide

A systematic approach to enhancing game modules in the Haive framework, following CLAUDE.md principles.

## Overview

This guide provides a repeatable process for enhancing game modules with comprehensive documentation, examples, and improved code organization. Each game module should follow this standardized enhancement pattern.

## Enhancement Process

### Step 1: Initial Assessment

1. **Check existing files**:
   ```bash
   ls -la packages/haive-games/src/haive/games/{game_name}/
   ```

2. **Identify what exists**:
   - [ ] README.md
   - [ ] example.py
   - [ ] __init__.py
   - [ ] agent.py
   - [ ] state.py
   - [ ] config.py
   - [ ] models.py
   - [ ] state_manager.py

3. **Read existing documentation**:
   - Review current README content
   - Check docstring quality
   - Note missing sections

### Step 2: README Enhancement Pattern

Each game README should follow this structure:

```markdown
# {Game Name}

{One-line description of the game}

## Overview

{2-3 paragraphs explaining:
- What the game is
- Key mechanics and rules
- Why it's interesting for AI agents
- Unique challenges or features}

## Architecture

```
{GameName}Agent (extends GameAgent)
├── State Management
│   ├── {GameName}State
│   ├── Move Validation
│   └── Win Condition Detection
├── Player Configuration
│   ├── Agent Engines
│   ├── Strategies
│   └── Skill Levels
├── Game Flow
│   ├── Turn Management
│   ├── Phase Transitions
│   └── Time Control
└── Visualization
    ├── Board/State Display
    ├── Move History
    └── Analysis Output
```

## Key Features

- **{Feature 1}** - {Description}
- **{Feature 2}** - {Description}
- **{Feature 3}** - {Description}
{Add 5-8 key features}

## Installation

```bash
pip install haive-games
```

## Quick Start

### Basic Game

```python
from haive.games.{game_name} import {GameName}Agent, {GameName}Config

# Simple setup
config = {GameName}Config(
    player_names=["Player1", "Player2"],
    difficulty="medium"
)

agent = {GameName}Agent(config)
result = agent.run()

print(f"Winner: {result.winner}")
```

### Advanced Configuration

```python
{More complex configuration example}
```

## Game Rules

### Objective
{Clear statement of how to win}

### Setup
{Initial game state}

### Gameplay
{Turn structure and allowed actions}

### Special Rules
{Any unique mechanics}

### Winning Conditions
{All ways the game can end}

## State Management

The game state is managed through the `{GameName}State` class:

```python
class {GameName}State(GameState):
    # State fields
    {field1}: {Type} = Field(...)
    {field2}: {Type} = Field(...)
    
    # Computed properties
    @property
    def {property_name}(self) -> {Type}:
        return {computation}
```

### State Fields

| Field | Type | Description |
|-------|------|-------------|
| `{field1}` | `{Type}` | {Description} |
| `{field2}` | `{Type}` | {Description} |

## Configuration Options

### Basic Parameters

```python
{GameName}Config(
    {param1}={default},  # {Description}
    {param2}={default},  # {Description}
)
```

### Advanced Parameters

{Table or detailed list of all configuration options}

## Strategy Guide

### For AI Agents

1. **{Strategy 1}**
   - {Details}
   - {Example}

2. **{Strategy 2}**
   - {Details}
   - {Example}

### Common Patterns

```python
{Code example showing common game patterns}
```

## Advanced Usage

### Custom Agent Implementation

```python
{Example of extending the base agent}
```

### Tournament Play

```python
{Example of running tournaments}
```

### Analysis Tools

```python
{Example of game analysis}
```

## Integration Examples

### With Custom Engines

```python
{Integration example}
```

### With Observers

```python
{Observer pattern example}
```

## Performance Considerations

- **State Size**: {Considerations}
- **Move Generation**: {Considerations}
- **Memory Usage**: {Considerations}
- **Computation Time**: {Considerations}

## Troubleshooting

### Common Issues

#### {Issue 1}
**Problem**: {Description}
**Solution**: {Solution with code}

#### {Issue 2}
**Problem**: {Description}
**Solution**: {Solution with code}

## Examples

For comprehensive examples, see [example.py](example.py) which demonstrates:
- Basic gameplay
- Advanced strategies
- Tournament setup
- Custom implementations
- Analysis tools

## API Reference

### Classes

| Class | Description |
|-------|-------------|
| `{GameName}Agent` | Main game agent |
| `{GameName}State` | Game state representation |
| `{GameName}Config` | Configuration parameters |
| `{GameName}StateManager` | Game logic handler |

### Key Methods

| Method | Description |
|--------|-------------|
| `agent.run()` | Run complete game |
| `manager.is_valid_move()` | Validate move |
| `state.get_legal_moves()` | Get available moves |

## Related Modules

- [Game Framework](../framework/README.md) - Base framework
- [{Similar Game}](../{similar_game}/README.md) - Similar mechanics
```

### Step 3: Example.py Enhancement Pattern

Each example.py should include:

```python
#!/usr/bin/env python3
"""
{Game Name} Examples

Comprehensive examples demonstrating gameplay, strategies, and advanced usage.
"""

def example_basic_game():
    """Example 1: Basic game setup and execution."""
    # Basic game with default settings
    pass

def example_advanced_configuration():
    """Example 2: Advanced configuration options."""
    # Demonstrate all config parameters
    pass

def example_custom_strategies():
    """Example 3: Different AI strategies."""
    # Show various playing styles
    pass

def example_tournament():
    """Example 4: Tournament organization."""
    # Multi-game tournament
    pass

def example_game_analysis():
    """Example 5: Post-game analysis."""
    # Analyze completed games
    pass

def example_custom_agent():
    """Example 6: Custom agent implementation."""
    # Extend base agent
    pass

def example_visualization():
    """Example 7: Game visualization."""
    # Display game state
    pass

def example_integration():
    """Example 8: Integration with other systems."""
    # External tool integration
    pass

def main():
    """Run all examples."""
    examples = [
        example_basic_game,
        example_advanced_configuration,
        example_custom_strategies,
        example_tournament,
        example_game_analysis,
        example_custom_agent,
        example_visualization,
        example_integration
    ]
    
    for example in examples:
        example()
        input("\nPress Enter for next example...")

if __name__ == "__main__":
    main()
```

### Step 4: Code Organization (__init__.py)

Enhance __init__.py with proper exports and type hints:

```python
"""
{Game Name} - {Brief description}

This module implements {game name} for the Haive games framework.
"""

from typing import TYPE_CHECKING

# Version
__version__ = "1.0.0"

# Core imports
from haive.games.{game_name}.agent import {GameName}Agent
from haive.games.{game_name}.config import {GameName}Config
from haive.games.{game_name}.state import {GameName}State

# Conditional imports for type checking
if TYPE_CHECKING:
    from haive.games.{game_name}.models import {GameName}Move
    from haive.games.{game_name}.state_manager import {GameName}StateManager

# Public API
__all__ = [
    "{GameName}Agent",
    "{GameName}Config", 
    "{GameName}State",
    "create_{game_name}_game",
]

# Convenience functions
def create_{game_name}_game(**kwargs) -> {GameName}Agent:
    """Create a {game name} game with the given configuration."""
    config = {GameName}Config(**kwargs)
    return {GameName}Agent(config)
```

### Step 5: Type Hints and Validation

Ensure all modules have proper type hints:

1. **Import typing modules**:
   ```python
   from typing import List, Dict, Optional, Tuple, Union, Any
   from typing import TYPE_CHECKING, TypeAlias
   ```

2. **Add type aliases**:
   ```python
   BoardType: TypeAlias = List[List[Optional[str]]]
   MoveType: TypeAlias = Tuple[int, int]
   ```

3. **Add validators**:
   ```python
   from pydantic import validator, Field
   
   @validator("move")
   def validate_move(cls, v):
       # Validation logic
       return v
   ```

### Step 6: Testing Structure

Create consistent test patterns:

```python
# tests/test_{game_name}/test_game_logic.py
import pytest
from haive.games.{game_name} import {GameName}State, {GameName}StateManager

class Test{GameName}Logic:
    def test_initial_state(self):
        """Test initial game setup."""
        pass
    
    def test_valid_moves(self):
        """Test move validation."""
        pass
    
    def test_win_conditions(self):
        """Test all win scenarios."""
        pass
```

## Quality Checklist

For each game module, ensure:

### Documentation
- [ ] README.md follows template (400+ lines)
- [ ] example.py has 6-8 comprehensive examples
- [ ] All classes have docstrings
- [ ] All public methods have docstrings
- [ ] Complex logic has inline comments

### Code Quality
- [ ] Type hints on all functions
- [ ] Proper error handling
- [ ] Input validation
- [ ] Consistent naming
- [ ] No code duplication

### Features
- [ ] Complete game rules implemented
- [ ] All win conditions handled
- [ ] Move validation works
- [ ] State serialization works
- [ ] Visualization included

### Testing
- [ ] Unit tests for game logic
- [ ] Integration tests for full games
- [ ] Edge cases covered
- [ ] Performance tests if needed

## Automation Script

Use this script to check module completeness:

```python
#!/usr/bin/env python3
"""Check game module completeness."""

import os
from pathlib import Path

def check_game_module(game_path: Path):
    """Check if game module has all required files."""
    required_files = [
        "README.md",
        "example.py",
        "__init__.py",
        "agent.py",
        "config.py",
        "state.py",
        "models.py",
        "state_manager.py"
    ]
    
    missing = []
    for file in required_files:
        if not (game_path / file).exists():
            missing.append(file)
    
    # Check file sizes
    if (game_path / "README.md").exists():
        readme_size = (game_path / "README.md").stat().st_size
        if readme_size < 10000:  # Less than ~400 lines
            print(f"  ⚠️  README.md seems too short ({readme_size} bytes)")
    
    return missing

def main():
    games_dir = Path("packages/haive-games/src/haive/games")
    
    for game_dir in games_dir.iterdir():
        if game_dir.is_dir() and not game_dir.name.startswith("_"):
            print(f"\n📁 {game_dir.name}")
            missing = check_game_module(game_dir)
            if missing:
                print(f"  ❌ Missing: {', '.join(missing)}")
            else:
                print(f"  ✅ All files present")

if __name__ == "__main__":
    main()
```

## Order of Enhancement

Prioritize games by:

1. **Popularity**: Chess, Poker, Tic-Tac-Toe
2. **Complexity**: Simple games first for template refinement
3. **Uniqueness**: Games with special mechanics
4. **Dependencies**: Base games before variants

Suggested order:
1. Tic-Tac-Toe (simple, complete example)
2. Connect4 (grid-based)
3. Chess (complex, important)
4. Poker (multi-player, hidden info)
5. Monopoly (economic, complex state)
6. Wordle (single-player)
7. Among Us (social deduction)
8. Others alphabetically

## Time Management

Allocate time per game:
- Simple games (Tic-Tac-Toe, Nim): 30-45 minutes
- Medium games (Connect4, Checkers): 45-60 minutes
- Complex games (Chess, Poker, Monopoly): 60-90 minutes

## Version Control

Commit after each game:
```bash
git add packages/haive-games/src/haive/games/{game_name}/
git commit -m "feat: Enhance {game_name} module with comprehensive docs and examples"
```

## Validation

After enhancement, verify:
1. Run example.py successfully
2. README renders correctly
3. All imports work
4. No type checking errors
5. Tests still pass

This systematic approach ensures consistency and quality across all game modules while adhering to CLAUDE.md principles.