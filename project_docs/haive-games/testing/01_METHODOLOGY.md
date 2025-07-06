# 01 - Testing Methodology: No Mocks Real Component Testing

**Reference**: [CODING_STYLE_GUIDE.md](../../CODING_STYLE_GUIDE.md)  
**Parent**: [Haive Games README.md](../README.md)  
**Status**: [Current Progress](../progress_tracking/01_CURRENT_STATUS.md)

## 1. Core Testing Philosophy

### 1.1 "When You Test Don't Use Mocks" Principle

**Source**: User requirement - all tests must use real components

**Implementation**:

- ✅ Real model instances: `Coordinates(row=3, col=5)`
- ✅ Actual state transitions: `state.switch_player()`
- ✅ Live enum validation: `ShipType.DESTROYER.size == 2`
- ✅ Complete workflow testing: end-to-end game scenarios
- ❌ No mocking of components, states, or game logic

### 1.2 Integration Over Isolation

**Approach**: Test real interactions between components
**Benefit**: Validates actual system behavior, not mock behavior

## 2. Four-File Test Structure Pattern

### 2.1 Standard Test Files Per Game

Applied to all 10 completed games:

1. **`test_{game}_models.py`**
   - Data structures and enumerations
   - Pydantic model validation
   - Enum value verification
   - Type checking and serialization

2. **`test_{game}_state.py`**
   - Game state management
   - Property calculations
   - State transitions
   - Serialization/deserialization

3. **`test_{game}_state_manager.py`**
   - State transition logic
   - Game rule enforcement
   - Move validation
   - Win condition detection

4. **`test_{game}_agent.py`**
   - Agent workflow testing
   - LLM integration patterns
   - Error handling scenarios
   - Configuration validation

### 2.2 Test Coverage Requirements

**Per Game Minimum**: 300-500+ test cases
**Coverage Areas**:

- ✅ All public methods and properties
- ✅ Edge cases and boundary conditions
- ✅ Error scenarios and validation
- ✅ Integration workflows
- ✅ Model serialization patterns

## 3. Real Component Testing Examples

### 3.1 Model Testing (No Mocks)

```python
def test_ship_placement_validation():
    """Test using real Coordinates and ShipPlacement objects."""
    coords = [Coordinates(row=0, col=i) for i in range(3)]
    placement = ShipPlacement(ship_type=ShipType.CRUISER, coordinates=coords)

    # Real validation, real objects
    assert len(placement.coordinates) == 3
    assert placement.ship_type == ShipType.CRUISER
    assert placement.ship_type.size == 3
```

### 3.2 State Transition Testing (No Mocks)

```python
def test_player_switch_real_state():
    """Test using real BattleshipState object."""
    state = BattleshipState()  # Real state instance

    assert state.current_player == "player1"
    state.switch_player()  # Real method call
    assert state.current_player == "player2"
    state.switch_player()  # Real transition
    assert state.current_player == "player1"
```

### 3.3 Workflow Integration Testing (No Mocks)

```python
def test_complete_ship_placement_workflow():
    """Test real ship placement end-to-end."""
    state = BattleshipStateManager.create_initial_state()  # Real state

    placements = [  # Real ship placements
        ShipPlacement(ship_type=ShipType.DESTROYER, coordinates=coords)
        for coords in valid_coordinate_sets
    ]

    # Real state manager operation
    new_state = BattleshipStateManager.place_ships(state, "player1", placements)

    # Real validation
    assert new_state.player1.has_placed_ships
    assert len(new_state.player1.ship_placements) == len(placements)
```

## 4. Quality Validation Patterns

### 4.1 Model Validation Testing

**Approach**: Test real Pydantic validation

