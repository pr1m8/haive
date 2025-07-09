# LangGraph Validation Nodes with Send Branching Guide

## Overview

This guide explains how LangGraph's validation nodes work with Send branching for tool routing in the haive codebase. The pattern allows for sophisticated tool call validation and dynamic routing based on validation results.

## Key Concepts

### 1. Validation Nodes

Validation nodes are special nodes in the graph that:

- Receive tool calls from AI messages
- Validate each tool call based on rules and state
- Determine routing for each tool call
- Return routing decisions using Send objects or node names

### 2. Send Objects

`Send` objects in LangGraph create parallel execution branches:

```python
from langgraph.types import Send

# Creates a new execution branch that sends data to a node
Send(node_name="tools", data={"tool_call": {...}})
```

### 3. Tool Routes

Tool routes determine how tools are categorized and routed:

- `langchain_tool`: LangChain tool instances
- `pydantic_model`: Pydantic model tools
- `function`: Function-based tools
- `retriever`: Retriever tools
- `agent`: Sub-agent tools

## Validation Node Pattern

### Basic Structure

```python
def validation_node(state: EnhancedToolState) -> Union[str, List[Send]]:
    """Validation node that routes tool calls based on validation."""

    # 1. Get tool calls from last AI message
    tool_calls = state.messages.get_tool_calls_from_message()
    if not tool_calls:
        return END

    # 2. Validate each tool call
    validation_state = ValidationStateManager.create_routing_state()

    for tool_call in tool_calls:
        # Perform validation logic
        result = validate_tool_call(tool_call, state)
        validation_state.add_validation_result(result)

    # 3. Apply validation results to state
    state.apply_validation_results(validation_state)

    # 4. Create Send objects for routing
    return create_routing_sends(validation_state, tool_calls)
```

### Validation Process

1. **Extract Tool Calls**: Get tool calls from the AI message
2. **Validate Each Call**: Check against rules, permissions, and state
3. **Determine Routes**: Map each valid tool to its destination node
4. **Create Send Objects**: Generate Send objects for parallel execution

## Routing Decisions

### Return Types

Validation nodes can return:

1. **List[Send]**: For routing multiple tool calls to different nodes
2. **String**: For routing to a single node (e.g., "agent")
3. **END**: To terminate processing

### Example Routing Logic

```python
def create_routing_sends(validation_state, tool_calls):
    sends = []

    # Group valid tools by target node
    tools_by_node = {}
    for result in validation_state.get_valid_tool_calls():
        target = result.target_node or "tools"
        if target not in tools_by_node:
            tools_by_node[target] = []
        tools_by_node[target].append(result)

    # Create Send for each tool
    for node_name, tools in tools_by_node.items():
        for tool in tools:
            sends.append(Send(node_name, tool))

    # Handle overall routing
    if sends:
        return sends  # Execute valid tools
    elif validation_state.should_return_to_agent():
        return "agent"  # Need clarification
    else:
        return END  # No valid tools
```

## Tool Route Mapping

### Route to Node Mapping

```python
def get_target_node_for_route(tool_route: str) -> str:
    """Map tool routes to target nodes."""
    route_to_node = {
        "langchain_tool": "langchain_tools",
        "pydantic_model": "pydantic_tools",
        "function": "function_tools",
        "retriever": "retriever_tools",
        "agent": "sub_agents",
    }
    return route_to_node.get(tool_route, "tools")
```

### Dynamic Route Configuration

```python
# Configure which routes an engine accepts
state.configure_engine_routes("llm", ["langchain_tool", "function"])
state.configure_engine_routes("retriever", ["retriever"])

# Add tools with specific routes
state.add_tool_enhanced(
    tool=my_tool,
    route="langchain_tool",
    category="execution",
    priority=10,
    target_engine="llm"
)
```

## Validation States

### ValidationStatus Enum

- `PENDING`: Not yet validated
- `VALID`: Passed validation
- `INVALID`: Failed validation but may be correctable
- `ERROR`: Critical error, cannot proceed
- `SKIPPED`: Skipped validation

### RouteRecommendation Enum

- `EXECUTE`: Execute the tool
- `RETRY`: Retry with corrections
- `SKIP`: Skip this tool
- `REDIRECT`: Redirect to different tool
- `AGENT`: Return to agent for clarification
- `END`: End processing

## Example Implementation

### Complete Validation Node

