"""Configuration for Language Agent Tree Search (LATS) agent."""

from agents.lats.state import TreeState
from haive.core.engine.agent.agent import AgentConfig
from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.tools.search_tools import tavily_search_tool
from langchain_core.tools import BaseTool, StructuredTool
from pydantic import BaseModel, Field


class LATSAgentConfig(AgentConfig):
    """Configuration for Language Agent Tree Search (LATS) agent.

    This agent implements a Monte Carlo Tree Search approach to generate
    high-quality responses through exploration and exploitation of different
    action trajectories.
    """

    # Core LATS parameters
    max_iterations: int = Field(
        default=5, description="Maximum number of search iterations"
    )

    max_depth: int = Field(default=5, description="Maximum depth of the search tree")

    exploration_weight: float = Field(
        default=1.0, description="Exploration weight for UCB calculation"
    )

    n_candidates: int = Field(
        default=5, description="Number of candidate actions to generate at each node"
    )

    # Component configurations
    reflection_engine: AugLLMConfig = Field(
        ..., description="Engine for reflection on candidate solutions"
    )

    action_engine: AugLLMConfig = Field(
        tools=[tavily_search_tool],
        description="Engine for generating candidate actions",
    )

    # Specific tools for this agent
    tools: list[BaseTool | StructuredTool] = Field(
        default_factory=list, description="Tools available to this agent"
    )

    # Custom state schema for LATS
    state_schema: type[BaseModel] = Field(
        default=TreeState, description="Schema for the LATS state"
    )

    input_schema_name: str | None = Field(
        default=None, description="Optional name of the input schema"
    )

    output_schema_name: str | None = Field(
        default=None, description="Optional name of the output schema"
    )

    @classmethod
    def from_llms(
        cls,
        reflection_llm: AugLLMConfig,
        action_llm: AugLLMConfig,
        tools: list[BaseTool | StructuredTool] | None = None,
        **kwargs
    ) -> "LATSAgentConfig":
        """Create a LATS agent configuration from LLM configs.

        Args:
            reflection_llm: LLM configuration for reflection
            action_llm: LLM configuration for action generation
            tools: Optional list of tools
            **kwargs: Additional configuration parameters

        Returns:
            LATSAgentConfig instance
        """
        return cls(
            reflection_engine=reflection_llm,
            action_engine=action_llm,
            tools=tools or [],
            **kwargs
        )
