"""Node Selector Agent for LATS algorithm.

This agent implements Upper Confidence Bound (UCB) selection logic to choose
the best node for expansion in the Monte Carlo Tree Search.
"""

from haive.core.engine.aug_llm import AugLLMConfig

from haive.agents.reasoning_and_critique.lats.v3.models.evaluation_models import (
    UCBSelection,
)
from haive.agents.reasoning_and_critique.lats.v3.models.tree_models import LATSNode
from haive.agents.simple.agent_v3 import SimpleAgentV3


class NodeSelector:
    """Agent that selects the best node for expansion using UCB selection."""

    def __init__(
        self,
        name: str = "node_selector",
        exploration_weight: float = 1.4,
        temperature: float = 0.3,
        engine: AugLLMConfig | None = None,
    ):
        """Initialize the node selector.

        Args:
            name: Agent name
            exploration_weight: UCB exploration weight (higher = more exploration)
            temperature: Temperature for LLM reasoning (lower = more consistent)
            engine: Optional engine configuration
        """
        self.name = name
        self.exploration_weight = exploration_weight

        if engine is None:
            engine = AugLLMConfig(
                temperature=temperature,
                structured_output_model=UCBSelection,
                system_message=f"""You are an expert at Monte Carlo Tree Search node selection.

Your task is to analyze a tree search state and select the best node for expansion using Upper Confidence Bound (UCB) logic.

UCB balances:
- EXPLOITATION: Nodes with high average rewards (successful paths)
- EXPLORATION: Nodes that haven't been visited much (unexplored potential)

The UCB formula is: UCB = average_reward + {exploration_weight} * sqrt(ln(parent_visits) / node_visits)

Guidelines:
1. Prioritize unvisited nodes (they have infinite UCB score)
2. Among visited nodes, balance high rewards vs low visit counts
3. Consider the strategic value of different search directions
4. Explain your selection reasoning clearly
5. Note what alternatives were considered

You will receive node information and must select the best one to expand.""",
            )

        # Use composition - create the underlying agent
        self.agent = SimpleAgentV3(name=name, engine=engine)

    @classmethod
    def create(
        cls,
        name: str = "node_selector",
        exploration_weight: float = 1.4,
        temperature: float = 0.3,
    ) -> "NodeSelector":
        """Create a NodeSelector with proper configuration."""
        return cls(
            name=name, exploration_weight=exploration_weight, temperature=temperature
        )

    def create_selection_prompt(
        self,
        nodes: dict[str, LATSNode],
        current_problem: str,
        search_context: str = "",
    ) -> str:
        """Create a prompt for node selection.

        Args:
            nodes: Dictionary of available nodes to select from
            current_problem: The problem being solved
            search_context: Additional context about the search state

        Returns:
            Formatted prompt for node selection
        """
        prompt_parts = [
            f"Problem being solved: {current_problem}",
        ]

        if search_context:
            prompt_parts.append(f"Search context: {search_context}")

        prompt_parts.append(f"Exploration weight: {self.exploration_weight}")
        prompt_parts.append("\nAvailable nodes for expansion:")

        # Calculate total visits for UCB calculation
        total_visits = sum(node.visits for node in nodes.values())

        for node_id, node in nodes.items():
            ucb_score = node.ucb_score(self.exploration_weight, total_visits)

            prompt_parts.append(
                f"""
Node ID: {node_id}
- Depth: {node.depth}
- Action: {node.action}
- State: {node.state_description}
- Visits: {node.visits}
- Average reward: {node.average_reward():.3f}
- UCB score: {ucb_score:.3f}
- Is leaf: {node.is_leaf()}
- Reflection score: {node.reflection_score:.3f}
"""
            )

        prompt_parts.append(
            """
Select the best node to expand next. Consider:
1. UCB scores (higher is better for selection)
2. Strategic value of different search directions
3. Balance between exploitation and exploration
4. Whether unvisited nodes should be prioritized"""
        )

        return "\n".join(prompt_parts)

    async def select_node(
        self,
        nodes: dict[str, LATSNode],
        current_problem: str,
        search_context: str = "",
    ) -> UCBSelection:
        """Select the best node for expansion.

        Args:
            nodes: Available nodes to select from
            current_problem: The problem being solved
            search_context: Additional search context

        Returns:
            UCBSelection with the chosen node and reasoning
        """
        prompt = self.create_selection_prompt(nodes, current_problem, search_context)

        # Use the composed agent's arun method
        result = await self.agent.arun(prompt)

        return result

    def calculate_ucb_scores(
        self, nodes: dict[str, LATSNode], parent_visits: int | None = None
    ) -> dict[str, float]:
        """Calculate UCB scores for all nodes (utility method).

        Args:
            nodes: Nodes to calculate scores for
            parent_visits: Parent node visits (defaults to sum of all visits)

        Returns:
            Dictionary mapping node_id to UCB score
        """
        if parent_visits is None:
            parent_visits = max(1, sum(node.visits for node in nodes.values()))

        ucb_scores = {}
        for node_id, node in nodes.items():
            ucb_scores[node_id] = node.ucb_score(self.exploration_weight, parent_visits)

        return ucb_scores


# Convenience function
def create_node_selector(
    exploration_weight: float = 1.4, temperature: float = 0.3
) -> NodeSelector:
    """Create a node selector with default settings.

    Args:
        exploration_weight: UCB exploration weight
        temperature: LLM temperature

    Returns:
        Configured NodeSelector
    """
    return NodeSelector(exploration_weight=exploration_weight, temperature=temperature)
