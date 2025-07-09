import operator
from typing import Annotated, Any, Dict, List, Literal, Optional, Union

from haive.core.schema.prebuilt.messages_state import MessagesState
from langchain_core.messages import HumanMessage
from pydantic import Field, computed_field, model_validator

from .models import Reflection, TreeNode


def update_nodes(
    existing: Optional[Dict[str, TreeNode]] = None,
    updates: Optional[Dict[str, TreeNode]] = None,
) -> Dict[str, TreeNode]:
    """Custom reducer for tree nodes."""
    if existing is None:
        existing = {}
    if updates is None:
        return existing

    # Merge updates into existing
    result = existing.copy()
    result.update(updates)
    return result


class LATSState(MessagesState):
    """State for Language Agent Tree Search."""

    # Tree structure
    nodes: Annotated[Dict[str, TreeNode], update_nodes] = Field(
        default_factory=dict, description="All nodes in the search tree, keyed by ID"
    )
    root_id: Optional[str] = Field(default=None, description="Root node ID")

    # Search parameters
    max_depth: int = Field(default=5, description="Maximum tree depth")
    max_rollouts: int = Field(default=10, description="Maximum number of expansions")
    rollouts_completed: Annotated[int, operator.add] = Field(default=0)
    exploration_weight: float = Field(
        default=1.0, description="UCT exploration parameter"
    )
    n_candidates: int = Field(
        default=5, description="Number of candidates per expansion"
    )

    # Current search state
    current_node_id: Optional[str] = Field(
        default=None, description="Node being processed"
    )
    candidate_nodes: List[TreeNode] = Field(
        default_factory=list, description="Nodes to evaluate"
    )

    # Results
    best_solution_id: Optional[str] = Field(default=None)
    should_terminate: bool = Field(default=False)
    termination_reason: Optional[str] = None

    # Tool integration
    tools: List[Dict[str, Any]] = Field(default_factory=list)

    @computed_field
    @property
    def input_query(self) -> str:
        """Extract query from first human message."""
        for msg in self.messages:
            if isinstance(msg, HumanMessage):
                return msg.content
        return "No query found"

    @computed_field
    @property
    def current_trajectory(self) -> str:
        """Get trajectory to current node for prompts."""
        if not self.current_node_id or self.current_node_id not in self.nodes:
            return "Starting fresh - no trajectory yet."

        # Build trajectory from current node to root
        trajectory = []
        node_id = self.current_node_id

        while node_id:
            node = self.nodes.get(node_id)
            if not node:
                break

            # Add node's messages and reflection
            if node.messages:
                trajectory.append(f"Step {node.depth}:")
                for msg in node.messages:
                    trajectory.append(
                        f"  {msg.get('role', 'unknown')}: {msg.get('content', '')}"
                    )

            if node.reflection_text:
                trajectory.append(
                    f"  Reflection (score: {node.reflection_score:.1f}): {node.reflection_text}"
                )

            node_id = node.parent_id

        # Reverse to get root-to-current order
        trajectory.reverse()
        return "\n".join(trajectory) if trajectory else "Empty trajectory"

    @computed_field
    @property
    def tree_statistics(self) -> str:
        """Summary of tree search progress."""
        if not self.nodes:
            return "No tree built yet."

        total_nodes = len(self.nodes)
        solved_nodes = sum(1 for n in self.nodes.values() if n.is_solved)
        max_depth_reached = max((n.depth for n in self.nodes.values()), default=0)

        stats = [
            f"Tree Statistics:",
            f"  - Total nodes: {total_nodes}",
            f"  - Solved nodes: {solved_nodes}",
            f"  - Max depth reached: {max_depth_reached}/{self.max_depth}",
            f"  - Rollouts completed: {self.rollouts_completed}/{self.max_rollouts}",
        ]

        if self.best_solution_id and self.best_solution_id in self.nodes:
            best = self.nodes[self.best_solution_id]
            stats.append(f"  - Best solution score: {best.value:.3f}")

        return "\n".join(stats)

    @computed_field
    @property
    def should_continue_search(self) -> bool:
        """Determine if search should continue."""
        if self.should_terminate:
            return False
        if self.rollouts_completed >= self.max_rollouts:
            return False
        if any(n.is_solved and n.value > 0.9 for n in self.nodes.values()):
            return False
        return True

    def get_node(self, node_id: str) -> Optional[TreeNode]:
        """Get a node by ID."""
        return self.nodes.get(node_id)

    def get_best_leaf_to_expand(self) -> Optional[str]:
        """Find the best leaf node to expand using UCT."""
        if not self.root_id:
            return None

        # Start from root and traverse down using UCT
        current_id = self.root_id

        while current_id:
            current = self.nodes[current_id]

            # If leaf node, return it
            if not current.children_ids:
                return current_id

            # Select best child using UCT
            best_child_id = None
            best_uct = -float("inf")

            for child_id in current.children_ids:
                child = self.nodes.get(child_id)
                if child:
                    uct = child.uct_score(current.visits, self.exploration_weight)
                    if uct > best_uct:
                        best_uct = uct
                        best_child_id = child_id

            current_id = best_child_id

        return None
