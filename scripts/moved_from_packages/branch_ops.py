"""Branch operations for the state graph system.

This module provides operations for adding, removing, and managing
branches (conditional routing) in a graph.
"""

import logging
import uuid
from collections.abc import Callable
from datetime import datetime
from typing import Any

from haive.core.graph.branches.branch import Branch
from haive.core.graph.branches.types import BranchMode, ComparisonType
from haive.core.graph.common.references import CallableReference
from haive.core.graph.state_graph.base.graph_base import GraphBase

# Set up logging
logger = logging.getLogger(__name__)


class BranchOperations:
    """Operations for managing branches in a graph.

    This class provides methods for adding, removing, updating,
    and querying branches in a graph.
    """

    @staticmethod
    def add_branch(
        graph: GraphBase,
        branch_or_name: Branch | str,
        source_node: str | None = None,
        condition: Any | None = None,
        routes: dict[bool | str, str] | None = None,
        branch_type: str | None = None,
        **kwargs,
    ) -> GraphBase:
        """Add a branch to the graph with flexible input options.

        Args:
            graph: Graph to add the branch to
            branch_or_name: Branch object or branch name
            source_node: Source node for the branch (required if branch_or_name is a string)
            condition: Condition function or key/value for evaluation
            routes: Mapping of condition results to target nodes
            branch_type: Type of branch (determined automatically if not provided)
            **kwargs: Additional parameters for branch creation

        Returns:
            Updated graph
        """
        if isinstance(branch_or_name, Branch):
            # Branch object
            branch = branch_or_name

            # Validate source node
            if branch.source_node is None:
                if source_node is None:
                    raise ValueError("Branch must have a source_node")
                branch.source_node = source_node

            if branch.source_node != "START" and branch.source_node not in graph.nodes:
                raise ValueError(
                    f"Source node '{branch.source_node}' not found in graph"
                )

            # Validate destination nodes
            for dest in branch.destinations.values():
                if dest != "END" and dest not in graph.nodes:
                    raise ValueError(f"Destination node '{dest}' not found in graph")

            # Validate default node
            if branch.default != "END" and branch.default not in graph.nodes:
                raise ValueError(f"Default node '{branch.default}' not found in graph")

            # Add the branch
            graph.branches[branch.id] = branch

        else:
            # String name
            branch_name = branch_or_name

            # Ensure source node is provided
            if not source_node:
                raise ValueError("source_node is required when adding a branch by name")

            # Validate source node
            if source_node != "START" and source_node not in graph.nodes:
                raise ValueError(f"Source node '{source_node}' not found in graph")

            # Create branch data
            branch_data = {"name": branch_name, "source_node": source_node, **kwargs}

            # Handle condition based on type
            if callable(condition):
                branch_data["function"] = condition
                branch_data["function_ref"] = CallableReference.from_callable(condition)
                branch_data["mode"] = BranchMode.FUNCTION
            elif isinstance(condition, tuple) and len(condition) >= 2:
                # Key-value branch: (key, value, [comparison])
                branch_data["key"] = condition[0]
                branch_data["value"] = condition[1]
                if len(condition) >= 3:
                    branch_data["comparison"] = condition[2]
                else:
                    branch_data["comparison"] = ComparisonType.EQUALS
            elif condition:
                # Direct condition value
                branch_data["key"] = kwargs.get("key")
                branch_data["value"] = condition
                branch_data["comparison"] = kwargs.get(
                    "comparison", ComparisonType.EQUALS
                )

            # Set routes
            if routes:
                branch_data["destinations"] = routes

            # Validate routes
            if "destinations" in branch_data:
                for dest in branch_data["destinations"].values():
                    if dest != "END" and dest not in graph.nodes:
                        raise ValueError(
                            f"Destination node '{dest}' not found in graph"
                        )

            # Create branch
            branch = Branch(**branch_data)
            graph.branches[branch.id] = branch

        logger.debug(f"Added branch '{branch.name}' from node '{branch.source_node}'")

        # Update graph timestamp
        graph.updated_at = datetime.now()

        return graph

    @staticmethod
    def add_conditional_edges(
        graph: GraphBase,
        source_node: str,
        condition: Callable,
        destinations: dict[Any, str],
        default: str = "END",
    ) -> GraphBase:
        """Add conditional edges from a source node based on a condition.

        Args:
            graph: Graph to add conditional edges to
            source_node: Source node name
            condition: Function that evaluates the state and returns a key for destinations
            destinations: Mapping of condition results to target nodes
            default: Default destination if no condition matches

        Returns:
            Updated graph
        """
        # Validate source node
        if source_node != "START" and source_node not in graph.nodes:
            raise ValueError(f"Source node '{source_node}' not found in graph")

        # Validate destination nodes
        for dest in destinations.values():
            if dest != "END" and dest not in graph.nodes:
                raise ValueError(f"Destination node '{dest}' not found in graph")

        # Generate a unique branch ID
        branch_id = str(uuid.uuid4())

        # Create the branch
        branch = Branch(
            id=branch_id,
            name=f"branch_{branch_id[:8]}",
            source_node=source_node,
            function=condition,
            function_ref=CallableReference.from_callable(condition),
            mode=BranchMode.FUNCTION,
            destinations=destinations,
            default=default,
        )

        # Add the branch to the graph
        graph.branches[branch_id] = branch

        logger.debug(
            f"Added conditional edges from '{source_node}' with {len(destinations)} destinations"
        )

        # Update graph timestamp
        graph.updated_at = datetime.now()

        return graph

    @staticmethod
    def add_function_branch(
        graph: GraphBase,
        source_node: str,
        condition: Callable,
        routes: dict[bool | str, str],
        default_route: str = "END",
        name: str | None = None,
    ) -> GraphBase:
        """Add a function-based branch.

        Args:
            graph: Graph to add the branch to
            source_node: Source node name
            condition: Condition function
            routes: Mapping of condition results to target nodes
            default_route: Default destination
            name: Optional branch name

        Returns:
            Updated graph
        """
        # Validate source node
        if source_node != "START" and source_node not in graph.nodes:
            raise ValueError(f"Source node '{source_node}' not found in graph")

        # Validate target nodes
        for dest in routes.values():
            if dest != "END" and dest not in graph.nodes:
                raise ValueError(f"Destination node '{dest}' not found in graph")

        # Validate default route
        if default_route != "END" and default_route not in graph.nodes:
            raise ValueError(f"Default node '{default_route}' not found in graph")

        # Create branch
        branch = Branch(
            id=str(uuid.uuid4()),
            name=name or f"func_branch_{uuid.uuid4().hex[:6]}",
            source_node=source_node,
            function=condition,
            function_ref=CallableReference.from_callable(condition),
            mode=BranchMode.FUNCTION,
            destinations=routes,
            default=default_route,
        )

        # Add to graph
        graph.branches[branch.id] = branch

        logger.debug(f"Added function branch '{branch.name}' from {source_node}")

        # Update graph timestamp
        graph.updated_at = datetime.now()

        return graph

    @staticmethod
    def add_key_value_branch(
        graph: GraphBase,
        source_node: str,
        key: str,
        value: Any,
        comparison: ComparisonType | str = ComparisonType.EQUALS,
        true_dest: str = "continue",
        false_dest: str = "END",
        name: str | None = None,
    ) -> GraphBase:
        """Add a key-value comparison branch.

        Args:
            graph: Graph to add the branch to
            source_node: Source node name
            key: State key to check
            value: Value to compare against
            comparison: Type of comparison
            true_dest: Destination if true
            false_dest: Destination if false
            name: Optional branch name

        Returns:
            Updated graph
        """
        # Validate source node
        if source_node != "START" and source_node not in graph.nodes:
            raise ValueError(f"Source node '{source_node}' not found in graph")

        # Validate target nodes
        if true_dest not in {"END", "continue"} and true_dest not in graph.nodes:
            raise ValueError(f"True destination node '{true_dest}' not found in graph")

        if false_dest != "END" and false_dest not in graph.nodes:
            raise ValueError(
                f"False destination node '{false_dest}' not found in graph"
            )

        # Create branch
        branch = Branch(
            id=str(uuid.uuid4()),
            name=name or f"kv_branch_{uuid.uuid4().hex[:6]}",
            source_node=source_node,
            key=key,
            value=value,
            comparison=comparison,
            destinations={True: true_dest, False: false_dest},
            default=false_dest,
            mode=BranchMode.DIRECT,
        )

        # Add to graph
        graph.branches[branch.id] = branch

        logger.debug(f"Added key-value branch '{branch.name}' from {source_node}")

        # Update graph timestamp
        graph.updated_at = datetime.now()

        return graph

    @staticmethod
    def remove_branch(graph: GraphBase, branch_id: str) -> GraphBase:
        """Remove a branch from the graph.

        Args:
            graph: Graph to remove the branch from
            branch_id: ID of the branch to remove

        Returns:
            Updated graph
        """
        if branch_id not in graph.branches:
            raise ValueError(f"Branch '{branch_id}' not found in graph")

        # Remove branch
        del graph.branches[branch_id]

        logger.debug(f"Removed branch '{branch_id}'")

        # Update graph timestamp
        graph.updated_at = datetime.now()

        return graph

    @staticmethod
    def update_branch(graph: GraphBase, branch_id: str, **updates) -> GraphBase:
        """Update a branch's properties.

        Args:
            graph: Graph containing the branch
            branch_id: ID of the branch to update
            **updates: Properties to update

        Returns:
            Updated graph
        """
        if branch_id not in graph.branches:
            raise ValueError(f"Branch '{branch_id}' not found in graph")

        # Get current branch
        branch = graph.branches[branch_id]

        # Apply updates
        for key, value in updates.items():
            if hasattr(branch, key):
                setattr(branch, key, value)

        # Validate connections if source/destinations were updated
        if "source_node" in updates:
            source = updates["source_node"]
            if source != "START" and source not in graph.nodes:
                raise ValueError(f"Updated source node '{source}' not found in graph")

        if "destinations" in updates:
            for dest in updates["destinations"].values():
                if dest != "END" and dest not in graph.nodes:
                    raise ValueError(
                        f"Updated destination node '{dest}' not found in graph"
                    )

        if "default" in updates:
            default = updates["default"]
            if default != "END" and default not in graph.nodes:
                raise ValueError(f"Updated default node '{default}' not found in graph")

        # Update graph timestamp
        graph.updated_at = datetime.now()

        return graph

    @staticmethod
    def replace_branch(
        graph: GraphBase, branch_id: str, new_branch: Branch
    ) -> GraphBase:
        """Replace a branch with a new one.

        Args:
            graph: Graph containing the branch
            branch_id: ID of the branch to replace
            new_branch: New branch to insert

        Returns:
            Updated graph
        """
        if branch_id not in graph.branches:
            raise ValueError(f"Branch '{branch_id}' not found in graph")

        # Validate new branch
        if (
            new_branch.source_node != "START"
            and new_branch.source_node not in graph.nodes
        ):
            raise ValueError(
                f"Source node '{new_branch.source_node}' not found in graph"
            )

        for dest in new_branch.destinations.values():
            if dest != "END" and dest not in graph.nodes:
                raise ValueError(f"Destination node '{dest}' not found in graph")

        if new_branch.default != "END" and new_branch.default not in graph.nodes:
            raise ValueError(f"Default node '{new_branch.default}' not found in graph")

        # Update the branch ID to match if needed
        if new_branch.id != branch_id:
            new_branch_copy = new_branch.model_copy(deep=True)
            new_branch_copy.id = branch_id
            graph.branches[branch_id] = new_branch_copy
        else:
            graph.branches[branch_id] = new_branch

        logger.debug(f"Replaced branch '{branch_id}'")

        # Update graph timestamp
        graph.updated_at = datetime.now()

        return graph

    @staticmethod
    def get_branches_for_node(graph: GraphBase, node_name: str) -> list[Branch]:
        """Get all branches with a given source node.

        Args:
            graph: Graph to query
            node_name: Name of the source node

        Returns:
            List of branch objects
        """
        return [
            branch
            for branch in graph.branches.values()
            if branch.source_node == node_name
        ]

    @staticmethod
    def get_branch(graph: GraphBase, branch_id: str) -> Branch | None:
        """Get a branch by ID.

        Args:
            graph: Graph to query
            branch_id: ID of the branch to retrieve

        Returns:
            Branch object if found, None otherwise
        """
        return graph.branches.get(branch_id)

    @staticmethod
    def get_branch_by_name(graph: GraphBase, name: str) -> Branch | None:
        """Get a branch by name.

        Args:
            graph: Graph to query
            name: Name of the branch to retrieve

        Returns:
            First matching branch or None if not found
        """
        for branch in graph.branches.values():
            if branch.name == name:
                return branch
        return None
