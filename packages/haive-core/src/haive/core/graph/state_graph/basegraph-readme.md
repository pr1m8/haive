# BaseGraph

## Overview

`BaseGraph` is the core graph implementation in the Haive framework, providing a comprehensive foundation for representing state-transition graphs. It serves as the underlying data structure for workflow orchestration, agent behavior modeling, and dynamic routing.

Unlike traditional graph libraries that focus primarily on mathematical graph operations, `BaseGraph` is specifically designed for AI workflows with features like conditional branching, dynamic routing, and serialization support.

## Key Features

- **Node Management**: Create, update, and remove graph nodes with associated callbacks
- **Edge Management**: Define directed connections between nodes
- **Branch Logic**: Rich support for conditional routing via branching mechanisms
- **Serialization**: Full serialization support for persistence and distribution
- **LangGraph Compatibility**: Two-way conversion with LangGraph StateGraphs
- **Visualization**: Built-in Mermaid diagram generation
- **Graph Manipulation**: Insert nodes, replace nodes, and rewire connections
- **Topology Analysis**: Path finding, orphan detection, dependency analysis

## Core Properties

| Property       | Description                                                  |
| -------------- | ------------------------------------------------------------ |
| `id`           | Unique identifier for the graph                              |
| `name`         | Human-readable name for the graph                            |
| `description`  | Optional description of the graph's purpose                  |
| `nodes`        | Dictionary of node objects keyed by name                     |
| `edges`        | List of edge tuples in the form `(source_node, target_node)` |
| `branches`     | Dictionary of Branch objects keyed by ID                     |
| `state_schema` | Optional schema defining the state structure (if any)        |
| `metadata`     | Arbitrary metadata for additional information                |
| `created_at`   | Timestamp when the graph was created                         |
| `updated_at`   | Timestamp when the graph was last updated                    |

## Primary Methods

### Node Management

```python
# Add a node
graph.add_node("process_query", process_query_func, node_type=NodeType.CALLABLE)

# Update a node
graph.update_node("process_query", description="Processes user queries")

# Get a node
node = graph.get_node("process_query")

# Remove a node
graph.remove_node("process_query")

# Replace a node
new_node = Node(name="new_process", metadata={"callable": new_func})
graph.replace_node("process_query", new_node)
```

### Edge Management

```python
# Add an edge
graph.add_edge("start_node", "process_node")

# Get edges
all_edges = graph.get_edges()
outgoing_edges = graph.get_edges(source="start_node")
incoming_edges = graph.get_edges(target="end_node")

# Remove an edge
graph.remove_edge("start_node", "process_node")

# Remove all edges from a source
graph.remove_edge("start_node")
```

### Branch Management

```python
# Create a branch checking a field value
branch = Branch(
    name="check_flag",
    source_node="router",
    key="flag",
    value=True,
    comparison=ComparisonType.EQUALS,
    destinations={True: "success_path", False: "error_path"}
)
graph.add_branch(branch)

# Add a function branch
graph.add_function_branch(
    source_node="router",
    condition=my_condition_func,
    routes={True: "success_path", False: "error_path"},
    name="custom_condition"
)

# Get a branch
branch = graph.get_branch(branch_id)
branch_by_name = graph.get_branch_by_name("check_flag")

# Update a branch
graph.update_branch(branch_id, default="fallback_node")

# Remove a branch
graph.remove_branch(branch_id)
```

### Advanced Node Operations

```python
# Insert a node after another node
graph.insert_node_after("source_node", "new_node", node_func)

# Insert a node before another node
graph.insert_node_before("target_node", "new_node", node_func)

# Add a node at the start of the graph
graph.add_prelude_node("prelude_node", prelude_func)

# Add a node at the end of the graph
graph.add_postlude_node("postlude_node", postlude_func)

# Add a sequence of nodes
sequence = [
    {"name": "node1", "node_type": NodeType.CALLABLE, "metadata": {"callable": func1}},
    {"name": "node2", "node_type": NodeType.CALLABLE, "metadata": {"callable": func2}}
]
graph.add_sequence(sequence, connect_start=True, connect_end=True)

# Add parallel branches
graph.add_parallel_branches(
    "source_node",
    [
        [{"name": "branch1_1", "metadata": {"callable": func1}}],
        [{"name": "branch2_1", "metadata": {"callable": func2}}]
    ],
    join_node={"name": "join_node", "metadata": {"callable": join_func}}
)
```

### Analysis Methods

