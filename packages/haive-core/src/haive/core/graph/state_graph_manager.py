from collections import defaultdict
from typing import Any

import matplotlib.pyplot as plt
import networkx as nx


class StateGraphManager:
    """A manager for extracting metadata and modifying a StateGraph."""

    def __init__(self, graph: Any):
        """Initialize the StateGraphManager.

        Args:
            graph (StateGraph): The StateGraph object to manage.
        """
        self.graph = graph
        self.metadata = self.extract_metadata()
        self.needs_recompile = False  # Track modifications requiring recompilation

    def extract_metadata(self) -> dict[str, Any]:
        """Extract metadata from the StateGraph, including conditional branches."""
        metadata = {
            "entry_point": getattr(self.graph, "entry_point", None),
            "finish_point": getattr(self.graph, "finish_point", None),
            "nodes": list(self.graph.nodes.keys()),
            "edges": list(self.graph.edges),
            "conditional_edges": defaultdict(list),
            "schemas": getattr(self.graph, "schemas", {}),
            "input_schema": getattr(self.graph, "input", None),
            "output_schema": getattr(self.graph, "output", None),
            "compiled": getattr(self.graph, "compiled", False),
            "support_multiple_edges": getattr(
                self.graph, "support_multiple_edges", True
            ),
        }

        branches = getattr(self.graph, "branches", {})
        for node, conditions in branches.items():
            for _condition_name, branch_obj in conditions.items():
                if hasattr(branch_obj, "ends"):
                    for condition, target in branch_obj.ends.items():
                        metadata["conditional_edges"][node].append(
                            (condition, "END" if target == "__end__" else target)
                        )

        return metadata

    def ensure_compiled(self):
        """Recompile the graph if modifications were made."""
        if self.needs_recompile:
            self.graph.compile()
            self.metadata = self.extract_metadata()
            self.needs_recompile = False

    def add_node(self, node: str):
        """Add a node to the graph."""
        if node not in self.graph.nodes:
            self.graph.nodes[node] = {}
            self.needs_recompile = True

    def remove_edge(self, src: str, dst: str):
        """Remove an edge from the graph."""
        if (src, dst) in self.graph.edges:
            self.graph.edges.remove((src, dst))
            self.needs_recompile = True

    # def insert_node(self, node: str, between: Tuple[str, str], func: callable = None):
    def insert_node(
        self, node: str, between: tuple[str, str], func: callable | None = None
    ):
        """Insert a new node between two existing nodes, using LangGraph's `add_node` and `add_edge` methods.

        Args:
            node (str): The name of the new node.
            between (Tuple[str, str]): A tuple (src, dst) indicating where to insert the node.
            func (callable, optional): The function that the node represents in LangGraph.
        """
        src, dst = between

        if src not in self.graph.nodes or dst not in self.graph.nodes:
            self.graph.add_node(node, func)
            raise ValueError(
                f"Cannot insert node: {src} or {dst} does not exist in the graph."
            )

        # Remove the existing edge
        self.remove_edge(src, dst)

        # If function is not provided, try to extract from the existing graph
        if func is None:
            func = getattr(self.graph, node, None)  # Try extracting from existing graph
            if not callable(func):
                raise ValueError(
                    f"No callable function found for `{node}`. Provide `func` explicitly."
                )

        # ✅ Add the new node with its function in LangGraph
        self.graph.add_node(func, node)

        # ✅ Add new edges
        self.graph.add_edge(src, node)
        self.graph.add_edge(node, dst)

        self.needs_recompile = True

    def insert_start_node(self, node: str):
        """Insert a node into the branch between `__start__` and the first connected node."""
        # Retrieve edges originating from `__start__`
        start_edges = [edge for edge in self.graph.edges if edge[0] == "__start__"]

        if not start_edges:
            raise ValueError(
                "No existing start edges found. Ensure `__start__` is connected in the graph."
            )

        # Pick the first transition from `__start__`
        _, first_node = start_edges[0]

        # Add the new node
        self.add_node(node)

        # Remove old edge and insert new ones
        self.remove_edge("__start__", first_node)
        self.graph.edges.add(("__start__", node))
        self.graph.edges.add((node, first_node))

        self.needs_recompile = True

    def insert_end_node(self, node: str):
        """Insert a node into the branch before `END`."""
        # Retrieve edges that connect to `END`
        end_edges = [edge for edge in self.graph.edges if edge[1] == "END"]

        if not end_edges:
            raise ValueError(
                "No existing end edges found. Ensure `END` is connected in the graph."
            )

        # Pick the first transition to `END`
        last_node, _ = end_edges[0]

        # Add the new node
        self.add_node(node)

        # Remove old edge and insert new edges

    def update_branch(self, node: str, condition: str, target: str):
        """Update a conditional branch using defaultdict."""
        if "branches" not in self.graph.__dict__:
            self.graph.branches = defaultdict(dict)
        if node not in self.graph.branches:
            self.graph.branches[node] = {}

        self.graph.branches[node][condition] = target
        self.needs_recompile = True

    def get_metadata(self):
        """Return the extracted metadata."""
        return self.metadata

    def __del__(self):
        """Ensure compilation before object is deleted."""
        self.ensure_compiled()

    def visualize(self, output_file: str = "state_graph.png"):
        """Visualize the StateGraph using NetworkX, ensuring **arrows are drawn correctly**.

        Args:
            output_file (str): The filename to save the visualization.
        """
        G = nx.DiGraph()
        solid_edges = []
        dashed_edges = []
        edge_labels = {}

        # ✅ Add nodes
        for node in self.metadata["nodes"]:
            G.add_node(node)

        # ✅ Add standard edges (Solid)
        for src, dst in self.metadata["edges"]:
            if dst == "__end__":
                dst = "END"
            G.add_edge(src, dst)
            solid_edges.append((src, dst))

        # ✅ Add conditional branching edges (Dashed)
        for node, conditions in self.metadata["conditional_edges"].items():
            for condition, target in conditions:
                G.add_edge(node, target)
                dashed_edges.append((node, target))
                edge_labels[(node, target)] = f"{condition}"

        # ✅ Layout for better separation
        plt.figure(figsize=(14, 8))
        pos = nx.spring_layout(G, seed=42)  # More natural positioning

        # **Draw Solid Edges (State Transitions)**
        nx.draw_networkx_edges(
            G,
            pos,
            edgelist=solid_edges,
            edge_color="black",
            width=2,
            alpha=0.8,
            arrows=True,
            arrowstyle="-|>",
            arrowsize=20,  # 🔥 Force arrows
            connectionstyle="arc3,rad=0.1",
        )

        # **Draw Dashed Conditional Edges (Branching Paths)**
        nx.draw_networkx_edges(
            G,
            pos,
            edgelist=dashed_edges,
            edge_color="red",
            style="dashed",
            width=2,
            arrows=True,
            arrowstyle="-|>",
            arrowsize=20,  # 🔥 Force arrows
            connectionstyle="arc3,rad=0.3",
        )

        # **Draw Nodes**
        nx.draw_networkx_nodes(
            G, pos, node_color="lightblue", node_size=2800, edgecolors="black"
        )
        nx.draw_networkx_labels(G, pos, font_size=12, font_weight="bold")

        # **Draw Conditional Labels**
        nx.draw_networkx_edge_labels(
            G, pos, edge_labels=edge_labels, font_color="red", font_size=10
        )

        # ✅ Highlight entry and finish points
        entry = self.metadata["entry_point"]
        finish = self.metadata["finish_point"]

        if entry:
            nx.draw_networkx_nodes(
                G,
                pos,
                nodelist=[entry],
                node_color="green",
                node_size=3000,
                edgecolors="black",
            )  # Entry point
        if finish and finish in self.metadata["nodes"]:
            nx.draw_networkx_nodes(
                G,
                pos,
                nodelist=[finish],
                node_color="red",
                node_size=3000,
                edgecolors="black",
            )  # Finish point

        # ✅ Save and display
        plt.title("State Graph Visualization", fontsize=14, fontweight="bold")
        plt.savefig(output_file, bbox_inches="tight")
        plt.show()

    def get_metadata(self):
        """Return the extracted metadata."""
        return self.metadata

    # Add this static method to create a manager and attach it to a graph
    @staticmethod
    def attach_to_graph(graph):
        """Create a manager and attach it to a StateGraph.

        This modifies the graph object to add a get_manager method.

        Args:
            graph: StateGraph to attach to

        Returns:
            The modified graph
        """
        # Create manager
        manager = StateGraphManager(graph)

        # Add get_manager method to the graph
        def get_manager():
            return manager

        # Attach the method to the graph
        graph.get_manager = get_manager

        return graph
