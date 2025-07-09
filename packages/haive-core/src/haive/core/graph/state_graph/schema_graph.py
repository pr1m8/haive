# haive/core/graph/graph.py

import logging
from typing import Optional

from langgraph.graph import StateGraph
from pydantic import ConfigDict
from rich.console import Console

from haive.core.graph.common.types import ConfigLike, StateLike
from haive.core.graph.state_graph.base_graph2 import BaseGraph
from haive.core.graph.state_graph.conversion.langgraph import convert_to_langgraph
from haive.core.graph.state_graph.schema_mixin import GraphSchemaMixin

logger = logging.getLogger(__name__)
console = Console()


class SchemaGraph(BaseGraph, GraphSchemaMixin[StateLike, Optional[ConfigLike]]):
    """
    Graph implementation with schema management capabilities.

    SchemaGraph extends BaseGraph with state schema management, enabling
    seamless integration with LangGraph and providing type validation.
    """

    model_config = ConfigDict(arbitrary_types_allowed=True)

    def to_langgraph(self) -> StateGraph:
        """
        Convert to a LangGraph StateGraph with schema information.

        Returns:
            LangGraph StateGraph instance
        """
        langgraph = convert_to_langgraph(self, self.state_schema)

        # Mark as compiled in BaseGraph tracking
        self.mark_compiled(
            input_schema=getattr(self, "input_schema", None),
            output_schema=getattr(self, "output_schema", None),
            config_schema=getattr(self, "config_schema", None),
        )

        return langgraph

    def compile(self, **kwargs) -> StateGraph:
        """
        Validate and compile the graph to a runnable StateGraph.

        Args:
            **kwargs: Additional compilation arguments (checkpointer, interrupt_before, etc.)

        Returns:
            Compiled LangGraph StateGraph
        """
        # Extract interrupt parameters for tracking
        interrupt_before = kwargs.get("interrupt_before")
        interrupt_after = kwargs.get("interrupt_after")

        # Mark as compiled in BaseGraph with compilation parameters
        self.mark_compiled(
            input_schema=getattr(self, "input_schema", None),
            output_schema=getattr(self, "output_schema", None),
            config_schema=getattr(self, "config_schema", None),
            interrupt_before=interrupt_before,
            interrupt_after=interrupt_after,
            **{
                k: v
                for k, v in kwargs.items()
                if k not in ["interrupt_before", "interrupt_after"]
            },
        )

        # Convert to LangGraph and compile
        return self.to_langgraph().compile(**kwargs)

    def display(self):
        """
        Display a visual representation of the graph structure.

        Outputs information about nodes, edges, and branches,
        and generates a Mermaid diagram for visualization.
        """
        print("\n" + "=" * 50)
        print(f"GRAPH: {self.name}")
        print("=" * 50)

        # Display basic graph info
        print(f"\nNodes ({len(self.nodes)}):")
        for name, _node in self.nodes.items():
            node_type = self.node_types.get(name, "unknown")
            print(f"  - {name} ({node_type})")

        print(f"\nEdges ({len(self.edges)}):")
        for src, dst in self.edges:
            print(f"  - {src} → {dst}")

        print(f"\nBranches ({len(self.branches)}):")
        for _branch_id, branch in self.branches.items():
            print(f"  - {branch.name} (from {branch.source_node}):")
            for cond, dest in branch.destinations.items():
                print(f"    - {cond} → {dest}")
            if branch.default:
                print(f"    - default → {branch.default}")

        # Generate and print Mermaid diagram
        print("\nMermaid Diagram:")
        print("```mermaid")
        print(self.to_mermaid())
        print("```")

        # Display validation issues if any
        issues = self.check_graph_validity()
        if issues:
            print("\nWARNING: Graph Validation Issues:")
            for issue in issues:
                print(f"  - {issue}")
        else:
            print("\nGraph validation: OK")

        print("\n" + "=" * 50 + "\n")

        return self
