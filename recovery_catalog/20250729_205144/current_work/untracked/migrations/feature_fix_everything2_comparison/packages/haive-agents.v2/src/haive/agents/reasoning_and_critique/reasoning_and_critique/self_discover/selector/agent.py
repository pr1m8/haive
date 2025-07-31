"""Self-Discover Selector Agent implementation."""

from haive.core.engine.aug_llm import AugLLMConfig

from haive.agents.simple import SimpleAgent

from .models import ModuleSelection
from .prompts import SELECTOR_PROMPT, SELECTOR_SYSTEM_MESSAGE


class SelectorAgent(SimpleAgent):
    r"""Agent that selects relevant reasoning modules for a given task.

    The Selector Agent is the first stage in the Self-Discover workflow.
    It analyzes the task and selects 3-5 reasoning modules from the available
    options that would be most effective for solving the problem.

    Attributes:
        name: Agent identifier (default: "selectof")
        engine: LLM configuration for the agent

    Example:
        >>> from haive.core.engine.aug_llm import AugLLMConfig
        >>>
        >>> config = AugLLMConfig(temperature=0.3)
        >>> selector = SelectorAgent(engine=config)
        >>>
        >>> result = await selector.arun({
        ...     "available_modules": "1. Critical thinking\\n2. Pattern recognition...",
        ...     "task_description": "Design a recommendation system"
        ... })
    """

    def __init__(self, name: str = "selector", engine: AugLLMConfig = None, **kwargs):
        """Initialize the Selector Agent.

        Args:
            name: Name for the agent
            engine: LLM configuration (if not provided, creates default)
            **kwargs: Additional arguments passed to SimpleAgent
        """
        if engine is None:
            engine = AugLLMConfig(
                temperature=0.3,
                max_tokens=1000,
                system_message=SELECTOR_SYSTEM_MESSAGE,
                prompt_template=SELECTOR_PROMPT,
                structured_output_model=ModuleSelection,
            )

        super().__init__(name=name, engine=engine, **kwargs)
