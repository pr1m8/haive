# Node Types and Patterns

This document covers the different types of nodes available in the Haive node system and common patterns for using them effectively.

## Node Types

### Basic Nodes

Basic nodes are simple functions that process state and optionally route to other nodes.

```python
from haive.core.graph.node import node

@node(command_goto="next_node")
def basic_node(state: State) -> State:
    # Process state
    if isinstance(state, dict):
        result = state.copy()
        result["output"] = process(state.get("input", ""))
    else:
        result = state
        result.output = process(state.input)
    return result
```

#### Key Features:
- Simple function signature
- Processes state directly
- Can return updated state or Command

#### Best For:
- Simple transformations
- Decision points
- State preparation

### Async Nodes

Async nodes are asynchronous functions that process state, useful for I/O-bound operations.

```python
from haive.core.graph.node import async_node

@async_node(command_goto="next_node")
async def async_node(state: State) -> State:
    # Process state asynchronously
    result = await async_process(state)
    return result
```

#### Key Features:
- Asynchronous execution
- Non-blocking operations
- Same interface as basic nodes

#### Best For:
- API calls
- Database operations
- File I/O
- Parallel processing

### Engine Nodes

Engine nodes wrap engines (LLMs, retrievers, etc.) with a consistent interface.

```python
from haive.core.graph.node import engine_node, llm_node, retriever_node

# Generic engine node
@engine_node(
    engine="my_engine",
    input_mapping={"input": "query"},
    output_mapping={"result": "output"}
)
def engine_node(state: State) -> State:
    # Function body not used - engine handles processing
    pass

# Specialized LLM node
llm = llm_node(
    engine="claude_3",
    input_mapping={"messages": "messages"},
    output_mapping={"response": "response"}
)

# Specialized retriever node
retriever = retriever_node(
    engine="vector_store",
    input_mapping={"query": "question"},
    output_mapping={"documents": "context"}
)
```

#### Key Features:
- Wraps engines with a node interface
- Handles input/output mapping
- Default mappings for specific engine types

#### Best For:
- LLM integration
- Retrieval operations
- Vector store queries
- Structured transformations

### Tool Nodes

Tool nodes handle tool execution from agent messages, following LangGraph's patterns.

```python
from haive.core.graph.node import tool_node, tools_condition

# Create tool node
tool_executor = tool_node(
    tools=[search_tool, calculator_tool],
    command_goto="agent",
    parallel=True,
    max_workers=4
)

# Create routing condition
router = create_tools_router(
    routes={"tools": "tool_executor", "continue": "next_step"}
)

# Use in graph
workflow.add_conditional_edges(
    "agent",
    router,
    {"tools": "tool_executor", "continue": "next_step"}
)
```

#### Key Features:
- Executes tools from messages
- Parallel execution support
- Standardized tool message format
- Automatic tool error handling

#### Best For:
- Agent workflows
- Tool execution
- Parallel processing of multiple tool calls

### Validation Nodes

Validation nodes validate state against a schema, routing based on validation results.

```python
from haive.core.graph.node import validation_node
from pydantic import BaseModel

class UserSchema(BaseModel):
    username: str
    email: str
    age: int

validator = validation_node(
    validation_schema=UserSchema,
    success_node="process_user",
    failure_node="handle_error"
)
```

#### Key Features:
- Schema-based validation
- Error reporting
- Conditional routing based on validation result

#### Best For:
- Input validation
- Schema enforcement
- Data quality checks
- API contract validation

### Retry Nodes

Retry nodes add retry capabilities to handle transient failures.

```python
from haive.core.graph.node import retry_node

@retry_node(
    max_attempts=3,
    initial_delay=1.0,
    backoff_factor=2.0,
    failure_node="handle_error"
)
def api_call(state: State) -> State:
    # Make API request that might fail
    result = make_api_request(state.query)
    state.response = result
    return state
```

#### Key Features:
- Automatic retries on failure
- Exponential backoff
- Jitter support
- Failure routing

#### Best For:
- API calls
- Database operations
- Network requests
- Resource-intensive operations

### Interruptible Nodes

Interruptible nodes support human-in-the-loop workflows with interruption and resumption.

```python
from haive.core.graph.node import interruptible_node, interrupt

@interruptible_node(resume_node="approval_handler")
def content_generator(state: State) -> State:
    # Generate content
    content = generate(state.prompt)
    
    # If content needs human review
    if needs_review(content):
        interrupt({
            "content": content,
            "action": "review"
        })
    
    state.content = content
    return state
```

