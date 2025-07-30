"""Reflection agents using generic pre/post hook pattern."""

from typing import Any, Generic, TypeVar

from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.graph.node.message_transformation_v2 import (
    TransformationType,
)
from pydantic import BaseModel, Field

from haive.agents.base.agent import Agent
from haive.agents.multi.base.agent import MultiAgent
from haive.agents.react.agent import ReactAgent
from haive.agents.simple.agent import SimpleAgent
from haive.agents.structured import StructuredOutputAgent

from .models import ExpertiseConfig, GradingResult, ReflectionConfig
from .prompts import (
    GRADING_SYSTEM_PROMPT,
    REFLECTION_SYSTEM_PROMPT,
)

# Generic type variables for agents
TMainAgent = TypeVar("TMainAgent", bound=Agent)
TPreAgent = TypeVar("TPreAgent", bound=Agent)
TPostAgent = TypeVar("TPostAgent", bound=Agent)


class PrePostMultiAgent(MultiAgent, Generic[TPreAgent, TMainAgent, TPostAgent]):
    """Generic pre/post hook multi-agent pattern.

    This provides a general pattern for:
    - Pre-processing (optional)
    - Main processing
    - Post-processing (optional)

    With optional message transformation between stages.
    """

    # Agent configuration
    pre_agent: TPreAgent | None = Field(
        default=None, description="Pre-processing agent"
    )
    main_agent: TMainAgent = Field(..., description="Main processing agent")
    post_agent: TPostAgent | None = Field(
        default=None, description="Post-processing agent"
    )

    # Message transformation config
    use_pre_transform: bool = Field(
        default=False, description="Transform messages before main"
    )
    use_post_transform: bool = Field(
        default=False, description="Transform messages before post"
    )
    pre_transform_type: TransformationType = Field(
        default=TransformationType.AI_TO_HUMAN
    )
    post_transform_type: TransformationType = Field(
        default=TransformationType.REFLECTION
    )

    # Execution config
    skip_pre_if_empty: bool = Field(
        default=True, description="Skip pre-agent if no input"
    )
    skip_post_if_empty: bool = Field(
        default=False, description="Skip post-agent if no output"
    )

    def model_post_init(self, __context: Any) -> None:
        """Set up the agents list."""
        super().model_post_init(__context)

        # Build agents list
        agents_list = []

        if self.pre_agent:
            agents_list.append(self.pre_agent)

        agents_list.append(self.main_agent)

        if self.post_agent:
            agents_list.append(self.post_agent)

        self.agents = {agent.name: agent for agent in agents_list}


class StructuredOutputMultiAgent(
    PrePostMultiAgent[None, TMainAgent, StructuredOutputAgent]
):
    """Any agent followed by structured output extraction.

    This is the pattern we already have:
    - Main agent produces unstructured output
    - StructuredOutputAgent extracts structure
    """

    # Always have post agent for structured output
    post_agent: StructuredOutputAgent = Field(
        ..., description="Structured output extractor"
    )

    # No message transform needed for structured output
    use_post_transform: bool = Field(default=False)

    @classmethod
    def create(
        cls,
        main_agent: TMainAgent,
        output_model: type[BaseModel],
        name: str | None = None,
        **kwargs,
    ) -> "StructuredOutputMultiAgent":
        """Create with main agent and output model."""
        name = name or f"{main_agent.name}_structured"

        # Create structured output agent
        structurer = StructuredOutputAgent(
            name=f"{main_agent.name}_structurer",
            output_model=output_model,
            engine=main_agent.engine,  # Use same engine config
        )

        return cls(name=name, main_agent=main_agent, post_agent=structurer, **kwargs)


class ReflectionMultiAgent(PrePostMultiAgent[None, TMainAgent, SimpleAgent]):
    """Any agent with reflection post-processing.

    Pattern:
    1. Main agent responds
    2. Message transform (AI → Human)
    3. Reflection agent improves response
    """

    # Reflection agent for post-processing
    post_agent: SimpleAgent = Field(..., description="Reflection agent")

    # Always use reflection transform
    use_post_transform: bool = Field(default=True)
    post_transform_type: TransformationType = Field(
        default=TransformationType.REFLECTION
    )

    # Reflection config
    reflection_config: ReflectionConfig = Field(default_factory=ReflectionConfig)

    @classmethod
    def create(
        cls,
        main_agent: TMainAgent,
        name: str | None = None,
        reflection_system_prompt: str = REFLECTION_SYSTEM_PROMPT,
        **kwargs,
    ) -> "ReflectionMultiAgent":
        """Create reflection multi-agent."""
        name = name or f"{main_agent.name}_with_reflection"

        # Create reflection agent
        reflector = SimpleAgent(
            name=f"{main_agent.name}_reflector",
            engine=AugLLMConfig(
                system_message=reflection_system_prompt,
                temperature=0.3,  # Lower temp for consistent improvement
            ),
        )

        return cls(name=name, main_agent=main_agent, post_agent=reflector, **kwargs)


