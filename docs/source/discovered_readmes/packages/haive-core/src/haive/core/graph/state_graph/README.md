# Haive Graph System

This module provides a comprehensive graph implementation for the Haive framework, with flexible node and branch management, visualization capabilities, and LangGraph integration.

## Overview

The state graph system serves as the core computational graph infrastructure in the Haive framework, enabling the creation, manipulation, and execution of complex workflows with robust state management and schema validation.

### Core Components

- `BaseGraph`: The foundational graph implementation with all core functionality
- `SchemaGraph`: Extended graph with schema validation and management capabilities
- `Node`: The node component implementation for processing state
- `Branch`: The branch component for conditional routing and decision points

### Key Features

- **Schema Validation**: Enforce type safety through Pydantic models
- **Dynamic Routing**: Create complex workflows with conditional branching
- **Serialization**: Full serialization and deserialization support
- **LangGraph Integration**: Seamless integration with LangChain's LangGraph
- **Visualization**: Built-in visualization capabilities
- **Pattern Support**: Reusable graph patterns and templates

### Directory Structure

```
haive/core/graph/state_graph/
├── __init__.py                   # Public exports
├── base_graph2.py                # Core graph implementation
├── schema_graph.py               # Schema-aware graph
├── state_graph.py                # State graph serialization model
├── validation_mixin.py           # Graph validation functionality
├── schema_mixin.py               # Schema management
├── graph_visualizer.py           # Graph visualization
├── components/                   # Core components
│   ├── __init__.py
│   ├── node.py                   # Node implementation
│   └── branch.py                 # Branch implementation
├── models/                       # Data models
│   ├── node_model.py             # Node models
│   ├── edge_model.py             # Edge models
│   ├── branch_model.py           # Branch models
│   └── state_graph_model.py      # Graph models
├── conversion/                   # Format conversion
│   ├── __init__.py
│   └── langgraph.py              # LangGraph conversion
├── pattern/                      # Graph patterns
│   ├── __init__.py
│   ├── base.py                   # Base pattern implementation
│   └── implementations.py        # Pattern implementations
└── utils/                        # Utilities
    ├── __init__.py
    └── ...                       # Utility functions
```

## Usage

### Basic Graph Creation

```python
from haive.core.graph.state_graph import BaseGraph
from langgraph.graph import START, END

# Create a new graph
graph = BaseGraph(name="my_graph")

# Add nodes
graph.add_node("node1", lambda state: state)
graph.add_node("node2", lambda state: state)

# Add edges
graph.add_edge(START, "node1")
graph.add_edge("node1", "node2")
graph.add_edge("node2", END)

# Compile and run the graph
compiled_graph = graph.compile()
result = compiled_graph.invoke({"input": "some input"})
```

### Schema-aware Graph

```python
from pydantic import BaseModel
from haive.core.graph.state_graph import SchemaGraph

# Define state schema
class MyState(BaseModel):
    count: int = 0
    messages: list = []

# Create schema-aware graph
graph = SchemaGraph(
    name="schema_graph",
    state_schema=MyState
)

# Add processing nodes
graph.add_node("increment", lambda state: {"count": state.count + 1})

# Convert to LangGraph for execution
langgraph = graph.to_langgraph()
```

### Conditional Branching

```python
from haive.core.graph.state_graph import BaseGraph
from langgraph.graph import START, END

graph = BaseGraph(name="branching_graph")

# Add nodes
graph.add_node("check_input", lambda state: state)
graph.add_node("process_a", lambda state: {"result": "processed by A"})
graph.add_node("process_b", lambda state: {"result": "processed by B"})

# Add conditional branch
def route_condition(state):
    if state.get("input", "").startswith("a"):
        return "a"
    return "b"

graph.add_conditional_edge(
    "check_input",
    route_condition,
    {"a": "process_a", "b": "process_b"}
)

# Connect start and end
graph.add_edge(START, "check_input")
graph.add_edge("process_a", END)
graph.add_edge("process_b", END)
```

### Using Components Directly

```python
from haive.core.graph.state_graph.components import Node, Branch
from haive.core.graph.common.types import NodeType

# Create a node
node = Node(
    name="my_node",
    node_type=NodeType.CALLABLE,
    metadata={"callable": lambda state: state}
)

# Create a branch
branch = Branch(
    name="my_branch",
    source_node="source",
    mode=BranchMode.FUNCTION,
    function=lambda state: "route_a" if state.get("value") > 10 else "route_b",
    destinations={"route_a": "target_a", "route_b": "target_b"}
)
```

## Advanced Features

### Graph Patterns

```python
from haive.core.graph.state_graph import BaseGraph
from haive.core.graph.state_graph.pattern import SequentialPattern

# Create a pattern
pattern = SequentialPattern(
    nodes=[
        ("extract", lambda state: {"extracted": state["input"]}),
        ("transform", lambda state: {"transformed": state["extracted"].upper()}),
        ("load", lambda state: {"result": f"Processed: {state['transformed']}"})
    ]
)

# Apply pattern to graph
graph = BaseGraph(name="etl_graph")
pattern.apply(graph)
```

### Graph Visualization

```python
from haive.core.graph.state_graph import BaseGraph, GraphVisualizer

graph = BaseGraph(name="visualization_example")
# ... add nodes and edges ...

# Create visualizer
visualizer = GraphVisualizer(graph)

# Generate visualization
visualizer.draw(output_path="graph.png")
```

## Development

The Haive graph system is designed to be extensible and modular. Key principles:

1. **Separation of Concerns**: Components are separated into their own files
2. **Clear Interfaces**: Each module has a well-defined public interface
3. **Type Safety**: Generic parameters ensure type safety
4. **Compatibility**: Both backward compatibility and LangGraph integration

When extending the system, follow these guidelines:

- Add new functionality via mixins or derived classes rather than modifying core classes
- Document all public methods and classes with docstrings
- Add type annotations to all methods and functions
- Write tests for new functionality

## Migration Path

The current implementation is in transition from the older `base_graph.py` to the newer `base_graph2.py`. The final step will be to rename `base_graph2.py` to `base_graph.py` once all functionality is migrated and tested.
