# src/haive/agents/selfdiscover/config.py

from datetime import datetime

from haive.core.engine.agent.agent import AgentConfig
from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.models.llm.base import AzureLLMConfig
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

from haive.agents.reasoning_and_critique.self_discover.engines import (
    create_selfdiscover_engines,
)
from haive.agents.reasoning_and_critique.self_discover.state import SelfDiscoverState


class SelfDiscoverAgentConfig(AgentConfig):
    """Configuration for a SelfDiscover agent.

    This configuration defines all parameters needed to create a SelfDiscover agent:
    - Engines for each stage of the reasoning process
    - State schema for tracking reasoning progress
    - Library of reasoning modules to use
    """

    # State schema
    state_schema: type[BaseModel] = Field(
        default=SelfDiscoverState, description="Schema for the agent state"
    )

    # Engines for each stage
    select_engine: AugLLMConfig = Field(
        default_factory=lambda: AugLLMConfig(
            name="default_select_engine",
            llm_config=AzureLLMConfig(model="gpt-4o", parameters={"temperature": 0.0}),
        ),
        description="Engine for the module selection stage",
    )

    adapt_engine: AugLLMConfig = Field(
        default_factory=lambda: AugLLMConfig(
            name="default_adapt_engine",
            llm_config=AzureLLMConfig(model="gpt-4o", parameters={"temperature": 0.0}),
        ),
        description="Engine for the module adaptation stage",
    )

    structure_engine: AugLLMConfig = Field(
        default_factory=lambda: AugLLMConfig(
            name="default_structure_engine",
            llm_config=AzureLLMConfig(model="gpt-4o", parameters={"temperature": 0.0}),
        ),
        description="Engine for the reasoning structure stage",
    )

    reasoning_engine: AugLLMConfig = Field(
        default_factory=lambda: AugLLMConfig(
            name="default_reasoning_engine",
            llm_config=AzureLLMConfig(model="gpt-4o", parameters={"temperature": 0.0}),
        ),
        description="Engine for the reasoning execution stage",
    )

    # Reasoning modules library
    reasoning_modules: list[str] = Field(
        default_factory=list, description="Library of reasoning modules to select from"
    )

    @classmethod
    def from_defaults(
        cls,
        model: str = "gpt-4o",
        temperature: float = 0.0,
        name: str | None = None,
        reasoning_modules: list[str] | None = None,
        select_prompt: str | ChatPromptTemplate | None = None,
        adapt_prompt: str | ChatPromptTemplate | None = None,
        structure_prompt: str | ChatPromptTemplate | None = None,
        reasoning_prompt: str | ChatPromptTemplate | None = None,
        **kwargs,
    ) -> "SelfDiscoverAgentConfig":
        """Create a SelfDiscoverAgentConfig with default settings.

        Args:
            model: Model name to use for all engines
            temperature: Temperature setting for all engines
            name: Optional name for the agent
            reasoning_modules: Optional list of reasoning modules
            select_prompt: Optional custom prompt for selection stage
            adapt_prompt: Optional custom prompt for adaptation stage
            structure_prompt: Optional custom prompt for structure stage
            reasoning_prompt: Optional custom prompt for reasoning stage
            **kwargs: Additional configuration parameters

        Returns:
            SelfDiscoverAgentConfig instance
        """
        # Include default reasoning modules if none provided
        if reasoning_modules is None:
            reasoning_modules = cls._get_default_reasoning_modules()

        # Create engines for each stage
        engines = create_selfdiscover_engines(
            model=model,
            temperature=temperature,
            select_prompt=select_prompt,
            adapt_prompt=adapt_prompt,
            structure_prompt=structure_prompt,
            reasoning_prompt=reasoning_prompt,
        )

        # Create the config
        return cls(
            name=name or f"self_discover_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            select_engine=engines["select"],
            adapt_engine=engines["adapt"],
            structure_engine=engines["structure"],
            reasoning_engine=engines["reasoning"],
            reasoning_modules=reasoning_modules,
            **kwargs,
        )

    @staticmethod
    def _get_default_reasoning_modules() -> list[str]:
        """Return a default list of reasoning modules."""
        return [
            "1. How could I devise an experiment to help solve that problem?",
            "2. Make a list of ideas for solving this problem, and apply them one by one to the problem to see if any progress can be made.",
            "3. How could I measure progress on this problem?",
            "4. How can I simplify the problem so that it is easier to solve?",
            "5. What are the key assumptions underlying this problem?",
            "6. What are the potential risks and drawbacks of each solution?",
            "7. What are the alternative perspectives or viewpoints on this problem?",
            "8. What are the long-term implications of this problem and its solutions?",
            "9. How can I break down this problem into smaller, more manageable parts?",
            "10. Critical Thinking: This style involves analyzing the problem from different perspectives, questioning assumptions, and evaluating the evidence or information available.",
            "11. Try creative thinking, generate innovative and out-of-the-box ideas to solve the problem.",
            "12. Seek input and collaboration from others to solve the problem.",
            "13. Use systems thinking: Consider the problem as part of a larger system and understanding the interconnectedness of various elements.",
            "14. Use Risk Analysis: Evaluate potential risks, uncertainties, and tradeoffs associated with different solutions.",
            "15. Use Reflective Thinking: Step back from the problem, take the time for introspection and self-reflection.",
            "16. What is the core issue or problem that needs to be addressed?",
            "17. What are the underlying causes or factors contributing to the problem?",
            "18. Are there any potential solutions or strategies that have been tried before?",
            "19. What are the potential obstacles or challenges that might arise in solving this problem?",
            "20. Are there any relevant data or information that can provide insights into the problem?",
            "21. Let's make a step by step plan and implement it with good notation and explanation.",
        ]
