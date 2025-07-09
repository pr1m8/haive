# Migration Guide for StateGraph System

This guide will help you migrate from the older base_graph2.py implementation to the new modular StateGraph system.

## Overview of Changes

- **New API**: More intuitive API similar to LangGraph
- **Better Organization**: Modular architecture with focused components
- **Compilation Tracking**: Automatic tracking of when recompilation is needed
- **Improved Schema Support**: Better handling of schemas and validation
- **Enhanced Visualization**: Better visualization of complex graphs

## Migration Steps

### 1. Update Imports

**Before:**

```python
from haive.core.graph.state_graph.base_graph2 import BaseGraph
from langgraph.graph import START, END
```

**After:**

```python
from haive.core.graph.state_graph import StateGraph, START, END
```

### 2. Replace BaseGraph with StateGraph

**Before:**

```python
graph = BaseGraph(name="my_graph")
```

**After:**

```python
graph = StateGraph(name="my_graph")
```

### 3. Update Schema Handling

**Before:**

```python
from pydantic import BaseModel

class MyState(BaseModel):
    count: int = 0

graph = BaseGraph(name="my_graph", state_schema=MyState)
```

**After:**

```python
from pydantic import BaseModel
from haive.core.graph.state_graph import SchemaGraph

class MyState(BaseModel):
    count: int = 0

graph = SchemaGraph(name="my_graph", state_schema=MyState)
```

### 4. Simplify Node Addition

**Before:**

```python
graph.add_node("node1", lambda state: state, node_type="CALLABLE")
```

**After:**

```python
graph.add_node("node1", lambda state: state)
```

### 5. Use the New Conditional Edges API

**Before:**

```python
graph.add_conditional_edges(
    "source_node",
    lambda state: state["count"] > 5,
    {"True": "high_count", "False": "low_count"},
    END
)
```

**After:**

```python
graph.add_conditional_edges(
    "source_node",
    lambda state: state["count"] > 5,
    {True: "high_count", False: "low_count"}
)
```

### 6. Take Advantage of Compilation Tracking

**Before:**

```python
# Always recompile after changes
lang_graph = graph.to_langgraph()
compiled = lang_graph.compile()
result = compiled.invoke(input_data)
```

**After:**

```python
# Compilation happens automatically when needed
result = graph.invoke(input_data)

# Or if you want to control when compilation happens:
compiled = graph.compile()  # Only recompiles if changes were made
result = compiled.invoke(input_data)
```

### 7. Use Enhanced Validation

**Before:**

```python
# Manual validation
issues = graph.check_graph_validity()
if issues:
    print("Issues found:", issues)
```

**After:**

```python
# Rich detailed validation
graph.display_validation_report()

# Or programmatically:
issues = graph.validate_graph()
if issues:
    print("Issues found:", issues)
```

## Feature-by-Feature Migration

### Node Operations

| Old (BaseGraph)                      | New (StateGraph)                     |
| ------------------------------------ | ------------------------------------ |
| `add_node(node_name, node_callable)` | `add_node(node_name, node_callable)` |
| `remove_node(node_name)`             | `remove_node(node_name)`             |
| `update_node(node_name, **updates)`  | `update_node(node_name, **updates)`  |
| `replace_node(node_name, new_node)`  | `replace_node(node_name, new_node)`  |

### Edge Operations

| Old (BaseGraph)               | New (StateGraph)              |
| ----------------------------- | ----------------------------- |
| `add_edge(source, target)`    | `add_edge(source, target)`    |
| `remove_edge(source, target)` | `remove_edge(source, target)` |

### Branch Operations

| Old (BaseGraph)                                          | New (StateGraph)                                         |
| -------------------------------------------------------- | -------------------------------------------------------- |
| `add_conditional_edges(source, condition, destinations)` | `add_conditional_edges(source, condition, destinations)` |
| `add_branch(branch_name, source_node, ...)`              | Use `add_conditional_edges` instead                      |

### Compilation & Execution

