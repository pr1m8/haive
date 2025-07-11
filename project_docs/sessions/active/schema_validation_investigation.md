# Schema Validation Investigation - Session Memory

**Date**: 2025-01-10  
**Issue**: Context and engine fields incorrectly marked as required in SimpleAgentV2  
**Status**: REAL validation error identified, investigating schema composer

## Current Problem Summary

**VALIDATED ERROR**: LangGraph validation failing with:
```
ValidationError: 2 validation errors for SimpleAgentV2State
engine
  Field required [type=missing, input_value={'messages': [], 'query':...}, input_type=dict]
context  
  Field required [type=missing, input_value={'messages': [], 'query':...}, input_type=dict]
```

**Root Cause**: Schema composer is marking `context` and `engine` as required in final state, despite:
- ✅ AugLLMConfig._compute_input_fields() fixed to exclude partial variables
- ❌ Schema composition process not preserving field optionality

## Progress Made

### Syntax Errors Fixed ✅
1. **general_protocols.py line 16**: Fixed empty `if TYPE_CHECKING:` block
2. **aug_llm/config.py**: Fixed all model validators to use `@classmethod`
3. **dashboard.py line 385**: Fixed mismatched brackets
4. **auto_config.py line 234**: Fixed unterminated string literal
5. **basic_agent_state import**: Removed non-existent module references

### Key Discovery ✅
- **Notebook test now runs** and shows the actual validation error
- **LangGraph validation** is failing at `loop.py:494` when trying to create `SimpleAgentV2State`
- **AugLLMConfig fix worked** - warning shows it tried to handle context but failed
- **Schema composer** is the remaining culprit - not preserving optionality

## Technical Details

### Where Error Occurs
```python
# In langgraph/pregel/loop.py:494
cast(Type[BaseModel], self.input_model)(
    **read_channels(self.checkpoint.pending_sends, self.channels)
)
```

### Expected vs Actual
- **Expected**: `context` field optional with default `''` from partial template
- **Expected**: `engine` field automatically provided by agent
- **Actual**: Both marked as required in final `SimpleAgentV2State`

## Investigation Plan

### Phase 1: Schema Composer Analysis 🔄
- Read entire schema_composer.py file (3500 lines)
- Add comprehensive logging to field composition process
- Trace how AugLLMConfig fields become required in final schema
- Focus on `build()`, `add_fields_from_engine()`, field definition creation

### Phase 2: State Schema Analysis 📋
- Read entire state_schema.py file
- Add logging to state creation and field handling
- Understand how field optionality is preserved/lost

### Phase 3: Field Definition Analysis 📋
- Analyze how FieldDefinition preserves optionality
- Check field metadata handling
- Verify default value propagation

## Next Actions

1. **Read schema_composer.py entirely** with comprehensive logging
2. **Add debug logging** to field composition process
3. **Trace field requirement logic** step by step
4. **Identify where optionality is lost** in the composition chain
5. **Fix the field requirement determination**

## Key Files

- `/packages/haive-core/src/haive/core/schema/schema_composer.py` (3500 lines)
- `/packages/haive-core/src/haive/core/schema/state_schema.py` 
- `/packages/haive-core/src/haive/core/schema/field_definition.py`
- `/packages/haive-core/src/haive/core/engine/aug_llm/config.py` (fixed)

## Success Criteria

- [ ] Context field optional in final SimpleAgentV2State
- [ ] Engine field optional in final SimpleAgentV2State  
- [ ] Notebook test runs successfully: `result = agent_tester(RAG_QUERY_REFINEMENT,QueryRefinementResponse,{"query":"what is the tallest building in france"})`

---

**Next**: Read schema_composer.py in its entirety and add comprehensive field composition logging.