#### Key Features:
- Interruption with payload
- Automatic state preservation
- Resume capability
- Human-in-the-loop support

#### Best For:
- Approval workflows
- Human review steps
- Long-running processes
- Conditional execution

## Common Patterns

### Chain of Nodes

The simplest pattern is a linear chain of nodes.

```python
# Create nodes
node1 = node(command_goto="node2")(process_input)
node2 = node(command_goto="node3")(transform_data)
node3 = node(command_goto="END")(format_output)

# Create graph
graph = StateGraph(...)
graph.add_node("node1", node1)
graph.add_node("node2", node2)
graph.add_node("node3", node3)
graph.add_edge("START", "node1")
```

### Conditional Branching

Branch based on state evaluation.

```python
# Create decision node
@node()
def decide_route(state: State) -> Command:
    if state.score > 0.8:
        return Command(goto="high_confidence")
    else:
        return Command(goto="low_confidence")

# Create branches
high_conf = node()(handle_high_confidence)
low_conf = node()(handle_low_confidence)

# Create graph
graph = StateGraph(...)
graph.add_node("decide", decide_route)
graph.add_node("high_confidence", high_conf)
graph.add_node("low_confidence", low_conf)
graph.add_edge("START", "decide")
```

### Agent-Tool Loop

Implement a standard agent-tool loop.

```python
# Create agent node
agent = llm_node(
    engine="claude_3",
    input_mapping={"messages": "messages", "context": "context"},
    output_mapping={"response": "messages[-1]"}
)

# Create tool node
tools = [search_tool, calculator_tool]
tool_executor = tool_node(
    tools=tools,
    command_goto="agent"
)

# Create router
router = create_tools_router(
    routes={"tools": "tool_executor", "continue": "end_node"}
)

# Create graph
graph = StateGraph(...)
graph.add_node("agent", agent)
graph.add_node("tool_executor", tool_executor)
graph.add_node("end_node", format_final_output)
graph.add_edge("START", "agent")
graph.add_conditional_edges("agent", router, {"tools": "tool_executor", "continue": "end_node"})
```

### Fan-Out/Fan-In

Process items in parallel and aggregate results.

```python
# Create mapper node
@node()
def mapper(state: State) -> List[Send]:
    return [Send("worker", {"item": item}) for item in state.items]

# Create worker node
@node()
def worker(state: State) -> Dict[str, Any]:
    item = state.get("item")
    result = process_item(item)
    return {"results": [result]}

# Create aggregator
@node(command_goto="END")
def aggregator(state: State) -> State:
    # State will have combined results
    summary = summarize(state.results)
    state.summary = summary
    return state

# Create graph
graph = StateGraph(...)
graph.add_node("mapper", mapper)
graph.add_node("worker", worker)
graph.add_node("aggregator", aggregator)
graph.add_edge("START", "mapper")
graph.add_edge("mapper", "worker")
graph.add_edge("worker", "aggregator")
```

### Human-in-the-Loop

Implement workflows that require human approval.

```python
# Content generation node
@interruptible_node(resume_node="reviewer")
def generate_content(state: State) -> State:
    content = generate(state.prompt)
    
    # Always interrupt for review
    interrupt({
        "content": content,
        "id": state.task_id
    })
    
    return state  # Never reached directly

# Human review node
@node()
def reviewer(state: State) -> Command:
    # Get the decision from resume_data
    decision = state.resume_data.get("decision")
    content = state.resume_data.get("content")
    
    if decision == "approve":
        # Use approved content
        state.content = content
        return Command(update=state, goto="finalize")
    else:
        # Regenerate with feedback
        state.feedback = state.resume_data.get("feedback", "")
        return Command(update=state, goto="regenerate")

# Create graph
graph = StateGraph(...)
graph.add_node("generate", generate_content)
graph.add_node("reviewer", reviewer)
graph.add_node("finalize", finalize_content)
graph.add_node("regenerate", regenerate_content)
graph.add_edge("START", "generate")
```

### Validation Pipeline

Implement a pipeline with validation at each step.

