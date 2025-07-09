# Comprehensive Guide to Haive Validation Nodes

## Overview

The Haive framework includes multiple validation node implementations that have evolved to handle tool call validation and routing. This guide provides complete information about which nodes to use, their features, and dynamic choice model support.

## Quick Answer: Which Node to Use?

### 🎯 **Use `UnifiedValidationNode`** for new implementations

```python
from haive.core.graph.node.unified_validation_node import UnifiedValidationNodeConfig

validation_node = UnifiedValidationNodeConfig(
    name="validation",
    engine_name="main_engine",
    parallel_execution=True,  # Enables Send for parallel tools
    create_tool_messages=True
)
```

## All Validation Nodes Comparison

| Node | Type | Status | Dynamic Choice | Key Features |
|------|------|--------|----------------|--------------|
| **UnifiedValidationNode** | Single Node | ✅ **RECOMMENDED** | ❌ No | Single node, Command/Send routing, Pydantic compliant |
| ValidationNodeConfig | Conditional Edge | ❌ Legacy | ❌ No | Can't update state properly |
| ValidationNodeV2 + router | Node + Router | ⚠️ Working | ❌ No | Two-part system, extra step |
| ValidationNodeConfigV2 | Simple Node | ⚠️ Limited | ❌ No | Basic Command routing |
| ValidationNodeWithRouting | Complex Node | ⚠️ Complex | ❌ No | Routing state tracking |
| StateUpdatingValidationNode | Mode-based | ⚠️ Special | ❌ No | STRICT/PARTIAL/PERMISSIVE modes |
| RoutingValidationNode | Send-focused | ⚠️ Special | ❌ No | Send-based parallel routing |
| StatefulValidationNode | History-tracking | ⚠️ Special | ❌ No | Validation analytics |

## Dynamic Choice Model Support

### What is DynamicChoiceModel?

`DynamicChoiceModel` is a Pydantic model builder that dynamically generates choice models with runtime-determined options:

```python
from haive.core.common.models.dynamic_choice_model import DynamicChoiceModel

# Create dynamic choice builder
choice_builder = DynamicChoiceModel(
    options=["agent1", "agent2", "agent3"],
    include_end=True
)

# Get current choice model
ChoiceModel = choice_builder.current_model
# Creates a model that validates: choice ∈ ["agent1", "agent2", "agent3", "END"]

# Add/remove options dynamically
choice_builder.add_option("agent4")
choice_builder.remove_option_by_name("agent2")
```

### Current Status: No Validation Nodes Use DynamicChoiceModel

**None of the current validation nodes directly integrate with `DynamicChoiceModel`**. The dynamic choice functionality is primarily used in:

1. **Dynamic Supervisor Agents** - For runtime agent selection
2. **StructuredOutputMixin** - For dynamic tool configuration
3. **Game States** - For dynamic player/action choices

### Why Don't Validation Nodes Use It?

Validation nodes focus on:
- Validating tool calls from AIMessages
- Routing to appropriate tool execution nodes
- Creating ToolMessages for validation results

They don't need dynamic choice models because:
- Tool routes are determined by the engine's `tool_routes` dictionary
- Routing destinations are fixed node names in the graph
- Validation is based on tool existence, not dynamic choices

## UnifiedValidationNode Deep Dive

### Architecture

```python
class UnifiedValidationNodeConfig(BaseNodeConfig):
    """
    Unified validation node that combines tool validation and routing.
    
    Key Features:
    - Single node (no separate router)
    - Proper Pydantic patterns (no custom __init__)
    - Command/Send routing support
    - Parallel tool execution
    """
    
    # Configuration
    engine_name: str  # Engine to get tool routes from
    tool_node: str = "tool_node"  # Langchain tool execution
    parse_output_node: str = "parse_output"  # Structured output parsing
    agent_node: str = "agent_node"  # Return to agent on errors
    create_tool_messages: bool = True  # Create ToolMessages
    parallel_execution: bool = True  # Use Send for parallel
```

### How It Works

1. **Analyzes Tool Calls**:
   ```python
   # Finds last AIMessage with tool_calls
   for msg in reversed(messages):
       if isinstance(msg, AIMessage) and msg.tool_calls:
           # Process each tool call
   ```

