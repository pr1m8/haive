"""Config configuration module.

This module provides config functionality for the Haive framework.

Classes:
    ToTAgentConfig: ToTAgentConfig implementation.

Functions:
    from_scratch: From Scratch functionality.
"""

from collections.abc import Callable
from datetime import datetime

from agents.tot.modular.state import ToTState
from haive.core.engine.agent.agent import AgentConfig
from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.models.llm.base import AzureLLMConfig
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field


class ToTAgentConfig(AgentConfig):
    """Configuration for a Tree of Thoughts agent.

    Tree of Thoughts implements a search algorithm for complex problems by:
    1. Generating multiple candidate solutions
    2. Evaluating those candidates
    3. Pruning to retain only the best candidates
    4. Repeating until a satisfactory solution is found
    """

    # State schema
    state_schema: type[BaseModel] = Field(
        default=ToTState, description="Schema for the agent state"
    )

    # Node names
    expand_node_name: str = Field(
        default="expand", description="Name for the expansion node"
    )

    score_node_name: str = Field(
        default="score", description="Name for the scoring node"
    )

    prune_node_name: str = Field(
        default="prune", description="Name for the pruning node"
    )

    # ToT parameters
    max_depth: int = Field(default=5, description="Maximum search depth")

    threshold: float = Field(default=0.9, description="Score threshold for success")

    beam_size: int = Field(
        default=3, description="Number of candidates to keep after pruning"
    )

    candidates_per_expansion: int = Field(
        default=3, description="Number of candidates to generate in each expansion"
    )

    # LLM configurations
    expand_llm_config: AugLLMConfig = Field(
        default_factory=lambda: AugLLMConfig(),
        description="LLM configuration for candidate expansion",
    )

    score_llm_config: AugLLMConfig | None = Field(
        default=None,
        description="LLM configuration for candidate scoring (if not provided, a function must be used)",
    )

    # Alternative function-based scoring
    score_function: Callable | None = Field(
        default=None,
        description="Function to score candidates. Takes (problem, candidate) and returns a score.",
    )

    # Customization
    visualize: bool = Field(
        default=True, description="Whether to visualize the ToT graph"
    )

    @classmethod
    def from_scratch(
        cls,
        model: str = "gpt-4o",
        temperature: float = 0.7,
        system_prompt: str = "You are a helpful assistant solving a complex problem step by step.",
        expand_prompt: ChatPromptTemplate | None = None,
        score_prompt: ChatPromptTemplate | None = None,
        name: str | None = None,
        **kwargs,
    ) -> "ToTAgentConfig":
        """Create a ToTAgentConfig from scratch.

        Args:
            model: Model name to use
            temperature: Temperature for generation
            system_prompt: System prompt for the agent
            expand_prompt: Optional specific prompt for expansion
            score_prompt: Optional specific prompt for scoring
            name: Optional agent name
            **kwargs: Additional kwargs for the config

        Returns:
            ToTAgentConfig instance
        """
        # Create default expand prompt if not provided
        if expand_prompt is None:
            expand_prompt = ChatPromptTemplate.from_messages(
                [
                    ("system", system_prompt),
                    (
                        "system",
                        "Generate {candidates_per_expansion} different approaches to solve this problem. Be creative and diverse in your thinking.",
                    ),
                    ("user", "Problem: {problem}"),
                    ("user", "Previous attempt: {seed}" if "seed" in kwargs else ""),
                ]
            )

        # Create default score prompt if not provided and no score function
        if score_prompt is None and "score_function" not in kwargs:
            score_prompt = ChatPromptTemplate.from_messages(
                [
                    (
                        "system",
                        "Rate the following solution attempt on a scale of 0.0 to 1.0.",
                    ),
                    ("system", "Provide feedback on the reasoning and accuracy."),
                    ("user", "Problem: {problem}"),
                    ("user", "Solution attempt: {candidate}"),
                ]
            )

        # Set up LLM configs
        llm_config = AzureLLMConfig(
            model=model, parameters={"temperature": temperature}
        )

        # Create expand LLM config
        expand_llm = AugLLMConfig(
            name="tot_expand_llm", llm_config=llm_config, prompt_template=expand_prompt
        )

        # Create score LLM config if needed
        score_llm = None
        if score_prompt is not None and "score_function" not in kwargs:
            score_llm = AugLLMConfig(
                name="tot_score_llm",
                llm_config=llm_config,
                prompt_template=score_prompt,
            )

        # Create and return the config
        return cls(
            name=name or f"tot_agent_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            expand_llm_config=expand_llm,
            score_llm_config=score_llm,
            **kwargs,
        )
