"""
Enhanced graph visualization utilities for Haive graphs with automatic Agent detection and expansion.

This module provides comprehensive visualization that automatically detects nodes with Agent engines
or nodes that are Agents themselves, expanding them to show their complete internal graph structure.
"""

import logging
import os
import uuid
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, NamedTuple, Optional, Set, Tuple, Union

from langgraph.graph import END, START

from haive.core.graph.common.types import NodeType
from haive.core.utils.mermaid_utils import (
    Environment,
    detect_environment,
    display_mermaid,
    mermaid_to_png,
)

# Set up module logger
logger = logging.getLogger(__name__)


# Supporting data classes
@dataclass
class AgentInfo:
    """Information about a detected agent node."""

    node: Any
    graph: Any
    depth: int
    parent_path: List[str]
    reason: str


@dataclass
class VisualizationContext:
    """Context object for tracking visualization state."""

    processed_nodes: Set[str]
    processed_edges: Set[str]
    agent_graphs: Dict[str, AgentInfo]
    node_mappings: Dict[str, str]
    highlight_nodes: Set[str]
    debug: bool = False


class NodeStyle(Enum):
    """Standardized node styles for consistent visualization."""

    # Primary node types
    ENGINE = "engineNode"
    TOOL = "toolNode"
    VALIDATION = "validationNode"
    PARSER = "parserNode"
    AGENT = "agentNode"
    CALLABLE = "callableNode"

    # Special nodes
    START = "startNode"
    END = "endNode"
    ENTRY = "entryNode"
    EXIT = "exitNode"

    # States
    HIGHLIGHT = "highlightNode"
    ERROR = "errorNode"
    SUCCESS = "successNode"


