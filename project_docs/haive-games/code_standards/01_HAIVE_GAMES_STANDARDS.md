# 01 - Haive Games Package: Code Standards & Memory Guide

**Reference**: [CODING_STYLE_GUIDE.md](../../CODING_STYLE_GUIDE.md)  
**Parent**: [Haive Games README.md](../README.md)  
**Memory Guide**: [CLAUDE_DOCUMENTATION/README.md](../../claude_documentation/README.md)

## 1. Package-Specific Standards

### 1.1 Core Requirements (From Global Standards)

**Base Standards**: [CODING_STYLE_GUIDE.md](../../CODING_STYLE_GUIDE.md)

**Haive Games Specific Applications**:

1. **No Print Statements** → Game logging only via `logger.debug()`, `logger.warning()`, `logger.error()`
2. **Game State Immutability** → Use `state.model_copy()` for state transitions
3. **Enum Usage** → All game constants as enums (ShipType, GamePhase, MoveResult)
4. **Pydantic Validation** → All models use proper validation and `field(default_factory=...)`

### 1.2 Package Architecture Standards

```
haive-games/src/haive/games/{game_name}/
├── models.py          # Enums, dataclasses, Pydantic models
├── state.py           # Game state representation
├── state_manager.py   # State transition logic
├── agent.py           # LangGraph agent workflow
├── config.py          # Configuration classes
└── __init__.py        # Public API exports
```

## 2. Critical Anti-Patterns (Fixed in 10/17 Games)

### 2.1 Mutable Default Arguments

**❌ WRONG**:

```python
@dataclass
class ClueHypothesis:
    excluded_suspects: list[ValidSuspect] = None  # DANGEROUS!
    excluded_weapons: list[ValidWeapon] = None    # SHARED STATE BUG!
```

**✅ CORRECT**:

```python
@dataclass
class ClueHypothesis:
    excluded_suspects: list[ValidSuspect] = field(default_factory=list)
    excluded_weapons: list[ValidWeapon] = field(default_factory=list)
```

### 2.2 Print Statement Debugging

**❌ WRONG**:

```python
print(f"[DEBUG] {player} successfully placed ships.")
print(f"WARNING: Missing analyzer engine: {engine_key}")
```

**✅ CORRECT**:

```python
import logging
logger = logging.getLogger(__name__)

logger.debug("Player successfully placed ships", extra={"player": player})
logger.warning("Missing analyzer engine", extra={"engine_key": engine_key})
```

### 2.3 Missing Type Safety

**❌ WRONG**:

```python
def analyze_position(self, state: dict[str, Any], player: str):  # No return type
    # Implementation...
```

**✅ CORRECT**:

```python
def analyze_position(self, state: dict[str, Any], player: str) -> Command:
    # Implementation...
    return Command(update=new_state, goto=next_node)
```

## 3. Testing Standards (No Mocks)

### 3.1 Testing Philosophy Reference

**Full Details**: [Testing Methodology](../testing/01_METHODOLOGY.md)

**Core Principle**: "when you test dont use mocks" - User requirement

### 3.2 Four Test Files Per Game

1. `test_{game}_models.py` - Real model validation
2. `test_{game}_state.py` - Real state management
3. `test_{game}_state_manager.py` - Real state transitions
4. `test_{game}_agent.py` - Real agent workflows

### 3.3 Real Component Examples

```python
# ✅ Real model testing
def test_ship_placement_real():
    coords = [Coordinates(row=0, col=i) for i in range(3)]
    placement = ShipPlacement(ship_type=ShipType.CRUISER, coordinates=coords)
    assert placement.ship_type.size == 3  # Real enum property

# ✅ Real state testing
def test_state_transition_real():
    state = BattleshipState()  # Real state object
    state.switch_player()      # Real method call
    assert state.current_player == "player2"  # Real verification
```

## 4. Game-Specific Patterns

### 4.1 State Management Pattern

