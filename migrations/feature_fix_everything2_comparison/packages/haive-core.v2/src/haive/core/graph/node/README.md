# Haive Core: Graph Node System

## Overview

The Graph Node System provides a comprehensive framework for creating, configuring, and managing nodes in LangGraph-based workflows. It offers a consistent interface for building complex AI application graphs with proper type safety, flexible routing, and seamless integration with Haive's engine and schema systems.

The system supports various node types including engine nodes, callable nodes, tool nodes, validation nodes, branch nodes, and send nodes—enabling sophisticated workflow patterns while maintaining clean, type-safe interfaces.

## Key Features

- **Unified Node Creation API**: Simple functions to create any type of node
- **Type-Safe Workflows**: Strong typing for inputs and outputs across nodes
- **Engine Integration**: Seamless conversion of engines to graph nodes
- **Flexible Routing**: Branch, send, and conditional routing support
- **Tool Handling**: Built-in support for LangChain tool integration
- **Validation**: Schema-based validation for state transitions
- **Extensibility**: Registry system for custom node types
- **Decorators**: Function decorators for declarative node definition

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
from haive.core.graph.node import create_node, create_engine_node
from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.graph.dynamic_graph_builder import DynamicGraphBuilder

# Create an LLM engine node
llm_engine = AugLLMConfig(model="gpt-4")
llm_node = create_engine_node(
    llm_engine,
    name="generate",
    command_goto="END"
)

# Create a custom node from a function
def process_input(state):
    state.processed_query = state.query.strip().lower()
    return state

input_node = create_node(
    process_input,
    name="process_input",
    command_goto="generate"
)

# Build a graph with these nodes
builder = DynamicGraphBuilder(state_type=MyState)
builder.add_node("process_input", input_node)
builder.add_node("generate", llm_node)
builder.set_entry_point("process_input")
graph = builder.build()
```

## Components

### Node Creation Functions

The package provides high-level functions for creating different types of nodes:

```python
from haive.core.graph.node import (
    create_node,              # General-purpose node creation
    create_engine_node,       # Specifically for engine nodes
    create_validation_node,   # For schema validation
    create_tool_node,         # For LangChain tools
    create_branch_node,       # For conditional routing
    create_send_node          # For fan-out operations
)
```

### Node Factory

The `NodeFactory` provides the underlying implementation for creating node functions:

```python
from haive.core.graph.node.factory import NodeFactory

# Create a node from configuration
node_function = NodeFactory.create_node_function(node_config)
```

### Node Config

The `NodeConfig` class provides a unified configuration system for all node types:

```python
from haive.core.graph.node.config import NodeConfig

# Create a node configuration
config = NodeConfig(
    name="retrieval",
    engine=retriever_engine,
    node_type=NodeType.ENGINE,
    command_goto="generate",
    input_mapping={"query": "user_query"},
    output_mapping={"documents": "context"}
)
```

### Node Registry

The `NodeRegistry` manages node types and their configurations:

```python
from haive.core.graph.node import get_registry, register_custom_node_type
from haive.core.graph.node.config import NodeConfig

# Create a custom node config class
class CustomNodeConfig(NodeConfig):
    custom_option: str

# Register the custom node type
register_custom_node_type("custom", CustomNodeConfig)

# Get the registry
registry = get_registry()
```

### Node Decorators

Function decorators provide a declarative way to define nodes:

```python
from haive.core.graph.node.decorators import (
    register_node,
    tool_node,
    validation_node,
    branch_node,
    send_node
)

# Create a registered node
@register_node(name="process_input", command_goto="generate")
def process_input(state):
    state.processed_query = state.query.strip().lower()
    return state

# Create a branch node
@branch_node(routes={"retrieval": "retrieve", "generation": "generate"})
def router(state):
    if "query" in state and state.query:
        return "retrieval"
    return "generation"
```

## Usage Patterns

### Basic Node Creation

```python
from haive.core.graph.node import create_node

# Create a node from a function
def process_input(state):
    state.processed_query = state.query.strip().lower()
    return state