class GraphVisualizer:
    """
    Enhanced visualization utilities with automatic Agent detection and expansion.

    Key features:
    - Detects nodes that are Agents or contain Agent engines
    - Recursively expands Agent graphs showing internal structure
    - Consistent styling with professional color scheme
    - Smart edge routing between parent and subgraphs
    - Handles nested agents and complex hierarchies
    """

    # Professional, accessible color palette
    STYLE_DEFINITIONS = {
        # Primary node types - using consistent, professional colors
        NodeStyle.ENGINE: {
            "fill": "#3B82F6",  # Blue
            "stroke": "#1E40AF",
            "color": "#FFFFFF",
            "strokeWidth": "2px",
        },
        NodeStyle.TOOL: {
            "fill": "#EF4444",  # Red
            "stroke": "#991B1B",
            "color": "#FFFFFF",
            "strokeWidth": "2px",
        },
        NodeStyle.VALIDATION: {
            "fill": "#10B981",  # Green
            "stroke": "#047857",
            "color": "#FFFFFF",
            "strokeWidth": "2px",
        },
        NodeStyle.PARSER: {
            "fill": "#F59E0B",  # Amber
            "stroke": "#D97706",
            "color": "#FFFFFF",
            "strokeWidth": "2px",
        },
        NodeStyle.AGENT: {
            "fill": "#8B5CF6",  # Purple
            "stroke": "#6D28D9",
            "color": "#FFFFFF",
            "strokeWidth": "3px",
            "fontWeight": "bold",
        },
        NodeStyle.CALLABLE: {
            "fill": "#6B7280",  # Gray
            "stroke": "#374151",
            "color": "#FFFFFF",
            "strokeWidth": "2px",
        },
        # Special nodes - consistent start/end styling
        NodeStyle.START: {
            "fill": "#059669",  # Emerald green
            "stroke": "#047857",
            "color": "#FFFFFF",
            "strokeWidth": "3px",
            "fontWeight": "bold",
        },
        NodeStyle.END: {
            "fill": "#DC2626",  # Bright red
            "stroke": "#991B1B",
            "color": "#FFFFFF",
            "strokeWidth": "3px",
            "fontWeight": "bold",
        },
        NodeStyle.ENTRY: {
            "fill": "transparent",  # Invisible by default
            "stroke": "transparent",
            "color": "#FFFFFF",
            "strokeWidth": "0px",
        },
        NodeStyle.EXIT: {
            "fill": "transparent",  # Invisible by default
            "stroke": "transparent",
            "color": "#FFFFFF",
            "strokeWidth": "0px",
        },
        # States
        NodeStyle.HIGHLIGHT: {
            "fill": "#FBBF24",  # Yellow
            "stroke": "#F59E0B",
            "color": "#000000",
            "strokeWidth": "4px",
            "fontWeight": "bold",
        },
        NodeStyle.ERROR: {
            "fill": "#FCA5A5",
            "stroke": "#DC2626",
            "color": "#000000",
            "strokeWidth": "3px",
        },
        NodeStyle.SUCCESS: {
            "fill": "#86EFAC",
            "stroke": "#10B981",
            "color": "#000000",
            "strokeWidth": "3px",
        },
    }

    # Subgraph styling
    SUBGRAPH_STYLES = {
        "agent": {
            "fill": "#F3E8FF",  # Light purple background for agents
            "stroke": "#8B5CF6",  # Purple border
            "strokeWidth": "3px",
            "rx": "10",  # Rounded corners
            "ry": "10",
        },
        "react": {
            "fill": "#EBF8FF",  # Light blue for React agents
            "stroke": "#3182CE",  # Blue border
            "strokeWidth": "3px",
            "rx": "10",  # Rounded corners
            "ry": "10",
        },
        "default": {
            "fill": "#F9FAFB",  # Light gray
            "stroke": "#6B7280",
            "strokeWidth": "2px",
            "rx": "5",
            "ry": "5",
        },
    }

    @classmethod
    def generate_mermaid(
        cls,
        graph: Any,
        include_subgraphs: bool = True,
        highlight_nodes: Optional[List[str]] = None,
        theme: str = "base",
        show_branch_labels: bool = True,
        direction: str = "TB",
        compact: bool = False,
        max_depth: int = 3,
        debug: bool = False,
    ) -> str:
        """
        Generate a comprehensive Mermaid diagram with automatic Agent expansion.

        Args:
            graph: The graph to visualize
            include_subgraphs: Whether to expand Agent nodes
            highlight_nodes: Nodes to highlight
            theme: Mermaid theme
            show_branch_labels: Whether to show labels on conditional branches
            direction: Graph direction (TB, LR, etc.)
            compact: Use compact layout
            max_depth: Maximum depth for nested agent expansion
            debug: Enable debug output

        Returns:
            Complete Mermaid diagram string
        """
        logger.info(
            f"Generating Mermaid for graph: {getattr(graph, 'name', 'Unnamed')}"
        )

        # Initialize diagram
        lines = cls._initialize_diagram(theme, direction, compact)

        # Add style definitions
        cls._add_style_definitions(lines)

        # Initialize tracking
        context = VisualizationContext(
            processed_nodes=set(),
            processed_edges=set(),
            agent_graphs={},
            node_mappings={},
            highlight_nodes=set(highlight_nodes or []),
            debug=debug,
        )

        # Detect all agent nodes if subgraphs enabled
        if include_subgraphs:
            context.agent_graphs = cls._detect_all_agents(graph, max_depth, debug)

        # Build the graph recursively
        cls._build_graph(lines, graph, context, depth=0, parent_prefix="")

        # Add any global highlights
        if context.highlight_nodes:
            cls._add_highlights(lines, context)

        return "\n".join(lines)

    @classmethod
    def _initialize_diagram(
        cls, theme: str, direction: str, compact: bool
    ) -> List[str]:
        """Initialize the Mermaid diagram with settings."""
        spacing = "30" if compact else "50"
        padding = "10" if compact else "15"

        return [
            f"%%{{ init: {{ "
            f'"theme": "{theme}", '
            f'"flowchart": {{ '
            f'"curve": "basis", '
            f'"padding": {padding}, '
            f'"nodeSpacing": {spacing}, '
            f'"rankSpacing": {int(spacing) * 1.6}, '
            f'"htmlLabels": true '
            f"}} }} }}%%",
            f"flowchart {direction}",
            "",
        ]

    @classmethod
    def _add_style_definitions(cls, lines: List[str]):
        """Add comprehensive style definitions."""
        lines.append("    %% ===== STYLE DEFINITIONS =====")

        for style, config in cls.STYLE_DEFINITIONS.items():
            class_name = style.value
            style_parts = []

            # Build style string
            for prop, value in config.items():
                if prop == "fill":
                    style_parts.append(f"fill:{value}")
                elif prop == "stroke":
                    style_parts.append(f"stroke:{value}")
                elif prop == "color":
                    style_parts.append(f"color:{value}")
                elif prop == "strokeWidth":
                    style_parts.append(f"stroke-width:{value}")
                elif prop == "fontWeight":
                    style_parts.append(f"font-weight:{value}")

            # Add font family for consistency
            style_parts.append("font-family:system-ui,-apple-system,sans-serif")

            lines.append(f"    classDef {class_name} {','.join(style_parts)}")

        lines.append("")

    @classmethod
    def _detect_all_agents(
        cls, graph: Any, max_depth: int, debug: bool, current_depth: int = 0
    ) -> Dict[str, AgentInfo]:
        """
        Recursively detect all agent nodes in the graph and nested subgraphs.

        Returns:
            Dict mapping node_id -> AgentInfo(node, graph, depth, parent_path)
        """
        agents = {}

        if current_depth >= max_depth:
            logger.warning(f"Max depth {max_depth} reached, stopping agent detection")
            return agents

        if not hasattr(graph, "nodes"):
            return agents

        logger.info(
            f"Detecting agents at depth {current_depth} in {getattr(graph, 'name', 'Unknown')}"
        )

        for node_name, node in (graph.nodes or {}).items():
            if node is None or node_name in (START, END):
                continue

            agent_info = cls._check_if_agent(node, node_name, debug)

            if agent_info:
                node_id = f"depth{current_depth}_{node_name}"
                agents[node_id] = AgentInfo(
                    node=node,
                    graph=agent_info["graph"],
                    depth=current_depth,
                    parent_path=[node_name],
                    reason=agent_info["reason"],
                )

                # Recursively check the agent's graph
                if agent_info["graph"]:
                    nested_agents = cls._detect_all_agents(
                        agent_info["graph"], max_depth, debug, current_depth + 1
                    )

                    # Add nested agents with updated paths
                    for nested_id, nested_info in nested_agents.items():
                        full_path = [node_name] + nested_info.parent_path
                        agents[f"{node_name}_{nested_id}"] = AgentInfo(
                            node=nested_info.node,
                            graph=nested_info.graph,
                            depth=nested_info.depth,
                            parent_path=full_path,
                            reason=nested_info.reason,
                        )

        logger.info(f"Found {len(agents)} agents at depth {current_depth}")
        return agents

    @classmethod
    def _check_if_agent(
        cls, node: Any, node_name: str, debug: bool
    ) -> Optional[Dict[str, Any]]:
        """
        Comprehensive check if a node is an agent with detailed detection logic.

        Returns:
            Dict with 'graph' and 'reason' if agent, None otherwise
        """
        if debug:
            logger.debug(f"Checking if '{node_name}' is an agent...")

        # Method 1: Direct Agent class check
        if cls._is_agent_class(node):
            graph = cls._get_graph_from_object(node, debug)
            if graph:
                return {"graph": graph, "reason": "direct_agent_class"}

        # Method 2: EngineNodeConfig with Agent engine
        if hasattr(node, "__class__") and "EngineNodeConfig" in node.__class__.__name__:
            if hasattr(node, "engine") and node.engine:
                engine = node.engine

                # Check engine type
                engine_type = cls._get_engine_type(engine)
                if engine_type == "agent":
                    graph = cls._get_graph_from_object(engine, debug)
                    if graph:
                        return {"graph": graph, "reason": "engine_type_agent"}

                # Check if engine is Agent class
                if cls._is_agent_class(engine):
                    graph = cls._get_graph_from_object(engine, debug)
                    if graph:
                        return {"graph": graph, "reason": "engine_is_agent_class"}

        # Method 3: Any object with a graph attribute
        if hasattr(node, "graph") and node.graph:
            return {"graph": node.graph, "reason": "has_graph_attribute"}

        # Method 4: Check for agent-like attributes
        agent_attributes = ["build_graph", "setup_workflow", "compile", "invoke"]
        matching_attrs = [attr for attr in agent_attributes if hasattr(node, attr)]

        if len(matching_attrs) >= 2:  # Has multiple agent-like attributes
            graph = cls._get_graph_from_object(node, debug)
            if graph:
                return {
                    "graph": graph,
                    "reason": f'agent_attributes:{",".join(matching_attrs)}',
                }

        return None

    @classmethod
    def _is_agent_class(cls, obj: Any) -> bool:
        """Check if object is an Agent class or instance."""
        if obj is None:
            return False

        # Check class name
        class_name = type(obj).__name__
        if "Agent" in class_name:
            return True

        # Check MRO
        for base in type(obj).__mro__:
            if base.__name__ == "Agent":
                return True

        return False

    @classmethod
    def _get_engine_type(cls, engine: Any) -> Optional[str]:
        """Extract engine type from an engine object."""
        if hasattr(engine, "engine_type"):
            engine_type = engine.engine_type

            # Handle enum
            if hasattr(engine_type, "value"):
                return engine_type.value
            else:
                return str(engine_type)

        return None

    @classmethod
    def _get_graph_from_object(cls, obj: Any, debug: bool) -> Optional[Any]:
        """Try to get a graph from an object using various methods."""
        # Direct graph attribute
        if hasattr(obj, "graph") and obj.graph:
            if debug:
                logger.debug(f"Got graph from {type(obj).__name__}.graph")
            return obj.graph

        # Try to build graph
        if hasattr(obj, "build_graph"):
            try:
                if debug:
                    logger.debug(
                        f"Attempting to build graph from {type(obj).__name__}.build_graph()"
                    )
                graph = obj.build_graph()
                if graph:
                    return graph
            except Exception as e:
                logger.warning(f"Failed to build graph: {e}")

        # Try to get compiled graph
        if hasattr(obj, "compile"):
            try:
                if debug:
                    logger.debug(
                        f"Attempting to compile graph from {type(obj).__name__}.compile()"
                    )
                compiled = obj.compile()
                if hasattr(compiled, "graph"):
                    return compiled.graph
            except Exception as e:
                logger.warning(f"Failed to compile graph: {e}")

        return None

    @classmethod
    def _build_graph(
        cls,
        lines: List[str],
        graph: Any,
        context: VisualizationContext,
        depth: int = 0,
        parent_prefix: str = "",
        subgraph_id: Optional[str] = None,
    ):
        """Recursively build the graph with proper node and edge handling."""
        indent = "    " * (depth + 1)

        # Add section comment
        graph_name = getattr(graph, "name", "Unnamed Graph")
        if depth == 0:
            lines.append(f"{indent}%% ===== MAIN GRAPH: {graph_name} =====")
        else:
            lines.append(
                f"{indent}%% ===== SUBGRAPH: {graph_name} (depth={depth}) ====="
            )

        # Process nodes
        if hasattr(graph, "nodes"):
            cls._process_nodes(lines, graph, context, depth, parent_prefix, subgraph_id)

        # Process edges
        if hasattr(graph, "edges"):
            cls._process_edges(lines, graph, context, depth, parent_prefix)

        # Process branches
        if hasattr(graph, "branches"):
            cls._process_branches(lines, graph, context, depth, parent_prefix)

        # If this is a top-level graph with agent subgraphs, add connection edges
        if depth == 0 and hasattr(graph, "nodes") and context.agent_graphs:
            # Add connections for agents in the main graph
            cls._add_agent_connections(lines, graph, context)

    @classmethod
    def _process_nodes(
        cls,
        lines: List[str],
        graph: Any,
        context: VisualizationContext,
        depth: int,
        parent_prefix: str,
        subgraph_id: Optional[str],
    ):
        """Process all nodes in a graph."""
        indent = "    " * (depth + 1)

        # Add START and END nodes for main graph or subgraphs
        if depth == 0 or subgraph_id:
            start_id = f"{parent_prefix}START" if parent_prefix else "START"
            end_id = f"{parent_prefix}END" if parent_prefix else "END"

            # Only add START/END nodes if they don't exist yet
            # This prevents duplicate START/END nodes in subgraphs
            if start_id not in context.processed_nodes:
                # Use consistent shapes for START/END
                lines.append(
                    f'{indent}{start_id}(["▶ START"]):::{NodeStyle.START.value}'
                )
                context.processed_nodes.add(start_id)
                context.node_mappings[f"{parent_prefix}START"] = start_id

            if end_id not in context.processed_nodes:
                lines.append(f'{indent}{end_id}(["■ END"]):::{NodeStyle.END.value}')
                context.processed_nodes.add(end_id)
                context.node_mappings[f"{parent_prefix}END"] = end_id

        for node_name, node in (graph.nodes or {}).items():
            if node_name in (START, END, "__start__", "__end__"):
                continue

            node_id = f"{parent_prefix}{cls._get_safe_node_id(node_name)}"

            # Check if this is an agent node to expand
            agent_key = cls._find_agent_key(
                node_name, parent_prefix, context.agent_graphs
            )

            # Special handling for subgraph nodes to avoid duplication
            if parent_prefix == "" and depth == 0:
                # For top-level nodes that will be represented as subgraphs,
                # track their names so we can properly handle connections
                subgraph_id = f"subgraph_{node_name}"
                context.node_mappings[f"main_subgraph_{node_name}"] = subgraph_id

                # Track the next node in the process after this subgraph
                # by examining the edges in the graph
                if hasattr(graph, "edges"):
                    for src, dst in graph.edges:
                        if src == node_name:
                            context.node_mappings["next_after_subgraph"] = dst

            if agent_key and agent_key in context.agent_graphs:
                # This is an agent - create a subgraph
                agent_info = context.agent_graphs[agent_key]
                cls._create_agent_subgraph(
                    lines, node_name, node_id, agent_info, context, depth, parent_prefix
                )
            else:
                # Regular node
                cls._add_regular_node(
                    lines, node_name, node_id, node, graph, context, depth
                )

    @classmethod
    def _add_regular_node(
        cls,
        lines: List[str],
        node_name: str,
        node_id: str,
        node: Any,
        graph: Any,
        context: VisualizationContext,
        depth: int,
    ):
        """Add a regular (non-agent) node."""
        indent = "    " * (depth + 1)

        # Get node style
        style = cls._determine_node_style(node, graph, node_name)

        # Get node label
        label = cls._create_node_label(node_name, node)

        # Determine shape based on style
        if style == NodeStyle.START or style == NodeStyle.END:
            shape_start, shape_end = '(["', '"])'
        elif style == NodeStyle.TOOL:
            shape_start, shape_end = '[["', '"]]'  # Stadium shape for tools
        elif style == NodeStyle.VALIDATION:
            shape_start, shape_end = '{"', '"}'  # Diamond for validation
        elif style == NodeStyle.AGENT:
            shape_start, shape_end = '(("', '"))'  # Circle for agents
        else:
            shape_start, shape_end = '["', '"]'  # Default rectangle

        # Add highlight if needed
        if node_name in context.highlight_nodes:
            style = NodeStyle.HIGHLIGHT

        lines.append(
            f"{indent}{node_id}{shape_start}{label}{shape_end}:::{style.value}"
        )

        context.processed_nodes.add(node_id)
        context.node_mappings[f"{node_id}_base"] = node_id

    @classmethod
    def _create_agent_subgraph(
        cls,
        lines: List[str],
        node_name: str,
        node_id: str,
        agent_info: AgentInfo,
        context: VisualizationContext,
        depth: int,
        parent_prefix: str,
    ):
        """Create an expanded agent subgraph."""
        indent = "    " * (depth + 1)
        subgraph_id = f"subgraph_{node_id}"

        # Create subgraph
        lines.append("")
        lines.append(
            f'{indent}subgraph {subgraph_id}["🤖 {cls._sanitize_label(node_name)} Agent"]'
        )
        lines.append(f"{indent}    direction TB")

        # Create START/END nodes directly in the subgraph with improved positioning
        start_id = f"{node_id}_START"
        end_id = f"{node_id}_END"

        # Check if these START/END nodes already exist to avoid duplication
        if start_id not in context.processed_nodes:
            # Add START at the top of the subgraph
            lines.append(
                f'{indent}    {start_id}(["▶ START"]):::{NodeStyle.START.value}'
            )
            context.processed_nodes.add(start_id)

        if end_id not in context.processed_nodes:
            # Add END at the bottom (will be rendered later after other nodes)
            lines.append(f'{indent}    {end_id}(["■ END"]):::{NodeStyle.END.value}')
            context.processed_nodes.add(end_id)

        # Map START/END nodes for proper edge connections
        context.node_mappings[f"{node_id}_START"] = start_id
        context.node_mappings[f"{node_id}_END"] = end_id

        # Use actual node IDs for entry/exit mappings
        context.node_mappings[f"{node_id}_entry"] = start_id
        context.node_mappings[f"{node_id}_exit"] = end_id

        # Recursively build the agent's internal graph
        if agent_info.graph:
            # Map internal START/END to our explicit subgraph START/END
            internal_prefix = f"{node_id}_"
            context.node_mappings[f"{internal_prefix}START"] = start_id
            context.node_mappings[f"{internal_prefix}END"] = end_id

            cls._build_graph(
                lines,
                agent_info.graph,
                context,
                depth + 1,
                internal_prefix,
                subgraph_id,
            )

        lines.append(f"{indent}end")

        # Style the subgraph
        style = cls.SUBGRAPH_STYLES["agent"]
        style_str = f"fill:{style['fill']},stroke:{style['stroke']},stroke-width:{style['strokeWidth']}"
        lines.append(f"{indent}style {subgraph_id} {style_str}")

        # Mark the original node as processed
        context.processed_nodes.add(node_id)

    @classmethod
    def _process_edges(
        cls,
        lines: List[str],
        graph: Any,
        context: VisualizationContext,
        depth: int,
        parent_prefix: str,
    ):
        """Process all edges in a graph."""
        indent = "    " * (depth + 1)

        if not hasattr(graph, "edges"):
            return

        lines.append(f"{indent}%% --- Edges ---")

        for source, target in graph.edges or []:
            # Handle edges for better flow
            source_id = cls._resolve_node_id(source, parent_prefix, context)
            target_id = cls._resolve_node_id(target, parent_prefix, context)

            if source_id and target_id:
                edge_key = f"{source_id}->{target_id}"

                # Skip self-loops
                if source_id == target_id:
                    continue

                # Skip duplicates and self-references
                if edge_key not in context.processed_edges and source_id != target_id:
                    # Skip any main graph edges with "react" as these will be handled specially
                    # with proper connections to subgraphs
                    if not (source_id == "START" and target_id == "react") and not (
                        source_id == "react" and target_id == "agent_node"
                    ):
                        # Add the edge with the right formatting
                        lines.append(f"{indent}{source_id} --> {target_id}")
                        context.processed_edges.add(edge_key)

    @classmethod
    def _process_branches(
        cls,
        lines: List[str],
        graph: Any,
        context: VisualizationContext,
        depth: int,
        parent_prefix: str,
    ):
        """Process all conditional branches in a graph."""
        indent = "    " * (depth + 1)

        if not hasattr(graph, "branches") or not graph.branches:
            return

        lines.append(f"{indent}%% --- Conditional Branches ---")

        for branch_id, branch in (graph.branches or {}).items():
            source = getattr(branch, "source_node", None)
            if not source:
                continue

            source_id = cls._resolve_node_id(source, parent_prefix, context)
            if not source_id:
                continue

            # Get destinations
            destinations = cls._get_branch_destinations(branch)

            for condition, target in destinations.items():
                target_id = cls._resolve_node_id(target, parent_prefix, context)
                if not target_id:
                    continue

                # Format condition label
                label = cls._format_condition_label(condition)

                # Create dotted edge for conditional
                edge_key = f"{source_id}-.{condition}.->{target_id}"
                if edge_key not in context.processed_edges:
                    lines.append(f'{indent}{source_id} -.->|"{label}"| {target_id}')
                    context.processed_edges.add(edge_key)

    @classmethod
    def _resolve_node_id(
        cls, node_name: str, parent_prefix: str, context: VisualizationContext
    ) -> Optional[str]:
        """Resolve a node name to its actual ID in the graph."""
        # Handle START/END nodes and their variants
        if node_name in (START, "__start__", "START"):
            key = f"{parent_prefix}START"
            return context.node_mappings.get(key, "START")
        elif node_name in (END, "__end__", "END"):
            key = f"{parent_prefix}END"
            return context.node_mappings.get(key, "END")

        # Special handling for agent/subgraph nodes
        # In the main diagram, we should try to use the subgraph box when connecting
        # to a node that's represented as a subgraph
        if parent_prefix == "":
            # Check if this node has a subgraph representation
            subgraph_id = f"subgraph_{node_name}"
            if subgraph_id in context.processed_nodes:
                # For incoming connections to a subgraph, use the subgraph ID
                return subgraph_id

        # Get the node ID with parent prefix
        node_id = f"{parent_prefix}{cls._get_safe_node_id(node_name)}"

        # Regular node in current scope
        if node_id in context.processed_nodes:
            return node_id

        # Simple node lookup by name
        safe_id = cls._get_safe_node_id(node_name)
        if safe_id in context.processed_nodes:
            return safe_id

        logger.warning(f"Could not resolve node: {node_name} (prefix={parent_prefix})")
        return None

    @classmethod
    def _find_agent_key(
        cls, node_name: str, parent_prefix: str, agent_graphs: Dict[str, AgentInfo]
    ) -> Optional[str]:
        """Find the agent key for a given node."""
        # Try exact match with prefix
        for key in agent_graphs:
            if key.endswith(f"_{node_name}") or key == f"depth0_{node_name}":
                return key

        return None

    @classmethod
    def _determine_node_style(cls, node: Any, graph: Any, node_name: str) -> NodeStyle:
        """Determine the appropriate style for a node."""
        # Check node_types mapping first
        if hasattr(graph, "node_types") and node_name in graph.node_types:
            node_type = graph.node_types[node_name]
            if hasattr(node_type, "value"):
                type_str = node_type.value.upper()
                if hasattr(NodeStyle, type_str):
                    return NodeStyle[type_str]

        # Check node.node_type
        if hasattr(node, "node_type"):
            if hasattr(node.node_type, "value"):
                type_str = node.node_type.value.upper()
                if hasattr(NodeStyle, type_str):
                    return NodeStyle[type_str]

        # Pattern matching on class name
        if node is not None:
            class_name = type(node).__name__.lower()
            if "tool" in class_name:
                return NodeStyle.TOOL
            elif "validation" in class_name or "validator" in class_name:
                return NodeStyle.VALIDATION
            elif "parser" in class_name or "parse" in class_name:
                return NodeStyle.PARSER
            elif "agent" in class_name:
                return NodeStyle.AGENT
            elif "engine" in class_name:
                return NodeStyle.ENGINE

        # Pattern matching on node name
        node_name_lower = node_name.lower()
        if "tool" in node_name_lower:
            return NodeStyle.TOOL
        elif "validat" in node_name_lower:
            return NodeStyle.VALIDATION
        elif "parse" in node_name_lower:
            return NodeStyle.PARSER
        elif "agent" in node_name_lower:
            return NodeStyle.AGENT

        # Default
        return NodeStyle.CALLABLE

    @classmethod
    def _create_node_label(cls, node_name: str, node: Any) -> str:
        """Create a clean, readable label for a node."""
        # Get base label
        label = cls._sanitize_label(node_name)

        # Add icon based on node type
        if node is not None:
            class_name = type(node).__name__.lower()
            if "tool" in class_name or "tool" in node_name.lower():
                label = f"🔧 {label}"
            elif "validation" in class_name or "validat" in node_name.lower():
                label = f"✓ {label}"
            elif "parser" in class_name or "parse" in node_name.lower():
                label = f"📝 {label}"
            elif "agent" in class_name or "agent" in node_name.lower():
                label = f"🤖 {label}"
            elif "engine" in class_name:
                label = f"⚙️ {label}"

        return label

    @classmethod
    def _sanitize_label(cls, text: str) -> str:
        """Create a clean, readable label from text."""
        # Handle special cases
        if text.upper() in ("START", "__START__"):
            return "START"
        if text.upper() in ("END", "__END__"):
            return "END"

        # Clean up underscores and common suffixes
        label = text.replace("_", " ").strip()

        # Remove common suffixes
        for suffix in ["node", "Node", "_node"]:
            if label.endswith(suffix):
                label = label[: -len(suffix)].strip()

        # Title case
        label = " ".join(word.capitalize() for word in label.split())

        # Common replacements
        replacements = {
            "Agent Node": "Agent",
            "Tool Node": "Tools",
            "Parse Output": "Parser",
            "Validation Node": "Validator",
        }

        for old, new in replacements.items():
            label = label.replace(old, new)

        return label

    @classmethod
    def _get_safe_node_id(cls, node_name: str) -> str:
        """Convert node name to safe Mermaid ID."""
        # Special handling
        if node_name.upper() in ("START", "__START__"):
            return "START"
        if node_name.upper() in ("END", "__END__"):
            return "END"

        # Remove problematic characters
        safe_id = node_name
        for char in " -./\\:()[]{}@#$%^&*+=|<>?~`\"',;!":
            safe_id = safe_id.replace(char, "_")

        # Ensure valid identifier
        if safe_id and safe_id[0].isdigit():
            safe_id = f"node_{safe_id}"

        # Handle reserved words
        reserved = {"end", "subgraph", "class", "classDef", "click", "style"}
        if safe_id.lower() in reserved:
            safe_id = f"node_{safe_id}"

        return safe_id

    @classmethod
    def _get_branch_destinations(cls, branch: Any) -> Dict[str, str]:
        """Extract destinations from a branch object."""
        for attr in ["destinations", "condition_map", "routes", "ends"]:
            if hasattr(branch, attr):
                dest = getattr(branch, attr)
                if isinstance(dest, dict):
                    return dest
        return {}

    @classmethod
    def _format_condition_label(cls, condition: Any) -> str:
        """Format a condition into a readable label."""
        condition_str = str(condition).lower()

        # Enhanced condition mapping
        label_map = {
            # Boolean
            "true": "✓ Yes",
            "false": "✗ No",
            # Validation
            "has_errors": "❌ Has Errors",
            "no_errors": "✅ Valid",
            "validation_passed": "✅ Passed",
            "validation_failed": "❌ Failed",
            # Tools
            "has_tool_calls": "🔧 Has Tools",
            "no_tool_calls": "📄 No Tools",
            "tool_node": "🔧 Use Tools",
            # Parsing
            "parse_output": "📝 Parse",
            "needs_parsing": "📝 Parse Required",
            # Flow control
            "continue": "➡️ Continue",
            "retry": "🔄 Retry",
            "default": "📍 Default",
            "fallback": "↩️ Fallback",
            # Success/Error
            "success": "✅ Success",
            "error": "❌ Error",
            "failed": "❌ Failed",
        }

        # Check exact match
        if condition_str in label_map:
            return label_map[condition_str]

        # Check partial matches
        for key, label in label_map.items():
            if key in condition_str:
                return label

        # Default formatting
        return str(condition).replace("_", " ").title()

    @classmethod
    def _add_highlights(cls, lines: List[str], context: VisualizationContext):
        """Add highlight styling for specified nodes."""
        if not context.highlight_nodes:
            return

        lines.append("")
        lines.append("    %% ===== HIGHLIGHTS =====")

        highlight_ids = []
        for node_name in context.highlight_nodes:
            # Find all variations of this node in processed nodes
            for processed_id in context.processed_nodes:
                if node_name in processed_id or processed_id.endswith(f"_{node_name}"):
                    highlight_ids.append(processed_id)

        if highlight_ids:
            lines.append(
                f"    class {','.join(highlight_ids)} {NodeStyle.HIGHLIGHT.value}"
            )

    @classmethod
    def _add_agent_connections(
        cls, lines: List[str], graph: Any, context: VisualizationContext
    ):
        """Add connections between main graph and agent subgraphs."""
        # First find all agent nodes and their START/END nodes
        agent_connections = []

        # Keep track of which connections we've already processed to avoid duplicates
        processed_connections = set()

        # Find all agent nodes by looking at processed_nodes
        agent_nodes = {}
        for node_id in context.processed_nodes:
            if "_START" in node_id and not node_id.startswith("START"):
                # This is an agent START node
                agent_name = node_id.split("_START")[0]
                if agent_name not in agent_nodes:
                    agent_nodes[agent_name] = {"start": node_id, "end": None}

            if "_END" in node_id and not node_id.startswith("END"):
                # This is an agent END node
                agent_name = node_id.split("_END")[0]
                if agent_name in agent_nodes:
                    agent_nodes[agent_name]["end"] = node_id
                else:
                    agent_nodes[agent_name] = {"start": None, "end": node_id}

        # Now find connections in the graph that involve agents
        if hasattr(graph, "edges") and graph.edges:
            # Check each edge to see if it connects to/from an agent
            for source, target in graph.edges:
                # Check if source is an agent name
                # We don't need to handle special connections here
                # The connections should be direct from the main graph nodes to subgraph nodes
                # without special handling that creates duplicates

                # Check if target is an agent name
                if target in agent_nodes:
                    # Connection TO agent from regular node
                    end_node = agent_nodes[target]["end"]
                    if (
                        end_node and source != "START"
                    ):  # Avoid duplicate START connections
                        # Fix for __start__ reference - replace with START
                        destination = "START" if source == "__start__" else source
                        conn_key = f"{end_node}_to_{destination}"
                        if conn_key not in processed_connections:
                            agent_connections.append(
                                f"    {end_node} --> {destination}"
                            )
                            processed_connections.add(conn_key)

        # Also process branches for agent connections
        if hasattr(graph, "branches") and graph.branches:
            for branch_id, branch in graph.branches.items():
                if hasattr(branch, "source_node") and branch.source_node:
                    source = branch.source_node
                    destinations = cls._get_branch_destinations(branch)

                    # Check if source is an agent
                    if source in agent_nodes:
                        # Branch FROM agent
                        end_node = agent_nodes[source]["end"]
                        if end_node:
                            # Connect each destination to agent's END
                            for target in destinations.values():
                                if target != "END":
                                    agent_connections.append(
                                        f"    {end_node} --> {target}"
                                    )

                    # Check if any destination is an agent
                    for condition, target in destinations.items():
                        if target in agent_nodes:
                            # Branch TO agent
                            start_node = agent_nodes[target]["start"]
                            if start_node:
                                # Connect source to agent's START
                                if (
                                    source != "START"
                                ):  # Avoid duplicate START connections
                                    conn_key = f"{source}_to_{start_node}"
                                    if conn_key not in processed_connections:
                                        agent_connections.append(
                                            f"    {source} --> {start_node}"
                                        )
                                        processed_connections.add(conn_key)

        # Add agent connections if any were found
        if agent_connections:
            lines.append("")
            lines.append("    %% ===== AGENT CONNECTIONS =====")

            # Add connections between main graph and subgraphs
            # We need to find proper connections from main graph to subgraphs and vice versa
            seen_connections = set()
            explicit_connections = []

            # First, explicitly add START --> react_START connection
            # This ensures the flow goes from main graph START to the subgraph's START
            if "react_START" in context.node_mappings:
                explicit_connections.append("    START --> react_START")

            # Second, explicitly add react_END --> agent_node connection
            # This ensures the flow continues from subgraph's END to the next node
            if "react_END" in context.processed_nodes:
                explicit_connections.append("    react_END --> agent_node")

            # Add all explicit connections first
            for connection in explicit_connections:
                if connection not in lines:
                    lines.append(connection)
                    seen_connections.add(connection)

            # Then process any other agent connections that might be needed
            for connection in agent_connections:
                # Skip connections we've explicitly handled
                if connection in seen_connections:
                    continue

                # Skip direct connections from START to internal START nodes
                if "START --> " in connection and "_START" in connection:
                    continue

                # Skip any react_END connections since we're handling those explicitly
                if "react_END -->" in connection:
                    continue

                # Clean up problematic special node references
                if "__start__" in connection:
                    connection = connection.replace("__start__", "START")

                if "__end__" in connection:
                    connection = connection.replace("__end__", "END")

                # Only add if it's not already in the diagram
                if connection not in seen_connections and connection not in lines:
                    lines.append(connection)
                    seen_connections.add(connection)

    @classmethod
    def display_graph(
        cls,
        graph: Any,
        output_path: Optional[str] = None,
        include_subgraphs: bool = True,
        highlight_nodes: Optional[List[str]] = None,
        highlight_paths: Optional[List[List[str]]] = None,
        save_png: bool = False,
        width: str = "100%",
        theme: str = "base",
        subgraph_mode: str = "cluster",
        show_default_branches: bool = True,
        direction: str = "TB",
        compact_mode: bool = False,
        title: Optional[str] = None,
        debug: bool = False,
    ) -> str:
        """
        Generate and display graph with Agent expansion.

        Returns:
            Generated Mermaid code
        """
        logger.info(f"Displaying graph: {getattr(graph, 'name', 'Unnamed')}")

        # Combine highlight nodes
        all_highlight_nodes = highlight_nodes or []
        if highlight_paths:
            for path in highlight_paths:
                all_highlight_nodes.extend(path)

        # Generate Mermaid
        mermaid_code = cls.generate_mermaid(
            graph,
            include_subgraphs=include_subgraphs,
            highlight_nodes=all_highlight_nodes if all_highlight_nodes else None,
            theme=theme,
            show_branch_labels=show_default_branches,
            direction=direction,
            compact=compact_mode,
            debug=debug,
        )

        # Add title if provided
        if title:
            title_line = f"    %% {title}"
            mermaid_lines = mermaid_code.split("\n")
            mermaid_lines.insert(2, title_line)
            mermaid_code = "\n".join(mermaid_lines)

        # Generate output path if needed
        if save_png and not output_path:
            graph_name = getattr(graph, "name", f"graph_{uuid.uuid4().hex[:8]}")
            clean_name = graph_name.replace(" ", "_").replace("/", "_")
            output_dir = os.path.join(os.getcwd(), "graph_images")
            os.makedirs(output_dir, exist_ok=True)
            output_path = os.path.join(output_dir, f"{clean_name}.png")

        # Display
        display_mermaid(
            mermaid_code, output_path=output_path, save_png=save_png, width=width
        )

        return mermaid_code

    @classmethod
    def debug_graph_structure(cls, graph: Any) -> Dict[str, Any]:
        """Debug helper to analyze graph structure."""
        info = {
            "graph_name": getattr(graph, "name", "Unnamed"),
            "graph_type": type(graph).__name__,
            "nodes": {},
            "edges": [],
            "branches": {},
            "node_types": {},
            "agent_nodes": {},
        }

        # Analyze nodes
        if hasattr(graph, "nodes"):
            for name, node in (graph.nodes or {}).items():
                node_info = {
                    "type": type(node).__name__ if node else "None",
                    "has_graph": hasattr(node, "graph") and node.graph is not None,
                }

                # Check for EngineNodeConfig
                if (
                    hasattr(node, "__class__")
                    and "EngineNodeConfig" in node.__class__.__name__
                ):
                    node_info["is_engine_node_config"] = True

                    # Check engine
                    if hasattr(node, "engine"):
                        engine = node.engine
                        node_info["engine_type"] = (
                            type(engine).__name__ if engine else "None"
                        )

                        if hasattr(engine, "engine_type"):
                            if hasattr(engine.engine_type, "value"):
                                node_info["engine_type_value"] = (
                                    engine.engine_type.value
                                )
                            else:
                                node_info["engine_type_value"] = str(engine.engine_type)

                        node_info["engine_has_graph"] = (
                            hasattr(engine, "graph") and engine.graph is not None
                        )

                        # Check if engine is Agent
                        engine_class_name = type(engine).__name__ if engine else ""
                        node_info["engine_is_agent"] = "Agent" in engine_class_name

                        # Check MRO
                        if engine:
                            for base in type(engine).__mro__:
                                if base.__name__ == "Agent":
                                    node_info["engine_inherits_agent"] = True
                                    break

                # Check if node itself is Agent
                node_class_name = type(node).__name__ if node else ""
                node_info["is_agent"] = "Agent" in node_class_name

                # Check MRO
                if node:
                    for base in type(node).__mro__:
                        if base.__name__ == "Agent":
                            node_info["inherits_agent"] = True
                            break

                info["nodes"][name] = node_info

                # Track agent nodes
                is_agent = (
                    node_info.get("is_agent")
                    or node_info.get("inherits_agent")
                    or node_info.get("engine_is_agent")
                    or node_info.get("engine_inherits_agent")
                    or (node_info.get("engine_type_value") == "agent")
                )

                if is_agent:
                    info["agent_nodes"][name] = {
                        "reason": [],
                        "has_graph": node_info.get("has_graph")
                        or node_info.get("engine_has_graph", False),
                    }

                    if node_info.get("is_agent"):
                        info["agent_nodes"][name]["reason"].append("node_is_agent")
                    if node_info.get("inherits_agent"):
                        info["agent_nodes"][name]["reason"].append(
                            "node_inherits_agent"
                        )
                    if node_info.get("engine_is_agent"):
                        info["agent_nodes"][name]["reason"].append("engine_is_agent")
                    if node_info.get("engine_inherits_agent"):
                        info["agent_nodes"][name]["reason"].append(
                            "engine_inherits_agent"
                        )
                    if node_info.get("engine_type_value") == "agent":
                        info["agent_nodes"][name]["reason"].append(
                            "engine_type_is_agent"
                        )

        # Edges
        if hasattr(graph, "edges"):
            info["edges"] = list(graph.edges) if graph.edges else []

        # Branches
        if hasattr(graph, "branches"):
            for branch_id, branch in (graph.branches or {}).items():
                info["branches"][branch_id] = {
                    "source": getattr(branch, "source_node", "unknown"),
                    "destinations": cls._get_branch_destinations(branch),
                    "type": type(branch).__name__,
                }

        # Node types
        if hasattr(graph, "node_types"):
            info["node_types"] = {k: str(v) for k, v in graph.node_types.items()}

        return info
