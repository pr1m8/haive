# Validation Routing Summary - Complete Analysis

**Created**: 2025-01-29
**Status**: Investigation Complete

## Executive Summary

SimpleAgent has a critical bug: the validation node has no outgoing edges, causing infinite recursion with structured output models.

## The Bug in One Sentence

**SimpleAgent creates `agent_node → validation` but forgets `validation → anywhere`**

## Quick Fix

```python
# In SimpleAgent._add_validation_nodes(), after creating validation node:
from haive.core.graph.node.validation_router_v2 import validation_router_v2

# Add conditional edges FROM validation
routing_map = {
    "tool_node": "tool_node" if needs_tools else None,
    "parse_output": "parse_output" if needs_parsing else None,
    "agent_node": "agent_node"  # For errors
}
routing_map = {k: v for k, v in routing_map.items() if v}

graph.add_conditional_edges(
    "validation",
    validation_router_v2,
    routing_map
)
```

## Why This Happens

1. **Tool Call**: Agent generates `Plan[Task]` → sanitized to `plan_task_generic`
2. **Route Assignment**: `plan_task_generic` correctly gets `parse_output` route
3. **Validation Node**: Processes tool call, creates ToolMessage
4. **Missing Router**: No edges from validation, graph doesn't know where to go
5. **Recursion**: LangGraph retries from START, hits limit after 100 attempts

## Evidence Trail

### 1. Route Assignment Works ✅
```python
# From test_route_assignment.py:
plan_task_generic → parse_output  # Correct!
```

### 2. Validation Node Works ✅
```python
# From integration tests:
# Node creates ToolMessages correctly
```

### 3. Router Function Works ✅
```python
# validation_router_v2.py handles parse_output:
elif route == "parse_output":
    destinations.add("parse_output")
```

### 4. SimpleAgent Missing Edges ❌
```python
# From agent.py:
graph.add_edge("agent_node", "validation")
# NO EDGES FROM VALIDATION!
```

### 5. SimpleAgentV2 Has Edges ✅
```python
# From archive/agent_v2.py:
graph.add_conditional_edges(
    "validation_v2", 
    validation_router_v2,
    routing_map
)
```

## File References

### Core Files
1. **The Bug**: `/packages/haive-agents/src/haive/agents/simple/agent.py` (line 812)
2. **Working Example**: `/packages/haive-agents/src/haive/agents/simple/archive/agent_v2.py` (line 360)
3. **Router Function**: `/packages/haive-core/src/haive/core/graph/node/validation_router_v2.py` (lines 145-162)
4. **Route Assignment**: `/packages/haive-core/src/haive/core/engine/aug_llm/config.py` (lines 378, 393)

### Test Files
1. **Integration**: `/packages/haive-core/tests/integration/test_step3_nodes_with_tool_system.py`
2. **Route Testing**: `test_route_assignment.py` (created during investigation)
3. **Graph Analysis**: `test_simple_agent_graph.py` (created during investigation)

### Documentation Created
1. `validation_routing_investigation.md` - Detailed investigation
2. `validation_routing_graphs.md` - Visual diagrams
3. `comprehensive_tool_system_analysis.md` - System understanding
4. `test_mapping_and_coverage.md` - All related tests

## The Pattern

### Broken (SimpleAgent)
```
agent_node → validation → ❌ (no edges)
```

### Working (SimpleAgentV2)
```
agent_node → validation_v2 → validation_router_v2 → {
    parse_output (structured output)
    tool_node (regular tools)
    agent_node (errors)
}
```

## Why No Tests Caught This

1. **No SimpleAgent + structured_output_model tests exist**
2. **All working tests use agents with proper routing**
3. **Integration tests use other agents, not SimpleAgent**

## Alternative Solutions

1. **Use SimpleAgentV2** from archive (it works)
2. **Use a different agent** (ReactAgent, etc.)
3. **Skip validation** for structured output
4. **Runtime patch** to add edges after creation

## Verification Steps

1. **Confirm Bug**:
   ```python
   agent = SimpleAgent(engine=AugLLMConfig(structured_output_model=Plan[Task]))
   agent.run("Create plan")  # RecursionError
   ```

2. **Apply Fix**: Add conditional edges from validation

3. **Verify Fix**:
   ```python
   agent.run("Create plan")  # Works, returns Plan[Task]
   ```

## Key Learnings

1. **Validation nodes need routing** - They update state but don't decide flow
2. **Conditional edges are critical** - They implement the routing logic
3. **Test coverage matters** - This bug exists because no tests cover it
4. **Working examples exist** - SimpleAgentV2 shows the correct pattern

## Next Steps

1. **Decide on approach** (fix SimpleAgent or use SimpleAgentV2)
2. **Add test coverage** for SimpleAgent + structured output
3. **Verify fix** with all route types
4. **Check other agents** for similar issues