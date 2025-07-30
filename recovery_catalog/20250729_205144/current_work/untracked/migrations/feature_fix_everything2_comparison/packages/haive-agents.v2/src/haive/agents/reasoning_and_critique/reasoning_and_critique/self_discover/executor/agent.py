"""Self-Discover Executor Agent implementation."""

from haive.core.engine.aug_llm import AugLLMConfig

from haive.agents.simple import SimpleAgent

from .models import ExecutionResult
from .prompts import EXECUTOR_PROMPT, EXECUTOR_SYSTEM_MESSAGE


class ExecutorAgent(SimpleAgent):
    """Agent that executes structured reasoning plans to solve tasks.

    The Executor Agent is the fourth and final stage in the Self-Discover workflow.
    It takes the structured reasoning plan and systematically executes it to
    arrive at a comprehensive solution for the original task.

    Attributes:
        name: Agent identifier (default: "executof")
        engine: LLM configuration for the agent

    Example:
        >>> from haive.core.engine.aug_llm import AugLLMConfig
        >>>
        >>> config = AugLLMConfig(temperature=0.5)
        >>> executor = ExecutorAgent(engine=config)
        >>>
        >>> result = await executor.arun({
        ...     "reasoning_structure": "Step 1: Analyze requirements...",
        ...     "task_description": "Design a recommendation system"
        ... })
    """

    def __init__(self, name: str = "executor", engine: AugLLMConfig = None, **kwargs):
        """Initialize the Executor Agent.

        Args:
            name: Name for the agent
            engine: LLM configuration (if not provided, creates default)
            **kwargs: Additional arguments passed to SimpleAgent
        """
        if engine is None:
            engine = AugLLMConfig(
                temperature=0.5,
                max_tokens=3000,
                system_message=EXECUTOR_SYSTEM_MESSAGE,
                prompt_template=EXECUTOR_PROMPT,
                structured_output_model=ExecutionResult,
            )

        super().__init__(name=name, engine=engine, **kwargs)
