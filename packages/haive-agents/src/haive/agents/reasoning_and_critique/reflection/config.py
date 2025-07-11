"""Configuration for the Reflection Agent."""

import logging

from agents.reflection.models import ReflectionOutput, ReflectionResult
from agents.reflection.state import ReflectionAgentState
from agents.simple.config import SimpleAgentConfig
from haive.core.engine.aug_llm import AugLLMConfig
from pydantic import BaseModel, Field

# Setup logging
logger = logging.getLogger(__name__)


class ReflectionConfig(BaseModel):
    """Configuration specific to the reflection mechanism."""

    enabled: bool = Field(default=True, description="Whether reflection is enabled")

    reflection_llm: AugLLMConfig | None = Field(
        default=None,
        description="LLM to use for reflection. If None, uses the same LLM as the main agent.",
    )

    max_reflection_rounds: int = Field(
        default=3, description="Maximum number of reflection rounds"
    )

    reflection_prompt_template: str = Field(
        default=(
            "You are a critical but constructive reviewer. Your task is to critique the response to the following request.\n\n"
            "Original request: {original_request}\n\n"
            "Response: {response}\n\n"
            "Provide specific, actionable feedback focusing on:\n"
            "1. Missing information or reasoning\n"
            "2. Superfluous or irrelevant content\n"
            "3. Overall quality of the response\n\n"
            "Format your critique as follows:\n"
            "Reflection: [detailed overall critique]\n"
            "Missing: [what important information or reasoning is missing]\n"
            "Superfluous: [what content is unnecessary or could be removed]\n"
            "Score (0-10): [your rating of the response quality]\n"
            "Found Solution (true/false): [whether this response fully solves the request]"
        ),
        description="Template for reflection prompt",
    )

    improvement_prompt_template: str = Field(
        default=(
            "You previously responded to a request, and received feedback on how to improve your response.\n\n"
            "Original request: {original_request}\n\n"
            "Your previous response: {response}\n\n"
            "Feedback: {feedback}\n\n"
            "Based on this feedback, provide an improved version of your response that addresses the critique."
            "Be sure to include all relevant information while removing anything unnecessary."
        ),
        description="Template for improvement prompt",
    )

    use_search: bool = Field(
        default=False,
        description="Whether to use search to gather additional information",
    )

    search_query_prompt_template: str = Field(
        default=(
            "Based on the feedback you received, generate 1-3 search queries that would help address "
            "the missing information in your response.\n\n"
            "Original request: {original_request}\n\n"
            "Your previous response: {response}\n\n"
            "Feedback: {feedback}\n\n"
            "Generate 1-3 specific search queries (one per line):"
        ),
        description="Template for generating search queries",
    )

    auto_accept_threshold: float | None = Field(
        default=0.8,
        description="If set, automatically accept responses with reflection score above this threshold",
    )


class ReflectionAgentConfig(SimpleAgentConfig):
    """Configuration for an agent that uses reflection to improve responses."""

    # Base configuration - inherit from SimpleAgentConfig
    state_schema: type[BaseModel] = Field(
        default=ReflectionAgentState,
        description="State schema for the reflection agent",
    )

    # Reflection-specific configuration
    reflection: ReflectionConfig = Field(
        default_factory=ReflectionConfig, description="Reflection configuration"
    )

    # Node names for the graph
    initial_node_name: str = Field(
        default="initial_response", description="Name of the initial response node"
    )

    reflection_node_name: str = Field(
        default="reflection", description="Name of the reflection node"
    )

    improvement_node_name: str = Field(
        default="improvement", description="Name of the improvement node"
    )

    evaluation_node_name: str = Field(
        default="evaluation", description="Name of the evaluation node"
    )

    search_node_name: str = Field(
        default="search", description="Name of the search node"
    )

    # Structured output models
    reflection_output_model: type[BaseModel] = Field(
        default=ReflectionResult, description="Model for structured reflection output"
    )

    agent_output_model: type[BaseModel] = Field(
        default=ReflectionOutput, description="Model for agent output"
    )

    @classmethod
    def from_aug_llm(
        cls,
        aug_llm: AugLLMConfig,
        name: str | None = None,
        system_prompt: str | None = None,
        **kwargs
    ) -> "ReflectionAgentConfig":
        """Create a ReflectionAgentConfig from an existing AugLLMConfig."""
        # First create a SimpleAgentConfig
        simple_config = SimpleAgentConfig.from_aug_llm(
            aug_llm=aug_llm, name=name, system_prompt=system_prompt
        )

        # Then extend it with reflection-specific config
        return cls(
            name=simple_config.name,
            engine=simple_config.engine,
            system_prompt=simple_config.system_prompt,
            **kwargs
        )

    @classmethod
    def from_scratch(
        cls,
        system_prompt: str | None = None,
        model: str = "gpt-4o",
        temperature: float = 0.7,
        name: str | None = None,
        **kwargs
    ) -> "ReflectionAgentConfig":
        """Create a ReflectionAgentConfig from scratch."""
        # First create a SimpleAgentConfig
        simple_config = SimpleAgentConfig.from_scratch(
            system_prompt=system_prompt, model=model, temperature=temperature, name=name
        )

        # Then extend it with reflection-specific config
        return cls(
            name=simple_config.name,
            engine=simple_config.engine,
            system_prompt=simple_config.system_prompt,
            **kwargs
        )
