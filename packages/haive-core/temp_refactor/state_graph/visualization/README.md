# Graph Visualization

This module provides enhanced visualization capabilities for Haive state graphs, with a focus on improved subgraph handling and customization options.

## MermaidGenerator

The `MermaidGenerator` class is designed to generate Mermaid flowchart diagrams from state graphs. It offers significant improvements over the original `GraphVisualizer` class:

### Key Features

- **Hierarchical Subgraph Support**: Properly visualizes nested subgraphs with configurable depth limits
- **Improved Branch Visualization**: Better formatting for branch conditions with proper edge styling
- **Customizable Node Styling**: Configure node appearances based on their types
- **Node Type Detection**: Automatically detects and displays node types
- **Highlight Support**: Highlight specific nodes or paths for better visual analysis
- **Compatibility**: Works with both old and new graph structures

### Usage Example

```python
from haive.core.graph.state_graph import StateGraph, MermaidGenerator

# Create your graph
graph = StateGraph(name="MyGraph")
# ... add nodes, edges, branches, etc.

# Generate Mermaid diagram code
mermaid_code = MermaidGenerator.generate(
    graph=graph,
    include_subgraphs=True,
    highlight_nodes=["important_node"],
    theme="forest",
    max_depth=3,
    show_node_type=True
)

# You can then render this code using Mermaid renderers
# or save it to a file for later use
```

### Improvements Over GraphVisualizer

1. **Better Subgraph Handling**:
   - Properly handles nested subgraphs to any depth
   - Configurable maximum depth for subgraph rendering
   - Works with both direct subgraphs and subgraph registries

2. **Cleaner Code Structure**:
   - Modular design with methods for specific aspects of diagram generation
   - Better code organization and documentation

3. **Enhanced Compatibility**:
   - Works with the new state graph architecture
   - Maintains backward compatibility with older graph structures
   - Compatible with upcoming subgraph registry approach

4. **Better Node Type Detection**:
   - Improved detection of node types from different graph structures
   - Consistent display of type information

5. **Customization Options**:
   - More options for customizing the visualization output
   - Control over node type display, theme, and highlighting

## Rendering Mermaid Diagrams

Mermaid diagrams can be rendered in various ways:

- In Jupyter notebooks using the `display_mermaid` utility
- As PNG images using the `mermaid_to_png` utility
- In HTML reports using embedded Mermaid JavaScript
- In markdown documentation on platforms that support Mermaid (like GitHub)

## Integration

The MermaidGenerator is integrated with the main StateGraph class through the visualization module, making it easy to generate diagrams for any state graph.
