# Comprehensive Games Review Checklist

## Overview

Systematic checklist for reviewing all 20 games in haive-games package to ensure CODING_STYLE_GUIDE.md compliance.

## Master Checklist Template

### Per Game Review Process

```markdown
## Game: [NAME] - Status: [ ] Pending / [⏳] In Progress / [✅] Complete

### Files to Review:

- [ ] models.py
- [ ] state.py
- [ ] agent.py
- [ ] state_manager.py
- [ ] config.py
- [ ] Other files: \***\*\_\_\_\*\***

### Code Quality Checks:

- [ ] Import organization (stdlib → third-party → local)
- [ ] No imports inside methods/functions
- [ ] Type hints on all public APIs
- [ ] No bare except clauses
- [ ] Line length ≤ 88 characters
- [ ] Google-style docstrings (module, class, method)
- [ ] Proper error handling with specific exceptions
- [ ] Replace print() with logging
- [ ] No code duplication
- [ ] File size < 500 lines (preferred)

### Tests Required:

- [ ] test\_{game}\_models.py
- [ ] test\_{game}\_state.py
- [ ] test\_{game}\_state_manager.py
- [ ] test\_{game}\_agent.py
- [ ] All tests use descriptive names
- [ ] No mocks used
- [ ] Proper fixtures

### Documentation:

- [ ] README.md updated
- [ ] FIXES_SUMMARY.md created
```

## All Games Status

### ✅ COMPLETED (2/20)

#### 1. ✅ Chess

- **Files**: 21 files
- **Issues Found**: 8 (import order, bare except, line length)
- **Fixes Applied**: All resolved
- **Tests**: 4 files created
- **Score**: 98/100

#### 2. ✅ Mancala

- **Files**: 10 files
- **Issues Found**: 12 (imports in methods, print statements, duplication)
- **Fixes Applied**: Major refactoring
- **Tests**: 4 files created
- **Score**: 98/100

### ⏳ PHASE 1: Simple Games Without Tests (3/20)

#### 3. [ ] Go

- **Files**: 10 files
- **Expected Issues**: Imports, print statements, missing type hints
- **Priority**: High

#### 4. [ ] Debate

- **Files**: 11 files
- **Expected Issues**: Standard violations
- **Priority**: High

### 🔄 PHASE 2: Simple Games With Partial Tests (3/20)

#### 5. [ ] Risk

- **Files**: 9 files
- **Has Tests**: Yes (review/enhance)
- **Priority**: High

#### 6. [ ] Reversi

- **Files**: 10 files
- **Has Tests**: Yes (review/enhance)
- **Priority**: High

#### 7. [ ] Checkers

- **Files**: 11 files
- **Has Tests**: Partial (test_checkers_generic.py)
- **Priority**: High

### 📋 PHASE 3: Medium Games Without Tests (5/20)

#### 8. [ ] Nim

- **Files**: 12 files
- **Priority**: Medium

#### 9. [ ] Mastermind

- **Files**: 12 files
- **Priority**: Medium

#### 10. [ ] Dominoes

- **Files**: 13 files
- **Priority**: Medium

#### 11. [ ] Clue

- **Files**: 13 files
- **Priority**: Medium

#### 12. [ ] Battleship

- **Files**: 13 files
- **Priority**: Medium

### 🔄 PHASE 4: Medium Games With Partial Tests (3/20)

#### 13. [ ] Tic Tac Toe

- **Files**: 12 files
- **Has Tests**: Yes (comprehensive)
- **Priority**: Medium

#### 14. [ ] Connect4

- **Files**: 12 files
- **Has Tests**: Partial (test_connect4_generic.py)
- **Priority**: Medium

#### 15. [ ] Poker

- **Files**: 13 files
- **Has Tests**: Partial (test_poker_agent.py)
- **Priority**: Medium

### 🏗️ PHASE 5: Complex Games (4/20)

#### 16. [ ] Fox and Geese

- **Files**: 14 files
- **Priority**: Medium

#### 17. [ ] Among Us

- **Files**: 15 files
- **Priority**: Medium

#### 18. [ ] Mafia

- **Files**: 15 files
- **Has Tests**: Partial (test_mafia.py)
- **Priority**: Medium

#### 19. [ ] Hold Em

- **Files**: 16 files
- **Priority**: Medium

### ⚠️ PHASE 6: Special Cases (1/20)

#### 20. [ ] Monopoly

- **Files**: 19 files
- **Special Issue**: Missing state_manager.py
- **Has Tests**: Partial (test_monopoly.py)
- **Priority**: Low

## Quick Reference Fixes

### Common Patterns to Apply:

#### 1. Import Organization

```python
# Before (❌)
from haive.games.X.models import Y
import json

# After (✅)
import json

from haive.games.X.models import Y
```

#### 2. Logging Setup

```python
# Add to top of file
import logging
logger = logging.getLogger(__name__)

# Replace print() with
logger.info()
logger.warning()
logger.error()
```

#### 3. Helper Functions for Duplication

```python
def extract_data_from_response(response: Any) -> Optional[Dict[str, Any]]:
    """Common pattern for extracting LLM response data."""
    # Implementation
```

#### 4. Error Handling

```python
# Before (❌)
except:
    pass

# After (✅)
except (ValueError, AttributeError) as e:
    logger.error(f"Specific error context: {e}")
```

## Execution Plan

### Daily Targets:

- **Day 1**: Go, Debate (2 games)
- **Day 2**: Risk, Reversi, Checkers (3 games)
- **Day 3**: Nim, Mastermind, Dominoes (3 games)
- **Day 4**: Clue, Battleship, Tic Tac Toe (3 games)
- **Day 5**: Connect4, Poker, Fox and Geese (3 games)
- **Day 6**: Among Us, Mafia, Hold Em (3 games)
- **Day 7**: Monopoly, final review (1 game + review)

### Success Criteria:

- All 20 games achieve 95+ compliance score
- All games have comprehensive test suites
- All common violations eliminated
- Consistent patterns across all games