```python
# Create validators
input_validator = validation_node(
    validation_schema=InputSchema,
    success_node="process",
    failure_node="handle_input_error"
)

output_validator = validation_node(
    validation_schema=OutputSchema,
    success_node="final",
    failure_node="handle_output_error"
)

# Processing node
@node(command_goto="validate_output")
def process(state: State) -> State:
    result = process_data(state)
    return result

# Create graph
graph = StateGraph(...)
graph.add_node("validate_input", input_validator)
graph.add_node("process", process)
graph.add_node("validate_output", output_validator)
graph.add_node("final", final_step)
graph.add_node("handle_input_error", input_error_handler)
graph.add_node("handle_output_error", output_error_handler)
graph.add_edge("START", "validate_input")
```

### Retry with Fallback

Implement retry logic with fallback options.

```python
# Primary API node with retry
@retry_node(
    max_attempts=3,
    failure_node="fallback_api"
)
def primary_api(state: State) -> State:
    result = call_primary_api(state.query)
    state.result = result
    return state

# Fallback API node
@node(command_goto="process_result")
def fallback_api(state: State) -> State:
    # Try alternative API
    result = call_fallback_api(state.query)
    state.result = result
    state.used_fallback = True
    return state

# Create graph
graph = StateGraph(...)
graph.add_node("primary_api", primary_api)
graph.add_node("fallback_api", fallback_api)
graph.add_node("process_result", process_result)
graph.add_edge("START", "primary_api")
```

## Advanced Patterns

### Dynamic Node Creation

Create nodes dynamically based on configuration.

```python
def create_processing_pipeline(config: Dict[str, Any]):
    """Create a pipeline of nodes based on configuration."""
    nodes = {}
    
    for i, step in enumerate(config["steps"]):
        step_name = f"step_{i}"
        next_step = f"step_{i+1}" if i < len(config["steps"])-1 else "END"
        
        # Create node based on step type
        if step["type"] == "llm":
            nodes[step_name] = llm_node(
                engine=step["engine"],
                command_goto=next_step
            )
        elif step["type"] == "retrieval":
            nodes[step_name] = retriever_node(
                engine=step["engine"],
                command_goto=next_step
            )
        elif step["type"] == "validation":
            nodes[step_name] = validation_node(
                validation_schema=SCHEMAS[step["schema"]],
                success_node=next_step,
                failure_node="error_handler"
            )
    
    # Create graph
    graph = StateGraph(...)
    
    # Add nodes
    for name, node_func in nodes.items():
        graph.add_node(name, node_func)
    
    # Add error handler
    graph.add_node("error_handler", error_handler)
    
    # Add edges
    graph.add_edge("START", "step_0")
    
    return graph
```

### Composable Node Patterns

Create reusable patterns by combining node types.

```python
def create_validator_with_retry(
    schema: Type[BaseModel],
    process_func: Callable,
    max_attempts: int = 3
):
    """Create a validation+processing+retry pattern."""
    
    # Create validator
    validator = validation_node(
        validation_schema=schema,
        success_node="process",
        failure_node="handle_error"
    )
    
    # Create processor with retry
    processor = retry_node(
        max_attempts=max_attempts,
        failure_node="handle_error"
    )(process_func)
    
    # Create error handler
    @node(command_goto="END")
    def error_handler(state: State) -> State:
        state.error = "Validation or processing failed"
        return state
    
    # Create graph
    graph = StateGraph(...)
    graph.add_node("validate", validator)
    graph.add_node("process", processor)
    graph.add_node("handle_error", error_handler)
    graph.add_edge("START", "validate")
    
    return graph
```

## Best Practices

1. **Use the Right Node Type**:
   - Choose the appropriate node type for each task
   - Match node type to functionality (async for I/O, retry for external calls, etc.)

2. **Keep Nodes Focused**:
   - Each node should do one thing well
   - Avoid complex logic in a single node

3. **Explicit State Handling**:
   - Use StateSchema for type safety
   - Document state requirements for each node

4. **Error Management**:
   - Use validation nodes for input verification
   - Add retry for unreliable operations
   - Include explicit error handlers

5. **Testing**:
   - Test nodes individually
   - Create test cases for edge conditions
   - Use NodeTester for isolated testing

6. **Documentation**:
   - Document node purpose and behavior
   - Include input/output requirements
   - Document routing logic

## Conclusion

The Haive node system provides a comprehensive set of node types to handle different workflow requirements. By combining these node types using the patterns described above, you can create sophisticated, resilient agent workflows that handle complex scenarios while maintaining code clarity and maintainability.