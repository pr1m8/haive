"""Compilation tracking mixin for the state graph system.

This module provides the CompilationMixin class for tracking when a
graph needs to be recompiled due to changes.
"""

import logging
from typing import Any, Dict, Optional

from pydantic import Field

from haive.core.graph.state_graph.base.graph_state import CompilationState

logger = logging.getLogger(__name__)


class CompilationMixin:
    """Mixin that adds compilation tracking to a graph.

    This mixin adds methods to track graph changes and determine
    when recompilation is needed.
    """

    _compilation_state: CompilationState = Field(default_factory=CompilationState)
    _compiled_graph: Any | None = None

    def needs_recompilation(self) -> bool:
        """Check if the graph needs recompilation.

        Returns:
            True if recompilation is needed, False otherwise
        """
        return self._compilation_state.needs_recompilation()

    def mark_as_compiled(self) -> None:
        """Mark the graph as compiled."""
        self._compilation_state.mark_as_compiled()

    def mark_as_dirty(self) -> None:
        """Mark the graph as needing recompilation."""
        self._compilation_state.mark_as_dirty()
        self._compiled_graph = None

    def track_schema_change(self, field_name: str) -> None:
        """Track a change to the schema.

        Args:
            field_name: Name of the changed schema field
        """
        self._compilation_state.track_schema_change(field_name)
        self._compiled_graph = None

    def track_node_change(self, node_name: str, change_type: str) -> None:
        """Track a node addition, update, or removal.

        Args:
            node_name: Name of the changed node
            change_type: Type of change (add, update, remove)
        """
        self._compilation_state.track_node_change(node_name, change_type)
        self._compiled_graph = None

    def track_edge_change(self, source: str, target: str, change_type: str) -> None:
        """Track an edge addition or removal.

        Args:
            source: Source node name
            target: Target node name
            change_type: Type of change (add, remove)
        """
        self._compilation_state.track_edge_change(source, target, change_type)
        self._compiled_graph = None

    def track_branch_change(self, branch_id: str, change_type: str) -> None:
        """Track a branch addition, update, or removal.

        Args:
            branch_id: ID of the changed branch
            change_type: Type of change (add, update, remove)
        """
        self._compilation_state.track_branch_change(branch_id, change_type)
        self._compiled_graph = None

    def get_compilation_status(self) -> dict[str, Any]:
        """Get compilation status information.

        Returns:
            Dictionary with compilation status information
        """
        return self._compilation_state.get_change_summary()

    def compile(self, force: bool = False) -> Any:
        """Compile the graph to a runnable form if needed.

        Args:
            force: Force recompilation even if not needed

        Returns:
            Compiled graph
        """
        # Skip compilation if not needed and not forced
        if (
            not force
            and not self.needs_recompilation()
            and self._compiled_graph is not None
        ):
            logger.debug("Skipping compilation - no changes detected")
            return self._compiled_graph

        logger.debug("Compiling graph - changes detected or forced compilation")

        # Run validation
        issues = self.validate_graph() if hasattr(self, "validate_graph") else []

        if issues:
            from rich.console import Console

            console = Console()
            console.print("\n[bold yellow]Graph Validation Issues:[/bold yellow]")
            for issue in issues:
                console.print(f"[yellow]- {issue}[/yellow]")
            console.print(
                "[yellow]Proceeding with compilation despite issues...[/yellow]"
            )

        # Convert to LangGraph
        if hasattr(self, "to_langgraph"):
            lang_graph = self.to_langgraph()

            # Compile the graph
            self._compiled_graph = lang_graph.compile()

            # Mark as compiled
            self.mark_as_compiled()

            return self._compiled_graph
        raise NotImplementedError("Graph must implement to_langgraph() method")

    def get_or_compile(self) -> Any:
        """Get the compiled graph, compiling if needed.

        Returns:
            Compiled graph
        """
        if self._compiled_graph is None or self.needs_recompilation():
            return self.compile()
        return self._compiled_graph

    def invoke(self, input_value: Any, config: Any | None = None) -> Any:
        """Invoke the graph with input.

        Automatically handles compilation if needed.

        Args:
            input_value: Input value for the graph
            config: Optional configuration

        Returns:
            Graph execution result
        """
        # Get or compile the graph
        compiled_graph = self.get_or_compile()

        # Validate input if schema is available
        if hasattr(self, "validate_input"):
            input_value = self.validate_input(input_value)

        # Invoke the compiled graph
        result = compiled_graph.invoke(input_value, config)

        # Validate output if schema is available
        if hasattr(self, "validate_output"):
            result = self.validate_output(result)

        return result
