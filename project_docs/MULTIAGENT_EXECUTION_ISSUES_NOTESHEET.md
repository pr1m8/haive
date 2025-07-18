# MultiAgent Execution Issues - Comprehensive Notesheet

**Date**: 2025-01-18  
**Issue**: Self-Discover MultiAgent execution fails with "No callable found, using pass-through"  
**Status**: Multiple issues identified, solutions documented

## 🎯 **Executive Summary**

MultiAgent sequential execution (SelectorAgent → AdapterAgent → StructurerAgent → ExecutorAgent) fails because agents are not being properly wrapped in executable node configurations when added to the graph.

## 🔍 **Root Cause Analysis**

### **Primary Issue: Agent Node Wrapping**

- **Problem**: `add_intelligent_agent_routing` method correctly calls `create_agent_node_v3` but configuration is wrong
- **Symptom**: "No callable found, using pass-through" warnings for each agent
- **Location**: `packages/haive-core/src/haive/core/graph/state_graph/base_graph2.py:4648`

### **Secondary Issues Discovered**

1. **Type Annotation Forward Reference Issues** ✅ **FIXED**
   - **Files Fixed**:
     - `packages/haive-core/src/haive/core/schema/prebuilt/multi_agent_state.py`
     - `packages/haive-agents/src/haive/agents/multi/clean.py`
     - `packages/haive-core/src/haive/core/graph/node/agent_node_v3.py`
   - **Fix Applied**: Added `from __future__ import annotations` and proper Agent import handling

2. **AgentNodeV3Config Validation Error** 🔄 **IN PROGRESS**
   - **Error**: `agent field - Input should be None [type=none_required]`
   - **Cause**: `extract_from_container=True` (default) conflicts with providing agent directly
   - **Solution**: Set `extract_from_container=False` when agent is provided

## 📋 **Issues Breakdown**

### **Issue 1: Type Annotation Resolution** ✅ **RESOLVED**

**Problem**:

```python
NameError: name 'Agent' is not defined
```

**Root Cause**:

- Forward references to `Agent` type in Pydantic schemas
- `Agent` imported only under `TYPE_CHECKING`
- LangGraph's `get_type_hints()` tries to resolve at runtime

**Files Affected**:

- `multi_agent_state.py`
- `clean.py` (MultiAgent)
- `agent_node_v3.py`

**Fix Applied**:

```python
from __future__ import annotations

# Import Agent to be available for type resolution
try:
    from haive.agents.base.agent import Agent
except ImportError:
    Agent = None

if TYPE_CHECKING and Agent is None:
    from haive.agents.base.agent import Agent
```

### **Issue 2: Agent Node Configuration** 🔄 **NEEDS FIX**

**Problem**:

```python
agent field - Input should be None [type=none_required, input_value=SimpleAgent(...)]
```

**Root Cause**:

- `AgentNodeV3Config.agent` field has `exclude=True` and expects `None` by default
- `extract_from_container=True` (default) means agent should be extracted from state
- But we're providing agent directly in `create_agent_node_v3(agent=agent)`

**Current Code**:

```python
# In base_graph2.py line 4648
agent_node = create_agent_node_v3(agent_name=agent_name, agent=agent, name=node_name)
```

**Required Fix**:

```python
# In base_graph2.py line 4648
agent_node = create_agent_node_v3(
    agent_name=agent_name,
    agent=agent,
    name=node_name,
    extract_from_container=False  # Use provided agent, don't extract from state
)
```

### **Issue 3: Engine Node vs Agent Node Pattern** 📚 **PATTERN IDENTIFIED**

**Engine Pattern** (working):

```python
engine_config = EngineNodeConfig(name="llm_node", engine=raw_engine)
self.add_node("llm_node", engine_config)  # ✅ Callable via __call__()
```

**Agent Pattern** (should work after fix):

```python
agent_config = create_agent_node_v3(
    agent_name="selector",
    agent=raw_agent,
    name="selector",
    extract_from_container=False
)
self.add_node("selector", agent_config)  # ✅ Should be callable via __call__()
```

## 🔧 **Required Fixes**

### **Fix 1: Update add_intelligent_agent_routing** 🎯 **HIGH PRIORITY**

**File**: `packages/haive-core/src/haive/core/graph/state_graph/base_graph2.py`  
**Line**: 4648

