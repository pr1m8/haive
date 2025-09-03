# Test Mapping and Coverage Analysis

**Created**: 2025-01-29
**Purpose**: Comprehensive mapping of all tests related to validation, routing, and structured output

## Test Categories

### 1. Core Tool System Tests

#### `/packages/haive-core/tests/engine/tool/`

**test_comprehensive_tool_integration.py**

- ✅ `test_basic_tool_creation_and_routing` - Basic tool → route assignment
- ✅ `test_pydantic_model_tool_creation` - Pydantic models as tools
- ✅ `test_structured_output_tool_integration` - Structured output tools
- ✅ `test_no_tool_duplication_bug` - Verifies duplication fix
- ✅ `test_dynamic_tool_addition` - Runtime tool addition

**test_tool_engine.py**

- ✅ `test_create_structured_output_tool` - ToolEngine structured output
- ✅ `test_create_state_tool` - State-aware tools
- ✅ `test_tool_validation` - Schema validation

### 2. Validation Node Tests

#### `/packages/haive-core/tests/graph/node/`

**test_validation_node_v2.py**

- ✅ `test_validation_with_tool_routes` - Route-based validation
- ✅ `test_pydantic_model_validation` - Pydantic model handling
- ✅ `test_error_handling` - Validation errors

**test_validation_node_config_v2.py**

- ✅ `test_langgraph_validation_node` - LangGraph integration
- ✅ `test_schema_name_matching` - Name sanitization issues

### 3. Routing Tests

#### `/packages/haive-core/tests/routing/`

**test_validation_router_v2.py**

- ✅ `test_parse_output_routing` - Structured output → parse_output
- ✅ `test_tool_node_routing` - Regular tools → tool_node
- ✅ `test_error_routing` - Errors → agent_node

**test_structured_output_routing_refactor.py**

- 🔄 Shows proposed `structured_output` route (not implemented)

### 4. Integration Tests

#### `/packages/haive-core/tests/integration/`

**test_step3_nodes_with_tool_system.py**

- ✅ `test_validation_node_v2_with_aug_llm_config_routes` - Full integration
- ✅ `test_tool_node_config_with_engine_tool_routes` - Tool filtering
- ✅ `test_validation_node_with_pydantic_model_routing` - Pydantic routing
- ✅ `test_comprehensive_node_tool_workflow` - End-to-end workflow

### 5. AugLLMConfig Tests

#### `/packages/haive-core/tests/engine/aug_llm/`

**test_aug_llm_config_v2.py**

- ✅ `test_structured_output_model_routing` - Model → parse_output
- ✅ `test_force_tool_use` - Tool-based structured output
- ✅ `test_tool_route_assignment` - Route assignment logic

### 6. Agent Tests (Where the Gap Is!)

#### `/packages/haive-agents/tests/simple/`

**test_simple_agent.py**

- ❌ **MISSING**: Test with structured_output_model
- ❌ **MISSING**: Test validation routing
- ✅ Basic agent creation and execution

## Critical Test Patterns

### 1. Route Syncing Pattern

```python
# Appears in EVERY validation node test:
validation_node.clear_tool_routes()
for tool_name, route in config.tool_routes.items():
    validation_node.set_tool_route(tool_name, route)
```

### 2. Structured Output Route Assignment

```python
# In AugLLMConfig (lines 378, 393):
self.set_tool_route(sanitized_name, "parse_output", metadata)
```

### 3. Validation Router Decision Logic

```python
# validation_router_v2.py (lines 145-162):
elif route == "parse_output":
    if has_tool_error_v2(tool_message):
        destinations.add("agent_node")  # Error
    else:
        destinations.add("parse_output")  # Success
```

## Test Coverage Gaps

### 1. SimpleAgent Specific

- ❌ No test for SimpleAgent + structured_output_model
- ❌ No test for SimpleAgent validation routing
- ❌ No test for SimpleAgent graph structure

### 2. Edge Configuration

- ❌ No test verifying conditional edges from validation
- ❌ No test for missing edge scenarios

### 3. Integration Gaps

- ❌ No test for Plan[Task] specifically
- ❌ No test for recursion limit scenarios

## Key Test Insights

### 1. All Working Tests Show Conditional Edges

Every successful validation test includes routing FROM validation node

### 2. Route Assignment Works

Tests confirm `parse_output` route is correctly assigned

### 3. Validation Node Works

The node itself processes correctly - it's the routing that's broken

### 4. The Pattern is Consistent

```
validation_node → validation_router_v2 → destination
```

## Test-Based Evidence

### Evidence for parse_output Route

From `test_route_assignment.py`:

```
🎯 KEY FINDING: plan_task_generic gets route: parse_output
   ✅ This is CORRECT for structured output!
```

### Evidence for Routing Function

From `agent_v2.py`:

```python
graph.add_conditional_edges("validation_v2", validation_router_v2, routing_map)
```

### Evidence for Missing Edges

From our graph inspection:

```
Edges from validation: set()  # EMPTY!
```

## Recommended Test Suite

### 1. Create Failing Test

```python
def test_simple_agent_structured_output_recursion():
    """Test that SimpleAgent works with structured output."""
    agent = SimpleAgent(
        name="planner",
        engine=AugLLMConfig(
            structured_output_model=Plan[Task],
            recursion_limit=5  # Prevent infinite loop
        )
    )
    with pytest.raises(RecursionError):
        agent.run("Create a plan")
```

### 2. Create Success Test (After Fix)

```python
def test_simple_agent_structured_output_success():
    """Test that SimpleAgent works with structured output after fix."""
    agent = SimpleAgent(
        name="planner",
        engine=AugLLMConfig(structured_output_model=Plan[Task])
    )
    result = agent.run("Create a plan with 2 steps")
    assert isinstance(result, Plan[Task])
    assert len(result.steps) <= 2
```

## Summary

The tests clearly show:

1. ✅ Tool routing works (`parse_output` route assigned)
2. ✅ Validation node works (processes tool calls)
3. ✅ Routing function works (validation_router_v2)
4. ❌ SimpleAgent missing edges FROM validation node
5. ❌ No tests catch this because no SimpleAgent + structured output tests exist
