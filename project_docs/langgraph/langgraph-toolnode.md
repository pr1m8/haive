# LangGraph: Tool Node and Routing

## Executive Summary

LangGraph's prebuilt `ToolNode` and `tools_condition` form the backbone of dynamic tool execution and workflow routing in AI agent systems. These components enable sophisticated decision-making patterns where agents iteratively call tools based on contextual needs while managing state transitions efficiently. This document analyzes their architecture, integration patterns, and implementation strategies for the Haive node system redesign.

## ToolNode: Architecture and Core Functionality

### 1. Component Design

`ToolNode` is a specialized `Runnable` that processes tool calls from the last `AIMessage` in the graph state. Its architecture features:

**Core Execution Flow**

1. **Input Handling**: Accepts state containing `messages` key with message history
2. **Tool Call Extraction**: Identifies `tool_calls` in the last `AIMessage`
3. **Parallel Execution**: Runs multiple tool invocations concurrently using thread/async pools
4. **Result Packaging**: Returns `ToolMessage` objects with execution outcomes

```python
from langgraph.prebuilt import ToolNode

tool_node = ToolNode(
    tools=[search_tool, calculate_tool],
    handle_tool_errors=True,
    return_direct=False
)
```

### 2. State Graph Integration

`ToolNode` operates within LangGraph's state management paradigm:

```
Agent -->|AIMessage with tool_calls| ToolNode
ToolNode -->|ToolMessages| Agent
```

Key integration points:

- **Message Reducers**: Uses `add_messages` reducer to maintain valid message sequences
- **State Preservation**: Maintains full message history while passing filtered context to LLMs
- **Metadata Injection**: Supports `InjectedState` and `InjectedStore` for tool argument enrichment

## Tools Condition: Dynamic Workflow Routing

### 1. Conditional Edge Mechanism

The `tools_condition` function enables intelligent workflow branching:

```python
from langgraph.prebuilt import tools_condition

workflow.add_conditional_edges(
    "agent",
    tools_condition,
    {"tools": "tool_node", "continue": "next_step"}
)
```

**Decision Logic**

```python
def tools_condition(state: State) -> Literal["tools", "__end__"]:
    last_message = state.messages[-1]
    return "tools" if last_message.tool_calls else "__end__"
```

### 2. Configuration Strategies

| Parameter          | Effect on Routing                     | Use Case                        |
| ------------------ | ------------------------------------- | ------------------------------- |
| `message_key`      | Custom state field for message access | Multi-modal agent architectures |
| `error_threshold`  | Automatic retry attempts              | Fault-tolerant workflows        |
| `tool_call_filter` | Selective tool execution              | Permission-based tool access    |

## Advanced Implementation Patterns

### 1. State-Aware Tool Execution

Inject runtime context into tool arguments:

```python
from langgraph.prebuilt import InjectedState

@tool
def contextual_search(
    query: str,
    state: Annotated[dict, InjectedState(field="session_context")]
):
    """Search with session-specific filters"""
    filters = state.get("search_filters", {})
    return execute_search(query, filters)
```

### 2. Hybrid Workflow Design

Combine ToolNode with custom nodes:

```python
workflow.add_node("tool_node", tool_node)
workflow.add_node("validation", validation_node)
workflow.add_conditional_edges(
    "tool_node",
    lambda s: "validation" if needs_approval(s) else "agent"
)
```

## Implications for Haive Node System Redesign

### 1. Specialized Tool Node Implementation

The Haive node system should include a specialized tool node implementation similar to LangGraph's approach:

```python
def create_tool_node(
    tools: List[BaseTool],
    handle_errors: bool = True,
    parallel: bool = True,
    max_workers: int = 4,
    tool_call_parser: Optional[Callable] = None,
    command_goto: Optional[str] = None
) -> Callable:
    """Create a node function for tool execution."""

    # Create tool map
    tool_map = {tool.name: tool for tool in tools}

    def tool_node(state: Dict[str, Any]) -> Any:
        # Extract messages
        messages = state.get("messages", [])
        if not messages:
            return Command(goto=command_goto) if command_goto else {}

        # Extract tool calls from last message
        last_message = messages[-1]
        tool_calls = get_tool_calls(last_message, tool_call_parser)

        if not tool_calls:
            return Command(goto=command_goto) if command_goto else {}

        # Execute tools (parallel or sequential)
        results = execute_tools(
            tool_calls,
            tool_map,
            parallel=parallel,
            max_workers=max_workers,
            handle_errors=handle_errors
        )

        # Create tool messages
        tool_messages = create_tool_messages(results)

        # Return updated state with tool messages
        return Command(
            update={"messages": messages + tool_messages},
            goto=command_goto
        ) if command_goto else {"messages": messages + tool_messages}

    return tool_node
```