```python
def test_coordinates_validation_real():
    """Test real coordinate validation."""
    # Valid coordinates - should work
    valid_coords = [(0, 0), (9, 9), (5, 3)]
    for row, col in valid_coords:
        coords = Coordinates(row=row, col=col)  # Real validation
        assert coords.row == row
        assert coords.col == col

    # Invalid coordinates - should raise real ValidationError
    invalid_coords = [(-1, 5), (10, 5)]
    for row, col in invalid_coords:
        with pytest.raises(ValidationError):  # Real Pydantic error
            Coordinates(row=row, col=col)
```

### 4.2 State Persistence Testing

**Approach**: Test real serialization/deserialization

```python
def test_state_serialization_real():
    """Test real state persistence."""
    state = BattleshipState()  # Real state
    state.current_player = "player2"
    state.turn_count = 5

    # Real serialization
    state_dict = state.model_dump()

    # Real deserialization
    new_state = BattleshipState(**state_dict)

    # Real comparison
    assert new_state.current_player == state.current_player
    assert new_state.turn_count == state.turn_count
```

## 5. Error Scenario Testing

### 5.1 Real Error Condition Testing

**Principle**: Test actual error conditions, not mocked errors

```python
def test_invalid_move_real_error():
    """Test real invalid move handling."""
    state = BattleshipStateManager.create_initial_state()

    # Real invalid move
    invalid_move = MoveCommand(row=10, col=5)  # Out of bounds

    # Real error from real validation
    with pytest.raises(ValueError, match="Invalid move coordinates"):
        BattleshipStateManager.execute_move(state, "player1", invalid_move)
```

### 5.2 Real Validation Error Testing

```python
def test_ship_placement_validation_real_errors():
    """Test real ship placement validation errors."""
    state = BattleshipStateManager.create_initial_state()

    # Real invalid placement - missing ship types
    incomplete_placements = [ShipPlacement(...)]  # Only one ship

    # Real validation error from real state manager
    with pytest.raises(ValueError, match="Missing ship types"):
        BattleshipStateManager.place_ships(state, "player1", incomplete_placements)
```

## 6. Integration Testing Approach

### 6.1 End-to-End Workflow Testing

**Goal**: Test complete game scenarios with real components

```python
def test_complete_game_flow_real():
    """Test complete game workflow with real components."""
    # Real initialization
    state = BattleshipStateManager.create_initial_state()

    # Real ship placement for both players
    state = place_all_ships_for_both_players(state)  # Real operations

    # Real game moves
    state = make_series_of_moves(state)  # Real state transitions

    # Real win condition checking
    if state.all_ships_sunk("player2"):  # Real method call
        assert state.winner == "player1"  # Real validation
```

### 6.2 Cross-Component Integration

**Approach**: Test real interactions between models, state, and managers

## 7. Performance and Edge Case Testing

### 7.1 Boundary Condition Testing

- Real coordinate boundary testing (0,0) and (9,9)
- Real ship placement edge cases
- Real state transition limits

### 7.2 Data Integrity Testing

- Real model field validation
- Real enum value verification
- Real type checking scenarios

## 8. Benefits of No-Mocks Approach

### 8.1 Real Behavior Validation

- Tests verify actual system behavior
- Catches real integration issues
- Validates real error conditions
- Ensures real performance characteristics

### 8.2 Maintenance Benefits

- Tests break when real behavior changes (good!)
- No mock maintenance overhead
- Real refactoring safety net
- Actual regression prevention

## 9. Applied Results

### 9.1 Games Successfully Tested (10/17)

All using this no-mocks methodology:

- Go, Risk, Reversi, Checkers
- Nim, Mastermind, Dominoes, Clue, Battleship

### 9.2 Test Statistics

- **Total Test Files**: 40 (4 per game)
- **Estimated Test Cases**: 3,000+
- **Zero Mocks Used**: 100% real component testing
- **Coverage**: All critical paths and edge cases

---

**References**:

- [Current Status](../progress_tracking/01_CURRENT_STATUS.md)
- [Code Standards](../code_standards/01_HAIVE_GAMES_STANDARDS.md)
- [Global Standards](../../CODING_STYLE_GUIDE.md)
- [Individual Game Results](../individual_games/)
