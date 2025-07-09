"""
Graph visualization utilities for DynamicGraph.

This module provides enhanced visualization capabilities using Mermaid diagrams
with rich styling, interactive features, and multiple output formats.
"""

import base64
import logging
import os
import webbrowser
from datetime import datetime
from enum import Enum
from typing import Any, Optional

# Configure logger
logger = logging.getLogger(__name__)

# Try to import optional dependencies
try:
    import matplotlib.pyplot as plt
    import networkx as nx
    VISUALIZATION_AVAILABLE = True
except ImportError:
    VISUALIZATION_AVAILABLE = False

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False

# Node status class for compatibility
class NodeStatus(str, Enum):
    """Status of nodes in the graph."""
    ADDED = "added"
    CONNECTED = "connected"
    UNREACHABLE = "unreachable"
    ERROR = "error"

class MermaidStyle:
    """Style configurations for Mermaid diagrams."""
    # Node styles by type and status
    NODE_STYLES = {
        # Basic types
        "default": "fill:#f9f9f9,stroke:#999,stroke-width:1px",
        "start": "fill:#d0f0c0,stroke:#2c6b2c,stroke-width:2px",
        "end": "fill:#ffcccc,stroke:#990000,stroke-width:2px",
        
        # Status-based styles
        "unreachable": "fill:#f5f5f5,stroke:#999,stroke-dasharray:5 2,stroke-width:1px",
        "error": "fill:#ffe6e6,stroke:#cc0000,stroke-width:1px",
        
        # Engine-based styles
        "llm": "fill:#e1f5fe,stroke:#0288d1,stroke-width:1px",
        "retriever": "fill:#e8f5e9,stroke:#388e3c,stroke-width:1px",
        "vectorstore": "fill:#ede7f6,stroke:#673ab7,stroke-width:1px",
        "embeddings": "fill:#fce4ec,stroke:#c2185b,stroke-width:1px",
        "tool": "fill:#fff8e1,stroke:#ffa000,stroke-width:1px",
        "agent": "fill:#bbdefb,stroke:#1976d2,stroke-width:1px"
    }
    
    # Edge styles by type
    EDGE_STYLES = {
        "default": "stroke:#666,stroke-width:1px",
        "conditional": "stroke:#ff6600,stroke-width:1.5px,stroke-dasharray:5 2",
        "start": "stroke:#2c6b2c,stroke-width:2px",
        "end": "stroke:#990000,stroke-width:1.5px"
    }
    
    # Node icons
    NODE_ICONS = {
        "start": "🚀",
        "end": "🏁",
        "llm": "💬",
        "retriever": "🔍",
        "vectorstore": "📊",
        "embeddings": "📈",
        "tool": "🔧",
        "agent": "🤖",
        "default": "⚙️"
    }
    
    # Graph theme settings
    GRAPH_THEME = {
        "background": "#ffffff",
        "font_family": "Arial, sans-serif",
        "title_color": "#333333",
        "node_border_radius": "8px",
        "edge_curve": "basis"
    }

