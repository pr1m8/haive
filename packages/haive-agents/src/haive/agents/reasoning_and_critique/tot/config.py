"""Configuration for the Tree of Thoughts agent.

This module defines the configuration schema for the ToT agent,
including engine configurations, algorithm parameters, and state schema.
"""

from typing import TypeVar

from haive.core.engine.agent.agent import AgentConfig
from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.models.llm.base import AzureLLMConfig
from pydantic import BaseModel, ConfigDict, Field, create_model

from haive.agents.reasoning_and_critique.tot.state import TOTInput, TOTOutput, TOTState

# Generic type variable for solution content
T = TypeVar("T")


class TOTAgentConfig(AgentConfig):
    """Configuration for the Tree of Thoughts agent.

    This configuration specifies the LLM engines used for generation and scoring,
    as well as the parameters for the search algorithm.
    """

    # Engine configurations
    engines: dict[str, AugLLMConfig] = Field(
        default_factory=lambda: {
            # Generator engine for generating candidate solutions
            "generator": AugLLMConfig(
                name="candidate_generator",
                description="Generates candidate solutions for the problem",
                llm_config=AzureLLMConfig(
                    model="gpt-4o", parameters={"temperature": 0.7, "max_tokens": 1500}
                ),
            ),
            # Evaluator engine for scoring solutions
            "evaluator": AugLLMConfig(
                name="solution_evaluator",
                description="Evaluates candidate solutions",
                llm_config=AzureLLMConfig(
                    model="gpt-4o", parameters={"temperature": 0.1, "max_tokens": 500}
                ),
            ),
        },
        description="Engine configurations for the ToT agent",
    )

    # Schema definitions
    state_schema: type[TOTState] = Field(default=TOTState)
    input_schema: type[TOTInput] = Field(default=TOTInput)
    output_schema: type[TOTOutput] = Field(default=TOTOutput)

    # Structured output configuration
    use_structured_output: bool = Field(
        default=True,
        description="Whether to use structured output parsing with Pydantic models",
    )

    generator_output_model: type[BaseModel] | None = Field(
        default=None,
        description="Pydantic model for generator structured output (if None, will use default)",
    )

    evaluator_output_model: type[BaseModel] | None = Field(
        default=None,
        description="Pydantic model for evaluator structured output (if None, will use default)",
    )

    # Search algorithm parameters
    max_depth: int = Field(
        default=3, description="Maximum depth of the Tree of Thoughts search"
    )

    beam_width: int = Field(
        default=3,
        description="Number of candidates to retain at each level (beam width)",
    )

    expansion_count: int = Field(
        default=5,
        description="Number of candidate solutions to generate in each expansion step",
    )

    threshold: float = Field(
        default=0.9, description="Score threshold for accepting a solution"
    )

    # Node names for the graph
    generator_node: str = Field(
        default="generate_candidates",
        description="Name of the node that generates candidates",
    )

    evaluator_node: str = Field(
        default="score_candidates",
        description="Name of the node that scores candidates",
    )

    selector_node: str = Field(
        default="select_best",
        description="Name of the node that selects the best candidates",
    )

    # Parallelization settings
    parallel_evaluation: bool = Field(
        default=True, description="Whether to evaluate candidates in parallel"
    )

    parallel_expansion: bool = Field(
        default=True,
        description="Whether to expand multiple candidates in parallel using beam search",
    )

    # Content type configuration
    content_type_name: str = Field(
        default="string",
        description="Name of the content type (string, equation, etc.)",
    )

    # Pydantic configuration
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
    )

    def get_engine(self, engine_key: str) -> AugLLMConfig:
        """Get an engine by key from the engines dictionary.

        Args:
            engine_key: Key of the engine to retrieve

        Returns:
            The requested engine configuration

        Raises:
            KeyError: If the engine key is not found
        """
        if engine_key not in self.engines:
            raise KeyError(f"Engine '{engine_key}' not found in configuration")
        return self.engines[engine_key]

    @classmethod
    def create_for_problem_type(
        cls, content_type: str = "string", **kwargs
    ) -> "TOTAgentConfig":
        """Create a TOT agent configuration specialized for a specific problem type.

        Args:
            content_type: Type of content ('string', 'equation', etc.)
            **kwargs: Additional configuration parameters

        Returns:
            Configured TOTAgentConfig
        """
        config = cls(**kwargs)
        config.content_type_name = content_type

        # Set up custom schemas based on content type
        if content_type == "equation":
            # Import here to avoid circular imports
            from haive.agents.reasoning_and_critique.tot.models import (
                Equation,
                EquationGeneration,
            )

            # Custom state schemas for equations
            config.generator_output_model = EquationGeneration

            # Create custom state schema derived from TOTState but with Equation content
            EquationState = create_model(
                "EquationState",
                __base__=TOTState[Equation],
            )
            config.state_schema = EquationState

        return config
