# Haive Core: Graph Module

## Overview

The Graph module provides a comprehensive system for building, manipulating, and executing computational graphs in the Haive framework. It extends LangGraph's capabilities with a focus on dynamic construction, schema validation, and enhanced node capabilities. The module serves as the backbone for agent workflows, enabling complex computational flows with robust state management and serialization support.

## Key Features

- **Schema-Validated Graphs**: Build graphs with strict type safety through Pydantic models
- **Dynamic Routing**: Create complex workflows with conditional branching and parallel execution
- **Node System**: Comprehensive node creation and management with configurable behaviors
- **LangGraph Integration**: Seamless integration with LangChain's LangGraph system
- **Visualization**: Built-in graph visualization capabilities for debugging and documentation
- **Pattern Support**: Reusable graph patterns and templates for common workflows
- **Serialization**: Full graph serialization and deserialization support

## Installation

This module is part of the `haive-core` package. Install the full package with:

```bash
pip install haive-core
```

Or install via Poetry:

```bash
poetry add haive-core
```

## Quick Start

```python
from haive.core.graph.state_graph import BaseGraph, SchemaGraph
from haive.core.graph.node import create_node
from langgraph.graph import START, END
from pydantic import BaseModel, Field
from typing import List

# Define state schema
class MyState(BaseModel):
    messages: List[dict] = Field(default_factory=list)
    context: dict = Field(default_factory=dict)

# Create a graph with schema validation
graph = SchemaGraph(name="my_workflow", state_schema=MyState)

# Create nodes
def retrieve_node(state):
    # Retrieval logic here
    return {"context": {"documents": ["doc1", "doc2"]}}

def generate_node(state):
    # Generation logic here
    return {"messages": state["messages"] + [{"role": "assistant", "content": "Response"}]}

# Add nodes to graph
graph.add_node("retrieve", create_node(retrieve_node, name="retrieve"))
graph.add_node("generate", create_node(generate_node, name="generate"))

# Add edges
graph.add_edge(START, "retrieve")
graph.add_edge("retrieve", "generate")
graph.add_edge("generate", END)

# Compile and run the graph
compiled = graph.compile()
result = compiled.invoke({"messages": [{"role": "user", "content": "Hello"}]})
```

## Components

### State Graph

The state graph system is the core computational graph infrastructure in Haive, enabling flexible workflows with robust state management.

```python
from haive.core.graph.state_graph import BaseGraph, SchemaGraph
from langgraph.graph import START, END

# Create a basic graph
graph = BaseGraph(name="simple_graph")

# Add simple nodes
graph.add_node("node1", lambda state: {"output": state["input"] + " processed"})
graph.add_node("node2", lambda state: {"final": state["output"] + " and finalized"})

# Connect nodes
graph.add_edge(START, "node1")
graph.add_edge("node1", "node2")
graph.add_edge("node2", END)

# Compile and run
compiled = graph.compile()
result = compiled.invoke({"input": "test data"})
print(result)  # {'input': 'test data', 'output': 'test data processed', 'final': 'test data processed and finalized'}
```

### Node System

The node system provides a comprehensive framework for creating, configuring, and managing nodes in a graph workflow.

```python
from haive.core.graph.node import create_node, create_branch_node, create_tool_node
from haive.core.graph.node.types import NodeType
from haive.core.graph.node.config import NodeConfig

# Create a node with custom configuration
config = NodeConfig(
    name="processor",
    debug=True,  # Enable debugging
    input_mapping={"input_data": "query"},  # Map state keys to function inputs
    output_mapping={"result": "processed_data"}  # Map function outputs to state keys
)

# Create node function
def process(input_data):
    return {"result": f"Processed: {input_data}"}

node_function = create_node(process, config=config)

# Create a branch node for conditional routing
branch_node = create_branch_node(
    condition=lambda state: "has_data" if state.get("data") else "no_data",
    routes={"has_data": "process_data", "no_data": "fetch_data"}
)

# Create a tool node for handling tool calls
tool_node = create_tool_node(
    tools=[search_tool, calculator_tool],
    handle_tool_errors=True
)
```

### Dynamic Graph Building

The dynamic graph builder provides an enhanced interface for creating complex graphs with schema validation.

```python
from haive.core.graph.dynamic_graph_builder import DynamicGraph
from haive.core.schema.state_schema import StateSchema
from pydantic import Field
from typing import List

# Define state schema
class AgentState(StateSchema):
    messages: List[dict] = Field(default_factory=list)
    context: dict = Field(default_factory=dict)

# Create graph with schema validation
graph = DynamicGraph(
    name="agent_workflow",
    state_schema=AgentState,
    components=[llm_engine, retriever_engine]  # Optional components
)

# Add nodes and edges
graph.add_node("retrieve", retriever_node)
graph.add_node("generate", llm_node)
graph.add_edge("retrieve", "generate")

# Add conditional routing
graph.add_conditional_edges(
    "router",
    lambda state: "need_tools" if "tool_calls" in state["messages"][-1] else "final",
    {
        "need_tools": "tools_node",
        "final": END
    }
)

# Compile and run
runnable = graph.build()
```

### Branches

The branches system enables complex parallel execution patterns with state merging.

```python
from haive.core.graph.branches import Branch
from haive.core.graph.state_graph import BaseGraph
from langgraph.graph import START, END

# Create a graph
graph = BaseGraph(name="parallel_workflow")

# Define regular nodes
graph.add_node("preprocessor", preprocess_function)
graph.add_node("postprocessor", postprocess_function)

# Create branch for parallel processing
branch = Branch(
    name="parallel_tasks",
    nodes=["task_a", "task_b", "task_c"],
    entry_node="task_a",  # First node in branch
    exit_node="task_c"    # Last node in branch
)

# Add nodes in branch
graph.add_node("task_a", task_a_function)
graph.add_node("task_b", task_b_function)
graph.add_node("task_c", task_c_function)

# Add branch to graph
graph.add_branch(branch)

# Connect main flow
graph.add_edge(START, "preprocessor")
graph.add_edge("preprocessor", branch.entry_point)
graph.add_edge(branch.exit_point, "postprocessor")
graph.add_edge("postprocessor", END)
```

