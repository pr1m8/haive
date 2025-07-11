"""Mermaid diagram generator for the state graph system.

This module provides the MermaidGenerator class for generating
Mermaid flowchart diagrams from graphs.
"""

from typing import Any


class MermaidGenerator:
    """Enhanced Mermaid diagram generator for graphs.

    This class provides advanced Mermaid diagram generation for graphs,
    with improved subgraph handling and customization options.
    """

    # Style configuration
    NODE_COLORS = {
        "ENGINE": "#90EE90",  # Light green
        "TOOL": "#FFD700",  # Gold
        "VALIDATION": "#B0E0E6",  # Light blue
        "SUBGRAPH": "#FFA07A",  # Light salmon
        "CALLABLE": "#F5F5DC",  # Beige
        "CUSTOM": "#DDA0DD",  # Plum
    }
    START_COLOR = "#5D8AA8"  # Blue
    END_COLOR = "#FF6347"  # Tomato red
    DIRECT_EDGE_STYLE = "stroke:#333,stroke-width:2px;"
    BRANCH_EDGE_STYLE = "stroke:#333,stroke-width:1.5px,stroke-dasharray:5 5;"

    @classmethod
    def generate(
        cls,
        graph: Any,
        include_subgraphs: bool = True,
        highlight_nodes: list[str] | None = None,
        highlight_color: str = "#FF69B4",
        theme: str = "default",
        max_depth: int = 2,
        show_node_type: bool = True,
    ) -> str:
        """Generate a Mermaid diagram for a graph.

        Args:
            graph: Graph object to visualize
            include_subgraphs: Whether to visualize subgraphs
            highlight_nodes: List of node names to highlight
            highlight_color: Color to use for highlighted nodes
            theme: Mermaid theme name
            max_depth: Maximum depth for subgraph rendering
            show_node_type: Whether to display node types

        Returns:
            Mermaid diagram code as string
        """
        # Import constants
        from langgraph.graph import END, START

        # Initialize Mermaid code with directives and styling
        lines = [
            f"%%{{ init: {{ 'theme': '{theme}', 'flowchart': {{ 'curve': 'basis' }} }} }}%%",
            "flowchart TD;",
            "    %% Node styling classes",
        ]

        # Define node type classes
        node_type_classes = {}
        for node_type, color in cls.NODE_COLORS.items():
            class_name = f"nodeType{node_type.capitalize()}"
            node_type_classes[node_type] = class_name
            lines.append(
                f"    classDef {class_name} fill:{color},stroke:#333,stroke-width:1px;"
            )

        # Add special node classes
        lines.append(
            f"    classDef startNode fill:{cls.START_COLOR},color:white,font-weight:bold;"
        )
        lines.append(
            f"    classDef endNode fill:{cls.END_COLOR},color:white,font-weight:bold;"
        )
        lines.append(
            f"    classDef highlightNode fill:{highlight_color},stroke:#fff,stroke-width:2px,color:white;"
        )

        # Set for tracking processed node IDs to avoid duplicates
        processed_nodes = set()

        # Helper function to get safe node ID for Mermaid
        def get_safe_node_id(node_name: str) -> str:
            # Replace characters that might cause issues in Mermaid
            safe_id = node_name.replace(" ", "_").replace("-", "_")

            # Check if it starts with a number, prefix with n_ if it does
            if safe_id and safe_id[0].isdigit():
                safe_id = f"n_{safe_id}"

            # Handle reserved Mermaid keywords
            reserved_keywords = [
                "subgraph",
                "end",
                "classDef",
                "class",
                "click",
                "style",
            ]
            if safe_id.lower() in reserved_keywords:
                safe_id = f"node_{safe_id}"

            return safe_id

        # Add subgraphs first if enabled
        if include_subgraphs:
            cls._add_subgraphs_to_diagram(
                graph,
                lines,
                processed_nodes,
                get_safe_node_id,
                node_type_classes,
                max_depth,
                1,
                show_node_type,
            )

        # Add remaining nodes
        lines.append("    %% Nodes")
        cls._add_nodes_to_diagram(
            graph,
            lines,
            processed_nodes,
            get_safe_node_id,
            node_type_classes,
            show_node_type,
        )

        # Add special nodes (START/END)
        start_id = get_safe_node_id("START")
        end_id = get_safe_node_id("END")

        lines.append(f'    {start_id}["{START}"]:::startNode;')
        lines.append(f'    {end_id}["{END}"]:::endNode;')

        # Track processed edges to avoid duplicates
        processed_edges = set()

        # Add direct edges
        lines.append("    %% Direct edges")
        cls._add_edges_to_diagram(
            graph, lines, processed_edges, get_safe_node_id, "START", "END"
        )

        # Add branches
        lines.append("    %% Branch connections")
        cls._add_branches_to_diagram(
            graph, lines, processed_edges, get_safe_node_id, "START", "END"
        )

        # Apply highlights if any
        if highlight_nodes:
            cls._add_highlights_to_diagram(
                lines,
                highlight_nodes,
                processed_nodes,
                get_safe_node_id,
                start_id,
                end_id,
            )

        return "\n".join(lines)

    @classmethod
    def _add_subgraphs_to_diagram(
        cls,
        graph: Any,
        lines: list[str],
        processed_nodes: set[str],
        get_safe_node_id: callable,
        node_type_classes: dict[str, str],
        max_depth: int,
        current_depth: int,
        show_node_type: bool,
    ) -> None:
        """Add subgraphs to the diagram.

        Args:
            graph: Graph object
            lines: List of Mermaid code lines
            processed_nodes: Set of already processed nodes
            get_safe_node_id: Function to get safe node IDs
            node_type_classes: Mapping of node types to CSS classes
            max_depth: Maximum depth for subgraph rendering
            current_depth: Current recursion depth
            show_node_type: Whether to show node types
        """
        from langgraph.graph import END, START

        # Skip if max depth reached
        if current_depth > max_depth:
            return

        # Check for subgraphs
        subgraphs = {}

        # Get subgraphs from either property or registry
        if hasattr(graph, "_subgraph_registry") and hasattr(
            graph._subgraph_registry, "subgraphs"
        ):
            # New style: Use subgraph registry
            subgraphs = graph._subgraph_registry.subgraphs
        elif hasattr(graph, "subgraphs"):
            # Old style: Use subgraphs property
            subgraphs = graph.subgraphs

        # Process each subgraph
        for sg_name, subgraph in subgraphs.items():
            # Create a subgraph cluster with its own ID
            subgraph_id = f"cluster_{get_safe_node_id(sg_name)}"

            lines.append(f"    subgraph {subgraph_id}[{sg_name}]")

            # Get the actual graph from the subgraph if needed
            sg_graph = None
            if hasattr(subgraph, "get_graph"):
                # New style: Use get_graph method
                sg_graph = subgraph.get_graph()
            elif hasattr(subgraph, "graph"):
                # New style: Access graph property
                sg_graph = subgraph.graph
            else:
                # Old style: Subgraph is the graph
                sg_graph = subgraph

            # Get subgraph nodes
            if sg_graph and hasattr(sg_graph, "nodes"):
                # Process nodes in the subgraph
                for sub_node_name, sub_node in sg_graph.nodes.items():
                    if sub_node is None:
                        continue

                    # Skip special nodes
                    if sub_node_name in (START, END):
                        continue

                    safe_id = f"{get_safe_node_id(sub_node_name)}"
                    processed_nodes.add(safe_id)

                    # Get node type
                    node_type = cls._get_node_type(sg_graph, sub_node_name, sub_node)
                    class_name = node_type_classes.get(node_type, "defaultNode")

                    # Add node with class
                    if show_node_type:
                        lines.append(
                            f'        {safe_id}["{sub_node_name} ({node_type})"]:::{class_name};'
                        )
                    else:
                        lines.append(
                            f'        {safe_id}["{sub_node_name}"]:::{class_name};'
                        )

            # Recursively add nested subgraphs
            if sg_graph and current_depth < max_depth:
                cls._add_subgraphs_to_diagram(
                    sg_graph,
                    lines,
                    processed_nodes,
                    get_safe_node_id,
                    node_type_classes,
                    max_depth,
                    current_depth + 1,
                    show_node_type,
                )

            lines.append("    end")

            # Add subgraph style
            lines.append(
                f"    style {subgraph_id} fill:#f0f0f0,stroke:#666,stroke-width:2px,stroke-dasharray:5 5;"
            )

    @classmethod
    def _add_nodes_to_diagram(
        cls,
        graph: Any,
        lines: list[str],
        processed_nodes: set[str],
        get_safe_node_id: callable,
        node_type_classes: dict[str, str],
        show_node_type: bool,
    ) -> None:
        """Add regular nodes to the diagram.

        Args:
            graph: Graph object
            lines: List of Mermaid code lines
            processed_nodes: Set of already processed nodes
            get_safe_node_id: Function to get safe node IDs
            node_type_classes: Mapping of node types to CSS classes
            show_node_type: Whether to show node types
        """
        from langgraph.graph import END, START

        # Add nodes
        if hasattr(graph, "nodes"):
            for name, node in graph.nodes.items():
                # Skip None nodes and already processed nodes
                if node is None or get_safe_node_id(name) in processed_nodes:
                    continue

                # Skip special nodes
                if name in (START, END):
                    continue

                safe_id = get_safe_node_id(name)

                # Get node type
                node_type = cls._get_node_type(graph, name, node)
                class_name = node_type_classes.get(node_type, "defaultNode")

                # Add node with class
                if show_node_type:
                    lines.append(
                        f'    {safe_id}["{name} ({node_type})"]:::{class_name};'
                    )
                else:
                    lines.append(f'    {safe_id}["{name}"]:::{class_name};')

                processed_nodes.add(safe_id)

    @classmethod
    def _add_edges_to_diagram(
        cls,
        graph: Any,
        lines: list[str],
        processed_edges: set[str],
        get_safe_node_id: callable,
        START: str,
        END: str,
    ) -> None:
        """Add edges to the diagram.

        Args:
            graph: Graph object
            lines: List of Mermaid code lines
            processed_edges: Set of already processed edges
            get_safe_node_id: Function to get safe node IDs
            START: START node name
            END: END node name
        """
        # Add direct edges if present
        if hasattr(graph, "edges"):
            for source, target in graph.edges:
                source_id = get_safe_node_id(source)
                target_id = get_safe_node_id(target)

                edge_key = f"{source_id}->{target_id}"
                if edge_key in processed_edges:
                    continue

                lines.append(f"    {source_id} --> {target_id};")
                processed_edges.add(edge_key)

    @classmethod
    def _add_branches_to_diagram(
        cls,
        graph: Any,
        lines: list[str],
        processed_edges: set[str],
        get_safe_node_id: callable,
        START: str,
        END: str,
    ) -> None:
        """Add branches to the diagram.

        Args:
            graph: Graph object
            lines: List of Mermaid code lines
            processed_edges: Set of already processed edges
            get_safe_node_id: Function to get safe node IDs
            START: START node name
            END: END node name
        """
        # Add branches if present
        if hasattr(graph, "branches") and graph.branches:
            for _branch_id, branch in graph.branches.items():
                source = branch.source_node
                source_id = get_safe_node_id(source)

                # Add branch mode comment
                if hasattr(branch, "mode"):
                    lines.append(f"    %% {branch.mode} Branch: {branch.name}")
                else:
                    lines.append(f"    %% Branch: {branch.name}")

                # Draw connections for destinations with dotted lines
                for condition, target in branch.destinations.items():
                    target_id = get_safe_node_id(target)

                    edge_key = f"{source_id}-->{target_id}"
                    if edge_key in processed_edges:
                        continue

                    # Format condition string
                    condition_str = str(condition)
                    if len(condition_str) > 15:
                        condition_str = condition_str[:12] + "..."

                    # Add branch edge with dash style
                    lines.append(
                        f'    {source_id} -.->|"{condition_str}"| {target_id};'
                    )
                    processed_edges.add(edge_key)

                # Draw default connection if different from destinations
                if hasattr(branch, "default") and branch.default:
                    target_id = get_safe_node_id(branch.default)

                    # Skip if this is already connected by a specific condition
                    is_duplicate = False
                    for dest in branch.destinations.values():
                        if dest == branch.default:
                            is_duplicate = True
                            break

                    if not is_duplicate:
                        edge_key = f"{source_id}-->{target_id}"
                        if edge_key not in processed_edges:
                            lines.append(
                                f'    {source_id} -.->|"default"| {target_id};'
                            )
                            processed_edges.add(edge_key)

    @classmethod
    def _add_highlights_to_diagram(
        cls,
        lines: list[str],
        highlight_nodes: list[str],
        processed_nodes: set[str],
        get_safe_node_id: callable,
        start_id: str,
        end_id: str,
    ) -> None:
        """Add highlights to the diagram.

        Args:
            lines: List of Mermaid code lines
            highlight_nodes: List of nodes to highlight
            processed_nodes: Set of already processed nodes
            get_safe_node_id: Function to get safe node IDs
            start_id: ID of the START node
            end_id: ID of the END node
        """
        # Apply highlights if any
        highlight_list = []
        for node in highlight_nodes:
            safe_id = get_safe_node_id(node)
            if safe_id in processed_nodes or safe_id in [start_id, end_id]:
                highlight_list.append(safe_id)

        if highlight_list:
            lines.append("    %% Highlight specified nodes")
            lines.append(f"    class {','.join(highlight_list)} highlightNode;")

    @classmethod
    def _get_node_type(cls, graph: Any, node_name: str, node: Any) -> str:
        """Get the node type as a string.

        Args:
            graph: Graph containing the node
            node_name: Name of the node
            node: Node object

        Returns:
            Node type as string
        """
        # Check if graph has node_types dictionary
        if hasattr(graph, "node_types") and node_name in graph.node_types:
            node_type = graph.node_types[node_name]
            # Convert to string if it's an enum
            return node_type.value if hasattr(node_type, "value") else str(node_type)

        # Check if node has a node_type attribute
        if hasattr(node, "node_type"):
            node_type = node.node_type
            # Convert to string if it's an enum
            return node_type.value if hasattr(node_type, "value") else str(node_type)

        # Default to CALLABLE
        return "CALLABLE"
