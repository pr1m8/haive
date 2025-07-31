# Haive Games Review and Fix Plan

## Overview

Systematic plan to review and fix all 20 games in haive-games package to ensure CODING_STYLE_GUIDE.md compliance.

## Review Checklist Per Game

- [ ] Import organization (stdlib → third-party → local)
- [ ] Type hints on all public APIs
- [ ] Error handling (no bare except)
- [ ] Line length ≤ 88 characters
- [ ] Google-style docstrings (module, class, method)
- [ ] Test suite creation/updates
- [ ] File size check (< 500 lines preferred)

## Games Grouped by Priority

### Phase 1: Simple Games Without Tests (High Priority)

1. **mancala** - 10 files, no tests
2. **go** - 10 files, no tests
3. **debate** - 11 files, no tests

### Phase 2: Simple Games With Partial Tests

4. **risk** - 9 files, has tests (review/enhance)
5. **reversi** - 10 files, has tests (review/enhance)
6. **checkers** - 11 files, partial tests

### Phase 3: Medium Games Without Tests

7. **nim** - 12 files, no tests
8. **mastermind** - 12 files, no tests
9. **dominoes** - 13 files, no tests
10. **clue** - 13 files, no tests
11. **battleship** - 13 files, no tests

### Phase 4: Medium Games With Partial Tests

12. **tic_tac_toe** - 12 files, has tests (review/enhance)
13. **connect4** - 12 files, partial tests
14. **poker** - 13 files, partial tests

### Phase 5: Complex Games

15. **fox_and_geese** - 14 files, no tests
16. **among_us** - 15 files, no tests
17. **mafia** - 15 files, partial tests
18. **hold_em** - 16 files, no tests

### Phase 6: Special Cases

19. **monopoly** - 19 files, missing state_manager.py
20. **chess** - ✅ COMPLETED

## Tracking Template

```markdown
## Game: [Name]

- Complexity: Simple/Medium/Complex
- Files reviewed: X/Y
- Issues found: [list]
- Fixes applied: [list]
- Tests created: [list]
- Status: ⏳ In Progress / ✅ Complete
```

## Common Issues to Check

1. Import organization violations
2. Missing type hints
3. Bare except clauses
4. Line length violations
5. Missing/incomplete docstrings
6. No error handling
7. Missing test coverage

## Test Creation Standards

- Create test directory: `tests/games/{game_name}/`
- Required test files:
  - `test_{game}_models.py`
  - `test_{game}_state.py`
  - `test_{game}_state_manager.py`
  - `test_{game}_agent.py`
- Follow chess test examples for structure
