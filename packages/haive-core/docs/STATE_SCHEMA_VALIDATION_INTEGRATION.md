# StateUpdatingValidationNode Integration with State Schemas

## Overview

The `StateUpdatingValidationNode` is designed to work seamlessly with Haive's state schema system, particularly `ToolState` and `EnhancedToolState`. This integration provides powerful validation, routing, and state management capabilities for complex agent workflows.

## State Schema Hierarchy

```
MessagesState (Base)
    ├── messages: List[BaseMessage]
    ├── Computed fields for message extraction
    └── Engine setup and management

ToolState (extends MessagesState)
    ├── tools: List[Any]
    ├── tool_routes: Dict[str, str]
    ├── engine_route_config: Dict[str, List[str]]
    ├── get_tool_calls() computed field
    └── Tool synchronization from engines

EnhancedToolState (extends ToolState)
    ├── validation_state: ValidationRoutingState
    ├── tool_metadata: Dict[str, Dict[str, Any]]
    ├── tool_message_status: Dict[str, str]
    ├── branch_conditions: Dict[str, Any]
    ├── apply_validation_results() method
    └── Conditional branching methods
```

## Key Integration Points

### 1. Computed Fields and Tool Extraction

The state schemas provide computed fields that automatically extract tool calls:

```python
# In ToolState/EnhancedToolState
@computed_field
def get_tool_calls(self) -> List[Dict[str, Any]]:
    """Extract tool calls from last AI message."""
    if not self.messages:
        return []

    last_msg = self.messages[-1]
    if isinstance(last_msg, AIMessage) and last_msg.tool_calls:
        return last_msg.tool_calls
    return []
```

The validation node uses this:

```python
def validation_node(state: EnhancedToolState) -> EnhancedToolState:
    # Uses state's computed field
    tool_calls = state.get_tool_calls()
    # ... validation logic
```

### 2. Tool and Route Management

State schemas manage tools and their routes:

```python
# State automatically maintains
state.tools = [search_tool, calculator, schema_parser]
state.tool_routes = {
    "search_tool": "langchain_tool",
    "calculator": "function",
    "schema_parser": "pydantic_model"
}
```

Validation node validates against these:

```python
def _validate_tool_call(self, tool_call, state):
    tool_name = tool_call["name"]

    # Check against state's tools
    available_tools = {getattr(t, 'name', str(t)): t for t in state.tools}
    if tool_name not in available_tools:
        return validation_error(...)

    # Use state's tool routes
    route = state.tool_routes.get(tool_name, "unknown")
    target_node = self.route_to_node_mapping.get(route)

    return validation_success(target_node=target_node)
```

### 3. State Update Integration

The `apply_validation_results()` method in `EnhancedToolState` provides the integration point:

```python
class EnhancedToolState(ToolState):
    def apply_validation_results(self, validation_state: ValidationRoutingState):
        """Apply validation results to update tool message states."""
        # Update validation state
        self.validation_state = validation_state

        # Update tool message statuses
        for tool_call_id, result in validation_state.tool_validations.items():
            self.tool_message_status[tool_call_id] = result.status.value

        # Update branch conditions for routing
        self.branch_conditions.update(validation_state.get_routing_decision())
```

The validation node calls this:

```python
def validation_node(state: EnhancedToolState) -> EnhancedToolState:
    # ... validation logic
    routing_state = validate_all_tools(...)

    # Use state's method to apply results
    state.apply_validation_results(routing_state)

    return state
```

### 4. Dynamic Router Integration

The router function reads from the updated state:

```python
def validation_router(state: EnhancedToolState) -> Union[List[Send], str]:
    # Use state's validation data
    if state.should_return_to_agent():
        return "agent"

    if not state.should_continue_to_tools():
        return END

    # Create sends for valid tools
    valid_results = state.validation_state.get_valid_tool_calls()
    sends = []
    for result in valid_results:
        sends.append(Send(result.target_node, enhanced_tool_call))

    return sends
```

### 5. Conditional Branching Support

State schemas provide methods for complex routing logic:

```python
# In EnhancedToolState
def should_continue_to_tools(self) -> bool:
    """Check if execution should continue to tool nodes."""
    return self.validation_state.should_continue_execution()

def should_return_to_agent(self) -> bool:
    """Check if execution should return to agent."""
    return self.validation_state.should_return_to_agent()

def get_next_nodes(self) -> List[str]:
    """Get recommended next nodes."""
    return list(self.validation_state.target_nodes)
```

Use in graph conditional edges:

```python
def route_after_validation(state: EnhancedToolState) -> str:
    if state.should_return_to_agent():
        return "agent"
    elif state.should_continue_to_tools():
        return "execute_tools"
    else:
        return END
```

## Complete Integration Example

### Graph Setup

```python
from langgraph.graph import StateGraph
from haive.core.schema.prebuilt.tool_state_with_validation import EnhancedToolState
from haive.core.graph.node.state_updating_validation_node import StateUpdatingValidationNode

# Create graph with enhanced state
graph = StateGraph(EnhancedToolState)

# Create dual-function validation node
validator = StateUpdatingValidationNode(
    validation_mode=ValidationMode.PARTIAL,
    update_messages=True,
    track_error_tools=True
)

# Get both functions
state_updater = validator.create_node_function()
dynamic_router = validator.create_router_function()

# Add nodes
graph.add_node("agent", agent_node)
graph.add_node("state_validator", state_updater)     # Updates state
graph.add_node("router", dynamic_router)             # Routes based on state
graph.add_node("tool_executor", tool_execution_node)
graph.add_node("structured_parser", parser_node)
```

