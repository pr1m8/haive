"""Self-Discover Adapter Agent implementation."""

from haive.core.engine.aug_llm import AugLLMConfig

from haive.agents.simple import SimpleAgent

from .models import AdaptedModules
from .prompts import ADAPTER_PROMPT, ADAPTER_SYSTEM_MESSAGE


class AdapterAgent(SimpleAgent):
    """Agent that adapts selected reasoning modules for specific tasks.

    The Adapter Agent is the second stage in the Self-Discover workflow.
    It takes the reasoning modules selected by the Selector Agent and adapts
    them to be concrete and actionable for the specific task at hand.

    Attributes:
        name: Agent identifier (default: "adaptef")
        engine: LLM configuration for the agent

    Example:
        >>> from haive.core.engine.aug_llm import AugLLMConfig
        >>>
        >>> config = AugLLMConfig(temperature=0.4)
        >>> adapter = AdapterAgent(engine=config)
        >>>
        >>> result = await adapter.arun({
        ...     "selected_modules": "1. Critical thinking: Analyze assumptions...",
        ...     "task_description": "Design a recommendation system"
        ... })
    """

    def __init__(self, name: str = "adapter", engine: AugLLMConfig = None, **kwargs):
        """Initialize the Adapter Agent.

        Args:
            name: Name for the agent
            engine: LLM configuration (if not provided, creates default)
            **kwargs: Additional arguments passed to SimpleAgent
        """
        if engine is None:
            engine = AugLLMConfig(
                temperature=0.4,
                max_tokens=1500,
                system_message=ADAPTER_SYSTEM_MESSAGE,
                prompt_template=ADAPTER_PROMPT,
                structured_output_model=AdaptedModules,
            )

        super().__init__(name=name, engine=engine, **kwargs)
