# Games Review Methodology - Claude Memory

## Systematic Review Process

### Step 1: Comprehensive Code Analysis

```bash
# Use Task tool for thorough review
- Read all core files: models.py, state.py, state_manager.py, agent.py, config.py
- Identify violations by severity: HIGH/MEDIUM/LOW
- Document specific line numbers and issues
- Categorize by type: logging, type hints, imports, style
```

### Step 2: Critical Fixes First

**Priority Order:**

1. **Mutable Default Arguments** - Can cause shared state bugs
2. **Print Statements** → Structured Logging - Production readiness
3. **Missing Type Hints** - Code safety and IDE support
4. **Import Organization** - PEP 8 compliance
5. **Missing Docstrings** - Documentation completeness

### Step 3: Test File Creation (NO MOCKS)

**Four Files Per Game:**

1. `test_{game}_models.py` - Data structures, enums, validation
2. `test_{game}_state.py` - Game state, properties, serialization
3. `test_{game}_state_manager.py` - State transitions, game logic
4. `test_{game}_agent.py` - Agent workflows, LLM integration

**Testing Philosophy:**

- Use real components: `Coordinates(row=3, col=5)`
- Test actual behavior: `state.switch_player()`
- Validate real workflows: complete game scenarios
- No mocking - test integration and real interactions

### Step 4: Validation Patterns

```python
# Example real component testing
def test_ship_placement_validation():
    coords = [Coordinates(row=0, col=i) for i in range(3)]
    placement = ShipPlacement(ship_type=ShipType.CRUISER, coordinates=coords)
    assert len(placement.coordinates) == 3
    assert placement.ship_type == ShipType.CRUISER
```

## Common Issues Found

### Critical Patterns:

- **Mutable Defaults**: `list[Type] = None` → `list[Type] = field(default_factory=list)`
- **Print Statements**: `print(f"DEBUG: {msg}")` → `logger.debug("message", extra={"context": value})`
- **Type Safety**: Missing return types, incorrect enum usage
- **Import Duplication**: Same imports in multiple locations

### Medium Issues:

- Missing `__all__` declarations
- Shebang lines in non-executable modules
- Long lines (>88 characters)
- Unclear variable names

## Quality Standards

### Code Style Compliance:

- Line length: 88 characters max
- Import order: stdlib → third-party → local
- Type hints on all public functions
- Google-style docstrings

### Test Coverage Goals:

- 300-500+ test cases per game
- All edge cases covered
- Error conditions tested
- Integration scenarios validated
- Real component interactions

## Memory Organization

### Files I Maintain:

- `project_docs/claude_documentation/GAMES_REVIEW_PROGRESS.md` - Status tracking
- `project_docs/claude_documentation/GAMES_REVIEW_METHODOLOGY.md` - This file
- TodoWrite/TodoRead - Active task management

### Results I Create:

- Fixed source files with proper logging
- Comprehensive test suites (4 files per game)
- Updated imports and type safety
- Documentation improvements

## Success Metrics

### Per Game Completion:

✅ All print statements → structured logging
✅ All mutable defaults fixed
✅ Type hints added where missing
✅ Import organization corrected
✅ 4 comprehensive test files created
✅ All tests use real components (no mocks)
✅ Documentation updated

### Repository Benefits:

- Consistent logging patterns across all games
- Bulletproof test coverage for maintenance
- Type safety for IDE support and error prevention
- Clear public APIs with proper exports
- Production-ready code quality standards