### Node Flow

```python
# 1. Agent generates tool calls
def agent_node(state: EnhancedToolState) -> EnhancedToolState:
    ai_message = AIMessage(
        content="Processing request...",
        tool_calls=[
            {"id": "1", "name": "search", "args": {"query": "info"}},
            {"id": "2", "name": "DocumentSchema", "args": {"title": "Report"}}
        ]
    )
    state.messages.append(ai_message)
    return state

# 2. State validator updates state with validation results
def state_validator_node(state: EnhancedToolState) -> EnhancedToolState:
    # This is the validation node function
    return state_updater(state)

# 3. Router uses updated state for routing decisions
def router_node(state: EnhancedToolState) -> Union[List[Send], str]:
    # This is the router function
    return dynamic_router(state)
```

### Edge Configuration

```python
# Flow control
graph.add_edge("agent", "state_validator")
graph.add_edge("state_validator", "router")

# Router creates Send branches - no explicit edges needed
# Tool nodes return to agent
graph.add_edge("tool_executor", "agent")
graph.add_edge("structured_parser", "agent")

# Alternative: Use conditional edges for complex logic
graph.add_conditional_edges(
    "state_validator",
    lambda state: "router" if state.should_continue_to_tools() else "agent"
)
```

## Benefits of State Schema Integration

### 1. **Automatic Tool Management**

- Tools are automatically synchronized from engines
- Tool routes are maintained consistently
- Computed fields extract tool calls seamlessly

### 2. **Persistent Validation State**

- Validation results persist in state across graph execution
- Tool message statuses tracked automatically
- Branch conditions enable sophisticated routing

### 3. **Type Safety and Validation**

- Pydantic models ensure type safety
- Field validation prevents configuration errors
- Rich metadata and performance tracking

### 4. **Extensibility**

- Easy to extend with custom fields
- Backward compatible with existing code
- Supports complex conditional logic

### 5. **Debugging and Monitoring**

- Rich state information for debugging
- Performance tracking built-in
- Comprehensive logging support

## Advanced Patterns

### Pattern 1: Multi-Engine Validation

```python
class MultiEngineState(EnhancedToolState):
    """State with multiple engines for different tool types."""

    def __init__(self):
        super().__init__()
        self.engines = {
            "llm_engine": llm_engine,
            "retriever_engine": retriever_engine,
            "parser_engine": parser_engine
        }

    def get_engine_for_tool(self, tool_name: str) -> Optional[str]:
        """Get appropriate engine for a tool."""
        route = self.tool_routes.get(tool_name)
        for engine_name, accepted_routes in self.engine_route_config.items():
            if route in accepted_routes:
                return engine_name
        return None

# Validation node can route to different engines
validator = StateUpdatingValidationNode(
    route_to_node_mapping={
        "langchain_tool": "llm_tools",
        "pydantic_model": "parser_tools",
        "retriever": "retriever_tools"
    }
)
```

### Pattern 2: Priority-Based Routing

```python
class PriorityState(EnhancedToolState):
    """State with tool priority support."""

    def get_high_priority_tools(self) -> List[str]:
        """Get tools marked as high priority."""
        return [
            name for name, priority in self.tool_priorities.items()
            if priority > 50
        ]

# Router can use priority information
def priority_router(state: PriorityState) -> Union[List[Send], str]:
    high_priority = state.get_high_priority_tools()

    # Route high priority tools to dedicated node
    sends = []
    for result in state.validation_state.get_valid_tool_calls():
        if result.tool_name in high_priority:
            target = "high_priority_executor"
        else:
            target = "standard_executor"

        sends.append(Send(target, enhanced_tool_call))

    return sends
```

### Pattern 3: Dependency-Aware Validation

```python
class DependencyState(EnhancedToolState):
    """State with tool dependency tracking."""

    def check_dependencies_satisfied(self, tool_name: str) -> bool:
        """Check if tool dependencies are satisfied."""
        deps = self.tool_dependencies.get(tool_name, [])
        return all(
            self.tool_message_status.get(dep) == "completed"
            for dep in deps
        )

# Validation can check dependencies
def dependency_validator(self, tool_call, state):
    tool_name = tool_call["name"]

    if not state.check_dependencies_satisfied(tool_name):
        return validation_result(
            status=ValidationStatus.INVALID,
            errors=["Dependencies not satisfied"],
            route_recommendation=RouteRecommendation.RETRY
        )

    return standard_validation(tool_call, state)
```

## Conclusion

The integration between `StateUpdatingValidationNode` and Haive's state schemas provides a powerful foundation for building sophisticated agent workflows. The state schemas handle tool management, validation state persistence, and conditional branching, while the validation node provides the dual functionality of state updates and dynamic routing.

This design enables:

- Clean separation of concerns
- Type-safe state management
- Rich validation and routing capabilities
- Easy extensibility for custom use cases
- Seamless integration with LangGraph workflows

The result is a robust, maintainable system for handling complex tool validation and routing scenarios in production agent applications.
