# MultiAgent Debug Plan & Testing Strategy

**Created**: 2025-01-28  
**Purpose**: Debug and fix EnhancedMultiAgentV4 "not subscriptable" issue  
**Status**: Issue Identified - Ready for Implementation

## 🎯 Problem Summary

**Original Issue**: EnhancedMultiAgentV4 fails with "'MultiAgentState' object is not subscriptable"

**Root Cause Discovered**:

- StateSchema objects (including MultiAgentState) don't implement `__getitem__`
- LangGraph nodes expect `state["key"]` dict access but get Pydantic model objects
- The issue occurs in BaseGraph2.to_langgraph() when LangGraph tries to access state

## 🔍 Debugging Results

### ✅ What Works

1. **EnhancedMultiAgentV4 creation**: ✅ Works perfectly
2. **Graph building**: ✅ BaseGraph2 builds correctly
3. **Compilation**: ✅ BaseGraph2.to_langgraph() succeeds
4. **Single agent execution**: ✅ Both SimpleAgent and ReactAgent work
5. **AgentNodeV3**: ✅ Returns correct Command objects
6. **MultiAgentState.get()**: ✅ Works for accessing fields

### ❌ What Fails

1. **Dict subscript access**: `state["key"]` fails with "not subscriptable"
2. **Dict containment**: `"key" in state` fails
3. **LangGraph node execution**: When nodes try dict access patterns

### 🧪 Test Evidence

```
# From our comprehensive testing:
✅ state.get('messages'): 1 messages  # WORKS
❌ state['messages'] failed: 'MultiAgentState' object is not subscriptable  # FAILS
```

## 📂 Relevant Files & Areas

### Core Files to Fix

```
packages/haive-core/src/haive/core/schema/
├── state_schema.py                    # 🔥 PRIMARY TARGET - Add dict methods
├── prebuilt/multi_agent_state.py     # 🔧 TEST TARGET - Verify inheritance
└── prebuilt/tool_state.py            # 🔧 TEST TARGET - Base class

packages/haive-core/src/haive/core/graph/state_graph/
└── base_graph2.py                    # 📍 WHERE ISSUE MANIFESTS
    └── to_langgraph() method (line ~3617)
```

### Test Files Created

```
packages/haive-core/tests/
└── test_agent_node_v3_with_simple_agent.py    # ✅ PASSING

packages/haive-agents/tests/
└── test_enhanced_multi_agent_v4_single_agent.py  # ✅ PASSING - Single agents work
```

### Integration Points

```
EnhancedMultiAgentV4 → BaseGraph2 → LangGraph StateGraph → Node Functions
                                                          ↑
                                                    HERE: state["key"] fails
```

## 🛠️ Implementation Strategy

### Phase 1: Core StateSchema Dict Support (haive-core)

**Location**: `packages/haive-core/src/haive/core/schema/state_schema.py`

```python
class StateSchema(BaseModel):
    """Add dict-like methods to StateSchema base class."""

    def __getitem__(self, key: str) -> Any:
        """Enable state["key"] access."""
        if hasattr(self, key):
            return getattr(self, key)
        raise KeyError(f"'{key}' not found in {self.__class__.__name__}")

    def __setitem__(self, key: str, value: Any) -> None:
        """Enable state["key"] = value assignment."""
        if key in self.model_fields:
            setattr(self, key, value)
        else:
            raise KeyError(f"Cannot set '{key}' - not a valid field")

    def __contains__(self, key: str) -> bool:
        """Enable 'key' in state checks."""
        return hasattr(self, key)

    def __iter__(self):
        """Enable iteration over state fields."""
        return iter(self.model_fields.keys())

    def keys(self):
        """Get state field names."""
        return self.model_fields.keys()

    def items(self):
        """Get (key, value) pairs."""
        return [(k, getattr(self, k)) for k in self.model_fields.keys()]

    def values(self):
        """Get state field values."""
        return [getattr(self, k) for k in self.model_fields.keys()]
```

### Phase 2: Test & Validate (haive-core)

**Test File**: `packages/haive-core/tests/test_state_schema_dict_compatibility.py`

```python
def test_state_schema_dict_methods():
    """Test StateSchema dict compatibility."""
    from haive.core.schema.prebuilt.multi_agent_state import MultiAgentState

    state = MultiAgentState(messages=[HumanMessage(content="test")])

    # Test dict access
    assert state["messages"] == state.messages  # Should work now
    assert "messages" in state                   # Should work now

    # Test iteration
    for key in state:
        assert hasattr(state, key)

    # Test dict methods
    assert "messages" in state.keys()
    assert state.messages in state.values()
```

### Phase 3: Integration Testing (haive-agents)

**Test Enhancement**: Update existing test to verify dict access works

