"""Action Generator Agent for LATS v3 - Generates candidate actions."""

from haive.core.engine.aug_llm import AugLLMConfig

from haive.agents.reasoning_and_critique.lats.v3.models.action_models import (
    ActionGeneration,
    CandidateAction,
)
from haive.agents.reasoning_and_critique.lats.v3.models.tree_models import LATSNode
from haive.agents.simple.agent_v3 import SimpleAgentV3


class ActionGenerator:
    """Agent that generates candidate actions for a given node in LATS.

    This agent analyzes the current state and generates multiple candidate
    actions that could be taken, each with confidence scores and reasoning.
    Uses composition pattern to avoid Pydantic inheritance issues.
    """

    def __init__(
        self,
        name: str = "action_generator",
        num_candidates: int = 5,
        temperature: float = 0.7,
    ):
        """Initialize the ActionGenerator.

        Args:
            name: Name for the agent
            num_candidates: Target number of candidate actions to generate
            temperature: LLM temperature for generation diversity
        """
        self.name = name
        self.num_candidates = num_candidates
        self.temperature = temperature

        # Create the composed agent with structured output
        engine = AugLLMConfig(
            temperature=temperature,
            system_message=self._create_system_message(),
        )

        self.agent = SimpleAgentV3(
            name=name,
            engine=engine,
            structured_output_model=ActionGeneration,
        )

    def _create_system_message(self) -> str:
        """Create the system message for action generation."""
        return f"""You are an expert action generator for Monte Carlo Tree Search.

Your task is to generate {self.num_candidates} diverse candidate actions for a given state in a problem-solving tree.

Guidelines:
1. Generate diverse actions that explore different approaches
2. Each action should be concrete and executable
3. Provide clear reasoning for why each action might be good
4. Estimate confidence based on the action's likely success
5. Consider both safe and risky strategies
6. Think about what hasn't been tried yet
7. Balance immediate gains vs long-term strategy

Diversity is crucial - avoid generating similar actions."""

    def create_generation_prompt(
        self,
        current_node: LATSNode,
        problem_description: str,
        search_history: list[str] | None = None,
    ) -> str:
        """Create a prompt for action generation.

        Args:
            current_node: The node to generate actions for
            problem_description: Description of the problem being solved
            search_history: Optional list of previous actions taken

        Returns:
            Formatted prompt for action generation
        """
        prompt_parts = [
            f"Problem: {problem_description}",
            f"\nCurrent state: {current_node.state_description}",
            f"Action that led here: {current_node.action}",
            f"Depth in search tree: {current_node.depth}",
        ]

        if current_node.reflection_reasoning:
            prompt_parts.append(
                f"Previous reflection: {current_node.reflection_reasoning}"
            )

        if search_history:
            prompt_parts.append("\nSearch history (most recent first):")
            for i, action in enumerate(search_history[:5]):  # Limit to recent 5
                prompt_parts.append(f"  {i+1}. {action}")

        prompt_parts.extend(
            [
                f"\nGenerate {self.num_candidates} diverse candidate actions for the next step.",
                "Each action should explore a different approach or strategy.",
                "Consider what hasn't been tried and what might lead to success.",
            ]
        )

        return "\n".join(prompt_parts)

    async def generate_actions(
        self,
        current_node: LATSNode,
        problem_description: str,
        search_history: list[str] | None = None,
    ) -> ActionGeneration:
        """Generate candidate actions for a node.

        Args:
            current_node: The node to generate actions for
            problem_description: Description of the problem
            search_history: Optional search history

        Returns:
            ActionGeneration with candidate actions
        """
        prompt = self.create_generation_prompt(
            current_node, problem_description, search_history
        )

        # Use the composed agent's arun method
        result = await self.agent.arun(prompt)

        # Ensure we have the right number of candidates
        if len(result.candidate_actions) < self.num_candidates:
            # Pad with variations if needed
            while len(result.candidate_actions) < self.num_candidates:
                base_action = result.candidate_actions[-1]
                variation = CandidateAction(
                    action=f"{base_action.action} (variation)",
                    reasoning=f"Alternative approach to {base_action.action}",
                    expected_outcome="Exploring different execution of similar strategy",
                    confidence=base_action.confidence * 0.9,
                )
                result.candidate_actions.append(variation)

        return result

    def rank_actions(self, actions: list[CandidateAction]) -> list[CandidateAction]:
        """Rank actions by confidence score.

        Args:
            actions: List of candidate actions

        Returns:
            Actions sorted by confidence (highest first)
        """
        return sorted(actions, key=lambda a: a.confidence, reverse=True)

    def filter_actions(
        self,
        actions: list[CandidateAction],
        min_confidence: float = 0.3,
    ) -> list[CandidateAction]:
        """Filter actions by minimum confidence threshold.

        Args:
            actions: List of candidate actions
            min_confidence: Minimum confidence threshold

        Returns:
            Filtered list of actions above threshold
        """
        return [a for a in actions if a.confidence >= min_confidence]

    def get_action_diversity_score(self, actions: list[CandidateAction]) -> float:
        """Calculate diversity score for a set of actions.

        Args:
            actions: List of candidate actions

        Returns:
            Diversity score between 0 and 1
        """
        if len(actions) <= 1:
            return 0.0

        # Simple diversity based on action text differences
        action_texts = [a.action.lower() for a in actions]
        unique_words = set()
        total_words = 0

        for text in action_texts:
            words = text.split()
            unique_words.update(words)
            total_words += len(words)

        if total_words == 0:
            return 0.0

        # Diversity is ratio of unique words to total words
        return len(unique_words) / total_words