## Usage Patterns

### Schema Validation

Build type-safe graphs with Pydantic models:

```python
from haive.core.graph.state_graph import SchemaGraph
from pydantic import BaseModel, Field
from typing import List, Optional

# Define state schema
class AgentState(BaseModel):
    messages: List[dict] = Field(default_factory=list)
    context: dict = Field(default_factory=dict)
    tools_results: Optional[List[dict]] = None

# Create schema-validated graph
graph = SchemaGraph(
    name="validated_workflow",
    state_schema=AgentState
)

# Any invalid state updates will raise validation errors
```

### Graph Patterns

Apply reusable patterns to standardize common workflows:

```python
from haive.core.graph.patterns.registry import GraphPatternRegistry
from haive.core.graph.state_graph import BaseGraph

# Create a graph
graph = BaseGraph(name="api_workflow")
graph.add_node("api_call", api_function)

# Get and apply retry pattern
retry_pattern = GraphPatternRegistry.get_pattern("retry_on_error")
retry_pattern.apply(
    graph,
    target_node="api_call",
    max_retries=3,
    retry_condition=lambda err: isinstance(err, ConnectionError)
)
```

## Configuration

Configure graph behavior and execution:

```python
from haive.core.graph.state_graph import BaseGraph
from langgraph.graph import StateGraph, START, END

# Create graph with configuration
graph = BaseGraph(
    name="configured_workflow",
    metadata={
        "author": "Development Team",
        "version": "1.0.0",
        "tags": ["api", "integration"]
    },
    log_level="INFO",
    debug=True
)

# Configure node execution
graph.add_node(
    "api_node",
    api_function,
    retry_policy={
        "max_retries": 3,
        "delay_factor": 2.0  # Exponential backoff
    }
)

# Configure graph execution
compiled = graph.compile(
    checkpointer=MemoryCheckpointer(),  # Checkpoint state between steps
    interrupt_before=["critical_node"],  # Pause before executing specific nodes
    event_callback=logging_callback     # Log execution events
)
```

## Integration with Other Modules

### Integration with Engine Module

```python
from haive.core.graph.node import create_engine_node
from haive.core.engine import BaseEngine

# Create an engine-based node
llm_node = create_engine_node(
    llm_engine,
    input_mapping={"messages": "messages", "context": "retrieval_result"},
    output_mapping={"generated_text": "response"}
)

# Add to graph
graph.add_node("generate", llm_node)
```

### Integration with Schema Module

```python
from haive.core.graph.state_graph import SchemaGraph
from haive.core.schema import SchemaComposer
from haive.core.schema.fields import MessagesField, DictField

# Create schema using SchemaComposer
schema = SchemaComposer.create({
    "messages": MessagesField(),
    "context": DictField(),
    "metadata": DictField(optional=True)
})

# Create graph with schema validation
graph = SchemaGraph(
    name="workflow",
    state_schema=schema
)
```

## Best Practices

- **Use Schema Validation**: Always define a state schema for robust type safety
- **Modularize Graphs**: Break complex workflows into subgraphs and branches
- **Keep Nodes Simple**: Design nodes to do one thing well with clear inputs/outputs
- **Use Graph Patterns**: Leverage reusable patterns for common workflows
- **Enable Debugging**: Use debug mode during development for detailed execution tracing
- **Visualize Graphs**: Generate visualizations for documentation and debugging
- **Test Isolated Components**: Test nodes and branches individually before integration

## Advanced Usage

### Custom Node Types

```python
from haive.core.graph.node import register_custom_node_type, NodeConfig
from haive.core.graph.node.types import NodeType
from pydantic import Field
from typing import Dict, Any, Optional

# Define custom node config
class StreamingNodeConfig(NodeConfig):
    batch_size: int = Field(default=10)
    stream_interval: float = Field(default=0.1)
    buffer_limit: Optional[int] = None

# Register custom node type
register_custom_node_type(
    name="streaming",
    config_class=StreamingNodeConfig
)

# Create custom node factory function
def create_streaming_node(
    process_func,
    batch_size=10,
    stream_interval=0.1,
    **kwargs
):
    return create_node(
        process_func,
        node_type="streaming",
        batch_size=batch_size,
        stream_interval=stream_interval,
        **kwargs
    )
```

### Graph Visualization

```python
from haive.core.graph.utils.mermaid_visualizer import MermaidVisualizer
from haive.core.graph.state_graph import BaseGraph

# Create a graph
graph = BaseGraph(name="visualization_example")
# Add nodes and edges...

# Generate Mermaid diagram
visualizer = MermaidVisualizer(graph)
mermaid_code = visualizer.generate()

# Save to file
visualizer.save_to_file("workflow_diagram.md")

# Generate HTML report with interactive diagram
visualizer.generate_html_report(
    output_path="workflow_report.html",
    include_node_details=True,
    include_edge_details=True
)
```

## API Reference

For full API details, see the [documentation](https://docs.haive.ai/core/graph).

## Related Modules

- **haive.core.engine**: Provides engines that can be used as node components
- **haive.core.schema**: Defines schemas for graph state validation
- **haive.core.common**: Provides common utilities used throughout the graph system
- **haive.core.utils**: Utilities for debugging, visualization, and testing
