# StateGraph System Implementation Plan

This document outlines the implementation plan for the new StateGraph system, tracking progress and next steps.

## 1. Completed Tasks

### High Priority

- ✅ Created directory structure for new architecture
- ✅ Implemented base module with core types and base classes
- ✅ Created mixins for schema and validation
- ✅ Implemented CompilationMixin and tracking
- ✅ Created StateGraph class composing all components
- ✅ Updated imports and created migration guide

### Current Directory Structure

```
temp_refactor/state_graph/
├── __init__.py                # Main exports
├── base/                      # Core components
│   ├── __init__.py
│   ├── graph_base.py          # Base graph structure
│   ├── graph_state.py         # Compilation state tracking
│   └── types.py               # Type definitions
├── mixins/                    # Reusable functionality
│   ├── __init__.py
│   ├── compilation_mixin.py   # Compilation tracking
│   ├── schema_mixin.py        # Schema management
│   └── validation_mixin.py    # Graph validation
├── components/                # Core components (empty)
├── operations/                # Graph operations (empty)
├── conversion/                # Format conversions (empty)
├── visualization/             # Visualization tools (empty)
├── utils/                     # Utility functions (empty)
├── graph.py                   # Main StateGraph implementation
├── schema_graph.py            # Schema-aware graph implementation
├── README.md                  # Usage documentation
└── MIGRATION.md               # Migration guide
```

## 2. Pending Tasks

### Medium Priority

- [ ] Extract node operations from base_graph2.py
- [ ] Extract edge and branch operations
- [ ] Implement Subgraph class and SubgraphMixin
- [ ] Enhance visualization with better subgraph support

### Low Priority

- [ ] Add tests for the new implementation
- [ ] Add examples demonstrating different use cases
- [ ] Create more detailed documentation of advanced features

## 3. Implementation Details

### 3.1. Extract Node Operations

These operations should be extracted into `operations/node_ops.py`:

- `add_node`
- `remove_node`
- `update_node`
- `replace_node`
- `insert_node_after/before`
- `add_prelude_node/postlude_node`
- `add_sequence`
- Node-related utilities (e.g., `_track_node_type`)

### 3.2. Extract Edge and Branch Operations

These operations should be extracted into `operations/edge_ops.py` and `operations/branch_ops.py`:

Edge operations:

- `add_edge`
- `remove_edge`
- `get_edges`
- `find_all_paths`

Branch operations:

- `add_branch`
- `add_conditional_edges`
- `add_function_branch`
- `add_key_value_branch`
- `remove_branch`
- `update_branch`
- `replace_branch`

### 3.3. Implement Subgraph Class and SubgraphMixin

Create components for subgraph handling:

- `components/subgraph.py`: Wrapper for a subgraph in a parent graph
- `components/subgraph_registry.py`: Registry for managing subgraphs
- `mixins/subgraph_mixin.py`: Mixin that adds subgraph management to a graph

Key functionality:

- Encapsulate subgraphs with input/output mapping
- Registry for managing subgraphs
- Methods for adding/removing/updating subgraphs

### 3.4. Enhance Visualization

Improve visualization with better subgraph support:

- `visualization/mermaid_generator.py`: Enhanced Mermaid diagram generation
- `visualization/graph_visualizer.py`: Graph visualization utilities
- `visualization/interactive_explorer.py`: Interactive graph explorer

Key features:

- Hierarchical rendering of subgraphs
- Proper styling and layout
- Interactive exploration

## 4. Usage Examples

### Basic Graph

```python
from haive.core.graph.state_graph import StateGraph, START, END

# Create a graph
graph = StateGraph(name="my_graph")

# Add nodes
graph.add_node("node1", lambda state: {"processed": True, **state})
graph.add_node("node2", lambda state: {"result": "success", **state})

# Add edges
graph.add_edge(START, "node1")
graph.add_edge("node1", "node2")
graph.add_edge("node2", END)

# Compile and run
result = graph.invoke({"input": "value"})
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

# Add nodes
graph.add_node("increment", lambda state: MyState(count=state.count + 1, messages=state.messages))
graph.add_node("add_message", lambda state: MyState(count=state.count, messages=state.messages + ["processed"]))

# Add edges
graph.add_edge(START, "increment")
graph.add_edge("increment", "add_message")
graph.add_edge("add_message", END)

# Input is validated against schema
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
graph.add_edge(START, "check_count")
graph.add_edge("high_count", END)
graph.add_edge("low_count", END)
```

## 5. Migration Path

1. Complete implementation of remaining components
2. Add comprehensive tests to verify functionality
3. Create clear documentation and examples
4. Rename `base_graph2.py` to `deprecated_base_graph2.py`
5. Update the current `__init__.py` to export the new classes
6. Support a transition period with warnings when using deprecated methods
7. Gradually update all code using BaseGraph to use StateGraph

## 6. Design Principles

The new StateGraph system follows these design principles:

1. **Separation of Concerns**: Each component has a single responsibility
2. **Composition over Inheritance**: Use mixins to add functionality
3. **Clean API**: Intuitive methods that mirror LangGraph
4. **Efficient Compilation**: Only recompile when necessary
5. **Type Safety**: Leverage Python type hints throughout
6. **Backward Compatibility**: Support easy migration
7. **Extensibility**: Allow adding new features easily
