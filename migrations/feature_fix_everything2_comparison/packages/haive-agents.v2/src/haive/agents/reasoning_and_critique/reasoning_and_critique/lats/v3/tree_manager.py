"""Tree Manager for LATS algorithm.

Manages the Monte Carlo Tree Search tree structure, including
node relationships, path finding, and tree statistics.
"""

import logging

from haive.agents.reasoning_and_critique.lats.v3.models.tree_models import LATSNode

logger = logging.getLogger(__name__)


class TreeManager:
    """Manages the LATS tree structure and operations."""

    def __init__(self):
        """Initialize the tree manager."""
        self.nodes: dict[str, LATSNode] = {}
        self.root_id: str | None = None

    def add_node(self, node: LATSNode, parent_id: str | None = None) -> None:
        """Add a node to the tree.

        Args:
            node: Node to add
            parent_id: ID of parent node (None for root)
        """
        self.nodes[node.node_id] = node

        if parent_id is None:
            # This is the root
            if self.root_id is None:
                self.root_id = node.node_id
                logger.info(f"Set root node: {node.node_id}")
        # Add as child of parent
        elif parent_id in self.nodes:
            parent = self.nodes[parent_id]
            parent.children.append(node.node_id)
            node.parent_id = parent_id
            logger.debug(f"Added node {node.node_id} as child of {parent_id}")
        else:
            logger.error(f"Parent node {parent_id} not found")

    def get_node(self, node_id: str) -> LATSNode | None:
        """Get a node by ID.

        Args:
            node_id: Node ID to retrieve

        Returns:
            Node if found, None otherwise
        """
        return self.nodes.get(node_id)

    def get_leaf_nodes(self) -> dict[str, LATSNode]:
        """Get all leaf nodes (nodes with no children).

        Returns:
            Dictionary of leaf nodes by ID
        """
        leaves = {}
        for node_id, node in self.nodes.items():
            if node.is_leaf():
                leaves[node_id] = node
        return leaves

    def get_children(self, node_id: str) -> list[LATSNode]:
        """Get children of a node.

        Args:
            node_id: Parent node ID

        Returns:
            List of child nodes
        """
        node = self.get_node(node_id)
        if node is None:
            return []

        children = []
        for child_id in node.children:
            child = self.get_node(child_id)
            if child:
                children.append(child)
        return children

    def get_path_to_node(self, node_id: str) -> list[LATSNode]:
        """Get path from root to a node.

        Args:
            node_id: Target node ID

        Returns:
            List of nodes from root to target
        """
        path = []
        current_id = node_id

        while current_id is not None:
            node = self.get_node(current_id)
            if node is None:
                break
            path.append(node)
            current_id = node.parent_id

        path.reverse()  # Root to leaf order
        return path

    def get_best_path(self) -> list[LATSNode]:
        """Get the best path based on average rewards.

        Returns:
            List of nodes representing best path
        """
        if self.root_id is None:
            return []

        best_path = []
        current_id = self.root_id

        while current_id is not None:
            node = self.get_node(current_id)
            if node is None:
                break

            best_path.append(node)

            # Get best child based on average reward
            children = self.get_children(current_id)
            if not children:
                break

            best_child = max(children, key=lambda n: n.average_reward())
            current_id = best_child.node_id

        return best_path

    def backpropagate(self, node_id: str, reward: float) -> None:
        """Backpropagate reward up the tree.

        Args:
            node_id: Starting node ID
            reward: Reward value to propagate
        """
        current_id = node_id

        while current_id is not None:
            node = self.get_node(current_id)
            if node is None:
                break

            # Update node statistics
            node.visits += 1
            node.reward_sum += reward

            logger.debug(
                f"Backpropagated to {current_id}: "
                f"visits={node.visits}, avg_reward={node.average_reward():.3f}"
            )

            current_id = node.parent_id

    def get_tree_size(self) -> int:
        """Get total number of nodes in tree.

        Returns:
            Number of nodes
        """
        return len(self.nodes)

    def get_max_depth(self) -> int:
        """Get maximum depth of tree.

        Returns:
            Maximum depth
        """
        max_depth = 0
        for node in self.nodes.values():
            max_depth = max(max_depth, node.depth)
        return max_depth

    def get_tree_statistics(self) -> dict[str, Any]:
        """Get comprehensive tree statistics.

        Returns:
            Dictionary of tree statistics
        """
        if not self.nodes:
            return {
                "size": 0,
                "max_depth": 0,
                "num_leaves": 0,
                "avg_branching_factor": 0.0,
                "most_visited_path": [],
            }

        # Calculate statistics
        num_leaves = len(self.get_leaf_nodes())
        total_children = sum(len(node.children) for node in self.nodes.values())
        num_internal = len(self.nodes) - num_leaves
        avg_branching = total_children / max(num_internal, 1)

        # Find most visited path
        most_visited_leaf = max(
            self.get_leaf_nodes().values(), key=lambda n: n.visits, default=None
        )

        most_visited_path = []
        if most_visited_leaf:
            most_visited_path = self.get_path_to_node(most_visited_leaf.node_id)

        return {
            "size": self.get_tree_size(),
            "max_depth": self.get_max_depth(),
            "num_leaves": num_leaves,
            "avg_branching_factor": avg_branching,
            "most_visited_path": [n.action for n in most_visited_path],
        }

    def prune_tree(self, max_depth: int) -> int:
        """Prune tree to maximum depth.

        Args:
            max_depth: Maximum allowed depth

        Returns:
            Number of nodes pruned
        """
        nodes_to_remove = []

        for node_id, node in self.nodes.items():
            if node.depth > max_depth:
                nodes_to_remove.append(node_id)

        for node_id in nodes_to_remove:
            # Remove from parent's children list
            node = self.nodes[node_id]
            if node.parent_id and node.parent_id in self.nodes:
                parent = self.nodes[node.parent_id]
                parent.children.remove(node_id)

            # Remove node
            del self.nodes[node_id]

        logger.info(f"Pruned {len(nodes_to_remove)} nodes")
        return len(nodes_to_remove)

    def visualize_tree(self, max_depth: int | None = None) -> str:
        """Create a text visualization of the tree.

        Args:
            max_depth: Maximum depth to visualize

        Returns:
            String representation of tree
        """
        if self.root_id is None:
            return "Empty tree"

        lines = []
        self._visualize_node(self.root_id, lines, "", True, max_depth, 0)
        return "\n".join(lines)

    def _visualize_node(
        self,
        node_id: str,
        lines: list[str],
        prefix: str,
        is_last: bool,
        max_depth: int | None,
        current_depth: int,
    ) -> None:
        """Recursively visualize a node and its children.

        Args:
            node_id: Node to visualize
            lines: List to append lines to
            prefix: Prefix for tree structure
            is_last: Whether this is the last child
            max_depth: Maximum depth to show
            current_depth: Current depth in tree
        """
        if max_depth is not None and current_depth > max_depth:
            return

        node = self.get_node(node_id)
        if node is None:
            return

        # Create node representation
        connector = "└── " if is_last else "├── "
        node_str = (
            f"{prefix}{connector}{node.action} "
            f"(visits={node.visits}, avg={node.average_reward():.2f})"
        )
        lines.append(node_str)

        # Prepare prefix for children
        extension = "    " if is_last else "│   "
        child_prefix = prefix + extension

        # Visualize children
        children = self.get_children(node_id)
        for i, child in enumerate(children):
            is_last_child = i == len(children) - 1
            self._visualize_node(
                child.node_id,
                lines,
                child_prefix,
                is_last_child,
                max_depth,
                current_depth + 1,
            )