input_node = create_node(
    process_input,
    name="process_input",
    command_goto="generate"
)

# Create a node with input/output mapping
mapped_node = create_node(
    some_function,
    name="mapped_node",
    input_mapping={"state_key": "function_arg"},
    output_mapping={"function_result": "state_key"}
)
```

### Engine Nodes

```python
from haive.core.graph.node import create_engine_node
from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.engine.retriever import RetrieverConfig

# Create an LLM engine node
llm_engine = AugLLMConfig(model="gpt-4")
llm_node = create_engine_node(
    llm_engine,
    name="generate",
    command_goto="END"
)

# Create a retriever engine node
retriever_engine = RetrieverConfig(
    type="vector_store",
    vector_store="chroma"
)
retriever_node = create_engine_node(
    retriever_engine,
    name="retrieve",
    command_goto="generate",
    input_mapping={"query": "user_query"},
    output_mapping={"documents": "context"}
)
```

### Tool Nodes

```python
from haive.core.graph.node import create_tool_node
from langchain.tools import DuckDuckGoSearchRun, WikipediaQueryRun

# Create a tool node with multiple tools
tools = [
    DuckDuckGoSearchRun(),
    WikipediaQueryRun()
]

tool_node = create_tool_node(
    tools,
    name="search_tools",
    command_goto="generate",
    messages_key="messages",
    handle_tool_errors=True
)
```

### Validation Nodes

```python
from haive.core.graph.node import create_validation_node
from pydantic import BaseModel, Field
from typing import List

# Create validation schemas
class QueryValidation(BaseModel):
    query: str = Field(..., min_length=3)

class ContextValidation(BaseModel):
    context: List[str] = Field(..., min_items=1)

# Create a validation node
validation_node = create_validation_node(
    schemas=[QueryValidation, ContextValidation],
    name="validate_input",
    command_goto="retrieve"
)
```

### Branch Nodes

```python
from haive.core.graph.node import create_branch_node

# Create a condition function
def route_by_query_type(state):
    if "retrieve" in state.query.lower():
        return "retrieval"
    return "generation"

# Create a branch node
branch_node = create_branch_node(
    condition=route_by_query_type,
    routes={
        "retrieval": "retrieve",
        "generation": "generate"
    },
    name="router"
)
```

### Send Nodes

```python
from haive.core.graph.node import create_send_node

# Create a send node for parallel processing
send_node = create_send_node(
    send_targets=["process_a", "process_b", "process_c"],
    send_state_key="items",
    name="distribute"
)
```

## Configuration

### Node Types

The system supports several built-in node types:

```python
from haive.core.graph.node.types import NodeType

# Available node types
NodeType.ENGINE     # For engine-based nodes
NodeType.CALLABLE   # For function-based nodes
NodeType.TOOL       # For LangChain tool handling
NodeType.VALIDATION # For schema validation
NodeType.BRANCH     # For conditional routing
NodeType.SEND       # For send operations
```

### Input/Output Mapping

Nodes can map between state fields and engine/function parameters:

```python
# Create a node with input mapping
node = create_node(
    some_function,
    input_mapping={
        "function_arg1": "state_field1",
        "function_arg2": "state_field2"
    }
)

# Create a node with output mapping
node = create_node(
    some_function,
    output_mapping={
        "function_result1": "state_field1",
        "function_result2": "state_field2"
    }
)
```

### Command Routing

Nodes can specify the next node to execute:

```python
# Create a node with explicit next node
node = create_node(
    some_function,
    command_goto="next_node"
)

# Create a node that ends the graph
node = create_node(
    some_function,
    command_goto="END"  # Special constant for ending execution
)
```

## Integration with Other Modules

### Integration with Engine System

```python
from haive.core.graph.node import create_engine_node
from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.engine.retriever import RetrieverConfig

# Create engine configurations
llm_engine = AugLLMConfig(model="gpt-4")
retriever_engine = RetrieverConfig(type="vector_store")