**Required for all games**:

```python
class GameStateManager:
    @staticmethod
    def create_initial_state() -> GameState:
        """Create initial game state."""

    @staticmethod
    def apply_move(state: GameState, player: str, move: Move) -> GameState:
        """Apply move and return new state."""
        return state.model_copy(deep=True)  # Immutable updates
```

### 4.2 Agent Workflow Pattern

**Required LangGraph structure**:

```python
@register_agent(GameConfig)
class GameAgent(Agent[GameConfig]):
    def __init__(self, config: GameConfig):
        # Setup logging
        self.logger = logging.getLogger(__name__)
        super().__init__(config)

    def analyze_position(self, state: dict[str, Any], player: str) -> Command:
        """Analyze game position."""
        # No print statements - use self.logger
```

## 5. Import Organization Standards

### 5.1 Required Order

```python
# 1. Standard library
import logging
import time
from typing import Any, Dict, List

# 2. Third-party
from pydantic import Field, validator
from langgraph.types import Command

# 3. Local haive imports
from haive.games.{game}.models import GameState, Move
from haive.games.{game}.state_manager import GameStateManager
```

### 5.2 Public API Exports

**Required in `__init__.py`**:

```python
__all__ = [
    "GameAgent",
    "GameConfig",
    "GameState",
    "GameStateManager",
]
```

## 6. Memory Organization Links

### 6.1 Documentation Structure

- **Global Memory**: [CLAUDE_DOCUMENTATION/](../../claude_documentation/)
- **Games Memory**: [Current Location](../README.md)
- **Progress Tracking**: [Current Status](../progress_tracking/01_CURRENT_STATUS.md)
- **Testing Standards**: [Methodology](../testing/01_METHODOLOGY.md)

### 6.2 Individual Game Documentation

**Location**: [individual_games/](../individual_games/)
**Format**: Each game gets dedicated folder with:

- `REVIEW_SUMMARY.md` - Issues found and fixed
- `TEST_RESULTS.md` - Test coverage and results
- `IMPLEMENTATION_NOTES.md` - Game-specific patterns

## 7. Quality Checkpoints

### 7.1 Pre-Completion Checklist

**Before marking game as complete**:

- [ ] All print statements → structured logging
- [ ] All mutable defaults fixed
- [ ] Type hints on all public methods
- [ ] Import organization corrected
- [ ] Four test files created (300+ tests)
- [ ] All tests use real components (no mocks)
- [ ] Documentation updated

### 7.2 Code Review Standards

**Apply to every game**:

1. **Run comprehensive analysis** via Task tool
2. **Fix HIGH severity issues first** (mutable defaults, print statements)
3. **Add missing type hints** and docstrings
4. **Create comprehensive test suites** with real components
5. **Update documentation** and progress tracking

## 8. Integration with Global Standards

### 8.1 Inheritance from Global Rules

This document **extends** [CODING_STYLE_GUIDE.md](../../CODING_STYLE_GUIDE.md) with:

- Game-specific patterns
- Package-specific anti-patterns
- Testing methodology applications
- Memory organization structure

### 8.2 Claude Memory Integration

**Memory Files**:

- **Global**: `~/.claude/CLAUDE.md` - Universal coding principles
- **Project**: `~/.claude/projects/haive.md` - Haive-specific patterns
- **Package**: This file - Games package standards
- **Progress**: [Status tracking](../progress_tracking/01_CURRENT_STATUS.md)

---

**References**:

- **Global Standards**: [CODING_STYLE_GUIDE.md](../../CODING_STYLE_GUIDE.md)
- **Testing Methodology**: [No Mocks Testing](../testing/01_METHODOLOGY.md)
- **Current Progress**: [Status Report](../progress_tracking/01_CURRENT_STATUS.md)
- **Claude Memory**: [Documentation Guide](../../claude_documentation/README.md)
- **Individual Games**: [Game Documentation](../individual_games/)
