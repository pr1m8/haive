# StateUpdatingValidationNode Integration Guide

## Overview

This guide demonstrates how to replace placeholder validation nodes in existing agents with the new `StateUpdatingValidationNode` that provides both state updates and dynamic routing capabilities.

## Problem Statement

The original `SimpleAgent` in `haive-agents/simple/agent.py` was using:

```python
# OLD APPROACH: Placeholder + separate routing
graph.add_node("validation", placeholder_node)  # Does nothing!

validation_config = ValidationNodeConfig(...)  # Only routing, no state updates
graph.add_conditional_edges("validation", validation_config, routing_map)
```

**Issues:**

- `placeholder_node` does nothing - just returns `Command(update={})`
- No state updates from validation results
- Validation logic separated from routing logic
- Limited flexibility and no validation persistence

## Solution: StateUpdatingValidationNode

The `StateUpdatingValidationNode` provides a **dual-function approach**:

1. **Node Function**: Updates state with validation results
2. **Router Function**: Routes based on updated validation state

### Key Integration Pattern

```python
# NEW APPROACH: Actual validation + integrated routing
validation_node = StateUpdatingValidationNode(
    engine_name=self.engine.name,
    validation_mode=ValidationMode.PARTIAL,
    update_messages=True,
    track_error_tools=True
)

# Get both functions
state_updater = validation_node.create_node_function()    # Updates state
router_func = validation_node.create_router_function()     # Routes from state

# Add to graph
graph.add_node("state_validator", state_updater)          # State updates
graph.add_node("validation_router", router_func)          # Dynamic routing
graph.add_edge("state_validator", "validation_router")    # Sequential flow
```

## Implementation Example: SimpleAgentWithValidation

### Core Changes

1. **Replace Placeholder Node**:

   ```python
   # OLD
   graph.add_node("validation", placeholder_node)

   # NEW
   validation_node = self._create_validation_node()
   state_updater = validation_node.create_node_function()
   graph.add_node("state_validator", state_updater)
   ```

2. **Add Dynamic Router**:

   ```python
   # NEW
   router_func = validation_node.create_router_function()
   graph.add_node("validation_router", router_func)
   ```

3. **Sequential Flow**:
   ```python
   # Agent → State Validator → Router → Tools
   graph.add_edge("agent_node", "state_validator")
   graph.add_edge("state_validator", "validation_router")
   # Router creates Send branches dynamically
   ```

### Configuration

```python
def _create_validation_node(self) -> StateUpdatingValidationNode:
    """Create properly configured validation node."""

    # Map routes to available nodes
    route_mapping = {}
    if self._needs_tool_node():
        route_mapping.update({
            "langchain_tool": "tool_node",
            "function": "tool_node"
        })
    if self._needs_parser_node():
        route_mapping["pydantic_model"] = "parse_output"

    return StateUpdatingValidationNode(
        name="state_validator",
        engine_name=self.engine.name,
        validation_mode=self.validation_mode,
        update_messages=self.update_validation_messages,
        track_error_tools=self.track_error_tools,
        route_to_node_mapping=route_mapping
    )
```

## Graph Flow Comparison

### Before (Placeholder)

```
START → agent_node → validation (placeholder) → routing_logic → tool_node → END
                  ↘ END (no tools)
```

### After (StateUpdatingValidationNode)

```
START → agent_node → state_validator → validation_router → [Send branches] → END
                  ↘ END (no tools)                        ↘ agent_node (errors)
```

## Key Benefits

### 1. **Actual Validation Logic**

- Validates tool calls against available tools
- Checks tool arguments and schemas
- Provides detailed error information

### 2. **State Persistence**

- Validation results stored in `state.validation_state`
- Tool message statuses tracked in `state.tool_message_status`
- Branch conditions updated for complex routing

### 3. **Multiple Validation Modes**

- **STRICT**: Any failure routes to agent
- **PARTIAL**: Continue with valid tools (default)
- **PERMISSIVE**: Only route to agent if all fail

### 4. **Dynamic Routing**

- Router function adapts to validation state changes
- Creates Send objects for parallel tool execution
- Supports complex conditional logic

### 5. **Error Tracking**

- Failed tool calls tracked in `state.error_tool_calls`
- Validation metadata added to tool calls
- Optional error messages added to conversation

## State Schema Integration

