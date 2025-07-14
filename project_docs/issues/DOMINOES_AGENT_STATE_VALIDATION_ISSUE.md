# DominoesAgent State Validation Issue - TODO

**Issue ID**: DOMINOES-001  
**Status**: 🔄 TODO  
**Priority**: Medium  
**Created**: 2025-07-11  
**Estimated Effort**: 2-3 hours

## Problem Summary

The DominoesAgent likely has a similar state validation timing issue as the DebateAgent where DynamicGraph validates input state against the DominoesState schema BEFORE calling the initialize_game method. This would cause validation errors for simple inputs that don't match the full state schema structure.

## Expected Root Cause

Based on the DebateAgent analysis, the DominoesAgent likely has:

- DynamicGraph using the same `state_schema` for both input validation and internal state management
- Simple inputs failing validation against the complex DominoesState schema
- The initialize_game method designed to transform simple input into proper DominoesState but never getting called due to validation failure

## Proposed Solution

Apply the same input schema pattern that was successful for DebateAgent:

### 1. Create DominoesInputSchema

- **File**: `/packages/haive-games/src/haive/games/dominoes/input_schema.py`
- **Purpose**: Flexible input schema for dominoes game initialization
- **Features**:
  - Accept simple game setup: `{"players": ["alice", "bob"], "max_pips": 6}`
  - Accept structured game config: `{"game_type": "mexican_train", "players": [...], "rules": {...}}`
  - Use `extra = "allow"` for flexibility

### 2. Update DominoesAgent Configuration

- **File**: `/packages/haive-games/src/haive/games/dominoes/agent.py`
- **Change**: Modify `setup_workflow()` method to use separate input schema:

```python
def setup_workflow(self) -> None:
    """Setup the dominoes workflow."""
    from haive.games.dominoes.input_schema import DominoesInputSchema

    gb = DynamicGraph(
        components=[self.config],
        state_schema=self.config.state_schema,
        input_schema=DominoesInputSchema  # ← NEW: Separate input validation
    )
```

### 3. Create Comprehensive Test

- **File**: `/test_dominoes_agent_fix.py`
- **Coverage**:
  - Agent creation
  - Input schema validation with simple formats
  - initialize_game method functionality
  - Graph compilation with simple inputs
- **Test Cases**:
  - Simple player list: `{"players": ["alice", "bob"]}`
  - Structured game setup: `{"game_type": "block", "players": [...], "max_pips": 6}`

## Files to Investigate

1. **Current Implementation**: `/packages/haive-games/src/haive/games/dominoes/agent.py`
2. **State Schema**: `/packages/haive-games/src/haive/games/dominoes/state.py`
3. **Config**: `/packages/haive-games/src/haive/games/dominoes/config.py`

## Expected Files to Create/Modify

1. **Create**: `/packages/haive-games/src/haive/games/dominoes/input_schema.py`
2. **Modify**: `/packages/haive-games/src/haive/games/dominoes/agent.py` (setup_workflow method)
3. **Create**: `/test_dominoes_agent_fix.py` (comprehensive test script)

## Verification Plan

```bash
# Test the fix
poetry run python test_dominoes_agent_fix.py

# Run existing dominoes tests to ensure no regressions
poetry run pytest packages/haive-games/tests/test_dominoes/ -v
```

## Success Criteria

✅ DominoesAgent accepts simple input formats like:

```python
{
    "players": ["alice", "bob"],
    "max_pips": 6
}
```

✅ All existing functionality remains intact
✅ Comprehensive test coverage for input validation
✅ No regressions in existing dominoes tests

## Technical Notes

- This follows the exact same pattern as the successful DebateAgent fix
- The input schema pattern leverages DynamicGraph's support for separate `input_schema` and `state_schema`
- Should be a straightforward application of the established solution pattern

## Dependencies

- Requires understanding of current DominoesAgent implementation
- May need to examine dominoes-specific state requirements
- Should reference the DebateAgent implementation as a template

---

**Labels**: `bug`, `enhancement`, `games`, `dominoes`, `todo`
**Priority**: Medium (similar to resolved DebateAgent issue)
**Status**: 🔄 TODO

**Next Steps**:

1. [ ] Investigate current DominoesAgent implementation
2. [ ] Create DominoesInputSchema based on game requirements
3. [ ] Apply the input schema pattern to setup_workflow method
4. [ ] Create comprehensive test to verify the fix
5. [ ] Run full test suite to ensure no regressions