# Create engine nodes
llm_node = create_engine_node(llm_engine)
retriever_node = create_engine_node(retriever_engine)
```

### Integration with Schema System

```python
from haive.core.graph.node import create_validation_node
from haive.core.schema.schema_composer import SchemaComposer

# Create a schema using SchemaComposer
composer = SchemaComposer(name="CustomSchema")
composer.add_field("query", str, default="")
composer.add_field("context", list, default_factory=list)
CustomSchema = composer.build()

# Create a validation node with the schema
validation_node = create_validation_node(
    schemas=[CustomSchema],
    name="validate"
)
```

### Integration with Graph Builder

```python
from haive.core.graph.node import create_node
from haive.core.graph.dynamic_graph_builder import DynamicGraphBuilder

# Create nodes
node1 = create_node(func1, name="node1", command_goto="node2")
node2 = create_node(func2, name="node2", command_goto="END")

# Add to graph builder
builder = DynamicGraphBuilder(state_type=MyState)
builder.add_node("node1", node1)
builder.add_node("node2", node2)
builder.set_entry_point("node1")

# Build the graph
graph = builder.build()
```

## Best Practices

- **Use Type Annotations**: Always use proper type annotations for node functions to ensure type safety
- **Isolate Node Logic**: Keep node functions focused on a single responsibility
- **Use Input/Output Mapping**: Instead of hardcoding field names, use mapping for flexibility
- **Leverage Decorators**: For simple nodes, use the decorator syntax for cleaner code
- **Use Validation Nodes**: Add validation nodes to ensure state consistency
- **Document Command Flow**: Clearly document the expected flow between nodes
- **Register Custom Nodes**: For specialized node types, register them with the registry

## Advanced Usage

### Custom Node Types

```python
from haive.core.graph.node import register_custom_node_type
from haive.core.graph.node.config import NodeConfig
from typing import List, Optional

# Create a custom node config
class BatchProcessorConfig(NodeConfig):
    batch_size: int = 10
    overlap: int = 0
    parallel: bool = False
    items_key: str = "items"

# Register the custom node type
register_custom_node_type("batch_processor", BatchProcessorConfig)

# Factory implementation for the custom node
def create_batch_processor_node(
    items_key: str,
    batch_size: int = 10,
    name: Optional[str] = None,
    command_goto: Optional[str] = None
):
    return create_node(
        None,
        name=name or "batch_processor",
        node_type="batch_processor",
        command_goto=command_goto,
        items_key=items_key,
        batch_size=batch_size
    )
```

### Complex Routing Patterns

```python
from haive.core.graph.node import create_branch_node, create_send_node

# Create a multi-condition branch
def complex_router(state):
    if state.query_type == "retrieval":
        return "retrieve"
    elif state.query_type == "generation":
        return "generate"
    elif state.query_type == "classification":
        return "classify"
    return "default"

router_node = create_branch_node(
    condition=complex_router,
    routes={
        "retrieve": "retriever_node",
        "generate": "generator_node",
        "classify": "classifier_node",
        "default": "default_node"
    }
)

# Create a fan-out pattern with send
def prepare_items(state):
    state.items = [{"id": i, "data": f"Item {i}"} for i in range(10)]
    return state

prepare_node = create_node(prepare_items, command_goto="distribute")

distribute_node = create_send_node(
    send_targets=["process_a", "process_b", "process_c"],
    send_state_key="items"
)
```

### Async Node Functions

```python
from haive.core.graph.node import create_node
import asyncio

# Create an async node function
async def async_processor(state):
    # Simulate async work
    await asyncio.sleep(1)
    state.result = "Processed asynchronously"
    return state

# Create a node with the async function
async_node = create_node(
    async_processor,
    name="async_processor",
    command_goto="next_node"
)
```

## API Reference

For full API details, see the [documentation](https://docs.haive.ai/core/graph/node).

## Related Modules

- **Graph System**: The broader graph system for building workflows
- **Engine System**: Provides the underlying execution engines used by nodes
- **Schema System**: Handles state schema definition and validation
- **Dynamic Graph Builder**: Constructs graphs with these nodes
