# Memory Management Guide: Haive-Games Review & Standardization

## 🎮 Purpose

This guide documents my memory management strategy for reviewing, fixing, documenting, and testing all games in the haive-games package according to the CODING_STYLE_GUIDE.md.

## 📋 Table of Contents

1. [Initial Task Analysis](#initial-task-analysis)
2. [Memory Priorities](#memory-priorities)
3. [Key Memory Anchors](#key-memory-anchors)
4. [Game Review Strategy](#game-review-strategy)
5. [Progress Tracking](#progress-tracking)
6. [Error Patterns](#error-patterns)
7. [Documentation Templates](#documentation-templates)
8. [Recovery Strategy](#recovery-strategy)

## 🎯 Initial Task Analysis

### Core Requirements

```python
CORE_REQUIREMENTS = {
    "review_focus": "haive-games package",
    "reference_doc": "/home/will/Projects/haive/backend/haive/project_docs/CODING_STYLE_GUIDE.md",
    "starting_point": "chess game",
    "objectives": [
        "Review all game implementations",
        "Fix code style violations",
        "Document all games properly",
        "Ensure comprehensive test coverage",
        "Create memory process for tracking"
    ]
}
```

### User Context

- User expressed need for thorough review
- Specific mention of chess as starting point
- Emphasis on documentation and testing
- Request for memory management process

## 🗂️ Memory Priorities

### 1. **Critical Information (Never Forget)**

```python
CRITICAL_MEMORY = {
    "style_guide_key_points": {
        "line_limit": 88,
        "type_hints": "everywhere",
        "docstrings": "Google-style for Sphinx",
        "testing": "Descriptive test names, proper fixtures",
        "structure": "Module < 500 lines (flexible)"
    },
    "game_package_structure": {
        "base_classes": "BaseGameAgent, GameState, StateManager",
        "common_patterns": "Agent -> State -> StateManager -> Models",
        "test_pattern": "Unit + Integration + Fixtures"
    },
    "quality_standards": {
        "documentation": "Module, class, method docstrings",
        "error_handling": "Specific exceptions with context",
        "logging": "Structured with get_logger(__name__)"
    }
}
```

### 2. **Game-Specific Patterns (Compress When Needed)**

```python
GAME_PATTERNS = {
    "common_structure": {
        "agent.py": "Main game agent implementation",
        "state.py": "Game state management",
        "models.py": "Pydantic models for game entities",
        "state_manager.py": "State transition logic",
        "engines.py": "LLM integration",
        "config.py": "Configuration classes",
        "example.py": "Usage examples"
    },
    "test_structure": {
        "test_models": "Model validation tests",
        "test_state": "State transition tests",
        "test_agent": "Agent behavior tests",
        "test_integration": "Full game flow tests"
    }
}
```

### 3. **Progress Tracking (Update Frequently)**

```python
PROGRESS_TRACKER = {
    "total_games": 30,  # Approximate count
    "reviewed": [],
    "fixed": [],
    "documented": [],
    "tested": [],
    "current_game": "chess",
    "issues_found": {}
}
```

## 🔑 Key Memory Anchors

### 1. **Style Guide Violations to Check**

```python
STYLE_CHECKPOINTS = {
    "imports": "Proper ordering with isort",
    "type_hints": "All public APIs typed",
    "docstrings": "Module, class, method documentation",
    "line_length": "Max 88 characters",
    "error_handling": "Custom exceptions, proper logging",
    "test_naming": "test_component_does_specific_thing",
    "fixture_usage": "Shared fixtures in conftest.py"
}
```

### 2. **Common Issues Pattern**

```python
COMMON_ISSUES = {
    "missing_docstrings": "Add Google-style docstrings",
    "no_type_hints": "Add type annotations",
    "poor_error_handling": "Add specific exceptions",
    "test_structure": "Follow CODING_STYLE_GUIDE patterns",
    "long_modules": "Consider splitting if >500 lines",
    "missing_examples": "Add example.py with clear usage"
}
```

## 📊 Game Review Strategy

### Review Checklist Per Game

```markdown
## Game: [Name]

- [ ] **Structure Review**
  - [ ] All expected files present
  - [ ] Module size < 500 lines
  - [ ] Proper package structure

- [ ] **Code Quality**
  - [ ] Type hints on all public APIs
  - [ ] Proper error handling
  - [ ] Logging implementation
  - [ ] No code style violations

- [ ] **Documentation**
  - [ ] Module docstrings
  - [ ] Class docstrings
  - [ ] Method docstrings
  - [ ] README.md updated
  - [ ] Example files

- [ ] **Testing**
  - [ ] Unit tests for models
  - [ ] State transition tests
  - [ ] Integration tests
  - [ ] Test naming conventions
  - [ ] Fixture usage
```

### Memory Template Per Game

```python
GAME_MEMORY_TEMPLATE = {
    "name": "",
    "complexity": "simple|medium|complex",
    "player_count": "",
    "key_components": [],
    "issues_found": [],
    "fixes_applied": [],
    "documentation_added": [],
    "tests_status": "",
    "notes": ""
}
```

## 🔧 Progress Tracking

### Current Status Format

```python
def update_progress(game_name: str, status: str):
    """Track progress for each game review."""
    PROGRESS_LOG[game_name] = {
        "status": status,  # "reviewing", "fixing", "documenting", "testing", "complete"
        "timestamp": datetime.now(),
        "issues": [],
        "completion": 0  # percentage
    }
```

### Batch Progress Summary

```markdown
## Progress Summary [Date]

- Games Reviewed: X/30
- Games Fixed: Y/30
- Documentation Complete: Z/30
- Tests Verified: W/30

### Priority Issues

1. Missing type hints in: [list]
2. No tests for: [list]
3. Documentation needed: [list]
```

## 🐛 Error Patterns

### Recognition and Solutions

```python
ERROR_PATTERNS = {
    "import_errors": {
        "symptom": "Cannot import from haive.games.X",
        "check": ["__init__.py exports", "circular imports"],
        "solution": "Update __all__ in __init__.py"
    },
    "test_failures": {
        "symptom": "Tests fail with fixture errors",
        "check": ["conftest.py setup", "fixture scope"],
        "solution": "Move shared fixtures to conftest.py"
    },
    "docstring_issues": {
        "symptom": "Sphinx warnings",
        "check": ["Docstring format", "Parameter descriptions"],
        "solution": "Use Google-style docstring template"
    }
}
```

## 📝 Documentation Templates

### Module Docstring Template

```python
"""Game implementation for [Game Name].

This module implements the [Game Name] game with support for:
- Multiple player configurations
- State persistence
- LLM-based agents
- Configurable difficulty levels

The game follows the standard haive-games architecture with
separate agent, state, and model components.

Examples:
    Basic game setup::

        from haive.games.[game] import [Game]Agent

        agent = [Game]Agent(name="player1")
        result = await agent.play()

    With custom configuration::

        config = [Game]Config(difficulty="hard")
        agent = [Game]Agent(config=config)

See Also:
    - :class:`~haive.games.base.Agent`: Base game agent
    - :mod:`haive.games.[game].models`: Game-specific models
"""
```

### Test Structure Template

```python
class Test[Game]Models:
    """Test suite for [Game] game models."""

    @pytest.fixture
    def sample_[entity](self) -> [Entity]:
        """Create a sample [entity] for testing."""
        return [Entity](...)

    def test_[entity]_validation_accepts_valid_data(
        self, sample_[entity]: [Entity]
    ) -> None:
        """Test that [entity] accepts valid data."""
        # Test implementation

    def test_[entity]_validation_rejects_invalid_data(self) -> None:
        """Test that [entity] rejects invalid data."""
        # Test implementation
```

## 🔄 Recovery Strategy

### When Returning to Task

1. **Check Current Game**: Look at PROGRESS_TRACKER["current_game"]
2. **Review Issues List**: Check PROGRESS_LOG[game]["issues"]
3. **Verify Last Action**: Check file modification times
4. **Read TODO State**: Use TodoRead for current status
5. **Continue Checklist**: Resume from last checkpoint

### Context Restoration

```python
def restore_context():
    """Steps to restore working context."""
    # 1. Read this memory guide
    # 2. Check progress tracker
    # 3. Review last game's issues
    # 4. Check git status for changes
    # 5. Continue with checklist
```

## 💡 Memory Optimization Tips

1. **Use Patterns Not Details**: Remember "all games need docstrings" not specific docstring content
2. **Track Completion Not Process**: Mark games as done, don't memorize fixes
3. **Document Immediately**: Write fixes/issues as found
4. **Batch Similar Work**: Do all docstrings, then all tests, etc.
5. **Create Checkpoints**: Commit after each game completion

## 📊 Metrics to Track

- **Games Total**: ~30 different game implementations
- **Common Issues**: Missing docstrings (90%), No type hints (70%), Poor tests (60%)
- **Time per Game**: Simple (30 min), Medium (1 hr), Complex (2 hr)
- **Documentation Added**: README updates, docstrings, examples
- **Test Coverage**: Aim for >80% per game

## 🎯 Success Criteria

A game is considered "complete" when:

1. ✅ All code follows CODING_STYLE_GUIDE.md
2. ✅ Full documentation (module, class, method)
3. ✅ Comprehensive test coverage
4. ✅ Working example.py file
5. ✅ Updated README.md
6. ✅ No linting/type errors

---

This memory management guide will help maintain consistency and track progress throughout the haive-games review process.
