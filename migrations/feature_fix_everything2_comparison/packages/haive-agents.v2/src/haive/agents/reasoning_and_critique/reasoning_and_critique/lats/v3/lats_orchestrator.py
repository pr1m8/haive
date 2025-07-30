"""LATS Orchestrator using EnhancedMultiAgentV4.

This orchestrator coordinates the LATS algorithm components using the same
multi-agent pattern as TOT and Self-Discover implementations.
"""

import logging
from typing import Any

from haive.agents.multi.enhanced_multi_agent_v4 import EnhancedMultiAgentV4
from haive.agents.reasoning_and_critique.lats.v3.agents.action_generator import (
    ActionGenerator,
)
from haive.agents.reasoning_and_critique.lats.v3.agents.node_selector import (
    NodeSelector,
)
from haive.agents.reasoning_and_critique.lats.v3.agents.reflection_evaluator import (
    ReflectionEvaluator,
)
from haive.agents.reasoning_and_critique.lats.v3.models.tree_models import LATSNode
from haive.agents.reasoning_and_critique.lats.v3.tree_manager import TreeManager

logger = logging.getLogger(__name__)


class LATSOrchestrator(EnhancedMultiAgentV4):
    """LATS Orchestrator using EnhancedMultiAgentV4 pattern.

    This orchestrator manages the LATS Monte Carlo Tree Search algorithm
    by coordinating three specialized agents:
    1. NodeSelector - Selects nodes using UCB
    2. ActionGenerator - Generates candidate actions
    3. ReflectionEvaluator - Evaluates and scores actions

    Similar to TOT and Self-Discover implementations, this uses the
    EnhancedMultiAgentV4 base class for coordination.
    """

    def __init__(
        self,
        name: str = "lats_orchestrator",
        problem: str = "",
        goal: str = "",
        max_iterations: int = 10,
        max_depth: int = 5,
        exploration_weight: float = 1.4,
        num_candidates: int = 3,
        **kwargs,
    ):
        """Initialize LATS Orchestrator.

        Args:
            name: Name of the orchestrator
            problem: Problem description to solve
            goal: Goal to achieve
            max_iterations: Maximum MCTS iterations
            max_depth: Maximum tree depth
            exploration_weight: UCB exploration parameter
            num_candidates: Number of action candidates to generate
            **kwargs: Additional arguments for EnhancedMultiAgentV4
        """
        self.problem = problem
        self.goal = goal
        self.max_iterations = max_iterations
        self.max_depth = max_depth
        self.exploration_weight = exploration_weight
        self.num_candidates = num_candidates

        # Initialize the tree manager
        self.tree_manager = TreeManager()

        # Create the three LATS agents
        self.node_selector = NodeSelector(
            name="lats_node_selector",
            exploration_weight=exploration_weight,
            temperature=0.3,
        )

        self.action_generator = ActionGenerator(
            name="lats_action_generator", num_candidates=num_candidates, temperature=0.7
        )

        self.reflection_evaluator = ReflectionEvaluator(
            name="lats_reflection_evaluator", temperature=0.5
        )

        # Initialize with the agents in sequence
        super().__init__(
            name=name,
            agents=[
                self.node_selector,
                self.action_generator,
                self.reflection_evaluator,
            ],
            execution_mode="sequential",  # LATS follows sequential steps
            build_mode="auto",  # Build graph automatically
            **kwargs,
        )

    async def run_mcts_iteration(self, iteration: int) -> dict[str, Any]:
        """Run one iteration of Monte Carlo Tree Search.

        Args:
            iteration: Current iteration number

        Returns:
            Dictionary with iteration results
        """
        logger.info(f"[{self.name}] Starting MCTS iteration {iteration}")

        # Step 1: Select node using UCB
        nodes = self.tree_manager.get_leaf_nodes()
        if not nodes:
            # Initialize with root if no nodes exist
            root = LATSNode(action="Start", state_description="Initial state", depth=0)
            self.tree_manager.add_node(root)
            nodes = {root.node_id: root}

        # Use the orchestrator to run the pipeline
        state = {
            "messages": [],
            "nodes": nodes,
            "problem": self.problem,
            "goal": self.goal,
            "iteration": iteration,
        }

        # Run the multi-agent pipeline
        result = await self.arun(state)

        # Extract results from the pipeline
        # The result should contain the selected node, generated actions,
        # and evaluation scores

        return result

    async def solve(self) -> dict[str, Any]:
        """Run the complete LATS algorithm to solve the problem.

        Returns:
            Dictionary with solution and search statistics
        """
        logger.info(f"[{self.name}] Starting LATS search for: {self.problem}")

        best_solution = None
        search_history = []

        for i in range(self.max_iterations):
            # Run one MCTS iteration
            iteration_result = await self.run_mcts_iteration(i)
            search_history.append(iteration_result)

            # Check if we found a solution
            if self._is_solution(iteration_result):
                best_solution = iteration_result
                logger.info(f"[{self.name}] Found solution at iteration {i}")
                break

            # Check depth limit
            if self.tree_manager.get_max_depth() >= self.max_depth:
                logger.warning(f"[{self.name}] Reached max depth {self.max_depth}")
                break

        # Get the best path from the tree
        best_path = self.tree_manager.get_best_path()

        return {
            "solution": best_solution,
            "best_path": best_path,
            "iterations": len(search_history),
            "search_history": search_history,
            "tree_size": self.tree_manager.get_tree_size(),
            "max_depth_reached": self.tree_manager.get_max_depth(),
        }

    def _is_solution(self, result: dict[str, Any]) -> bool:
        """Check if the result contains a valid solution.

        Args:
            result: Iteration result

        Returns:
            True if solution found
        """
        # Check if evaluation indicates solution
        if "evaluation" in result:
            eval_data = result["evaluation"]
            if hasattr(eval_data, "termination_recommendation"):
                return "terminate" in eval_data.termination_recommendation.lower()
        return False

    def add_custom_node_processor(self, processor: Any) -> None:
        """Add custom node processing logic.

        Args:
            processor: Custom processor for nodes
        """
        # This allows extending LATS with custom logic
        logger.info(f"[{self.name}] Added custom node processor")


# Factory function for easy creation
def create_lats_orchestrator(
    problem: str, goal: str, name: str = "lats_solver", **kwargs
) -> LATSOrchestrator:
    """Create a LATS orchestrator for solving a problem.

    Args:
        problem: Problem description
        goal: Goal to achieve
        name: Name for the orchestrator
        **kwargs: Additional configuration

    Returns:
        Configured LATSOrchestrator
    """
    return LATSOrchestrator(name=name, problem=problem, goal=goal, **kwargs)