```python
def validation_node(state: EnhancedToolState) -> Union[str, List[Send]]:
    """Full validation node implementation."""

    # Get tool calls
    last_ai = state.messages.last_ai_message
    if not last_ai or not hasattr(last_ai, "tool_calls"):
        return END

    tool_calls = last_ai.tool_calls
    validation_state = ValidationStateManager.create_routing_state()

    # Validate each tool
    for tool_call in tool_calls:
        tool_name = tool_call.get("name")
        tool_id = tool_call.get("id")
        tool_args = tool_call.get("args", {})

        # Get tool route from state
        tool_route = state.tool_routes.get(tool_name, "unknown")

        # Validation logic
        if tool_name not in state.tool_routes:
            # Unknown tool
            result = ValidationStateManager.create_validation_result(
                tool_call_id=tool_id,
                tool_name=tool_name,
                status=ValidationStatus.INVALID,
                errors=[f"Unknown tool: {tool_name}"],
                route_recommendation=RouteRecommendation.SKIP,
            )
        elif not _check_permissions(tool_name, state):
            # Permission denied
            result = ValidationStateManager.create_validation_result(
                tool_call_id=tool_id,
                tool_name=tool_name,
                status=ValidationStatus.ERROR,
                errors=["Permission denied"],
                route_recommendation=RouteRecommendation.AGENT,
            )
        elif missing_args := _check_required_args(tool_name, tool_args, state):
            # Missing required arguments
            result = ValidationStateManager.create_validation_result(
                tool_call_id=tool_id,
                tool_name=tool_name,
                status=ValidationStatus.INVALID,
                errors=[f"Missing args: {missing_args}"],
                route_recommendation=RouteRecommendation.RETRY,
                corrected_args=_get_default_args(tool_name),
            )
        else:
            # Valid tool call
            target_node = get_target_node_for_route(tool_route)
            priority = state.tool_priorities.get(tool_name, 0)

            result = ValidationStateManager.create_validation_result(
                tool_call_id=tool_id,
                tool_name=tool_name,
                status=ValidationStatus.VALID,
                route_recommendation=RouteRecommendation.EXECUTE,
                target_node=target_node,
                priority=priority,
            )

        validation_state.add_validation_result(result)

    # Apply results
    state.apply_validation_results(validation_state)

    # Create routing
    sends = []
    for result in validation_state.get_valid_tool_calls():
        # Find original tool call
        tool_call = next(
            (tc for tc in tool_calls if tc.get("id") == result.tool_call_id),
            None
        )
        if tool_call:
            # Enhance with validation metadata
            enhanced_call = {
                **tool_call,
                "validation": {
                    "status": result.status.value,
                    "priority": result.priority,
                    "target_node": result.target_node,
                }
            }
            sends.append(Send(result.target_node, enhanced_call))

    # Return routing decision
    if sends:
        return sends
    elif validation_state.should_return_to_agent():
        return "agent"
    else:
        return END
```

## Graph Construction

### Building a Graph with Validation

```python
def build_graph_with_validation():
    graph = StateGraph(EnhancedToolState)

    # Add nodes
    graph.add_node("agent", agent_node)
    graph.add_node("validation", validation_node)
    graph.add_node("langchain_tools", langchain_tools_node)
    graph.add_node("pydantic_tools", pydantic_tools_node)
    graph.add_node("function_tools", function_tools_node)

    # Entry point
    graph.set_entry_point("agent")

    # Conditional edge from agent
    graph.add_conditional_edges(
        "agent",
        lambda state: "validation" if state.messages.has_tool_calls else END,
    )

    # Validation node uses Send for routing
    # No explicit edges needed - Send handles routing

    # Tool nodes return to agent
    for tool_node in ["langchain_tools", "pydantic_tools", "function_tools"]:
        graph.add_edge(tool_node, "agent")

    return graph.compile()
```

## Best Practices

### 1. Validation Logic

- Validate tool existence first
- Check permissions and security policies
- Validate required arguments
- Provide helpful error messages
- Suggest corrections when possible

### 2. Route Management

- Use consistent route naming
- Map routes to appropriate nodes
- Configure engine-specific routes
- Document custom routes

### 3. Send Usage

- Create one Send per tool call for parallel execution
- Include validation metadata in sent data
- Handle Send creation errors gracefully
- Group by target node when beneficial

### 4. State Updates

- Always apply validation results to state
- Track validation history
- Update tool message statuses
- Maintain branch conditions

## Common Patterns

### Pattern 1: Security Validation

```python
if _is_dangerous_tool(tool_name) and not state.allow_dangerous_tools:
    result = ValidationStateManager.create_validation_result(
        tool_call_id=tool_id,
        tool_name=tool_name,
        status=ValidationStatus.ERROR,
        errors=["Tool blocked by security policy"],
        route_recommendation=RouteRecommendation.END,
    )
```

### Pattern 2: Argument Correction

```python
if missing_args := _get_missing_args(tool_name, tool_args):
    corrected_args = {**tool_args, **_get_defaults(tool_name, missing_args)}
    result = ValidationStateManager.create_validation_result(
        tool_call_id=tool_id,
        tool_name=tool_name,
        status=ValidationStatus.INVALID,
        errors=[f"Missing: {missing_args}"],
        corrected_args=corrected_args,
        route_recommendation=RouteRecommendation.RETRY,
    )
```

### Pattern 3: Priority-Based Routing

```python
# Route high-priority tools to dedicated nodes
if state.tool_priorities.get(tool_name, 0) > 50:
    target_node = "high_priority_tools"
else:
    target_node = get_target_node_for_route(tool_route)
```

## Debugging Tips

1. **Log Validation Results**:

   ```python
   logger.info(f"Validation summary: {validation_state.get_routing_summary()}")
   ```

2. **Track Send Creation**:

   ```python
   for send in sends:
       logger.debug(f"Creating Send to {send.node} with data: {send.data}")
   ```

3. **Monitor State Changes**:

   ```python
   logger.debug(f"Tool message statuses: {state.tool_message_status}")
   ```

4. **Validate Route Configuration**:
   ```python
   logger.info(f"Engine routes: {state.engine_route_config}")
   ```

## Conclusion

The validation node pattern with Send branching provides a powerful way to:

- Validate tool calls before execution
- Route tools to appropriate processing nodes
- Handle errors and provide corrections
- Execute tools in parallel
- Maintain comprehensive state tracking

This pattern is essential for building robust, production-ready agents that can handle complex tool interactions safely and efficiently.
