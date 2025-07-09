# Haive StateGraph System

A modular, maintainable, and powerful graph system for the Haive framework.

## Overview

The StateGraph system is a comprehensive graph implementation that provides:

- Efficient compilation tracking to optimize performance
- Powerful schema validation and management
- Flexible node, edge, and branch operations
- Subgraph support for hierarchical structures
- Enhanced visualization capabilities

## Core Components

- **GraphBase**: The foundation graph data structure
- **StateGraph**: Main graph implementation with all features
- **SchemaGraph**: Schema-aware graph with enhanced validation

## Usage Examples

### Basic Graph Creation

```python
from haive.core.graph.state_graph import StateGraph, START, END

# Create a graph
graph = StateGraph(name="my_graph")

# Add nodes
graph.add_node("node1", lambda state: state)
graph.add_node("node2", lambda state: state)

# Add edges
graph.add_edge(START, "node1")
graph.add_edge("node1", "node2")
graph.add_edge("node2", END)

# Compile and run
compiled_graph = graph.compile()
result = compiled_graph.invoke({"input": "value"})
```

### Schema-Aware Graph

```python
from pydantic import BaseModel
from haive.core.graph.state_graph import SchemaGraph

# Define a schema
class MyState(BaseModel):
    count: int = 0
    messages: list = []

# Create a schema-aware graph
graph = SchemaGraph(
    name="schema_graph",
    state_schema=MyState
)

# All inputs and outputs will be validated against the schema
result = graph.invoke({"count": 1, "messages": ["Hello"]})
```

### Conditional Branching

```python
from haive.core.graph.state_graph import StateGraph

# Create a graph
graph = StateGraph(name="branch_example")

# Add nodes
graph.add_node("check_count", lambda state: {"count": state.get("count", 0) + 1})
graph.add_node("high_count", lambda state: {"result": "high", **state})
graph.add_node("low_count", lambda state: {"result": "low", **state})

# Add conditional branching
graph.add_conditional_edges(
    "check_count",
    lambda state: state["count"] > 5,  # Condition function
    {True: "high_count", False: "low_count"}  # Routing
)

# Connect to START and END
graph.set_entry_point("check_count")
graph.add_edge("high_count", END)
graph.add_edge("low_count", END)
```

## Migration Guide

If you're migrating from the older BaseGraph implementation, here's how to update your code:

### Before

```python
from haive.core.graph.state_graph.base_graph2 import BaseGraph

graph = BaseGraph(name="my_graph")
graph.add_node("node1", lambda state: state)
```

### After

```python
from haive.core.graph.state_graph import StateGraph

graph = StateGraph(name="my_graph")
graph.add_node("node1", lambda state: state)
```

Key differences:

- Use `StateGraph` instead of `BaseGraph`
- Imports are simplified (just import from `haive.core.graph.state_graph`)
- Compilation is tracked automatically
- Methods like `add_node` and `add_edge` automatically mark the graph as needing recompilation

## Advanced Features

The new StateGraph system includes many advanced features:

- **Compilation Tracking**: Smart detection of when recompilation is needed
- **Validation**: Built-in graph validation to catch issues early
- **Schema Management**: Type-safe schema validation for state
- **Subgraphs**: Support for hierarchical graph structures
- **Enhanced Visualization**: Better visualization with hierarchical subgraph support

### Visualization

The system includes a powerful visualization system through the `MermaidGenerator` class:

```python
from haive.core.graph.state_graph import StateGraph, MermaidGenerator

# Create and set up your graph
graph = StateGraph(name="my_workflow")
# ... add nodes, edges, etc.

# Generate Mermaid diagram
mermaid_code = MermaidGenerator.generate(
    graph=graph,
    include_subgraphs=True,
    highlight_nodes=["important_node"],
    theme="forest",
    max_depth=3
)

# Use with mermaid utilities
from haive.core.utils.mermaid_utils import display_mermaid
display_mermaid(mermaid_code)
```

Key visualization features:

- Hierarchical rendering of nested subgraphs
- Customizable node and edge styling
- Conditional branch visualization
- Node highlighting for path analysis
- Configurable depth limit for complex graphs

## Architecture

The system follows a modular architecture with components organized by responsibility:

```
state_graph/
├── base/              # Core data structures and types
├── components/        # Key building blocks
├── mixins/            # Reusable functionality
├── operations/        # Graph operations
├── conversion/        # Format conversions
├── visualization/     # Visualization tools
├── utils/             # Utility functions
├── graph.py           # Main StateGraph implementation
└── schema_graph.py    # Schema-aware graph
```

## Extending the System

To extend the system, you can create new mixins or subclass existing components.

### Creating a custom graph

```python
from haive.core.graph.state_graph import StateGraph

class MyCustomGraph(StateGraph):
    def __init__(self, name, **kwargs):
        super().__init__(name=name, **kwargs)

    def my_custom_method(self):
        # Custom functionality
        pass
```
