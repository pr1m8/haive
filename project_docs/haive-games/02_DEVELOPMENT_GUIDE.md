# 02 - Haive Games Development Guide

**Reference**: [CODING_STYLE_GUIDE.md](../CODING_STYLE_GUIDE.md)  
**Parent**: [Haive Games README.md](README.md)  
**Testing Standards**: [No Mocks Methodology](testing/01_METHODOLOGY.md)

## 1. Essential Development Workflow

### 1.1 Before Starting Any Game Review

```bash
# 1. Check current status and progress
git status
git diff --cached

# 2. Verify you're in the right location
pwd
# Should be: /home/will/Projects/haive/backend/haive/packages/haive-games

# 3. Read current memory state
# Check: project_docs/haive-games/progress_tracking/01_CURRENT_STATUS.md
```

### 1.2 Git Integration Best Practices

```bash
# Always check what's changed before commits
git diff HEAD~1..HEAD

# Review staging area before committing
git diff --cached

# Check specific file changes
git diff HEAD~1 path/to/file.py

# View commit history for context
git log --oneline -10
```

## 2. Code Quality Standards & Anti-Patterns

### 2.1 ❌ CRITICAL VIOLATIONS - Never Do These

#### **Print Statements (FORBIDDEN)**

```python
# ❌ WRONG - Never use print statements
print(f"[DEBUG] Player {player} made move {move}")
print("Game state:", game_state)
traceback.print_exc()

# ✅ CORRECT - Always use structured logging
import logging
logger = logging.getLogger(__name__)

logger.debug("Player made move", extra={"player": player, "move": move})
logger.debug("Game state", extra={"state": game_state.model_dump()})
logger.error("Move execution failed", exc_info=True)
```

#### **Mutable Default Arguments (DANGEROUS)**

```python
# ❌ WRONG - Causes shared state bugs
@dataclass
class GameHypothesis:
    excluded_moves: list[Move] = None  # DANGER!

def process_moves(moves: list[Move] = []):  # DANGER!
    moves.append(new_move)

# ✅ CORRECT - Use field(default_factory=...)
@dataclass
class GameHypothesis:
    excluded_moves: list[Move] = field(default_factory=list)

def process_moves(moves: list[Move] = None):
    if moves is None:
        moves = []
    moves.append(new_move)
```

#### **Mock Testing (FORBIDDEN)**

```python
# ❌ WRONG - Never use mocks in haive-games tests
@patch('haive.games.chess.state_manager.ChessStateManager')
def test_game_logic(mock_manager):
    mock_manager.apply_move.return_value = fake_state

# ✅ CORRECT - Always use real components
def test_game_logic():
    state = ChessStateManager.create_initial_state()  # Real state
    move = ChessMove(from_pos="e2", to_pos="e4")      # Real move
    new_state = ChessStateManager.apply_move(state, move)  # Real operation
    assert new_state.current_player == "black"  # Real validation
```

### 2.2 ✅ REQUIRED PATTERNS - Always Do These

#### **Structured Logging Pattern**

```python
# Required imports
import logging
logger = logging.getLogger(__name__)

# Required patterns
logger.debug("Operation started", extra={"context": "value"})
logger.info("Game completed", extra={"winner": winner, "turns": turn_count})
logger.warning("Invalid move attempted", extra={"player": player, "move": move})
logger.error("Critical failure", extra={"error": str(e)}, exc_info=True)
```

#### **Type Safety Pattern**

```python
# Required type hints on all public functions
def apply_move(state: GameState, player: str, move: Move) -> GameState:
    """Apply move and return new state."""

def analyze_position(state: dict[str, Any], player: str) -> Command:
    """Analyze position and return command."""

# Required imports organization
# 1. Standard library
import logging
import time
from typing import Any, Dict, List, Optional

# 2. Third-party
from pydantic import Field, validator
from langgraph.types import Command

# 3. Local haive imports
from haive.games.{game}.models import GameState, Move
```

#### **Real Component Testing Pattern**

```python
# Required test structure - no mocks anywhere
def test_move_validation_real():
    """Test real move validation with real components."""
    # Real state creation
    state = GameStateManager.create_initial_state()

    # Real move creation
    move = GameMove(row=0, col=0)

    # Real validation
    assert GameStateManager.is_valid_move(state, move)

    # Real state transition
    new_state = GameStateManager.apply_move(state, "player1", move)

    # Real verification
    assert new_state.board[0][0] == "player1"
    assert new_state.current_player == "player2"
```

## 3. Memory Management & Development Flow

### 3.1 Claude Memory Integration

```bash
# Memory hierarchy (READ THESE BEFORE STARTING)
~/.claude/CLAUDE.md                     # Global coding principles
~/.claude/projects/haive.md             # Haive-specific patterns
project_docs/CODING_STYLE_GUIDE.md     # Repository standards
project_docs/haive-games/               # Package-specific memory
```

