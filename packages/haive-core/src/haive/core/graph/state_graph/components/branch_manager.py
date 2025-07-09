"""Branch management component for BaseGraph.

This module provides the BranchManager class that handles all conditional routing
and branch operations in the BaseGraph architecture.
"""

import uuid
from typing import TYPE_CHECKING, Any, Callable, Dict, List, Literal, Optional, Union

from langgraph.types import Send

from haive.core.graph.branches.branch import Branch
from haive.core.graph.branches.types import BranchMode, ComparisonType
from haive.core.graph.common.references import CallableReference
from haive.core.graph.state_graph.components.base_component import BaseGraphComponent
from haive.core.logging.rich_logger import get_logger

if TYPE_CHECKING:
    from haive.core.graph.state_graph.base_graph2 import BaseGraph, BranchResultType

logger = get_logger(__name__)


class BranchManager(BaseGraphComponent):
    """Manages all branch and conditional routing operations for BaseGraph.

    This component handles conditional edges, routing logic, and branch management
    following the single responsibility principle. It provides a clean interface
    for all conditional routing operations.

    Args:
        graph: Reference to the parent BaseGraph instance

    Attributes:
        component_name: Always "branch_manager"

    Example:
        Using the BranchManager::

            branch_manager = BranchManager(graph)
            branch_manager.initialize()

            # Add conditional routing
            def route_condition(state):
                return "success" if state.success else "failure"

            destinations = {"success": "success_node", "failure": "retry_node"}
            branch_manager.add_conditional_edges("decision", route_condition, destinations)

            # Add function-based branch
            branch_manager.add_function_branch("router", my_router_function)

            # Add key-value conditional branch
            branch_manager.add_key_value_branch("status_check", "status", {
                "ready": "process",
                "waiting": "wait",
                "error": "handle_error"
            })
    """

    component_name = "branch_manager"

    def __init__(self, graph: "BaseGraph") -> None:
        """Initialize BranchManager with graph reference."""
        super().__init__(graph)
        self._branch_counter = 0

    def initialize(self) -> None:
        """Initialize the branch manager."""
        super().initialize()
        self._branch_counter = 0
        logger.debug(f"BranchManager initialized for graph '{self.graph.name}'")

    def cleanup(self) -> None:
        """Clean up branch manager resources."""
        self._branch_counter = 0
        super().cleanup()
        logger.debug(f"BranchManager cleaned up for graph '{self.graph.name}'")

    def add_conditional_edges(
        self,
        source_node: str,
        condition: Union[Branch, Callable, Any],
        destinations: Optional[
            Union[str, List[str], Dict[Union[bool, str, int], str]]
        ] = None,
        default: Union[str, Literal["END"], None] = "END",
        create_missing_nodes: bool = False,
    ) -> "BaseGraph":
        """Add conditional edges from a source node.

        This is the main method for adding conditional routing to the graph.
        It supports various types of conditions and destination mappings.

        Args:
            source_node: Name of the source node
            condition: Condition function or Branch object
            destinations: Mapping of condition results to target nodes
            default: Default destination if condition doesn't match
            create_missing_nodes: Whether to create missing destination nodes

        Returns:
            Reference to parent graph for method chaining

        Raises:
            ValueError: If source node doesn't exist or destinations are invalid

        Example:
            Simple boolean routing::

                def is_complete(state):
                    return state.task_complete

                branch_manager.add_conditional_edges(
                    "processor",
                    is_complete,
                    {True: "finish", False: "continue"}
                )

            String-based routing::

                def get_next_action(state):
                    return state.next_action

                branch_manager.add_conditional_edges(
                    "decision",
                    get_next_action,
                    {"process": "processor", "validate": "validator", "finish": "END"}
                )
        """
        if not self._initialized:
            raise RuntimeError("BranchManager not initialized")

        # Validate source node exists
        if source_node not in self.graph.nodes:
            raise ValueError(f"Source node '{source_node}' not found in graph")

        # Create branch object if needed
        if not isinstance(condition, Branch):
            branch = self._create_branch_from_condition(
                condition, destinations, default
            )
        else:
            branch = condition

        # Generate unique branch ID
        branch_id = self._generate_branch_id(source_node)

        # Validate destinations
        if destinations:
            self._validate_destinations(destinations, create_missing_nodes)

        # Add branch to graph
        self.graph.branches[branch_id] = branch

        # Update graph metadata
        self.graph.updated_at = self._get_current_time()

        logger.debug(
            f"Added conditional edges from '{source_node}' with {len(destinations) if destinations else 0} destinations"
        )

        return self.graph

    def add_function_branch(
        self,
        source_node: str,
        function: Callable,
        default_destination: Union[str, Literal["END"]] = "END",
    ) -> "BaseGraph":
        """Add a function-based branch.

        Args:
            source_node: Name of the source node
            function: Function that returns routing decision
            default_destination: Default destination if function returns None

        Returns:
            Reference to parent graph for method chaining

        Example:
            Complex routing function::

                def complex_router(state):
                    if state.error_count > 3:
                        return "error_handler"
                    elif state.retry_count < 5:
                        return "retry"
                    else:
                        return "give_up"

                branch_manager.add_function_branch("processor", complex_router)
        """
        branch = Branch(
            source_node=source_node,
            mode=BranchMode.FUNCTION,
            function_ref=CallableReference.from_callable(function),
            default_destination=default_destination,
        )

        return self.add_conditional_edges(source_node, branch)

    def add_key_value_branch(
        self,
        source_node: str,
        key: str,
        value_map: Dict[Any, str],
        comparison_type: ComparisonType = ComparisonType.EQUALS,
        default_destination: Union[str, Literal["END"]] = "END",
    ) -> "BaseGraph":
        """Add a key-value conditional branch.

        Args:
            source_node: Name of the source node
            key: State key to evaluate
            value_map: Mapping of values to destination nodes
            comparison_type: Type of comparison to perform
            default_destination: Default destination for unmatched values

        Returns:
            Reference to parent graph for method chaining

        Example:
            Status-based routing::

                branch_manager.add_key_value_branch(
                    "status_checker",
                    "task_status",
                    {
                        "pending": "wait_node",
                        "ready": "process_node",
                        "complete": "finish_node",
                        "error": "error_handler"
                    }
                )
        """
        branch = Branch(
            source_node=source_node,
            mode=BranchMode.KEY_VALUE,
            state_key=key,
            value_mapping=value_map,
            comparison_type=comparison_type,
            default_destination=default_destination,
        )

        return self.add_conditional_edges(source_node, branch)

    def add_send_branch(
        self,
        source_node: str,
        send_function: Callable[[Any], Union[Send, List[Send]]],
        default_destination: Union[str, Literal["END"]] = "END",
    ) -> "BaseGraph":
        """Add a Send-based branch for parallel processing.

        Args:
            source_node: Name of the source node
            send_function: Function that returns Send objects
            default_destination: Default destination if no sends generated

        Returns:
            Reference to parent graph for method chaining

        Example:
            Parallel processing branch::

                def create_parallel_tasks(state):
                    sends = []
                    for task in state.tasks:
                        sends.append(Send("worker", {"task": task}))
                    return sends

                branch_manager.add_send_branch("distributor", create_parallel_tasks)
        """
        branch = Branch(
            source_node=source_node,
            mode=BranchMode.SEND,
            function_ref=CallableReference.from_callable(send_function),
            default_destination=default_destination,
        )

        return self.add_conditional_edges(source_node, branch)

    def remove_branch(self, branch_id: str) -> "BaseGraph":
        """Remove a branch from the graph.

        Args:
            branch_id: ID of the branch to remove

        Returns:
            Reference to parent graph for method chaining

        Raises:
            ValueError: If branch doesn't exist
        """
        if not self._initialized:
            raise RuntimeError("BranchManager not initialized")

        if branch_id not in self.graph.branches:
            raise ValueError(f"Branch '{branch_id}' not found in graph")

        del self.graph.branches[branch_id]

        # Update graph metadata
        self.graph.updated_at = self._get_current_time()

        logger.debug(f"Removed branch '{branch_id}' from graph '{self.graph.name}'")

        return self.graph

    def get_branch(self, branch_id: str) -> Optional[Branch]:
        """Get a branch by ID.

        Args:
            branch_id: ID of the branch to retrieve

        Returns:
            Branch object if found, None otherwise
        """
        return self.graph.branches.get(branch_id)

    def get_branches_for_node(self, node_name: str) -> List[Branch]:
        """Get all branches originating from a specific node.

        Args:
            node_name: Name of the source node

        Returns:
            List of branches from the specified node
        """
        return [
            branch
            for branch in self.graph.branches.values()
            if hasattr(branch, "source_node") and branch.source_node == node_name
        ]

    def update_branch(self, branch_id: str, **updates) -> "BaseGraph":
        """Update properties of an existing branch.

        Args:
            branch_id: ID of the branch to update
            **updates: Properties to update

        Returns:
            Reference to parent graph for method chaining

        Raises:
            ValueError: If branch doesn't exist
        """
        if not self._initialized:
            raise RuntimeError("BranchManager not initialized")

        if branch_id not in self.graph.branches:
            raise ValueError(f"Branch '{branch_id}' not found in graph")

        branch = self.graph.branches[branch_id]

        # Update branch properties
        for key, value in updates.items():
            if hasattr(branch, key):
                setattr(branch, key, value)

        # Update graph metadata
        self.graph.updated_at = self._get_current_time()

        logger.debug(f"Updated branch '{branch_id}' in graph '{self.graph.name}'")

        return self.graph

    def get_branch_count(self) -> int:
        """Get total number of branches in the graph."""
        return len(self.graph.branches)

    def get_branches_by_mode(self, mode: BranchMode) -> List[Branch]:
        """Get all branches of a specific mode.

        Args:
            mode: Branch mode to filter by

        Returns:
            List of branches with the specified mode
        """
        return [
            branch
            for branch in self.graph.branches.values()
            if hasattr(branch, "mode") and branch.mode == mode
        ]

    def validate_state(self) -> List[str]:
        """Validate the branch manager state.

        Returns:
            List of validation error messages
        """
        errors = super().validate_state()

        # Validate each branch
        for branch_id, branch in self.graph.branches.items():
            branch_errors = self._validate_branch(branch_id, branch)
            errors.extend(branch_errors)

        return errors

    def _create_branch_from_condition(
        self,
        condition: Callable,
        destinations: Optional[Union[str, List[str], Dict[Union[bool, str, int], str]]],
        default: Union[str, Literal["END"], None],
    ) -> Branch:
        """Create a Branch object from condition and destinations."""
        return Branch(
            mode=BranchMode.FUNCTION,
            function_ref=CallableReference.from_callable(condition),
            value_mapping=destinations if isinstance(destinations, dict) else None,
            default_destination=default or "END",
        )

    def _generate_branch_id(self, source_node: str) -> str:
        """Generate a unique branch ID."""
        self._branch_counter += 1
        return f"{source_node}_branch_{self._branch_counter}_{uuid.uuid4().hex[:8]}"

    def _validate_destinations(self, destinations: Any, create_missing: bool) -> None:
        """Validate that destination nodes exist or can be created."""
        if isinstance(destinations, dict):
            dest_nodes = set(destinations.values())
        elif isinstance(destinations, list):
            dest_nodes = set(destinations)
        elif isinstance(destinations, str):
            dest_nodes = {destinations}
        else:
            return  # No validation needed for other types

        # Check each destination
        for dest in dest_nodes:
            if dest in {"END", "__end__", "end"}:
                continue  # Special nodes are always valid

            if dest not in self.graph.nodes:
                if create_missing:
                    # Create a placeholder node
                    self.graph.nodes[dest] = self._create_placeholder_node(dest)
                    logger.debug(
                        f"Created placeholder node '{dest}' for branch destination"
                    )
                else:
                    raise ValueError(f"Destination node '{dest}' not found in graph")

    def _create_placeholder_node(self, name: str):
        """Create a placeholder node for missing destinations."""
        # Import here to avoid circular imports
        from haive.core.graph.common.types import NodeType
        from haive.core.graph.state_graph.base_graph2 import Node

        return Node(
            id=str(uuid.uuid4()),
            name=name,
            node_type=NodeType.PLACEHOLDER,
            metadata={"created_by": "branch_manager", "placeholder": True},
        )

    def _validate_branch(self, branch_id: str, branch: Branch) -> List[str]:
        """Validate a single branch."""
        errors = []

        # Check source node exists
        if (
            hasattr(branch, "source_node")
            and branch.source_node not in self.graph.nodes
        ):
            errors.append(
                f"Branch '{branch_id}' references non-existent source node '{branch.source_node}'"
            )

        # Check function reference is valid
        if hasattr(branch, "function_ref") and branch.function_ref:
            try:
                branch.function_ref.get_callable()
            except Exception as e:
                errors.append(
                    f"Branch '{branch_id}' has invalid function reference: {e}"
                )

        # Check value mapping destinations
        if hasattr(branch, "value_mapping") and branch.value_mapping:
            for value, destination in branch.value_mapping.items():
                if destination not in self.graph.nodes and destination not in {
                    "END",
                    "__end__",
                    "end",
                }:
                    errors.append(
                        f"Branch '{branch_id}' maps to non-existent destination '{destination}'"
                    )

        return errors

    def _get_current_time(self):
        """Get current timestamp."""
        from datetime import datetime

        return datetime.now()

    def get_component_info(self) -> Dict[str, Any]:
        """Get detailed component information."""
        base_info = super().get_component_info()

        # Calculate branch statistics by mode
        mode_counts = {}
        for mode in BranchMode:
            mode_counts[mode.value] = len(self.get_branches_by_mode(mode))

        base_info.update(
            {
                "total_branches": self.get_branch_count(),
                "branch_modes": mode_counts,
                "branch_counter": self._branch_counter,
            }
        )

        return base_info
