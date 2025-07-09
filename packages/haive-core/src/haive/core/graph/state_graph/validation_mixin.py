# haive/core/graph/validation.py

from abc import abstractmethod
from typing import (
    List,
    Protocol,
    Tuple,
    runtime_checkable,
)

from rich.console import Console
from rich.table import Table

console = Console()


@runtime_checkable
class GraphValidationProtocol(Protocol):
    """Protocol defining requirements for graph validation."""

    allow_cycles: bool
    require_end_path: bool

    @abstractmethod
    def analyze_cycles(self) -> List[List[str]]:
        """Find all cycles in the graph."""
        ...

    @abstractmethod
    def find_orphan_nodes(self) -> List[str]:
        """Find nodes with no incoming or outgoing edges."""
        ...

    @abstractmethod
    def find_dangling_edges(self) -> List[Tuple[str, str]]:
        """Find edges pointing to non-existent nodes."""
        ...

    @abstractmethod
    def find_unreachable_nodes(self) -> List[str]:
        """Find nodes that cannot be reached from the entry point."""
        ...

    @abstractmethod
    def find_nodes_without_end_path(self) -> List[str]:
        """Find nodes that cannot reach the END node."""
        ...

    @abstractmethod
    def has_entry_point(self) -> bool:
        """Check if the graph has an entry point."""
        ...


class ValidationMixin:
    """
    Mixin for graph validation functionality.

    Provides methods for validating graph integrity, detecting cycles,
    finding orphaned nodes, and ensuring paths to END.

    This mixin expects the implementing class to provide:
    - allow_cycles: bool
    - require_end_path: bool
    - Various analysis methods defined in GraphValidationProtocol
    """

    def validate_graph(self) -> List[str]:  # Renamed from validate()
        """
        Perform comprehensive validation of the graph.

        Returns:
            List of validation issues (empty if valid)
        """
        issues: List[str] = []

        # Check for circular references only if cycles are not allowed
        if not self.allow_cycles:
            cycles = self.analyze_cycles()
            if cycles:
                cycle_strs = [" -> ".join(cycle) for cycle in cycles]
                issues.append(
                    f"Graph contains circular dependencies: {', '.join(cycle_strs)}"
                )

        # Check for orphan nodes (no incoming or outgoing edges)
        orphans = self.find_orphan_nodes()
        if orphans:
            issues.append(f"Graph contains orphan nodes: {', '.join(orphans)}")

        # Check for dangling edges (pointing to non-existent nodes)
        dangling_edges = self.find_dangling_edges()
        if dangling_edges:
            edge_strs = [f"{src} -> {dst}" for src, dst in dangling_edges]
            issues.append(f"Graph contains dangling edges: {', '.join(edge_strs)}")

        # Check for unreachable nodes
        unreachable = self.find_unreachable_nodes()
        if unreachable:
            issues.append(f"Graph contains unreachable nodes: {', '.join(unreachable)}")

        # Check for nodes that can't reach END (if required)
        if self.require_end_path:
            no_end_path = self.find_nodes_without_end_path()
            if no_end_path:
                issues.append(f"Nodes without path to END: {', '.join(no_end_path)}")

        # Check for missing entry point
        if not self.has_entry_point():
            issues.append("Graph has no entry point")

        return issues

    def display_validation_report(self) -> None:
        """Display a rich validation report."""
        issues = self.validate_graph()

        if not issues:
            console.print("[green]✓[/] Graph validation passed with no issues")
            return

        table = Table(title="Graph Validation Issues")
        table.add_column("Issue", style="red")

        for issue in issues:
            table.add_row(issue)

        console.print(table)
