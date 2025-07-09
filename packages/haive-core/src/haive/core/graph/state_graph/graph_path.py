# haive/core/graph/paths.py

from typing import List

from pydantic import BaseModel, Field
from rich.console import Console
from rich.panel import Panel

console = Console()


class GraphPath(BaseModel):
    """
    Model representing a path through the graph with analysis capabilities.

    Provides methods for analyzing paths including conditional branches,
    reaching END nodes, and path visualization.
    """

    nodes: List[str] = Field(
        default_factory=list, description="Ordered list of nodes in the path"
    )
    contains_conditional: bool = Field(
        default=False, description="Whether the path contains conditional branches"
    )
    reaches_end: bool = Field(
        default=False, description="Whether the path reaches the END node"
    )

    def __str__(self) -> str:
        """Get string representation of the path."""
        return " -> ".join(self.nodes)

    def display(self) -> None:
        """Display the path with rich formatting."""
        if not self.nodes:
            console.print("[yellow]Empty path[/]")
            return

        path_str = " → ".join(
            [
                (
                    f"[green]{node}[/]"
                    if i == 0
                    else (
                        f"[red]{node}[/]"
                        if i == len(self.nodes) - 1
                        else (
                            f"[yellow]{node}[/]"
                            if self.contains_conditional
                            else f"[blue]{node}[/]"
                        )
                    )
                )
                for i, node in enumerate(self.nodes)
            ]
        )

        status = []
        if self.contains_conditional:
            status.append("[yellow]Contains conditional branches[/]")
        if self.reaches_end:
            status.append("[green]Reaches END[/]")
        else:
            status.append("[red]Does not reach END[/]")

        panel = Panel(
            path_str,
            title="Graph Path",
            subtitle=" | ".join(status) if status else None,
            border_style="blue",
        )
        console.print(panel)

    def merge(self, other: "GraphPath") -> "GraphPath":
        """
        Merge this path with another path, continuing from the last node.

        Args:
            other: The path to merge with this one

        Returns:
            A new merged path
        """
        if not self.nodes:
            return other
        if not other.nodes:
            return self

        # If paths don't connect, return a copy of this path
        if self.nodes[-1] != other.nodes[0]:
            return GraphPath(
                nodes=self.nodes.copy(),
                contains_conditional=self.contains_conditional,
                reaches_end=self.reaches_end,
            )

        # Create new path with merged nodes (avoiding duplication)
        merged_nodes = self.nodes + other.nodes[1:]

        return GraphPath(
            nodes=merged_nodes,
            contains_conditional=self.contains_conditional
            or other.contains_conditional,
            reaches_end=other.reaches_end,
        )

    def append(
        self, node: str, is_conditional: bool = False, is_end: bool = False
    ) -> "GraphPath":
        """
        Append a node to this path.

        Args:
            node: Node to append
            is_conditional: Whether this node is added via a conditional edge
            is_end: Whether this node is an END node

        Returns:
            A new path with the node appended
        """
        # Skip append if it would create a duplicate of the last node
        if self.nodes and self.nodes[-1] == node:
            # Return a copy with updated flags only
            return GraphPath(
                nodes=self.nodes.copy(),  # Keep existing nodes
                contains_conditional=self.contains_conditional or is_conditional,
                reaches_end=self.reaches_end or is_end,
            )

        # Normal append
        new_nodes = self.nodes.copy()
        new_nodes.append(node)

        return GraphPath(
            nodes=new_nodes,
            contains_conditional=self.contains_conditional or is_conditional,
            reaches_end=self.reaches_end or is_end,
        )