| Old (BaseGraph)              | New (StateGraph)                                   |
| ---------------------------- | -------------------------------------------------- |
| `to_langgraph(); .compile()` | `compile()` or `invoke()` (automatic compilation)  |
| Manual recompilation         | Automatic tracking of when recompilation is needed |

## Common Migration Scenarios

### Scenario 1: Simple Graph with Direct Edges

**Before:**

```python
from haive.core.graph.state_graph.base_graph2 import BaseGraph
from langgraph.graph import START, END

graph = BaseGraph(name="simple_graph")
graph.add_node("node1", lambda state: state)
graph.add_node("node2", lambda state: state)
graph.add_edge(START, "node1")
graph.add_edge("node1", "node2")
graph.add_edge("node2", END)

lang_graph = graph.to_langgraph()
compiled = lang_graph.compile()
result = compiled.invoke({"input": "value"})
```

**After:**

```python
from haive.core.graph.state_graph import StateGraph, START, END

graph = StateGraph(name="simple_graph")
graph.add_node("node1", lambda state: state)
graph.add_node("node2", lambda state: state)
graph.add_edge(START, "node1")
graph.add_edge("node1", "node2")
graph.add_edge("node2", END)

result = graph.invoke({"input": "value"})
```

### Scenario 2: Graph with Conditional Routing

**Before:**

```python
from haive.core.graph.state_graph.base_graph2 import BaseGraph
from langgraph.graph import START, END

graph = BaseGraph(name="conditional_graph")
graph.add_node("check", lambda state: state)
graph.add_node("path_a", lambda state: state)
graph.add_node("path_b", lambda state: state)

graph.add_edge(START, "check")
graph.add_conditional_edges(
    "check",
    lambda state: state.get("condition", False),
    {True: "path_a", False: "path_b"}
)
graph.add_edge("path_a", END)
graph.add_edge("path_b", END)

lang_graph = graph.to_langgraph()
compiled = lang_graph.compile()
result = compiled.invoke({"condition": True})
```

**After:**

```python
from haive.core.graph.state_graph import StateGraph, START, END

graph = StateGraph(name="conditional_graph")
graph.add_node("check", lambda state: state)
graph.add_node("path_a", lambda state: state)
graph.add_node("path_b", lambda state: state)

graph.add_edge(START, "check")
graph.add_conditional_edges(
    "check",
    lambda state: state.get("condition", False),
    {True: "path_a", False: "path_b"}
)
graph.add_edge("path_a", END)
graph.add_edge("path_b", END)

result = graph.invoke({"condition": True})
```

## Handling Deprecated Features

Some features from the old implementation are deprecated or have been replaced with better alternatives:

| Deprecated Feature | Replacement                                     |
| ------------------ | ----------------------------------------------- |
| `entry_point`      | `entry_points` (supports multiple entry points) |
| `finish_point`     | `finish_points` (supports multiple exit points) |
| `add_branch(...)`  | `add_conditional_edges(...)` (cleaner API)      |
| `to_langgraph()`   | `compile()` (includes validation)               |
| `to_mermaid()`     | `visualize()` (enhanced visualization)          |

### 8. Use the New Visualization System

**Before:**

```python
from haive.core.graph.state_graph.graph_visualizer import GraphVisualizer

# Generate and display a diagram
mermaid = GraphVisualizer.generate_mermaid(graph)
GraphVisualizer.display_graph(graph, highlight_nodes=["important_node"])
```

**After:**

```python
from haive.core.graph.state_graph import MermaidGenerator
from haive.core.utils.mermaid_utils import display_mermaid

# Generate a diagram with more options
mermaid = MermaidGenerator.generate(
    graph=graph,
    include_subgraphs=True,
    max_depth=3,
    highlight_nodes=["important_node"]
)

# Display the diagram
display_mermaid(mermaid)

# Or use the convenience method on the graph
graph.visualize(highlight_nodes=["important_node"])
```

Key improvements:

- Better handling of nested subgraphs (configurable depth)
- Improved styling and readability
- More customization options
- Better support for complex branch conditions

## Need Help?

If you encounter issues during migration, please refer to the documentation or ask for assistance from the development team.
