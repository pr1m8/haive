"""Self-Discover Structurer Agent implementation."""

from __future__ import annotations

from haive.agents.simple import SimpleAgent
from haive.core.engine.aug_llm import AugLLMConfig

from migrations.feature_fix_everything2_comparison.packages.haive-agents.v2.src.haive.agents.reasoning_and_critique.reasoning_and_critique.self_discover.structurer.models import ReasoningStructure
from migrations.feature_fix_everything2_comparison.packages.haive-agents.v2.src.haive.agents.reasoning_and_critique.reasoning_and_critique.self_discover.structurer.prompts import STRUCTURER_PROMPT, STRUCTURER_SYSTEM_MESSAGE


class StructurerAgent(SimpleAgent):
    """Agent that creates structured reasoning plans from adapted modules.

    The Structurer Agent is the third stage in the Self-Discover workflow.
    It takes the adapted reasoning modules and organizes them into a coherent,
    step-by-step plan for solving the specific task.

    Attributes:
        name: Agent identifier (default: "structuref")
        engine: LLM configuration for the agent

    Example:
        >>> from haive.core.engine.aug_llm import AugLLMConfig
        >>>
        >>> config = AugLLMConfig(temperature=0.2)
        >>> structurer = StructurerAgent(engine=config)
        >>>
        >>> result = await structurer.arun({
        ...     "adapted_modules": "1. Critical analysis: Look for biases...",
        ...     "task_description": "Design a recommendation system"
        ... })
    """

    def __init__(self,
                 name: str = "structurer",
                 engine: AugLLMConfig = None,
                 **kwargs):
        """Initialize the Structurer Agent.

        Args:
            name: Name for the agent
            engine: LLM configuration (if not provided, creates default)
            **kwargs: Additional arguments passed to SimpleAgent
        """
        if engine is None:
            engine = AugLLMConfig(
                temperature=0.2,
                max_tokens=2000,
                system_message=STRUCTURER_SYSTEM_MESSAGE,
                prompt_template=STRUCTURER_PROMPT,
                structured_output_model=ReasoningStructure,
            )

        super().__init__(name=name, engine=engine, **kwargs)