class MermaidVisualizer:
    """
    Enhanced Mermaid diagram visualizer for DynamicGraph.
    
    Generates interactive, richly styled Mermaid diagrams for graph visualization
    with special handling for different node and edge types.
    """
    
    def __init__(self, graph: Any):
        """
        Initialize with a DynamicGraph instance.
        
        Args:
            graph: DynamicGraph instance to visualize
        """
        self.graph = graph
        self.node_types = {}
        self.edge_types = {}
        
        # Analyze graph structure
        self._analyze_graph()
    
    def _analyze_graph(self):
        """Analyze graph structure to categorize nodes and edges."""
        self._analyze_node_types()
        self._analyze_edge_types()
    
    def _analyze_node_types(self):
        """
        Analyze and categorize nodes by their engine types.
        """
        for name, node_config in getattr(self.graph, 'nodes', {}).items():
            # Default type
            node_type = "default"
            
            # Try to determine node type from engine
            engine = getattr(node_config, 'engine', None)
            
            if engine:
                if hasattr(engine, 'engine_type'):
                    # Get type from engine_type attribute
                    engine_type = getattr(engine, 'engine_type', None)
                    if engine_type:
                        # Convert enum to string if needed
                        if hasattr(engine_type, 'value'):
                            node_type = str(engine_type.value).lower()
                        else:
                            node_type = str(engine_type).lower()
                elif isinstance(engine, str):
                    # For string references, try to infer type from name
                    engine_lower = engine.lower()
                    if any(t in engine_lower for t in ['llm', 'gpt', 'chat']):
                        node_type = 'llm'
                    elif any(t in engine_lower for t in ['retriev', 'search']):
                        node_type = 'retriever'
                    elif any(t in engine_lower for t in ['vector', 'store', 'db']):
                        node_type = 'vectorstore'
                    elif any(t in engine_lower for t in ['embed']):
                        node_type = 'embeddings'
                    elif any(t in engine_lower for t in ['tool', 'util']):
                        node_type = 'tool'
                    elif any(t in engine_lower for t in ['agent']):
                        node_type = 'agent'
                elif callable(engine):
                    # For callable functions, use "tool" type
                    node_type = 'tool'
            
            self.node_types[name] = node_type
    
    def _analyze_edge_types(self):
        """
        Analyze and categorize edges by their types.
        """
        for edge in getattr(self.graph, 'edges', []):
            source = edge.source
            target = edge.target
            
            # Determine edge type
            if hasattr(edge, 'condition') and edge.condition:
                edge_type = "conditional"
            elif source in ["START", "__start__", "start"]:
                edge_type = "start"
            elif target in ["END", "__end__", "end"]:
                edge_type = "end"
            else:
                edge_type = "default"
            
            self.edge_types[(source, target)] = edge_type
    
    def _sanitize_id(self, node_id: str) -> str:
        """
        Sanitize node ID for Mermaid compatibility.
        
        Args:
            node_id: Original node ID
            
        Returns:
            Sanitized node ID safe for Mermaid
        """
        # Handle special constants
        if node_id in ["START", "__start__", "start"]:
            return "START"
        if node_id in ["END", "__end__", "end"]:
            return "END"
        
        # Remove problematic characters and spaces
        sanitized = str(node_id).replace(" ", "_").replace("-", "_")
        
        # If the ID starts with a number, prefix with n_
        if sanitized and sanitized[0].isdigit():
            sanitized = f"n_{sanitized}"
            
        # Handle any other special characters by replacing them
        import re
        sanitized = re.sub(r'[^a-zA-Z0-9_]', '_', sanitized)
        
        return sanitized
    
    def generate_mermaid(self, include_stats: bool = True) -> str:
        """
        Generate Mermaid diagram definition.
        
        Args:
            include_stats: Whether to include graph statistics
            
        Returns:
            Mermaid diagram definition string
        """
        # Start with graph definition and theme configuration
        mermaid_lines = [
            "%%{init: {",
            "  'theme': 'base',",
            "  'themeVariables': {",
            f"    'primaryColor': '{MermaidStyle.GRAPH_THEME['background']}',",
            "    'primaryTextColor': '#333',",
            "    'primaryBorderColor': '#999',",
            "    'lineColor': '#666',",
            f"    'fontFamily': '{MermaidStyle.GRAPH_THEME['font_family']}'",
            "  }",
            "} }%%",
            "",
            "flowchart TB",
            f"  %% {getattr(self.graph, 'name', 'DynamicGraph')} Visualization",
            "  %% Generated by MermaidVisualizer"
        ]
        
        # Add statistics if requested
        if include_stats:
            nodes_count = len(getattr(self.graph, 'nodes', {}))
            edges_count = len(getattr(self.graph, 'edges', []))
            branches_count = len(getattr(self.graph, 'branches', []))
            
            mermaid_lines.extend([
                f"  %% Nodes: {nodes_count}",
                f"  %% Edges: {edges_count}",
                f"  %% Branches: {branches_count}",
                f"  %% Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            ])
        
        # Add special nodes (START/END)
        special_nodes = set()
        
        # Add START node
        mermaid_lines.append("  START([\"🚀 Start\"])"])")
        mermaid_lines.append(f"  style START {MermaidStyle.NODE_STYLES['start']}")
        special_nodes.add("START")
        
        # Add END node
        mermaid_lines.append("  END([\"🏁 End\"])"])")
        mermaid_lines.append(f"  style END {MermaidStyle.NODE_STYLES['end']}")
        special_nodes.add("END")
        
        # Track processed nodes to avoid duplicates
        processed_nodes = set(special_nodes)
        
        # Add regular nodes
        for name, _node_config in getattr(self.graph, 'nodes', {}).items():
            if name in processed_nodes:
                continue
                
            # Get node details for richer visualization
            node_type = self.node_types.get(name, "default")
            node_status = getattr(self.graph, 'node_statuses', {}).get(name, NodeStatus.ADDED)
            
            # Create node ID (escape special characters for Mermaid)
            node_id = self._sanitize_id(name)
            
            # Get icon for node type
            icon = MermaidStyle.NODE_ICONS.get(node_type, MermaidStyle.NODE_ICONS["default"])
            
            # Add node with appropriate shape and icon
            mermaid_lines.append(f"  {node_id}[\"{icon} {name}\"]")
            
            # Apply style based on node type and status
            if node_status == NodeStatus.UNREACHABLE:
                mermaid_lines.append(f"  style {node_id} {MermaidStyle.NODE_STYLES['unreachable']}")
            elif node_status == NodeStatus.ERROR:
                mermaid_lines.append(f"  style {node_id} {MermaidStyle.NODE_STYLES['error']}")
            else:
                mermaid_lines.append(f"  style {node_id} {MermaidStyle.NODE_STYLES[node_type]}")
            
            processed_nodes.add(name)
        
        # Add edges
        processed_edges = set()
        
        for edge in getattr(self.graph, 'edges', []):
            source = edge.source
            target = edge.target
            
            # Handle special node references
            if source in ["START", "__start__", "start"]:
                source = "START"
            if target in ["END", "__end__", "end"]:
                target = "END"
            
            # Create edge key for tracking
            edge_key = (source, target)
            
            # Skip duplicate edges
            if edge_key in processed_edges:
                continue
                
            # Sanitize IDs for Mermaid
            source_id = self._sanitize_id(source)
            target_id = self._sanitize_id(target)
            
            # Determine edge type and formatting
            edge_type = self.edge_types.get(edge_key, "default")
            
            # Add edge with appropriate styling
            if edge_type == "conditional":
                # Include condition name if available
                condition_name = ""
                if hasattr(edge, 'condition') and edge.condition and hasattr(edge.condition, '__name__'):
                    condition_name = f" |{edge.condition.__name__}|"
                
                # Check for condition key in metadata
                if hasattr(edge, 'metadata') and edge.metadata and edge.metadata.get('condition_key'):
                    condition_key = edge.metadata.get('condition_key')
                    mermaid_lines.append(f"  {source_id} -->|{condition_key}| {target_id}")
                else:
                    # Generic conditional edge
                    mermaid_lines.append(f"  {source_id} -.->|cond{condition_name}| {target_id}")
            else:
                # Standard edge with different styles based on type
                if edge_type == "start":
                    mermaid_lines.append(f"  {source_id} ==> {target_id}")
                elif edge_type == "end":
                    mermaid_lines.append(f"  {source_id} ==> {target_id}")
                else:
                    mermaid_lines.append(f"  {source_id} --> {target_id}")
            
            processed_edges.add(edge_key)
        
        # Return the complete Mermaid diagram definition
        return "\n".join(mermaid_lines)
    
    def render_to_file(self, output_file: Optional[str] = None, open_browser: bool = True,
                       include_legend: bool = True, include_stats: bool = True) -> str:
        """
        Render Mermaid diagram to an HTML file with interactive features.
        
        Args:
            output_file: Path to save the HTML file
            open_browser: Whether to open the rendered diagram in browser
            include_legend: Whether to include a legend for node/edge types
            include_stats: Whether to include graph statistics
            
        Returns:
            Path to the generated HTML file
        """
        # Generate Mermaid diagram definition
        mermaid_code = self.generate_mermaid(include_stats=include_stats)
        
        # Set default output file if not provided
        if output_file is None:
            # Generate a default filename with timestamp
            graph_name = getattr(self.graph, 'name', 'graph').replace(' ', '_').lower()
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = f"{graph_name}_mermaid_{timestamp}.html"
        
        # Create HTML template with Mermaid.js and interactive features
        html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{getattr(self.graph, 'name', 'Graph')} Visualization</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/mermaid/10.9.0/mermaid.min.js"></script>
    <style>
        body {{
            font-family: {MermaidStyle.GRAPH_THEME['font_family']};
            margin: 0;
            padding: 20px;
            background-color: #fafafa;
            color: #333;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background-color: white;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            padding: 20px;
            position: relative;
        }}
        h1 {{
            color: {MermaidStyle.GRAPH_THEME['title_color']};
            margin-top: 0;
            border-bottom: 1px solid #eee;
            padding-bottom: 10px;
        }}
        .graph-info {{
            margin-bottom: 20px;
            color: #666;
            font-size: 14px;
        }}
        .legend {{
            margin-top: 30px;
            border-top: 1px solid #eee;
            padding-top: 20px;
        }}
        .legend h3 {{
            color: #555;
            margin-top: 0;
        }}
        .legend-item {{
            display: inline-block;
            margin-right: 15px;
            margin-bottom: 10px;
        }}
        .legend-color {{
            display: inline-block;
            width: 20px;
            height: 20px;
            border-radius: 3px;
            vertical-align: middle;
            margin-right: 5px;
            border: 1px solid #ddd;
        }}
        .controls {{
            position: absolute;
            top: 20px;
            right: 20px;
            z-index: 100;
        }}
        button {{
            background-color: #f5f5f5;
            border: 1px solid #ddd;
            padding: 6px 12px;
            border-radius: 4px;
            cursor: pointer;
            font-size: 14px;
            margin-left: 5px;
        }}
        button:hover {{
            background-color: #e5e5e5;
        }}
        .mermaid {{
            overflow: auto;
            text-align: center;
            min-height: 400px;
        }}
        .timestamp {{
            text-align: right;
            font-size: 12px;
            color: #999;
            margin-top: 20px;
        }}
        .download-link {{
            display: inline-block;
            margin-top: 10px;
            color: #0366d6;
            text-decoration: none;
        }}
        .download-link:hover {{
            text-decoration: underline;
        }}
        .error-message {{
            color: #d32f2f;
            background-color: #ffebee;
            padding: 10px;
            border-radius: 4px;
            margin: 10px 0;
            display: none;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>{getattr(self.graph, 'name', 'Graph')} Visualization</h1>
        
        <div class="graph-info">
            <p><strong>Description:</strong> {getattr(self.graph, 'description', 'Dynamic graph visualization')}</p>
            <p><strong>Nodes:</strong> {len(getattr(self.graph, 'nodes', {}))}</p>
            <p><strong>Edges:</strong> {len(getattr(self.graph, 'edges', []))}</p>
            <p><strong>ID:</strong> {getattr(self.graph, 'id', 'N/A')}</p>
        </div>
        
        <div class="controls">
            <button onclick="zoomIn()">Zoom In</button>
            <button onclick="zoomOut()">Zoom Out</button>
            <button onclick="resetZoom()">Reset</button>
            <button onclick="saveSVG()">Save SVG</button>
            <button onclick="copyMermaidCode()">Copy Code</button>
        </div>
        
        <div class="error-message" id="error-message"></div>
        
        <div class="mermaid" id="mermaid-graph">
{mermaid_code}
        </div>
        
        <a id="download-link" class="download-link" style="display: none;">Download SVG</a>
"""

        # Add legend if requested
        if include_legend:
            node_legend = ""
            for node_type, style in MermaidStyle.NODE_STYLES.items():
                # Skip 'default' type in the legend
                if node_type == 'default':
                    continue
                    
                # Extract fill color from style
                fill_color = "#f9f9f9"  # Default
                if "fill:" in style:
                    fill_color = style.split("fill:")[1].split(",")[0]
                
                # Add icon
                icon = MermaidStyle.NODE_ICONS.get(node_type, "")
                
                # Add to legend
                node_legend += f"""
                <div class="legend-item">
                    <div class="legend-color" style="background-color: {fill_color};"></div>
                    <span>{icon} {node_type.capitalize()}</span>
                </div>"""
            
            # Add edge legend
            edge_legend = ""
            for edge_type, style in MermaidStyle.EDGE_STYLES.items():
                # Extract color and style from the style string
                color = "#666"  # Default
                line_style = "solid"
                
                if "stroke:" in style:
                    color = style.split("stroke:")[1].split(",")[0].split(";")[0]
                if "stroke-dasharray:" in style:
                    line_style = "dashed"
                
                edge_legend += f"""
                <div class="legend-item">
                    <div class="legend-color" style="background-color: {color}; height: 4px; width: 30px; border: none; {'' if line_style == 'solid' else 'border-top: 2px dashed ' + color + ';'}"></div>
                    <span>{edge_type.capitalize()} Edge</span>
                </div>"""
            
            html_template += f"""
        <div class="legend">
            <h3>Legend</h3>
            <div>
                <h4>Node Types</h4>
                {node_legend}
            </div>
            <div>
                <h4>Edge Types</h4>
                {edge_legend}
            </div>
        </div>"""
        
        # Add timestamp and close HTML
        html_template += f"""
        <div class="timestamp">
            Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        </div>
    </div>

    <script>
        // Initialize Mermaid
        mermaid.initialize({{ 
            startOnLoad: true,
            securityLevel: 'loose',
            theme: 'default',
            flowchart: {{
                curve: '{MermaidStyle.GRAPH_THEME["edge_curve"]}',
                diagramPadding: 20
            }},
            logLevel: 'error',
            errorHandler: function(error) {{
                document.getElementById('error-message').style.display = 'block';
                document.getElementById('error-message').textContent = 'Mermaid diagram error: ' + error;
            }}
        }});
        
        // Zoom functionality
        var currentZoom = 1;
        var mermaidGraph = document.getElementById('mermaid-graph');
        
        function zoomIn() {{
            currentZoom += 0.1;
            applyZoom();
        }}
        
        function zoomOut() {{
            currentZoom = Math.max(0.5, currentZoom - 0.1);
            applyZoom();
        }}
        
        function resetZoom() {{
            currentZoom = 1;
            applyZoom();
        }}
        
        function applyZoom() {{
            mermaidGraph.style.transform = `scale(${{currentZoom}})`;
            mermaidGraph.style.transformOrigin = 'center top';
        }}
        
        // Save SVG function
        function saveSVG() {{
            var svgElement = document.querySelector('.mermaid svg');
            if (svgElement) {{
                var svgData = new XMLSerializer().serializeToString(svgElement);
                var blob = new Blob([svgData], {{type: 'image/svg+xml'}});
                var url = URL.createObjectURL(blob);
                
                var downloadLink = document.getElementById('download-link');
                downloadLink.href = url;
                downloadLink.download = '{getattr(self.graph, "name", "graph").replace(" ", "_").lower()}_diagram.svg';
                downloadLink.style.display = 'inline-block';
                downloadLink.textContent = 'Download SVG Diagram';
                downloadLink.click();
            }}
        }}
        
        // Copy Mermaid code
        function copyMermaidCode() {{
            var mermaidCode = `{mermaid_code.replace('`', '\\`')}`;
            navigator.clipboard.writeText(mermaidCode).then(function() {{
                alert('Mermaid code copied to clipboard!');
            }}, function(err) {{
                console.error('Could not copy text: ', err);
            }});
        }}
    </script>
</body>
</html>
"""
        
        # Save HTML to file
        try:
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(os.path.abspath(output_file)) or '.', exist_ok=True)
            
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(html_template)
            
            logger.info(f"Mermaid diagram saved to: {output_file}")
            
            # Open in browser if requested
            if open_browser:
                try:
                    webbrowser.open(f"file://{os.path.abspath(output_file)}")
                except Exception as e:
                    logger.warning(f"Failed to open browser: {str(e)}")
            
            return output_file
            
        except Exception as e:
            logger.error(f"Error saving Mermaid diagram: {str(e)}")
            raise
    
    def render_as_png(self, output_file: Optional[str] = None, open_image: bool = True) -> str:
        """
        Render Mermaid diagram to a PNG file.
        
        This uses the mermaid.ink service to render the diagram.
        
        Args:
            output_file: Path to save the PNG file
            open_image: Whether to open the image after generation
            
        Returns:
            Path to the generated PNG file
        """
        if not REQUESTS_AVAILABLE:
            logger.error("Requests library is required for PNG rendering")
            raise ImportError("Please install requests to use render_as_png")
        
        # Generate Mermaid diagram
        mermaid_code = self.generate_mermaid()
        
        # Set default output file if not provided
        if output_file is None:
            graph_name = getattr(self.graph, 'name', 'graph').replace(' ', '_').lower()
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = f"{graph_name}_diagram_{timestamp}.png"
        
        try:
            # Encode the Mermaid diagram for URL
            encoded_diagram = base64.b64encode(mermaid_code.encode('utf-8')).decode('utf-8')
            
            # Construct the URL for the Mermaid.ink service
            mermaid_url = f"https://mermaid.ink/img/{encoded_diagram}"
            
            # Download the PNG
            response = requests.get(mermaid_url, stream=True)
            response.raise_for_status()
            
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(os.path.abspath(output_file)) or '.', exist_ok=True)
            
            # Save the PNG to file
            with open(output_file, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            logger.info(f"PNG diagram saved to: {output_file}")
            
            # Open the image if requested
            if open_image:
                try:
                    if os.name == 'nt':  # Windows
                        os.system(f'start {output_file}')
                    elif os.name == 'posix':  # macOS or Linux
                        os.system(f'open {output_file}' if os.uname().sysname == 'Darwin' else f'xdg-open {output_file}')
                except Exception as e:
                    logger.warning(f"Failed to open image: {str(e)}")
            
            return output_file
            
        except Exception as e:
            logger.error(f"Error rendering PNG: {str(e)}")
            raise

def visualize_graph(graph, output_file=None, open_browser=True, include_legend=True, 
                   format="html", include_stats=True):
    """
    Visualize a DynamicGraph using Mermaid diagrams.
    
    This function replaces the original visualization function in DynamicGraph
    with an enhanced version that produces beautiful, interactive diagrams.
    
    Args:
        graph: DynamicGraph instance to visualize
        output_file: Optional path to save the visualization
        open_browser: Whether to open the result in browser automatically
        include_legend: Whether to include a legend in the visualization
        format: Output format ('html' or 'png')
        include_stats: Whether to include graph statistics
        
    Returns:
        Path to the generated visualization file
    """
    # Log operation
    logger.info(f"Visualizing graph: {getattr(graph, 'name', 'unnamed')}")
    
    # Create visualizer instance
    visualizer = MermaidVisualizer(graph)
    
    # Generate visualization based on format
    if format.lower() == "png":
        return visualizer.render_as_png(output_file, open_browser)
    else:
        return visualizer.render_to_file(output_file, open_browser, include_legend, include_stats)

# Function that replaces the original visualization method
def replace_visualization_method():
    """
    Replace the original visualization method in DynamicGraph with the enhanced version.
    
    This should be called once to extend DynamicGraph with the new visualization capability.
    
    Returns:
        True if successful, False otherwise
    """
    try:
        # Try to import DynamicGraph
        # This may need adjustment based on your actual import path
        from haive.core.graph.dynamic_graph_builder import DynamicGraph

        # Store original method for fallback
        if hasattr(DynamicGraph, 'visualize_graph'):
            DynamicGraph.visualize_graph_original = DynamicGraph.visualize_graph
        
        # Replace with new method
        def new_visualize_graph(self, output_file=None, open_browser=True, include_legend=True,
                                format="html", include_stats=True):
            """
            Visualize the graph using Mermaid diagrams.
            
            Args:
                output_file: Path to save the visualization (optional)
                open_browser: Whether to open the visualization
                include_legend: Whether to include a legend
                format: Output format ('html' or 'png')
                include_stats: Whether to include graph statistics
                
            Returns:
                Path to the generated file
            """
            return visualize_graph(
                self, output_file, open_browser, include_legend, format, include_stats
            )
        
        # Replace the method
        DynamicGraph.visualize_graph = new_visualize_graph
        
        # Also add a dedicated method for Mermaid visualization
        DynamicGraph.visualize_mermaid = new_visualize_graph
        
        logger.info("Successfully replaced DynamicGraph visualization method")
        return True
    except (ImportError, AttributeError) as e:
        logger.warning(f"Could not replace visualization method: {str(e)}")
        return False

# Sample usage function to demonstrate how to use the visualizer directly
def generate_mermaid_diagram(graph, output_file=None, format="html", open_result=True):
    """
    Helper function to generate a Mermaid diagram from a DynamicGraph.
    
    Args:
        graph: DynamicGraph instance
        output_file: Optional output file path
        format: Output format ('html' or 'png')
        open_result: Whether to open the result automatically
        
    Returns:
        Path to the generated file
    """
    return visualize_graph(
        graph=graph,
        output_file=output_file,
        open_browser=open_result,
        format=format
    )