```python
# Get node dependencies (incoming and outgoing connections)
deps = graph.get_node_dependencies("process_node")

# Check if there's a path between nodes
has_path = graph.has_path("start_node", "end_node")

# Get start nodes (nodes with incoming edges from START)
start_nodes = graph.get_start_nodes()

# Get end nodes (nodes with outgoing edges to END)
end_nodes = graph.get_end_nodes()

# Find orphaned nodes (not connected to the graph)
orphans = graph.get_orphan_nodes()

# Validate the graph structure
is_valid = graph.validate()
```

### Serialization

```python
# Convert to dictionary
graph_dict = graph.to_dict()

# Create from dictionary
reconstructed = BaseGraph.from_dict(graph_dict)

# Convert to JSON
json_str = graph.to_json()

# Create from JSON
from_json = BaseGraph.from_json(json_str)
```

### LangGraph Conversion

```python
# Convert from LangGraph StateGraph
from langgraph.graph import StateGraph
lg_graph = StateGraph(dict)
# ... configure LangGraph ...
base_graph = BaseGraph.from_langgraph(lg_graph, name="converted")

# Convert to LangGraph StateGraph
langgraph_graph = base_graph.to_langgraph()
```

### Visualization

```python
# Generate Mermaid diagram
mermaid = graph.to_mermaid()

# With custom settings
mermaid = graph.to_mermaid(
    include_branches=True,
    include_metadata=True,
    orientation="TD"  # Top-Down
)
```

## Usage Example

Here's a complete example of creating a graph with nodes, edges, and conditional branching:

```python
from haive.core.graph.state_graph.base_graph import BaseGraph, Node, NodeType, START_NODE, END_NODE
from haive.core.graph.branches import Branch, BranchMode, ComparisonType

# Define node functions
def process_input(state):
    # Process input
    return {"processed_input": state.get("input", "").upper()}

def check_input(state):
    # Check if input is valid
    return {"is_valid": len(state.get("processed_input", "")) > 0}

def handle_valid_input(state):
    # Handle valid input
    return {"response": f"Processed: {state.get('processed_input')}"}

def handle_invalid_input(state):
    # Handle invalid input
    return {"response": "Invalid input"}

# Create the graph
graph = BaseGraph(
    name="input_processor",
    description="Processes and validates user input"
)

# Add nodes
graph.add_node("process", process_input)
graph.add_node("check", check_input)
graph.add_node("handle_valid", handle_valid_input)
graph.add_node("handle_invalid", handle_invalid_input)

# Add edges
graph.add_edge(START_NODE, "process")
graph.add_edge("process", "check")

# Add branch
branch = Branch(
    name="input_validator",
    source_node="check",
    key="is_valid",
    value=True,
    comparison=ComparisonType.EQUALS,
    destinations={True: "handle_valid", False: "handle_invalid"}
)
graph.add_branch(branch)

# Connect to END
graph.add_edge("handle_valid", END_NODE)
graph.add_edge("handle_invalid", END_NODE)

# Validate the graph
graph.validate()

# Generate visualization
mermaid = graph.to_mermaid()
```

## Integration with SerializableGraph

While `BaseGraph` provides the core functionality, use `SerializableGraph` for full serialization support:

```python
from haive.core.graph.state_graph.serializable import SerializableGraph

# Convert BaseGraph to SerializableGraph
serializable = SerializableGraph.from_graph(graph)

# Export to JSON
json_str = serializable.to_json()

# Reconstruct
reconstructed_serializable = SerializableGraph.from_json(json_str)
reconstructed_graph = reconstructed_serializable.to_graph()
```

## Best Practices

1. **Unique Node Names**: Use descriptive, unique names for nodes to aid in debugging and visualization
2. **Node Reuse**: When possible, reuse node functions to maintain consistency
3. **Schema Definition**: Define a state schema when working with structured data
4. **Branch Organization**: Group related branches and use descriptive names
5. **Validation**: Always call `validate()` after making significant changes to ensure graph integrity
6. **Serialization**: Use `SerializableGraph` for persistence and distribution
7. **Metadata**: Use metadata to store additional information about nodes and the graph

## Limitations and Considerations

- Branch conditions should be pure functions to ensure predictable behavior
- Use caution when removing nodes that may be referenced by branches
- Very large graphs may impact performance and should be optimized
- Circular dependencies are allowed but can lead to infinite loops if not handled properly

## See Also

- `SerializableGraph`: For full serialization support
- `Branch`: For conditional routing and dynamic mapping
- `NodeType`: Enum defining supported node types
- `DynamicGraph`: Higher-level builder for workflow construction