### 3.2 Required Reading Order

1. **Global Standards**: [CODING_STYLE_GUIDE.md](../CODING_STYLE_GUIDE.md)
2. **Package Memory**: [Current Status](progress_tracking/01_CURRENT_STATUS.md)
3. **Testing Standards**: [No Mocks Methodology](testing/01_METHODOLOGY.md)
4. **Code Standards**: [Package Standards](code_standards/01_HAIVE_GAMES_STANDARDS.md)

### 3.3 Memory Update Pattern

```bash
# After completing each game review:
# 1. Update progress tracking
vim project_docs/haive-games/progress_tracking/01_CURRENT_STATUS.md

# 2. Create individual game summary
mkdir -p project_docs/haive-games/individual_games/{game_name}/
vim project_docs/haive-games/individual_games/{game_name}/REVIEW_SUMMARY.md

# 3. Update todo list
# Use TodoWrite tool to mark completed and set next target
```

## 4. IDE Integration & Development Tools

### 4.1 Essential IDE Commands

```bash
# Code navigation
Ctrl+Shift+F    # Search across all files
Ctrl+P          # Quick file open
Ctrl+Shift+P    # Command palette
F12             # Go to definition

# Git integration
Ctrl+Shift+G    # Git panel
Ctrl+Enter      # Commit staged changes
Ctrl+Shift+P -> "Git: View Changes"

# Code quality
Ctrl+Shift+E    # Problems panel (see type errors)
Ctrl+Shift+M    # Diagnostics
F8              # Next error/warning
```

### 4.2 Git Diff Integration Workflow

```bash
# Before making changes
git diff HEAD~1..HEAD                    # See what changed recently
git log --oneline -5                     # Check recent commits

# During development
git diff                                 # See current changes
git diff --cached                        # See staged changes
git add -p                              # Stage changes interactively

# After changes
git diff HEAD~1 -- "tests/*.py"         # See test file changes
git diff HEAD~1 -- "src/haive/games/*/agent.py"  # See agent changes
```

### 4.3 Code Quality Checks

```bash
# Run before committing
poetry run nox -s lint                  # Check style violations
poetry run nox -s typecheck             # Check type annotations
poetry run pytest tests/test_{game}_*.py  # Run game-specific tests

# IDE diagnostics integration
# Check Problems panel (Ctrl+Shift+E) for:
# - Type errors
# - Import issues
# - Linting violations
```

## 5. Testing Standards & Anti-Patterns

### 5.1 ❌ Testing Anti-Patterns (NEVER DO)

#### **Mocking Core Game Logic**

```python
# ❌ WRONG - Don't mock the things you're testing
@patch('ChessStateManager.apply_move')
def test_chess_move(mock_apply):
    mock_apply.return_value = fake_state
    # This tests nothing real!

# ✅ CORRECT - Test real game logic
def test_chess_move():
    state = ChessStateManager.create_initial_state()
    move = ChessMove(from_pos="e2", to_pos="e4")
    new_state = ChessStateManager.apply_move(state, "white", move)
    # This tests actual behavior!
```

#### **Stubbing Game State**

```python
# ❌ WRONG - Don't fake game states
def test_win_condition():
    fake_state = Mock()
    fake_state.is_game_over = True
    # This is meaningless!

# ✅ CORRECT - Create real win conditions
def test_win_condition():
    state = GameStateManager.create_initial_state()
    # Set up actual winning position
    for move in winning_sequence:
        state = GameStateManager.apply_move(state, player, move)
    assert state.is_game_over  # Real validation!
```

### 5.2 ✅ Required Testing Patterns

#### **Real Component Integration**

```python
def test_complete_game_workflow():
    """Test entire game workflow with real components."""
    # Real initialization
    state = GameStateManager.create_initial_state()

    # Real moves sequence
    moves = [Move(row=0, col=0), Move(row=1, col=1), Move(row=0, col=1)]

    # Real state transitions
    for i, move in enumerate(moves):
        player = "player1" if i % 2 == 0 else "player2"
        state = GameStateManager.apply_move(state, player, move)

        # Real validation at each step
        assert state.current_player == ("player2" if i % 2 == 0 else "player1")

    # Real end-state validation
    assert state.board[0][0] == "player1"
    assert state.board[1][1] == "player1"
```

#### **Boundary Testing with Real Data**

```python
def test_boundary_conditions_real():
    """Test boundary conditions with real game components."""
    state = GameStateManager.create_initial_state()

    # Test real edge positions
    edge_moves = [
        Move(row=0, col=0),      # Top-left
        Move(row=0, col=6),      # Top-right
        Move(row=5, col=0),      # Bottom-left
        Move(row=5, col=6),      # Bottom-right
    ]

    for move in edge_moves:
        # Real validation
        assert GameStateManager.is_valid_move(state, move)

        # Real state transition
        new_state = GameStateManager.apply_move(state, "player1", move)
        assert new_state.board[move.row][move.col] == "player1"
```