2. **Determines Tool Route**:
   ```python
   # Check engine.tool_routes
   route = engine.tool_routes.get(tool_name)
   # Returns: "pydantic_model", "langchain_tool", "function", etc.
   ```

3. **Routes Appropriately**:
   - `pydantic_model` → Validates and routes to `parse_output_node`
   - `langchain_tool` → Routes to `tool_node` for execution
   - Unknown tools → Creates error ToolMessage, routes to `agent_node`

4. **Supports Parallel Execution**:
   ```python
   if parallel_execution and multiple_tools:
       return Command(goto=[
           Send("tool_node", {"tool_call": tool1}),
           Send("tool_node", {"tool_call": tool2})
       ])
   ```

### Integration Example

```python
from haive.core.graph.state_graph.base_graph2 import BaseGraph
from haive.core.graph.node.unified_validation_node import UnifiedValidationNodeConfig

# Build graph
graph = BaseGraph()

# Add unified validation
validation = UnifiedValidationNodeConfig(
    name="validate_and_route",
    engine_name="main_engine"
)

# Add nodes
graph.add_node("agent", agent_node)
graph.add_node("validate_and_route", validation)
graph.add_node("tool_node", tool_executor)
graph.add_node("parse_output", output_parser)

# Connect
graph.add_edge("agent", "validate_and_route")
# Validation node handles routing internally via Command
```

## Migration Guide

### From ValidationNodeConfig (Legacy)

```python
# OLD: Conditional edge approach
graph.add_conditional_edge(
    "agent",
    validation_node_config,  # Function that returns route
    {
        "tool_node": "tool_node",
        "parse_output": "parse_output",
        "END": END
    }
)

# NEW: Proper node approach
graph.add_node("validation", UnifiedValidationNodeConfig(
    engine_name="main_engine"
))
graph.add_edge("agent", "validation")
# Routing handled internally by validation node
```

### From ValidationNodeV2 + Router

```python
# OLD: Two-part system
graph.add_node("validation", ValidationNodeConfigV2(...))
graph.add_node("router", validation_router_v2)
graph.add_edge("agent", "validation")
graph.add_edge("validation", "router")

# NEW: Single unified node
graph.add_node("validation", UnifiedValidationNodeConfig(...))
graph.add_edge("agent", "validation")
```

## Special Use Cases

### Need Validation History?

Use `StatefulValidationNode`:
```python
# Tracks validation patterns and statistics
stateful_validation = StatefulValidationNode(
    history_limit=100,
    track_patterns=True
)
```

### Need Strict/Partial Validation?

Use `StateUpdatingValidationNode`:
```python
# Different validation modes
validation = StateUpdatingValidationNode(
    validation_mode="PARTIAL"  # or "STRICT", "PERMISSIVE"
)
```

### Need Pure Send-based Routing?

Use `RoutingValidationNode`:
```python
# Always returns Send objects for routing
routing_validation = RoutingValidationNode(
    always_use_send=True
)
```

## Best Practices

1. **Always Use Proper Nodes**: Never use conditional edges for validation
2. **Let Engines Handle Tool Routes**: Don't hardcode tool type detection
3. **Use UnifiedValidationNode**: Unless you have specific requirements
4. **Enable Parallel Execution**: For better performance with multiple tools
5. **Create ToolMessages**: For proper conversation history

## Common Pitfalls

1. **Using Legacy ValidationNodeConfig**: It can't update state reliably
2. **Manual Tool Type Detection**: Use `engine.tool_routes` instead
3. **Forgetting Engine Context**: Always pass `engine_name`
4. **Complex Routing Logic**: Keep it simple, let the node handle it
5. **Missing Error Handling**: Always create error ToolMessages

## Future: Dynamic Choice Integration?

While current validation nodes don't use `DynamicChoiceModel`, future implementations could:

1. **Dynamic Tool Selection**: Choose which tools to validate based on context
2. **Conditional Routing**: Dynamic destination selection based on validation results
3. **Adaptive Validation**: Change validation strictness based on conversation state

For now, use `UnifiedValidationNode` for clean, maintainable validation and routing.