**Change**:

```python
# BEFORE:
agent_node = create_agent_node_v3(agent_name=agent_name, agent=agent, name=node_name)

# AFTER:
agent_node = create_agent_node_v3(
    agent_name=agent_name,
    agent=agent,
    name=node_name,
    extract_from_container=False  # Use provided agent directly
)
```

### **Fix 2: Verify Agent Node Callable** 🔍 **VALIDATION**

**Test**:

```python
agent_node = create_agent_node_v3(
    agent_name="selector",
    agent=SelectorAgent(),
    name="selector",
    extract_from_container=False
)
assert callable(agent_node)  # Should have __call__ method
```

## 🧪 **Testing Strategy**

### **Test 1: Agent Node Creation**

```python
from haive.core.graph.node.agent_node_v3 import create_agent_node_v3
from haive.agents.reasoning_and_critique.self_discover.selector import SelectorAgent

agent_node = create_agent_node_v3(
    agent_name="selector",
    agent=SelectorAgent(),
    name="selector",
    extract_from_container=False
)
print(f"Callable: {callable(agent_node)}")
```

### **Test 2: MultiAgent Graph Build**

```python
from haive.agents.multi.clean import MultiAgent
from haive.agents.reasoning_and_critique.self_discover.selector import SelectorAgent

multi_agent = MultiAgent(agents=[SelectorAgent()])
graph = multi_agent.build_graph()  # Should not fail
```

### **Test 3: Full Execution**

```python
multi_agent = MultiAgent(agents=[
    SelectorAgent(), AdapterAgent(), StructurerAgent(), ExecutorAgent()
])

result = await multi_agent.arun({
    "available_modules": "1. Critical Thinking\n2. Systems Analysis",
    "task_description": "What is 2 + 2?"
})
```

## 🚨 **Known Working Patterns**

### **Individual Agent Execution** ✅ **WORKS**

```python
agent = SelectorAgent()
result = agent.run(input_data)  # Works fine
```

### **Agent Compilation** ✅ **WORKS**

```python
multi_agent = MultiAgent(agents=[SelectorAgent()])
multi_agent.compile()  # Works after type annotation fixes
```

### **LangGraph Node Structure** ✅ **DETECTED**

```python
# LangGraph sees these nodes after compilation:
['__start__', 'selector']
```

## 🔮 **Expected Behavior After Fixes**

1. **Agent Node Creation**: `create_agent_node_v3` succeeds without validation errors
2. **Graph Compilation**: `MultiAgent.build_graph()` succeeds
3. **Node Execution**: No "No callable found" warnings
4. **Sequential Execution**: SelectorAgent → AdapterAgent → StructurerAgent → ExecutorAgent
5. **State Management**: Proper state flow between agents
6. **Real LLM Calls**: Actual agent execution with structured outputs

## 🎯 **Success Criteria**

- [ ] **Fix 1 Applied**: `extract_from_container=False` in `add_intelligent_agent_routing`
- [ ] **Agent Node Creation**: `create_agent_node_v3` validates successfully
- [ ] **Graph Build**: `MultiAgent.build_graph()` completes without errors
- [ ] **Node Callable**: Agent nodes have working `__call__` methods
- [ ] **No Pass-through**: Agents execute instead of pass-through behavior
- [ ] **Full Workflow**: Self-Discover agents execute sequentially
- [ ] **Real Results**: Actual LLM responses, not empty outputs

## 📚 **References**

- **Engine Node Pattern**: `packages/haive-core/src/haive/core/graph/node/engine_node.py`
- **Agent Node V3**: `packages/haive-core/src/haive/core/graph/node/agent_node_v3.py`
- **MultiAgent Implementation**: `packages/haive-agents/src/haive/agents/multi/clean.py`
- **Test File**: `packages/haive-agents/tests/reasoning_and_critique/self_discover/test_self_discover_clean.py`

## 💡 **Future Improvements**

1. **Smart Detection**: Automatically detect if object is Agent and wrap appropriately
2. **Better Error Messages**: Clearer errors when agent nodes fail to create
3. **Validation**: Runtime validation that agent nodes are properly callable
4. **Documentation**: Update MultiAgent docs with agent node v3 requirements

---

**Next Steps**: Apply Fix 1, test agent node creation, validate full execution flow.