## 6. Quality Assurance Checklist

### 6.1 Before Committing Any Changes

```bash
# ✅ Code Quality Checklist
□ All print statements replaced with logger calls
□ All mutable default arguments fixed
□ All public functions have type hints
□ Import organization follows: stdlib → third-party → local
□ No mock objects in test files
□ All tests use real components
□ git diff shows only intended changes
□ IDE shows no type errors (Ctrl+Shift+E)

# ✅ Memory Management Checklist
□ Progress tracking updated
□ Individual game summary created
□ Todo list updated via TodoWrite
□ Cross-references verified in documentation
```

### 6.2 Game Review Completion Criteria

```bash
# ✅ Required for game completion
□ All critical violations fixed (print statements, mutable defaults)
□ 4 test files created: models, state, state_manager, agent
□ All tests use real components (zero mocks)
□ Individual game documentation created
□ Progress tracking updated
□ Next target identified

# ✅ Documentation Requirements
□ REVIEW_SUMMARY.md created with detailed findings
□ Cross-references to global standards included
□ Next steps clearly documented
□ Quality metrics captured
```

## 7. Development Workflow Integration

### 7.1 Standard Game Review Process

```bash
# 1. Setup and Analysis
git status && git diff
Read: project_docs/haive-games/progress_tracking/01_CURRENT_STATUS.md
Run: Task tool comprehensive review of game files

# 2. Critical Fixes
Fix: Print statements → structured logging
Fix: Mutable default arguments → field(default_factory=...)
Fix: Missing type hints → complete annotations
Fix: Import organization → proper ordering

# 3. Test Creation (NO MOCKS)
Create: test_{game}_models.py     - Real model validation
Create: test_{game}_state.py      - Real state management
Create: test_{game}_state_manager.py - Real state transitions
Create: test_{game}_agent.py      - Real agent workflows

# 4. Documentation & Memory
Create: individual_games/{game}/REVIEW_SUMMARY.md
Update: progress_tracking/01_CURRENT_STATUS.md
Update: TodoWrite with completion and next target

# 5. Quality Verification
Run: git diff to verify changes
Check: IDE diagnostics panel for errors
Verify: All tests use real components (no mocks anywhere)
```

### 7.2 Memory Integration Workflow

```bash
# Memory hierarchy integration
Global Standards    →  Package Standards  →  Individual Game
CODING_STYLE_GUIDE  →  haive-games docs   →  game review summary
│                   │                     │
├─ Universal rules  ├─ Package patterns   ├─ Specific fixes
├─ Testing philosophy ├─ Quality metrics  ├─ Issues found
└─ Git workflow     └─ Progress tracking  └─ Next actions
```

## 8. Success Validation

### 8.1 Quality Metrics to Track

- **Critical Issues Fixed**: Print statements, mutable defaults, type hints
- **Test Coverage**: 4 files per game, 300+ tests total, zero mocks
- **Code Compliance**: CODING_STYLE_GUIDE.md adherence percentage
- **Production Readiness**: No debugging output, proper error handling

### 8.2 Documentation Quality Gates

- **Cross-References**: All documents properly linked
- **Progress Tracking**: Current status accurately reflected
- **Memory Integration**: Claude memory properly maintained
- **Workflow Documentation**: Process clearly documented for future use

---

## 🎯 Quick Reference Commands

| Need                | Command                                       | Purpose                   |
| ------------------- | --------------------------------------------- | ------------------------- |
| **Check Status**    | `git status && git diff`                      | See current changes       |
| **Review Progress** | Read `progress_tracking/01_CURRENT_STATUS.md` | Current completion status |
| **Fix Logging**     | Replace `print()` → `logger.debug()`          | Structured logging        |
| **Fix Defaults**    | `field(default_factory=list)`                 | Immutable defaults        |
| **Test Real**       | Use actual objects, no `@patch`               | Real component testing    |
| **Update Memory**   | Edit progress docs + TodoWrite                | Maintain context          |

**Golden Rule**: If you're tempted to use `print()`, `Mock()`, or `@patch` - STOP and use the real components instead! 🚀

---

**References**:

- **Global Standards**: [CODING_STYLE_GUIDE.md](../CODING_STYLE_GUIDE.md)
- **Testing Philosophy**: [No Mocks Methodology](testing/01_METHODOLOGY.md)
- **Progress Status**: [Current Status](progress_tracking/01_CURRENT_STATUS.md)
- **Claude Memory**: [Documentation](../claude_documentation/)