```python
# In test_enhanced_multi_agent_v4_single_agent.py
def test_state_dict_access_in_langgraph_context():
    """Test that MultiAgentState works in LangGraph context."""

    def mock_langgraph_node(state):
        # This should work now with dict compatibility
        messages = state["messages"]  # Previously failed
        agents = state["agents"]      # Previously failed
        return {"messages": messages + [AIMessage(content="response")]}

    state = MultiAgentState(...)
    result = mock_langgraph_node(state)  # Should succeed
    assert isinstance(result, dict)
```

## 🧪 Testing Plan

### Test Sequence

1. **Unit Test StateSchema**: Verify dict methods work in isolation
2. **Test MultiAgentState**: Verify inheritance preserves dict compatibility
3. **Test LangGraph Integration**: Verify BaseGraph2.to_langgraph() works
4. **Test EnhancedMultiAgentV4**: Verify end-to-end multi-agent execution
5. **Regression Testing**: Ensure existing functionality unchanged

### Testing Commands (Submodule-Aware)

```bash
# 1. Test StateSchema dict compatibility (haive-core)
cd packages/haive-core/
poetry run pytest tests/test_state_schema_dict_compatibility.py -v

# 2. Test MultiAgentState integration (haive-core)
cd packages/haive-core/
poetry run pytest tests/test_multi_agent_state_dict_access.py -v

# 3. Test EnhancedMultiAgentV4 (haive-agents)
cd packages/haive-agents/
poetry run pytest tests/test_enhanced_multi_agent_v4_single_agent.py -v

# 4. Full regression test (from root)
poetry run pytest packages/haive-core/tests/ -x
poetry run pytest packages/haive-agents/tests/ -x
```

## 📊 Success Criteria

### Functional Requirements

- [ ] `state["key"]` access works for all StateSchema objects
- [ ] `"key" in state` containment checks work
- [ ] EnhancedMultiAgentV4 executes successfully with multiple agents
- [ ] All existing tests continue to pass (no regressions)

### Technical Requirements

- [ ] Dict methods implemented in StateSchema base class
- [ ] Type safety maintained (proper type hints)
- [ ] Performance impact minimal (< 5% slower than attribute access)
- [ ] Backward compatibility preserved

### Integration Requirements

- [ ] BaseGraph2.to_langgraph() works without workarounds
- [ ] AgentNodeV3 continues to return Command objects correctly
- [ ] LangGraph nodes can access state fields via dict syntax
- [ ] Multi-agent workflows execute end-to-end

## 🚨 Risk Areas & Mitigation

### High-Risk Areas

1. **Pydantic Conflicts**: Dict methods might interfere with Pydantic internals
2. **Performance**: Dict emulation could slow state access
3. **Type Safety**: Dynamic access might break static type checking

### Mitigation Strategies

1. **Careful Implementation**: Follow Pydantic patterns, test extensively
2. **Performance Monitoring**: Benchmark before/after, optimize if needed
3. **Type Annotations**: Proper type hints for all dict methods

### Rollback Plan

- Implement in feature branch: `packages/haive-core: fix/state-schema-dict-compat`
- Test thoroughly before merging
- Keep original StateSchema as fallback if issues arise

## 🎯 Implementation Order

### Step 1: haive-core Changes

```bash
cd packages/haive-core/
git checkout -b fix/state-schema-dict-compat
# Implement dict methods in StateSchema
# Create comprehensive tests
git add . && git commit -m "fix: add dict compatibility to StateSchema"
```

### Step 2: haive-agents Testing

```bash
cd packages/haive-agents/
git checkout -b test/dict-compatible-states
# Update tests to verify dict access
# Test EnhancedMultiAgentV4 with new StateSchema
git add . && git commit -m "test: verify dict-compatible StateSchema integration"
```

### Step 3: Integration & Root Update

```bash
cd ../../  # Back to root
# Test cross-package integration
poetry run pytest packages/haive-agents/tests/test_enhanced_multi_agent_v4_single_agent.py -v

# Update submodule references if tests pass
git add packages/haive-core packages/haive-agents
git commit -m "update: submodule refs for StateSchema dict compatibility fix"
```

## 📈 Expected Outcome

**Before Fix**:

```python
state = MultiAgentState(...)
state["messages"]  # ❌ 'MultiAgentState' object is not subscriptable
```

**After Fix**:

```python
state = MultiAgentState(...)
state["messages"]  # ✅ Returns messages list
"messages" in state  # ✅ Returns True
```

**EnhancedMultiAgentV4 Result**:

- ✅ Multi-agent workflows execute successfully
- ✅ LangGraph nodes can access state via dict syntax
- ✅ No workarounds needed in BaseGraph2.to_langgraph()
- ✅ Clean, maintainable code

---

**Next Actions**:

1. Implement dict methods in StateSchema (haive-core)
2. Test with MultiAgentState
3. Verify EnhancedMultiAgentV4 works end-to-end
