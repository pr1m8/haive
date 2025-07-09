# DynamicGraph Mermaid Visualizer

## Overview

A beautiful Mermaid-based visualization utility for Haive DynamicGraph instances. This utility replaces the original NetworkX-based visualization with an interactive, richly styled Mermaid diagram generator.

## Features

- **Rich Visual Styling**: Automatically styles nodes based on engine type (LLM, Retriever, VectorStore, etc.)
- **Interactive Diagrams**: Zoomable diagrams with interactive controls
- **Conditional Edge Visualization**: Clearly displays conditional routing with dashed lines and labels
- **Node Status Indicators**: Shows unreachable nodes with special styling
- **SVG Export**: One-click export to SVG format
- **PNG Rendering**: Optional rendering to PNG using mermaid.ink service
- **Type-Based Icons**: Adds intuitive icons to nodes based on their engine type
- **Comprehensive Legend**: Includes a detailed legend for all node and edge types
- **Graph Statistics**: Displays node, edge, and branch counts

## Installation

1. Copy the `graph_visualization_utils.py` file into your project
2. Import the necessary functions from the module

```python
from graph_visualization_utils import visualize_graph, replace_visualization_method
```

3. (Optional) Replace the original visualization method in DynamicGraph:

```python
replace_visualization_method()
```

## Usage

### Direct Usage

Use the `visualize_graph` function directly with any DynamicGraph instance:

```python
from graph_visualization_utils import visualize_graph

# Create your DynamicGraph
graph = DynamicGraph(...)

# Generate HTML visualization
html_path = visualize_graph(
    graph=graph,
    output_file="my_graph.html",
    open_browser=True,
    include_legend=True,
    format="html"
)

# Generate PNG visualization
png_path = visualize_graph(
    graph=graph,
    output_file="my_graph.png",
    open_browser=True,
    format="png"
)
```

### Replacing the Original Method

You can replace the original `visualize_graph` method in DynamicGraph:

```python
from graph_visualization_utils import replace_visualization_method

# Replace the visualization method
replace_visualization_method()

# Now use the enhanced visualization directly on your graph
graph = DynamicGraph(...)
graph.visualize_graph(output_file="my_graph.html")

# Or use the dedicated Mermaid method
graph.visualize_mermaid(output_file="my_graph.html")
```

## Examples

See the included example files:

- `test_graph_visualization.py`: Basic testing of the visualization functionality
- `visualization_comparison_example.py`: Comparison of original vs. enhanced visualization

## Requirements

- Required: `mermaid.js` (included via CDN in the generated HTML)
- Optional: `requests` (for PNG rendering)
- Optional: `networkx` and `matplotlib` (for maintaining compatibility with the original method)

## Visualization Types

### HTML Visualization

The primary output format is an HTML file with an embedded Mermaid diagram. This provides:

- Interactive zooming and panning
- One-click SVG download
- Mermaid code copying
- Detailed legend
- Graph statistics

### PNG Visualization

For static graphics, the utility can also generate PNG files using the mermaid.ink service:

- Requires internet connection
- Requires the `requests` library
- Creates a clean, shareable image file

## Configuration

You can configure the appearance of the diagrams by modifying the `MermaidStyle` class in the utility:

- `NODE_STYLES`: Styling for different node types
- `EDGE_STYLES`: Styling for different edge types
- `NODE_ICONS`: Icons for different node types
- `GRAPH_THEME`: Overall theme settings for the diagram

## License

This utility is provided as part of the Haive framework.