The validation node integrates seamlessly with state schemas:

```python
# State schemas provide the interface
class EnhancedToolState(ToolState):
    validation_state: ValidationRoutingState

    def get_tool_calls(self) -> List[Dict[str, Any]]:
        """Computed field - extracts tool calls automatically."""

    def apply_validation_results(self, validation_state):
        """Interface for validation node to update state."""

    def should_continue_to_tools(self) -> bool:
        """Conditional logic for routing."""
```

## Usage Examples

### Basic Usage

```python
agent = SimpleAgentWithValidation.from_engine(engine)
result = agent.invoke({"query": "process this"})
```

### With Structured Output

```python
agent = SimpleAgentWithValidation(
    engine=engine,
    structured_output_model=TaskResult,
    validation_mode=ValidationMode.PARTIAL
)
```

### Strict Validation

```python
agent = SimpleAgentWithValidation.create_strict_validation(engine)
# Any validation failure routes to agent for clarification
```

### Upgrade Existing Agent

```python
old_agent = SimpleAgent(engine=engine)
new_agent = upgrade_simple_agent_with_validation(old_agent)
```

## Migration Steps

### 1. Identify Placeholder Usage

Look for patterns like:

```python
graph.add_node("validation", placeholder_node)
```

### 2. Create StateUpdatingValidationNode

```python
validation_node = StateUpdatingValidationNode(
    engine_name=engine_name,
    validation_mode=ValidationMode.PARTIAL,
    # ... other config
)
```

### 3. Replace Node and Add Router

```python
# Replace placeholder
state_updater = validation_node.create_node_function()
graph.add_node("state_validator", state_updater)

# Add router
router_func = validation_node.create_router_function()
graph.add_node("validation_router", router_func)

# Connect
graph.add_edge("state_validator", "validation_router")
```

### 4. Update Conditional Edges

```python
# OLD
graph.add_conditional_edges("validation", validation_config, routing_map)

# NEW - Router function handles routing via Send objects
# No explicit edges needed for router - Send objects create branches
```

### 5. Test Validation Modes

- Test with valid tools
- Test with invalid tools
- Test with mixed scenarios
- Verify state persistence

## Debugging Tips

### 1. **Check Engine Registration**

```python
from haive.core.engine.base import EngineRegistry
registry = EngineRegistry.get_instance()
engine = registry.find(engine_name)  # Should not be None
```

### 2. **Verify Tool Routes**

```python
print(f"Tool routes: {state.tool_routes}")
print(f"Available tools: {[t.name for t in state.tools]}")
```

### 3. **Inspect Validation State**

```python
if state.validation_state:
    summary = state.validation_state.get_routing_decision()
    print(f"Validation summary: {summary}")
```

### 4. **Monitor Send Creation**

```python
# Router function logs Send creation
[validation_router] Created 3 Send branches
```

## Performance Considerations

1. **State Updates**: Validation results persist in state - no re-computation
2. **Parallel Execution**: Send objects enable parallel tool execution
3. **Engine Lookup**: Engine registered once, reused for validation
4. **Route Caching**: Tool routes computed once per state update

## Best Practices

1. **Use Appropriate Validation Mode**:
   - STRICT for critical applications
   - PARTIAL for balanced workflow (default)
   - PERMISSIVE for experimental/development

2. **Configure Error Tracking**:

   ```python
   track_error_tools=True,  # For debugging
   update_messages=True     # For user feedback
   ```

3. **Map Routes to Available Nodes**:

   ```python
   route_mapping = {
       "langchain_tool": "tool_node",
       "pydantic_model": "parser_node",
       # Only include nodes that exist in graph
   }
   ```

4. **Handle State Schema Evolution**:
   - Use `apply_validation_results()` for consistent updates
   - Leverage computed fields for tool call extraction
   - Implement conditional methods for complex routing

## Conclusion

The `StateUpdatingValidationNode` transforms placeholder validation into a powerful, stateful validation and routing system. By providing both state updates and dynamic routing in a unified interface, it enables sophisticated agent workflows while maintaining clean separation of concerns.

The integration pattern demonstrated in `SimpleAgentWithValidation` shows how to replace placeholders with actual functionality, providing a template for upgrading other agents in the Haive ecosystem.

Key takeaway: **Replace placeholders with actual validation logic that persists state and enables dynamic routing based on validation results.**