class GradedReflectionMultiAgent(
    PrePostMultiAgent[SimpleAgent, TMainAgent, SimpleAgent]
):
    """Grade → Main → Reflect pattern.

    Pattern:
    1. Main agent responds
    2. Grading agent evaluates (with structured output)
    3. Message transform for reflection
    4. Reflection agent improves based on grade
    """

    # Pre-agent for grading
    pre_agent: SimpleAgent = Field(..., description="Grading agent")

    # Post-agent for reflection
    post_agent: SimpleAgent = Field(..., description="Reflection agent")

    # Transform for reflection
    use_post_transform: bool = Field(default=True)
    post_transform_type: TransformationType = Field(
        default=TransformationType.REFLECTION
    )

    # Grading output model
    grading_model: type[BaseModel] = Field(default=GradingResult)

    @classmethod
    def create(
        cls,
        main_agent: TMainAgent,
        name: str | None = None,
        grading_system_prompt: str = GRADING_SYSTEM_PROMPT,
        reflection_system_prompt: str = REFLECTION_SYSTEM_PROMPT,
        **kwargs,
    ) -> "GradedReflectionMultiAgent":
        """Create graded reflection multi-agent."""
        name = name or f"{main_agent.name}_graded_reflection"

        # Create grading agent with structured output
        grader = SimpleAgent(
            name=f"{main_agent.name}_grader",
            engine=AugLLMConfig(
                system_message=grading_system_prompt,
                temperature=0.1,  # Very low for consistent grading
            ),
            structured_output_model=GradingResult,
        )

        # Create reflection agent
        reflector = SimpleAgent(
            name=f"{main_agent.name}_reflector",
            engine=AugLLMConfig(
                system_message=reflection_system_prompt, temperature=0.3
            ),
        )

        return cls(
            name=name,
            pre_agent=grader,
            main_agent=main_agent,
            post_agent=reflector,
            **kwargs,
        )


# Specific agent implementations


class ReflectionAgent(SimpleAgent):
    """Simple reflection agent for improving responses."""

    reflection_mode: str = Field(
        default="improve", description="Mode: improve, critique, or both"
    )

    def model_post_init(self, __context: Any) -> None:
        """Set up reflection prompt."""
        super().model_post_init(__context)

        if not self.engine.system_message:
            self.engine.system_message = REFLECTION_SYSTEM_PROMPT


class GradingAgent(SimpleAgent):
    """Agent that grades responses with structured output."""

    structured_output_model: type[BaseModel] = Field(default=GradingResult)
    structured_output_version: str = Field(default="v2")

    def model_post_init(self, __context: Any) -> None:
        """Set up grading configuration."""
        super().model_post_init(__context)

        if not self.engine.system_message:
            self.engine.system_message = GRADING_SYSTEM_PROMPT


class ExpertAgent(SimpleAgent):
    """Agent with configurable expertise."""

    expertise_config: ExpertiseConfig = Field(..., description="Expert configuration")

    def model_post_init(self, __context: Any) -> None:
        """Set up expert prompt from config."""
        super().model_post_init(__context)

        # Build system prompt from expertise config
        self.engine.system_message = self.expertise_config.to_prompt()


class ToolBasedReflectionAgent(ReactAgent):
    """Reflection agent that uses tools to cite improvements.

    Similar to LangChain's reflexion but more flexible.
    """

    reflection_mode: str = Field(default="improve_with_citations")
    require_citations: bool = Field(default=True)

    def model_post_init(self, __context: Any) -> None:
        """Set up tool-based reflection."""
        super().model_post_init(__context)

        if not self.engine.system_message:
            self.engine.system_message = (
                REFLECTION_SYSTEM_PROMPT
                + "\n\nWhen suggesting improvements, use available tools to "
                "cite sources or verify information."
            )


# Factory functions


def create_reflection_agent(
    name: str = "reflector", engine: AugLLMConfig | None = None, **kwargs
) -> ReflectionAgent:
    """Create a simple reflection agent."""
    if not engine:
        engine = AugLLMConfig(system_message=REFLECTION_SYSTEM_PROMPT, temperature=0.3)

    return ReflectionAgent(name=name, engine=engine, **kwargs)


def create_graded_reflection_agent(
    name: str = "graded_reflector", main_agent: Agent | None = None, **kwargs
) -> GradingAgent | GradedReflectionMultiAgent:
    """Create grading agent or full graded reflection system."""
    if main_agent:
        return GradedReflectionMultiAgent.create(
            main_agent=main_agent, name=name, **kwargs
        )
    # Just return grading agent
    return GradingAgent(
        name=name,
        engine=AugLLMConfig(system_message=GRADING_SYSTEM_PROMPT, temperature=0.1),
        **kwargs,
    )


def create_expert_agent(
    name: str, domain: str, expertise_level: str = "expert", **kwargs
) -> ExpertAgent:
    """Create an expert agent."""
    expertise_config = ExpertiseConfig(
        domain=domain, expertise_level=expertise_level, **kwargs
    )

    return ExpertAgent(
        name=name,
        expertise_config=expertise_config,
        engine=AugLLMConfig(temperature=0.7),
    )


def create_tool_based_reflection_agent(
    name: str = "tool_reflector", tools: list | None = None, **kwargs
) -> ToolBasedReflectionAgent:
    """Create tool-based reflection agent."""
    return ToolBasedReflectionAgent(
        name=name, engine=AugLLMConfig(temperature=0.3), tools=tools or [], **kwargs
    )
