"""Reflection Evaluator Agent for LATS v3 - Evaluates and scores actions."""

from haive.core.engine.aug_llm import AugLLMConfig

from haive.agents.reasoning_and_critique.lats.v3.models.action_models import (
    CandidateAction,
)
from haive.agents.reasoning_and_critique.lats.v3.models.evaluation_models import (
    ReflectionEvaluation,
    ScoredAction,
)
from haive.agents.reasoning_and_critique.lats.v3.models.tree_models import LATSNode
from haive.agents.simple.agent_v3 import SimpleAgentV3


class ReflectionEvaluator:
    """Agent that reflects on and evaluates candidate actions.

    This agent analyzes candidate actions and provides scores based on
    their likelihood of success, strategic value, and problem-solving potential.
    Uses composition pattern to avoid Pydantic inheritance issues.
    """

    def __init__(
        self,
        name: str = "reflection_evaluator",
        temperature: float = 0.3,  # Lower temperature for more consistent evaluation
    ):
        """Initialize the ReflectionEvaluator.

        Args:
            name: Name for the agent
            temperature: LLM temperature for evaluation consistency
        """
        self.name = name
        self.temperature = temperature

        # Create the composed agent with structured output
        engine = AugLLMConfig(
            temperature=temperature,
            system_message=self._create_system_message(),
        )

        self.agent = SimpleAgentV3(
            name=name,
            engine=engine,
            structured_output_model=ReflectionEvaluation,
        )

    def _create_system_message(self) -> str:
        """Create the system message for reflection and evaluation."""
        return """You are an expert evaluator for Monte Carlo Tree Search actions.

Your task is to reflect on and evaluate candidate actions, scoring them based on:
1. Likelihood of success (0.0-1.0)
2. Strategic value for reaching the goal
3. Information gain potential
4. Risk vs reward balance
5. Efficiency of approach

Guidelines for scoring:
- 0.9-1.0: Excellent action with high success probability
- 0.7-0.8: Good action with strong potential
- 0.5-0.6: Average action with moderate potential
- 0.3-0.4: Below average action with risks
- 0.0-0.2: Poor action with low success chance

Consider:
- Past successes and failures (from reflection history)
- Strategic positioning toward the goal
- Balance between exploration and exploitation
- Potential for discovering new information
- Efficiency in reaching the solution"""

    def create_evaluation_prompt(
        self,
        current_node: LATSNode,
        candidate_actions: list[CandidateAction],
        problem_description: str,
        goal_description: str,
        reflection_history: list[str] | None = None,
    ) -> str:
        """Create a prompt for action evaluation.

        Args:
            current_node: Current node in the search tree
            candidate_actions: Actions to evaluate
            problem_description: Description of the problem
            goal_description: Description of the goal
            reflection_history: Optional previous reflections

        Returns:
            Formatted prompt for evaluation
        """
        prompt_parts = [
            f"Problem: {problem_description}",
            f"Goal: {goal_description}",
            f"\nCurrent state: {current_node.state_description}",
            f"Current position in search (depth {current_node.depth})",
        ]

        if current_node.visits > 0:
            prompt_parts.append(
                f"This node has been visited {current_node.visits} times with average reward {current_node.average_reward():.2f}"
            )

        if reflection_history:
            prompt_parts.append("\nPrevious reflections:")
            for i, reflection in enumerate(reflection_history[-3:]):  # Last 3
                prompt_parts.append(f"  {i+1}. {reflection}")

        prompt_parts.append("\nCandidate actions to evaluate:")
        for i, action in enumerate(candidate_actions, 1):
            prompt_parts.append(
                f"\n{i}. Action: {action.action}"
                f"\n   Reasoning: {action.reasoning}"
                f"\n   Expected outcome: {action.expected_outcome}"
                f"\n   Initial confidence: {action.confidence:.2f}"
            )

        prompt_parts.extend(
            [
                "\nEvaluate each action carefully, considering:",
                "- How likely is this action to succeed?",
                "- Does it move us closer to the goal?",
                "- What new information might we gain?",
                "- What are the risks vs rewards?",
                "- How efficient is this approach?",
            ]
        )

        return "\n".join(prompt_parts)

    async def evaluate_actions(
        self,
        current_node: LATSNode,
        candidate_actions: list[CandidateAction],
        problem_description: str,
        goal_description: str,
        reflection_history: list[str] | None = None,
    ) -> ReflectionEvaluation:
        """Evaluate and score candidate actions.

        Args:
            current_node: Current node in search tree
            candidate_actions: Actions to evaluate
            problem_description: Problem being solved
            goal_description: Goal to achieve
            reflection_history: Optional previous reflections

        Returns:
            ReflectionEvaluation with scored actions
        """
        prompt = self.create_evaluation_prompt(
            current_node,
            candidate_actions,
            problem_description,
            goal_description,
            reflection_history,
        )

        # Use the composed agent's arun method
        result = await self.agent.arun(prompt)

        return result

    def get_best_action(self, evaluation: ReflectionEvaluation) -> ScoredAction | None:
        """Get the highest-scored action from an evaluation.

        Args:
            evaluation: Reflection evaluation result

        Returns:
            Best scored action or None if no actions
        """
        if not evaluation.scored_actions:
            return None

        return max(evaluation.scored_actions, key=lambda a: a.score)

    def get_actions_above_threshold(
        self,
        evaluation: ReflectionEvaluation,
        threshold: float = 0.6,
    ) -> list[ScoredAction]:
        """Get all actions scoring above a threshold.

        Args:
            evaluation: Reflection evaluation result
            threshold: Minimum score threshold

        Returns:
            List of actions above threshold
        """
        return [
            action for action in evaluation.scored_actions if action.score >= threshold
        ]

    def should_backtrack(
        self,
        evaluation: ReflectionEvaluation,
        backtrack_threshold: float = 0.3,
    ) -> bool:
        """Determine if we should backtrack based on action scores.

        Args:
            evaluation: Reflection evaluation result
            backtrack_threshold: Score below which we should backtrack

        Returns:
            True if all actions are below threshold
        """
        if not evaluation.scored_actions:
            return True

        # If all actions score poorly, we should backtrack
        max_score = max(action.score for action in evaluation.scored_actions)
        return max_score < backtrack_threshold

    def get_reflection_summary(self, evaluation: ReflectionEvaluation) -> str:
        """Get a summary of the reflection for history tracking.

        Args:
            evaluation: Reflection evaluation result

        Returns:
            Summary string for reflection history
        """
        if not evaluation.scored_actions:
            return evaluation.overall_reflection

        best_action = self.get_best_action(evaluation)
        return (
            f"{evaluation.overall_reflection} "
            f"Best action: '{best_action.action}' (score: {best_action.score:.2f})"
        )
