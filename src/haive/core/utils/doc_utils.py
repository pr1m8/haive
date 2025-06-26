"""Utilities for generating standardized documentation visualizations from agent outputs.

This module provides functions for converting agent state histories, graphs, and
outputs into standardized formats for documentation.
"""

import datetime
import json
import logging
import os
from pathlib import Path
from typing import Any
import uuid

from graphviz import Digraph
import markdown


# Set up logging
logger = logging.getLogger(__name__)


class AgentVisualizer:
    """Standardized visualization of agent outputs and graphs for documentation.

    This class provides methods to:
    1. Convert agent state history to markdown
    2. Visualize agent graphs consistently
    3. Save outputs in documentation-friendly formats
    4. Generate embeddable HTML/SVG for Sphinx

    Works with both haive.core.engine.agent and haive.agents.base.agent patterns.
    """

    def __init__(
        self,
        output_dir: str | None = None,
        state_history_dir: str | None = None,
        graph_dir: str | None = None,
    ):
        """Initialize the visualizer with output directories.

        Args:
            output_dir: Base directory for all outputs
            state_history_dir: Directory for state history files
            graph_dir: Directory for graph visualizations
        """
        # Set up default directories
        self.output_dir = Path(
            output_dir
            or os.environ.get(
                "HAIVE_DOCS_OUTPUT",
                Path(__file__).parents[5]
                / "docs"
                / "source"
                / "_static"
                / "agent_outputs",
            )
        )
        self.state_history_dir = Path(
            state_history_dir or self.output_dir / "state_history"
        )
        self.graph_dir = Path(graph_dir or self.output_dir / "graphs")

        # Create directories if they don't exist
        self.output_dir.mkdir(exist_ok=True, parents=True)
        self.state_history_dir.mkdir(exist_ok=True, parents=True)
        self.graph_dir.mkdir(exist_ok=True, parents=True)

    def save_agent_state_history(
        self,
        agent_name: str,
        state_history: list[dict[str, Any]],
        metadata: dict[str, Any] | None = None,
    ) -> str:
        """Save agent state history to a standardized format for documentation.

        Args:
            agent_name: Name of the agent
            state_history: List of state dictionaries
            metadata: Additional metadata about the agent run

        Returns:
            Path to the saved state history file
        """
        # Generate timestamp and ID for the file
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        run_id = str(uuid.uuid4())[:8]

        # Prepare metadata
        metadata = metadata or {}
        metadata.update(
            {
                "agent_name": agent_name,
                "timestamp": timestamp,
                "run_id": run_id,
                "generated_by": "haive.core.utils.doc_utils.AgentVisualizer",
            }
        )

        # Prepare output
        output = {"metadata": metadata, "state_history": state_history}

        # Generate filename and save
        filename = f"{agent_name}_{timestamp}_{run_id}.json"
        filepath = self.state_history_dir / filename

        with open(filepath, "w") as f:
            json.dump(output, f, indent=2, default=str)

        logger.info(f"Saved agent state history to {filepath}")
        return str(filepath)

    def state_history_to_markdown(
        self,
        state_history_path: str | Path,
        include_metadata: bool = True,
        max_states: int | None = None,
    ) -> str:
        """Convert a state history file to markdown for documentation.

        Args:
            state_history_path: Path to state history JSON file
            include_metadata: Whether to include metadata in the output
            max_states: Maximum number of states to include (None for all)

        Returns:
            Markdown string representation of the state history
        """
        # Load state history
        try:
            with open(state_history_path) as f:
                data = json.load(f)
        except Exception as e:
            logger.error(f"Failed to load state history from {state_history_path}: {e}")
            return f"Error loading state history: {e}"

        # Extract metadata and state history
        metadata = data.get("metadata", {})
        state_history = data.get("state_history", [])

        if max_states:
            state_history = state_history[:max_states]

        # Generate markdown
        md_lines = []

        # Add metadata
        if include_metadata:
            md_lines.append("# Agent Run Details\n")
            md_lines.append(
                f"- **Agent Name**: {metadata.get('agent_name', 'Unknown')}"
            )
            md_lines.append(f"- **Timestamp**: {metadata.get('timestamp', 'Unknown')}")
            md_lines.append(f"- **Run ID**: {metadata.get('run_id', 'Unknown')}")

            # Add any additional metadata
            for key, value in metadata.items():
                if key not in ["agent_name", "timestamp", "run_id", "generated_by"]:
                    md_lines.append(f"- **{key}**: {value}")

            md_lines.append("\n---\n")

        # Add state history
        md_lines.append("# State History\n")

        for i, state in enumerate(state_history):
            md_lines.append(f"## State {i+1}\n")

            # Handle different state formats
            if isinstance(state, dict):
                for key, value in state.items():
                    if key in ["input", "output", "thought", "action", "observation"]:
                        md_lines.append(f"### {key.capitalize()}\n")

                        # Format based on content type
                        if isinstance(value, (dict, list)):
                            md_lines.append("```json")
                            md_lines.append(json.dumps(value, indent=2, default=str))
                            md_lines.append("```\n")
                        else:
                            md_lines.append(f"```\n{value}\n```\n")
            else:
                md_lines.append(f"```\n{state}\n```\n")

            md_lines.append("---\n")

        return "\n".join(md_lines)

    def save_agent_graph(
        self,
        agent_name: str,
        graph: Any,
        format: str = "svg",
        metadata: dict[str, Any] | None = None,
    ) -> str:
        """Save agent graph visualization for documentation.

        Works with both langgraph Graph objects and custom Digraph objects.

        Args:
            agent_name: Name of the agent
            graph: Graph object to visualize
            format: Output format (svg, png, etc.)
            metadata: Additional metadata

        Returns:
            Path to the saved graph file
        """
        # Generate timestamp and ID for the file
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        run_id = str(uuid.uuid4())[:8]

        # Generate filename
        filename = f"{agent_name}_graph_{timestamp}_{run_id}.{format}"
        filepath = self.graph_dir / filename

        try:
            # Handle different graph types
            # Case 1: LangGraph Graph object
            if hasattr(graph, "get_graph"):
                dot = graph.get_graph()
                dot.format = format
                dot.render(filepath.with_suffix(""), cleanup=True)
            # Case 2: Graphviz Digraph object
            elif isinstance(graph, Digraph):
                graph.format = format
                graph.render(filepath.with_suffix(""), cleanup=True)
            # Case 3: Dictionary representation
            elif isinstance(graph, dict):
                dot = Digraph(name=agent_name)
                # Convert dict to Digraph
                for node, edges in graph.items():
                    dot.node(str(node))
                    if isinstance(edges, (list, tuple)):
                        for edge in edges:
                            dot.edge(str(node), str(edge))
                    elif edges:
                        dot.edge(str(node), str(edges))

                dot.format = format
                dot.render(filepath.with_suffix(""), cleanup=True)
            else:
                logger.error(f"Unsupported graph type: {type(graph)}")
                return None

            logger.info(f"Saved agent graph to {filepath}")
            return str(filepath)
        except Exception as e:
            logger.error(f"Failed to save graph: {e}")
            return None

    def generate_agent_visualization_page(
        self,
        agent_name: str,
        agent_description: str,
        state_history_path: str | Path | None = None,
        graph_path: str | Path | None = None,
        additional_content: str | None = None,
    ) -> str:
        """Generate a complete documentation page for an agent with visualizations.

        Args:
            agent_name: Name of the agent
            agent_description: Description of the agent
            state_history_path: Path to state history file
            graph_path: Path to graph visualization
            additional_content: Additional markdown content to include

        Returns:
            RST content for a complete documentation page
        """
        # Generate timestamp
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Start building RST content
        rst_lines = []

        # Add title and description
        rst_lines.append(f".. title:: {agent_name} Example")
        rst_lines.append(f".. _{agent_name.lower().replace(' ', '_')}:\n")
        rst_lines.append(f"{agent_name}")
        rst_lines.append("=" * len(agent_name))
        rst_lines.append("")
        rst_lines.append(f"{agent_description}\n")
        rst_lines.append(f"*Generated on: {timestamp}*\n")

        # Add graph visualization if provided
        if graph_path:
            graph_path = Path(graph_path)
            if graph_path.exists():
                # Determine relative path for documentation
                rel_path = f"../_static/agent_outputs/graphs/{graph_path.name}"
                rst_lines.append("Agent Graph")
                rst_lines.append("-----------\n")
                rst_lines.append(f".. image:: {rel_path}")
                rst_lines.append("   :alt: Agent Graph Visualization")
                rst_lines.append("   :width: 100%\n")

        # Add state history if provided
        if state_history_path:
            rst_lines.append("Example Run")
            rst_lines.append("------------\n")

            # Convert state history to markdown
            md_content = self.state_history_to_markdown(
                state_history_path,
                include_metadata=True,
                max_states=5,  # Limit to 5 states for documentation
            )

            # Embed markdown content in RST
            rst_lines.append(".. raw:: html\n")

            # Convert markdown to HTML
            html_content = markdown.markdown(
                md_content, extensions=["fenced_code", "tables", "nl2br"]
            )

            # Indent HTML content for RST
            html_lines = html_content.split("\n")
            rst_lines.extend([f"   {line}" for line in html_lines])
            rst_lines.append("\n")

        # Add additional content if provided
        if additional_content:
            rst_lines.append(additional_content)

        # Generate file path for the RST file
        safe_name = agent_name.lower().replace(" ", "_")
        rst_filename = f"{safe_name}_example.rst"
        rst_path = self.output_dir.parent.parent / "agents" / "examples" / rst_filename

        # Create directory if it doesn't exist
        rst_path.parent.mkdir(exist_ok=True, parents=True)

        # Write RST file
        with open(rst_path, "w") as f:
            f.write("\n".join(rst_lines))

        logger.info(f"Generated agent documentation page at {rst_path}")
        return str(rst_path)


