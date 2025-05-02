# Node System Overview

The Haive node system provides a streamlined way to create, configure, and execute nodes in a graph-based workflow. This document provides an overview of the system, its components, and usage patterns.

## Core Concepts

The node system is built around these key concepts:

1. **Nodes**: Functions that process state and optionally route to other nodes
2. **State**: Data passed between nodes (preferably using `StateSchema`)
3. **Commands**: Control flow instructions for routing between nodes
4. **Decorators**: Simple ways to create different types of nodes

## Key Components

### Protocols and Types

The system defines clear protocols for node functions:

```python
# Simple function type
def my_node(state: State) -> Any:
    return updated_state

# Async function type
async def my_async_node(state: State) -> Any:
    return updated_state
```

The return type can be:
- A modified state (dict, StateSchema, or BaseModel)
- A Command (for routing to another node)
- A Send object (for parallel workflows)
- A list of Send objects (for fan-out patterns)

### NodeConfig

The `NodeConfig` class provides configuration for nodes, handling:

- Input/output mappings
- Command routing
- State schema preservation
- Engine integration

### NodeFactory

The `NodeFactory` creates node functions from different sources:

- Engine instances
- Callable functions 
- NodeConfig objects

It handles input/output processing, command routing, and schema preservation.

### Decorators

Decorators provide a simple way to create different types of nodes:

```python
@node()  # Basic node
def simple_node(state: State) -> State:
    return state

@async_node()  # Async node
async def async_node(state: State) -> State:
    return state

@engine_node(engine="llm_engine")  # Engine node
def llm_node(state: State) -> State:
    return state

@validation_node(ValidationSchema)  # Validation node
def validate(state: State) -> State:
    return state

@retry_node(max_attempts=3)  # Retry node
def retry_node(state: State) -> State:
    return state

@interruptible_node()  # Interruptible node
def interruptible(state: State) -> State:
    return state
```

## Usage Patterns

### Basic Node Creation

```python
from haive.core.graph.node import node

@node(command_goto="next_node")
def my_node(state: StateSchema) -> StateSchema:
    state.output = process(state.input)
    return state
```

### Engine Node Creation

```python
from haive.core.graph.node import engine_node, llm_node

# Generic engine node
@engine_node(engine="retriever_engine")
def retrieval(state: StateSchema) -> StateSchema:
    # Function body not used - engine handles processing
    pass

# Specialized LLM node
llm = llm_node(
    engine="claude_3", 
    input_mapping={"messages": "messages"},
    output_mapping={"response": "answer"}
)
```

### Tool Node Creation

```python
from haive.core.graph.node import tool_node, tools_condition

# Create tools
tools = [search_tool, calculator_tool]

# Create tool node
tool_executor = tool_node(
    tools=tools,
    command_goto="agent",
    parallel=True
)

# Create routing condition
def route_tools(state):
    return tools_condition(state)

# Use in graph
workflow.add_conditional_edges(
    "agent",
    route_tools,
    {"tools": "tool_executor", "continue": "next_step"}
)
```

### Validation Node

```python
from haive.core.graph.node import validation_node
from pydantic import BaseModel

class UserSchema(BaseModel):
    username: str
    email: str

validator = validation_node(
    validation_schema=UserSchema,
    success_node="process_user",
    failure_node="handle_error"
)
```

### Retry Node

```python
from haive.core.graph.node import retry_node

@retry_node(
    max_attempts=3,
    initial_delay=1.0,
    backoff_factor=2.0,
    failure_node="handle_error"
)
def api_call(state: StateSchema) -> StateSchema:
    result = make_api_request(state.query)
    state.response = result
    return state
```

### Interrupt Node

```python
from haive.core.graph.node import interruptible_node, interrupt

@interruptible_node(resume_node="approval_handler")
def generate_content(state: StateSchema) -> StateSchema:
    # Generate content
    content = generate(state.prompt)
    
    # If content needs human review
    if needs_review(content):
        interrupt(payload={
            "content": content,
            "action": "review"
        })
    
    state.content = content
    return state

# To resume execution
def approval_handler(state: StateSchema) -> StateSchema:
    # Get approval decision
    decision = state.resume_data.get("decision")
    
    if decision == "approved":
        return Command(goto="continue_workflow")
    else:
        return Command(goto="revise_content")
```

## StateSchema Integration

The node system fully supports `StateSchema` for type-safe state management:

```python
from haive.core.schema.state_schema import StateSchema
from haive.core.graph.node import node

class ChatState(StateSchema):
    messages: List[Dict[str, Any]] = Field(default_factory=list)
    context: List[Dict[str, Any]] = Field(default_factory=list)
    
    def add_message(self, role: str, content: str) -> None:
        self.messages.append({"role": role, "content": content})

@node()
def add_user_message(state: ChatState, message: str) -> ChatState:
    state.add_message("user", message)
    return state
```

## Testing Nodes

The system includes utilities for testing nodes:

```python
from haive.core.graph.node.utils.testing import NodeTester

# Run a node with input
result = NodeTester.run_node(my_node, {"input": "hello"})

# Assert output
NodeTester.assert_node_output(
    my_node,
    {"input": "hello"},
    "HELLO",
    path="output"
)
```

## Best Practices

1. **Use StateSchema**: Prefer `StateSchema` over dictionaries for type safety.
2. **Keep Nodes Simple**: Each node should do one thing well.
3. **Use Decorators**: Use the appropriate decorator for each node type.
4. **Explicit Routing**: Use explicit `command_goto` for clear flow control.
5. **Error Handling**: Use retry nodes for operations that might fail.
6. **Human-in-the-Loop**: Use interrupt nodes for human interaction points.
7. **Test Individually**: Test nodes in isolation before integration.

## Advanced Features

### Execution Context

Execution utilities provide additional functionality:

```python
from haive.core.graph.node.execution import RetryPolicy, create_resume_command

# Create custom retry policy
policy = RetryPolicy(
    max_attempts=5,
    initial_interval=1.0,
    backoff_factor=2.0
)

# Create resume command
command = create_resume_command(
    state,
    resume_data={"decision": "approved"},
    resume_node="content_generator"
)
```

### Custom Node Types

You can easily create custom node types:

```python
def custom_node_type(
    name: Optional[str] = None,
    **kwargs
):
    """Custom node type decorator."""
    def decorator(func: Callable) -> Callable:
        # Create node with custom logic
        node_name = name or func.__name__
        
        # Create node config
        config = NodeConfig(
            name=node_name,
            engine=func,
            **kwargs
        )
        
        # Create and return node
        return NodeFactory.create_node(config)
    
    return decorator
```

## Conclusion

The node system provides a flexible, type-safe way to build complex workflows with minimal boilerplate. By leveraging decorators and StateSchema integration, you can create powerful, maintainable agent workflows that handle interrupts, retries, and complex routing with ease.