### 2. Standard Routing Function

Implement a standard tools condition function for common routing patterns:

```python
def create_tools_condition(
    message_key: str = "messages",
    tool_call_parser: Optional[Callable] = None,
    routes: Dict[str, str] = None
) -> Callable:
    """Create a tools condition function for routing."""

    routes = routes or {"has_tools": "tools", "no_tools": "continue"}

    def condition_func(state: Dict[str, Any]) -> str:
        # Extract messages
        messages = state.get(message_key, [])
        if not messages:
            return routes.get("no_tools")

        # Check last message for tool calls
        last_message = messages[-1]
        tool_calls = get_tool_calls(last_message, tool_call_parser)

        if tool_calls:
            return routes.get("has_tools")
        return routes.get("no_tools")

    return condition_func
```

### 3. State Injection Support

Support state injection for tool execution:

```python
def create_state_injected_tool(
    func: Callable,
    name: str,
    description: str,
    state_fields: List[str],
    schema: Optional[Type[BaseModel]] = None
) -> BaseTool:
    """Create a tool with state injection support."""

    # Create a wrapped function that injects state fields
    def wrapped_func(*args, **kwargs):
        # Get injected state from context
        state = kwargs.pop("__state__", {})

        # Inject requested state fields
        for field in state_fields:
            if field in state and field not in kwargs:
                kwargs[field] = state[field]

        # Call original function
        return func(*args, **kwargs)

    # Create and return tool
    return BaseTool(
        name=name,
        description=description,
        func=wrapped_func,
        schema=schema
    )
```

### 4. Parallel Tool Execution

Implement efficient parallel tool execution:

```python
def execute_tools(
    tool_calls: List[ToolCall],
    tool_map: Dict[str, BaseTool],
    parallel: bool = True,
    max_workers: int = 4,
    handle_errors: bool = True
) -> List[Dict[str, Any]]:
    """Execute tools in parallel or sequentially."""

    results = []

    if parallel and len(tool_calls) > 1:
        # Execute tools in parallel
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = []
            for tool_call in tool_calls:
                if tool_call.name in tool_map:
                    tool = tool_map[tool_call.name]
                    futures.append(
                        executor.submit(
                            _safe_execute_tool,
                            tool,
                            tool_call.args,
                            handle_errors
                        )
                    )

            # Gather results
            for future in as_completed(futures):
                results.append(future.result())
    else:
        # Execute tools sequentially
        for tool_call in tool_calls:
            if tool_call.name in tool_map:
                tool = tool_map[tool_call.name]
                result = _safe_execute_tool(tool, tool_call.args, handle_errors)
                results.append(result)

    return results
```

## Integration with Schema System

The tool node implementation should integrate with Haive's schema system:

```python
class AgentState(StateSchema):
    """Agent state with tools support."""
    messages: List[BaseMessage] = Field(default_factory=list)
    tools_used: List[str] = Field(default_factory=list)

    # Reducer for tools_used field
    __reducer_fields__ = {
        "tools_used": operator.add
    }

    # Tool tracking method
    def add_tool_usage(self, tool_name: str) -> None:
        """Add a tool usage to the state."""
        self.tools_used.append(tool_name)

# Enhanced tool node that updates tools_used field
def create_enhanced_tool_node(
    tools: List[BaseTool],
    state_schema: Type[StateSchema] = None,
    track_usage: bool = True,
    command_goto: Optional[str] = None
) -> Callable:
    """Create an enhanced tool node that integrates with schema system."""

    # Implementation details...

    def tool_node(state: Dict[str, Any]) -> Any:
        # Tool execution logic...

        # Update tools_used field if tracking is enabled
        updates = {"messages": messages + tool_messages}
        if track_usage and state_schema and hasattr(state_schema, "tools_used"):
            updates["tools_used"] = [tool["name"] for tool in results]

        return Command(update=updates, goto=command_goto) if command_goto else updates

    return tool_node
```

## Conclusion

LangGraph's `ToolNode` and `tools_condition` provide a robust framework for implementing complex tool-execution workflows in AI agent systems. For Haive's node system redesign, we should adopt these patterns with enhanced schema integration and configuration support to create a more powerful and maintainable tool execution system.

Key elements to implement include:

1. Specialized tool node function creators
2. Standard routing condition functions
3. Parallel tool execution support
4. State injection mechanisms
5. Schema integration for tool tracking and validation

By implementing these patterns, the Haive framework will support sophisticated agent architectures that can effectively leverage tool capabilities while maintaining clean state management and workflow control.