# Helper functions for easy use in scripts or notebooks


def visualize_agent_run(
    agent_name: str,
    state_history: list[dict[str, Any]],
    graph: Any | None = None,
    description: str | None = None,
    metadata: dict[str, Any] | None = None,
) -> dict[str, str]:
    """Convenience function to visualize an agent run and save to documentation.

    Args:
        agent_name: Name of the agent
        state_history: State history from the agent run
        graph: Optional graph object from the agent
        description: Optional description of the agent
        metadata: Optional metadata about the agent run

    Returns:
        Dictionary with paths to generated files
    """
    visualizer = AgentVisualizer()

    # Save state history
    state_path = visualizer.save_agent_state_history(
        agent_name=agent_name, state_history=state_history, metadata=metadata
    )

    # Save graph if provided
    graph_path = None
    if graph:
        graph_path = visualizer.save_agent_graph(
            agent_name=agent_name, graph=graph, metadata=metadata
        )

    # Generate documentation page
    doc_path = visualizer.generate_agent_visualization_page(
        agent_name=agent_name,
        agent_description=description or f"{agent_name} agent implementation example",
        state_history_path=state_path,
        graph_path=graph_path,
    )

    return {"state_history": state_path, "graph": graph_path, "documentation": doc_path}


def create_agent_example_index(examples_dir: str | Path | None = None) -> str:
    """Create an index page for all agent examples.

    Args:
        examples_dir: Directory containing agent example RST files

    Returns:
        Path to the generated index file
    """
    visualizer = AgentVisualizer()
    examples_dir = Path(
        examples_dir or visualizer.output_dir.parent.parent / "agents" / "examples"
    )

    if not examples_dir.exists():
        logger.warning(f"Examples directory {examples_dir} does not exist")
        return None

    # Gather all example files
    example_files = list(examples_dir.glob("*_example.rst"))

    if not example_files:
        logger.warning(f"No example files found in {examples_dir}")
        return None

    # Generate index content
    rst_lines = []

    rst_lines.append(".. title:: Agent Examples")
    rst_lines.append(".. _agent_examples:\n")
    rst_lines.append("Agent Examples")
    rst_lines.append("==============\n")
    rst_lines.append("Real-world examples of Haive agents in action.\n")

    # Add toctree
    rst_lines.append(".. toctree::")
    rst_lines.append("   :maxdepth: 1\n")

    for example_file in sorted(example_files):
        # Get file name without extension
        name = example_file.stem
        rst_lines.append(f"   {name}")

    # Generate index file path
    index_path = examples_dir / "index.rst"

    # Write index file
    with open(index_path, "w") as f:
        f.write("\n".join(rst_lines))

    logger.info(f"Generated agent examples index at {index_path}")
    return str(index_path)
