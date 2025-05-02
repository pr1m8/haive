# Dynamic Graph Building in Haive

## Overview

Haive's graph system extends LangGraph's capabilities with a focus on dynamic construction, validation, and enhanced node capabilities. The `DynamicGraph` class serves as the primary entry point for building agent workflows.

## Core Components

### DynamicGraph

The main builder class for creating state-aware, validated workflows:

```python
from haive.core.graph.dynamic_graph_builder import DynamicGraph
from haive.core.schema.state_schema import StateSchema
from pydantic import Field
from typing import List

# Define state schema
class MyAgentState(StateSchema):
    messages: List[dict] = Field(default_factory=list)
    context: dict = Field(default_factory=dict)

# Create graph builder
graph = DynamicGraph(
    name="MyAgentWorkflow",
    state_schema=MyAgentState,
    components=[llm_engine, retriever_engine]
)

# Add nodes
graph.add_node("retrieve", retriever_node)
graph.add_node("generate", llm_node)

# Add edges
graph.add_edge("retrieve", "generate")
graph.add_edge("generate", END)

# Compile the graph
runnable_graph = graph.build()
```

### NodeConfig

Configuration wrapper for node functions with enhanced debugging:

```python
from haive.core.graph.node.config import NodeConfig

# Create node with config
node_config = NodeConfig(
    debug=True,  # Enable debugging
    rich_debug=True,  # Use rich UI for debugging
    preserve_model=True,  # Preserve BaseModel instances in state
    input_mapping={"query": "user_query"},  # Map state fields to function parameters
    output_mapping={"result": "llm_result"}  # Map function outputs to state fields
)

# Create node function and add to graph
node = NodeFactory.create_node(llm_engine, config=node_config)
graph.add_node("llm_node", node)
```

## Advanced Routing

### Conditional Edges

Route execution based on state content:

```python
# Simple conditional
graph.add_conditional_edges(
    "router_node",
    lambda state: "path_a" if condition(state) else "path_b",
    {
        "path_a": "node_a",
        "path_b": "node_b"
    }
)

# Multi-path condition (parallel execution)
graph.add_conditional_edges(
    "router_node",
    lambda state: ["path_a", "path_b"] if parallel_condition(state) else ["path_c"],
    {
        "path_a": "node_a",
        "path_b": "node_b",
        "path_c": "node_c"
    }
)
```

### Branch Processing

Branches allow parallel execution with state merging:

```python
from haive.core.graph.branches import Branch

# Create a branch
branch = Branch(
    name="parallel_processing",
    nodes=["process_a", "process_b", "process_c"],
    entry_node="process_a",
    exit_node="process_c"
)

# Add branch to graph
graph.add_branch(branch)

# Connect to main flow
graph.add_edge("main_node", branch.entry_point)
graph.add_edge(branch.exit_point, "next_node")
```

## Node Types and Factory

The `NodeFactory` creates different types of node functions:

```python
from haive.core.graph.node.factory import NodeFactory

# Create engine-based node
retriever_node = NodeFactory.create_node(retriever_engine)

# Create callable-based node
def process_func(state):
    # Process state
    return {"result": process_result}

process_node = NodeFactory.create_callable_node(process_func)

# Create tool node
tool_node = NodeFactory.create_tool_node(tools=[search_tool, math_tool])
```

## Graph Patterns

Reusable workflow patterns can be applied to graphs:

```python
from haive.core.graph.patterns.registry import GraphPatternRegistry

# Get a registered pattern
pattern = GraphPatternRegistry.get_pattern("retry_on_error")

# Apply pattern to graph
pattern.apply(graph, target_node="api_call", max_retries=3)
```

Common patterns include:

- Retry policies
- Human-in-the-loop approvals
- Parallel processing
- Conditional branching
- Tool execution flows

## Interrupt Handling

For human-in-the-loop scenarios:

```python
from langgraph.graph import NodeInterrupt

def review_node(state):
    if requires_human_review(state):
        raise NodeInterrupt(
            {"state": state, "reason": "Requires human approval"}
        )
    return {"status": "auto_approved"}

# Resume execution
graph.stream(Command(resume={"approved": True, "feedback": "Looks good"}))
```

## Debugging and Visualization

Graph visualization tools:

```python
from haive.core.graph.utils.mermaid_visualizer import MermaidVisualizer

# Generate Mermaid diagram
visualizer = MermaidVisualizer(graph)
mermaid_code = visualizer.generate()

# Save to file
visualizer.save_to_file("graph_diagram.md")
```

To enable detailed node debugging:

```python
# Global debug configuration
NodeFactory.set_debug(True, rich_ui=True, log_path="debug_logs/")

# Per-node configuration
node_config = NodeConfig(
    debug=True,
    rich_debug=True,
    debug_log_path="debug_logs/node_execution.log"
)
```
