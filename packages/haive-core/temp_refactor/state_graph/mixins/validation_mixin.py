"""Graph validation mixin for the state graph system.

This module provides the ValidationMixin class for validating graph
structure and integrity.
"""

from typing import List, Tuple

from rich.console import Console
from rich.table import Table

console = Console()


class ValidationMixin:
    """Mixin for graph validation functionality.

    Provides methods for validating graph integrity, detecting cycles,
    finding orphaned nodes, and ensuring paths to END.

    This mixin expects the implementing class to provide:
    - allow_cycles: bool
    - require_end_path: bool
    - Various analysis methods
    """

    allow_cycles: bool = False
    require_end_path: bool = True

    def validate_graph(self) -> list[str]:
        """Perform comprehensive validation of the graph.

        Returns:
            List of validation issues (empty if valid)
        """
        issues: list[str] = []

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

    # Abstract methods that must be implemented

    def analyze_cycles(self) -> list[list[str]]:
        """Find all cycles in the graph."""
        cycles = []
        visited = set()
        path = []
        path_set = set()

        def dfs(node):
            if node in path_set:
                # Found a cycle, extract it
                cycle_start = path.index(node)
                cycles.append([*path[cycle_start:], node])
                return

            if node in visited:
                return

            visited.add(node)
            path.append(node)
            path_set.add(node)

            # Follow direct edges
            for src, dst in self.edges:
                if src == node and dst != "END":
                    dfs(dst)

            # Follow branch destinations
            for branch in self.branches.values():
                if branch.source_node == node:
                    for dest in branch.destinations.values():
                        if dest != "END":
                            dfs(dest)

                    if branch.default and branch.default != "END":
                        dfs(branch.default)

            path.pop()
            path_set.remove(node)

        # Start DFS from each node
        for node in self.nodes:
            if node not in visited:
                dfs(node)

        return cycles

    def find_orphan_nodes(self) -> list[str]:
        """Find nodes with no incoming or outgoing edges."""
        orphans = []

        for node_name in self.nodes:
            # Skip None nodes
            if self.nodes[node_name] is None:
                continue

            # Check if node has any incoming edges
            has_incoming = False
            for _, dst in self.edges:
                if dst == node_name:
                    has_incoming = True
                    break

            for branch in self.branches.values():
                for dest in branch.destinations.values():
                    if dest == node_name:
                        has_incoming = True
                        break
                if branch.default == node_name:
                    has_incoming = True
                    break

            # Check if node has any outgoing edges
            has_outgoing = False
            for src, _ in self.edges:
                if src == node_name:
                    has_outgoing = True
                    break

            for branch in self.branches.values():
                if branch.source_node == node_name:
                    has_outgoing = True
                    break

            # If node has neither incoming nor outgoing edges, it's an orphan
            if not has_incoming and not has_outgoing:
                orphans.append(node_name)

        return orphans

    def find_dangling_edges(self) -> list[tuple[str, str]]:
        """Find edges pointing to non-existent nodes."""
        dangling = []

        # Check direct edges
        for src, dst in self.edges:
            if src != "START" and src not in self.nodes:
                dangling.append((src, dst))
            if dst != "END" and dst not in self.nodes:
                dangling.append((src, dst))

        # Check branch destinations
        for branch in self.branches.values():
            src = branch.source_node
            if src != "START" and src not in self.nodes:
                for dest in branch.destinations.values():
                    dangling.append((src, dest))
            else:
                for dest in branch.destinations.values():
                    if dest != "END" and dest not in self.nodes:
                        dangling.append((src, dest))

                if (
                    branch.default
                    and branch.default != "END"
                    and branch.default not in self.nodes
                ):
                    dangling.append((src, branch.default))

        return dangling

    def find_unreachable_nodes(self) -> list[str]:
        """Find nodes that can't be reached from START."""
        # Get all nodes reachable from START
        reachable = set()

        def dfs(node):
            if node in reachable:
                return

            reachable.add(node)

            # Follow direct edges
            for src, dst in self.edges:
                if src == node:
                    dfs(dst)

            # Follow branch destinations
            for branch in self.branches.values():
                if branch.source_node == node:
                    for dest in branch.destinations.values():
                        dfs(dest)

                    if branch.default:
                        dfs(branch.default)

        # Start from START node
        dfs("START")

        # Return unreachable nodes (excluding special nodes)
        return [
            node
            for node in self.nodes
            if node not in reachable and self.nodes[node] is not None
        ]

    def find_nodes_without_end_path(self) -> list[str]:
        """Find nodes that can't reach END."""
        # For each node, check if there's a path to END
        no_end_path = []

        # Helper function to check if a path exists from source to target
        def has_path(source, target, visited=None):
            if visited is None:
                visited = set()

            if source == target:
                return True

            if source in visited:
                return False

            visited.add(source)

            # Check direct edges
            for src, dst in self.edges:
                if src == source and dst not in visited:
                    if has_path(dst, target, visited):
                        return True

            # Check branch destinations
            for branch in self.branches.values():
                if branch.source_node == source:
                    for dest in branch.destinations.values():
                        if dest not in visited:
                            if has_path(dest, target, visited):
                                return True

                    if branch.default and branch.default not in visited:
                        if has_path(branch.default, target, visited):
                            return True

            return False

        for node_name in self.nodes:
            # Skip None nodes
            if self.nodes[node_name] is None:
                continue

            if not has_path(node_name, "END"):
                no_end_path.append(node_name)

        return no_end_path

    def has_entry_point(self) -> bool:
        """Check if the graph has an entry point."""
        # Check for direct edges from START
        for src, _ in self.edges:
            if src == "START":
                return True

        # Check for branches from START
        return any(branch.source_node == "START" for branch in self.branches.values())
