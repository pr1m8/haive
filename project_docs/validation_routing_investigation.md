# Validation Routing Investigation - SimpleAgent vs SimpleAgentV2

**Created**: 2025-01-29
**Status**: Investigation Complete, Solution Identified

## Executive Summary

SimpleAgent has a critical graph routing issue where the validation node has no outgoing edges, causing infinite recursion when using structured output models like `Plan[Task]`.

## The Problem

### Symptoms

1. **Error**: "Validation error: 'plan_task_generic'"
2. **RecursionError**: Graph executes 100+ times without stopping
3. **Works fine**: Without structured output (no validation node)

### Root Cause

SimpleAgent creates a validation node but doesn't add any edges FROM it:

```
START → agent_node → validation (DEAD END!)
```

## Investigation Timeline

### 1. Initial Discovery

- User reported validation errors still occurring despite believing structured output fixes were implemented
- Found that `Plan[Task]` gets sanitized to `plan_task_generic` causing name mismatches

### 2. Deep Dive into Validation Nodes

- **ValidationNodeConfigV2**: Uses LangGraph's prebuilt ValidationNode internally
- **ValidationNodeV2**: Custom implementation with proper routing logic
- Both expect exact schema names, but LLM uses sanitized names

### 3. Route Analysis

- Confirmed `Plan[Task]` correctly gets `parse_output` route when used as `structured_output_model`
- Found that `validation_router_v2` properly handles the `parse_output` route (lines 145-162)
- Route assignment is working correctly

### 4. Graph Structure Analysis

- Created test files to examine SimpleAgent's graph structure
- **Critical Finding**: SimpleAgent adds validation node but NO outgoing edges
- The graph literally has nowhere to go after validation

### 5. Comparison with Working Implementation

- SimpleAgentV2 (in archive) shows the correct pattern:
  - Uses `validation_v2` node to update state
  - Uses `validation_router_v2` as a CONDITIONAL EDGE function
  - Properly routes to tool_node, parse_output, or agent_node

### 6. Git History Check

- Current implementation from commit 06d7d354 (August 8, 2025)
- Major refactoring that consolidated agent base classes
- The `_add_validation_nodes` method clearly shows the missing edges

## Code Analysis

### SimpleAgent (BROKEN)

Location: `/packages/haive-agents/src/haive/agents/simple/agent.py`

```python
def _add_validation_nodes(self, graph: BaseGraph, engine_name: str, needs_tools: bool, needs_parsing: bool) -> None:
    # ... setup ...
    validation_config = ValidationNodeConfigV2(**validation_kwargs)
    graph.add_node("validation", validation_config)

    # Add edge TO validation
    if self.force_tool_use or self._always_needs_validation():
        graph.add_edge("agent_node", "validation")
    # BUT NO EDGES FROM VALIDATION!
```

### SimpleAgentV2 (WORKING)

Location: `/packages/haive-agents/src/haive/agents/simple/archive/agent_v2.py`

```python
# Correct pattern:
graph.add_node("validation_v2", validation_node_v2)

# Add CONDITIONAL EDGES from validation
graph.add_conditional_edges(
    "validation_v2",
    validation_router_v2,  # This is a routing FUNCTION
    {
        "agent_node": "agent_node",
        "tool_node": "tool_node",
        "parse_output": "parse_output"
    }
)
```

## Key Files Referenced

### Core Implementation Files

1. `/packages/haive-agents/src/haive/agents/simple/agent.py` - The broken SimpleAgent
2. `/packages/haive-agents/src/haive/agents/simple/archive/agent_v2.py` - Working reference implementation
3. `/packages/haive-core/src/haive/core/graph/node/validation_node_config_v2.py` - Validation node implementation
4. `/packages/haive-core/src/haive/core/graph/node/validation_router_v2.py` - Routing function (lines 145-162 handle parse_output)

### Test Files Created During Investigation

1. `test_simple_agent_graph.py` - Confirmed no outgoing edges from validation
2. `test_simple_agent_validation_edge.py` - Detailed edge analysis
3. `test_route_assignment.py` - Confirmed routes are assigned correctly

### Reference Tests in haive-core

1. `/packages/haive-core/tests/engine/tool/test_comprehensive_tool_integration.py` - Shows tool routing patterns
2. `/packages/haive-core/tests/integration/test_step3_nodes_with_tool_system.py` - Shows validation node integration
3. `/packages/haive-core/tests/routing/test_structured_output_routing_refactor.py` - Shows routing refactor patterns

## Understanding the Components

### 1. Validation Node vs Validation Router

- **ValidationNodeConfigV2**: A NODE that validates tool calls and creates ToolMessages
- **validation_router_v2**: A FUNCTION that decides where to route based on tool routes

### 2. Route Types

- `parse_output`: For structured output models (like `Plan[Task]`)
- `pydantic_model`: For BaseModel validation (error case)
- `langchain_tool`: For regular tool execution
- `pydantic_tool`: For BaseModel with `__call__` method

### 3. How It Should Work

1. agent_node produces AIMessage with tool calls
2. validation node validates and creates ToolMessages
3. validation_router_v2 examines tool routes and decides next node:
   - `parse_output` route → goes to parse_output node
   - `langchain_tool` route → goes to tool_node
   - Errors → back to agent_node

## Proposed Solution

Add the missing conditional edges from validation node:

```python
from haive.core.graph.node.validation_router_v2 import validation_router_v2

def _add_validation_nodes(self, ...):
    # ... existing code to create validation node ...

    # ADD THIS - conditional edges FROM validation
    routing_map = {}
    if needs_tools:
        routing_map["tool_node"] = "tool_node"
    if needs_parsing:
        routing_map["parse_output"] = "parse_output"
    routing_map["agent_node"] = "agent_node"  # For errors

    graph.add_conditional_edges(
        "validation",
        validation_router_v2,
        routing_map
    )
```

## Alternative Approaches to Consider

1. **Use SimpleAgentV2**: The archive version works correctly
2. **Create New Agent**: Build a fresh implementation with proper routing
3. **Patch at Runtime**: Add edges dynamically after graph creation
4. **Different Validation Strategy**: Skip validation for structured output

## Questions to Resolve

1. Why was the routing removed in the consolidation?
2. Is there a different intended pattern for SimpleAgent?
3. Should we use SimpleAgentV2 instead?
4. Are there other agents with the same issue?

## Next Steps

1. Confirm the approach with the team
2. Test the fix thoroughly with all route types
3. Check other agents for similar issues
4. Update tests to prevent regression
